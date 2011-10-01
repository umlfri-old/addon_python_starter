from threading import Event

from .consts import RESP_OK
from .server import Server

class StartupMessage(object):
    def __init__(self):
        self.__sendEvent = Event()
        self.__allOk = False
    
    def create_message(self):
        return 'plugin', 'init', (), {}
    
    def send(self):
        Server.instance.send_command(self)
        self.__sendEvent.wait()
        if not self.__allOk:
            raise Exception("Server was not initialized properly")
    
    def accept(self, cmd, params):
        self.__allOk = cmd == RESP_OK

