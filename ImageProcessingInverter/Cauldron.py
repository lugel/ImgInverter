import os
from Config import Config
from PIL import Image

#This class loads unordered files and puts them in a originals folder.
class Cauldron(object):
    #Default constructor
    def __init__(self, config:Config):
        self.config=config
    #Calling this function will cause a process of normalization of unordered files.
    def CookNSpill(self):
        normalizedfiles = os.listdir(os.getcwd()+"\\"+self.config.originalFilePath)
        counter = len(normalizedfiles)
        soup = os.listdir(os.getcwd()+"\\"+self.config.cauldronFilePath)
        for ingredient in soup:
            if ingredient == ".gitkeep":
                continue
            im = Image.open(os.getcwd()+"\\"+self.config.cauldronFilePath+"\\"+ingredient)
            im = im.resize((100,100))
            im = im.convert('RGB')
            im.save(os.getcwd()+"\\"+self.config.originalFilePath+"\\image"+str(counter)+".jpg")
            os.remove(os.getcwd()+"\\"+self.config.cauldronFilePath+"\\"+ingredient)
            counter=counter+1