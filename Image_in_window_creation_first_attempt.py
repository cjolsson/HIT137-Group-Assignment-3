
"""Set up the window"""
class ImageDemo(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="Image Demo")
        self.setResizable(True)  
        

        """Load the image. Pillow library used here"""
        image = Image.open("cube-14564_256.gif")  ## file path

        """Resize the image to a smaller size""" 
        # image = image.resize((300, 300), Image.Resampling.LANCZOS)  
        # image = image.rotate(-90)

        """Convert the resized image to Tkinter format"""
        # self.image = ImageTk.PhotoImage(image)

        """Add image label"""
        imageLabel = self.addLabel(text="", row=0, column=0, sticky="NSEW")
        imageLabel["image"] = self.image  

        """Add text label"""
        textLabel = self.addLabel(text="Cube", row=1, column=0, sticky="NSEW")

        """font for the text label"""
        font = Font(family="Verdana", size=20, slant="italic")
        textLabel["font"] = font
        textLabel["foreground"] = "blue"  

def main():
    ImageDemo().mainloop()

if __name__ == "__main__":
    main()