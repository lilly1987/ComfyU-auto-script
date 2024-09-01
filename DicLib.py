import os, sys, glob, random, time, copy, string, collections

def update(d, u):
    #print(f"[{ccolor}]update d: [/{ccolor}]",d)
    #print(f"[{ccolor}]update u: [/{ccolor}]",u)
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
    
