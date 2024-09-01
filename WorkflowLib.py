import copy
import os, sys, glob, random, time, copy, string, re, numbers

from ConsoleColor import print, console
from DicLib import *
from SetLib import *

positive={}
negative={}

def workflow_setup(workflow_api,setup):
    
    workflow=setup["workflow"]
    
    for item in workflow: 
        if item in workflow_api:
            #print(setup[item])
            #print(workflow_api[item])
            update(workflow_api[item]["inputs"],workflow[item])
            #print(workflow_api[item])
        
    global positive
    global negative
    positive=setup.get("positive",{})
    negative=setup.get("negative",{})
            
            
def SetArrRnd2(setup,d,f,k,v):
    if k in f :
        d[k]=f[k]
    else:
        d[k]=setup.get(k,v)
        
    r=SetArrRnd(d,k,v)    
    if r is None: 
        d.set(k,v)
    
def workflow_Loras(workflow_api,setup):
    
    LorasDic=setup["Loras"]
    
    global positive
    global negative
    
    LoraLoader=workflow_api["LoraLoader"]
    linputs=LoraLoader["inputs"]
    SetArrRnd2(setup,linputs,{},"A",(1.0,4.0))
    SetArrRnd2(setup,linputs,{},"B",(1.0,2.0))
    fname="CheckpointLoaderSimple"
    
    for k, v in LorasDic.items():
        #print(k, v)
        
        name=f"LoraLoader-{k}"
        workflow_api[name]=tLoraLoader=copy.deepcopy(LoraLoader)
        inputs=tLoraLoader["inputs"]
        update(inputs,v)
        
        if "positive" in inputs:
            update(positive,inputs.pop("positive"))
        if "negative" in inputs:
            update(negative,inputs.pop("negative"))
        SetSeed(inputs)
        SetArrRnd2(setup,inputs,v,"strength_model",1)
        SetArrRnd2(setup,inputs,v,"strength_clip",1)
        SetArrRnd2(setup,inputs,v,"A",(1.0,4.0))
        SetArrRnd2(setup,inputs,v,"B",(1.0,2.0))
        
        inputs["model"][0]=fname
        inputs["clip"][0]=fname
        linputs["model"][0]=name
        linputs["clip"][0]=name
        fname=name
        #print("inputs",inputs)
        
    #print("LoraLoader",LoraLoader)
    
def workflow_Wildcard(workflow_api,setup):
    global positive
    global negative
    #print("positive",positive)
    #print("negative",negative)
    
    lpositive=list(positive.values())
    lnegative=list(negative.values())
    
    if setup.get("shuffle",False):
        random.shuffle(lpositive)
        random.shuffle(lnegative)
    
    workflow_api["positive"]["inputs"]['wildcard_text']=",".join(lpositive)
    workflow_api["negative"]["inputs"]['wildcard_text']=",".join(lnegative)
    #workflow_api["negative"]["inputs"]['populated_text']=
    #workflow_api["positive"]["inputs"]['populated_text']=
    #print("positive",workflow_api["positive"]["inputs"]['populated_text'])
    #print("negative",workflow_api["negative"]["inputs"]['populated_text'])