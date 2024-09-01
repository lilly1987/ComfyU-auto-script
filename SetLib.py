import os, sys, glob, json, random, time, copy, string, collections
from ConsoleColor import print, console

def SetArrRnd(d,k,v=None):
    if k in d:
        v=d[k]
        if isinstance(v,tuple):
            #print(v)
            if isinstance(v[0], float) or isinstance(v[1], float):
                v=d[k]=random.uniform(v[0],v[1])
            elif isinstance(v[0], int):
                v=d[k]=random.randint(v[0],v[1])
            #print(d[k])
        elif isinstance(v,list):
            #print(v)
            v=d[k]=random.choice(v)
    elif not v is None :
        d[k]=v
    return v