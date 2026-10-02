"""Synthetic inputs. Hidden identities/origins returned for scoring ONLY."""
import numpy as np
import torch
from .common import data

FAMILIES=('known_exact','known_q05','known_q20','novel','novel_noisy20',
          'known_q40','known_scale025','known_scale2','erased','sentinel',
          'novel_near010','novel_near030','novel_near060','mixture',
          'known_raw02','known_raw08','known_raw16','removed')

def sample(rng,n,family,active_count=16):
    book=np.zeros((n,16,17),np.float32)
    book[:,:,:16]=data.normalize(rng.normal(size=(n,16,16))).astype(np.float32)
    ac=np.full(n,active_count) if np.isscalar(active_count) else np.asarray(active_count)
    active=np.arange(16)[None,:]<ac[:,None]
    book[~active]=0
    origin=np.array([rng.integers(k) for k in ac],dtype=np.int64)
    x=book[np.arange(n),origin].copy()
    known=family.startswith('known')
    if family.startswith('known_q'):
        sigma={'known_q05':.05,'known_q20':.2,'known_q40':.4}[family]
        x[:,:16]+=rng.normal(0,sigma,(n,16)).astype(np.float32);x=data.normalize(x).astype(np.float32)
    elif family.startswith('known_raw'):
        sigma={'known_raw02':.02,'known_raw08':.08,'known_raw16':.16}[family]
        x+=rng.normal(0,sigma,x.shape).astype(np.float32)
    elif family=='known_scale025':x*=.25
    elif family=='known_scale2':x*=2.
    elif family=='removed':
        active[np.arange(n),origin]=False;book[np.arange(n),origin]=0
    elif family in ('novel','novel_noisy20'):
        x.fill(0);x[:,:16]=data.normalize(rng.normal(size=(n,16))).astype(np.float32)
        if family=='novel_noisy20':
            x[:,:16]+=rng.normal(0,.2,(n,16)).astype(np.float32);x=data.normalize(x).astype(np.float32)
    elif family.startswith('novel_near'):
        sig={'novel_near010':.1,'novel_near030':.3,'novel_near060':.6}[family]
        x[:,:16]+=rng.normal(0,sig,(n,16)).astype(np.float32);x=data.normalize(x).astype(np.float32)
    elif family=='mixture':
        second=(origin+1)%ac;x=data.normalize((x+book[np.arange(n),second])*.5).astype(np.float32)
    elif family=='erased':x.fill(0)
    elif family=='sentinel':x.fill(0);x[:,-1]=1
    elif family!='known_exact':raise ValueError(family)
    return {'book':book,'active':active,'x':x[:,None,:],
            'target':origin if known else np.full(n,-1,dtype=np.int64),'known':np.full(n,known,dtype=bool)}

def training_batch(rng,n=256):
    fams=['known_exact','known_q05','known_q20','known_raw02','known_raw08','known_raw16',
          'novel','novel','novel_noisy20','novel_near030','mixture','novel_near060']
    parts=[]
    for i,f in enumerate(fams):
        count=n//len(fams)+(i<n%len(fams));counts=rng.choice([8,12,16],count)
        parts.append(sample(rng,count,f,counts))
    perm=rng.permutation(n)
    return {k:np.concatenate([p[k] for p in parts])[perm] for k in parts[0]}
