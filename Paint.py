
import cv2  # OpenCV
import numpy as np
import os
import tkinter as tk
from   tkinter import filedialog, messagebox, colorchooser
from   PIL     import Image, ImageTk, ImageOps, ImageDraw
import breezypythongui as bpg
from   breezypythongui import EasyFrame
class ImageDemo(EasyFrame):  # Set up the window
    def __init__(self):
        EasyFrame.__init__(self, title="Demonstrate Image Handling", width=1200, height=700, resizable = False, background="white")
        
        self.rectangle = self.start_x = self.start_y = self.end_x = self.end_y = None
        self.image_loaded = self.drawing = False
        self.undo_stack = self.redo_stack = []
        self.working_image = self.working_image_id = None
        self.draw_color = "black"
        
        self.create_buttons()
        
        self.bind_canvas_events(self.on_button_press, self.on_mouse_drag, self.on_button_release)
        self.bind_all("<Alt-l>"    , self.load_image)
        self.bind_all("<Alt-e>"    , self.enable_crop)
        self.bind_all("<Alt-r>"    , self.rotate_image)
        self.bind_all("<Alt-i>"    , self.invert_image)
        self.bind_all("<Alt-g>"    , self.convert_to_grey)
        self.bind_all("<Alt-d>"    , self.enable_draw)
        self.bind_all("<Alt-c>"    , self.select_colour)
        self.bind_all("<Control-s>", self.save_image)
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)
 
    def create_buttons(self):
        button_frame = tk.Frame(self)  # Create a frame for buttons
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)  # Place at the top  
        buttons = [
            ("Select Image\n<Alt+l>"         , self.load_image),
            ("Crop Image\n<Alt+e>"           , self.enable_crop),
            ("Rotate Image\n<Alt+r>"         , self.rotate_image),
            ("Invert Image\n<Alt+i>"         , self.invert_image),
            ("Grey Scale\n<Alt+g>"           , self.convert_to_grey),
            ("Draw on Image\n<Alt+d>"        , self.enable_draw),
            ("Select Drawing Colour\n<Alt+c>", self.select_colour),
            ("Save Image\nCtrl+s"            , self.save_image),
            ("Undo ↩\nCtrl+z"               , self.undo),
            ("Redo ↪\nCtrl+y"               , self.redo)
        ]   
        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)
        # Insert resizing slider
        self.slider = tk.Scale(button_frame, from_=1, to=600, orient=tk.HORIZONTAL, command=self.resize_image, label="Resize Image")
        self.slider.set(300)
        self.slider.pack(side=tk.LEFT, padx=5)
        # Insert Image label
        label_frame = tk.Frame(self)
        label_frame.pack(side=tk.TOP, fill=tk.X, pady=5)    
        self.image_label = tk.Label(label_frame, text="No image loaded")  # Image label
        self.image_label.pack(side=tk.LEFT, pady=5)
        # Insert working canvas
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, width=1200, height=600)
        self.canvas.pack(pady=5)

    def bind_canvas_events(self, press, drag, release): # Centralise binding operations
        self.canvas.bind("<ButtonPress-1>", press)
        self.canvas.bind("<B1-Motion>", drag)
        self.canvas.bind("<ButtonRelease-1>", release)

    def load_image(self, event=None):  # Find and display the image.
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
        if file_path:
            file_path = os.path.normpath(file_path)  # Normalize the file path avoiding slashes and spaces
            try:
                self.image_Original = Image.open(file_path)  # Check to ensure file path is usable
                self.image_loaded = True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return
            # Extract image label
            self.image_label.config(text=f"Loaded Image: {file_path.split('/')[-1]}")
            # Create and display the image
            self.image_Copy = self.image_Original.copy()
            self.image_Copy.thumbnail((600, 600))  # Size image to fit canvas
            self.image_Copy_tk = ImageTk.PhotoImage(self.image_Copy)  # Display the image
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_Copy_tk)  # Display the image on the canvas
            self.canvas.image = self.image_Copy_tk  # Keep a reference to avoid garbage collection
            
    def enable_crop(self, event=None):
        if not self.image_loaded:
            messagebox.showerror("Error", "Please load an image first.")
        else:
            self.drawing = False
            self.bind_canvas_events(self.on_button_press, self.on_mouse_drag, self.on_button_release)

    def on_button_press(self, event):
        if self.drawing:
            self.last_x, self.last_y = event.x - 610, event.y
        else:
            self.start_x = event.x
            self.start_y = event.y
            self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        if self.drawing:
            self.draw_on_image(event.x - 610, event.y)
        else:
            cur_x, cur_y = (event.x, event.y)
            self.canvas.coords(self.rectangle, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        if not self.drawing:
            self.end_x, self.end_y = (event.x, event.y)
            self.crop_image()

    def crop_image(self, event=None):
        if self.rectangle:
            self.canvas.delete(self.rectangle)
            self.rectangle = None
        if self.start_x and self.start_y and self.end_x and self.end_y: # Has a cropped image been drawn?
            
            x1, y1, x2, y2 = min(self.start_x, self.end_x), min(self.start_y, self.end_y), max(self.start_x, self.end_x), max(self.start_y, self.end_y) # Adjust coordinates to match the image dimensions            
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(self.image_Copy.width, x2), min(self.image_Copy.height, y2) # Ensure coordinates are within the image bounds
            
            self.working_image = self.image_Copy.crop((x1, y1, x2, y2)) # Crop to coordinates and display
            self.display_image()
            
            self.undo_stack = self.redo_stack = [] # Clear the undo and redo stacks when a new cropped image is created
            self.start_x = self.start_y = self.end_x = self.end_y = None # Stop error from occurring if user clicks outside of image
            
    def display_image(self, event=None):
        
        self.undo_stack.append(self.working_image) # Save state for undo
        self.working_image_tk = ImageTk.PhotoImage(self.working_image) # Create tkinter object
        self.canvas.delete(self.working_image_id) # Deletes existing image on canvas
        self.working_image_id = self.canvas.create_image(610, 0, anchor="nw", image=self.working_image_tk) # Displays new image on canvas
        
        print("undo 0 " + len(self.undo_stack))
            
    def resize_image(self, value):
        if self.image_loaded: 
            if not self.working_image_id:
                messagebox.showerror("Error", "Please crop an image first.")
            else:
                width, height = self.working_image.size #retrieve dimensions of working image
                new_width = int(value) #retrieve resize slider value
                resize_scale = float(new_width/width) # compute scale to keep aspect ratio when resizing
                new_height = round(height*resize_scale) 
                self.working_image = self.working_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.display_image()
            
    def rotate_image(self, event=None):   
        if not self.working_image_id:
            messagebox.showerror("Error", "Please crop an image first.")
        else:
            self.working_image = self.working_image.rotate(90, expand=True) 
            self.display_image()  
            
    def invert_image(self, event=None):
        if not self.working_image_id:
            messagebox.showerror("Error", "Please crop an image first.")
        else:
            self.working_image = ImageOps.invert(self.working_image.convert('RGB'))
            self.display_image() 
            
    def convert_to_grey(self, event=None):
        if not self.working_image_id:
            messagebox.showerror("Error", "Please crop an image first.")
        else:   
            self.grey_image_cv = np.array(self.working_image) #convert PIL to OPENCV object
            self.grey_image_cv = cv2.cvtColor(self.grey_image_cv, cv2.COLOR_RGB2BGR) 
            self.grey_image_cv = cv2.cvtColor(self.grey_image_cv, cv2.COLOR_BGR2GRAY)
            self.grey_image_cv = cv2.cvtColor(self.grey_image_cv, cv2.COLOR_GRAY2RGB) # convert back to RGB
            self.working_image = Image.fromarray(self.grey_image_cv)  # convert back to PIL object
            self.display_image()

    def undo(self, event=None):
        
        if len(self.undo_stack) > 1: # The undo_stack should always have at least one image saved i.e. the original clipped image
            
            self.redo_stack.append(self.undo_stack.pop()) # Save the current image into the redo list
            
            self.working_image = self.undo_stack.pop() # Retrieve the penultimate saved image
            print("len undo 1 " + str(len(self.undo_stack)))
            print("len redo 1 " + str(len(self.redo_stack)))
            
            self.display_image() # Display the penultimate saved image
            
        else:
            
            messagebox.showerror("Error", "No undo steps available.")
            
    def redo(self, event=None):
        
        if len(self.redo_stack) > 0:
            
            self.working_image = self.redo_stack.pop()
            print("len redo 2 " + str(len(self.redo_stack)))
            self.display_image()
            
        else:
            
            messagebox.showerror("Error", "No redo steps available.")

    def save_image(self, event=None):
        
        if not self.working_image_id:
            
            messagebox.showerror("Error", "Please crop an image first.")
            
        else:
            
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            
            if save_path:
                
                self.working_image.save(save_path)

    def enable_draw(self, event=None):
        
        if not self.working_image_id:
            
            messagebox.showerror("Error", "Please crop an image first.")
        else:
            
            self.drawing = True
            self.bind_canvas_events(self.on_button_press, self.on_mouse_drag, self.on_button_release)
        
    def select_colour(self, event=None):
        
        self.draw_color = colorchooser.askcolor(color=self.draw_color)[1]

    def draw_on_image(self, x, y, event=None):
        
        if not self.working_image_id:
            
            messagebox.showerror("Error", "Please crop an image first.")
            
        else:
            
            draw = ImageDraw.Draw(self.working_image)
            draw.line([self.last_x, self.last_y, x, y], fill=self.draw_color, width=5)
            self.last_x, self.last_y = x, y
            self.display_image()
                    
def main():
    app = ImageDemo()
    app.mainloop()

if __name__ == "__main__":
    main()