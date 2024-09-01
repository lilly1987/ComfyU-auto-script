import os, sys, glob, random, time, copy, string
from os import path

#print(os.getcwd())
#print(__name__)
#print( path.dirname( path.abspath(__file__) ))
sys.path.append( path.dirname( path.abspath(__file__) ) )

from ConsoleColor import print, console
from FileLib import *

try:
    while True:
        setup=readJson("setup.json")
        print(setup)
        
        workflow_api=readJson("workflow_api.json")
        #print(workflow_api)
        #print(type(workflow_api))
        
        
        
        break
        
except Exception:
    console.print_exception()
    quit()