from lib.Addons.Plugin.Starter import starters
from .pythonStarter import CPythonStarter

class CPlugin(object):
    def __init__(self, app):
        self.__app = app
    
    def Start(self):
        starters['pythonNew'] = CPythonStarter
    
    def CanStop(self):
        return True
    
    def Stop(self):
        del starters['pythonNew']
