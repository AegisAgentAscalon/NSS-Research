"""Fixed-weight held-out evaluation. All ground truth lives outside Memory.
Every lifecycle/chronic-noise read is saved, not only successful endpoints.
"""
from pathlib import Path
import time
import numpy as np
import torch
from .models import *
from .util import setup,write_json,array_digest,sha,digest_tensors

class Records:
    def __init__(self,seed,mode):self.seed=seed;self.mode=mode;self.rows=[];self.arrays={};self.counter=0;self.traces=[]
    def add(self,case,m,y,**meta):
        p=m.read();self.counter+=1;key=f'p{self.counter:05d}'
        self.arrays[key]=p.numpy().astype(np.uint8)
        self.arrays[key+'_target']=y.numpy().astype(np.uint8)
        self.arrays[key+'_exist']=m.existence().numpy().astype(np.uint8)
        known=y<8;empty=y==8
        def rate(mask):return float((p[mask]==y[mask]).double().mean()) if mask.any() else None
        self.rows.append(dict(case=case,seed=self.seed,mode=self.mode,prediction_key=key,
            known_n=int(known.sum()),unknown_n=int(empty.sum()),known_accuracy=rate(known),unknown_accuracy=rate(empty),
            focus_accuracy=float((p[:,0]==y[:,0]).double().mean()),existence_accuracy=float((m.existence()==(y<8)).double().mean()),
            present_unreadable_fraction=float((m.read_status()==2).double().mean()),**meta))
        return p
    def trace(self,key,answers,y,existences=None,**meta):
        a=np.stack(answers);self.arrays[key]=a
        target=y.numpy().astype(np.uint8);self.arrays[key+'_target']=target
        e=np.stack(existences) if existences is not None else a<8
        self.arrays[key+'_exist']=e.astype(np.uint8)
        self.traces.append(dict(key=key,shape=list(a.shape),every_read_stream_success=float(((a==target[None])&(e==(target<8)[None])).all(axis=(0,2)).mean()),
            answer_only_stream_success=float((a==target[None]).all(axis=(0,2)).mean()),**meta))

def make(rep,old,new,mode,n=64):return Memory(rep,mode,old,new,n)

def initialize(m):
    base=torch.arange(len(m.z)).remainder(8);y=torch.full(m.z.shape[:2],UNKNOWN,dtype=torch.long)
    m.event('write',1,base);y[:,1]=base
    m.event('write',2,(base+3)%8);y[:,2]=(base+3)%8
    return y,base

def generators(seed,case):
    return (torch.Generator().manual_seed(20_000_000+seed*100+case),torch.Generator().manual_seed(30_000_000+seed*100+case))

def noisy_step(m,gc,gp,sigma,common=False,content_sigma=None,guard=True):
    # ALWAYS draw the same 16+4 coordinates, including arms which do not use p.
    # Changing width cannot shift subsequent content-noise draws.
    c=torch.randn(m.z.shape,generator=gc)*(sigma if content_sigma is None else content_sigma)
    p4=torch.randn((*m.z.shape[:2],4),generator=gp)*sigma
    if common:p4=p4[...,:1].expand_as(p4).clone()
    p=p4[...,:m.width] if m.p is not None else None
    m.maintain(c,p,guard=guard)

@torch.no_grad()
def lifecycle(rep,old,new,mode,seed,rec,sigma,length=1024):
    m=make(rep,old,new,mode);y,base=initialize(m);gc,gp=generators(seed,100+int(sigma*1000))
    all_ok=torch.ones(len(y),dtype=torch.bool)
    for ph,phase in enumerate(('empty','first_write','correction','cleared','rewritten')):
        if phase in ('first_write','correction','rewritten'):
            offset={'first_write':1,'correction':2,'rewritten':4}[phase]
            m.event('write',0,(base+offset)%8,score=.5001);y[:,0]=(base+offset)%8
        elif phase=='cleared':m.event('clear',0);y[:,0]=UNKNOWN
        p=rec.add('lifecycle',m,y,sigma=sigma,phase=phase,round=0);all_ok&=((p==y)&(m.existence()==(y<8))).all(-1)
        answers=[p.numpy().astype(np.uint8)];exists=[m.existence().numpy().astype(np.uint8)]
        for t in range(1,length+1):
            if t==17:m.event('write',0,(base+6)%8,score=.4999)
            if t==33:m.event('write',0,(base+7)%8,score=1.,scope='unrelated')
            noisy_step(m,gc,gp,sigma);p=m.read();answers.append(p.numpy().astype(np.uint8));exists.append(m.existence().numpy().astype(np.uint8));all_ok&=((p==y)&(m.existence()==(y<8))).all(-1)
            if t in (1,16,64,256,length):rec.add('lifecycle',m,y,sigma=sigma,phase=phase,round=t,all_read_stream_success=float(all_ok.double().mean()))
        rec.trace(f'trace_life_{int(sigma*1000)}_{ph}',answers,y,existences=exists,case='lifecycle',sigma=sigma,phase=phase)
    m.event('clear_all');y.fill_(8);rec.add('global_clear',m,y,sigma=sigma,round=0)
    for t in range(1,129):
        noisy_step(m,gc,gp,sigma)
        if t in (1,128):rec.add('global_clear',m,y,sigma=sigma,round=t)

