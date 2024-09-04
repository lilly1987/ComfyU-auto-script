import os, sys, glob, random, time, copy, string
from os import path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

sys.path.append( path.dirname( path.abspath(__file__) ) )
main=sys.argv.pop(0)

from ConsoleColor import print, console

def tensorsInfo(file):
    tensors = {}
    with safe_open(file, framework="pt", device="cpu") as f:
        if "__metadata__" in f :
            print("__metadata__",f["__metadata__"])
            
        #print("__metadata__",f.get("__metadata__"))
        #for key in f.keys():
        #   print(key)
        #   #tensors[key] = f.get_tensor(key)
           
if __name__ == '__main__':
    for arg in sys.argv:
        tensorsInfo(arg)
    pass