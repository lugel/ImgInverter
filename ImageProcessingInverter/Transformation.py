#Base transformation. Implements no transformation and acts as generic one.
class Transformation(object):
    #Default ctor.
    def __init__(self):
        return None
    #Returns transformation code.
    def GetCode(self):
        return "NON"
    #Simply returns copy of the array.
    def Transform(self,imageArray):
        return imageArray.copy()