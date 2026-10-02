"""Prospective fresh capability fixtures. No labels are used in execution plans."""
import copy,math
import numpy as np
from retained_common import worlds

def make_episode(n:int,seed:int,family:str)->dict:
    rng=np.random.default_rng(seed)
    w=worlds(seed,1,n)[0];width=math.ceil(math.sqrt(n))
    # Public dependency links distributed across regions; no precomputed decisions.
    for i in range(n):
        eligible=[j for j in range(n) if j//width!=i//width]
        if len(eligible)<2:eligible=[j for j in range(n) if j!=i]
        w['deps'][i]=rng.choice(eligible,2,replace=False).tolist()
    targets=sorted(int(x) for x in rng.choice(n,min(8,n),replace=False))
    w['freeze']=0
    second=copy.deepcopy(w);change={}
    if family=='dispersed':
        dep=w['deps'][targets[0]][0]
        second['progress'][dep]^=1;change={'kind':'progress_revision','task':dep}
    elif family=='override':
        second['freeze']=1;change={'kind':'global_override','value':1}
    elif family=='resume':
        t=targets[0];old=list(w['deps'][t]);options=[j for j in range(n) if j!=t and j not in old]
        second['deps'][t]=[int(rng.choice(options)),old[1]]
        change={'kind':'dependency_revision','task':t,'old':old,'new':second['deps'][t]}
    else:raise ValueError(family)
    return {'id':f'n{n}_{seed}_{family}','n':n,'seed':seed,'family':family,'targets':targets,
            'worlds':[w,second],'change':change}

def exact_targets(world,targets):
    # Independently written scalar reference, not the retained vector oracle.
    out=[]
    for t in sorted(targets):
        if world['freeze']==1:answer=0
        elif world['progress'][t]==1:answer=1
        else:
            a,b=world['deps'][t]
            answer=2 if world['progress'][a]==1 and world['progress'][b]==1 else 3
        out.append(answer)
    return np.asarray(out,dtype=np.int64)

def grid():
    out=[]
    for n in [8,32,128]:
        for s in [1017101,1017102]:
            for f in ['dispersed','override','resume']:
                out.append({'stratum':'primary','episode':make_episode(n,s+n*100,f),'models':[8801,8802,8804],'caps':[32]})
    # Separate size-transfer stress; not three-seed confirmation.
    for f in ['dispersed','override','resume']:
        out.append({'stratum':'stress','episode':make_episode(512,1068301,f),'models':[8801],'caps':[32]})
    # Fixed additional tile sizes; no size or model selection based on results.
    for n in [128,512]:
        out.append({'stratum':'tile_sensitivity','episode':make_episode(n,1089101+n,'dispersed'),
                    'models':[8801],'caps':[16,64]})
    return out
