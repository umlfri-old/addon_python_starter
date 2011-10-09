from cStringIO import StringIO

class MessageResult(object):
    def __init__(self, cmd, params):
        self.__cmd = cmd
        self.__params = params
    
    def throws_exception(self, cmd, exception):
        if cmd == self.__cmd:
            raise exception(self.__params['params'])
        return self
    
    def __control_exception(self):
        if self.__cmd is not None:
            if 'params' in self.__params:
                params = self.__params['params']
            else:
                params = None
            raise Exception("Unknown exception %d: %r"%(self.__cmd, params))
    
    def return_void(self):
        self.__control_exception()
        
    def return_boolean(self):
        self.__control_exception()
        
        return bool(self.__params['result'])
        
    def return_inputstream(self):
        self.__control_exception()
        
        ret = self.__params['result']
        if not isinstance(ret, basestring):
            ret = str(ret)
        return StringIO(ret)
    
    def return_int32(self):
        self.__control_exception()
        
        return int(self.__params['result'])
    
    def return_float(self):
        self.__control_exception()
        
        return float(self.__params['result'])
    
    def return_variant(self):
        self.__control_exception()
        
        return self.__params['result']
    
    def return_string(self):
        self.__control_exception()
        
        ret = self.__params['result']
        if not isinstance(ret, basestring) and ret is not None:
            ret = str(ret)
        return ret
    
    def return_xy(self):
        self.__control_exception()
        
        return tuple(self.__params['result'])
    
    def return_xywh(self):
        self.__control_exception()
        
        return tuple(self.__params['result'])
    
    def return_wh(self):
        self.__control_exception()
        
        return tuple(self.__params['result'])
    
    def return_keyvalue(self):
        self.__control_exception()
        
        return tuple(self.__params['result'])
    
    def return_object(self):
        self.__control_exception()
        
        return self.__params['result']
        
    def iterate_boolean(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield bool(item)
        
    def iterate_inputstream(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            if not isinstance(item, basestring):
                item = str(item)
            yield StringIO(item)
    
    def iterate_int32(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield int(item)
    
    def iterate_float(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield float(item)
    
    def iterate_variant(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield item
    
    def iterate_string(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            if not isinstance(item, basestring) and item is not None:
                item = str(item)
            yield item
    
    def iterate_xy(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield tuple(item)
    
    def iterate_xywh(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield tuple(item)
    
    def iterate_wh(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield tuple(item)
    
    def iterate_keyvalue(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield tuple(item)
    
    def iterate_object(self):
        self.__control_exception()
        
        for item in self.__params['result']:
            yield item
