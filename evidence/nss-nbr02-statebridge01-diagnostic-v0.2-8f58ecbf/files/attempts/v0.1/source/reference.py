"""Independent NumPy GRU, derivatives and Boolean task oracle. No producer imports."""
from __future__ import annotations
import numpy as np
KEYS=['cell.weight_ih','cell.weight_hh','cell.bias_ih','cell.bias_hh','head.weight','head.bias']
SHAPES=[(192,16),(192,64),(192,),(192,),(9,64),(9,)]
def from_flat(v):
    w={};j=0
    for k,s in zip(KEYS,SHAPES):n=int(np.prod(s));w[k]=np.asarray(v[j:j+n],np.float64).reshape(s);j+=n
    assert j==len(v)==16329
    return w

def sigmoid(x):return 1/(1+np.exp(-x))
def softmax(x):
    y=np.exp(x-np.max(x,axis=-1,keepdims=True));return y/y.sum(axis=-1,keepdims=True)

def oracle(events):
    events=np.asarray(events);events=events[None] if events.ndim==1 else events
    h=[[False]*4 for _ in range(len(events))];bits=[];nxt=[]
    for t in range(events.shape[1]):
        for row,code in zip(h,events[:,t]):
            k=int(code)
            if 0<=k<4:row[k]=True
            elif 4<=k<8:row[k-4]=False
            elif k==8:row[:]=[False]*4
            elif k!=255:raise ValueError('Illegal task-A input')
        bits.append([r.copy() for r in h]);nxt.append([next((k for k,x in enumerate(r) if not x),4) for r in h])
    return np.transpose(np.array(bits,np.float64),(1,0,2)),np.array(nxt,np.int64).T

def forward(w,events,h=None):
    events=np.asarray(events);events=events[None] if events.ndim==1 else events
    h=np.zeros((len(events),64),np.float64) if h is None else np.asarray(h,np.float64).copy()
    W,U,bi,bh,V,a=[np.asarray(w[k],np.float64) for k in KEYS];hs=[];outs=[];cache=[]
    for codes in events.T:
        active=codes!=255;x=np.zeros((len(events),16));x[np.arange(len(events))[active],codes[active].astype(int)]=1
        gi=x@W.T+bi;gh=h@U.T+bh
        r=sigmoid(gi[:,:64]+gh[:,:64]);z=sigmoid(gi[:,64:128]+gh[:,64:128]);n=np.tanh(gi[:,128:]+r*gh[:,128:])
        cand=(1-z)*n+z*h
        cache.append((x,h.copy(),r,z,n,gh[:,128:].copy(),active))
        h=np.where(active[:,None],cand,h);hs.append(h.copy());outs.append(h@V.T+a)
    return np.stack(hs,axis=1),np.stack(outs,axis=1),cache

def grad_one(w,events,kind,targets=None):
    hs,lo,cache=forward(w,events);b,t,_=lo.shape;dlo=np.zeros_like(lo)
    if kind=='A':
        truth,nxt=oracle(events);p=sigmoid(lo[:,:,:4]);dlo[:,:,:4]=(p-truth)/(b*t*4)
        ce=softmax(lo[:,:,4:]);ce[np.arange(b)[:,None],np.arange(t),nxt]-=1;dlo[:,:,4:]=ce/(b*t)
        loss=np.mean(np.logaddexp(0,lo[:,:,:4])-truth*lo[:,:,:4])
        zz=lo[:,:,4:];mx=zz.max(-1);logz=mx+np.log(np.exp(zz-mx[:,:,None]).sum(-1))
        loss+=np.mean(logz-np.take_along_axis(zz,nxt[:,:,None],-1)[:,:,0])
    elif kind=='B':
        y=np.asarray(targets,np.float64);z=lo[:,-1,0];dlo[:,-1,0]=(sigmoid(z)-y)/b
        loss=np.mean(np.logaddexp(0,z)-y*z)
    else:raise ValueError(kind)
    g={k:np.zeros(s,np.float64) for k,s in zip(KEYS,SHAPES)}
    V=np.asarray(w['head.weight'],np.float64);U=np.asarray(w['cell.weight_hh'],np.float64)
    g['head.weight']=np.einsum('bto,bth->oh',dlo,hs);g['head.bias']=dlo.sum((0,1));dh=np.zeros((b,64))
    for n in range(t-1,-1,-1):
        x,h,r,z,actn,ghn,active=cache[n]
        dh=dh+dlo[:,n]@V;d=dh*active[:,None]
        dan=d*(1-z)*(1-actn**2);daz=d*(h-actn)*z*(1-z);dar=dan*ghn*r*(1-r)
        di=np.concatenate([dar,daz,dan],axis=1);dg=np.concatenate([dar,daz,dan*r],axis=1)
        g['cell.weight_ih']+=di.T@x;g['cell.weight_hh']+=dg.T@h
        g['cell.bias_ih']+=di.sum(0);g['cell.bias_hh']+=dg.sum(0)
        dh=d*z+dg@U+dh*(~active)[:,None]
    return float(loss),np.concatenate([g[k].reshape(-1) for k in KEYS]),hs,lo

def gradient(w,record):
    val=0.;der=np.zeros(16329)
    if 'A_events' in record:
        l,g,_,_=grad_one(w,record['A_events'],'A');val+=l;der+=g
    l,g,_,_=grad_one(w,record['B_events'],'B',record['B_labels']);val+=l;der+=g
    return val,der
