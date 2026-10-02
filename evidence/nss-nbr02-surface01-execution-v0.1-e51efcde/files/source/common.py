"""SURFACE01 fixed implementation. Synthetic diagnostic, not a product model."""
from __future__ import annotations
import os
for _k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k] = '1'
import copy, hashlib, json, platform, resource, sys, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as TF

torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True)
torch.backends.mkldnn.enabled = False
ROOT = Path(__file__).resolve().parents[1]
FAMILIES = ['mixed','idempotent','revision','reset']
SEEDS = [4101,4102,4103,4104]
STAGES = [0,1,2,4,8,16,32,64]
PARENT_STAGES = [0,250,500,1000,1500,2000]
CAP_RSS = 2*1024**3
CAP_BYTES = 512*1024**2
ATOL, RTOL = 2e-6, 2e-5
EYE = torch.eye(26, dtype=torch.float32)
COUNTERS = {'optimizer_applications':0,'backward_calls':0,'canonical_state_rows':0,'reference_state_rows':0}

def js(x):
    if isinstance(x, Path): return str(x)
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, np.generic): return x.item()
    if isinstance(x, torch.Tensor): return x.detach().cpu().tolist()
    raise TypeError(type(x).__name__)

def write_json(path, x):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(x, indent=2, default=js, allow_nan=False)+'\n')
    temp.replace(path)

def append_json(path,x):
    with Path(path).open('a') as f: f.write(json.dumps(x,default=js,allow_nan=False)+'\n')

def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha_arr(a):
    a=np.ascontiguousarray(a)
    return hashlib.sha256(str(a.dtype).encode()+str(a.shape).encode()+a.tobytes()).hexdigest()
def hash_sd(sd):
    h=hashlib.sha256()
    for k,v in sorted(sd.items()):
        h.update(k.encode()); h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()
def utc():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024

def assert_ok(ok,code,detail=''):
    if not bool(ok): raise RuntimeError(code+': '+str(detail))

def oracle(tokens):
    """Canonical labels: bitmask implementation, no neural predictions involved."""
    a=np.asarray(tokens); out=np.empty(a.shape,dtype=np.uint8); masks=np.empty_like(out)
    flat=a.reshape(-1,a.shape[-1]); oo=out.reshape(flat.shape); mm=masks.reshape(flat.shape)
    for b,row in enumerate(flat):
        m=0
        for t,e in enumerate(row):
            e=int(e)
            if e<8: m |= 1<<e
            elif e<16: m &= ~(1<<(e-8))
            elif e==16: m=0
            elif e!=17: raise ValueError('Not an A token')
            oo[b,t]=next((i for i in range(8) if not m & (1<<i)),8)
            mm[b,t]=m
    return out,masks

def independent_oracle(tokens):
    """Independent label implementation: Python set of completed identifiers."""
    result=[]
    for row in np.asarray(tokens):
        done=set(); labels=[]
        for token in row:
            n=int(token)
            if 0<=n<=7: done.add(n)
            elif 8<=n<=15: done.discard(n-8)
            elif n==16: done.clear()
            elif n!=17: raise ValueError(n)
            labels.append(min(set(range(8))-done) if len(done)<8 else 8)
        result.append(labels)
    return np.asarray(result,dtype=np.uint8)

def stream(rng, length, family):
    """TARGET_MASK_ROUNDS_V1. Target masks guide data generation only.
    All intermediate events are exposed; target masks/labels never enter inputs.
    """
    events=[]; mask=0; round_n=0
    def emit(e):
        nonlocal mask
        if len(events)>=length: return
        events.append(int(e))
        if e<8: mask |= 1<<e
        elif e<16: mask &= ~(1<<(e-8))
        elif e==16: mask=0
    while len(events)<length:
        if family==3 and round_n%3==0: emit(16)
        # Ordinary and repeat families sample all next-action labels uniformly.
        # Revision family alternates complete and partially reopened targets.
        k=8 if family==2 and round_n%2==0 else int(rng.integers(0,8 if family==2 else 9))
        target=(1<<k)-1
        for j in range(k+1,8):
            if rng.random()<0.5: target |= 1<<j
        edits=[j if target & (1<<j) else j+8 for j in range(8) if bool(mask&(1<<j))!=bool(target&(1<<j))]
        rng.shuffle(edits)
        for e in edits: emit(e)
        # Holds mix actual NOOP and genuinely idempotent SET/CLEAR commands.
        dwell=int(rng.integers(5,10) if family==1 else rng.integers(1,5))
        for _ in range(dwell):
            if rng.random()<0.5: emit(17)
            else:
                j=int(rng.integers(0,8)); emit(j if mask & (1<<j) else j+8)
        round_n+=1
    return np.asarray(events,dtype=np.uint8)

