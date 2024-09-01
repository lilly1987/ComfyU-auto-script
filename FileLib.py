import ast
import glob
import os, sys
import subprocess
import pkg_resources
from pathlib import *
from ConsoleColor import print, console

required  = {'json5'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import json5 
import json


def readJson(path,dic={}):
    with open(path) as file:
        dic = json5.load(file)
    return dic
    
def readDic(path,dic={}):
    try:
        with open(path) as file:
            #dic = json.load(file)
            text=file.read()
            text=text.replace('true', 'True')
            text=text.replace('false', 'False')
            dic=ast.literal_eval(text)
        return dic
    except Exception:
        print("path : ",path,style="reset")
        raise
    
    
def GetFileList(path,dir="."):
    list=[i.relative_to(dir) for i in Path(dir).glob(path)]
    #if not d is None:
    #    for f in list:
    #        #print(os.path.relpath(f,d))
    #        print(PurePath.relative_to(f,d))
    return list
    
def GetFileDic(path,dir="."):
    list=GetFileList(path,dir)
    dic=dict(zip( [i.stem for i in list], list))
    #if not d is None:
    #    for f in list:
    #        #print(os.path.relpath(f,d))
    #        print(PurePath.relative_to(f,d))
    return dic
    
def dicToJsonFile(d,path):
    with open(path,"w") as f:
        #f.write(t)
        json.dump(d, f, indent=4)