@torch.no_grad()
def extended(rep,old,new,mode,seed,rec):
    m=make(rep,old,new,mode);y,base=initialize(m);gc,gp=generators(seed,900)
    answers=[m.read().numpy().astype(np.uint8)];exists=[m.existence().numpy().astype(np.uint8)];ok=torch.ones(len(y),dtype=torch.bool)
    for t in range(1,4097):
        noisy_step(m,gc,gp,.15);p=m.read();answers.append(p.numpy().astype(np.uint8));exists.append(m.existence().numpy().astype(np.uint8));ok&=((p==y)&(m.existence()==(y<8))).all(-1)
        if t in (1024,4096):rec.add('extended_empty',m,y,round=t,sigma=.15,all_read_stream_success=float(ok.double().mean()))
    rec.trace('trace_extended_empty',answers,y,existences=exists,case='extended_empty',sigma=.15)
    m.event('write',0,(base+2)%8,score=.5001);y[:,0]=(base+2)%8
    p=rec.add('extended_write',m,y,round=0,sigma=.15);answers=[p.numpy().astype(np.uint8)];exists=[m.existence().numpy().astype(np.uint8)]
    for t in range(1,257):
        noisy_step(m,gc,gp,.15);p=m.read();answers.append(p.numpy().astype(np.uint8));exists.append(m.existence().numpy().astype(np.uint8))
        if t in (1,256):rec.add('extended_write',m,y,round=t,sigma=.15)
    rec.trace('trace_extended_write',answers,y,existences=exists,case='extended_write',sigma=.15)

@torch.no_grad()
def presence_chronic(rep,old,new,mode,seed,rec):
    if mode not in ('split1','split4','coupled17','fixed1','fixed4','hold1'):return
    for sigma,common in ((.15,False),(.30,False),(.45,False),(.30,True),(.45,True)):
        m=make(rep,old,new,mode);y,base=initialize(m);gc,gp=generators(seed,1000+int(sigma*1000))
        ok=torch.ones(len(y),dtype=torch.bool);answers=[m.read().numpy().astype(np.uint8)];exists=[m.existence().numpy().astype(np.uint8)]
        for t in range(1,2049):
            noisy_step(m,gc,gp,sigma,common=common,content_sigma=0.)
            p=m.read();answers.append(p.numpy().astype(np.uint8));exists.append(m.existence().numpy().astype(np.uint8));ok&=((p==y)&(m.existence()==(y<8))).all(-1)
            if t in (1,16,128,1024,2048):
                rec.add('presence_chronic',m,y,sigma=sigma,common=common,round=t,all_read_stream_success=float(ok.double().mean()))
        rec.trace(f'trace_presence_{int(sigma*1000)}_{int(common)}',answers,y,existences=exists,case='presence_chronic',sigma=sigma,common=common)
        m.event('write',1,(base+5)%8);y[:,1]=(base+5)%8;m.event('clear',0);y[:,0]=8
        rec.add('presence_chronic_rewrite',m,y,sigma=sigma,common=common,round=0)

