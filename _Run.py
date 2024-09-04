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

vdebug=True

def debug(txt,setup):
    if vdebug:
        print(txt,setup)
        os.system("pause")
    
try:
    #while True:
    max=readDic("setup.json").get("totalMax",1280)
    for i in range(max):

        setup=readDic("setup.json")
        vdebug=setup.pop("debug",False)
        debug("setup_start",setup)
        
        
        dicFileCheckpoint,dicFileLora,dicFileChar=setup_start(setup)
        debug("setup_start",setup)
        
        setup_checkpoint(setup)
        debug("setup_checkpoint",setup)
        
        setup_list(setup)
        debug("setup_list",setup)
        
        setup_lora_add(setup)
        debug("setup_lora_add",setup)
        
        setup_dic(setup)
        debug("setup_dic",setup)
        
        setup_workflow(setup)
        debug("setup_workflow",setup)
        
        #==============================================
        #setup_last(setup)
        #==============================================
        
        workflow_api=readJson(Path(setup["Path"],"workflow_api.json"))
        #print(workflow_api)
        #print(type(workflow_api))
        
        workflow_setup(workflow_api,setup)
        debug("workflow_setup",workflow_api)
        workflow_Loras(workflow_api,setup)
        debug("workflow_Loras",workflow_api)
        workflow_Wildcard(workflow_api,setup)
        debug("workflow_Wildcard",workflow_api)
        
        dicToJsonFile(workflow_api,"test.json")
        
        if setup.get("print setup",False):
            print("setup",setup)
        if setup.get("print workflow",False):
            print("workflow_api",workflow_api)
        
        #==============================================
        if setup.get("queue_prompt",True):
            if queue_prompt(workflow_api,url=url):
                pass
                
        Setup_print(i,max)
        
        #==============================================
        if setup.get("queue_prompt_wait",True):
            queue_prompt_wait(url=url)
        time.sleep(setup.get("sleep",0))
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