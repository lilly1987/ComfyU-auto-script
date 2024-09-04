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
dicFileChar={}
dicFileCharKeys=[]
dicCheckpoint={} # Checkpoint 사전
listDic={} #  사전

ckptPath=None
ckptMax=64
listMax=8
ckptCnt=0
listCnt=0
listFile=None
listFileName=""
ckptFileName=""
workflow={}
Loras={}
sPath=None

def setup_start(setup):

    
    global sPath
    sPath=setup["Path"]
    
    global workflow
    workflow=setup.setdefault("workflow",{})
    global Loras
    Loras=setup.setdefault("Loras",{})
    
    global ckptMax
    global ckptCnt
    global listMax
    global listCnt
    ckptMax=setup.pop("ckptMax",64)
    listMax=setup.pop("listMax",8)
    ckptCnt-=1
    listCnt-=1    
    
    global dicFileCheckpoint
    global dicFileLora
    global dicFileChar
    global dicFileCharKeys

    dicFileCheckpoint=GetFileDic(str(Path(sPath,setup.pop("CheckpointPath"))),dcheckpoints)
    dicFileLora=GetFileDic(str(Path(sPath,setup.pop("LoraPath"))),dLora)    
    dicFileChar=GetFileDic(str(Path(sPath,setup.pop("CharPath"))),dLora)    
    dicFileCharKeys=list(dicFileChar.keys())

    global ckptPath
    global ckptFileName
    if ckptCnt<=0:
        ckptCnt=ckptMax
        k=random.choice(list(dicFileCheckpoint.keys()))
        ckptPath=dicFileCheckpoint[k]
        ckptFileName=ckptPath.stem
    setup.setdefault("ckpt_name",ckptFileName)   
    #print(type(ckptPath))
    #print(ckptPath)
    return dicFileCheckpoint,dicFileLora,dicFileChar
    
def setup_checkpoint(setup):
    global workflow
    global dicCheckpoint
    dicCheckpoint={}
    dicFiles=GetFileList("checkpoint/*.json")
    for f in dicFiles:
        update(dicCheckpoint,readDic(f))
    
    name=setup.get("ckpt_name")
    d=dicCheckpoint.get(name)
    if d is None:
        print("[yellow]Dic Checkpoint No[/yellow] : ",name)
    else:
    #print("dicCheckpoint : ",d)
        updatek(setup,d,"negative")
        updatek(setup,d,"positive")
        d.pop("positive",{})
        d.pop("negative",{})
        update(workflow["KSampler"],d)
        update(workflow["FaceDetailer"],d)
    
    
    
  
def setup_list(setup):
    global listMax
    global listCnt
    global listFile
    global listFileName
    global listDic
    global sPath
    if listCnt<=0:
        listCnt=listMax
        listFiles=GetFileList(str(Path(sPath,"list/*.json")))
        if len(listFiles)>0 and setup.pop("perList",1) >random.random() :
            listFile=random.choice(listFiles)
            listFileName=listFile.stem
            listDic=readDic(listFile)
            #setup["list_name"]=listFile.stem
            #list_name=listFile.stem
            if "loras" in listDic:
                listDic["Loras"]=listDic.pop("loras")
        else:            
            global dicFileCharKeys
            listFileName=random.choice(dicFileCharKeys)
            listDic={
                "Loras":{
                    listFileName : listFileName,
                },
            }
            #listFile=None
            #listFileName=""
    setup.setdefault("list_name",listFileName)   
    update(setup,listDic)

def setup_lora_add(setup):

    global Loras

    v=setup.pop("LoraAdd",True)
    if v:
        LoraAddCnt=SetArrRnd(setup,"LoraAddCnt")
        setup.pop("LoraAddCnt")
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

def setup_dic(setup):
    
    #==============================================
    dicLora={}
    dicFiles=GetFileList("dic/*.json")
    for f in dicFiles:
        update(dicLora,readDic(f))
    
    global Loras
    
    #print("Loras : ",Loras)    
    for k, v in Loras.items():
        char=False
        if isinstance(v,str):
            d=dicLora.get(v)            
            if d is None:
                print("[yellow]Dic Lora No[/yellow] : ",v)
                d={}
            #else:
            #    print("[green]Dic Lora add[/green] : ",v)
            #    continue
            f=dicFileChar.get(v)
            if f is None:
                f=dicFileLora.get(v,v)
            else:
                char=True
                
            #print("dicFileLora",f)
            d.setdefault("lora_name",str(f))
            v=Loras[k]=d
        
        if char or dicFileChar.get(k) is not None :
            dset=setup.pop("charSet",{
            "strength_model": (0.75,1.0),
            "strength_clip": 1,
        })
        else:
            dset=setup.pop("loraSet",{
            "strength_model": (0.0,1.0),
            "strength_clip": 1,
        })
        updaten(v,dset)



def setup_workflow(setup):
    
    #==============================================
    global workflow
    
    
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
    
    
    global dicFileCharKeys
    n=random.choice(dicFileCharKeys)
    d=workflow.setdefault("LoraLoader",{})
    d.setdefault("lora_name",str(dicFileChar[n]))
    
    #==============================================
    global Loras
    for k, v in Loras.items():
        for k in v:
            SetArrRnd(v,k)
    #print(wd)
    #print(dcheckpoints)

    
    global ckptMax
    global ckptCnt
    global ckptPath
    
    d=workflow.setdefault("CheckpointLoaderSimple",{})    
    d.setdefault("ckpt_name",str(ckptPath))    
      
#def setup_last(setup):
    tm=time.strftime('%Y%m%d-%H%M%S')
    n=f"{ckptFileName}/{listFileName}/{ckptFileName}-{listFileName}-{tm}"
    
    #workflow=setup["workflow"]
    
    d=workflow.setdefault("SaveImage1",{})    
    d.setdefault("filename_prefix",f"{n}-1")    
    d=workflow.setdefault("SaveImage2",{})    
    d.setdefault("filename_prefix",f"{n}-2")    
    #workflow_api["SaveImage1"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-1"
    #workflow_api["SaveImage2"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-2"
    
def Setup_print(i,max):
    print(f"{i}/{max} ; {ckptCnt}/{ckptMax} ; {listCnt}/{listMax} ; {ckptFileName} ; {listFileName}")
    