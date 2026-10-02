"""Scoped, owner-explicit record store for the Study009 controlled comparison.

An exact handle is accepted ONLY in the explicitly resolved-identity track.
The observation track obtains its handle from the supplied frozen resolver.
No destination handle or clean payload copy is retained. Book = identity codes,
not facts. Unguarded learned trials keep their mistakes in the actual store.
"""
from pathlib import Path
from types import SimpleNamespace
import json,hashlib,os
import numpy as np
import torch
from .common import dump,sha,weights_hash
D=17;N=16;ABI='nbr009-owner-state-v1'

class OwnedState:
    tensor_names=('book','active','keys','vals','present','kr','vr','owner','owner_epoch','row_revision','allocation','epoch','catalogue_revision','state_revision')
    def __init__(self,book,active,binder,scope='study',allocation=None,mode='identity'):
        if tuple(book.shape[1:])!=(N,D) or active.shape!=book.shape[:2] or book.dtype!=torch.float32 or active.dtype!=torch.bool:raise ValueError('Bad registry shape/dtype')
        if not torch.isfinite(book).all() or (book[~active]!=0).any():raise ValueError('Invalid/hidden registry code')
        if active.any() and ((book[active].norm(dim=-1)-1).abs().max()>1e-4 or book[active][:,-1].abs().max()>1e-5):raise ValueError('Invalid canonical code')
        if mode not in ('identity','learned','guarded'):raise ValueError(mode)
        self.mode=mode;self.scope=scope;self.matcher=binder;self.binder_hash=weights_hash(binder)
        self.book=book.clone();self.active=active.clone();b=len(book)
        self.keys=torch.zeros(b,N,D);self.vals=torch.zeros_like(self.keys)
        self.present=torch.zeros(b,N,dtype=torch.bool);self.kr=self.present.clone();self.vr=self.present.clone()
        self.owner=torch.full((b,N),-1,dtype=torch.int64);self.owner_epoch=torch.zeros(b,N,dtype=torch.int64)
        self.row_revision=torch.zeros_like(self.owner);self.epoch=torch.ones(b,dtype=torch.int64)
        self.catalogue_revision=torch.ones(b,dtype=torch.int64);self.state_revision=torch.zeros(b,dtype=torch.int64)
        self.allocation=torch.arange(N).expand(b,N).clone() if allocation is None else allocation.clone()
        if not torch.equal(self.allocation.sort(-1).values,torch.arange(N).expand(b,N)):raise ValueError('Invalid allocation permutation')
        self.tick=0;self._bind_store()
    def _bind_store(self):
        self.store=SimpleNamespace(keys=self.keys,vals=self.vals,present=self.present,matcher=self.matcher,events=0)
    @property
    def revision(self):return self.catalogue_revision.numpy()
    def arrays(self):return {k:getattr(self,k).numpy().copy() for k in self.tensor_names}
    def signature(self):
        h=hashlib.sha256()
        for k in self.tensor_names:h.update(k.encode());h.update(getattr(self,k).numpy().tobytes())
        h.update(f'{ABI}:{self.scope}:{self.mode}:{self.tick}'.encode());return h.hexdigest()
    def validate(self,expected_revision=None,scope=None):
        if scope is not None and scope!=self.scope:raise ValueError('Scope mismatch')
        if expected_revision is not None and not np.array_equal(expected_revision,self.revision):raise ValueError('Stale catalogue revision')
        if (self.book[~self.active]!=0).any() or not torch.isfinite(self.book).all():raise ValueError('Invalid registry')
        if not torch.isfinite(self.keys).all() or not torch.isfinite(self.vals).all():raise ValueError('Nonfinite state')
        if (self.kr&~self.present).any() or (self.vr&~self.present).any():raise ValueError('Readable absent record')
        legal=(self.owner>=0)&(self.owner<N)&(self.owner_epoch==self.epoch[:,None])
        owned_active=self.active.gather(1,self.owner.clamp(0,N-1))
        if (self.present&~(legal&owned_active)).any():raise ValueError('Invalid owner metadata')
    def clone(self):
        x=OwnedState(self.book,self.active,self.matcher,self.scope,self.allocation,self.mode)
        for k in self.tensor_names:getattr(x,k).copy_(getattr(self,k))
        x.tick=self.tick;return x
    def bytes(self):return sum(getattr(self,k).numel()*getattr(self,k).element_size() for k in self.tensor_names)
    def register(self,code,allowed=True,scope='study'):
        b=len(self.book);r=torch.arange(b)
        if code.shape!=(b,D) or not torch.isfinite(code).all() or (code[:,-1].abs()>1e-5).any() or ((code.norm(dim=-1)-1).abs()>1e-4).any():raise ValueError('Invalid registration')
        ok=torch.as_tensor(allowed,dtype=torch.bool).expand(b)&(scope==self.scope)
        eq=(self.book==code[:,None,:]).all(-1)&self.active;duplicate=eq.any(-1)
        free=(~self.active).any(-1);slot=(~self.active).long().argmax(-1);added=ok&~duplicate&free
        self.book[r[added],slot[added]]=code[added];self.active[r[added],slot[added]]=True
        self.catalogue_revision+=added;self.state_revision+=added
        handle=torch.where(added,slot,torch.where(ok&duplicate,eq.long().argmax(-1),torch.full_like(slot,-1)))
        return {'added':added,'duplicate':ok&duplicate,'full':ok&~duplicate&~free,'denied':~ok,'handle':handle,'epoch':self.epoch.clone()}
    @torch.no_grad()
    def prepare(self,src,val,op=1,qualified=True,scope='study',epoch=None):
        """src is a declared handle, from registration OR the resolver's own output.
        Captures a compare-and-commit revision. Does not mutate records or RNG.
        """
        b=len(self.book);r=torch.arange(b);src=torch.as_tensor(src,dtype=torch.long).expand(b).clone()
        op=torch.as_tensor(op,dtype=torch.long).expand(b).clone()
        if val.shape!=(b,D) or not torch.isfinite(val).all():raise ValueError('Invalid value')
        if not ((op==-1)|(op==0)|(op==1)).all():raise ValueError('Invalid op')
        e=self.epoch.clone() if epoch is None else torch.as_tensor(epoch,dtype=torch.long).expand(b).clone()
        ok=torch.as_tensor(qualified,dtype=torch.bool).expand(b)&(scope==self.scope)&(e==self.epoch)&(src>=0)&(src<N)
        ok &= self.active[r,src.clamp(0,N-1)]&(op!=0)
        exact=(self.owner==src[:,None])&self.present&(self.owner_epoch==self.epoch[:,None])
        exists=exact.any(-1);multiple=exact.sum(-1)>1
        q=self.book[r,src.clamp(0,N-1)]
        
        if self.mode=='identity':
            proposed=torch.where(exists,exact.long().argmax(-1),torch.full_like(src,N));logits=torch.zeros(b,N+1)
        else:
            logits=self.matcher(q,self.keys,self.present);proposed=logits.argmax(-1)
        free_mask=(~self.present).gather(1,self.allocation);free=self.allocation[r,free_mask.long().argmax(-1)];has_free=free_mask.any(-1)
        if self.mode=='identity':selected=torch.where(exists,exact.long().argmax(-1),torch.full_like(src,N))
        else:selected=proposed
        target=torch.where(selected<N,selected,free);existing=selected<N
        if self.mode=='guarded':
            target_owner=self.owner[r,target]
            guard=(existing&(target_owner==src))|(~existing&~exists)
        else:guard=torch.ones_like(ok)
        # A duplicate owner is an integrity error for checked commits, not repaired silently.
        if self.mode in ('identity','guarded'):guard &= ~multiple
        write=ok&(op==1)&(existing|has_free)&guard
        clear=ok&(op==-1)&existing&guard
        before_owner=self.owner[r,target]
        wrong=ok&existing&(before_owner!=src)
        return {'src':src,'val':val.clone(),'op':op,'epoch':e,'revision':self.state_revision.clone(),'selected':selected,'proposed':proposed,'target':target,'existing':existing,'write':write,'clear':clear,'qualified':ok,'veto':ok&~guard,'capacity':ok&(op==1)&~existing&~has_free,'wrong_owner_proposal':wrong,'target_owner_before':before_owner.clone(),'logits':logits.detach().clone()}
    def commit(self,tx):
        b=len(self.book);r=torch.arange(b)
        fresh=(tx['revision']==self.state_revision)&(tx['epoch']==self.epoch)
        write=tx['write']&fresh;clear=tx['clear']&fresh;target=tx['target'];src=tx['src']
        new=write&~tx['existing']
        self.keys[r[new],target[new]]=self.book[r[new],src[new]]
        self.owner[r[new],target[new]]=src[new];self.owner_epoch[r[new],target[new]]=self.epoch[new]
        self.vals[r[write],target[write]]=tx['val'][write];self.present[r[write],target[write]]=True
        self.kr[r[write],target[write]]=True;self.vr[r[write],target[write]]=True
        for x in (self.keys,self.vals):x[r[clear],target[clear]]=0
        for x in (self.present,self.kr,self.vr):x[r[clear],target[clear]]=False
        self.owner[r[clear],target[clear]]=-1;self.owner_epoch[r[clear],target[clear]]=0
        changed=write|clear;self.row_revision[r[changed],target[changed]]+=1;self.state_revision+=changed
        return {k:v.clone() for k,v in tx.items() if k not in ('val','logits')}|{'written':write,'cleared':clear,'stale':~fresh,'wrong_owner_commit':(write|clear)&tx['wrong_owner_proposal']}
    def event(self,src,val,op=1,qualified=True,scope='study',epoch=None):return self.commit(self.prepare(src,val,op,qualified,scope,epoch))
    def observed_event(self,src,val,resolver,op=1,qualified=True,scope='study'):
        sd=resolver(src[:,None,:],self.book,self.active);vd=resolver(val[:,None,:],self.book,self.active)
        op=torch.as_tensor(op,dtype=torch.long).expand(len(src))
        ok=torch.as_tensor(qualified,dtype=torch.bool).expand(len(src))&sd.accept[:,0]&((op==-1)|vd.accept[:,0])
        out=self.event(sd.index[:,0],vd.value[:,0],op,ok,scope)
        out.update(resolved_source=sd.index[:,0],source_accepted=sd.accept[:,0],value_accepted=vd.accept[:,0]);return out
    def clear_scope(self):
        for k in ('book','active','keys','vals','present','kr','vr','owner_epoch','row_revision'):getattr(self,k).zero_()
        self.owner.fill_(-1);self.epoch+=1;self.catalogue_revision+=1;self.state_revision+=1
    def add_noise(self,rng,sigma,fields='both',common=False):
        nk=rng.normal(0,sigma,self.keys.shape).astype(np.float32);nv=rng.normal(0,sigma,self.vals.shape).astype(np.float32)
        if common:nv=nk.copy()
        if fields in ('keys','both'):self.keys.add_(torch.from_numpy(nk)*self.present[...,None])
        if fields in ('values','both'):self.vals.add_(torch.from_numpy(nv)*self.present[...,None])
        self.tick+=1
    @torch.no_grad()
    def maintain(self,resolver,policy='shared',fields='both',value_restorer=None):
        self.validate();b=len(self.book);r=torch.arange(b)[:,None]
        if policy not in ('shared','internal','none'):raise ValueError(policy)
        if policy=='none':return
        for field,flag in (('keys','kr'),('values','vr')):
            if fields not in (field,'both'):continue
            x=self.keys if field=='keys' else self.vals;readable=getattr(self,flag)
            if policy=='internal' and field=='keys':
                # EXACT key rehydration from protected owner metadata. No payload backup.
                clean=self.book[r,self.owner.clamp(0,N-1)]
                x.copy_(torch.where(self.present[...,None],clean,x));readable.copy_(self.present)
            else:
                rr=value_restorer if policy=='internal' and value_restorer is not None else resolver
                d=rr(x,self.book,self.active)
                eligible=self.present if policy=='internal' else self.present&readable
                x.copy_(torch.where((eligible&d.accept)[...,None],d.value,x))
                if policy=='internal':readable.copy_(self.present&d.accept)
                else:readable.copy_(self.present&readable&d.accept)
    def save(self,path,rng,contract,query=None,transaction=None):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        if weights_hash(self.matcher)!=self.binder_hash:raise ValueError('Changed binder weights')
        arrays=self.arrays()
        for prefix,obj in (('query_',query),('tx_',transaction)):
            if obj:
                arrays.update({prefix+k:v.numpy() for k,v in obj.items()})
        temp=path.with_suffix('.tmp.npz');np.savez_compressed(temp,**arrays);os.replace(temp,path)
        dump(path.with_suffix('.json'),{'abi':ABI,'scope':self.scope,'mode':self.mode,'contract':contract,'tick':self.tick,'binder_hash':self.binder_hash,'array_sha256':sha(path),'rng':rng.bit_generator.state})
    @classmethod
    def load(cls,path,binder,contract,scope='study'):
        path=Path(path);meta=json.loads(path.with_suffix('.json').read_text())
        if meta['abi']!=ABI or meta['scope']!=scope or meta['contract']!=contract or meta['binder_hash']!=weights_hash(binder):raise ValueError('Incompatible state')
        if meta['array_sha256']!=sha(path):raise ValueError('Corrupt snapshot')
        with np.load(path,allow_pickle=False) as a:
            obj=cls(torch.from_numpy(a['book']),torch.from_numpy(a['active']),binder,scope,torch.from_numpy(a['allocation']),meta['mode'])
            for k in cls.tensor_names:
                src=torch.from_numpy(a[k]);dst=getattr(obj,k)
                if src.dtype!=dst.dtype or src.shape!=dst.shape or not torch.isfinite(src).all():raise ValueError('Invalid snapshot field')
                dst.copy_(src)
            extras={pre:{k[len(pre):]:torch.from_numpy(a[k].copy()) for k in a.files if k.startswith(pre)} for pre in ('query_','tx_')}
        obj.tick=meta['tick'];obj.validate();rng=np.random.default_rng();rng.bit_generator.state=meta['rng']
        return obj,rng,extras['query_'],extras['tx_']
