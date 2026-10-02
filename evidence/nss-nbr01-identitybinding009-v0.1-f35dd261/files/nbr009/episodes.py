"""Synthetic source events and isolated scorer data. No graph enters models."""
from .common import data
import numpy as np
import torch
from .state import N,D,OwnedState

def paired(seed,b=64,family='ordinary'):
    rng=np.random.default_rng(seed)
    codes=np.zeros((b,N+1,D),np.float32);codes[:,:N,:16]=data.normalize(rng.normal(size=(b,N,16))).astype(np.float32);codes[:,N,-1]=1
    ids=np.argsort(rng.random((b,N)),axis=-1).astype(np.int64)
    r=np.arange(b);old,new,room0,room1,room2,mid0,mid1,neighbor=[ids[:,j] for j in range(8)]
    def near(a,z,sigma):
        x=codes[r,a].copy();x[:,:16]+=rng.normal(0,sigma,(b,16)).astype(np.float32)
        codes[r,z]=data.normalize(x).astype(np.float32)
    if family in ('source01','both01'):near(old,new,.01)
    if family=='source10':near(old,new,.10)
    if family=='room01':near(room0,room1,.01)
    if family in ('middle01','both01'):near(mid0,mid1,.01)
    parent=np.full((b,N+1),N,np.int64)
    for room in (room0,room1,room2):parent[r,room]=room
    parent[r,mid0]=room0;parent[r,mid1]=room1;parent[r,old]=mid0;parent[r,neighbor]=room2
    # Existing noncritical records; distinct physical layout per stream.
    for j in range(8,12):parent[r,ids[:,j]]=room2
    active=np.ones((b,N),bool);active[r,new]=False
    book=codes[:,:N].copy();book[~active]=0
    alloc=np.argsort(rng.random((b,N)),axis=-1).astype(np.int64)
    return {'codes':codes,'ids':ids,'parent':parent,'active':active,'book':book,'allocation':alloc,'seed':seed,'family':family}

def build_state(p,binder,mode='identity',track='resolved',resolver=None):
    s=OwnedState(torch.from_numpy(p['book']),torch.from_numpy(p['active']),binder,allocation=torch.from_numpy(p['allocation']),mode=mode)
    b=len(p['codes']);r=np.arange(b)
    # Structured permitted source events, NOT target physical slot labels.
    for j in range(N):
        src=p['ids'][:,j];dst=p['parent'][r,src];allowed=(dst!=N)&p['active'][r,src]
        q=torch.from_numpy(p['codes'][r,src]);v=torch.from_numpy(p['codes'][r,dst])
        if track=='resolved':s.event(src,v,1,allowed)
        else:s.observed_event(q,v,resolver,1,allowed)
    return s