def training_data(seed, nupdates=2000):
    rng=np.random.default_rng(100000+seed)
    tokens=np.empty((nupdates,32,32),dtype=np.uint8)
    fam=np.empty((nupdates,32),dtype=np.uint8)
    initial=copy.deepcopy(rng.bit_generator.state)
    for s in range(nupdates):
        families=rng.permutation(np.repeat(np.arange(4),8))
        fam[s]=families
        for b,f in enumerate(families): tokens[s,b]=stream(rng,32,int(f))
    labels,masks=oracle(tokens)
    return tokens,labels,masks,fam,{'seed':100000+seed,'initial':initial,'final':rng.bit_generator.state}

def make_panel(seed, partition, training_tokens):
    """Admission: 64 per family. Confirmation: 8 per family, only after A0."""
    assert partition in ('admission','confirmation')
    nper=64 if partition=='admission' else 8
    suffix=32 if partition=='admission' else 128
    salt=200000 if partition=='admission' else 300000
    rng=np.random.default_rng(salt+seed)
    trainrows={row.tobytes() for row in training_tokens.reshape(-1,32)}
    tokens=[]; prefixes=[]; families=[]; seen=set(); rejects=0
    for f in range(4):
        for i in range(nper):
            p=8 if i%2==0 else 24
            while True:
                row=stream(rng,p+suffix,f)
                # Reject exact history reuse; also reject any full training-length window.
                key=row.tobytes()
                overlap=any(row[j:j+32].tobytes() in trainrows for j in range(len(row)-31))
                if key not in seen and not overlap: break
                rejects+=1
                if rejects>10000: raise RuntimeError('FIXTURE_DEDUP_EXHAUSTED')
            seen.add(key); tokens.append(row); prefixes.append(p); families.append(f)
    arr=np.full((len(tokens),24+suffix),255,dtype=np.uint8)
    lab=np.full_like(arr,255); masks=np.full_like(arr,0)
    for i,row in enumerate(tokens):
        yy,mm=oracle(row[None,:]); arr[i,:len(row)]=row; lab[i,:len(row)]=yy[0]; masks[i,:len(row)]=mm[0]
    return {'tokens':arr,'labels':lab,'masks':masks,'prefixes':np.array(prefixes), 'families':np.array(families),
            'suffix':np.array(suffix),'seed':np.array(salt+seed),'rejects':np.array(rejects)}

class Learner(nn.Module):
    def __init__(self, seed):
        super().__init__(); torch.manual_seed(seed)
        self.cell=nn.GRUCell(26,64); self.head=nn.Linear(64,9)
    def rollout(self,tokens,h=None):
        if not isinstance(tokens,torch.Tensor): tokens=torch.tensor(tokens,dtype=torch.long)
        else: tokens=tokens.long()
        if h is None: h=torch.zeros(tokens.shape[0],64)
        xx=EYE[tokens]; hs=[]; logits=[]
        for t in range(tokens.shape[1]):
            h=self.cell(xx[:,t],h); hs.append(h); logits.append(self.head(h))
        COUNTERS['canonical_state_rows']+=int(tokens.numel())
        return torch.stack(hs,1),torch.stack(logits,1)
    def b_logits(self):
        h=self.cell(EYE[18:26],torch.zeros(8,64)); COUNTERS['canonical_state_rows']+=8
        return self.head(h)

def opt_for(model,frozen=False):
    for p in model.cell.parameters(): p.requires_grad_(not frozen)
    return torch.optim.Adam([p for p in model.parameters() if p.requires_grad],lr=.003,betas=(.9,.999),eps=1e-8,weight_decay=0,foreach=False,fused=False)

