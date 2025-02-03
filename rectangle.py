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

ix, iy = -1, -1
drawing = False

def draw_Rectangle(event, x, y, flags, param):

    global ix, iy, drawing, img

    if   event == cv2.EVENT_LBUTTONDOWN:

        drawing = True
        ix = x
        iy = y			 

    elif event == cv2.EVENT_MOUSEMOVE:
    
        if drawing:

            cv2.rectangle(img, pt1 =(ix, iy), pt2 =(x, y), color =(0, 255, 255), thickness = -1)

    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False
        cv2.rectangle(img, pt1 =(ix, iy), pt2 =(x, y), color =(0, 255, 255), thickness = 2)
    
img = np.zeros((512, 700 ,3), np.uint8) # Create a black image

cv2.namedWindow("Title of Popup Window", flags = cv2.WINDOW_GUI_EXPANDED) # Display a window the size of which can be manually changed

cv2.setMouseCallback("Title of Popup Window", draw_Rectangle) # Connect the mouse button to our callback function
                
while True:

    cv2.imshow("Title of Popup Window", img) # Display the image
    
    if cv2.waitKey(10) & 0xFF == 27: # Break the loop when the Esc key is pressed
        break

cv2.destroyAllWindows() # Close all windows