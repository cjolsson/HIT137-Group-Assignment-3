""" In Git Bash run, pip install BreezyPythonGUI """
from breezypythongui import EasyFrame
from tkinter.font import Font
import tkinter as tk
"""In Git Bash run, pip install pillow"""
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os

"""Set up the window"""
class ImageDemo(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="Image Demo")
        self.setResizable(True)  

        """Label to display the image"""
        self.image_label = tk.Label(self)
        self.image_label.pack(side = tk.TOP, pady = 5)

        self.load_button()
        

        """Load the image. """
    
    def load_button(self):
        """Create the load button"""
        load_button = tk.Button(self, text="Load Image", command=self.load_image)
        load_button.pack(side=tk.TOP, pady=5)

    def load_image(self):
        """File path made normal, avoiding slashes and spaces"""
        file_path = filedialog.askopenfilename(
            title="Select an Image", 
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])

         if file_path:
            """ Remove any characters not needed"""
            file_path = os.path.normpath(file_path)


            """Check to ensure file path is usable"""
            try:
                self.original_image = Image.open(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return

            """Create the image and display it"""
            self.thumbnail_image = self.original_image.copy()
            self.thumbnail_image.thumbnail((200, 200))  # Resize image
            self.display_image = ImageTk.PhotoImage(self.thumbnail_image)

            """Display image on the lavbel"""
            self.image_label.config(image=self.display_image)

            self.image_label.image = self.display_image  # Keep a reference to avoid garbage collection      

    
def main():
    ImageDemo().mainloop()

if __name__ == "__main__":
    main()