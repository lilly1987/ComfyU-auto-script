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
from queue_prompt import *
import SetupLib 

url="http://127.0.0.1:8188/prompt"

try:
    while True:
        
        queue_prompt_wait(url=url)
        
        #==============================================
        
        setup=readDic("setup.json")
        #print(setup)
        
        dicFileCheckpoint,dicFileLora=setup_loop(setup)
        
        
        setup_workflow(setup)
        #print(cname)
        #==============================================
        
        dicLora={}
        dicFiles=GetFileList("dic/*.json")
        for f in dicFiles:
            update(dicLora,readDic(f))
            
        #print(dicLora)
        
        #==============================================
        
        
        
        #==============================================
        

        setup_list(setup)
        
        #print("listDic : ",listDic)
        
        #==============================================
        setup_lora(setup,dicLora)
        #print("setup",setup)
        #==============================================
        setup_last(setup)
        #==============================================
        
        workflow_api=readJson(Path(setup["Path"],"workflow_api.json"))
        #print(workflow_api)
        #print(type(workflow_api))
        
        workflow_setup(workflow_api,setup)
        workflow_Loras(workflow_api,setup)
        workflow_Wildcard(workflow_api,setup)
        
        dicToJsonFile(workflow_api,"test.json")
        print(setup)
        print(workflow_api)
        
        #==============================================
        if setup.get("queue_prompt",True):
            if queue_prompt(workflow_api,url=url):
                time.sleep(1)
                #pass
                
        Setup_print()
        
        #==============================================
        
        #break
        
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