import breezypythongui as bpg
"""Ensure to install pip install breezypythongui in git bash"""
from breezypythongui import EasyFrame
import cv2  # OpenCV
"""Ensure to install pip install opencv-python in git bash"""
import numpy as np
import os
import matplotlib.pyplot as plt
"""Ensure to install pip install matplotlib in git bash"""
from matplotlib.colors import LogNorm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
"""Ensure to install pip install tk in git bash"""
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageGrab, ImageDraw

class ImageDemo(EasyFrame):  # Set up the window
    def __init__(self):
        EasyFrame.__init__(self, title="Demonstrate Image Handling", width=1200, height=800, background="white")
        self.setResizable(True)

        self.load_button()
        self.crop_button()
        self.resize_slider()
        self.rotate_button()
        self.save_button()
        self.invert_button()
        self.greyscale_button()
        self.draw_button()
        self.color_button()
        self.canvas = tk.Canvas(self, width=1200, height=600)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.cropped_image = None
        self.image_loaded = False
        self.undo_stack = []
        self.redo_stack = []
        self.drawing = False
        self.draw_color = "black"
        self.working_image = None
        self.working_image_id = None
        self.grey_image = None
        
    def load_button(self):  # Create the load button
        load_button = tk.Button(self, text="Select Image", command=self.load_image)
        self.image_label = tk.Label(self)  # Image label
        self.image_label.pack(side=tk.TOP, pady=5)
        load_button.pack(side=tk.TOP, pady=5)

    def crop_button(self):  # Create the crop button
        crop_button = tk.Button(self, text="Crop Image", command=self.enable_crop)
        crop_button.pack(side=tk.TOP, pady=5)

    def resize_slider(self):  # Create the resize slider
        self.slider = tk.Scale(self, from_=1, to=600, orient=tk.HORIZONTAL, command=self.resize_image)
        self.slider.set(300)  # Set default value to 300
        self.slider.pack(side=tk.TOP, pady=5)

    def rotate_button(self):  # Create the rotate button
        rotate_button = tk.Button(self, text="Rotate", command=self.rotate_image)
        rotate_button.pack(side=tk.TOP, pady=5)

    def save_button(self):  # Create the save button
        save_button = tk.Button(self, text="Save Image", command=self.save_image)
        save_button.pack(side=tk.TOP, pady=5)

    def invert_button(self):  # Create the invert button
        invert_button = tk.Button(self, text="Invert Image", command=self.invert_image)
        invert_button.pack(side=tk.TOP, pady=5)
        
    def greyscale_button(self):
        grey_button = tk.Button(self, text="Grey Scale", command=self.convert_to_grey)
        grey_button.pack(side=tk.TOP, pady=5)

    def draw_button(self):  # Create the draw button
        draw_button = tk.Button(self, text="Draw on Image", command=self.enable_draw)
        draw_button.pack(side=tk.TOP, pady=5)

    def color_button(self):  # Create the color button
        color_button = tk.Button(self, text="Select Color", command=self.select_color)
        color_button.pack(side=tk.TOP, pady=5)

    def load_image(self):  # Find and display the image.
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
        if file_path:
            file_path = os.path.normpath(file_path)  # Normalize the file path avoiding slashes and spaces
            try:
                self.image_Original = Image.open(file_path)  # Check to ensure file path is usable
                print(f"Image loaded successfully: {file_path}")  # Debug statement
                self.image_loaded = True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return
            # Extract image label
            self.image_label.config(text=f"Loaded Image: {file_path.split('/')[-1]}")
            # Create and display the image
            self.image_Copy = self.image_Original.copy()
            self.image_Copy.thumbnail((600, 600))  # Size image to fit canvas
            self.image_Display = ImageTk.PhotoImage(self.image_Copy)  # Display the image

            self.canvas.create_image(0, 0, anchor="nw", image=self.image_Display)  # Display the image on the canvas
            self.canvas.image = self.image_Display  # Keep a reference to avoid garbage collection
            print("Image displayed successfully")  # Debug statement
            print(type(self.working_image))

    def enable_crop(self):
        if self.image_loaded:
            self.drawing = False
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        else:
            messagebox.showerror("Error", "Please load an image first.")

    def on_button_press(self, event):
        if self.drawing:
            self.last_x, self.last_y = event.x - 610, event.y
        else:
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        if self.drawing:
            self.draw_on_image(event.x - 610, event.y)
        else:
            cur_x, cur_y = (event.x, event.y)
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        if not self.drawing:
            self.end_x, self.end_y = (event.x, event.y)
            self.crop_image()

    def crop_image(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        if self.start_x and self.start_y and self.end_x and self.end_y:
            # Adjust coordinates to match the image dimensions
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)

            # Ensure coordinates are within the image bounds
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(self.image_Copy.width, x2)
            y2 = min(self.image_Copy.height, y2)
            
            
            self.working_image = self.image_Copy.crop((x1, y1, x2, y2))
            self.cropped_image = ImageTk.PhotoImage(self.working_image)
            if self.working_image_id:
                self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.cropped_image)  # Display cropped image next to original
            self.undo_stack.append(self.working_image.copy())  # Save state for undo

    def resize_image(self, value):
        if self.working_image_id:
            width, height = self.working_image.size #retrieve dimensions of working image
            new_width = int(value) #retrieve resize slider value
            resize_scale = float(new_width/width)
            new_height = round(height*resize_scale)
            self.working_image = self.working_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.resized_image = ImageTk.PhotoImage(self.working_image)
            self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.resized_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo

    def rotate_image(self):   
        if self.working_image_id:
            self.working_image = self.working_image.rotate(90, expand=True) 
            # convert the PIL image to a Tkinter PhotoImage and display it on the canvas
            self.rotated_image = ImageTk.PhotoImage(self.working_image)
            self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.rotated_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo
        
    def invert_image(self):
        if self.working_image_id:
            self.working_image = ImageOps.invert(self.working_image.convert('RGB'))
            self.inverted_image = ImageTk.PhotoImage(self.working_image)
            self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.inverted_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo
    
    def convert_to_grey(self):
        if self.working_image_id:    
            self.grey_image = np.array(self.working_image) #convert PIL to OPENCV object
            self.grey_image = cv2.cvtColor(self.grey_image, cv2.COLOR_RGB2BGR) 
            self.grey_image = cv2.cvtColor(self.grey_image, cv2.COLOR_BGR2GRAY)
            self.working_image = Image.fromarray(self.grey_image)  # convert back to PIL object
            self.grey_image = ImageTk.PhotoImage(self.working_image) # conver to Tkinter for canvas display
            self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.grey_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo

    def undo(self, event=None):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            if self.undo_stack:
                self.working_image = self.undo_stack[-1]
                self.undo_image = ImageTk.PhotoImage(self.working_image)
                if self.working_image_id:
                    self.canvas.delete(self.working_image_id)
                self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.undo_image)

    def redo(self, event=None):
        if self.redo_stack:
            self.working_image = self.redo_stack.pop()
            self.redo_image = ImageTk.PhotoImage(self.working_image)
            if self.working_image_id:
                self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.redo_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo

    def save_image(self):
        if self.working_image_id:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                self.working_image.save(save_path)

    def enable_draw(self):
        if self.working_image_id:
            self.drawing = True
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        else:
            messagebox.showerror("Error", "Please crop an image first.")

    def select_color(self):
        self.draw_color = colorchooser.askcolor(color=self.draw_color)[1]

    def draw_on_image(self, x, y):
        if self.working_image_id:
            draw = ImageDraw.Draw(self.working_image)
            draw.line([self.last_x, self.last_y, x, y], fill=self.draw_color, width=5)
            self.last_x, self.last_y = x, y
            self.drawn_image = ImageTk.PhotoImage(self.working_image)
            self.canvas.delete(self.working_image_id)
            self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.drawn_image)
            self.undo_stack.append(self.working_image.copy())  # Save state for undo

def main():
    app = ImageDemo()
    app.mainloop()

if __name__ == "__main__":
    main()