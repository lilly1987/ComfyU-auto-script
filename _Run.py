import os, sys, glob, random, time, copy, string
from os import path

#print(os.getcwd())
#print(__name__)
#print( path.dirname( path.abspath(__file__) ))
sys.path.append( path.dirname( path.abspath(__file__) ) )

from ConsoleColor import print, console
from FileLib import *
from WorkflowLib import *
from DicLib import *
from SetupLib import *

try:
    while True:
        
        #==============================================
        
        setup=readDic("setup.json")
        #print(setup)
        
        dicFileCheckpoint,dicFileLora=setup_workflow(setup)
        
        #==============================================
        
        dicLora={}
        dicFiles=GetFileList("dic/*.json")
        for f in dicFiles:
            update(dicLora,readDic(f))
            
        #print(dicLora)
        
        #==============================================
        
        
        
        #==============================================
        
        listFiles=GetFileList("list/*.json")
        listFile=random.choice(listFiles)
        listDic=readDic(listFile)
        #print("listDic : ",listDic)
        
        #==============================================
        setup_lora(setup,dicLora)
        #print("setup",setup)
        #==============================================
        
        workflow_api=readJson("workflow_api.json")
        #print(workflow_api)
        #print(type(workflow_api))
        
        workflow_setup(workflow_api,setup["workflow"])
        workflow_Loras(workflow_api,setup["Loras"])
        
        #print(workflow_api)
        
        #==============================================
        
        break
        
except KeyboardInterrupt:
    print('Interrupted')
    console.save_html(logFile)
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)
except Exception:
    #console.print_exception(show_locals=True)
    console.print_exception()
    #console.save_html(logFile)
    #quit()