"""Frozen learned relation traversal, with explicit no-match propagation.

Each learned hop still uses the inherited trained matcher/GRU. The resolver
never chooses the next graph edge. Exact traversal is a labelled control.
"""
import torch
from torch.nn import functional as F
from .state import State
from .common import data

def make_problem(seed,h=4,b=64,n=16):
    import numpy as np
    parts=[data.batch(np.random.default_rng(seed+300001*int(m)),b//2,n=n,max_h=h,hops=h,missing=m) for m in (False,True)]
    p={k:np.concatenate([x[k] for x in parts]) for k in parts[0]}
    if n<16:
        book=np.zeros((b,17,17),np.float32);book[:,:n]=p['codes'][:,:n];book[:,16,-1]=1
        parent=np.full((b,17),16,np.int64);parent[:,:n]=np.where(p['parent'][:,:n]==n,16,p['parent'][:,:n]);p['parent']=parent;p['codes']=book
        k=np.zeros((b,16,17),np.float32);v=k.copy();e=np.zeros((b,16),bool)
        k[:,:n]=p['keys'];v[:,:n]=p['vals'];e[:,:n]=p['present'];p['keys']=k;p['vals']=v;p['present']=e
    return p

def install(p,binder,resolver=None,learned=False):
    book=torch.from_numpy(p['codes'][:,:16]);active=book.square().sum(-1)>.5
    s=State(book,active,binder)
    if learned:
        b=len(book);r=torch.arange(b)
        for j in range(p['slot_ids'].shape[1]):
            ids=torch.from_numpy(p['slot_ids'][:,j]);dst=torch.from_numpy(p['parent'][r.numpy(),ids.numpy()])
            src=torch.from_numpy(p['codes'][r.numpy(),ids.numpy()]);val=torch.from_numpy(p['codes'][r.numpy(),dst.numpy()])
            s.event(src,val,1,resolver,qualified=dst!=16)
    else:
        s.store.keys.copy_(torch.from_numpy(p['keys']));s.store.vals.copy_(torch.from_numpy(p['vals']));s.present.copy_(torch.from_numpy(p['present']));s.kr.copy_(s.present);s.vr.copy_(s.present)
    return s

def init_query(q):
    return {'h':q.clone(),'alive':torch.ones(len(q),dtype=torch.bool),'round':torch.zeros(len(q),dtype=torch.int64)}

@torch.no_grad()
def step_query(s,reader,resolver,qs,exact=False):
    h=qs['h'];alive=qs['alive'];d=resolver(h[:,None,:],s.book,s.active)
    # none/normalize retain earlier reader baseline, including exact UNKNOWN input.
    if resolver.method not in ('none','normalize'):
        alive=alive&d.accept[:,0]
    h=d.value[:,0]
    valid=s.present&s.kr&s.vr
    if exact:
        # Resolve key identities using the SAME state; no gold graph or target slots.
        kd=resolver(s.store.keys,s.book,s.active)
        query_idx=d.index[:,0]
        match=(kd.index==query_idx[:,None])&valid&kd.accept&(query_idx[:,None]>=0)
        found=match.any(-1)&alive;sel=match.long().argmax(-1)
        next_h=s.store.vals[torch.arange(len(h)),sel].clone()
        null=torch.zeros_like(next_h);null[:,-1]=1
        next_h=torch.where(found[:,None],next_h,null)
    else:
        # One authentic inherited learned step. No exact slot supplied.
        next_h=reader(s.store.keys,s.store.vals,valid,h,1)[:,0]
    null=torch.zeros_like(next_h);null[:,-1]=1
    next_h=torch.where(alive[:,None],next_h,null)
    new={'h':next_h,'alive':alive,'round':qs['round']+1}
    return new,d

@torch.no_grad()
def read(s,reader,resolver,q,depth=8,exact=False,qs=None,expected_revision=None,scope=None):
    s.validate(expected_revision,scope)
    before=s.signature();qs=init_query(q) if qs is None else qs
    outputs=[];ids=[];accepted=[];feats=[];scores=[];statuses=[]
    for _ in range(depth):
        qs,d=step_query(s,reader,resolver,qs,exact)
        # Read-only final decode at each declared round. Does not change recurrent h.
        final=resolver(qs['h'][:,None,:],s.book,s.active)
        idx=final.index[:,0]
        if resolver.method in ('none','normalize'):
            full=torch.zeros((len(q),17,17));full[:,:16]=s.book;full[:,16,-1]=1
            mask=torch.cat([s.active,torch.ones((len(q),1),dtype=torch.bool)],-1)
            score=torch.einsum('bd,bnd->bn',F.normalize(qs['h'],dim=-1),full).masked_fill(~mask,-1e6)
            idx=score.argmax(-1)
        else:idx=torch.where(qs['alive']&final.accept[:,0],idx,torch.full_like(idx,16))
        outputs.append(idx);ids.append(d.index[:,0]);accepted.append(d.accept[:,0]);feats.append(d.feat[:,0]);scores.append(d.score[:,0]);statuses.append(d.status[:,0])
    if before!=s.signature():raise RuntimeError('Query mutated record/registry state')
    return {'pred':torch.stack(outputs,1),'matched':torch.stack(ids,1),'accepted':torch.stack(accepted,1),'raw_features':torch.stack(feats,1),'match_score':torch.stack(scores,1),'status':torch.stack(statuses,1),'qs':qs}
