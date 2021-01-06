#Implementation of grey scale algorithm.
class GreyScale(object):
    #Default constructor
    def __init__(self):
        return None
    #Returns transformation code.
    def GetCode(self):
        return "GRA"
    #Performs transformation. Returns copy of input array.
    def Transform(self,imageArray):
        copy = imageArray.copy()
        for i in range(0,len(copy)):
            for j in range(0,len(copy[i])):
                r = copy[i][j][0]
                g = copy[i][j][1]
                b = copy[i][j][2]
                mean = (float(int(r)+int(g)+int(b)))/3.0
                copy[i][j][0]=int(mean)
                copy[i][j][1]=int(mean)
                copy[i][j][2]=int(mean)
        return copy
