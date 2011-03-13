class AdvProperty(object):
    def __init__(self, name, haveIndex, documentation):
        self.__name = name
        self.__haveIndex = haveIndex
        self.documentation = documentation
    
    def getter(self, function):
        self.__getter = function
        return self
    
    def setter(self, function):
        self.__setter = function
        return self
    
    def indexer(self, function):
        self.__indexer = function
        return self
