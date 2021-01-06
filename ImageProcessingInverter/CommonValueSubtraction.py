#Implementation of common value subtraction algorithm.
class CommonValueSubtraction(object):
    #Default constructor
    def __init__(self):
        return None

    #Returns code of the transformation.
    def GetCode(self):
        return "CVS"

    #Performs a transformation, returns a copy of entered array.
    def Transform(self,imageArray):
        copy = imageArray.copy()
        for i in range(0,len(imageArray)):
            for j in range(0,len(imageArray[i])):
                r = imageArray[i][j][0]
                g = imageArray[i][j][1]
                b = imageArray[i][j][2]
                copy[i][j][0]=imageArray[i][j][0]-min(r,g,b)
                copy[i][j][1]=imageArray[i][j][1]-min(r,g,b)
                copy[i][j][2]=imageArray[i][j][2]-min(r,g,b)
        return copy
