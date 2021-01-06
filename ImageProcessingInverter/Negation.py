#Implementation of negation algorithm.
class Negation(object):
    #Default constructor
    def __init__(self): return None
    #Returns code of the transformation.
    def GetCode(self): return "NEG"
    #Transforms the image. Returns copy of input.
    def Transform(self, imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                copy[i][j][0] = 255 - imageArray[i][j][0]
                copy[i][j][1] = 255 - imageArray[i][j][1]
                copy[i][j][2] = 255 - imageArray[i][j][2]
        return copy