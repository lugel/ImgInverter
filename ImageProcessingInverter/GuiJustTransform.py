import tkinter as tk
from PIL import ImageTk, Image
from PIL.ImageFilter import numpy
from tkinter import filedialog
from Config import Config
from ImageTransformer import ImageTransformer
from Transformation import Transformation

class GuiJustTransform():
    #Default constructor
    def __init__(self, config:Config):
        self.config = Config("config.ini")
        self.transformer = ImageTransformer(self.config)
        self.transfList = ['NON']
        self.buildMainWindow()
        return None

    #opens photo and saves it to the self.original variable
    def open_image(self):
        tmp = self.openfilename() 

        try:
            self.original = Image.open(tmp)
            print("User has chosen " + tmp + " as base image")
        except AttributeError:
            print("User didn't choose an image")
            return None

        self.show_img(self.base, self.original, 0, 1, 4)
        return None

    #saves photo with given name
    def savePhoto(self):
        filename = filedialog.asksaveasfilename(title = "save", defaultextension = ".jpg", filetypes = (("jpg files","*.jpg"),("all files","*.*")))
        try:
            self.original.save(filename)
            print("Photo saved")
        except ValueError:
            print("File not saved")
        except AttributeError:
            print("User has not chosen an image to save")
        return None

    #opens file with given filename
    def openfilename(self):
        filename = filedialog.askopenfilename(title ="open") 
        return filename

    #shows image - curWindow -> current tk window | r,c -> row and column | rSpan -> row span
    def show_img(self, curWindow:tk, img:Image, r ,c, rSpan=1):
        img = img.copy()
        imgToShow = img.resize((250, 250))
        imgToShow = ImageTk.PhotoImage(imgToShow) 
        panel = tk.Label(curWindow, image = imgToShow)
        panel.image = imgToShow 
        panel.grid(row = r, column = c, rowspan = rSpan)
        return None

    #prints list of available transformations to the app window - window -> app window | transfList -> list of transformations | r -> row | c -> column
    def showAvailableTransformations(self, window:tk, transfList:list, r, c):
        availableTransf = "List of available transformations:\n\n"
        for count,transformation in enumerate(transfList):
            availableTransf += transformation.GetCode()
            availableTransf += " "
            if count == 3:
                availableTransf += "\n"
        availableTransf += "\n\nEnter any number of them below,\nseparated by space (' ') and press\n 'Transform image'\nto perform written transformations" 
        textToWindow = tk.Label(window, text = availableTransf)
        textToWindow.grid(row=r, column=c)
        return None

    #transforms image based on user's input
    def transformImage(self):
        tmplist = self.retrieve_input()
        try:
            arraytmp = numpy.array(self.original)
            for element in tmplist:
                arraytmp = self.transformer.GetTransformationByCode(element).Transform(arraytmp)
        
            self.original = Image.fromarray(arraytmp)
            self.show_img(self.base, self.original, 0, 1, 4)
        except AttributeError:
            print("User has not chosen an image to transform or provide bad input string")
       
        return None

    #reads user's input
    def retrieve_input(self):
        userInput = self.enterText.get()
        userInput = userInput.upper()
        transfList = userInput.split()
        availList = []
        for x in self.transformer.transformations:
            availList.append(x.GetCode())
        transfList = [i for i in transfList if i in availList]
        self.enterText.delete(0, 99)
        return transfList

    #exits the application
    def finish(self):
        self.base.destroy()

    #shows main menu window
    def buildMainWindow(self):
        self.base = tk.Toplevel()
        self.base.title("Image processing inverter - transformator")

        btnPickImage = tk.Button(self.base, text ="Pick image to transform", command = lambda : self.open_image()).grid(row = 4, column = 1)
        btnTransform = tk.Button(self.base, text ="Transform image", command = lambda : self.transformImage()).grid(row = 2, column = 0) 
        btnSave = tk.Button(self.base, text = "Save image", command = lambda : self.savePhoto()).grid(row = 3, column = 0)
        btnFinish = tk.Button(self.base, text ="Close", command = lambda : self.finish()).grid(row = 4, column = 0)

        self.showAvailableTransformations(self.base, self.transformer.transformations, 0, 0)
        self.enterText = tk.Entry(self.base)
        self.enterText.grid(row = 1, column = 0, sticky = "WE")

        self.base.grid_columnconfigure(1, minsize = 255)
        self.base.grid_rowconfigure(0, minsize = 135)
        self.base.grid_rowconfigure(1, minsize = 40)
        self.base.grid_rowconfigure(2, minsize = 40)
        self.base.grid_rowconfigure(3, minsize = 40)
        self.base.resizable(False, False)
        self.base.mainloop()
        return None