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
    
def updatek(d, u, k):
    #print(f"[{ccolor}]update d: [/{ccolor}]",d)
    #print(f"[{ccolor}]update u: [/{ccolor}]",u)
    if k in u:
        if k in d:
            update(d[k], u[k])
        else:
            d[k]=u[k]
    return d


def updaten(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = updaten(d.get(k, {}), v)
        else:
            if not k in d:
                d[k] = v
    return d

        # A 
        #   B
        # C D
        # =ABC
        # !ABD