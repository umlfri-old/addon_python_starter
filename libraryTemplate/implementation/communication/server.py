from ...mainLoops import DefaultMainLoop
import thread
from .consts import RESP_FINALIZE, RESP_CALLBACK, IDENTIFIER, VERSION
from .encoding import Encoding

from threading import Lock

class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class Server(object):
    __instance = None
    
    @ClassProperty
    @classmethod
    def instance(cls):
        if cls.__instance is None:
            raise Exception("Server instance not initialized!")
        return cls.__instance
    
    @classmethod
    def crate_instance(cls, channel):
        if cls.__instance is not None:
            raise Exception("Server instance already initialized!")
        cls.__instance = Server(channel)
    
    def __init__(self, channel):
        self.__channel = channel
        
        self.__mainLoop = DefaultMainLoop()
        self.__encoding = Encoding()
        
        self.__messageLock = Lock()
        self.__messages = {}
        self.__messagesId = 0
        
        thread.start_new_thread(self.__serve, ())
        self.command()
            
    def set_main_loop(self, main_loop):
        if self.__mainLoop.in_main_loop():
            raise Exception("Cannot change main loop while plugin is running")
        self.__mainLoop = main_loop
    
    def send_command(self, message):
        with self.__messageLock:
            self.__messagesId += 1
            id = self.__messagesId
            self.__messages[id] = message
            cmd, uri, params = message.create_message()
            self.__channel.write_line('%s %s %s/%s'%(cmd, uri, IDENTIFIER, VERSION))
            for name, value in params.iteritems():
                self.__channel.write_line('%s: %s'%(name, self.__encoding.encode_to_string(value)))
            self.__channel.write_line('__id__: %d'%id)
            self.__channel.write_line()
            self.__channel.write_line()
    
    def __serve(self):
        while True:
            line = self.__channel.read_line()
            
            if not line:
                continue
            
            ver, cmd = line.split()
            params = {}
            
            while line != '':
                name, value = line.split(':')
                params[name] = value.strip()
            
            for name in 'params', 'args', 'kwds', 'result':
                if name in params:
                    params[name] = self.__encoding.decode_from_string(params[name])
            
            with self.__messageLock:
                if '__id__' in params:
                    id = params['__id__']
                    del params['__id__']
                    msg = self.__messages[id]
                    del self.__messages[id]
                else:
                    msg = None
            
            if msg is None:
                self.__accept(cmd, params)
            else:
                msg.accept(cmd, params)
                    
    
    def __accept(self, cmd, params):
        if cmd == RESP_FINALIZE:
            self.__mainLoop.quit()
        elif cmd == RESP_CALLBACK:
            callback = self.__encoding.decode(('callback', params['callback']))
            self.__mainLoop.call(callback, params['args'])
