"""Scoped frozen-reader comparisons. Event truth is confined to generators/scorer.

Predeclared core and stress conditions; serial paired schedules. No online update.
"""
import argparse,copy,time
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from .common import *
from .config import *
from .pipeline import make_problem,install,read
from .samples import sample


def metric(pred,p):
    truth=data.oracle_answer(p);known=truth!=16;hit=pred==truth;room=(pred[:,None]==p['rooms']).any(-1)
    return {'n':len(pred),'known_n':int(known.sum()),'unknown_n':int((~known).sum()),'correct_n':int(hit.sum()),'known_correct_n':int(hit[known].sum()),'unknown_correct_n':int(hit[~known].sum()),'unsupported_room_n':int(room[~known].sum()),'known_accuracy':float(hit[known].mean()) if known.any() else None,'unknown_accuracy':float(hit[~known].mean()) if (~known).any() else None,'unsupported_room_rate':float(room[~known].mean()) if (~known).any() else None,'accuracy':float(hit.mean())}

@torch.no_grad()
def expose(s,r,rng,ticks,sigma,fields='both',cadence=1,common=False):
    # Observer-only damage tracker; never passed to a resolver/reader.
    book=s.book;mask=s.present
    def decode(x):return torch.einsum('bsd,bnd->bsn',F.normalize(x,dim=-1),book).masked_fill(~s.active[:,None,:],-1e6).argmax(-1)
    ideal_k=decode(s.store.keys);ideal_v=decode(s.store.vals)
    first_wrong=np.full(len(book),-1,np.int32);first_unread=np.full(len(book),-1,np.int32)
    calls0=r.calls;t=time.perf_counter()
    for j in range(ticks):
        s.add_noise(rng,sigma,fields,common)
        if cadence>0 and (j+1)%cadence==0:
            s.maintain(r,fields)
            wrong=((((decode(s.store.keys)!=ideal_k)|(decode(s.store.vals)!=ideal_v))&mask).any(-1)).numpy()
            unread=((~s.kr|~s.vr)&mask).any(-1).numpy()
            first_wrong[(first_wrong<0)&wrong]=j+1;first_unread[(first_unread<0)&unread]=j+1
    if cadence==0 or (ticks%max(1,cadence)):
        s.maintain(r,fields)
    return {'first_wrong':first_wrong,'first_unreadable':first_unread,'maintenance_calls':r.calls-calls0,'seconds':time.perf_counter()-t}

