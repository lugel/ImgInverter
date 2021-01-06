#Implementation of division algorithm.
class Divide2(object):
    #Default ctor.
    def __init__(self): return None
    #Returns transformation code.
    def GetCode(self): return "DIV"
    #Perfroms a transformation. Returns copy of given array.
    def Transform(self, imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                copy[i][j][0] = int(imageArray[i][j][0] /2)
                copy[i][j][1] = int(imageArray[i][j][1] /2)
                copy[i][j][2] = int(imageArray[i][j][2] /2)
        return copy