@torch.no_grad()
def faults(rep,old,new,mode,seed,rec):
    fault_names=('one_sign','all_signs','erase_presence','erase_content')
    for fault in fault_names:
        m=make(rep,old,new,mode);y,base=initialize(m)
        if fault!='erase_content' and m.p is None and m.flag is None:continue
        if fault=='erase_content':m.z[:,1]=0.
        elif m.flag is not None:
            if fault=='erase_presence':m.flag[:,0:2]=False
            else:m.flag[:,0:2]=~m.flag[:,0:2]
        elif fault=='one_sign':m.p[:,0:2,0]*=-1
        elif fault=='all_signs':m.p[:,0:2]*=-1
        else:m.p[:,0:2]=0.
        rec.add('state_fault',m,y,fault=fault,round=0)
        for t in range(1,129):
            m.maintain()
            if t in (1,4,128):rec.add('state_fault',m,y,fault=fault,round=t)
        m.event('write',1,(base+5)%8);y[:,1]=(base+5)%8;m.event('clear',0);y[:,0]=8;m.maintain()
        rec.add('fault_repaired_by_events',m,y,fault=fault,round=1)

@torch.no_grad()
def write_delivery(rep,old,new,mode,seed,rec):
    for old_kind in ('empty','populated'):
        for delivery in ('content_only','whole_state'):
            for alpha in (.25,.5,.75,1.):
                m=make(rep,old,new,mode);y,base=initialize(m)
                if old_kind=='populated':m.event('write',0,base);y[:,0]=base
                before=m.z[:,0].clone();bp=m.p[:,0].clone() if m.p is not None else None
                value=(base+1)%8;m.event('write',0,value,score=.5001);y[:,0]=value
                m.z[:,0]=before*(1-alpha)+m.z[:,0]*alpha
                if delivery=='whole_state' and m.p is not None:m.p[:,0]=bp*(1-alpha)+m.p[:,0]*alpha
                # Protected boolean intentionally still knows a write happened.
                rec.add('write_delivery',m,y,old_kind=old_kind,delivery=delivery,alpha=alpha,round=0)
                for t in range(1,17):
                    m.maintain()
                    if t in (1,4,16):rec.add('write_delivery',m,y,old_kind=old_kind,delivery=delivery,alpha=alpha,round=t)

@torch.no_grad()
def local_dynamics(new,mode):
    if mode not in ('split1','split4'):return None
    result=[]
    for sign in (-1.,1.):
        p=torch.full((new.width,),sign)
        for _ in range(128):p=new(p)
        eps=.0001;eye=torch.eye(new.width)*eps
        jac=((new(p+eye)-new(p-eye))/(2*eps)).T.double()
        result.append(dict(start_sign=sign,settled=p.tolist(),spectral_radius=float(torch.linalg.eigvals(jac).abs().max()),epsilon=eps))
    return result

@torch.no_grad()
def evaluate_one(root,out,seed,mode,learn_seed=None,checkpoint_dir=None,development=False):
    setup();root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    stem=f'{mode}_rep{seed}'
    if (out/(stem+'.json')).exists():raise FileExistsError('Immutable evaluation')
    rep,old,new=load_components(root,seed,mode,learn_seed,checkpoint_dir)
    before=[digest_tensors(x.state_dict()) if x else None for x in (rep,old,new)]
    rec=Records(seed,mode);start=time.perf_counter()
    for sigma in (0.,.15,.30):lifecycle(rep,old,new,mode,seed,rec,sigma)
    extended(rep,old,new,mode,seed,rec)
    presence_chronic(rep,old,new,mode,seed,rec)
    faults(rep,old,new,mode,seed,rec)
    write_delivery(rep,old,new,mode,seed,rec)
    dynamics=local_dynamics(new,mode)
    after=[digest_tensors(x.state_dict()) if x else None for x in (rep,old,new)]
    if before!=after:raise RuntimeError('Evaluation mutated weights')
    np.savez_compressed(out/(stem+'.npz'),**rec.arrays)
    result=dict(status='RUN',development=development,seed=seed,mode=mode,rows=rec.rows,traces=rec.traces,
        metric_rows=len(rec.rows),saved_answer_evaluations=sum(v.size for k,v in rec.arrays.items() if not k.endswith(('_target','_exist'))),
        array_digest=array_digest(*[rec.arrays[k] for k in sorted(rec.arrays)]),model_digests=before,
        evaluation_parameter_updates=0,elapsed_seconds=time.perf_counter()-start,protocol_sha256=sha(root/'spec/protocol.json'),local_dynamics=dynamics,
        raw_state_bytes_per_stream=make(rep,old,new,mode).raw_state_bytes()//64)
    write_json(out/(stem+'.json'),result)
    print(stem,'rows',len(rec.rows),'seconds',round(result['elapsed_seconds'],2),flush=True)
    return result
