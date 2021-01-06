import os
from ImageMetaElement import ImageMetaElement
from Config import Config

#Class that takes care of meta information that creates relationships between original and transformed images.
class ImageMeta(object):
    #Default constructor
    def __init__(self, config):
        self.config = config
        self.collection:[ImageMetaElement] = []
    #Adds a new entry.
    def Add(self,metaElement:ImageMetaElement):
        self.collection.append(metaElement)
    #Clears all entries.
    def Clear(self):
        collection:[ImageMetaElement] = []
    #Saves meta entries to file.
    def SaveMeta(self):
        print("Saving meta to: " + self.config.metaFilePath)
        lines = []
        for item in self.collection:
            entry = item.originalFile+','+item.transformedFile+','
            tids = ""
            for tId in item.transformationIds:
                tids += tId + ','
            entry += tids[:-1] + '\n'
            lines.append(entry)
        metaFile = open(os.getcwd()+"\\"+self.config.metaFilePath,"w")
        metaFile.flush()
        metaFile.writelines(lines)
        metaFile.close()
    #Loads metas from a file.
    def LoadMeta(self):
        self.Clear()
        metaFile = open(os.getcwd()+"\\"+self.config.metaFilePath,"r")
        lines = metaFile.readlines()
        for line in lines:
            line = line[:-1]
            entry = ImageMetaElement()
            entry.originalFile = line.split(',')[0]
            entry.transformedFile = line.split(',')[1]
            entry.transformationIds = line.split(',')[2:]
            self.Add(entry)