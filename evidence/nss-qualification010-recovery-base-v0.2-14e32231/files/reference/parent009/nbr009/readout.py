"""Reader remains frozen; owner traversal is a separately labelled exact control."""
from .state import N
from nbr008.pipeline import read as neural_read,init_query,step_query
import numpy as np
import torch

@torch.no_grad()
def exact_owner_read(s,q,resolver,depth=8):
    before=s.signature();d=resolver(q[:,None,:],s.book,s.active);cur=d.index[:,0];alive=d.accept[:,0];out=[]
    b=len(q);r=torch.arange(b)
    for _ in range(depth):
        match=(s.owner==cur[:,None])&s.present&s.kr&s.vr&(s.owner_epoch==s.epoch[:,None])
        found=(match.sum(-1)==1)&alive;slot=match.long().argmax(-1)
        val=s.vals[r,slot];vd=resolver(val[:,None,:],s.book,s.active)
        alive=found&vd.accept[:,0];cur=torch.where(alive,vd.index[:,0],torch.full_like(cur,N));out.append(cur.clone())
    if s.signature()!=before:raise RuntimeError('Exact read mutated state')
    return torch.stack(out,1)

def logical_graph_arrays(owners,values,present,kr,vr,book,active,owner_epoch=None,epoch=None):
    """Audit view only. Uses candidate state, never expected facts to repair it."""
    b,cap=owners.shape;out=np.full((b,N+1),N,np.int64);counts=np.zeros((b,N),np.int64)
    for i in range(b):
        for j in range(cap):
            own=int(owners[i,j])
            if not present[i,j] or not (0<=own<N):continue
            counts[i,own]+=1
            if owner_epoch is not None and owner_epoch[i,j]!=epoch[i]:continue
            if not kr[i,j] or not vr[i,j] or not active[i,own]:continue
            value=values[i,j];dist=((book[i]-value)**2).sum(-1);dist[~active[i]]=np.inf
            unknown_dist=float((value[:-1]**2).sum()+(value[-1]-1)**2)
            if np.linalg.norm(value)<1e-6 or unknown_dist<=dist.min():continue
            out[i,own]=int(dist.argmin())
        out[i,:N][counts[i]>1]=N
    return out,counts
