"""Matched continued preparation of ONLY inherited binder parameters.

Ordinary and near-negative arms use paired RNG draws/batch masks/steps. Half of
hard-arm examples replace a generic nearest neighbor with a close but distinct
identity. Both existing-vs-NEW and competing existing-record cases are included.
No online optimizer runs during evaluation.
"""
from .common import *
from torch.nn import functional as F
import argparse

def batch(rng,b=128,hard=False):
    # Generate all draws in both arms; only candidate representations differ.
    keys=np.zeros((b,16,17),np.float32);keys[:,:,:16]=data.normalize(rng.normal(size=(b,16,16))).astype(np.float32)
    present=rng.random((b,16))>.25;anchor=rng.integers(0,16,b);r=np.arange(b)
    present[r,anchor]=True
    target=anchor.copy();q=keys[r,anchor].copy()
    new=rng.random(b)<.40;close=rng.random(b)<.65
    random_new=np.zeros((b,17),np.float32);random_new[:,:16]=data.normalize(rng.normal(size=(b,16))).astype(np.float32)
    delta=np.zeros((b,17),np.float32);delta[:,:16]=rng.normal(size=(b,16)).astype(np.float32)
    sigma=rng.choice(np.array([.01,.03,.10],np.float32),size=b)
    near=data.normalize(q+sigma[:,None]*delta).astype(np.float32)
    competitor=(anchor+1+rng.integers(0,15,b))%16
    competitor_code=np.zeros((b,17),np.float32);competitor_code[:,:16]=data.normalize(rng.normal(size=(b,16))).astype(np.float32)
    q[new]=random_new[new];target[new]=16
    chosen=close&~new
    keys[r[chosen],competitor[chosen]]=near[chosen] if hard else competitor_code[chosen]
    present[r[chosen],competitor[chosen]]=True
    if hard:q[new&close]=near[new&close]
    # Training is on resolved canonical numeric observations in the main arms.
    keys*=present[...,None]
    return torch.from_numpy(q),torch.from_numpy(keys),torch.from_numpy(present),torch.from_numpy(target)

def fit(pair,kind,seed,steps,path,development=False):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    setup(seed);m=load_binder(pair,'parent')
    for p in m.parameters():p.requires_grad_(True)
    m.train();initial=weights_hash(m);rng=np.random.default_rng(seed+910000)
    opt=torch.optim.AdamW(m.parameters(),lr=.002,weight_decay=1e-4)
    t=time.perf_counter();started=utc();history=[];checks={}
    for step in range(steps):
        q,k,p,y=batch(rng,128,kind=='near');opt.zero_grad(set_to_none=True)
        out=m(q,k,p);loss=F.cross_entropy(out,y)
        if not torch.isfinite(loss):raise RuntimeError('Nonfinite loss')
        loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),1.);opt.step()
        if step in (0,steps//2,steps-1):checks[str(step+1)]=array_digest({'q':q.numpy(),'keys':k.numpy(),'present':p.numpy(),'target':y.numpy()})
        if step==0 or (step+1)%200==0:
            rec={'step':step+1,'loss':float(loss.detach()),'accuracy':float((out.argmax(-1)==y).float().mean()),'seconds':time.perf_counter()-t};history.append(rec);print(pair,kind,seed,rec,flush=True)
    save_model(path,m)
    info={'pair':pair,'kind':kind,'seed':seed,'steps':steps,'batch':128,'examples':steps*128,'development':development,'optimizer':'AdamW','lr':.002,'weight_decay':1e-4,'initial_weight_hash':initial,'final_weight_hash':weights_hash(m),'checkpoint_sha256':sha(path),'data_checks':checks,'history':history,'start_utc':started,'end_utc':utc(),'fit_seconds':time.perf_counter()-t,'parameters':sum(p.numel() for p in m.parameters()),'threshold':float(m.threshold.detach()),'scale':float(m.log_scale.exp().clamp(max=80).detach()),'env':env()}
    dump(path.with_suffix('.json'),info);return info

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pair',type=int,required=True);ap.add_argument('--kind',choices=['ordinary','near'],required=True);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--steps',type=int,default=1200);ap.add_argument('--out',required=True);ap.add_argument('--development',action='store_true');a=ap.parse_args();fit(a.pair,a.kind,a.seed,a.steps,a.out,a.development)
