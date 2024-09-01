
from ConsoleColor import print, console
from DicLib import *

def workflow_setup(workflow_api,setup):
    for item in setup: 
        if item in workflow_api:
            #print(setup[item])
            #print(workflow_api[item])
            update(workflow_api[item]["inputs"],setup[item])
            #print(workflow_api[item])
            
            
def workflow_Loras(workflow_api,LorasDic):
    for k, v in LorasDic.items():
        print(k, v)
        