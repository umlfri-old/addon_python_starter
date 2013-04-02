from lib.config import config
from lib.Distconfig import IS_FROZEN
from lib.Depend.sysplatform import getPythonVersion
from lib.Addons.Plugin.Communication.Medium import CPipeMedium
from multiprocessing.forking import duplicate

import os
import os.path
import sys
import subprocess
import signal

try:
    import updateLib
except:
    updateLib = None

ADDON_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class CPythonStarter(object):
    if IS_FROZEN:
        __pl_runner = (os.path.join(ADDON_ROOT_PATH, 'starter', 'pl_runner.exe'), )
        __lib_root = None
    else:
        __pl_runner = (sys.executable, os.path.join(ADDON_ROOT_PATH, 'starter', 'pl_runner.py'))
        __lib_root = os.path.join(ADDON_ROOT_PATH, 'library')
    
    def __init__(self, plugin):
        self.__plugin = plugin
    
    def Start(self):
        if updateLib is not None:
            updateLib.update()
        
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        env = os.environ.copy()
        if self.__lib_root is not None:
            env['UMLFRI_LIB'] = str(self.__lib_root)
        env['UMLFRI_URI'] = str(uri)
        env['UMLFRI_PATH'] = str(path)
        
        pin = os.pipe()
        pout = os.pipe()
        self.__plugin.GetPluginManager().NewConnection(CPipeMedium(pin[0], pout[1]), (pin[0], pout[1]))
        
        if os.name == 'nt':
            import msvcrt
            ppin = duplicate(msvcrt.get_osfhandle(pout[0]), inheritable=True)
            ppout = duplicate(msvcrt.get_osfhandle(pin[1]), inheritable=True)
            env['UMLFRI_PIN'] = str(ppin) 
            env['UMLFRI_POUT'] = str(ppout)
            ppin = msvcrt.open_osfhandle(ppin, os.O_RDONLY)
            ppout = msvcrt.open_osfhandle(ppout, os.O_APPEND)
            self.__process = subprocess.Popen(self.__pl_runner, close_fds = False, env = env)
            os.close(pin[1])
            os.close(pout[0])
            os.close(ppin)
            os.close(ppout)
            
        else:
            env['UMLFRI_PIN'] = str(pout[0])
            env['UMLFRI_POUT'] = str(pin[1])
            pid = os.fork()
            if pid:
                #parent
                self.__pid = pid
                os.close(pin[1])
                os.close(pout[0])
            else:
                #child
                os.close(pin[0])
                os.close(pout[1])
                os.execve(self.__pl_runner[0], self.__pl_runner, env)
    
    def Terminate(self):
        if os.name == 'nt':
            self.__process.terminate()
        else:
            os.kill(self.__pid, signal.SIGTERM)
        
    def Kill(self):
        if os.name == 'nt':
            self.__process.kill()
        else:
            os.kill(self.__pid, signal.SIGKILL)
    
    def IsAlive(self):
        if os.name == 'nt':
            return self.__process.poll() is None
        else:
            try:
                return (0, 0) == os.waitpid(self.__pid, os.WNOHANG)
            except:
                return False
    
    def GetPid(self):
        if os.name == 'nt':
            return self.__process.pid
        else:
            return self.__pid
