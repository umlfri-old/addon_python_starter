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

debugCommunication = 'UMLFRI_PLUGIN_DEBUG' in os.environ

from org.umlfri.api.implementation import Server, FileChannel, MIMChannel, StartupMessage, InitializedMessage
from org.umlfri.api.base import Adapter

fin = os.fdopen(pin, 'r')
fout = os.fdopen(pout, 'w')

channel = FileChannel(fin, fout)

if debugCommunication:
    channel = MIMChannel(channel)

server = Server(channel)
StartupMessage(uri).send(server)

import plugin

adapter=Adapter(server, 'adapter')
plugin.pluginMain(adapter)

InitializedMessage().send(server)

server.main_loop()
