import keras

from Config import Config
from ImageTransformer import ImageTransformer
from Dataset import Dataset
from Cauldron import Cauldron
from AImodel import AImodel
from ImagePreprocessor import ImagePreprocessor

from PIL import Image
import numpy
import os
import pydot
import copy

#Main class that handles process of creating the application through AI.
class ImageProcessingInverter:
    config:Config=None
    transformer:ImageTransformer=None
    dataset:Dataset=None
    cauldron:Cauldron=None
    aiModel:AImodel=None
    #Default ctor.
    def __init__(self):
        print("Application built.")
    #Main function of the application.
    def main(self):
        print("Running main.")

        print("Generating config.")
        self.config = Config("config.ini")

        begin = 1
        if self.config.includeLowerSteps==False:
            begin = self.config.transformationSteps
        else:
            begin = 1

        print("Cooking soup.")
        self.cauldron = Cauldron(self.config)
        self.cauldron.CookNSpill()
        steps = self.config.transformationSteps+1
        for stepNo in range(begin,steps):
            self.config = Config("config.ini")
            self.config.transformationSteps = stepNo
            self.config.transformedFilePath = self.config.transformedFilePath.replace(Config.placeholderI,str(stepNo))
            self.config.metaFilePath = self.config.metaFilePath.replace(Config.placeholderI,str(stepNo))

            print("Handling lower steps. Current step is:"+str(stepNo))
            print("Transforming images.")
            self.transformer = ImageTransformer(self.config)
            self.transformer.Transform()

            print("Building dataset.")
            self.dataset = Dataset(self.config)
            print("Building pages.")
            self.dataset.BuildDataPages()

            print("Building similar config.")
            self.configSimilar = Config("configSimilar.ini")
            self.configSimilar.transformationSteps = stepNo
            self.configSimilar.transformedFilePath = self.configSimilar.transformedFilePath.replace(Config.placeholderI,str(stepNo))
            self.configSimilar.metaFilePath = self.configSimilar.metaFilePath.replace(Config.placeholderI,str(stepNo))
            
            print("Cooking similar soup.")
            self.cauldronSimilar = Cauldron(self.configSimilar)
            self.cauldronSimilar.CookNSpill()

            print("Transforming similar images.")
            self.transformerSimilar = ImageTransformer(self.configSimilar)
            self.transformerSimilar.Transform()

            print("Building similar dataset.")
            self.datasetSimilar = Dataset(self.configSimilar)
            print("Building similar pages.")
            self.datasetSimilar.BuildDataPages()

            print("Building different config.")
            self.configDifferent = Config("configDifferent.ini")
            self.configDifferent.transformationSteps = stepNo
            self.configDifferent.transformedFilePath = self.configDifferent.transformedFilePath.replace(Config.placeholderI,str(stepNo))
            self.configDifferent.metaFilePath = self.configDifferent.metaFilePath.replace(Config.placeholderI,str(stepNo))

            print("Cooking different soup.")
            self.cauldronDifferent = Cauldron(self.configDifferent)
            self.cauldronDifferent.CookNSpill()

            print("Transforming different images.")
            self.transformerDifferent = ImageTransformer(self.configDifferent)
            self.transformerDifferent.Transform()

            print("Building different dataset.")
            self.datasetDifferent = Dataset(self.configDifferent)
            print("Building different pages.")
            self.datasetDifferent.BuildDataPages()
            
            print("Building AI model.")
            self.aiModel = AImodel(transformations=self.transformer.transformations,config=self.config)
            for i in range(0,len(self.dataset.dataPages)):
                print("Learning page: "+ str(i) +" of:"+str(len(self.dataset.dataPages)-1))
                self.dataset.LoadTrainingDataset(i)
                print(numpy.asarray(self.dataset.collectionOrg).shape)
                if self.config.doTraining:
                    print("Learning")
                    self.aiModel.Learn(self.dataset)
                if self.config.doEvaluation:
                    print("Training dataset evaluation:")
                    self.aiModel.Evaluate(self.dataset,"Training dataset evaluation")
                if self.configSimilar.doEvaluation:
                    print("Similar dataset evaluation:")
                    self.datasetSimilar.LoadTrainingDataset(0)
                    self.aiModel.EvaluateIndependent(self.datasetSimilar,"Similar dataset evaluation")
                if self.configDifferent.doEvaluation:
                    print("Different dataset evaluation:")
                    self.datasetDifferent.LoadTrainingDataset(0)
                    self.aiModel.EvaluateIndependent(self.datasetDifferent,"Different dataset evaluation")
    
            for file in os.listdir(os.getcwd()+"\\"+self.config.testSetFilePath):
                if file==".gitkeep":
                    continue
                preprocessor = ImagePreprocessor(self.config) 
                original = Image.open(os.getcwd()+"\\"+self.config.testSetFilePath+"\\"+file)
                transformed = Image.open(os.getcwd()+"\\"+self.config.testSetTransformedFilePath+"\\"+file)
                originalNp = preprocessor.PreprocessImage(original)
                transformedNp = preprocessor.PreprocessImage(transformed)
                self.aiModel.Predict([originalNp],[transformedNp])
            keras.backend.clear_session()       
        print("Exiting main.")

application = ImageProcessingInverter()
application.main()
