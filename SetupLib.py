from ConsoleColor import print, console
from DicLib import *
from SetLib import *
from FileLib import *
from pathlib import *
import re

wd=Path.cwd()
dcheckpoints=Path(wd,"../ComfyUI/models/checkpoints")
dLora=Path(wd,"../ComfyUI/models/Loras")
dicFileCheckpoint={}
dicFileLoraAll={}
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
    Loras=setup.setdefault("Loras",setup.pop("loras",{}))
    
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
    global dicFileLoraAll

    dicFileCheckpoint=GetFileDic(str(Path(sPath,setup.pop("CheckpointPath"))),dcheckpoints)
    dicFileLora=GetFileDic(str(Path(sPath,setup.pop("LoraPath"))),dLora)    
    dicFileChar=GetFileDic(str(Path(sPath,setup.pop("CharPath"))),dLora)    
    dicFileLoraAll=GetFileDic(str(Path("**/*.safetensors")),dLora)  
    #print("dicFileLoraAll",dicFileLoraAll)    
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
    global dicFileChar
    global dicFileCharKeys
    
    if listCnt<=0:
        listCnt=listMax
        listFiles=GetFileList(str(Path(sPath,"list/*.json")))
        isNo=True
        listFileName=random.choice(dicFileCharKeys)
        if len(listFiles)>0:
            if setup.pop("perListCard",1) >random.random() :
                ListCard=setup.pop("ListCard",[])
                card=random.choice(ListCard) #str
                list=[ f for f in listFiles if re.search(card,  f.stem)]
                if len(list)>0:
                    isNo=False
                else:
                    list=[ dicFileChar.get(f) for f in dicFileCharKeys if re.search(card,  f)] 
                    if len(list)>0:
                        listFile=random.choice(list)
                        listFileName=listFile.stem
                #print("list",list)
            if isNo and setup.pop("perList",1) >random.random() :
                list=listFiles
                isNo=False
        else:
            setup.pop("perList",1)
            setup.pop("perListCard",1)
            setup.pop("ListCard",[])
        if isNo:
            listDic={
                "Loras":{
                    listFileName : listFileName,
                },
            }
        else:
            listFile=random.choice(list)
            listFileName=listFile.stem
            listDic=readDic(listFile)
            if "loras" in listDic:
                listDic["Loras"]=listDic.pop("loras")
                
    setup.setdefault("list_name",listFileName)   
    update(setup,listDic)
    
    
def lora_dic(dicLora,l,loraSet,charSet):
    global Loras
    #print("l",l)
    for k, v in l.items():
        
        if isinstance(v,str):
            name=v
            d=dicLora.get(v)
            if d is None:
                print("[yellow]Dic Lora No[/yellow] : ",v)
                d={}
        else:
            d=v
            name=k
        #print("d",d) # {'positive': {'char': 'mayumi saegusa, red eyes, black hair, long hair, ,
        
        n=d.pop("file_name",name)
        f=dicFileChar.get(n)                
        if f is not None:
            dset=charSet
        else:
            f=dicFileLora.get(n)
            if f is None:
                #print("[yellow]No Lora File[/yellow] : ",n)
                #continue 
                f=dicFileLoraAll.get(n)
                if f is None:
                    print("[yellow]No Lora File[/yellow] : ",n)
                    continue
            #    else:
            #        dset=loraSet
            #else:
            #    dset=loraSet
            dset=loraSet
                
        lora_name=d.setdefault("lora_name",str(f))
        updaten(d,dset)
        Loras[k]=l[k]=d
        #print("l",l)
        print("[green]lora_name[/green]",name)
        
    return l
    
def setup_lora_add(setup):
    #==============================================
    dicLora={}
    dicFiles=GetFileList("dic/*.json")
    for f in dicFiles:
        update(dicLora,readDic(f))
    #==============================================    
    global Loras
    charSet=setup.pop("charSet",{})
    loraSet=setup.pop("randSet",{})
    
    max=SetArrRnd(setup,"LoraMaxCnt")
    #==============================================
    for k, v in Loras.items():
        l=lora_dic(dicLora,{k:v},loraSet,charSet)
    now=len(Loras)
    if now>=max:
        #setup_lora_max(setup)
        return
    #==============================================
    v=setup.pop("LoraAdd",True)
    if v:
        
        #==============================================
        r=setup.pop("loras_random",{})
        for k, v in r.items():
            p=v.pop("per",1.0)
            if p>=random.random():
                l=SetArrRnd(v,"loras")
                l=lora_dic(dicLora,l,loraSet,charSet)
                now+=1
                if now>=max:
                    return
        ##==============================================
        LoraAddCnt=SetArrRnd(setup,"LoraAddCnt")
        setup.pop("LoraAddCnt")
        loraSet=setup.pop("loraSet",{})
        listLora=list(dicFileLora.keys())
        for i in range(LoraAddCnt):
            if len(listLora)==0 :
                break
            name=random.choice(listLora)
            l=lora_dic(dicLora,{name:name},loraSet,charSet)
            now+=1
            if now>=max:
                return
            listLora.remove(name)

def setup_lora_max(setup):
    #Loras=setup.get("Loras")
    global Loras
    #print("Loras",Loras)
    n=SetArrRnd(setup,"LoraMaxCnt")
    Loras={k:v for i, (k, v) in enumerate(Loras.items()) if i < n}
    # print("Loras",Loras)
    setup["Loras"]=Loras
        
    
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
            v=d.pop("file_name",v)
            f=dicFileChar.get(v)
            if f is None:
                #print("[yellow]Dic No Char[/yellow] : ",v)
                f=dicFileLora.get(v)
                if f is None:
                    #print("[yellow]No Lora File[/yellow] : ",v)
                    #continue
                    f=dicFileLoraAll.get(v)
                    if f is None:
                        print("[yellow]No Lora File[/yellow] : ",v)
                        continue
            else:
                char=True
                
            #print("dicFileLora",f)
            
            lora_name=d.setdefault("lora_name",str(f))
            print("[green]lora_name[/green]",lora_name)
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
    #SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
            
    d=workflow.setdefault("FaceDetailer",{})    
    #SetSeed(d)
    SetArrRnd(d,"denoise")
    for k in d:
        SetArrRnd(d,k)
            
    d=workflow.setdefault("positiveWildcard",{})
    # SetSeed(d)            
        
    d=workflow.setdefault("negativeWildcard",{})
    #SetSeed(d)
    
    
    global dicFileCharKeys
    n=random.choice(dicFileCharKeys)
    d=workflow.setdefault("LoraLoader",{})
    d.setdefault("lora_name",str(dicFileChar[n]))
    
    #==============================================
    global Loras
    for k, v in Loras.items():
        if isinstance(v,str):
            print("[yellow]No Lora File[/yellow] : ",v)
            Loras.pop(k)
            continue
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
    #tm=time.strftime('%Y%m%d-%H%M%S')
    #n=f"{ckptFileName}/{listFileName}/{ckptFileName}-{listFileName}-{tm}"
    n=f"{ckptFileName}/{listFileName}/{ckptFileName}-{listFileName}"
    
    #workflow=setup["workflow"]
    
    d=workflow.setdefault("SaveImage1",{})    
    d.setdefault("filename_prefix",f"{n}")    
    d=workflow.setdefault("SaveImage2",{})    
    d.setdefault("filename_prefix",f"{n}")    
    
def Setup_print(i,max,j,queue_loop):
    print(f"{max-i}/{max} ; {ckptCnt}/{ckptMax} ; {listCnt}/{listMax} ; {queue_loop-j}/{queue_loop} ; {ckptFileName} ; {listFileName}")
    