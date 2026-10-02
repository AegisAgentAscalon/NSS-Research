"""Public event generation; targets are supplied only to supervised losses/scoring."""
from __future__ import annotations
import numpy as np
from common import CFG,seed
NOP=255

def rng(name):return np.random.Generator(np.random.PCG64(seed(name)))
def training(fit,steps=None,batch=None):
    steps=CFG['initial_updates'] if steps is None else steps
    batch=CFG['initial_batch'] if batch is None else batch
    g=rng(f'train/{fit}')
    ev=g.integers(0,10,(steps,batch,33),dtype=np.uint8);ev[ev==9]=NOP
    lengths=np.where(np.arange(steps)%2==0,17,33).astype(np.uint8)
    for u,n in enumerate(lengths):ev[u,:,int(n):]=NOP
    return ev,lengths,g.bit_generator.state

def a_truth(events):
    """Producer bit-mask implementation, independent scorer uses four Boolean lists."""
    e=np.asarray(events);e=e[None,:] if e.ndim==1 else e
    v=np.zeros(e.shape[0],np.uint8);out=[]
    for col in e.T:
        for b,c in enumerate(col):
            c=int(c)
            if c<4:v[b]|=1<<c
            elif c<8:v[b]&=255^(1<<(c-4))
            elif c==8:v[b]=0
            elif c!=NOP:raise ValueError('Not task A')
        out.append(v.copy())
    packed=np.stack(out,axis=1)
    bits=((packed[...,None]>>np.arange(4))&1).astype(np.float32)
    nxt=np.where(bits==0,np.arange(4),4).min(-1).astype(np.int64)
    return bits,nxt,packed

def labels():
    v=np.array([0,0,1,1],np.int64);rng('initial/B_labels').shuffle(v);return v

def b_prefix(cues):
    return np.array([[9,10+int(c)//2,12+int(c)] for c in cues],np.uint8)

def evaluation(split):
    lengths=CFG['dev_lengths'] if split=='dev' else CFG['test_lengths']
    g=rng(f'eval/{split}');events=np.full((32,max(lengths)),NOP,np.uint8);ls=[];masks=[]
    for i,(n,m) in enumerate((n,m) for n in lengths for m in range(16)):
        e=g.integers(0,10,n,dtype=np.uint8);e[e==9]=NOP
        # Balanced public SET/CLEAR histories; no answer vector enters the model.
        e[-4:]=np.array([j if (m>>j)&1 else j+4 for j in range(4)],np.uint8)
        events[i,:n]=e;ls.append(n);masks.append(m)
    return {'events':events,'lengths':np.array(ls,np.int16),'mask_ids':np.array(masks,np.uint8)},g.bit_generator.state

def suffix(rotation):
    m=rotation%4
    return np.array([m,4+(m+1)%4,NOP,(m+2)%4,4+m,NOP,4+(m+2)%4,m],np.uint8)

def cue_order(focal,order):
    others=[c for c in range(4) if c!=focal]
    if order==0:return np.array([focal,focal,others[0],focal,others[1],focal,others[2],focal],np.int8)
    return np.array([others[0],focal,others[1],focal,others[2],focal,focal,focal],np.int8)
