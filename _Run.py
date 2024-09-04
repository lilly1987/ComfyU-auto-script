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
    #while True:
    max=readDic("setup.json").get("totalMax",1280)
    for i in range(max):
        
        
        
        #==============================================
        
        setup=readDic("setup.json")
        #print(setup)
        if setup.get("queue_prompt_wait",True):
            queue_prompt_wait(url=url)
        
        
        dicFileCheckpoint,dicFileLora,dicFileChar=setup_start(setup)
        
        
        setup_workflow(setup)
        #print(cname)
        #==============================================
        setup_checkpoint(setup)

        setup_list(setup)
        
        #print("listDic : ",listDic)
        
        #==============================================
        setup_lora(setup)
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
        
        if setup.get("print setup",False):
            print("setup",setup)
        if setup.get("print workflow",False):
            print("workflow_api",workflow_api)
        
        #==============================================
        if setup.get("queue_prompt",True):
            if queue_prompt(workflow_api,url=url):
                time.sleep(1)
                #pass
                
        Setup_print(i,max)
        
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