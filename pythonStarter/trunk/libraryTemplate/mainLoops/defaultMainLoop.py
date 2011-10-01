from Queue import Queue

class DefaultMainLoop(object):
    def __init__(self):
        self.__evtQueue = Queue()
        self.__running = False
    
    @property
    def in_main_loop(self):
        return self.__running
        
    def main_loop(self):
        self.__running = True
        while True:
            cmd = self.__evtQueue.get()
            if cmd is None:
                break
            cmd[0](*cmd[1])
        self.__running = False
            
    def call(self, callable, *args):
        self.__evtQueue.put((callable, args))
    
    def quit(self):
        self.__evtQueue.put(None)
