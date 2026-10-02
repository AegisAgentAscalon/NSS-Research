"""Held-out fixed-weight evaluations. Scorer targets are outside Memory.
All noise streams are matched across mechanisms by seed, not by outcomes.
"""
from pathlib import Path
import time
import numpy as np
import torch
from .models import *
from .util import setup,write_json,array_digest,sha,digest_tensors

class Records:
    def __init__(self,seed,mode):self.seed=seed;self.mode=mode;self.rows=[];self.arrays={};self.counter=0
    def add(self,name,m,y,**meta):
        pred=m.read();self.counter+=1;key=f'p{self.counter:05d}'
        self.arrays[key]=pred.numpy();self.arrays[key+'_target']=y.numpy().copy()
        known=y<8;empty=y==8
        def rate(mask):
            return float((pred[mask]==y[mask]).double().mean()) if mask.any() else None
        row=dict(case=name,seed=self.seed,mode=self.mode,prediction_key=key,known_n=int(known.sum()),unknown_n=int(empty.sum()),
                 known_accuracy=rate(known),unknown_accuracy=rate(empty),focus_accuracy=float((pred[:,0]==y[:,0]).double().mean()),
                 neighbors_accuracy=float((pred[:,1:]==y[:,1:]).double().mean()),**meta)
        self.rows.append(row);return pred

def setup_memory(rep,mode,repair,n=64):
    m=Memory(rep,mode,repair,n)
    base=torch.arange(n).remainder(8)
    y=torch.full((n,KEYS),UNKNOWN,dtype=torch.long)
    # Source events, not labels, initialize the candidate.
    m.event('write',1,base);y[:,1]=base
    m.event('write',2,(base+3)%8);y[:,2]=(base+3)%8
    return m,y,base

@torch.no_grad()
def lifecycle(rep,mode,repair,seed,rec,sigma,length=1024):
    m,y,base=setup_memory(rep,mode,repair)
    g=torch.Generator().manual_seed(8_000_000+seed+int(sigma*1000)*10)
    all_ok=torch.ones(len(y),dtype=torch.bool)
    for phase in ('empty','first_write','correction','cleared','rewritten'):
        if phase in ('first_write','correction','rewritten'):
            offset={'first_write':1,'correction':2,'rewritten':4}[phase]
            value=(base+offset)%8
            m.event('write',0,value,score=.5001);y[:,0]=value
        elif phase=='cleared':m.event('clear',0);y[:,0]=UNKNOWN
        p=rec.add('lifecycle',m,y,sigma=sigma,phase=phase,round=0)
        all_ok&=(p==y).all(-1)
        ever_empty=torch.zeros_like(y,dtype=torch.bool);ever_known=torch.zeros_like(y,dtype=torch.bool)
        for t in range(1,length+1):
            # Rejected low-score and wrong-scope payloads cannot become writes.
            if t==17:m.event('write',0,(base+6)%8,score=.4999)
            if t==33:m.event('write',0,(base+7)%8,score=1.,scope='unrelated-scope')
            m.maintain(sigma*torch.randn(m.z.shape,generator=g))
            p=m.read();wrong=p!=y
            ever_empty|=wrong&(y==8);ever_known|=wrong&(y<8);all_ok&=~wrong.any(-1)
            if t in (1,16,64,256,length):
                rec.add('lifecycle',m,y,sigma=sigma,phase=phase,round=t,
                    empty_ever_error_fraction=float(ever_empty[y==8].double().mean()) if (y==8).any() else None,
                    known_ever_error_fraction=float(ever_known[y<8].double().mean()) if (y<8).any() else None,
                    all_read_stream_success=float(all_ok.double().mean()))
    m.event('clear_all');y.fill_(8)
    rec.add('global_clear',m,y,sigma=sigma,round=0)
    for t in range(1,129):
        m.maintain(sigma*torch.randn(m.z.shape,generator=g))
        if t in (1,128):rec.add('global_clear',m,y,sigma=sigma,round=t)

@torch.no_grad()
def extended(rep,mode,repair,seed,rec):
    m,y,base=setup_memory(rep,mode,repair)
    g=torch.Generator().manual_seed(9_000_000+seed)
    all_ok=torch.ones(len(y),dtype=torch.bool)
    for t in range(1,4097):
        m.maintain(.15*torch.randn(m.z.shape,generator=g));all_ok&=(m.read()==y).all(-1)
        if t in (1024,4096):rec.add('extended_empty',m,y,sigma=.15,round=t,all_read_stream_success=float(all_ok.double().mean()))
    m.event('write',0,(base+2)%8,score=.5001);y[:,0]=(base+2)%8
    rec.add('extended_first_write',m,y,sigma=.15,round=0)
    for t in range(1,257):
        m.maintain(.15*torch.randn(m.z.shape,generator=g))
        if t in (1,256):rec.add('extended_first_write',m,y,sigma=.15,round=t)

