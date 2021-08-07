
class Entity:
    def __init__(self, tag, entType, getMethod="default"):
        self.tag=tag
        self.entType=entType
        self.getMethod = getMethod
        self.price = -1
    
    def get(self):
        if self.getMethod == "default":
            pass

    def decision(self):
        pass    

    