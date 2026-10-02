"""Versioned, scoped active-identity/reference and relationship working state.

No graph or origin labels are available here. Membership admission is not write
permission. Rejected fields remain present with raw data, but unreadable until a
qualified write/clear. Query operations are strictly read-only.
"""
import hashlib,json
from pathlib import Path
import numpy as np
import torch
from .common import *
from .resolver import ABI
from nbr006.store import RecordStore

class State:
    def __init__(self,book,active,binder,scope='study'):
        if book.ndim!=3 or book.shape[1:]!=(16,17) or active.shape!=book.shape[:2]:raise ValueError('Invalid reference dimensions')
        if not torch.isfinite(book).all():raise ValueError('Nonfinite reference')
        if (book[~active]!=0).any():raise ValueError('Inactive rows must be zero; no future codes')
        if active.any() and (not torch.allclose(book[active].norm(dim=-1),torch.ones_like(book[active,0]),atol=1e-4) or (book[active][:,-1].abs()>1e-5).any()):
            raise ValueError('Canonical identity codes must be unit vectors, no UNKNOWN marker')
        self.book=book.clone();self.active=active.clone();self.scope=scope
        self.store=RecordStore(len(book),16,binder,scope)
        self.kr=torch.zeros_like(self.store.present);self.vr=torch.zeros_like(self.kr)
        self.revision=np.ones(len(book),np.int64);self.tick=0
    def validate(self,expected_revision=None,scope=None):
        if scope is not None and scope!=self.scope:raise ValueError("INVALID_REFERENCE: scope")
        if expected_revision is not None and not np.array_equal(np.asarray(expected_revision),self.revision):raise ValueError("INVALID_REFERENCE: stale revision")
        if (self.book[~self.active]!=0).any() or not torch.isfinite(self.book).all():raise ValueError("INVALID_REFERENCE: damaged catalogue")
    @property
    def present(self):return self.store.present
    def signature(self):
        h=hashlib.sha256()
        for t in (self.book,self.active,self.store.keys,self.store.vals,self.present,self.kr,self.vr):h.update(t.numpy().tobytes())
        h.update(self.revision.tobytes());h.update(str(self.tick).encode());h.update(self.scope.encode());return h.hexdigest()
    def clone(self):
        x=State(self.book,self.active,self.store.matcher,self.scope)
        for name in ('keys','vals','present'):getattr(x.store,name).copy_(getattr(self.store,name))
        x.kr.copy_(self.kr);x.vr.copy_(self.vr);x.revision=self.revision.copy();x.tick=self.tick;x.store.events=self.store.events
        return x
    def register(self,code,allowed=True,scope='study'):
        b=len(self.book)
        if code.shape!=(b,17) or not torch.isfinite(code).all():raise ValueError('Invalid registration code')
        if (code[:,-1].abs()>1e-5).any() or not torch.allclose(code.norm(dim=-1),torch.ones(b),atol=1e-4):raise ValueError('Registration must supply canonical unit identity')
        ok=torch.as_tensor(allowed,dtype=torch.bool).expand(b)&(scope==self.scope)
        equal=(self.book==code[:,None,:]).all(-1)&self.active
        duplicate=equal.any(-1);free=(~self.active).any(-1);slot=(~self.active).long().argmax(-1)
        added=ok&~duplicate&free;r=torch.arange(b)
        self.book[r[added],slot[added]]=code[added];self.active[r[added],slot[added]]=True
        self.revision[added.numpy()]+=1
        return {'added':added,'duplicate':ok&duplicate,'denied':~ok,'full':ok&~duplicate&~free,'slot':torch.where(added,slot,torch.full_like(slot,-1))}
    @torch.no_grad()
    def event(self,src,val,operation,resolver,qualified=True,scope='study'):
        b=len(self.book);op=torch.as_tensor(operation,dtype=torch.int64).expand(b)
        if not ((op==1)|(op==0)|(op==-1)).all():raise ValueError('Invalid event operation')
        permission=torch.as_tensor(qualified,dtype=torch.bool).expand(b)&(scope==self.scope)
        # Canonical new codes must first be explicitly registered; queries cannot enroll.
        sd=resolver(src[:,None,:],self.book,self.active);vd=resolver(val[:,None,:],self.book,self.active)
        effective=permission&sd.accept[:,0]&((op==-1)|vd.accept[:,0])
        free=(~self.present).long().argmax(-1)
        receipt=self.store.event(sd.value[:,0],vd.value[:,0],op,effective,scope)
        targets=torch.where(receipt['selected']<16,receipt['selected'],free);r=torch.arange(b)
        w=receipt['written'];cl=receipt['cleared']
        self.kr[r[w],targets[w]]=True;self.vr[r[w],targets[w]]=True
        self.kr[r[cl],targets[cl]]=False;self.vr[r[cl],targets[cl]]=False
        receipt['membership_rejected']=permission&(op!=0)&~effective
        return receipt
    def clear_scope(self):
        self.store.clear_all();self.kr.zero_();self.vr.zero_();self.book.zero_();self.active.zero_();self.revision+=1
    def add_noise(self,rng,sigma,fields='both',common=False):
        # Always draw both fields for paired schedule consistency.
        nk=rng.normal(0,sigma,self.store.keys.shape).astype(np.float32)
        nv=rng.normal(0,sigma,self.store.vals.shape).astype(np.float32)
        if common:nv=nk.copy()
        for key,noise in (('keys',nk),('values',nv)):
            if fields in (key,'both'):
                x=self.store.keys if key=='keys' else self.store.vals
                x.add_(torch.from_numpy(noise)*self.present[...,None])
        self.tick+=1
    @torch.no_grad()
    def maintain(self,resolver,fields='both'):
        accepted=[]
        for key in ('keys','values'):
            if fields not in (key,'both'):continue
            x=self.store.keys if key=='keys' else self.store.vals
            readable=self.kr if key=='keys' else self.vr
            d=resolver(x,self.book,self.active)
            eligible=self.present&readable
            x.copy_(torch.where((eligible&d.accept)[...,None],d.value,x))
            # Sticky quarantine, no confidence accumulation by repeatedly projecting.
            readable &= (~self.present)|d.accept
            readable &= self.present
            accepted.append(d)
        return accepted
    def bytes(self):return sum(t.numel()*t.element_size() for t in (self.book,self.active,self.store.keys,self.store.vals,self.present,self.kr,self.vr))+self.revision.nbytes
    def save(self,path,rng,contract,query=None):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        arr={k:getattr(self.store,k).numpy() for k in ('keys','vals','present')}
        arr.update(book=self.book.numpy(),active=self.active.numpy(),kr=self.kr.numpy(),vr=self.vr.numpy(),revision=self.revision)
        if query:
            for k,v in query.items():arr['query_'+k]=v.numpy()
        np.savez_compressed(path,**arr)
        dump(path.with_suffix('.json'),{'abi':ABI,'scope':self.scope,'contract':contract,'binder':weights_hash(self.store.matcher),'tick':self.tick,'events':self.store.events,'sha256':sha(path),'rng':rng.bit_generator.state})
    @classmethod
    def load(cls,path,binder,contract,scope='study'):
        path=Path(path);m=json.loads(path.with_suffix('.json').read_text())
        if m['abi']!=ABI or m['scope']!=scope or m['contract']!=contract or m['binder']!=weights_hash(binder):raise ValueError('Incompatible state contract')
        if sha(path)!=m['sha256']:raise ValueError('Corrupt state snapshot')
        with np.load(path,allow_pickle=False) as a:
            obj=cls(torch.from_numpy(a['book']),torch.from_numpy(a['active']),binder,scope)
            for k in ('keys','vals','present'):
                dst=getattr(obj.store,k);src=torch.from_numpy(a[k])
                if src.shape!=dst.shape or src.dtype!=dst.dtype or not torch.isfinite(src).all():raise ValueError('Invalid record tensor')
                dst.copy_(src)
            for k in ('kr','vr'):
                src=torch.from_numpy(a[k]);dst=getattr(obj,k)
                if src.shape!=dst.shape or src.dtype!=torch.bool:raise ValueError('Invalid readability')
                dst.copy_(src)
            if (obj.kr&~obj.present).any() or (obj.vr&~obj.present).any():raise ValueError('Empty record cannot be readable')
            obj.revision=a['revision'].copy();q={k[6:]:torch.from_numpy(a[k].copy()) for k in a.files if k.startswith('query_')}
        obj.tick=m['tick'];obj.store.events=m['events'];rng=np.random.default_rng();rng.bit_generator.state=m['rng'];return obj,rng,q
