import random
#Implementation of noise algorithm.
class Noise(object):
    #Default constructor
    def __init__(self): return None
    #Returns code of the transformation.
    def GetCode(self): return "NIS"
    #Performs transformation. Returns copy of input.
    def Transform(self, imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                r = random.randint(1,10)
                if r==1:
                     copy[i][j][0] = 255
                     copy[i][j][1] = 255
                     copy[i][j][2] = 255
        return copy