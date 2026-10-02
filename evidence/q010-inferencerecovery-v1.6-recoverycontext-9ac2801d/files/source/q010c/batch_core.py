"""Same declared Q010 records and reader transitions, batched over independent cases.

Public numerical inputs remain exactly K,V,valid,Q. Owner handles and scenario
truth are only used by storage bookkeeping, exact controls and separate scoring.
The columnar layout replaces millions of duplicated per-call files, not cases.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
import copy, hashlib, json, re
import numpy as np
import torch
from q010r import evaluation as ev
from q010r.conditions import ConditionCell, derive_seed_u64, make_seed_context
from q010r.data import GraphCase
from q010r.models import PublicInput, compose_read, model_state_hash, UNKNOWN_CODE
from q010r.store import OwnedState, IdentityStoreBinder, STORE_ARRAY_NAMES, OwnedRecordStore, array_digest
from q010r.models import resolve_code

UNKNOWN=-1

def arrays_of(state: Any) -> dict[str,np.ndarray]:
    return {n:getattr(state,n).detach().cpu().numpy().copy() for n in STORE_ARRAY_NAMES}

def digest_arrays(arrays: Mapping[str,np.ndarray]) -> str:
    h=hashlib.sha256()
    for k,v in sorted(arrays.items()):
        a=np.ascontiguousarray(v);h.update(k.encode());h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()

def case_index(c: GraphCase) -> int:
    # The opaque case hash is not reversible. Use its retained generation recipe.
    episode = c.rng_record.get('episode_id')
    if not isinstance(episode,str) or re.search(r'-e([0-9]+)$',episode) is None:
        raise ValueError('case lacks a bound episode index')
    return int(re.search(r'-e([0-9]+)$',episode).group(1))

def case_meta(c: GraphCase) -> dict[str,Any]:
    from q010c.catalogue_spec import case_spec
    return dict(c.manifest_record(),case_spec=case_spec(c))

@dataclass
class BatchStore:
    state: Any
    cases: list[GraphCase]
    symbols: np.ndarray
    facts: list[dict[int,int]]

    @classmethod
    @torch.no_grad()
    def initialize(cls,cases:Sequence[GraphCase],*,enabled:bool=True)->'BatchStore':
        cases=list(cases);b=len(cases)
        if not b:raise ValueError('empty case batch')
        book=np.stack([c.book for c in cases]);symbols=np.stack([c.symbols for c in cases])
        orders=np.stack([np.r_[np.flatnonzero(c.present),np.flatnonzero(~c.present)] for c in cases])
        s=OwnedState(torch.zeros((b,16,17),dtype=torch.float32),torch.zeros((b,16),dtype=torch.bool),IdentityStoreBinder(),scope='study',allocation=torch.tensor(orders,dtype=torch.long),mode='identity')
        if enabled:
            for handle in range(16):
                rc=s.register(torch.from_numpy(book[:,handle].copy()))
                if not torch.equal(rc['handle'],torch.full((b,),handle,dtype=torch.long)):raise AssertionError('initial registration order drift')
            for physical in range(16):
                src=torch.tensor([int(c.owner[physical]) if c.present[physical] else 0 for c in cases],dtype=torch.long)
                vals=torch.from_numpy(np.stack([c.values[physical] for c in cases]))
                qual=torch.tensor([bool(c.present[physical]) for c in cases],dtype=torch.bool)
                result=s.event(src,vals,1,qual)
                if not torch.equal(result['written'],qual) or result['wrong_owner_commit'].any():raise AssertionError('initial owner write failed')
        else:
            # The scalar empty-store helper allocates in physical order, not case order.
            s.allocation=torch.arange(16,dtype=torch.long).expand(b,16).clone()
        s.validate()
        return cls(s,cases,symbols,[dict(c.truth_edges) if enabled else {} for c in cases])

    def raw(self)->dict[str,np.ndarray]:return arrays_of(self.state)

    @torch.no_grad()
    def noise_event(self,cell:ConditionCell,paired_seed:int,event:int,split:str)->np.ndarray:
        b=len(self.cases);noise=np.empty((b,2,16,17),np.float32);seeds=np.empty(b,np.uint64)
        sigma=float(cell.factors.get('noise_sigma',.02));fields=str(cell.factors.get('noise_fields','both'))
        for i,c in enumerate(self.cases):
            context=make_seed_context(split=split,purpose='durability_noise_event',paired_seed=paired_seed,condition_id=cell.condition_id,episode_id=f'{c.case_id}-noise-{event:04d}',stage_index=None)
            seed=derive_seed_u64(**context);seeds[i]=seed;rng=np.random.Generator(np.random.PCG64(seed))
            # Match the scalar implementation's successive full-array normal draws.
            noise[i,0]=rng.normal(0.,sigma,size=(1,16,17))[0].astype(np.float32) if fields in ('keys','both') else 0
            noise[i,1]=rng.normal(0.,sigma,size=(1,16,17))[0].astype(np.float32) if fields in ('values','both') else 0
        mask=self.state.present.unsqueeze(-1)
        if fields in ('keys','both'):self.state.keys.add_(torch.from_numpy(noise[:,0])*mask)
        if fields in ('values','both'):self.state.vals.add_(torch.from_numpy(noise[:,1])*mask)
        self.state.tick+=1;self.state.validate()
        return seeds

    @torch.no_grad()
    def maintain(self)->None:
        self.state.maintain(ev._maintenance_resolver,'internal',value_restorer=ev._maintenance_resolver,fields='both');self.state.validate()

    @torch.no_grad()
    def unrelated_write(self)->None:
        src=torch.tensor([int(c.displaced_decoy_id) for c in self.cases],dtype=torch.long)
        dst=torch.tensor([dict(c.truth_edges)[int(c.displaced_decoy_id)] for c in self.cases],dtype=torch.long)
        vals=self.state.book[torch.arange(len(src)),dst]
        result=self.state.event(src,vals,1,True)
        if not result['written'].all() or result['wrong_owner_commit'].any():raise AssertionError('unrelated qualified write failed')

    @torch.no_grad()
    def fault(self,cell:ConditionCell,paired_seed:int,split:str)->dict[str,Any]:
        # Invoke the exact supplied scalar fault/transaction implementation; only
        # its artifact layout differs. These are infrequent non-horizon events.
        f=cell.factors
        if f.get('fault') in (None,'none'):return {}
        raw=[];meta=[];ticks=[]
        for i,c in enumerate(self.cases):
            sc=OwnedRecordStore.from_case(c,run_id='chat13-fault',protocol_id=ev.RUN_PROTOCOL_ID,model_id='shared-actual-store')
            sc.state=state_from_arrays({n:getattr(self.state,n)[i:i+1].detach().cpu().numpy().copy() for n in STORE_ARRAY_NAMES},scope=self.state.scope,mode=self.state.mode,tick=self.state.tick)
            before=len(sc.storage_ops)
            ev._apply_declared_fault(cell,c,sc,paired_seed=paired_seed,episode_index=case_index(c))
            raw.append(sc.actual_arrays());ticks.append(sc.state.tick);meta.append({'source_events':copy.deepcopy(sc.source_events),'storage_ops':copy.deepcopy(sc.storage_ops[before:])})
        merged={n:np.concatenate([r[n] for r in raw],axis=0) for n in STORE_ARRAY_NAMES}
        if len(set(ticks)) != 1:raise AssertionError('heterogeneous physical fault clocks')
        self.state=state_from_arrays(merged,scope=self.state.scope,mode=self.state.mode,tick=ticks[0])
        return {'operations_by_case':meta}


def prepare_cases(cell:ConditionCell,seed:int,split:str='heldout')->list[GraphCase]:
    result=[]
    for i in range(cell.episodes_per_seed):
        c=ev.make_condition_case(cell,paired_seed=seed,episode_index=i,arm='paired_eval',split=split)
        if 'identity_role' in cell.factors:
            c=ev.make_close_identity_case(c,role=str(cell.factors['identity_role']),
                paired_seed=seed,sigma=float(cell.factors.get('close_sigma',.01)))
        result.append(c)
    return result


def prepare_queries(cases:Sequence[GraphCase],cell:ConditionCell,seed:int,split:str,checkpoint:int|None=None)->tuple[np.ndarray,np.ndarray,list[dict]]:
    qs=[];sources=[];recipes=[]
    kind=str(cell.factors.get('query_kind','exact_symbol'))
    for i,c in enumerate(cases):
        ep=f'{c.case_id}-cp{checkpoint:04d}' if checkpoint is not None else f'{cell.condition_id}-s{seed}-e{case_index(c):03d}'
        sigma=float(cell.factors.get('query_sigma',.2)) if kind=='normalized_noise' else float(cell.factors.get('near_sigma',.01)) if kind=='near_novel' else None
        anchor=int(c.query_symbol_id) if kind=='normalized_noise' else int(c.near_center_id if c.near_center_id is not None else c.query_symbol_id) if kind=='near_novel' else None
        q,src,rec=ev.make_query(c,kind=kind,split=split,condition_id=cell.condition_id,episode_id=ep,source_catalogue_sha256=digest_arrays({'book':c.book,'symbols':c.symbols,'active':c.active}),sigma=sigma,anchor_symbol_id=anchor)
        qs.append(q);sources.append(-1 if src=='UNKNOWN' else int(src));recipes.append(rec)
    return np.stack(qs),np.array(sources,np.int64),recipes


def exact_logits(state:Any,symbols:np.ndarray,source_ids:np.ndarray)->torch.Tensor:
    b=len(symbols);logits=torch.full((b,17),-20.,dtype=torch.float32);logits[:,16]=20
    for i,src in enumerate(source_ids):
        ix=np.flatnonzero(symbols[i]==src) if src>=0 else np.empty(0,dtype=int)
        if not len(ix):continue
        handle=int(ix[0])
        if not bool(state.active[i,handle]):continue
        rows=torch.where((state.owner[i]==handle)&state.present[i]&(state.owner_epoch[i]==state.epoch[i]))[0]
        if len(rows)>1:raise ValueError('exact control found duplicate owners')
        if len(rows) and bool(state.kr[i,rows[0]] and state.vr[i,rows[0]]):logits[i,rows[0]]=20;logits[i,16]=-20
    return logits


@torch.no_grad()
def read_batch(state:Any,symbols:np.ndarray,query:np.ndarray,source_ids:np.ndarray,model:Any,*,depth:int,feedback_mode:str,reader_id:str)->dict[str,np.ndarray]:
    if not 1<=depth<=8:raise ValueError('bad depth')
    if feedback_mode=='direct' and depth!=1:raise ValueError('direct must be one stage')
    b=len(query);valid=state.present&state.kr&state.vr
    keys=state.keys.masked_fill(~valid.unsqueeze(-1),0);values=state.vals.masked_fill(~valid.unsqueeze(-1),0)
    q=torch.from_numpy(np.ascontiguousarray(query).copy());src=source_ids.copy();trace={k:[] for k in ('query','logits','weights','weighted_code','read_code','clean_code','resolved_ids','source_ids','selected_rows','state_unchanged')}
    before=digest_arrays(arrays_of(state));weights_before=model_state_hash(model) if model is not None else None
    if model is not None:model.eval()
    for stage in range(depth):
        public=PublicInput.sanitized(keys,values,valid,q)
        if model is None:
            out_logits=exact_logits(state,symbols,src)
            composed=compose_read(out_logits,public.values)
            raw=composed.read_code
        else:
            returned=model.forward_step(public,stage)
            out_logits=returned.selection_logits
            raw=returned.read_code
            composed=compose_read(out_logits,public.values)
            if not torch.equal(raw,composed.read_code):
                raise AssertionError('forward read differs from declared pointer-copy arithmetic')
        indexes,status,clean=resolve_code(raw,state.book,state.active)
        ids=np.full(b,-1,np.int64)
        for i in range(b):
            if int(status[i])>0:ids[i]=int(symbols[i,int(indexes[i])])
        for name,value in [('query',q),('logits',out_logits),('weights',composed.weights),('weighted_code',composed.weighted_code),('read_code',raw),('clean_code',clean)]:trace[name].append(value.detach().cpu().numpy().copy())
        trace['source_ids'].append(src.copy());trace['resolved_ids'].append(ids);trace['selected_rows'].append(out_logits.argmax(-1).cpu().numpy().copy())
        same=digest_arrays(arrays_of(state))==before
        if not same:raise AssertionError('read-only model changed actual store')
        trace['state_unchanged'].append(np.full(b,same,np.bool_))
        q=clean;src=ids.copy()
    if model is not None and model_state_hash(model)!=weights_before:raise AssertionError('evaluation changed learned weights')
    return {k:np.stack(v,axis=1) for k,v in trace.items()}


class LifecycleCollector:
    """Lossless small control-case journal; never invokes a model or supplies labels."""
    def __init__(self):
        self.run_id='chat13-lifecycle';self.protocol_id=ev.RUN_PROTOCOL_ID;self.source_id='chat13-columnar-source';self._source_catalogues={};self.events=[];self.operations=[];self.frames=[]
    def register_source_catalogue(self,case,*,provenance=None):
        if case.case_id not in self._source_catalogues:
            a={'book':case.book.copy(),'symbols':case.symbols.copy(),'active':case.active.copy()};self._source_catalogues[case.case_id]={'sha256':digest_arrays(a),'arrays':a}
        return self._source_catalogues[case.case_id]
    def append_source_event(self,record):self.events.append(copy.deepcopy(record))
    def snapshot_store(self,store,**kwargs):return 'snapshot-'+digest_arrays(store.actual_arrays())
    def record_storage_operation(self,store,row,**kwargs):self.operations.append(copy.deepcopy(row));return {}
    def capture(self,case,store,evidence,readers,**kwargs):
        raw=store.actual_arrays();self.frames.append({'case':case,'raw':raw,'scope':store.scope,'mode':store.state.mode,'tick':store.state.tick,'symbols':np.array([store.handle_to_symbol.get(i,-1) for i in range(16)],np.int64),'facts':dict(store.facts),'events':copy.deepcopy(self.events),'operations':copy.deepcopy(self.operations),'query':np.asarray(kwargs['query'],np.float32).copy(),'source_id':-1 if kwargs['source_symbol_id']=='UNKNOWN' else int(kwargs['source_symbol_id']),'condition_id':kwargs['condition_id'],'episode_id':kwargs['episode_id'],'recipe':copy.deepcopy(kwargs['initial_recipe'])});return []


def collect_lifecycle(seed:int,split:str='lifecycle')->LifecycleCollector:
    from unittest.mock import patch
    col=LifecycleCollector()
    with patch.object(ev,'capture_reader_comparison',side_effect=col.capture):
        ev.capture_lifecycle_trace(evidence=col,readers=[],paired_seed=seed,arm='paired_eval',split=split)
    if len(col.frames)!=12:raise AssertionError('lifecycle coverage changed')
    return col


def state_from_arrays(raw:Mapping[str,np.ndarray],*,scope:str='study',mode:str='identity',tick:int=0):
    book=torch.from_numpy(raw['book'].copy());active=torch.from_numpy(raw['active'].copy())
    s=OwnedState(book,active,IdentityStoreBinder(),scope,torch.from_numpy(raw['allocation'].copy()),mode)
    for n in STORE_ARRAY_NAMES:setattr(s,n,torch.from_numpy(raw[n].copy()))
    s.tick=int(tick);s.validate();return s
