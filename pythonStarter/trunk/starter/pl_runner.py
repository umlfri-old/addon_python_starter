#!/usr/bin/python
import sys

import os

uri = os.environ['UMLFRI_URI']

pin = int(os.environ['UMLFRI_PIN'])
pout = int(os.environ['UMLFRI_POUT'])

if os.name == 'nt':
    import msvcrt
    pin = msvcrt.open_osfhandle(pin, os.O_RDONLY)
    pout = msvcrt.open_osfhandle(pout, os.O_APPEND)

if 'UMLFRI_LIB' in os.environ:
    sys.path.insert(0, os.environ['UMLFRI_LIB'])

sys.path.insert(0, os.environ['UMLFRI_PATH'])

from org.umlfri.api.implementation import Server, FileChannel, MIMChannel, StartupMessage
from org.umlfri.api.base import Adapter
fin = os.fdopen(pin, 'r')
fout = os.fdopen(pout, 'w')
Server.crate_instance(MIMChannel(FileChannel(fin, fout)))
StartupMessage(uri).send()

import plugin



adapter=Adapter('adapter')
plugin.pluginMain(adapter)
Server.instance.main_loop()
