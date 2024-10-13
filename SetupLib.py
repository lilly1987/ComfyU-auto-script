from ConsoleColor import print, console
from DicLib import *
from SetLib import *
from FileLib import *
from pathlib import *
import re

wd=Path.cwd()
pathCheckpointsDir=Path(wd,"../ComfyUI/models/checkpoints")
pathLoraDir=Path(wd,"../ComfyUI/models/Loras")
dicFileCheckpoint={}
dicFileLoraAll={}
dicFileLora={}
dicFileChar={}
loraFileNameToDicName={}
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

    dicFileCheckpoint=GetFileDic(str(Path(sPath,setup.pop("CheckpointPath"))),pathCheckpointsDir)
    dicFileLora=GetFileDic(str(Path(sPath,setup.pop("LoraPath"))),pathLoraDir)    
    dicFileChar=GetFileDic(str(Path(sPath,setup.pop("CharPath"))),pathLoraDir)    
    dicFileLoraAll=GetFileDic(str(Path("**/*.safetensors")),pathLoraDir)  
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
    dicTagLoraFiles=GetFileList("checkpoint/*.json")
    for f in dicTagLoraFiles:
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
        updatek(setup,d,"workflow")
        d.pop("workflow",{})
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
        ListCard=setup.pop("ListCard",[])
        perListCard=setup.pop("perListCard",1)
        perList=setup.pop("perList",1)
        if len(listFiles)>0:
            if perListCard >random.random() :
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
            if isNo and perList >random.random() :
                list=listFiles
                isNo=False
                
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
    
    
def lora_dic(dicTagLora,dicLoraFileNameToTag,l,loraSet,charSet,txt=""):
    global Loras
    #print("l",l)
    for k, v in l.copy().items():
        l.pop(k)
        if isinstance(v,str):
            file_name=v
            tag=dicLoraFileNameToTag.get(v)
            if tag is None:
                tag=v
            #else:
            #    name=v
            d=dicTagLora.get(tag)
            if d is None:
                print(f"[yellow]Dic Lora No -{txt}[/yellow] : ",tag)
                d={}
        else:
            file_name=k
            tag=k
            d=v
        #print("d",d) # {'positive': {'char': 'mayumi saegusa, red eyes, black hair, long hair, ,
        #print("file_name",file_name)  
        p=d.pop("per",1)
        if not p>=random.random():
            print(f"[cyan]SKIP -{txt}[/cyan] : ",tag)
            continue
            
        n=d.pop("file_name",file_name)
        #print(f"file_name : ",n)
        n=SetArrRndV(n)
        f=dicFileChar.get(n)                        
        if f is not None:
            dset=charSet
        else:
            f=dicFileLora.get(n)
            if f is None:
                f=dicFileLoraAll.get(n)
                if f is None:
                    print(f"[magenta]No Lora File -{txt}[/magenta] : ",n)
                    continue
            #    else:
            #        dset=loraSet
            #else:
            #    dset=loraSet
            dset=loraSet
                
        lora_name=d.setdefault("lora_name",str(f))
        updaten(d,dset)
        Loras[tag]=l[tag]=d
        #print("l",l)
        print(f"[green]lora_name -{txt}[/green]",file_name)
        
    return l
    
