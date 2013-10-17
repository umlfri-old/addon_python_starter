import ast
import base64
import threading

from ..factory import Factory

class Encoding(object):
    def __init__(self, server):
        self.__callbacks = {}
        self.__callbackIds = {}
        self.__callbackLock = threading.Lock()
        self.__callbackId = 0
        self.__factory = Factory(server)
    
    def encode(self, value):
        if isinstance(value, bool):
            return 'bool', self.__encode_boolean(value)
        elif hasattr(value, '__id__'):
            return 'object', self.__encode_object(value)
        elif isinstance(value, basestring):
            return 'str', self.__encode_string(value)
        elif isinstance(value, (int, long)):
            return 'int', self.__encode_int(value)
        elif isinstance(value, list) and (len(value) == 0 or all(hasattr(val, '__id__') for val in value)):
            return 'objectlist', self.__encode_object_list(value)
        elif callable(value):
            return 'callback', self.__encode_callback(value)
        elif value is None:
            return 'none', self.__encode_none(value)
        else:
            return 'eval', self.__encode_eval(value)

    def __encode_boolean(self, value):
        return 'True' if value else 'False'

    def __encode_object(self, value):
        return '#%s' % value.__id__

    def __encode_string(self, value):
        if isinstance(value, str):
            return base64.b64encode(value + '\0')
        elif isinstance(value, unicode):
            return base64.b64encode(value + '\x01')

    def __encode_int(self, value):
        return str(value)

    def __encode_object_list(self, value):
        return '[' + ','.join(self.__encode_object(item) for item in value) + ']'

    def __encode_callback(self, value):
        with self.__callbackLock:
            if id(value) in self.__callbackIds:
                return str(self.__callbackIds[id(value)])
            self.__callbackId += 1
            self.__callbacks[self.__callbackId] = value
            self.__callbackIds[id(value)] = self.__callbackId
            return str(self.__callbackId)

    def __encode_none(self, value):
        return 'None'

    def __encode_eval(self, value):
        return repr(value)
    
    def decode(self, value):
        type, value = value
        if type == 'bool':
            return self.__decode_boolean(value)
        elif type == 'object':
            return self.__decode_object(value)
        elif type == 'str':
            return self.__decode_string(value)
        elif type == 'int':
            return self.__decode_int(value)
        elif type == 'objectlist':
            return self.__decode_object_list(value)
        elif type == 'callback':
            return self.__decode_callback(value)
        elif type == 'none':
            return self.__decode_none(value)
        else:
            return self.__decode_eval(value)

    def __decode_boolean(self, value):
        return True if value == 'True' else False

    def __decode_object(self, value):
        id, type = value[1:].split('::')
        return self.__factory.get_instance(type, id)

    def __decode_string(self, value):
        value = base64.b64decode(value)
        if value[-1] == '\0':
            return value[:-1]
        else:
            return unicode(value[:-1])

    def __decode_int(self, value):
        return int(value)

    def __decode_object_list(self, value):
        return [self.__decode_object(item) for item in value[1:-1].split(',') if item != '']

    def __decode_callback(self, value):
        return self.__callbacks[int(value)]

    def __decode_none(self, value):
        return None

    def __decode_eval(self, value):
        return ast.literal_eval(value)
    
    def encode_many(self, values):
        if isinstance(values, dict):
            ret = {}
            for name, value in values.iteritems():
                ret[name] = self.encode(value)
            return repr(ret)
        else:
            ret = tuple(self.encode(value) for value in values)
            return repr(ret)
    
    def decode_many(self, str):
        values = ast.literal_eval(str)
        
        if isinstance(values, dict):
            ret = {}
            for name, value in values.iteritems():
                ret[name] = self.decode(value)
            return ret
        else:
            ret = tuple(self.decode(value) for value in values)
            return ret
    
    def decode_one(self, str):
        value = ast.literal_eval(str)
        return self.decode(value)
    
    def decode_simple(self, str):
        return ast.literal_eval(str)