@torch.no_grad()
def shock(rep,mode,repair,seed,rec):
    for sigma in (.5,1.):
        m=Memory(rep,mode,repair,256)
        g=torch.Generator().manual_seed(10_000_000+seed+int(sigma*100))
        y=torch.randint(0,9,(256,KEYS),generator=g)
        # Every address uses real writes then exact per-row absence restoration
        # as a synthetic setup, independent from maintenance/read methods.
        for k in range(KEYS):
            m.event('write',k,y[:,k].clamp_max(7));mask=y[:,k]==8
            m.z[mask,k]=0
            if m.presence is not None:m.presence[mask,k]=False
        m.z+=sigma*torch.randn(m.z.shape,generator=g)
        rec.add('shock',m,y,sigma=sigma,round=0)
        for t in range(1,129):
            m.maintain()
            if t in (1,4,16,128):rec.add('shock',m,y,sigma=sigma,round=t)

@torch.no_grad()
def attenuated_write(rep,mode,repair,seed,rec):
    for old_kind in ('empty','populated'):
        for alpha in (.05,.1,.25,.5,.75,1.):
            m,y,base=setup_memory(rep,mode,repair)
            if old_kind=='populated':m.event('write',0,base);y[:,0]=base
            old=m.z[:,0].clone();new=(base+1)%8
            m.event('write',0,new,score=.5001);y[:,0]=new
            # Explicit post-admission delivery fault. A low score is NOT used
            # as this mixing coefficient. Presence controls know a write occurred.
            m.z[:,0]=(1-alpha)*old+alpha*m.z[:,0]
            rec.add('attenuated_write',m,y,old_kind=old_kind,alpha=alpha,round=0)
            for t in range(1,17):
                m.maintain()
                if t in (1,4,16):rec.add('attenuated_write',m,y,old_kind=old_kind,alpha=alpha,round=t)

@torch.no_grad()
def metadata_fault(rep,mode,repair,seed,rec):
    if not mode.startswith('presence_'):return
    for kind in ('false_absent','false_present'):
        m,y,base=setup_memory(rep,mode,repair)
        if kind=='false_absent':m.presence[:,1]=False
        else:m.presence[:,0]=True
        g=torch.Generator().manual_seed(11_000_000+seed)
        for t in range(1,1025):
            m.maintain(.15*torch.randn(m.z.shape,generator=g))
            if t in (1,128,1024):rec.add('metadata_fault',m,y,fault=kind,round=t)
        m.event('clear',0);y[:,0]=8
        m.event('write',1,(base+5)%8);y[:,1]=(base+5)%8
        m.maintain();rec.add('metadata_repaired_by_events',m,y,fault=kind,round=1)

@torch.no_grad()
def stability(rep,repair):
    out=[]
    for index in range(9):
        z=rep.codes[index].clone()
        for _ in range(128):z=repair(z)
        for eps in (.001,.0001):
            eye=torch.eye(D)*eps
            jac=((repair(z+eye)-repair(z-eye))/(2*eps)).T.double()
            eig=torch.linalg.eigvals(jac);sing=torch.linalg.svdvals(jac)
            out.append(dict(code=index,epsilon=eps,spectral_radius=float(eig.abs().max()),
                spectral_norm=float(sing.max()),settled_prediction=int(rep(z).argmax()),
                settled_norm=float(z.norm())))
    return out

@torch.no_grad()
def evaluate_one(root,outdir,seed,mode):
    setup();root=Path(root);outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    rep,repair=load_components(root,seed,mode)
    identity=digest_tensors(repair.state_dict()) if repair else None
    refidentity=digest_tensors(rep.state_dict());rec=Records(seed,mode);t=time.perf_counter()
    for sigma in (0.,.15,.3):lifecycle(rep,mode,repair,seed,rec,sigma)
    extended(rep,mode,repair,seed,rec)
    shock(rep,mode,repair,seed,rec)
    attenuated_write(rep,mode,repair,seed,rec)
    metadata_fault(rep,mode,repair,seed,rec)
    diagnostic=stability(rep,repair) if mode in ('historical','replay','contract','local_empty') else None
    if identity!=(digest_tensors(repair.state_dict()) if repair else None) or refidentity!=digest_tensors(rep.state_dict()):raise RuntimeError('Evaluation changed weights')
    stem=f'{mode}_rep{seed}';np.savez_compressed(outdir/(stem+'.npz'),**rec.arrays)
    result=dict(status='RUN',mode=mode,seed=seed,rows=rec.rows,stability=diagnostic,
        result_array_digest=array_digest(*[rec.arrays[k] for k in sorted(rec.arrays)]),
        weight_identity=identity,source_identity=rep.source_sha256,evaluation_parameter_updates=0,
        elapsed_seconds=time.perf_counter()-t,metric_rows=len(rec.rows),answer_evaluations=sum(rec.arrays[k].size for k in rec.arrays if not k.endswith('_target')),
        joint_success_defined_on_every_read=True,protocol_sha256=sha(root/'spec/protocol.json'))
    write_json(outdir/(stem+'.json'),result)
    print(stem,'rows',len(rec.rows),'seconds',round(result['elapsed_seconds'],2),flush=True)
    return result