def setup_lora_add(setup):
    #==============================================
    dicTagLora={}
    dicTagLoraFiles=GetFileList("dic/*.json")
    for f in dicTagLoraFiles:
        update(dicTagLora,readDic(f))
    
    dicLoraFileNameToTag={}
    for k, v in dicTagLora.copy().items():
        #print("dicTagLora",k, v)
        a=v.get("file_name",None)
        if a is None:
            dicLoraFileNameToTag[k]=k
        else:
            if isinstance(a,str):
                dicLoraFileNameToTag[a]=k
            elif isinstance(a,list):
                for p in a:
                    dicLoraFileNameToTag[p]=k
            else:
                print(f"[yellow]err lora dic[/yellow] : ",k,a)
                dicTagLora.pop(k)
                
    #==============================================    
    global Loras
    charSet=setup.pop("charSet",{})
    randSet=setup.pop("randSet",{})
    loraSet=setup.pop("loraSet",{})
    
    
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    #print("test",SetArrRndV(setup.get("LoraMaxCnt")))
    max=SetArrRndV(setup.pop("LoraMaxCnt",0))
    #setup.pop("LoraMaxCnt")
    #==============================================
    for k, v in Loras.copy().items():
        Loras.pop(k)
        l=lora_dic(dicTagLora,dicLoraFileNameToTag,{k:v},loraSet,charSet,"Loras")
    now=len(Loras)
    if now>=max:
        #setup_lora_max(setup)
        print("now>=max Loras",now,max)
        return
    #==============================================
    v=setup.pop("LoraAdd",True)
    r=setup.pop("loras_random",{})
    if v:
        #==============================================
        if setup.pop("loras_random_mod") == "weights" :
            arv=[]
            arp=[]
            for k, v in r.items():                
                arp.append(v.get("per",1.0))
                arv.append(v)
                
            #print("arv : ",arv)
            #print("arp : ",arp)
            lst=random.choices(arv,weights =arp,k=SetArrRndV((1,max-now)) )
            #print("weights : ",lst)
            for v in lst:                
                l=SetArrRnd(v,"loras")
                l=lora_dic(dicTagLora,dicLoraFileNameToTag,l,randSet,charSet,f"random w {k}")
                now+=len(l)
            #print("now>=max weights",now,max)
            if now>=max:
                print("now>=max weights",now,max)
                return
        else:
            for k, v in r.items():
                p=v.pop("per",1.0)
                if p>=random.random():
                    l=SetArrRnd(v,"loras")
                    l=lora_dic(dicTagLora,dicLoraFileNameToTag,l,randSet,charSet,f"random a {k}")
                    now+=len(l)
                    if now>=max:
                        print("now>=max loras_random",now,max)
                        return
        ##==============================================
        LoraAddCnt=SetArrRndV(setup.pop("LoraAddCnt",0))
        listLora=list(dicFileLora.keys())
        for i in range(LoraAddCnt):
            if len(listLora)==0 :
                break
            name=random.choice(listLora)
            l=lora_dic(dicTagLora,dicLoraFileNameToTag,{name:name},loraSet,charSet,"add")
            now+=len(l)
            if now>=max:
                print("now>=max LoraAddCnt",now,max,i+1, LoraAddCnt)
                return
            listLora.remove(name)
    else:
        print("LoraAdd no")
    #setup.pop("LoraAddCnt")
    print("now>=max all",now,max)


def setup_workflow(setup):
    
    #==============================================
    global workflow    
    
    d=workflow.setdefault("KSampler",{})    

    d=workflow.setdefault("FaceDetailer",{})    

    d=workflow.setdefault("positiveWildcard",{})
        
    d=workflow.setdefault("negativeWildcard",{})
    
    global dicFileCharKeys
    n=random.choice(dicFileCharKeys)
    d=workflow.setdefault("LoraLoader",{})
    d.setdefault("lora_name",str(dicFileChar[n]))

    global ckptMax
    global ckptCnt
    global ckptPath
    
    d=workflow.setdefault("CheckpointLoaderSimple",{})    
    d.setdefault("ckpt_name",str(ckptPath))    

    n=f"{ckptFileName}/{listFileName}/{ckptFileName}-{listFileName}"

    d=workflow.setdefault("SaveImage1",{})    
    d.setdefault("filename_prefix",f"{n}")    
    d=workflow.setdefault("SaveImage2",{})    
    d.setdefault("filename_prefix",f"{n}")    
    
def Setup_print(i,max,j,queue_loop):
    print(f"{max-i}/{max} ; {ckptCnt}/{ckptMax} ; {listCnt}/{listMax} ; {queue_loop-j}/{queue_loop} ; {ckptFileName} ; {listFileName}")
    