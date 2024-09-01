from ConsoleColor import print, console
from DicLib import *
from SetLib import *
from FileLib import *
from pathlib import *

wd=Path.cwd()
dcheckpoints=Path(wd,"../ComfyUI/models/checkpoints")
dLora=Path(wd,"../ComfyUI/models/Loras")
dicFileCheckpoint={}
dicFileLora={}

def SetSeed(d):
    if SetArrRnd(d,"seed") is None:
        d["seed"]=random.randint(0, 0xffffffffffffffff )

def setup_workflow(setup):
    
    #==============================================
    
    w=setup["workflow"]
    
    d=w.setdefault("KSampler",{})    
    SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
            
    d=w.setdefault("FaceDetailer",{})    
    SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
            
    d=w.setdefault("positive",{})
    SetSeed(d)            
        
    d=w.setdefault("negative",{})
    SetSeed(d)
    
    #==============================================
    
    #print(wd)
    #print(dcheckpoints)
    global dicFileCheckpoint
    global dicFileLora
    dicFileCheckpoint=GetFileDic(setup["CheckpointPath"],dcheckpoints)
    dicFileLora=GetFileDic(setup["LoraPath"],dLora)


        
    
    #print(PurePath.relative_to(Path(dLora),LoraFile))
    
    
    
    
    #==============================================
    
    return dicFileCheckpoint,dicFileLora
    #print(listLora)
    #print(clist)
    
def setup_lora(setup,dicLora):
    #==============================================
    
    Loras=setup.setdefault("Loras",{})
    
    #==============================================
    v=setup.setdefault("LoraAdd",True)
    if v:
        LoraAddCnt=SetArrRnd(setup,"LoraAddCnt")
        #print("LoraAddCnt",LoraAddCnt)
        listLora=list(dicFileLora.keys())
        for i in range(LoraAddCnt):
            #print(len(listLora1))
            if len(listLora)==0 :
                break
            name=random.choice(listLora)
            #name=loraFile.stem
            Loras[name]=name
            #print("name : ",name)
            listLora.remove(name)
    #==============================================
    
    #print("Loras : ",Loras)    
    for k, v in Loras.items():
        if isinstance(v,str):
            d=dicLora.get(v,{})
            #print("dicLora",d)
            #if d is None:
            #    continue
            f=dicFileLora.get(v)
            #print("dicFileLora",f)
            d.setdefault("lora_name",str(f))
            Loras[k]=d