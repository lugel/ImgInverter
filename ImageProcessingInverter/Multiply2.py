#Implementation of multilpication by 2.
class Multiply2(object):
    #Default constructor
    def __init__(self): return None
    #Returns transformation code.
    def GetCode(self): return "MUL"
    #Transforms input array. Returns copy of input.
    def Transform(self, imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                copy[i][j][0] = min(imageArray[i][j][0] *2, 255)
                copy[i][j][1] = min(imageArray[i][j][1] *2, 255)
                copy[i][j][2] = min(imageArray[i][j][2] *2, 255)
        return copy
