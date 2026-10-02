"""CYCLE01-A: fixed-weight serving plus separate float64 maintenance candidates."""
from __future__ import annotations
import os
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[k]='1'
import copy, hashlib, json, platform, resource, sys, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from task import oracle, independent_oracle, stream
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'protocol/CONFIG.json').read_text())
torch.set_num_threads(1);torch.set_num_interop_threads(1)
torch.use_deterministic_algorithms(True);torch.backends.mkldnn.enabled=False
DTYPE=torch.float64
COUNTS={'updates':0,'backward':0,'forward_state_rows':0,'numpy_state_rows':0,'numerical_scalars':0,'numerical_violations':0,'argmax_disagreements':0}

def native(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,torch.Tensor):return x.detach().cpu().tolist()
    if isinstance(x,Path):return str(x)
    raise TypeError(type(x))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False,default=native).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def write_json(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_bytes(canonical(x)+b'\n');tmp.replace(p)
def append(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('ab') as f:f.write(canonical(x)+b'\n');f.flush()
def utc():
    from datetime import datetime,timezone
    return datetime.now(timezone.utc).isoformat()
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024

def state_hash(sd):
    h=hashlib.sha256()
    for k,v in sorted(sd.items()):
        a=v.detach().cpu().contiguous().numpy();h.update(k.encode());h.update(str(a.dtype).encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()
def legacy_hash(sd):
    h=hashlib.sha256()
    for k,v in sorted(sd.items()):h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

class Learner(nn.Module):
    def __init__(self):
        super().__init__();self.cell=nn.GRUCell(26,64,dtype=DTYPE);self.head=nn.Linear(64,9,dtype=DTYPE)
    def rollout(self,tokens,h=None):
        t=torch.as_tensor(tokens,dtype=torch.long);x=F.one_hot(t,26).to(DTYPE)
        h=torch.zeros(t.shape[0],64,dtype=DTYPE) if h is None else torch.as_tensor(h,dtype=DTYPE).clone()
        hs=[];zs=[]
        for j in range(t.shape[1]):h=self.cell(x[:,j],h);hs.append(h);zs.append(self.head(h))
        COUNTS['forward_state_rows']+=int(t.numel())
        return torch.stack(hs,1),torch.stack(zs,1)
    def b_logits(self):return self.rollout(np.arange(18,26)[:,None])[1][:,0]

def load_parent(seed):
    p=ROOT/f'inputs/parents/parent_{seed}.pt';q=torch.load(p,map_location='cpu',weights_only=True)
    assert legacy_hash(q['model'])==q['model_hash'],'OLD_PARENT_HASH'
    m=Learner();m.load_state_dict(q['model'])
    assert sum(p.numel() for p in m.parameters())==18249
    for k,v in q['model'].items():assert torch.equal(v.double(),m.state_dict()[k]),'CAST_NOT_EXACT'
    return m,q['model_hash']
def clone(m):
    out=Learner();out.load_state_dict(copy.deepcopy(m.state_dict()));return out

def optim(m):return torch.optim.Adam(m.parameters(),lr=C['lr'],betas=(.9,.999),eps=1e-8,weight_decay=0,foreach=False,fused=False)

def loss_parts(m,targets,tokens=None,labels=None):
    lb=F.cross_entropy(m.b_logits(),torch.tensor(targets,dtype=torch.long))
    la=None
    if tokens is not None:
        _,z=m.rollout(tokens);la=F.cross_entropy(z.reshape(-1,9),torch.as_tensor(labels,dtype=torch.long).reshape(-1))
    return la,lb

def update(m,opt,phase,targets,tokens=None,labels=None):
    opt.zero_grad(set_to_none=True)
    if phase=='B':la=None;lb=F.cross_entropy(m.b_logits(),torch.tensor(targets,dtype=torch.long));loss=lb
    elif phase=='A':
        _,z=m.rollout(tokens);la=F.cross_entropy(z.reshape(-1,9),torch.as_tensor(labels,dtype=torch.long).reshape(-1));lb=None;loss=la
    elif phase=='AB':la,lb=loss_parts(m,targets,tokens,labels);loss=la+lb
    else:raise ValueError(phase)
    if not torch.isfinite(loss):raise RuntimeError('NONFINITE_LOSS')
    loss.backward();COUNTS['backward']+=1
    g=torch.nn.utils.clip_grad_norm_(m.parameters(),1.,error_if_nonfinite=True)
    opt.step();COUNTS['updates']+=1
    if not all(torch.isfinite(p).all() for p in m.parameters()):raise RuntimeError('NONFINITE_PARAMETER')
    if rss()>C['max_rss']:raise RuntimeError('RSS_CAP')
    return {'loss':float(loss.detach()),'A_loss':None if la is None else float(la.detach()),'B_loss':None if lb is None else float(lb.detach()),'gradient_norm':float(g),'model_hash':state_hash(m.state_dict())}

def cp(path,m,opt,cursor,extra=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    d={'model':copy.deepcopy(m.state_dict()),'optimizer':None if opt is None else copy.deepcopy(opt.state_dict()),'cursor':cursor,'model_hash':state_hash(m.state_dict()),'torch_rng':torch.get_rng_state(),'extra':extra or {}}
    tmp=path.with_suffix('.tmp');torch.save(d,tmp);tmp.replace(path);return {'path':str(path.relative_to(ROOT)),'file_sha256':file_sha(path),'model_hash':d['model_hash']}
def load_cp(path):
    d=torch.load(path,map_location='cpu',weights_only=True);assert state_hash(d['model'])==d['model_hash'],'CHECKPOINT_HASH'
    m=Learner();m.load_state_dict(d['model']);return m,d

def ref(m,tokens,h0=None):
    w={k:v.detach().numpy() for k,v in m.state_dict().items()};t=np.asarray(tokens);h=np.zeros((len(t),64),np.float64) if h0 is None else np.asarray(h0,np.float64).copy();hh=[];zz=[]
    eye=np.eye(26,dtype=np.float64)
    for j in range(t.shape[1]):
        a=eye[t[:,j]]@w['cell.weight_ih'].T+w['cell.bias_ih'];b=h@w['cell.weight_hh'].T+w['cell.bias_hh']
        ar,az,an=np.split(a,3,axis=-1);br,bz,bn=np.split(b,3,axis=-1)
        r=1/(1+np.exp(-(ar+br)));z=1/(1+np.exp(-(az+bz)));n=np.tanh(an+r*bn)
        h=(1-z)*n+z*h;hh.append(h.copy());zz.append(h@w['head.weight'].T+w['head.bias'])
    COUNTS['numpy_state_rows']+=int(t.size)
    return np.stack(hh,1),np.stack(zz,1)

def compare(a,b):
    a=np.asarray(a);b=np.asarray(b);err=np.abs(a-b);tol=C['atol']+C['rtol']*np.abs(b)
    out={'scalars':a.size,'outside':int((err>tol).sum()),'max_absolute':float(err.max(initial=0)),'max_envelope_fraction':float((err/tol).max(initial=0)),'finite':bool(np.isfinite(a).all() and np.isfinite(b).all())}
    COUNTS['numerical_scalars']+=a.size;COUNTS['numerical_violations']+=out['outside']
    return out

def verify(m,t,hs,z,h0=None):
    rh,rz=ref(m,t,h0);a=compare(hs,rh);b=compare(z,rz);d=int((np.asarray(z).argmax(-1)!=rz.argmax(-1)).sum());COUNTS['argmax_disagreements']+=d
    out={'hidden':a,'logits':b,'argmax_differences':d,'pass':a['outside']==b['outside']==d==0 and a['finite'] and b['finite']}
    return out

@torch.no_grad()
def prefix_state(m,panel,additional=0):
    h=np.zeros((len(panel['prefixes']),64),np.float64);checks=[]
    for p in sorted(set(map(int,panel['prefixes']))):
        ids=np.where(panel['prefixes']==p)[0];t=panel['tokens'][ids,:p+additional];hh,z=m.rollout(t)
        checks.append(verify(m,t,hh.numpy(),z.numpy()));h[ids]=hh[:,-1].numpy()
    if not all(c['pass'] for c in checks):raise RuntimeError('PREFIX_NUMERICAL')
    return h,checks

def suffix_tokens(panel,offset=0):return np.stack([panel['tokens'][i,int(p)+offset:int(p)+offset+32] for i,p in enumerate(panel['prefixes'])])
def suffix_labels(panel,offset=0):return np.stack([panel['labels'][i,int(p)+offset:int(p)+offset+32] for i,p in enumerate(panel['prefixes'])])

def metrics(z,y,families):
    p=z.argmax(-1);ok=p==y;fd=(p==8)&(y!=8)
    result={'correct':int(ok.sum()),'total':int(ok.size),'accuracy':float(ok.mean()),'whole_correct':int(ok.all(1).sum()),'histories':len(y),'whole_rate':float(ok.all(1).mean()),'false_done':int(fd.sum()),'families':{}}
    for f in range(4):
        ids=np.where(families==f)[0];c=ok[ids];d=fd[ids]
        result['families'][str(f)]={'correct':int(c.sum()),'total':int(c.size),'whole_correct':int(c.all(1).sum()),'histories':len(ids),'false_done':int(d.sum())}
    return result

@torch.no_grad()
def evaluate(m,panel,h0,offset=0):
    t=suffix_tokens(panel,offset);y=suffix_labels(panel,offset);hh,z=m.rollout(t,h0);hh=hh.numpy();z=z.numpy()
    numeric=verify(m,t,hh,z,h0)
    bound=m.head(torch.tensor(h0,dtype=DTYPE)).numpy();w=m.state_dict();bref=h0@w['head.weight'].numpy().T+w['head.bias'].numpy();bc=compare(bound,bref)
    numeric['boundary']=bc;numeric['pass'] &= bc['outside']==0 and bc['finite']
    # Boundary target follows the last already received event; no future label enters model inputs.
    by=np.array([panel['labels'][i,int(p)+offset-1] for i,p in enumerate(panel['prefixes'])])
    met=metrics(z,y,panel['families']);met['boundary_correct']=int((bound.argmax(-1)==by).sum())
    return {'logits':z,'targets':y,'h0':h0.copy(),'h_end':hh[:,-1].copy(),'boundary':bound,'boundary_targets':by,'tokens':t,'metrics':met,'numerical':numeric}

@torch.no_grad()
def b_score(m,targets):
    t=np.arange(18,26)[:,None];h,z=m.rollout(t);arr=z[:,0].numpy();shift=arr-arr.max(-1,keepdims=True);pr=np.exp(shift);pr/=pr.sum(-1,keepdims=True);pred=arr.argmax(-1);true=pr[np.arange(8),targets]
    return {'targets':list(map(int,targets)),'predictions':pred.tolist(),'logits':arr.tolist(),'true_probabilities':true.tolist(),'correct':int((pred==targets).sum()),'minimum_target_probability':float(true.min()),'acquired':bool((pred==targets).all() and (true>=.8).all()),'numerical':verify(m,t,h.numpy(),z.numpy())}

def adoption(candidate,original,prior,b):
    cm=candidate['metrics'];om=original['metrics'];pm=prior['metrics'];reasons=[]
    if not b['acquired']:reasons.append('CURRENT_CUE_ACQUISITION')
    if cm['accuracy']<.98-1e-12:reasons.append('OLD_EVENT_FLOOR')
    if cm['whole_rate']<.90-1e-12:reasons.append('OLD_WHOLE_FLOOR')
    for name,m in [('ORIGINAL',om),('PRIOR',pm)]:
        if cm['accuracy']<m['accuracy']-.01-1e-12:reasons.append(name+'_EVENT_LOSS')
        if cm['whole_rate']<m['whole_rate']-.0625-1e-12:reasons.append(name+'_WHOLE_LOSS')
    y=candidate['targets'];fd=(candidate['logits'].argmax(-1)==8)&(y!=8)
    for name,e in [('ORIGINAL',original),('PRIOR',prior)]:
        old=(e['logits'].argmax(-1)==8)&(y!=8)
        if (fd&~old).any() or fd.sum()>old.sum():reasons.append(name+'_FALSE_DONE')
    if not candidate['numerical']['pass'] or not b['numerical']['pass']:reasons.append('NUMERICAL')
    return {'adopt':len(reasons)==0,'reasons':reasons}

class Ledger:
    def __init__(self):self.revision=0;self.labels=(np.arange(8)%2).tolist();self.events=[]
    def change(self,cue,value):
        self.revision+=1;self.labels[cue]=int(value);self.events.append({'revision':self.revision,'cue':int(cue),'value':int(value)})
    def export(self):return {'revision':self.revision,'labels':self.labels.copy(),'events':copy.deepcopy(self.events)}

def seal(data):return {'payload':copy.deepcopy(data),'sha256':sha(canonical(data))}
def unseal(env,expected):
    if sha(canonical(env['payload']))!=env['sha256']:raise ValueError('BAD_CHECKSUM')
    p=copy.deepcopy(env['payload'])
    for key,val in expected.items():
        if p.get(key)!=val:raise ValueError('BINDING_'+key)
    return p

def check_lock():
    l=json.loads((ROOT/'protocol/LOCK.json').read_text())
    for r in l['files']:
        if file_sha(ROOT/r['path'])!=r['sha256']:raise RuntimeError('LOCK_CHANGED:'+r['path'])
    return True
