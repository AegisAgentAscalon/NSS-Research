"""Offline fitting and held-out calibration; never imported by scored evaluator."""
import argparse,hashlib,time,json
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from .common import *
from .resolver import MatchHead,features
from .samples import sample,training_batch


def fit(seed,steps,out):
    setup(seed);rng=np.random.default_rng(200000000+seed)
    model=MatchHead();init=weights_hash(model)
    opt=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=.0001)
    start=time.perf_counter();history=[];fp=[]
    for j in range(steps):
        a=training_batch(rng);book=torch.from_numpy(a['book']);x=torch.from_numpy(a['x']);act=torch.from_numpy(a['active'])
        with torch.no_grad():f,idx=features(x,book,act)
        y=torch.from_numpy(a['known']) & (idx[:,0]==torch.from_numpy(a['target']))
        if j in (0,steps//2,steps-1):fp.append(hashlib.sha256(b''.join(a[k].tobytes() for k in sorted(a))).hexdigest())
        loss=F.binary_cross_entropy_with_logits(model(f)[:,0],y.float())
        opt.zero_grad(set_to_none=True);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step()
        if j%300==0 or j==steps-1:
            history.append({'step':j+1,'loss':float(loss.detach())});print('FIT',seed,history[-1],flush=True)
    path=Path(out)/f'match_head_{seed}.safetensors'
    if path.exists():raise FileExistsError(path)
    save_model(path,model)
    info={'seed':seed,'steps':steps,'batch_size':256,'presentations':steps*256,'parameters':sum(p.numel() for p in model.parameters()),'initial_hash':init,'final_hash':weights_hash(model),'checkpoint_sha256':sha(path),'seconds':time.perf_counter()-start,'history':history,'batch_fingerprints':fp,'environment':env()}
    dump(path.with_suffix('.json'),info);return model,info

@torch.no_grad()
def calibrate(seed,model,out,n=4096):
    rng=np.random.default_rng(300000000+seed);fams=['known_exact','known_q05','known_q20','known_raw02','known_raw08','novel','novel_noisy20']
    fs={};target={};probs={};idxs={}
    for fam in fams:
        a=sample(rng,n,fam);f,idx=features(torch.from_numpy(a['x']),torch.from_numpy(a['book']),torch.from_numpy(a['active']))
        fs[fam]=f[:,0].numpy();idxs[fam]=idx[:,0].numpy();target[fam]=a['target'];probs[fam]=model(f)[:,0].sigmoid().numpy()
    # Predeclared family-balanced objective at <=0.5% calibration FPR in EACH
    # independent novel family. Same data for both candidates; stress not optimized.
    best=None;frontier=[]
    for distance in np.linspace(.02,1.8,180):
        for margin in np.linspace(0,.5,26):
            decisions={f:(v[:,0]<=distance)&(v[:,1]>=margin) for f,v in fs.items()}
            fpr=max(decisions[f].mean() for f in ('novel','novel_noisy20'))
            tpr=np.mean([((target[f]==idxs[f])&decisions[f]).mean() for f in fams[:5]])
            key=(tpr,-fpr,margin,-distance)
            if fpr<=.005 and (best is None or key>best[0]):best=(key,float(distance),float(margin))
        # Curve at best margin per distance is not used to select main data.
    if best is None:raise RuntimeError('No geometric threshold')
    A={'distance':best[1],'margin':best[2]}
    neg=np.concatenate([probs[f] for f in ('novel','novel_noisy20')]);grid=np.unique(np.r_[0,1,neg])
    # Lowest threshold obeying <=0.5% per negative family maximizes acceptance.
    threshold=1.
    for t in grid:
        if all((probs[f]>=t).mean()<=.005 for f in ('novel','novel_noisy20')):
            threshold=float(t);break
    B={'threshold':threshold}
    metrics={}
    for fam in fams:
        f=fs[fam];ad=(f[:,0]<=A['distance'])&(f[:,1]>=A['margin']);bd=probs[fam]>=threshold
        metrics[fam]={'n':n,'A_accept':float(ad.mean()),'B_accept':float(bd.mean()),'A_correct':float(((idxs[fam]==target[fam])&ad).mean()) if fam.startswith('known') else None,'B_correct':float(((idxs[fam]==target[fam])&bd).mean()) if fam.startswith('known') else None}
    path=Path(out)/f'calibration_{seed}.json'
    info={'seed':seed,'n_per_family':n,'families':fams,'labelled_examples':n*len(fams),'A':A,'B':B,'selection':'maximize mean five-family correct acceptance subject to <=0.005 each independent-negative family; B lowest admissible probability threshold','metrics':metrics}
    dump(path,info)
    arrays={}
    for fam in fams:arrays[fam+'_features']=fs[fam];arrays[fam+'_target']=target[fam];arrays[fam+'_closest']=idxs[fam];arrays[fam+'_prob']=probs[fam]
    np.savez_compressed(path.with_suffix('.npz'),**arrays)
    print('CALIBRATED',seed,A,B,metrics,flush=True);return info

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True);p.add_argument('--steps',type=int,default=1200);p.add_argument('--out',required=True);p.add_argument('--cal-n',type=int,default=4096);a=p.parse_args()
    model,_=fit(a.seed,a.steps,a.out);calibrate(a.seed,model,a.out,a.cal_n)
