import os
import numpy
from PIL import Image
from Config import Config
from ImageMeta import ImageMeta
from ImagePreprocessor import ImagePreprocessor

#Represents a dataset. Handles loading the dataset.
class Dataset(object):
    #Default constructor
    def __init__(self,config:Config):
        self.config:Config
        self.collectionOrg = []
        self.collectionTransf = []
        self.collectionLabels = []
        self.meta:ImageMeta
        self.currentDataPage = 0
        self.dataPages = []
        self.config = config

    #Sums all file sizes in a folder.Takes path to original files and transfrmed files as inputs.
    def SumFileSizes(self,originalFile,transformedFile):
        sum = 0
        files = os.listdir(os.getcwd()+"\\"+self.config.originalFilePath)
        for file in files:
            if file == ".gitkeep":
                continue
            if file==originalFile:
                sum+=os.path.getsize(os.getcwd()+"\\"+self.config.originalFilePath+"\\"+file)
        files = os.listdir(os.getcwd()+"\\"+self.config.transformedFilePath)
        for file in files:
            if file == ".gitkeep":
                continue
            if file==transformedFile:
                sum+=os.path.getsize(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+file)
        return sum

    #Builds a list of data pages based on max page size. Due to excessive page building times it returns a list of files to load.
    def BuildDataPages(self):
        self.meta = ImageMeta(self.config)
        self.meta.LoadMeta()
        page = []
        summedSize = 0
        for i in range(0,len(self.meta.collection)):
            item = self.meta.collection[i]
            page.append(i)
        if len(page)!=0:
            self.dataPages.append(page)

    #Loads a dataset for training. Uses data pages.
    def LoadTrainingDataset(self,pageIndex):
        self.collectionOrg = []
        self.collectionTransf = []
        self.collectionLabels = []

        for i in self.dataPages[pageIndex]:
            item = self.meta.collection[i]
            preprocessor = ImagePreprocessor(self.config)
            original = Image.open(os.getcwd()+"\\"+self.config.originalFilePath+"\\"+item.originalFile)
            transformed = Image.open(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+item.transformedFile)
            originalNp = preprocessor.PreprocessImage(original)
            transformedNp = preprocessor.PreprocessImage(transformed)
            self.collectionOrg.append(originalNp)
            self.collectionTransf.append(transformedNp)
            self.collectionLabels.append(item.transformationIds[0])
            
    #Loads any dataset based on original and transformed files paths.
    def LoadDataset(self,originalPath,transformedPath,meta):
        self.collectionOrg = []
        self.collectionTransf = []
        self.collectionLabels = []

        for item in self.meta.collection:
            preprocessor = ImagePreprocessor(self.config)
            original = Image.open(os.getcwd()+"\\"+originalPath+"\\"+item.originalFile)
            transformed = Image.open(os.getcwd()+"\\"+self.transformedPath+"\\"+item.transformedFile)
            originalNp = preprocessor.PreprocessImage(original)
            transformedNp = preprocessor.PreprocessImage(transformed)
            self.collectionOrg.append(originalNp)
            self.collectionTransf.append(transformedNp)
            self.collectionLabels.append(item.transformationIds[0])