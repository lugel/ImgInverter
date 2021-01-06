#Implementation of black-white gradient algorithm.
class GradientBW(object):
    #Default constructor.
    def __init__(self):
        return None
    #Returns transformation code.
    def GetCode(self):
        return "GBW"
    #Transforms an array. Returns copy of given array.
    def Transform(self,imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                maskR =128.0
                maskG =128.0
                maskB =128.0
                copy[i][j][0] = min(imageArray[i][j][0]+(maskR*float(j/len(imageArray))),255)
                copy[i][j][1] = min(imageArray[i][j][1]+(maskG*float(j/len(imageArray))),255)
                copy[i][j][2] = min(imageArray[i][j][2]+(maskB*float(j/len(imageArray))),255)
        return copy