def update(model,opt, tokens=None,labels=None,correction=None):
    old={k:p.detach().clone() for k,p in model.named_parameters()}
    opt.zero_grad(set_to_none=True)
    btargets=torch.arange(8)%2
    if correction is not None: btargets[correction]=1-btargets[correction]
    bl=model.b_logits(); lb=TF.cross_entropy(bl,btargets)
    if tokens is not None:
        _,logits=model.rollout(tokens)
        la=TF.cross_entropy(logits.reshape(-1,9),torch.as_tensor(labels,dtype=torch.long).reshape(-1))
        loss=.5*la+.5*lb
    else: la=torch.tensor(0.); loss=lb
    loss.backward(); COUNTERS['backward_calls']+=1
    active=[p for p in model.parameters() if p.requires_grad]
    grad=torch.nn.utils.clip_grad_norm_(active,1.0,error_if_nonfinite=True)
    opt.step(); COUNTERS['optimizer_applications']+=1
    deltas={k:float(torch.linalg.vector_norm(p.detach()-old[k])) for k,p in model.named_parameters()}
    assert_ok(all(torch.isfinite(p).all() for p in model.parameters()),'NONFINITE_PARAMETER')
    assert_ok(rss()<CAP_RSS,'RSS_LIMIT',rss())
    return {'loss':float(loss.detach()),'A_loss':float(la.detach()),'B_loss':float(lb.detach()),
            'grad_norm':float(grad),'clip_scale':min(1.,1./(float(grad)+1e-6)),'delta_by_tensor':deltas}

def save_checkpoint(path,model,opt,cursor,extra=None):
    payload={'model':model.state_dict(),'optimizer':opt.state_dict() if opt else None,'torch_rng':torch.get_rng_state(),
             'cursor':cursor,'extra':extra or {},'model_hash':hash_sd(model.state_dict())}
    torch.save(payload,path)
    return sha_file(path)

def load_checkpoint(path):
    p=torch.load(path,map_location='cpu',weights_only=True)
    m=Learner(0); m.load_state_dict(p['model'])
    assert_ok(hash_sd(m.state_dict())==p['model_hash'],'CHECKPOINT_TENSOR_HASH')
    return m,p

def reference_rollout(model,tokens,h0=None,head=None,dtype=np.float32):
    """Independent NumPy GRU equations; free-running full trajectory, not reseeded each step."""
    w={k:v.detach().numpy().astype(dtype) for k,v in model.cell.state_dict().items()}
    hd=model.head if head is None else head
    hw=hd.weight.detach().numpy().astype(dtype); hb=hd.bias.detach().numpy().astype(dtype)
    tok=np.asarray(tokens); x=np.eye(26,dtype=dtype)[tok]
    h=np.zeros((len(tok),64),dtype=dtype) if h0 is None else np.asarray(h0,dtype=dtype).copy()
    hs=[]; ls=[]
    for t in range(tok.shape[1]):
        xi=x[:,t]@w['weight_ih'].T+w['bias_ih']
        hh=h@w['weight_hh'].T+w['bias_hh']
        ir,iz,inn=np.split(xi,3,axis=-1); hr,hz,hn=np.split(hh,3,axis=-1)
        r=1/(1+np.exp(-(ir+hr))); z=1/(1+np.exp(-(iz+hz)))
        n=np.tanh(inn+r*hn)
        h=(1-z)*n+z*h
        hs.append(h.copy()); ls.append(h@hw.T+hb)
    COUNTERS['reference_state_rows']+=int(tok.size)
    return np.stack(hs,1),np.stack(ls,1)

def compare_arrays(actual,ref,name):
    a=np.asarray(actual); r=np.asarray(ref)
    assert_ok(a.shape==r.shape,'SHAPE_MISMATCH',(a.shape,r.shape))
    assert_ok(np.isfinite(a).all() and np.isfinite(r).all(),'NONFINITE_CHECKER')
    diff=np.abs(a-r); ratio=diff/(ATOL+RTOL*np.abs(r))
    idx=np.unravel_index(int(np.argmax(ratio)),ratio.shape)
    return {'name':name,'pass':bool(np.all(ratio<=1)),'max_abs':float(diff.max()),'max_scaled':float(ratio.max()),
            'argmax_scaled':list(idx),'actual_at_max':float(a[idx]),'reference_at_max':float(r[idx]),
            'bad_coordinates':int((ratio>1).sum()),'coordinates':int(a.size)}

def check_trajectory(model,tokens,hs,logits,h0=None,tag='trajectory',head=None):
    rh,rl=reference_rollout(model,tokens,h0,head=head)
    checks=[compare_arrays(hs,rh,tag+'/hidden'),compare_arrays(logits,rl,tag+'/logits')]
    agree=bool(np.array_equal(np.argmax(logits,-1),np.argmax(rl,-1)))
    return {'pass':all(c['pass'] for c in checks) and agree,'checks':checks,'class_agreement':agree}

