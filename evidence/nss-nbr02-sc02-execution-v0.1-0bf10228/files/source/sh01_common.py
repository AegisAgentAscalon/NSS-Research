"""Typed-record maintenance reader and native selected-edge HSA. See PROTOCOL.md."""
from __future__ import annotations
import hashlib, json, math, os, time
from pathlib import Path
from typing import Any
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

CLASSES = ['DEFER','COMPLETE','READY','BLOCKED']
D_IN=37
G=4

def canonical(x: Any) -> bytes:
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def write_json(p: Path,x: Any):
    p.parent.mkdir(parents=True,exist_ok=True)
    b=canonical(x); temp=p.with_suffix(p.suffix+'.tmp'); temp.write_bytes(b); os.replace(temp,p)
def setup():
    torch.set_num_threads(1); torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)

def worlds(seed:int,count:int,n:int) -> list[dict]:
    r=np.random.default_rng(seed); out=[]
    for w in range(count):
        codes=r.normal(size=(n,8)); codes/=np.linalg.norm(codes,axis=1,keepdims=True)
        deps=[]
        for i in range(n): deps.append(r.choice([j for j in range(n) if j!=i],2,replace=False).tolist())
        # Explicit observable evidence, not desired policy labels.
        out.append({'id':f'{seed}:{w}', 'codes':codes.tolist(),'deps':deps,
                    'progress':r.integers(0,2,n).tolist(),'receipts':r.integers(0,2,n).tolist(),
                    'constraints':r.integers(0,2,n).tolist(),'freeze':int(r.random()<0.15),
                    'nuisance':r.normal(0,0.25,size=(n,4)).tolist()})
    return out

def oracle(w:dict) -> np.ndarray:
    p=w['progress']
    return np.array([0 if w['freeze'] else 1 if p[i] else
                    2 if all(p[d] for d in w['deps'][i]) else 3 for i in range(len(p))],np.int64)

def compile_world(w:dict):
    """Compiler supplies metadata and evidence; never inspects policy targets."""
    n=len(w['progress']); width=math.ceil(math.sqrt(n)); nr=math.ceil(n/width)
    t=n*G+nr+1; glob=t-1
    x=np.zeros((t,D_IN),np.float32)
    codes=np.asarray(w['codes'],np.float32)
    for i in range(n):
        for role in range(G):
            a=i*G+role; x[a,role]=1
            x[a,6:14]=codes[i]
            if role==0:
                x[a,14:22]=codes[w['deps'][i][0]]
                x[a,22:30]=codes[w['deps'][i][1]]
            if role==1:x[a,30]=2*w['progress'][i]-1
            if role==2:x[a,31]=2*w['receipts'][i]-1
            if role==3:x[a,32]=2*w['constraints'][i]-1
            x[a,33:37]=w['nuisance'][i]
    for rr in range(nr):
        a=n*G+rr;x[a,4]=1;x[a,6:14]=codes[rr*width:min(n,(rr+1)*width)].mean(0)
    x[glob,5]=1;x[glob,32]=2*w['freeze']-1
    rows=[]
    for i in range(n):
        rr=i//width
        allowed=set(range(i*G,(i+1)*G))
        allowed.update(j*G for j in range(rr*width,min(n,(rr+1)*width)))
        for dep in w['deps'][i]: allowed.update(range(dep*G,(dep+1)*G))
        allowed.update(range(n*G,t))
        for role in range(G): rows.append(sorted(allowed))
    for rr in range(nr):
        rows.append(sorted({n*G+rr,glob}|{i*G for i in range(rr*width,min(n,(rr+1)*width))}))
    rows.append(list(range(n*G,t)))
    # A fixed layout bound, independent of labels. Padding is explicitly charged.
    k=G*3+width+nr+1
    idx=np.zeros((t,k),np.int64);valid=np.zeros((t,k),bool)
    for a,row in enumerate(rows):
        assert len(row)<=k
        idx[a,:len(row)]=row;idx[a,len(row):]=a;valid[a,:len(row)]=True
    return x,idx,valid

