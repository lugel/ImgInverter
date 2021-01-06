import os
import string

#Implementation of a configuration class. 
#Contains all properties that are stored in config file.
class Config:
    #Format of a placeholder for specialized entries.
    placeholderI = "[i]"
    
    #Default constructor
    def __init__(self,configName):
        file = open(os.getcwd()+"\\"+configName)
        self.configName = configName
        self.originalFilePath=file.readline().split(':')[1].replace('\n','')
        self.transformedFilePath=file.readline().split(':')[1].replace('\n','')
        self.cauldronFilePath=file.readline().split(':')[1].replace('\n','')
        self.metaFilePath=file.readline().split(':')[1].replace('\n','')
        self.testSetFilePath=file.readline().split(':')[1].replace('\n','')
        self.testSetTransformedFilePath=file.readline().split(':')[1].replace('\n','')
        self.generateTransformed=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.saveModel=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.generateModelPlot=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.transformationSteps=int(file.readline().split(':')[1].replace('\n',''))
        self.includeLowerSteps=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.imageTrainSize=int(file.readline().split(':')[1].replace('\n',''))
        self.doTraining=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.doEvaluation=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.savePlots=bool("True"==file.readline().split(':')[1].replace('\n',''))
        self.plotsOutFolder=file.readline().split(':')[1].replace('\n','')
        self.Epochs=int(file.readline().split(':')[1].replace('\n',''))
        file.close()
        return None

    #Saves the config.
    def Save(self,destinationFile):
        lines=[]
        entry = "originalFilePath:"+self.originalFilePath+"\n"
        lines.append(entry)
        entry = "transformedFilePath:"+self.transformedFilePath+"\n"
        lines.append(entry)
        entry = "cauldronFilePath:"+self.cauldronFilePath+"\n"
        lines.append(entry)
        entry = "metaFilePath:"+self.metaFilePath+"\n"
        lines.append(entry)
        entry = "testSetFilePath:"+self.testSetFilePath+"\n"
        lines.append(entry)
        entry = "testSetTransformedFilePath:"+self.testSetTransformedFilePath+"\n"
        lines.append(entry)
        entry = "generateTransformed:"+str(self.generateTransformed)+"\n"
        lines.append(entry)
        entry = "saveModel:"+str(self.saveModel)+"\n"
        lines.append(entry)
        entry = "generateModelPlot:"+str(self.generateModelPlot)+"\n"
        lines.append(entry)
        entry = "transformationSteps:"+str(self.transformationSteps)+"\n"
        lines.append(entry)
        entry = "includeLowerSteps:"+str(self.includeLowerSteps)+"\n"
        lines.append(entry)
        entry = "imageTrainSize:"+str(self.imageTrainSize)+"\n"
        lines.append(entry)
        entry = "doTraining:"+str(self.doTraining)+"\n"
        lines.append(entry)
        entry = "doEvaluation:"+str(self.doEvaluation)+"\n"
        lines.append(entry)
        entry = "savePlots:"+str(self.savePlots)+"\n"
        lines.append(entry)
        entry = "plotsOutFolder:"+str(self.plotsOutFolder)+"\n"
        lines.append(entry)
        entry = "Epochs:"+str(self.Epochs)+"\n"
        lines.append(entry)

        file = open(destinationFile,"w")
        file.flush()
        file.writelines(lines)
        file.close()