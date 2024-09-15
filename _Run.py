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
        setup.pop("totalMax")
        vdebug=setup.pop("debug",False)
        print_setup=setup.pop("print_setup",False)
        print_workflow=setup.pop("print_workflow",False)
        vqueue_prompt=setup.pop("queue_prompt",True)
        vqueue_prompt_wait=setup.pop("queue_prompt_wait",True)
        queue_loop=setup.pop("queue_loop",1)
        vsleep=setup.pop("sleep",0)
        
        debug("setup_start",setup)
        
        
        dicFileCheckpoint,dicFileLora,dicFileChar=setup_start(setup)
        debug("setup_start",setup)
        
        setup_checkpoint(setup)
        debug("setup_checkpoint",setup)
        
        setup_list(setup)
        debug("setup_list",setup)
        
        setup_lora_add(setup)
        debug("setup_lora_add",setup)
        
        #setup_lora_max(setup)
        #debug("setup_lora_max",setup)        
        
        #setup_dic(setup)
        #debug("setup_dic",setup)
        
        setup_workflow(setup)
        debug("setup_workflow",setup)
        
        #==============================================
        #setup_last(setup)
        #==============================================
        setup_bak=setup
        for j in range(queue_loop):
            workflow_api=readJson(Path(setup["Path"],"workflow_api.json"))
            setup=copy.deepcopy(setup_bak)
            #print(workflow_api)
            #print(type(workflow_api))
            
            workflow_setup(workflow_api,setup)
            debug("workflow_setup",setup)
            debug("workflow_setup",workflow_api)
            workflow_Loras(workflow_api,setup)
            debug("workflow_Loras",setup)
            debug("workflow_Loras",workflow_api)
            workflow_Wildcard(workflow_api,setup)
            debug("workflow_Wildcard",setup)
            debug("workflow_Wildcard",workflow_api)
            
            dicToJsonFile(workflow_api,"test.json")
            
            if print_setup:
                print("setup",setup)
            if print_workflow:
                print("workflow_api",workflow_api)
            
            #==============================================
            if vqueue_prompt:
                if queue_prompt(workflow_api,url=url):
                    pass
                    
            Setup_print(i,max,j,queue_loop)
            
            #==============================================
            if vqueue_prompt_wait:
                queue_prompt_wait(url=url)
            time.sleep(vsleep)
        #break
        
except KeyboardInterrupt:
    print('Interrupted')
    tm=time.strftime('%Y%m%d-%H%M%S')
    console.save_html(f"log/{tm}.html")
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)
except Exception:
    #console.print_exception(show_locals=True)
    console.print_exception()
    #console.save_html(logFile)
    #quit()