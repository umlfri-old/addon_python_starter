import glob
import os
import os.path
import subprocess
import sys
import shutil
from lib.Distconfig import IS_FROZEN

templatePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libraryTemplate", "index.xml.tmpl"))
libraryPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "library"))
mkaddonLib = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "share", "tools", "mkaddonlib", "main.py")

if IS_FROZEN:
    raise  Exception("Cannot update lib in the frozen environment")
if not os.path.exists(templatePath):
    raise Exception("Cannot find library template")
if not os.path.exists(mkaddonLib):
    raise Exception("Cannot find mkaddonlib utility")
if not os.path.exists(libraryPath):
    os.mkdir(libraryPath, 0755)

def update():
    # remove old generated library
    for name in glob.glob(os.path.join(libraryPath, "*")):
        shutil.rmtree(name)
    
    # generate new library
    p = subprocess.Popen([sys.executable, mkaddonLib, "-o", libraryPath, templatePath])
    p.wait()
