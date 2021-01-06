import tkinter as tk
from PIL import ImageTk, Image
import keras
import os
from PIL.ImageFilter import numpy
from ImagePreprocessor import ImagePreprocessor
from Config import Config
from tkinter import filedialog
from ImageTransformer import ImageTransformer
from Transformation import Transformation
from AImodel import AImodel
from GuiJustTransform import GuiJustTransform
import time

class GuiMainMenu(object):
    #Default constructor
    def __init__(self, config:Config):
        self.config = Config("config.ini")
        self.transformer = ImageTransformer(self.config)
        self.preprocessor = ImagePreprocessor(self.config)
        self.aiModel = AImodel()

        self.buildMainWindow()
        return None


    #opens photo and saves it to the self.original variable
    def open_org(self):
        tmp = self.openfilename() 

        try:
            self.original = Image.open(tmp)
            print("User has chosen " + tmp + " as base image")
        except AttributeError:
            print("User didn't choose an image")
            return None

        self.show_img(self.root, self.original, 1, 0, 1, 2)
        return None

    #opens photo and saves it to the self.transformed variable
    def open_tran(self):
        tmp = self.openfilename() 

        try:
            self.transformed = Image.open(tmp)
            print("User has chosen " + tmp + " as transformed image")
        except AttributeError:
            print("User didn't choose an image")
            return None

        self.show_img(self.root, self.transformed, 1, 2)
        return None

    #opens photo and saves it to the self.toProcess variable also copies to self.processed variable
    def open_toProcess(self):
        tmp = self.openfilename() 

        try:
            self.toProcess = Image.open(tmp)
            self.processed = self.toProcess.copy()
            print("User has chosen " + tmp + " to process")
        except AttributeError:
            print("User didn't choose an image")
            return None

        self.show_img(self.process, self.toProcess, 0, 1, 3)
        return None

    #opens file with given filename
    def openfilename(self):
        filename = filedialog.askopenfilename(title ="open") 
        return filename

    #saves photo with given name
    def savePhoto(self):
        filename = filedialog.asksaveasfilename(title = "save", defaultextension = ".jpg", filetypes = (("jpg files","*.jpg"),("all files","*.*")))
        try:
            self.processed.save(filename)
            print("Photo saved")
        except ValueError:
            print("File not saved")
        except AttributeError:
            print("User has not chosen an image to save")
        return None

    #shows image - curWindow -> current tk window | r,c -> row and column | rSpan -> row span
    def show_img(self, curWindow:tk, img:Image, r ,c, rSpan=1, cSpan=1):
        img = img.copy()
        imgToShow = img.resize((250, 250))
        imgToShow = ImageTk.PhotoImage(imgToShow) 
        panel = tk.Label(curWindow, image = imgToShow)
        panel.image = imgToShow 
        panel.grid(row = r, column = c, rowspan = rSpan, columnspan = cSpan)
        return None


    #performs reverse tranfsormation for 3 steps
    def reverseTrans(self): 
        self.originalNp = self.preprocessor.PreprocessImage(self.original)
        self.transformedNp = self.preprocessor.PreprocessImage(self.transformed)

        self.aiModel.Build(3)
        pred3 = self.aiModel.Predict([self.originalNp],[self.transformedNp])
        self.IMGtransformed31 = self.doTransformation(pred3, self.original)
        self.codes31 = []
        self.codes31.append(self.transformer.transformations[numpy.argmax(pred3[0])].GetCode())
        keras.backend.clear_session()

        self.aiModel.Build(2)
        transformedNp1 = self.preprocessor.PreprocessImage(self.IMGtransformed31)
        pred2 = self.aiModel.Predict([transformedNp1],[self.transformedNp])
        self.IMGtransformed32 = self.doTransformation(pred2, self.IMGtransformed31)
        self.codes32 = self.codes31.copy()
        self.codes32.append(self.transformer.transformations[numpy.argmax(pred2[0])].GetCode())
        keras.backend.clear_session()

        self.aiModel.Build(1)
        transformedNp2 = self.preprocessor.PreprocessImage(self.IMGtransformed32)
        pred1 = self.aiModel.Predict([transformedNp2],[self.transformedNp])
        self.IMGtransformed33 = self.doTransformation(pred1, self.IMGtransformed32)
        self.codes33 = self.codes32.copy()
        self.codes33.append(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())
        keras.backend.clear_session()

        print("Step 3 results")
        print(self.transformer.transformations[numpy.argmax(pred3[0])].GetCode())
        print(self.transformer.transformations[numpy.argmax(pred2[0])].GetCode())
        print(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())

        self.build3StepWindow()
        return None

    #performs reverse tranfsormation for 2 steps
    def run2StepReverseTransformation(self):
        self.aiModel.Build(2)
        pred2 = self.aiModel.Predict([self.originalNp],[self.transformedNp])
        self.IMGtransformed21 = self.doTransformation(pred2, self.original)
        self.codes21 = []
        self.codes21.append(self.transformer.transformations[numpy.argmax(pred2[0])].GetCode())
        keras.backend.clear_session()

        self.aiModel.Build(1)
        transformedNp1 = self.preprocessor.PreprocessImage(self.IMGtransformed21)
        pred1 = self.aiModel.Predict([transformedNp1],[self.transformedNp])
        self.IMGtransformed22 = self.doTransformation(pred1, self.IMGtransformed21)
        self.codes22 = self.codes21.copy()
        self.codes22.append(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())
        keras.backend.clear_session()

        print("Step 2 results")
        print(self.transformer.transformations[numpy.argmax(pred2[0])].GetCode())
        print(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())

        self.build2StepWindow()
        return None

    #performs reverse tranfsormation for 1 step
    def run1StepReverseTransformation(self):
        self.aiModel.Build(1)
        pred1 = self.aiModel.Predict([self.originalNp],[self.transformedNp])
        self.IMGtransformed11 = self.doTransformation(pred1, self.original)
        self.codes11 = []
        self.codes11.append(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())

        print("Step 1 results")
        print(self.transformer.transformations[numpy.argmax(pred1[0])].GetCode())

        self.build1StepWindow()
        return None
        
    #process photo with transformations predicted by AI, tmplist -> transformation list
    def processPhoto(self, tmplist:list):
        arraytmp = numpy.array(self.processed)

        for element in tmplist:
            arraytmp = self.transformer.GetTransformationByCode(element).Transform(arraytmp)
        
        self.processed = Image.fromarray(arraytmp)
        self.show_img(self.process, self.processed, 0, 1, 3)
        return None


    #performs transformation on image - tmplist -> transformation list | img -> image to transform
    def doTransformation(self, tmplist:list, img:Image):
        tmpFlatList = [x for l in tmplist for x in l]
        indexOfTransformation = numpy.argmax(numpy.array(tmpFlatList))
        transformationTMP = self.transformer.transformations[indexOfTransformation]
        arrayTransformed = numpy.array(img)
        arrayTransformed = transformationTMP.Transform(arrayTransformed)
        transformedImg = Image.fromarray(arrayTransformed)
        return transformedImg


    #runs image transformer
    def runTransformator(self):
        GuiJustTransform(Config)
        return None


    def showAbout(self):
        nwin = tk.Toplevel()
        nwin.title("Image processing inverter - about")
        aboutText = "Image processing inverter - an app made for enginner's degree\nauthors: Wojciech Król & Tomasz Skowron"
        textToWindow = tk.Label(nwin, text = aboutText)
        textToWindow.grid(row=0, column=0)
        return None

    #shows main menu window
    def buildMainWindow(self):
        self.root = tk.Tk()
        self.root.title("Image processing inverter - main menu")

        btnRunTransform = tk.Button(self.root, text ="Open image transformer", command = lambda : self.runTransformator()).grid(row = 0, column = 0)
        btnAbout = tk.Button(self.root, text ="About", command = lambda : self.showAbout()).grid(row = 0, column = 1, sticky = "W")
        btnPickOriginal = tk.Button(self.root, text ="Pick original image", command = lambda : self.open_org()).grid(row = 2, column = 0, columnspan = 2)
        btnPickOTransformed = tk.Button(self.root, text ="Pick transformed image", command = lambda : self.open_tran()).grid(row = 2, column = 2) 
        btnTransform = tk.Button(self.root, text = "Run reverse transformation process", command = lambda : self.reverseTrans()).grid(row = 3, column = 0, columnspan = 3)
        self.root.grid_columnconfigure(0, minsize = 145)
        self.root.grid_columnconfigure(1, minsize = 110)
        self.root.grid_rowconfigure(1, minsize = 255)
        self.root.grid_columnconfigure(2, minsize = 255)
        self.root.resizable(False, False)
        self.root.mainloop()
        return None

    #shows window with 3-step prediction results
    def build3StepWindow(self):
        self.threeStep = tk.Toplevel()
        self.threeStep.title("Image processing inverter - 3 step results")

        self.show_img(self.threeStep, self.original, 0, 0)
        self.show_img(self.threeStep, self.IMGtransformed31, 0, 1)
        self.show_img(self.threeStep, self.IMGtransformed32, 0, 2)
        self.show_img(self.threeStep, self.IMGtransformed33, 0, 3)
        btnThis1 = tk.Button(self.threeStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes31)).grid(row = 1, column = 1)
        btnThis2 = tk.Button(self.threeStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes32)).grid(row = 1, column = 2)
        btnThis3 = tk.Button(self.threeStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes33)).grid(row = 1, column = 3)
        btnDoFor2Steps = tk.Button(self.threeStep, text ="Run reverse transformation process again, this time for 2 steps only", command = lambda : self.run2StepReverseTransformation()).grid(row = 2, column = 1, columnspan = 2)

        self.threeStep.grid_rowconfigure(0, minsize = 255)
        for col in range(0, 4):
            self.threeStep.grid_columnconfigure(col, minsize=255)

        self.threeStep.resizable(False, False)
        self.threeStep.mainloop()
        return None

    #shows window with 2-step prediction results
    def build2StepWindow(self):
        self.twoStep = tk.Toplevel()
        self.twoStep.title("Image processing inverter - 2 step results")

        self.show_img(self.twoStep, self.original, 0, 0)
        self.show_img(self.twoStep, self.IMGtransformed21, 0, 1)
        self.show_img(self.twoStep, self.IMGtransformed22, 0, 2)
        btnThis1 = tk.Button(self.twoStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes21)).grid(row = 1, column = 1)
        btnThis2 = tk.Button(self.twoStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes22)).grid(row = 1, column = 2)
        btnDoFor1Step = tk.Button(self.twoStep, text ="Run reverse transformation process again, this time for 1 step only", command = lambda : self.run1StepReverseTransformation()).grid(row = 2, column = 1, columnspan = 2)

        self.twoStep.grid_rowconfigure(0, minsize = 255)
        for col in range(0, 3):
            self.twoStep.grid_columnconfigure(col, minsize=255)

        self.twoStep.resizable(False, False)
        self.twoStep.mainloop()
        return None

    #shows window with 1-step prediction results
    def build1StepWindow(self):
        self.oneStep = tk.Toplevel()
        self.oneStep.title("Image processing inverter - 1 step results")

        self.show_img(self.oneStep, self.original, 0, 0)
        self.show_img(self.oneStep, self.IMGtransformed11, 0, 1)
        btnThis1 = tk.Button(self.oneStep, text ="Pick this transformation", command = lambda : self.buildProcessWindow(self.codes11)).grid(row = 1, column = 1)

        self.oneStep.grid_rowconfigure(0, minsize = 255)
        for col in range(0, 2):
            self.oneStep.grid_columnconfigure(col, minsize=255)

        self.oneStep.resizable(False, False)
        self.oneStep.mainloop()
        return None

    #shows window with image picker to perform transformations
    def buildProcessWindow(self, tmplist:list):
        self.process = tk.Toplevel()
        self.process.title("Image processing inverter - process photo")

        codes = " "
        codes = codes.join(tmplist)
        print(tmplist)

        panel = tk.Label(self.process, text = codes)
        panel.grid(row = 0, column = 0)
        btnChoosePhoto = tk.Button(self.process, text = "Choose photo to process", command = lambda : self.open_toProcess()).grid(row = 1, column = 0)
        btnSave = tk.Button(self.process, text = "Save photo", command = lambda : self.savePhoto()).grid(row = 2, column = 0)
        btnFinish = tk.Button(self.process, text ="Finish", command = lambda : self.finish()).grid(row = 3, column = 0)
        btnProcessPhoto = tk.Button(self.process, text = "Process photo", command = lambda : self.processPhoto(tmplist)).grid(row = 3, column = 1)

        self.process.grid_columnconfigure(1, minsize = 255)
        for row in range(0, 3):
            self.process.grid_rowconfigure(row, minsize = 90)

        self.process.resizable(False, False)
        self.process.mainloop()
        return None

    #exits the application
    def finish(self):
        exit()

app = GuiMainMenu(Config)