import breezypythongui as bpg
from breezypythongui import EasyFrame

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.colors import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog, messagebox
from pylab import rcParams
from PIL import Image, ImageTk

class ImageDemo(EasyFrame): #Set up the window
    def __init__(self):
        EasyFrame.__init__(self, title="Image Demo")
        self.setResizable(True)  

        self.image_label = tk.Label(self) #Image label
        self.image_label.pack(side = tk.TOP, pady = 5)

        self.load_button()
        
    def load_button(self): #Create the load button
    
        load_button = tk.Button(self, text="Load Image", command=self.load_image)
        load_button.pack(side=tk.TOP, pady=5)

    def load_image(self): #Find and display the image.

        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])

        if file_path:

            file_path = os.path.normpath(file_path) #Normalise the file path avoiding slashes and spaces

            try:
                self.original_image = Image.open(file_path) #Check to ensure file path is usable
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return

#           Create and display the image
            self.thumbnail_image = self.original_image.copy()
            self.thumbnail_image.thumbnail((200, 200))  # Resize image
            self.display_image = ImageTk.PhotoImage(self.thumbnail_image)

            self.image_label.config(image=self.display_image) #Display the image on the label

            self.image_label.image = self.display_image  # Keep a reference to avoid garbage collection      

def main():
    ImageDemo().mainloop()

if __name__ == "__main__":
    main()
