from ...mainLoops import DefaultMainLoop
from .consts import RESP_FINALIZE, RESP_CALLBACK, IDENTIFIER, VERSION, RESP_RESULT
from .encoding import Encoding

import thread
from threading import Lock, Event

class Server(object):
    def __init__(self, channel):
        self.__channel = channel
        
        self.__mainLoop = DefaultMainLoop()
        self.__encoding = Encoding(self)
        
        self.__messageLock = Lock()
        self.__messages = {}
        self.__messagesId = 0
        
        thread.start_new_thread(self.__serve, ())
            
    def set_main_loop(self, main_loop):
        if self.__mainLoop.in_main_loop:
            raise Exception("Cannot change main loop while plugin is running")
        self.__mainLoop = main_loop
    
    def main_loop(self):
        self.__mainLoop.main_loop()
            
    def send_command(self, message, async = False):
        with self.__messageLock:
            self.__messagesId += 1
            id = self.__messagesId
            if not async:
                self.__messages[id] = message
            cmd, uri, args, kwds = message.create_message()
            self.__channel.write_line('%s %s %s/%s'%(cmd, uri, IDENTIFIER, VERSION))
            self.__channel.write_line('args: %s'%self.__encoding.encode_many(args))
            self.__channel.write_line('kwds: %s'%self.__encoding.encode_many(kwds))
            self.__channel.write_line('__id__: %d'%id)
            self.__channel.write_line()
            self.__channel.write_line()
    
    def __serve(self):
        while True:
            try:
                line = self.__channel.read_line()
            except ValueError:
                thread.interrupt_main()
            
            if not line:
                continue
            
            firstRow = line.split()
            params = {}
            
            cmd = int(firstRow[1])
            
            while True:
                line = self.__channel.read_line()
                if line == '':
                    break
                
                name, value = line.split(':', 1)
                params[name] = value.strip()
            
            if 'args' in params:
                params['args'] = self.__encoding.decode_many(params['args'])
            if 'kwds' in params:
                params['kwds'] = self.__encoding.decode_many(params['kwds'])
            if 'result' in params:
                params['result'] = self.__encoding.decode_one(params['result'])
            if 'params' in params:
                params['result'] = self.__encoding.decode_simple(params['params'])
            
            with self.__messageLock:
                if '__id__' in params:
                    id = int(params['__id__'])
                    del params['__id__']
                    if id in self.__messages:
                        msg = self.__messages[id]
                        del self.__messages[id]
                    else:
                        msg = None
                else:
                    msg = None
            
            if msg is None:
                self.__accept(cmd, params)
            else:
                if cmd == RESP_RESULT:
                    cmd = None
                msg.accept(cmd, params)
    
    def __accept(self, cmd, params):
        if cmd == RESP_FINALIZE:
            self.__mainLoop.quit()
        elif cmd == RESP_CALLBACK:
            callback = self.__encoding.decode(('callback', params['callback']))
            self.__mainLoop.call(callback, *params['args'])
