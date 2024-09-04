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

def setup_start(setup):

    global ckptMax
    global ckptCnt
    global listMax
    global listCnt
    global ckptPath
    global ckptFileName
    
    ckptMax=setup.get("ckptMax",64)
    listMax=setup.get("listMax",8)
    ckptCnt-=1
    listCnt-=1    
    
    global dicFileCheckpoint
    global dicFileLora
    global dicFileChar
    print(Path(setup["Path"],setup["CheckpointPath"]))
    dicFileCheckpoint=GetFileDic(str( Path(setup["Path"],setup["CheckpointPath"]) ),dcheckpoints)
    dicFileLora=GetFileDic(str(Path(setup["Path"],setup["LoraPath"])),dLora)    
    dicFileChar=GetFileDic(str(Path(setup["Path"],setup["CharPath"])),dLora)    

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
        updatek(workflow["KSampler"],d)
        updatek(workflow["FaceDetailer"],d)
    
    
    
def setup_workflow(setup):
    
    #==============================================
    global workflow
    workflow=setup.setdefault("workflow",{})
    
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
    
    listLora=list(dicFileChar.keys())
    n=random.choice(listLora)
    d=workflow.setdefault("LoraLoader",{})
    d.setdefault("lora_name",str(dicFileChar[n]))
    
    #==============================================
    
    #print(wd)
    #print(dcheckpoints)

    
    global ckptMax
    global ckptCnt
    global ckptPath
    
    d=workflow.setdefault("CheckpointLoaderSimple",{})    
    d.setdefault("ckpt_name",str(ckptPath))    
        


    
    
def setup_list(setup):
    global listMax
    global listCnt
    global listFile
    global listFileName
    if listCnt<=0:
        listCnt=listMax
        global listDic
        listFiles=GetFileList(str(Path(setup["Path"],"list/*.json")))
        if len(listFiles)>0:
            listFile=random.choice(listFiles)
            listFileName=listFile.stem
            listDic=readDic(listFile)
            #setup["list_name"]=listFile.stem
            #list_name=listFile.stem
            if "loras" in listDic:
                listDic["Loras"]=listDic.pop("loras")
        else:
            listFile=None
            listFileName=""
    setup.setdefault("list_name",listFileName)   
    
def setup_lora(setup):
    
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
    
    global listDic
    update(setup,listDic)
    #print("listDic : ",listDic)
    
    
    #==============================================
    dicLora={}
    dicFiles=GetFileList("dic/*.json")
    for f in dicFiles:
        update(dicLora,readDic(f))
    
    #print("Loras : ",Loras)    
    for k, v in Loras.items():
        if isinstance(v,str):
            d=dicLora.get(v)            
            if d is None:
                print("[yellow]Dic Lora No[/yellow] : ",v)
                d={}
            #    continue
            f=dicFileLora.get(v,dicFileChar.get(v))
            #print("dicFileLora",f)
            d.setdefault("lora_name",str(f))
            Loras[k]=d
            
def setup_last(setup):
    tm=time.strftime('%Y%m%d-%H%M%S')
    n=f"{ckptFileName}/{listFileName}/{ckptFileName}-{listFileName}-{tm}"
    
    w=setup["workflow"]
    
    d=w.setdefault("SaveImage1",{})    
    d.setdefault("filename_prefix",f"{n}-1")    
    d=w.setdefault("SaveImage2",{})    
    d.setdefault("filename_prefix",f"{n}-2")    
    #workflow_api["SaveImage1"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-1"
    #workflow_api["SaveImage2"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-2"
    
def Setup_print(i,max):
    print(f"{i}/{max} ; {ckptCnt}/{ckptMax} ; {listCnt}/{listMax} ; {ckptFileName} ; {listFileName}")
    