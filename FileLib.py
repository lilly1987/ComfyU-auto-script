import os, sys
import sys
import subprocess
import pkg_resources
required  = {'json5'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 as json

def readJson(path,dic={}):
    with open(path) as f:
        dic = json.load(f)
    return dic