@torch.no_grad()
def evaluate(pair,out,dev=False,quick=False,only=None):
    seed=1000 if dev else 1000+pair;setup(seed);models=parents(pair);head,cfg=load_gate(seed,dev);frozen=model_hashes({**models,'head':head})
    methods=tuple(only.split(',')) if only else METHODS
    dpair=pair+10000 if dev else pair
    b=16 if quick else 64;rows=[];arrays={};cases=[];counter=0;t=time.perf_counter()
    def record(label,m,p,s,r,q=None,extra=None):
        nonlocal counter
        key=f'c{counter:04d}';counter+=1;q=torch.from_numpy(p['q']) if q is None else q
        arrays[key+'_parent']=p['parent'].astype(np.int16);arrays[key+'_query']=p['query'].astype(np.int16);arrays[key+'_rooms']=p['rooms'].astype(np.int16)
        arrays[key+'_q_vector']=q.numpy();arrays[key+'_book']=s.book.numpy().copy();arrays[key+'_active']=s.active.numpy().copy()
        for n in ('keys','vals','present'):arrays[key+'_'+n]=getattr(s.store,n).numpy().copy()
        arrays[key+'_kr']=s.kr.numpy().copy();arrays[key+'_vr']=s.vr.numpy().copy()
        cases.append({'key':key,'case':label,'method':m,'state_signature':s.signature(),'raw_state_bytes_per_stream':s.bytes()/b,**(extra or {})})
        for name in ('record_hop','gated_hop','exact'):
            answer=read(s,models.get(name),r,q,8,exact=name=='exact')
            for n,v in answer.items():
                if n!='qs':arrays[key+'_'+name+'_'+n]=v.numpy()
            for depth in (1,2,4,8):rows.append({'key':key,'case':label,'method':m,'reader':name,'pair':pair,'depth':depth,**metric(answer['pred'][:,depth-1].numpy(),p)})
        print('STATE',pair,key,label,m,flush=True)
    scenarios=[('clean_h4',4,0,.0,'both'),('keys02_t64',4,64,.02,'keys'),('values02_t64',4,64,.02,'values'),('both02_t64',4,64,.02,'both'),('both02_t1024_h8',8,1024,.02,'both'),('both08_t64',4,64,.08,'both')]
    if quick:scenarios=[scenarios[0],scenarios[3]]
    for label,h,nt,sigma,fields in scenarios:
        p=make_problem((510000000 if not dev else 500000000)+dpair*1000+h,h,b)
        for m in methods:
            r=resolver(m,models,head,cfg);s=install(p,models['binder']);stats=expose(s,r,np.random.default_rng(520000000+dpair),nt,sigma,fields)
            extra={k:v for k,v in stats.items() if not isinstance(v,np.ndarray)}
            record('storage/'+label,m,p,s,r,extra=extra)
            key=cases[-1]['key'];arrays[key+'_first_wrong']=stats['first_wrong'];arrays[key+'_first_unreadable']=stats['first_unreadable']
    # Query-only conditions, no changed storage, no automatic registration.
    families=('known_q05','known_q20','novel','novel_near010','known_q40') if not quick else ('known_q20','novel')
    for j,family in enumerate(families):
        p=make_problem((530000000 if not dev else 500010000)+dpair,4,b);rng=np.random.default_rng(530100000+dpair+j)
        q=p['q'].copy()
        if family.startswith('known_q'):
            sigma={'known_q05':.05,'known_q20':.2,'known_q40':.4}[family];q[:,:16]+=rng.normal(0,sigma,(b,16)).astype(np.float32);q=data.normalize(q).astype(np.float32)
        elif family=='novel':
            q.fill(0);q[:,:16]=data.normalize(rng.normal(size=(b,16))).astype(np.float32);p['query'][:]=16
        else:
            q[:,:16]+=rng.normal(0,.1,(b,16)).astype(np.float32);q=data.normalize(q).astype(np.float32);p['query'][:]=16
        for m in methods:
            r=resolver(m,models,head,cfg);s=install(p,models['binder']);record('query/'+family,m,p,s,r,torch.from_numpy(q))
    if not quick:
        # Declared maintenance cadence grid, applied to geometric and learned gate
        # with nearest restoration. Both prespecified even if a joint screen fails.
        for cadence in (8,32,0):
            p=make_problem(510000000+dpair*1000+8,8,b)
            for m in ('nearest','A_nearest','B_nearest'):
                if m not in methods:continue
                r=resolver(m,models,head,cfg);s=install(p,models['binder']);stats=expose(s,r,np.random.default_rng(520000000+dpair),1024,.02,'both',cadence)
                record('cadence/'+str(cadence),m,p,s,r,extra={'cadence':cadence,'maintenance_calls':stats['maintenance_calls'],'seconds':stats['seconds']})
        # State-removal and impossible recovery controls.
        for fault in ('state_off','erased_value','wrong_valid_value','common_noise'):
            p=make_problem(540000000+dpair,4,b)
            for m in ('nearest','A_nearest','B_nearest'):
                if m not in methods:continue
                r=resolver(m,models,head,cfg);s=install(p,models['binder'])
                if fault=='state_off':s.store.clear_all();s.kr.zero_();s.vr.zero_()
                elif fault=='common_noise':expose(s,r,np.random.default_rng(540100000+dpair),64,.08,'both',1,True)
                else:
                    focus=p['order'][:,2];slot=(p['slot_ids']==focus[:,None]).argmax(-1);rr=np.arange(b);live=s.present[rr,slot]
                    if fault=='erased_value':s.store.vals[rr[live],slot[live]]=0
                    else:s.store.vals[rr[live],slot[live]]=torch.from_numpy(p['codes'][rr[live],p['rooms'][live,1]])
                    s.maintain(r)
                record('fault/'+fault,m,p,s,r)
        # Writable novelty through the inherited binder. New code unavailable until
        # REGISTER; registering an identity supplies NO relation.
        for m in methods:
            r=resolver(m,models,head,cfg);p=make_problem(550000000+dpair,4,b,n=12);s=install(p,models['binder'],r,True)
            rng=np.random.default_rng(550100000+dpair);new=np.zeros((b,17),np.float32);new[:,:16]=data.normalize(rng.normal(size=(b,16))).astype(np.float32)
            rr=np.arange(b);original_q=p['q'].copy();original_query=p['query'].copy()
            p['q']=new.copy();p['query'][:]=16
            for phase in ('before_register','after_register','after_write','correction','clear','rewrite','reset','fresh'):
                if phase=='after_register':
                    rc=s.register(torch.from_numpy(new));assert rc['added'].all();p['codes'][:,12]=new;p['query'][:]=12
                elif phase in ('after_write','correction','clear','rewrite'):
                    # Use a multi-hop tail for first write and rewrite; supplied room
                    # alternative for correction. Missing tails remain missing.
                    dest=p['order'][:,3] if phase in ('after_write','rewrite') else p['rooms'][:,1] if phase=='correction' else np.full(b,16)
                    val=torch.from_numpy(p['codes'][rr,dest]);s.event(torch.from_numpy(new),val,-1 if phase=='clear' else 1,r,True)
                    p['parent'][:,12]=dest
                elif phase=='reset':s.clear_scope();p['parent'][:]=16;p['query'][:]=16
                elif phase=='fresh':
                    # A fresh explicit scope setup, then registration and one write.
                    p=make_problem(551000000+dpair,4,b,n=12);s=install(p,models['binder'],r,True)
                    s.register(torch.from_numpy(new));p['codes'][:,12]=new;p['q']=new.copy();p['query'][:]=12
                    dest=p['rooms'][:,0];s.event(torch.from_numpy(new),torch.from_numpy(p['codes'][rr,dest]),1,r,True);p['parent'][:,12]=dest
                # Match background events and noise, preserve write authority.
                for j in range(64):
                    if phase!='reset':
                        ids=p['order'][:,-1];dst=p['rooms'][:,j%2];allowed=j%7 not in (0,1)
                        s.event(torch.from_numpy(p['codes'][rr,ids]),torch.from_numpy(p['codes'][rr,dst]),1,r,j%7!=1,'other' if j%7==0 else 'study')
                        if allowed:p['parent'][rr,ids]=dst
                    s.add_noise(rng,.02);s.maintain(r)
                record('registration/'+phase,m,p,s,r)
                if phase not in ('reset','fresh'):
                    neighbor=copy.deepcopy(p);neighbor['q']=original_q;neighbor['query']=original_query
                    record('neighbor/'+phase,m,neighbor,s,r)
        # Registered near-collision stress, not silently merged by the registry.
        for m in ('nearest','A_nearest','B_nearest'):
            if m not in methods:continue
            r=resolver(m,models,head,cfg);p=make_problem(560000000+dpair,4,b,n=12);s=install(p,models['binder'],r,True)
            rng=np.random.default_rng(560100000+dpair);near=p['codes'][:,0].copy();near[:,:16]+=rng.normal(0,.01,(b,16)).astype(np.float32);near=data.normalize(near).astype(np.float32)
            s.register(torch.from_numpy(near));p['codes'][:,12]=near;p['query'][:]=12;p['q']=near.copy()
            dest=p['rooms'][:,1];s.event(torch.from_numpy(near),torch.from_numpy(p['codes'][np.arange(b),dest]),1,r,True);p['parent'][:,12]=dest
            record('stress/near_registered_write',m,p,s,r)
    current=model_hashes({**models,'head':head});assert frozen==current,'Frozen weights changed'
    path=Path(out)/f'state_pair{pair}.npz';path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError(path)
    np.savez_compressed(path,**arrays);info={'pair':pair,'seed':seed,'quick':quick,'n_per_state':b,'cases':cases,'rows':rows,'n_cases':len(cases),'n_rows':len(rows),'answer_evaluations':sum(x['n'] for x in rows),'seconds':time.perf_counter()-t,'frozen_weights':frozen,'weights_unchanged':True,'array_sha256':sha(path),'environment':env()}
    dump(path.with_suffix('.json'),info);print('EVALUATED',pair,len(cases),info['seconds'],flush=True);return info
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pair',type=int,required=True);p.add_argument('--out',required=True);p.add_argument('--dev',action='store_true');p.add_argument('--quick',action='store_true');p.add_argument('--only');a=p.parse_args();evaluate(a.pair,a.out,a.dev,a.quick,a.only)