def batch(ws:list[dict]):
    triples=[compile_world(w) for w in ws]
    return tuple(torch.from_numpy(np.stack([r[k] for r in triples])) for k in range(3))+(
        torch.from_numpy(np.stack([oracle(w) for w in ws])),)

def sparse_attention(q:torch.Tensor,k:torch.Tensor,v:torch.Tensor,idx:torch.Tensor,valid:torch.Tensor):
    """q,k,v[B,H,T,D], idx/valid[B,T,K]. No full pairwise scores allocated."""
    b,h,t,d=q.shape; width=idx.shape[-1]
    # Advanced indexing allocates [B,H,T,K,D], not [B,H,T,T].
    bi=torch.arange(b,device=q.device)[:,None,None,None]
    hi=torch.arange(h,device=q.device)[None,:,None,None]
    keys=k[bi,hi,idx[:,None,:,:],:]
    vals=v[bi,hi,idx[:,None,:,:],:]
    scores=(q.unsqueeze(-2)*keys).sum(-1)/math.sqrt(d)
    scores=scores.masked_fill(~valid[:,None,:,:],float('-inf'))
    return (scores.softmax(-1).unsqueeze(-1)*vals).sum(-2)

def masked_attention(q,k,v,idx,valid):
    b,h,t,d=q.shape
    mask=torch.zeros((b,t,t),device=q.device,dtype=torch.bool)
    # invalid padded entries must never clear existing true entries.
    for z in range(b):
        rr=torch.arange(t,device=q.device)[:,None].expand_as(idx[z])
        mask[z,rr[valid[z]],idx[z][valid[z]]]=True
    score=(q@k.transpose(-2,-1))/math.sqrt(d)
    return score.masked_fill(~mask[:,None],float('-inf')).softmax(-1)@v

class Block(nn.Module):
    def __init__(self,d=32,heads=2):
        super().__init__(); self.d=d;self.heads=heads
        self.norm1=nn.LayerNorm(d); self.qkv=nn.Linear(d,3*d);self.proj=nn.Linear(d,d)
        self.norm2=nn.LayerNorm(d);self.ff=nn.Sequential(nn.Linear(d,64),nn.GELU(),nn.Linear(64,d))
    def forward(self,x,idx,valid,mode):
        b,t,d=x.shape;y=self.norm1(x)
        q,k,v=self.qkv(y).reshape(b,t,3,self.heads,d//self.heads).permute(2,0,3,1,4).unbind(0)
        if mode=='hsa': a=sparse_attention(q,k,v,idx,valid)
        elif mode=='masked':a=masked_attention(q,k,v,idx,valid)
        else:a=F.scaled_dot_product_attention(q,k,v,dropout_p=0.0)
        x=x+self.proj(a.transpose(1,2).reshape(b,t,d))
        return x+self.ff(self.norm2(x))

class Reader(nn.Module):
    def __init__(self):
        super().__init__();self.enc=nn.Linear(D_IN,32);self.blocks=nn.ModuleList([Block(),Block()])
        self.norm=nn.LayerNorm(32);self.head=nn.Linear(32,4)
    def forward(self,x,idx,valid,n:int,mode:str):
        z=self.enc(x)
        for block in self.blocks:z=block(z,idx,valid,mode)
        return self.head(self.norm(z[:,0:n*G:G]))

def model_hash(m:nn.Module):
    h=hashlib.sha256()
    for k,v in sorted(m.state_dict().items()):h.update(k.encode());h.update(v.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def metrics(y:np.ndarray,p:np.ndarray):
    c=np.zeros((4,4),np.int64)
    for a,b in zip(y.ravel(),p.ravel()):c[a,b]+=1
    recall=np.divide(c.diagonal(),c.sum(1),out=np.zeros(4,dtype=float),where=c.sum(1)!=0)
    return {'decisions':int(y.size),'correct':int((p==y).sum()),'accuracy':float((p==y).mean()),
            'worlds':len(y),'whole_correct':int((p==y).all(1).sum()),'macro_recall':float(recall.mean()),
            'false_complete':int(((p==1)&(y!=1)).sum()),'class_counts':c.sum(1).tolist(),
            'confusion':c.tolist(),'recall':recall.tolist()}
