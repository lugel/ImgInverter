from PIL import Image
import numpy
from Config import Config
#Class that handles all preprocessing that may occur to an input image. It resolves a problem of image preparation in different parts of code.
class ImagePreprocessor(object):
    #Default constructor
    def __init__(self, config:Config):
        self.config = config
    #Preprocesses the image.
    def PreprocessImage(self, img:Image):
        img = img.resize((self.config.imageTrainSize,self.config.imageTrainSize))
        imgNp = (numpy.array(img)).astype(numpy.float32)/255.0
        return imgNp