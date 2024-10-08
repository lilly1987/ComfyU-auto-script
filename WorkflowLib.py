import copy
import os, sys, glob, random, time, copy, string, re, numbers

from ConsoleColor import print, console
from DicLib import *
from SetLib import *

positive={}
negative={}
image=None

def workflow_setup(workflow_api,setup):
    
    workflow=setup.pop("workflow")
    
    d=workflow.setdefault("KSampler",{})    
    SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
    d=workflow.setdefault("FaceDetailer",{})    
    SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
    d=workflow.setdefault("positiveWildcard",{})
    SetSeed(d)  
    d=workflow.setdefault("negativeWildcard",{})
    SetSeed(d)
    
    Loras=setup.get("Loras",{})
    for k, v in Loras.copy().items():
        if isinstance(v,str):
            print("[magenta]No Lora File -setup[/magenta] : ",v)
            Loras.pop(k)
            continue
        for k in v:
            SetArrRnd(v,k)
    
    tm=time.strftime('%Y%m%d-%H%M%S')
    
    d=workflow.setdefault("SaveImage1",{})    
    v=d.pop("filename_prefix","")  
    d.setdefault("filename_prefix",f"{v}-{tm}-1")    
    
    d=workflow.setdefault("SaveImage2",{})    
    v=d.pop("filename_prefix","")  
    d.setdefault("filename_prefix",f"{v}-{tm}-2")    
    
    
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
    
    if setup.pop("noFaceDetailer",False):
        global image
        i=workflow_api["FaceDetailer"]["inputs"]["image"]
        image=i.copy()
        #workflow_api["FaceDetailer"]["inputs"]["image"]=None
        del workflow_api["FaceDetailer"]["inputs"]["image"]
        #print(workflow_api)
    #workflow_api["FaceDetailer"]["inputs"].remove(image)
    
# SetArrRnd2(setup,linputs,{},"A",(1.0,4.0))
def SetArrRnd2(setup,d,f,k,v):
    if k in f :
        d[k]=f[k]
    if k in d :
        pass
    else:
        d[k]=setup.get(k,v)
    #print(f"d[{k}]" , d[k])
    r=SetArrRnd(d,k,v)    
    if r is None: 
        d.set(k,v)
    
def workflow_Loras(workflow_api,setup):
    
    LorasDic=setup.pop("Loras")
    
    global positive
    global negative
    positive=setup.get("positive",{})
    negative=setup.get("negative",{})
    
    LoraLoader=workflow_api["LoraLoader"]
    linputs=LoraLoader["inputs"]
    fname="CheckpointLoaderSimple"
    
    for k, v in LorasDic.items():
        #print(k, v)
        
        name=f"LoraLoader-{k}"
        workflow_api[name]=tLoraLoader=copy.deepcopy(LoraLoader)
        inputs=tLoraLoader["inputs"]
        del inputs["seed"]
        update(inputs,v)
        
        if "positive" in inputs:
            update(positive,inputs.pop("positive"))
        if "negative" in inputs:
            update(negative,inputs.pop("negative"))
        #print("inputs",inputs)
        SetSeed(inputs)
        #print("inputs",inputs)
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
        
    SetArrRnd2(setup,linputs,{},"A",(1.0,4.0))
    SetArrRnd2(setup,linputs,{},"B",(1.0,2.0))
    #print("LoraLoader",LoraLoader)
    
def workflow_Wildcard(workflow_api,setup):
    global positive
    global negative
    #print("positive",positive)
    #print("negative",negative)
    positive=setup.pop("positive",{})
    negative=setup.pop("negative",{})
    
    lpositive=list(positive.values())
    lnegative=list(negative.values())
    
    if setup.pop("shuffle",False):
        random.shuffle(lpositive)
        random.shuffle(lnegative)
    
    workflow_api["positiveWildcard"]["inputs"]['wildcard_text']=",".join(lpositive)
    workflow_api["negativeWildcard"]["inputs"]['wildcard_text']=",".join(lnegative)
    #workflow_api["negative"]["inputs"]['populated_text']=
    #workflow_api["positive"]["inputs"]['populated_text']=
    #print("positive",workflow_api["positive"]["inputs"]['populated_text'])
    #print("negative",workflow_api["negative"]["inputs"]['populated_text'])