"""SC01: exact graph-closure segments and versioned maintenance workspaces.

This is software-managed context for the unchanged, typed SH02 reader. No
weights are updated, no oracle labels enter selection, and row IDs are global.
"""
from __future__ import annotations
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
import copy, hashlib, json, os, time
from pathlib import Path
from typing import Any, Iterable
import numpy as np
import torch
from torch.nn import functional as F
from nss_hsa.hierarchy import Hierarchy
from nss_hsa.records import compile_features

SCHEMA = 'nss.sc01.workspace.v1'

def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(v: Any) -> str:
    return hashlib.sha256(canonical(v)).hexdigest()

def save(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_bytes(canonical(obj)); os.replace(temp, path)

class SCError(ValueError):
    def __init__(self, code: str, detail: str = ''):
        self.code = code
        super().__init__(f'{code}: {detail}')

@dataclass
class Stage:
    inputs: tuple[int, ...]
    outputs: tuple[int, ...]
    query_indices: torch.Tensor
    buckets: list[dict]
    edges: int

@dataclass
class SlicePlan:
    topology: str
    targets: tuple[int, ...]
    input_ids: tuple[int, ...]
    stages: tuple[Stage, Stage]
    model_positions: int
    @property
    def record_count(self) -> int: return len(self.input_ids)
    @property
    def index_bytes(self) -> int:
        return sum(s.query_indices.numel()*s.query_indices.element_size() +
                   sum(v.numel()*v.element_size() for b in s.buckets for v in b.values() if isinstance(v, torch.Tensor))
                   for s in self.stages)

def closure(spec: Hierarchy, targets: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    ts = tuple(sorted(set(targets)))
    if not ts or any(type(i) is not int or i < 0 or i >= spec.tasks for i in ts):
        raise SCError('INVALID_TARGETS')
    graph = spec.rows()
    out = tuple(4*i for i in ts)
    one = tuple(sorted({k for q in out for k in graph[q]} | set(out)))
    zero = tuple(sorted({k for q in one for k in graph[q]} | set(one)))
    return zero, one, out

def build_stage(graph, inputs, outputs) -> Stage:
    imap = {p:i for i,p in enumerate(inputs)}
    shared = defaultdict(list)
    for j,q in enumerate(outputs): shared[graph[q]].append((j,q))
    sizes = defaultdict(list)
    for keys, qs in shared.items(): sizes[len(qs)].append((keys,qs))
    buckets = []
    for qlen, groups in sorted(sizes.items()):
        width = max(len(keys) for keys,_ in groups)
        inds = np.empty((len(groups),width), np.int64)
        valid = np.zeros_like(inds,dtype=bool)
        qi = np.empty((len(groups),qlen),np.int64)
        oi = np.empty_like(qi)
        for g,(keys,qs) in enumerate(groups):
            if any(k not in imap for k in keys): raise SCError('MISSING_GRAPH_DEPENDENCY')
            inds[g] = imap[qs[0][1]]
            inds[g,:len(keys)] = [imap[k] for k in keys]
            valid[g,:len(keys)] = True
            qi[g] = [imap[q] for _,q in qs]; oi[g] = [j for j,_ in qs]
        buckets.append({'keys':torch.from_numpy(inds),'valid':torch.from_numpy(valid),
                        'queries':torch.from_numpy(qi),'outputs':torch.from_numpy(oi)})
    return Stage(inputs,outputs,torch.tensor([imap[q] for q in outputs]),buckets,sum(len(graph[q]) for q in outputs))

def make_plan(spec: Hierarchy, targets: Iterable[int]) -> SlicePlan:
    targets = tuple(sorted(set(targets))); zero, one, out = closure(spec, targets)
    graph = spec.rows()
    return SlicePlan(spec.identity,targets,zero,(build_stage(graph,zero,one),build_stage(graph,one,out)),spec.positions)

def slice_forward(model, x: torch.Tensor, plan: SlicePlan) -> torch.Tensor:
    """Exact original two-block computation restricted to its backward closure.

    Inputs retain their original compiled features. No positional renumbering,
    edge pruning, output-conditioned routing, approximate summaries, or replay.
    """
    if x.ndim != 2 or x.shape != (len(plan.input_ids),37): raise SCError('SLICE_SHAPE')
    if not torch.isfinite(x).all(): raise SCError('NONFINITE_INPUT')
    z = model.enc(x)
    for block, stage in zip(model.blocks, plan.stages):
        h, d = block.heads, block.d
        q,k,v = block.qkv(block.norm1(z)).reshape(len(z),3,h,d//h).permute(1,2,0,3).unbind(0)
        a = torch.empty((len(stage.outputs),d),dtype=z.dtype,device=z.device)
        for b in stage.buckets:
            qq = q[:,b['queries'],:].permute(1,0,2,3)
            kk = k[:,b['keys'],:].permute(1,0,2,3)
            vv = v[:,b['keys'],:].permute(1,0,2,3)
            yy = F.scaled_dot_product_attention(qq,kk,vv,attn_mask=b['valid'][:,None,None,:],dropout_p=0.0)
            a[b['outputs'].reshape(-1)] = yy.permute(0,2,1,3).reshape(-1,d)
        z = z[stage.query_indices] + block.proj(a)
        z = z + block.ff(block.norm2(z))
    return model.head(model.norm(z))

class Store:
    """RAM-backed simulation of an external exact, versioned archive.

    Full raw and encoded archive memory and ingestion cost are explicitly
    outside the active-row cap, but are included in cost reporting.
    """
    def __init__(self, world: dict, scope: str = 'maintenance'):
        self.scope=scope; self.world=copy.deepcopy(world); self.epoch=0;self.events=[]
        self.ingest_seconds=0.; self.ingest_bytes=0
        self._publish(initial=True)
    def _publish(self, initial=False):
        t=time.perf_counter()
        spec=Hierarchy.from_dependencies(self.world['deps'],scope=self.scope)
        arr=compile_features(self.world,spec).numpy()
        new=[r.tobytes() for r in arr]
        if initial:
            changed=list(range(len(new))); self.versions=[1]*len(new)
        else:
            if len(new)!=len(self.rows): raise SCError('UNSUPPORTED_LAYOUT_RESIZE')
            changed=[i for i,(a,b) in enumerate(zip(self.rows,new)) if a!=b]
            self.versions=[r+int(i in changed) for i,r in enumerate(self.versions)]
        self.spec=spec; self.topology=spec.identity; self.rows=new; self.epoch+=1
        self.events.append({'epoch':self.epoch,'changed':changed,'topology':spec.identity})
        self.ingest_bytes+=sum(map(len,new));self.ingest_seconds+=time.perf_counter()-t
    def mutate(self, change: dict):
        field=change['field']
        if field=='freeze': self.world[field]=1-self.world[field]
        elif field in ('progress','receipts','constraints'):
            i=change['task']; self.world[field][i]=1-self.world[field][i]
        elif field=='dependency':
            i=change['task']; self.world['deps'][i]=list(change['value'])
        else: raise SCError('UNKNOWN_CHANGE',field)
        self._publish()
    def identity(self):
        return {'scope':self.scope,'world_id':self.world['id'],'positions':len(self.rows)}
    def to_dict(self):
        return {'world':self.world,'scope':self.scope,'epoch':self.epoch,'versions':self.versions,
                'events':self.events,'ingest_seconds':self.ingest_seconds,'ingest_bytes':self.ingest_bytes}
    @classmethod
    def from_dict(cls,d):
        obj=cls(d['world'],d['scope']); obj.epoch=d['epoch'];obj.versions=d['versions'];obj.events=d['events']
        obj.ingest_seconds=d['ingest_seconds'];obj.ingest_bytes=d['ingest_bytes']
        if len(obj.versions)!=len(obj.rows):raise SCError('CORRUPT_STORE')
        return obj

class Workspace:
    """Three prospective policies with shared durable progress/receipt semantics.

    INDEX: no transient source/result reuse, caller ordering.
    CACHE: ordinary bounded LRU source and per-task result memoization; complete
      dependency versions are checked on every result lookup, caller ordering.
    SEGMENT: same cache capacities, event-driven invalidation and dependency-
      overlap scheduling; a persisted unfinished-job ledger is NOT exclusive.
    """
    def __init__(self, store: Store, model_id: str, policy: str, record_cap: int,
                 result_cap: int = 32):
        if policy not in ('index','cache','segment'): raise SCError('INVALID_POLICY')
        if record_cap<1 or result_cap<1:raise SCError('INVALID_BUDGET')
        self.store=store; self.model_id=model_id;self.policy=policy
        self.record_cap=record_cap;self.result_cap=result_cap
        self.row_cache=OrderedDict(); self.result_cache=OrderedDict();self.plan_cache=OrderedDict()
        self.jobs={};self.receipts={};self.history=[];self.cursor=store.epoch
        self.topology=store.topology;self.dirty=set();self.trace=[]
        self.graph_topology=store.topology;self.graph=store.spec.rows();self.closure_cache={}
        self.stats=defaultdict(int)
    def _closure(self,t):
        if self.graph_topology!=self.store.topology:
            self.graph_topology=self.store.topology;self.graph=self.store.spec.rows();self.closure_cache.clear();self.plan_cache.clear()
        if t not in self.closure_cache:
            first=set(self.graph[4*t]);self.closure_cache[t]=tuple(sorted({k for q in first for k in self.graph[q]}|first))
        return self.closure_cache[t]
    def _sync(self):
        if self.policy!='segment':return
        newer=[e for e in self.store.events if e['epoch']>self.cursor]
        if self.store.epoch!=self.cursor and (not newer or newer[0]['epoch']!=self.cursor+1 or newer[-1]['epoch']!=self.store.epoch):
            raise SCError('MISSING_REVISION_EVENT')
        for e in newer:
            changes=set(e['changed']);self.stats['invalidation_events']+=1
            for task,entry in self.result_cache.items():
                self.stats['invalidation_entries_checked']+=1
                if e['topology']!=self.topology or changes.intersection(entry['ids']):self.dirty.add(task)
            self.topology=e['topology']
        self.cursor=self.store.epoch
    def signature(self,task,ids=None):
        ids=self._closure(task) if ids is None else ids
        self.stats['revision_fields_checked']+=len(ids)
        return digest([self.store.identity(),self.store.topology,self.model_id,task,[(i,self.store.versions[i]) for i in ids]])
    def _valid_result(self,task):
        if self.policy=='index':return None
        entry=self.result_cache.get(task)
        if entry is None:return None
        if self.policy=='segment':
            valid=(task not in self.dirty and entry['topology']==self.store.topology)
        else:valid=(entry['signature']==self.signature(task,entry['ids']) and entry['topology']==self.store.topology)
        if not valid:
            del self.result_cache[task];self.dirty.discard(task);self.stats['invalidated_results']+=1;return None
        self.result_cache.move_to_end(task);self.stats['result_hits']+=1
        return entry
    def _put_result(self,task,logits,signature,ids):
        if self.policy=='index':return
        self.result_cache[task]={'logits':list(logits),'signature':signature,'ids':list(ids),'topology':self.store.topology}
        self.result_cache.move_to_end(task);self.dirty.discard(task)
        if len(self.result_cache)>self.result_cap:
            t,_=self.result_cache.popitem(last=False);self.dirty.discard(t);self.stats['result_evictions']+=1
        self.stats['peak_result_entries']=max(self.stats['peak_result_entries'],len(self.result_cache))
    def _load(self,ids):
        out=[]
        for i in ids:
            key=(i,self.store.versions[i]);self.stats['source_metadata_checks']+=1
            if self.policy!='index' and key in self.row_cache:
                row=self.row_cache[key];self.row_cache.move_to_end(key);self.stats['row_hits']+=1
            else:
                raw=self.store.rows[i];row=torch.from_numpy(np.frombuffer(raw,dtype=np.float32).copy())
                self.stats['archive_rows_read']+=1;self.stats['archive_bytes_read']+=len(raw)
                if self.policy!='index':
                    self.row_cache[key]=row
                    if len(self.row_cache)>self.record_cap:self.row_cache.popitem(last=False);self.stats['row_evictions']+=1
            out.append(row)
        self.stats['peak_active_rows']=max(self.stats['peak_active_rows'],len(ids))
        self.stats['peak_row_cache_rows']=max(self.stats['peak_row_cache_rows'],len(self.row_cache))
        return torch.stack(out)
    def _plan(self,targets):
        key=(self.store.topology,tuple(sorted(targets)))
        if key in self.plan_cache:
            self.plan_cache.move_to_end(key);self.stats['plan_hits']+=1;return self.plan_cache[key]
        p=make_plan(self.store.spec,targets);self.stats['plans_built']+=1;self.plan_cache[key]=p
        if len(self.plan_cache)>16:self.plan_cache.popitem(last=False)
        self.stats['peak_plan_index_bytes']=max(self.stats['peak_plan_index_bytes'],sum(p.index_bytes for p in self.plan_cache.values()))
        return p
    def _select(self,tasks):
        first=tasks[0]; group=[first]; need=set(self._closure(first))
        if len(need)>self.record_cap:return [],first
        candidates=list(tasks[1:])
        while candidates:
            if self.policy=='segment':
                candidates.sort(key=lambda t:(len(set(self._closure(t))-need),t))
            nxt=candidates.pop(0);new=need|set(self._closure(nxt))
            if len(new)<=self.record_cap:group.append(nxt);need=new
            elif self.policy!='segment':break
        return group,None
    def _commit(self,job,task,sig,logits,origin):
        key=f'{job}:{task}';old=self.receipts.get(key)
        if old and old['signature']==sig:
            self.stats['receipt_reuses']+=1;return
        if old:
            self.history.append(old);self.stats['superseded_receipts']+=1
        rec={'job':job,'task':task,'signature':sig,'label':int(np.argmax(logits)),
             'logits':list(logits),'epoch':self.store.epoch,'origin':origin}
        self.receipts[key]=rec;self.stats['emitted_receipts']+=1
        self.trace.append(dict(rec))
    def job(self,job:str,tasks:list[int],model,*,limit_tasks:int|None=None):
        self._sync()
        if len(set(tasks))!=len(tasks):raise SCError('DUPLICATE_JOB_TASK')
        if job in self.jobs and self.jobs[job]['tasks']!=tasks:raise SCError('JOB_ID_COLLISION')
        self.jobs.setdefault(job,{'tasks':list(tasks),'deferred':[]})
        work=[]
        for t in tasks:
            if type(t)is not int or t<0 or t>=self.store.spec.tasks:raise SCError('INVALID_TARGETS')
            prior=self.receipts.get(f'{job}:{t}')
            if prior and prior['signature']==self.signature(t):
                self.stats['resumed_completed_tasks']+=1;continue
            work.append(t)
        if limit_tasks is not None:work=work[:limit_tasks]
        pending=[]
        for t in work:
            entry=self._valid_result(t)
            if entry:self._commit(job,t,entry['signature'],entry['logits'],'memo')
            else:pending.append(t)
        while pending:
            group,failed=self._select(pending)
            if failed is not None:
                required=len(self._closure(failed));self.stats['budget_deferrals']+=1
                self.trace.append({'job':job,'task':failed,'status':'DEFER_BUDGET','required_rows':required,'cap':self.record_cap,'epoch':self.store.epoch})
                self.jobs[job]['deferred'].append(failed);pending.remove(failed);continue
            p=self._plan(group)
            if p.record_count>self.record_cap:raise SCError('WORKSPACE_OVERFLOW')
            x=self._load(p.input_ids)
            with torch.no_grad():out=slice_forward(model,x,p).detach().numpy()
            self.stats['reader_calls']+=1;self.stats['reader_input_rows']+=len(p.input_ids)
            self.stats['block_query_rows']+=sum(len(s.outputs) for s in p.stages)
            self.stats['logical_attention_edges']+=sum(s.edges for s in p.stages)
            for t,yy in zip(p.targets,out):
                ids=self._closure(t);sig=self.signature(t,ids);ls=[float(v) for v in yy]
                self._put_result(t,ls,sig,ids);self._commit(job,t,sig,ls,'reader')
            pending=[t for t in pending if t not in group]
        return {t:self.receipts.get(f'{job}:{t}') for t in tasks}
    def snapshot(self)->bytes:
        """Durable progress + bounded result memo. Raw row/plan caches rebuild.

        Omitting transient caches is identical across policies and charged as
        restart cache-cold behavior, not a zero-cost warm restoration.
        """
        d={'schema':SCHEMA,'store_identity':self.store.identity(),'model':self.model_id,'policy':self.policy,
           'record_cap':self.record_cap,'result_cap':self.result_cap,'cursor':self.cursor,'topology':self.topology,
           'results':list(self.result_cache.items()),'dirty':sorted(self.dirty),'jobs':self.jobs,'receipts':self.receipts,
           'history':self.history,'stats':dict(self.stats),'trace':self.trace}
        raw=canonical({'payload':d,'sha256':digest(d)})
        self.stats['checkpoint_bytes']+=len(raw);self.stats['checkpoints']+=1
        return raw
    @classmethod
    def restore(cls,raw:bytes,store:Store,model_id:str):
        try:e=json.loads(raw);d=e['payload']
        except Exception as exc:raise SCError('MALFORMED_CHECKPOINT')from exc
        if digest(d)!=e['sha256']:raise SCError('CORRUPT_CHECKPOINT')
        if d['schema']!=SCHEMA:raise SCError('WRONG_SCHEMA')
        if d['model']!=model_id:raise SCError('WRONG_MODEL_REVISION')
        if d['store_identity']!=store.identity():raise SCError('WRONG_STORE_OR_SCOPE')
        if d['cursor']>store.epoch:raise SCError('FUTURE_CHECKPOINT')
        obj=cls(store,model_id,d['policy'],d['record_cap'],d['result_cap'])
        obj.cursor=d['cursor'];obj.topology=d['topology'];obj.jobs=d['jobs'];obj.receipts=d['receipts'];obj.history=d['history'];obj.trace=d['trace']
        obj.result_cache=OrderedDict((int(k),v)for k,v in d['results']);obj.dirty=set(d['dirty']);obj.stats=defaultdict(int,d['stats'])
        if len(obj.result_cache)>obj.result_cap:raise SCError('OVERSIZED_RESULT_CACHE')
        # Verify every persisted result independently of notification assumptions.
        for task,entry in obj.result_cache.items():
            if entry['signature']!=obj.signature(task) or entry['topology']!=store.topology:obj.dirty.add(task)
        obj.stats['checkpoint_bytes']+=len(raw);obj.stats['checkpoints']+=1;obj.stats['restores']+=1
        return obj
    def accounting(self):
        # Serialized payload measures are exact for declared representation, not Python RSS.
        return {'row_cache_payload_bytes':sum(t.numel()*t.element_size()for t in self.row_cache.values()),
                'result_cache_json_bytes':len(canonical(list(self.result_cache.items()))),
                'progress_and_receipts_json_bytes':len(canonical([self.jobs,self.receipts,self.history])),
                'plan_index_bytes':sum(p.index_bytes for p in self.plan_cache.values()),
                'archive_encoded_bytes':sum(map(len,self.store.rows)),
                'archive_raw_json_bytes':len(canonical(self.store.world)),
                'revision_log_json_bytes':len(canonical(self.store.events)),
                'closure_index_json_bytes':len(canonical({str(k):v for k,v in self.closure_cache.items()})),
                'graph_index_json_bytes':len(canonical(self.graph))}
