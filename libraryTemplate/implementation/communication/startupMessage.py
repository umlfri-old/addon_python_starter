from threading import Event

from .consts import RESP_OK

class StartupMessage(object):
    def __init__(self, uri):
        self.__sendEvent = Event()
        self.__allOk = False
        self.__uri = uri
    
    def create_message(self):
        return 'plugin', 'connect', (), {'uri': self.__uri}
    
    def send(self, server):
        server.send_command(self)
        self.__sendEvent.wait()
        if not self.__allOk:
            raise Exception("Server was not initialized properly")
    
    def accept(self, cmd, params):
        self.__allOk = cmd == RESP_OK
        self.__sendEvent.set()

