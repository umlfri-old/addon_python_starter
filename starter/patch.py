from lib.Addons.Plugin.Starter import starters
from .pythonStarter import CPythonStarter

try:
    import updateLib
except:
    updateLib = None

class CPlugin(object):
    __identifiers = 'python', 'pythonNew'
    
    def __init__(self, app):
        self.__app = app
        self.__oldValues = {}
    
    def Start(self):
        if updateLib:
            updateLib.update()
        
        for name in self.__identifiers:
            if name in starters:
                self.__oldValues[name] = starters[name]
            starters[name] = CPythonStarter
    
    def CanStop(self):
        return True
    
    def Stop(self):
        for name in self.__identifiers:
            del starters[name]
        starters.update(self.__oldValues)
