#Implementation of blurr algorithm. Here mean of pixels.
class MeanOfPxl(object):
    #Default constructor
    def __init__(self): return None
    #Returns transformation code.
    def GetCode(self): return "MOP"
    #Performs a transformation. Returns a copy of input array.
    def Transform(self, imageArray):
        copy = imageArray.copy()
        copyImg = imageArray.copy()
        for i in range(1,len(imageArray)-1):
            for j in range(1,len(imageArray[i])-1):
                copy[i][j][0] =   float((int(copyImg[i-1][j-1][0]) +   int(copyImg[i][j-1][0])  +  int(copyImg[i+1][j-1][0]) +
                                               int(copyImg[i-1][j][0])   +   int(copyImg[i][j][0])    +  int(copyImg[i+1][j][0]) +
                                               int(copyImg[i-1][j+1][0]) +   int(copyImg[i][j+1][0])  +  int(copyImg[i+1][j+1][0]))/9.0)

                copy[i][j][1] =   float((int(copyImg[i-1][j-1][1]) +   int(copyImg[i][j-1][1])  +  int(copyImg[i+1][j-1][1]) +
                                               int(copyImg[i-1][j][1])   +   int(copyImg[i][j][1])    +  int(copyImg[i+1][j][1]) +
                                               int(copyImg[i-1][j+1][1]) +   int(copyImg[i][j+1][1])  +  int(copyImg[i+1][j+1][1]))/9.0)

                copy[i][j][2] =   float((int(copyImg[i-1][j-1][2]) +   int(copyImg[i][j-1][2])  +  int(copyImg[i+1][j-1][2]) +
                                               int(copyImg[i-1][j][2])   +   int(copyImg[i][j][2])    +  int(copyImg[i+1][j][2]) +
                                               int(copyImg[i-1][j+1][2]) +   int(copyImg[i][j+1][2])  +  int(copyImg[i+1][j+1][2]))/9.0)
        return copy