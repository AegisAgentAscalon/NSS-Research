"""Offline supervised preparation only. This module is not imported by evaluator."""
import argparse,hashlib,time,json
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from . import ROOT
from . import repair
from nbr006 import common as c, data

def training_batch(rng,b=96):
    book=np.zeros((b,17,17),np.float32)
    book[:,:16,:16]=data.normalize(rng.normal(size=(b,16,16))).astype(np.float32)
    book[:,16,-1]=1
    idx=rng.integers(0,17,size=(b,1));target=book[np.arange(b)[:,None],idx]
    levels=np.array([0.,.02,.05,.10,.20],np.float32)
    sigma=rng.choice(levels,size=(b,1,1))
    noises=rng.normal(size=(3,b,1,17)).astype(np.float32)*sigma
    x=target+noises[0]
    erased=rng.random(b)<.05
    x[erased]=0;target[erased]=book[erased,16,None,:];idx[erased]=16
    return (torch.from_numpy(a) for a in (book,x,target,idx,noises))
def train(kind,seed,steps,out):
    c.setup(seed);rng=np.random.default_rng(seed+7000000)
    model=repair.make(kind);init=c.weights_hash(model)
    opt=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=0)
    history=[];fingerprints=[];t=time.perf_counter()
    for step in range(steps):
        book,x,target,idx,noise=training_batch(rng)
        if step in (0,steps//2,steps-1):
            fingerprints.append(hashlib.sha256(b''.join(a.numpy().tobytes() for a in (book,x,target,idx,noise))).hexdigest())
        h=x;loss=0
        for j in range(3):
            if j:h=h+noise[j]
            if kind=='learned_dictionary':
                logits=model.logits(h,book);loss=loss+F.cross_entropy(logits.reshape(-1,17),idx.reshape(-1))
            pred=model(h,book)
            loss=loss+8*F.mse_loss(pred,target)
            h=pred
        # Direct clean consistency protects preserved valid codes and UNKNOWN.
        loss=loss+8*F.mse_loss(model(target,book),target)
        opt.zero_grad(set_to_none=True);loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        opt.step()
        if step%300==0 or step==steps-1:
            entry={'step':step+1,'loss':float(loss.detach())};history.append(entry);print(kind,seed,entry,flush=True)
    seconds=time.perf_counter()-t
    path=Path(out)/f'{kind}_{seed}.safetensors'
    if path.exists():raise FileExistsError(path)
    c.save_model(path,model)
    info={'kind':kind,'seed':seed,'steps':steps,'batch_size':96,'sequence_presentations':steps*96,'noisy_updates_per_sequence':3,'clean_consistency_updates':1,'parameters':sum(p.numel() for p in model.parameters()),'seconds':seconds,'initial_hash':init,'final_hash':c.weights_hash(model),'checkpoint_sha256':c.sha(path),'history':history,'batch_fingerprints':fingerprints,'environment':c.env()}
    c.dump(path.with_suffix('.json'),info)
    return info
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['learned_dictionary','intrinsic_mlp'],required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--steps',type=int,default=1800);p.add_argument('--out',default=str(ROOT/'checkpoints'));a=p.parse_args();train(a.kind,a.seed,a.steps,a.out)
