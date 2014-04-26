from itertools import chain
from lib.Distconfig import IS_FROZEN
from multiprocessing.forking import duplicate

import os
import os.path
import sys
import subprocess
import signal

try:
    from exceptions import WindowsError
except ImportError:
    class WindowsError(Exception):
        """
        Never occuring exception. WindowsError replacement for non-windows system.
        """

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
    
    def Start(self, channel):
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        env = os.environ.copy()
        if self.__lib_root is not None:
            env['UMLFRI_LIB'] = str(self.__lib_root)
        env['UMLFRI_URI'] = str(uri)
        env['UMLFRI_PATH'] = str(path)
        
        if os.name == 'nt':
            import msvcrt
            ppin = duplicate(msvcrt.get_osfhandle(channel.GetReaderFD()), inheritable=True)
            ppout = duplicate(msvcrt.get_osfhandle(channel.GetWriterFD()), inheritable=True)
            env['UMLFRI_PIN'] = str(ppin)
            env['UMLFRI_POUT'] = str(ppout)
            ppin = msvcrt.open_osfhandle(ppin, os.O_RDONLY)
            ppout = msvcrt.open_osfhandle(ppout, os.O_APPEND)
            self.__process = subprocess.Popen(self.__pl_runner, close_fds = False, env = env)
            channel.CloseOthers()
            os.close(ppin)
            os.close(ppout)
            
        else:
            env['UMLFRI_PIN'] = str(channel.GetReaderFD())
            env['UMLFRI_POUT'] = str(channel.GetWriterFD())
            pid = os.fork()
            if pid:
                #parent
                self.__pid = pid
                channel.CloseOthers()
                os.close(pin[1])
                os.close(pout[0])
            else:
                #child
                channel.Close()
                os.execve(self.__pl_runner[0], self.__pl_runner, env)
    
    def Terminate(self):
        if os.name == 'nt':
            try:
                self.__process.terminate()
            except WindowsError:
                if self.__process.poll() is None:
                    raise

        else:
            os.kill(self.__pid, signal.SIGTERM)
        
    def Kill(self):
        if os.name == 'nt':
            try:
                self.__process.kill()
            except WindowsError:
                if self.__process.poll() is None:
                    raise
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
