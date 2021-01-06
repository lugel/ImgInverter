import os
import numpy
import string
from PIL import Image
from Config import Config
from ImageMeta import ImageMeta
from ImageMetaElement import ImageMetaElement
from Transformation import Transformation
from CommonValueSubtraction import CommonValueSubtraction
from GradientBW import GradientBW
from GreyScale import GreyScale
from Multiply2 import Multiply2
from Divide2 import Divide2
from Negation import Negation
from MeanOfPxl import MeanOfPxl
from Noise import Noise
import random

class ImageTransformer(object):
    #Default constructor
    def __init__(self, config:Config):
        self.config = config
        self.imageMeta = ImageMeta(self.config)
        self.transformations:[Transformation] = []
        self.transformations.append(Transformation())
        self.transformations.append(CommonValueSubtraction())
        self.transformations.append(GradientBW())
        self.transformations.append(GreyScale())
        self.transformations.append(Multiply2())
        self.transformations.append(Divide2())
        self.transformations.append(Negation())
        self.transformations.append(MeanOfPxl())
        self.transformations.append(Noise())

    #Execute transformation of images
    def Transform(self):
        if(self.config.generateTransformed == True):
            counter = 0
            files = os.listdir(os.getcwd()+"\\"+self.config.transformedFilePath)
            for file in files:
                if file== ".gitkeep":
                    continue
                os.remove(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+file)

            files = os.listdir(os.getcwd()+"\\"+self.config.originalFilePath)
            orgIndex=0
            for file in files:
                if file == ".gitkeep":
                    continue
                print(str(orgIndex)+" done, out of "+ str(len(files)))
                orgIndex=orgIndex+1
                image = Image.open(os.getcwd()+"\\"+self.config.originalFilePath+"\\"+file)
                for transformation in self.transformations:
                    imageData = numpy.array(image) 
                    firstStep = transformation.Transform(imageData)
                    firstTransformId = transformation.GetCode()
                    newFileName = file.split('.')[0]+"t"+str(counter)+".jpg"
                    counter+=1
                    transformedImage1 = Image.fromarray(firstStep)
                    transformedImage1.save(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+newFileName)
                    metaEntry = ImageMetaElement()
                    metaEntry.originalFile = file
                    metaEntry.transformationIds.append(firstTransformId)
                    metaEntry.transformedFile = newFileName
                    self.imageMeta.Add(metaEntry)

                    if self.config.transformationSteps >1:
                        random.seed()
                        choice1 = random.randint(0,len(self.transformations)-1)
                        transformation1 = self.transformations[choice1]
                        secondStep = transformation1.Transform(firstStep)
                        secondTransformId = transformation1.GetCode()
                        newFileName = file.split('.')[0]+"t"+str(counter)+".jpg"
                        counter+=1
                        transformedImage2 = Image.fromarray(secondStep)
                        transformedImage2.save(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+newFileName)
                        metaEntry = ImageMetaElement()
                        metaEntry.originalFile = file
                        metaEntry.transformationIds.append(firstTransformId)
                        metaEntry.transformationIds.append(secondTransformId)
                        metaEntry.transformedFile = newFileName
                        self.imageMeta.Add(metaEntry)

                        if self.config.transformationSteps >2:
                            random.seed()
                            choice2 = random.randint(0,len(self.transformations)-1)
                            transformation2 = self.transformations[choice2]
                            thirdStep = transformation2.Transform(secondStep)
                            thirdTransformId = transformation2.GetCode()
                            newFileName = file.split('.')[0]+"t"+str(counter)+".jpg"
                            counter+=1
                            transformedImage3 = Image.fromarray(thirdStep)
                            transformedImage3.save(os.getcwd()+"\\"+self.config.transformedFilePath+"\\"+newFileName)
                            metaEntry = ImageMetaElement()
                            metaEntry.originalFile = file
                            metaEntry.transformationIds.append(firstTransformId)
                            metaEntry.transformationIds.append(secondTransformId)
                            metaEntry.transformationIds.append(thirdTransformId)
                            metaEntry.transformedFile = newFileName
                            self.imageMeta.Add(metaEntry)  

                            if self.config.transformationSteps >3:
                                print("Reached maximum number of steps (3), further steps wil not be performed.")
            self.imageMeta.SaveMeta()

    #Return transformation object by code
    def GetTransformationByCode(self,code):
        for transformation in self.transformations:
            if transformation.GetCode().lower() == code.lower():
                return transformation
        return None