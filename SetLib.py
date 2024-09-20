import os, sys, glob, json, random, time, copy, string, collections
from ConsoleColor import print, console


def SetArrRndV(v):
    if isinstance(v,tuple):
        #print(v)
        if isinstance(v[0], float) or isinstance(v[1], float):
            v=random.uniform(v[0],v[1])
        elif isinstance(v[0], int):
            v=random.randint(v[0],v[1])
        #print(d[k])
    elif isinstance(v,list):
        #print(v)
        if len(v)>0:
            v=random.choice(v)
        else:
            v=None
    return v


def SetArrRnd(d,k,v=None):
    try:
        if k in d:
            v=d[k]
            v=d[k]=SetArrRndV(v)
            #if isinstance(v,tuple):
            #    #print(v)
            #    if isinstance(v[0], float) or isinstance(v[1], float):
            #        v=d[k]=random.uniform(v[0],v[1])
            #    elif isinstance(v[0], int):
            #        v=d[k]=random.randint(v[0],v[1])
            #    #print(d[k])
            #elif isinstance(v,list):
            #    #print(v)
            #    v=d[k]=random.choice(v)
        elif not v is None :
            d[k]=v
        return v
    except Exception:
        print("d : ",d,style="reset")
        print("k : ",k,style="reset")
        print("v : ",v,style="reset")
        raise
    
def SetSeed(d):
    if SetArrRnd(d,"seed") is None:
        d["seed"]=random.randint(0, 0xffffffffffffffff )