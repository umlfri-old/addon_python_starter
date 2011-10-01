from threading import Event

from .messageResult import MessageResult

class Message(object):
    def __init__(self, objId, name):
        self.__objId = objId
        self.__name = name
        self.__params = {}
        self.__sendEvent = Event()
        self.__result = None
    
    def boolean_parameter(self, name, value):
        self.__params[name] = bool(value)
        return self
    
    def int32_parameter(self, name, value):
        self.__params[name] = int(value)
        return self
    
    def float_parameter(self, name, value):
        self.__params[name] = float(value)
        return self
    
    def variant_parameter(self, name, value):
        self.__params[name] = value
        return self
    
    def string_parameter(self, name, value):
        if not isinstance(value, basestring) and value is not None:
            value = str(value)
        self.__params[name] = value
        return self
    
    def xy_parameter(self, name, value):
        self.__params[name] = tuple(value)
        return self
    
    def xywh_parameter(self, name, value):
        self.__params[name] = tuple(value)
        return self
    
    def wh_parameter(self, name, value):
        self.__params[name] = tuple(value)
        return self
    
    def keyvalue_parameter(self, name, value):
        self.__params[name] = tuple(value)
        return self
    
    def object_parameter(self, name, value):
        self.__params[name] = value
        return self
    
    def send(self, server):
        server.send_command(self)
        self.__sendEvent.wait()
        return MessageResult(*self.__result)
    
    def send_async(self, server):
        server.send_command(self, True)
    
    def create_message(self):
        return 'exec', '#%s.%s'%(self.__objId, self.__name), (), self.__params
    
    def accept(self, cmd, params):
        self.__result = cmd, params
        self.__sendEvent.set()
