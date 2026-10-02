"""Predeclared repair/binding factorial. All weights frozen; no optimizer here.

Initial exact-visible stores isolate maintenance. Separate learned-writer streams
measure propagation to legitimate changes. Identity dictionary is protected and
contains no graph edges; target graph is only used by scoring.
"""
import copy,json,time,argparse
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from safetensors.torch import load_file
from . import ROOT,repair
from nbr006 import data,models,common as c
from nbr006.eval import install

METHODS=('none','normalize','intrinsic_mlp','learned_dictionary','nearest')
DEPTHS=(1,2,4,8)

def problem(seed,h=4,b=128):
    parts=[data.batch(np.random.default_rng(seed+int(m)*300001),b//2,max_h=h,hops=h,missing=m) for m in (False,True)]
    return {k:np.concatenate([p[k] for p in parts]) for k in parts[0]}
def load_models(seed,root=ROOT,dev=False):
    ps=801 if dev else seed-100
    readers={k:models.make(k) for k in ('record_hop','gated_hop')}
    for k,v in readers.items():v.load_state_dict(load_file(str(root/'reference/checkpoints'/f'{k}_{ps}.safetensors')))
    binder=models.make('binder');binder.load_state_dict(load_file(str(root/'reference/checkpoints'/f'binder_{ps}.safetensors')))
    folder=root/('evidence/development' if dev else 'checkpoints')
    fitted={k:repair.make(k) for k in ('learned_dictionary','intrinsic_mlp')}
    for k,m in fitted.items():m.load_state_dict(load_file(str(folder/f'{k}_{seed}.safetensors')))
    allmodels={**readers,'binder':binder,**fitted}
    for m in allmodels.values():
        m.eval()
        for p in m.parameters():p.requires_grad_(False)
    return readers,binder,fitted

def scores(pred,p):
    truth=data.oracle_answer(p);n=p['codes'].shape[1]-1
    known=truth!=n;room=(pred[:,None]==p['rooms']).any(1);hit=pred==truth
    return {'accuracy':float(hit.mean()),'known_accuracy':float(hit[known].mean()) if known.any() else None,'unknown_accuracy':float(hit[~known].mean()) if (~known).any() else None,'unsupported_room_rate':float(room[~known].mean()) if (~known).any() else None,'unresolved_rate':float(((pred!=n)&~room).mean()),'n':len(pred),'known_n':int(known.sum()),'unknown_n':int((~known).sum())}

def statehash(k,v,e):
    import hashlib
    return hashlib.sha256(k.numpy().tobytes()+v.numpy().tobytes()+e.numpy().tobytes()).hexdigest()

def exposure(k,v,e,book,kind,fitted,rng,steps,sigma,fields,policy='periodic',maintenance_fields=None):
    """Fixed repair budget: one field repair per noise tick, not per query round."""
    model=fitted.get(kind)
    mf=fields if maintenance_fields is None else maintenance_fields
    for _ in range(steps):
        # Always draw both arrays: same stochastic schedule for all interventions.
        nk=torch.from_numpy(rng.normal(0,sigma,k.shape).astype(np.float32))
        nv=torch.from_numpy(rng.normal(0,sigma,v.shape).astype(np.float32))
        if fields in ('keys','both'):k=k+nk*e[...,None]
        if fields in ('values','both'):v=v+nv*e[...,None]
        if policy=='periodic':k,v=repair.maintain(k,v,e,book,kind,model,mf)
    if policy=='late_equal':
        for _ in range(steps):k,v=repair.maintain(k,v,e,book,kind,model,mf)
    return k,v

@torch.no_grad()
def evaluate(seed,outdir,dev=False,quick=False,only=None):
    c.setup(seed);readers,binder,fitted=load_models(seed,dev=dev)
    hashes={k:c.weights_hash(v) for k,v in {**readers,**fitted,'binder':binder}.items()}
    rows=[];arrays={};states=[];start=time.perf_counter();idx=0;b=32 if quick else 64
    methods=METHODS if only is None else tuple(only.split(','))
    def record(case,method,p,k,v,e,q=None,book=None,extra=None,canonical_slots=False):
        nonlocal idx
        key=f'c{idx:04d}';idx+=1
        print('CASE',seed,key,case,method,flush=True)
        truebook=torch.from_numpy(p['codes']);q=torch.from_numpy(p['q']) if q is None else q
        arrays[key+'_parent']=p['parent'].astype(np.int16);arrays[key+'_query']=p['query'].astype(np.int16);arrays[key+'_rooms']=p['rooms'].astype(np.int16)
        arrays[key+'_present']=e.numpy()
        arrays[key+'_decoded_keys']=torch.einsum('bsd,bnd->bsn',F.normalize(k,dim=-1),truebook).argmax(-1).numpy().astype(np.int16)
        arrays[key+'_decoded_values']=torch.einsum('bsd,bnd->bsn',F.normalize(v,dim=-1),truebook).argmax(-1).numpy().astype(np.int16)
        fidelity={}
        if canonical_slots:
            targetk=p['slot_ids'];targetv=np.take_along_axis(p['parent'],targetk,1)
            arrays[key+'_target_keys']=targetk.astype(np.int16);arrays[key+'_target_values']=targetv.astype(np.int16)
            live=e.numpy();kp=arrays[key+'_decoded_keys'];vp=arrays[key+'_decoded_values']
            fidelity={'key_identity_accuracy':float((kp==targetk)[live].mean()),'value_identity_accuracy':float((vp==targetv)[live].mean())}
            rr=np.arange(len(k))[:,None]
            kt=p['codes'][rr,targetk];vt=p['codes'][rr,targetv]
            fidelity['key_cosine']=float((F.normalize(k,dim=-1).numpy()*kt).sum(-1)[live].mean())
            fidelity['value_cosine']=float((F.normalize(v,dim=-1).numpy()*vt).sum(-1)[live].mean())
        states.append({'key':key,'case':case,'method':method,'state_hash':statehash(k,v,e),**fidelity,**(extra or {})})
        for name,reader in readers.items():
            out=reader(k,v,e,q,8);pred=models.logits(out,truebook).argmax(-1).numpy()[:,[0,1,3,7]]
            arrays[key+'_'+name]=pred.astype(np.int16)
            for j,d in enumerate(DEPTHS):
                rows.append({'key':key,'case':case,'method':method,'reader':name,'seed':seed,'depth':d,**scores(pred[:,j],p),**fidelity,**(extra or {})})
    # Controlled state corruption: explicit initial store, no post-install writes.
    scenarios=[('clean4',4,0,0.,'both'),('keys02_t64',4,64,.02,'keys'),('values02_t64',4,64,.02,'values'),('both02_t64',4,64,.02,'both'),('both08_t64',4,64,.08,'both'),('both02_t1024_h8',8,1024,.02,'both')]
    if quick:scenarios=scenarios[:4]
    for case,h,t,sigma,fields in scenarios:
        p=problem(81000000+seed*100+h,h,b);base=data.tensors(p);book=base[-1]
        for kind in methods:
            rng=np.random.default_rng(620000+seed)
            k,v=exposure(base[0].clone(),base[1].clone(),base[2],book,kind,fitted,rng,t,sigma,fields)
            record('isolation/'+case,kind,p,k,v,base[2],canonical_slots=True,extra={'noise_sigma':sigma,'ticks':t,'repair_schedule':'periodic','repair_fields':fields})
    if quick:return finalize(seed,outdir,rows,arrays,states,hashes,readers,binder,fitted,start)
    # Query-only shift: intact storage, one repair before the unchanged reader.
    for sigma in (.05,.2,.4):
        p=problem(83000000+seed,4,b);k,v,e,q,book=data.tensors(p)
        rng=np.random.default_rng(81000+seed)
        noisy=q.clone();noisy[:,:16]+=torch.from_numpy(rng.normal(0,sigma,(b,16)).astype(np.float32));noisy=F.normalize(noisy,dim=-1)
        for kind in methods:
            qq=repair.apply(kind,noisy[:,None,:],book,fitted.get(kind))[:,0]
            record(f'query/sigma{sigma}',kind,p,k,v,e,qq,canonical_slots=True)
    # Equal call count after damage, versus periodic maintenance.
    for ticks in (64,1024):
        p=problem(81000000+seed*100+4,4,b);k0,v0,e,q,book=data.tensors(p)
        for kind in ('learned_dictionary','nearest'):
            if kind not in methods:continue
            k,v=exposure(k0.clone(),v0.clone(),e,book,kind,fitted,np.random.default_rng(620000+seed),ticks,.02,'both',policy='late_equal')
            record(f'ablation/late_equal{ticks}',kind,p,k,v,e,canonical_slots=True,extra={'ticks':ticks,'repair_schedule':'late_equal'})
    # Isolate which damaged field requires repair when both are corrupted.
    p=problem(81000000+seed*100+4,4,b);k0,v0,e,q,book=data.tensors(p)
    for mf in ('keys','values'):
        for kind in ('learned_dictionary','nearest'):
            if kind not in methods:continue
            k,v=exposure(k0.clone(),v0.clone(),e,book,kind,fitted,np.random.default_rng(620000+seed),64,.02,'both',maintenance_fields=mf)
            record(f'ablation/repair_{mf}_only',kind,p,k,v,e,canonical_slots=True)
    # State/depth ablation: useful depth remains distinct from event-time repair.
    p=problem(81000000+seed*100+8,8,b);k0,v0,e,q,book=data.tensors(p)
    for kind in ('learned_dictionary','nearest'):
        if kind not in methods:continue
        record('ablation/state_off_h8',kind,p,k0*0,v0*0,e&False,canonical_slots=False)
    # End-to-end learned installation, live distractor writes and lifecycle.
    for kind in methods:
        rng=np.random.default_rng(84000000+seed);p=problem(84000000+seed,4,b)
        st=install(p,binder);book=torch.from_numpy(p['codes']);rr=np.arange(b);focus=p['order'][:,2];old=p['parent'][rr,focus].copy()
        phases=('initial','correction','clear','rewrite','reset','new_scope')
        for phase in phases:
            if phase in ('correction','clear','rewrite'):
                dest=p['rooms'][:,1] if phase=='correction' else np.full(b,16) if phase=='clear' else old
                op=-1 if phase=='clear' else 1
                qualified=(dest!=16) if phase=='rewrite' else np.ones(b,bool)
                # If original relation was absent, rewriting means leave it cleared.
                st.event(torch.from_numpy(p['codes'][rr,focus]),torch.from_numpy(p['codes'][rr,dest]),op,torch.from_numpy(qualified))
                p['parent'][rr,focus]=dest
            elif phase=='reset':
                st.clear_all();p['parent'][:]=16
            elif phase=='new_scope':
                p=problem(84500000+seed,4,b);st=install(p,binder);book=torch.from_numpy(p['codes'])
            for j in range(64):
                if phase!='reset':
                    ids=p['order'][:,-1];dst=p['rooms'][:,j%2]
                    allowed=j%7 not in (0,1)
                    st.event(torch.from_numpy(p['codes'][rr,ids]),torch.from_numpy(p['codes'][rr,dst]),1,qualified=(j%7!=1),scope='other' if j%7==0 else 'study')
                    if allowed:p['parent'][rr,ids]=dst
                st.keys,st.vals=exposure(st.keys,st.vals,st.present,book,kind,fitted,rng,1,.02,'both')
            record('stream/'+phase,kind,p,*st.snapshot())
    # Registered failure boundaries: identity catalogue is not a record archive.
    for fault in ('unknown_identity','wrong_dictionary','wrong_valid_value','erased_value'):
        p=problem(85000000+seed,4,b);k0,v0,e,q,book=data.tensors(p);rr=np.arange(b)
        if fault=='unknown_identity':
            rng=np.random.default_rng(89000000+seed);q=torch.zeros_like(q);q[:,:16]=torch.from_numpy(data.normalize(rng.normal(size=(b,16))).astype(np.float32))
            p['query'][:]=16 # scorer expects no relation for an unregistered subject
        for kind in methods:
            k,v=k0.clone(),v0.clone();qq=q.clone();usedbook=book
            if fault=='wrong_dictionary':
                # Corrupt identity references, not the original evidence/scoring book.
                usedbook=book.clone();usedbook[:,:16,:16]=usedbook[:,:16,:16].roll(1,-1)
                k,v=repair.maintain(k,v,e,usedbook,kind,fitted.get(kind),'both')
            elif fault in ('wrong_valid_value','erased_value'):
                focus=p['order'][:,2];slots=(p['slot_ids']==focus[:,None]).argmax(1)
                live=e[torch.arange(b),torch.from_numpy(slots)]
                if fault=='wrong_valid_value':v[torch.arange(b)[live],torch.from_numpy(slots)[live]]=book[torch.arange(b)[live],torch.from_numpy(p['rooms'][:,1])[live]]
                else:v[torch.arange(b)[live],torch.from_numpy(slots)[live]]=0
                k,v=repair.maintain(k,v,e,book,kind,fitted.get(kind),'both')
            else:qq=repair.apply(kind,qq[:,None,:],book,fitted.get(kind))[:,0]
            record('fault/'+fault,kind,p,k,v,e,qq)
    return finalize(seed,outdir,rows,arrays,states,hashes,readers,binder,fitted,start)

def finalize(seed,outdir,rows,arrays,states,hashes,readers,binder,fitted,start):
    current={k:c.weights_hash(v) for k,v in {**readers,**fitted,'binder':binder}.items()}
    if hashes!=current:raise RuntimeError('Evaluation mutated learned weights')
    d=Path(outdir);d.mkdir(parents=True,exist_ok=True)
    path=d/f'pair_{seed}.npz'
    if path.exists():raise FileExistsError(path)
    np.savez_compressed(path,**arrays)
    info={'seed':seed,'rows':rows,'states':states,'state_count':len(states),'rows_count':len(rows),'answer_evaluations':sum(r['n'] for r in rows),'seconds':time.perf_counter()-start,'frozen_weight_hashes':hashes,'weights_unchanged':True,'array_sha256':c.sha(path),'environment':c.env()}
    c.dump(path.with_suffix('.json'),info)
    print('EVALUATED',seed,len(states),len(rows),info['seconds'],flush=True)
    return info
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seed',type=int,required=True);a.add_argument('--out',default=str(ROOT/'results'));a.add_argument('--dev',action='store_true');a.add_argument('--quick',action='store_true');a.add_argument('--only');p=a.parse_args();evaluate(p.seed,p.out,p.dev,p.quick,p.only)
