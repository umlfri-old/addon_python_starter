from .exceptions import ReadOnlyException, NonIterableException

# hack for correct help in IPython
class FakeProperty(property):
    def __init__(self, doc):
        self.__doc__ = doc
    
    def __repr__(self):
        return '<property object>'

FakeProperty.__name__ = property.__name__
FakeProperty.__module__ = property.__module__

class AdvPropertyIndexer(object):
    def __init__(self, name, documentation, instance, getter, setter, iterator):
        self.__name__ = name
        self.__doc__ = documentation
        
        self.__instance = instance
        self.__getter = getter
        self.__setter = setter
        self.__iterator = iterator
    
    def __getitem__(self, index):
        return self.__getter(self.__instance, index)
    
    def __setitem__(self, index, value):
        if self.__setter is None:
            raise ReadOnlyException()
        else:
            self.__setter(self.__instance, index, value)
    
    def __iter__(self):
        if self.__iterator is None:
            raise NonIterableException()
        else:
            return iter(self.__iterator(self.__instance))

class AdvProperty(object):
    def __init__(self, name, hasIndex, documentation):
        self.__name__ = name
        self.__doc__ = documentation
        
        self.__hasIndex = hasIndex
        
        self.__getter = None
        self.__setter = None
        self.__iterator = None
    
    def getter(self, function):
        self.__getter = function
        return self
    
    def setter(self, function):
        self.__setter = function
        return self
    
    def iterator(self, function):
        self.__iterator = function
        return self
    
    def __get__(self, instance, cls = None):
        if instance is None:
            return FakeProperty(doc = self.__doc__)
        
        if self.__hasIndex:
            return AdvPropertyIndexer(self.__name__, self.__doc__, instance, self.__getter, self.__setter, self.__iterator)
        elif self.__iterator is not None:
            return iter(self.__iterator(instance))
        else:
            return self.__getter(instance)
    
    def __set__(self, instance, value):
        if self.__hasIndex or self.__setter is None:
            raise ReadOnlyException()
        else:
            self.__setter(instance, value)
