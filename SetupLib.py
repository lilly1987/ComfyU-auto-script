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

ckptPath=None
ckptMax=64
listMax=8
ckptCnt=0
listCnt=0
listFile=None


def setup_loop(setup):

    global ckptMax
    global ckptCnt
    global listMax
    global listCnt
    
    ckptMax=setup.get("ckptMax",64)
    listMax=setup.get("listMax",8)
    ckptCnt-=1
    listCnt-=1
    
    global dicFileCheckpoint
    global dicFileLora

    dicFileCheckpoint=GetFileDic(setup["CheckpointPath"],dcheckpoints)
    dicFileLora=GetFileDic(setup["LoraPath"],dLora)    
    
    return dicFileCheckpoint,dicFileLora
    
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
    
    listLora=list(dicFileLora.keys())
    n=random.choice(listLora)
    d=w.setdefault("LoraLoader",{})
    d.setdefault("lora_name",str(dicFileLora[n]))
    
    #==============================================
    
    #print(wd)
    #print(dcheckpoints)

    global ckptMax
    global ckptCnt
    global ckptPath
    
    d=w.setdefault("CheckpointLoaderSimple",{})    
    if ckptCnt<=0:
        ckptCnt=ckptMax
        k=random.choice(list(dicFileCheckpoint.keys()))
        ckptPath=dicFileCheckpoint[k]

    d.setdefault("ckpt_name",str(ckptPath))    
    setup.setdefault("ckpt_name",ckptPath.stem)   
        

    
def setup_list(setup):
    global listMax
    global listCnt
    global listFile
    if listCnt<=0:
        listCnt=listMax
        global listDic
        listFiles=GetFileList("list/*.json")
        listFile=random.choice(listFiles)
        listDic=readDic(listFile)
        #setup["list_name"]=listFile.stem
        #list_name=listFile.stem
        if "loras" in listDic:
            listDic["Loras"]=listDic.pop("loras")
    setup.setdefault("list_name",listFile.stem)   
    
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
    
    global listDic
    update(setup,listDic)
    #print("listDic : ",listDic)
    
    
    #==============================================
    
    #print("Loras : ",Loras)    
    for k, v in Loras.items():
        if isinstance(v,str):
            d=dicLora.get(v,{})            
            #if d is None:
            #    continue
            f=dicFileLora.get(v)
            #print("dicFileLora",f)
            d.setdefault("lora_name",str(f))
            Loras[k]=d
            
def setup_last(setup):
    tm=time.strftime('%Y%m%d-%H%M%S')
    
    w=setup["workflow"]
    
    d=w.setdefault("SaveImage1",{})    
    d.setdefault("filename_prefix",f"{ckptPath.stem}-{listFile.stem}-{tm}-1")    
    d=w.setdefault("SaveImage2",{})    
    d.setdefault("filename_prefix",f"{ckptPath.stem}-{listFile.stem}-{tm}-2")    
    #workflow_api["SaveImage1"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-1"
    #workflow_api["SaveImage2"]["inputs"]['filename_prefix']=f"{ckptPath.stem}-{listFile.stem}-{tm}-2"
    
def Setup_print():
    print(f"{ckptCnt}/{ckptMax} ; {listCnt}/{listMax} ; {ckptPath.stem} ; {listFile.stem}")
    