@torch.no_grad()
def score_panel(model,panel,tag, save=True):
    """Parent full-history scoring, with canonical batching grouped by interruption length."""
    N=len(panel['prefixes']); suffix=int(panel['suffix'])
    out=np.empty((N,suffix+1,9),np.float32); hidden=np.empty((N,suffix+1,64),np.float32)
    targets=np.empty((N,suffix+1),np.uint8); checks=[]; prefixes_h=np.zeros((N,24,64),np.float32)
    full_logits=np.zeros((N,24+suffix,9),np.float32)
    full_hidden=np.zeros((N,24+suffix,64),np.float32)
    for p in (8,24):
        rows=np.where(panel['prefixes']==p)[0]; toks=panel['tokens'][rows,:p+suffix]
        hs,ll=model.rollout(toks); hh=hs.numpy(); logits=ll.numpy()
        ck=check_trajectory(model,toks,hh,logits,tag=f'{tag}/prefix{p}'); checks.append(ck)
        out[rows]=logits[:,p-1:]; hidden[rows]=hh[:,p-1:]; targets[rows]=panel['labels'][rows,p-1:p+suffix]
        prefixes_h[rows,:p]=hh[:,:p]; full_logits[rows,:p+suffix]=logits; full_hidden[rows,:p+suffix]=hh
    if save:
        np.savez_compressed(ROOT/'evidence'/f'{tag}.npz',logits=out,targets=targets,full_hidden=full_hidden)
        write_json(ROOT/'evidence'/f'{tag}_numerical.json',checks)
    metrics=metrics_by_family(out,targets,panel['families'],horizons=[8,32] if suffix==32 else [8,32,128])
    return {'logits':out,'hidden':hidden,'targets':targets,'checks':checks,'metrics':metrics,
            'full_logits':full_logits,'full_hidden':full_hidden}

def metrics_by_family(logits,targets,families,horizons=(8,32,128),reference=None):
    pred=logits.argmax(-1); result={}
    for h in horizons:
        blocks={}
        for f,name in enumerate(FAMILIES):
            idx=np.where(families==f)[0]; pp=pred[idx,1:h+1]; yy=targets[idx,1:h+1]
            correct=pp==yy; false_done=(pp==8)&(yy!=8)
            z=logits[idx,1:h+1].astype(np.float64); maximum=z.max(-1,keepdims=True)
            ce=np.log(np.exp(z-maximum).sum(-1))+maximum[...,0]-np.take_along_axis(z,yy[...,None],-1)[...,0]
            true=np.take_along_axis(z,yy[...,None],-1)[...,0]; z[np.arange(len(idx))[:,None],np.arange(h),yy]=-np.inf
            margins=true-z.max(-1)
            first=np.where(correct.all(1),0,np.argmax(~correct,axis=1)+1)
            d={'events_correct':int(correct.sum()),'events_total':int(correct.size),'event_accuracy':float(correct.mean()),
               'whole_correct':int(correct.all(1).sum()),'histories':int(len(idx)),'whole_rate':float(correct.all(1).mean()),
               'false_done':int(false_done.sum()),'boundary_correct':int((pred[idx,0]==targets[idx,0]).sum()),
               'mean_loss':float(ce.mean()),'max_loss':float(ce.max()),'mean_margin':float(margins.mean()),'min_margin':float(margins.min()),'first_error_positions':first.tolist()}
            if reference is not None:
                rp=reference[idx,1:h+1].argmax(-1)
                d['new_errors']=int((~correct & (rp==yy)).sum())
                d['new_false_done']=int((false_done & ~((rp==8)&(yy!=8))).sum())
                d['accuracy_drop_pp']=float(((rp==yy).mean()-correct.mean())*100)
            blocks[name]=d
        result[str(h)]=blocks
    return result

@torch.no_grad()
def b_score(model,correction=None):
    logits=model.b_logits().numpy(); targets=np.arange(8)%2
    if correction is not None: targets[correction]=1-targets[correction]
    zz=logits.astype(np.float64); zz-=zz.max(-1,keepdims=True); p=np.exp(zz); p/=p.sum(-1,keepdims=True)
    prob=p[np.arange(8),targets]; pred=logits.argmax(-1)
    # Independently check a one-event zero-state history for every cue.
    hs,ll=model.rollout(np.arange(18,26)[:,None]); ck=check_trajectory(model,np.arange(18,26)[:,None],hs.numpy(),ll.numpy(),tag='B')
    return {'logits':logits.tolist(),'targets':targets.tolist(),'predictions':pred.tolist(),'true_probabilities':prob.tolist(),
            'min_true_probability':float(prob.min()),'all_correct':bool((pred==targets).all()),
            'pass':bool((pred==targets).all() and (prob>=.8).all()),'numerical':ck}

def competence(metrics,b):
    rows=metrics['32']
    return bool(b['pass'] and all(r['event_accuracy']>=.99 and r['whole_rate']>=.95 and r['false_done']==0 for r in rows.values()))
