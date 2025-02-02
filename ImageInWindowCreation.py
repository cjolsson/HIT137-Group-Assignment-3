import breezypythongui as bpg
from   breezypythongui import EasyFrame
import cv2 #OpenCV
import numpy as np
import os
#import requests
import matplotlib.pyplot as plt
from   matplotlib.colors import LogNorm
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import pandas as pd
import tkinter as tk
#from   tkinter.font import Font
from   tkinter import filedialog, messagebox
#from   pylab import rcParams
from   PIL import Image, ImageTk

class ImageDemo(EasyFrame): #Set up the window
    def __init__(self):
        EasyFrame.__init__(self, title = "Demonstrate Image Handling", width = 400, height = 400, background = "white")
        self.setResizable(True)  

        self.image_label = tk.Label(self) #Image label
        self.image_label.pack(side = tk.TOP, pady = 5)

        self.load_button()
#==================================================================================================================================================       
    def load_button(self): #Create the load button
    
        load_button = tk.Button(self, text="Select Image", command=self.load_image)
        load_button.pack(side=tk.TOP, pady=5)
#================================================================================================================================================== 
    def load_image(self): #Find and display the image.

        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])

        if file_path:

            file_path = os.path.normpath(file_path) #Normalise the file path avoiding slashes and spaces

            try:
                self.image_Original = Image.open(file_path) #Check to ensure file path is usable
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return

#       Create and display the image
        self.image_Copy = self.image_Original.copy()
        self.image_Copy.thumbnail((300, 300))  # Size image
        self.image_Display = ImageTk.PhotoImage(self.image_Copy) #Display the image

        self.image_label.config(image=self.image_Display) #Display the image on the label

        self.image_label.image = self.image_Display  # Keep a reference to avoid garbage collection      
#==================================================================================================================================================

def main():
    ImageDemo().mainloop()

if __name__ == "__main__":
    main()