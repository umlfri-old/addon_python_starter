from lib.Addons.Plugin.Starter import CBaseProgramStarter
from lib.Distconfig import IS_FROZEN

import os
import os.path
import sys

ADDON_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

class CPythonStarter(CBaseProgramStarter):
    if IS_FROZEN:
        program = (os.path.join(ADDON_ROOT_PATH, 'starter', 'pl_runner.exe'), )
        environment = {}
    else:
        program = (sys.executable, os.path.join(ADDON_ROOT_PATH, 'starter', 'pl_runner.py'))
        environment = {'LIB': os.path.join(ADDON_ROOT_PATH, 'library')}
