"""Incremental SC01 execution. Same evidence, graph, layers, and immutable weights.

Explicit records remain authoritative. Intermediate neural rows are disposable,
model-bound memoized functions of their complete first-layer neighborhood.
"""
from __future__ import annotations
import copy, hashlib, json, time
from collections import OrderedDict, defaultdict
import numpy as np
import torch
from torch.nn import functional as F
from sc01 import (Store, Workspace, SCError, canonical, digest, SlicePlan,
                   build_stage, slice_forward, SCHEMA)
from nss_hsa.hierarchy import Hierarchy,HierarchyError

class IncrementalStore(Store):
    """Changes supported by SC01 modify exactly one row unless topology changes."""
    def _publish(self,initial=False):
        # Exact vectorized SH01 feature materialization; same validation contract.
        t0=time.perf_counter();spec=Hierarchy.from_dependencies(self.world['deps'],scope=self.scope)
        w=self.world;n=spec.tasks;codes=np.asarray(w['codes'],dtype=np.float32)
        if codes.shape!=(n,8):raise HierarchyError('INVALID_ADDRESS_SHAPE')
        if any(len(d)!=2 for d in spec.dependencies):raise HierarchyError('SH01_ADAPTER_REQUIRES_TWO_DEPENDENCIES')
        for key in ('progress','receipts','constraints'):
            if len(w[key])!=n or any(v not in [0,1]for v in w[key]):raise HierarchyError('INVALID_BINARY_FIELD',key)
        nuisance=np.asarray(w['nuisance'],np.float32)
        if nuisance.shape!=(n,4)or w['freeze']not in [0,1]:raise HierarchyError('INVALID_EVIDENCE_SHAPE')
        arr=np.zeros((spec.positions,37),np.float32);task=arr[:4*n].reshape(n,4,37)
        task[:,:,0:4]=np.eye(4,dtype=np.float32);task[:,:,6:14]=codes[:,None,:]
        task[:,:,33:37]=nuisance[:,None,:];deps=np.asarray(w['deps'],dtype=np.int64)
        task[:,0,14:22]=codes[deps[:,0]];task[:,0,22:30]=codes[deps[:,1]]
        for role,key in enumerate(('progress','receipts','constraints'),1):task[:,role,29+role]=2*np.asarray(w[key],np.float32)-1
        for r in range(spec.regions):
            pos=4*n+r;arr[pos,4]=1;arr[pos,6:14]=codes[r*spec.region_width:min(n,(r+1)*spec.region_width)].mean(0)
        arr[-1,5]=1;arr[-1,32]=2*w['freeze']-1
        if not np.isfinite(arr).all():raise HierarchyError('NONFINITE_FEATURE')
        new=[r.tobytes()for r in arr]
        if initial:changed=list(range(len(new)));versions=[1]*len(new)
        else:
            if len(new)!=len(self.rows):raise SCError('UNSUPPORTED_LAYOUT_RESIZE')
            changed=[i for i,(a,b)in enumerate(zip(self.rows,new))if a!=b];changed_set=set(changed)
            versions=[v+int(i in changed_set)for i,v in enumerate(self.versions)]
        self.spec=spec;self.topology=spec.identity;self.rows=new;self.versions=versions;self.epoch+=1
        self.events.append({'epoch':self.epoch,'changed':changed,'topology':self.topology})
        self.ingest_bytes+=sum(map(len,new));self.ingest_seconds+=time.perf_counter()-t0
    def mutate(self, change: dict):
        field=change.get('field'); t0=time.perf_counter()
        if field=='dependency':
            # Validate on a detached copy before replacing the published world.
            old=self.world
            new=copy.deepcopy(old)
            i=change['task']
            if type(i)is not int or not 0<=i<self.spec.tasks:raise SCError('INVALID_TARGETS')
            new['deps'][i]=list(change['value']);self.world=new
            try:self._publish()
            except Exception:self.world=old;raise
            return
        if field=='freeze':i=self.spec.global_index;column=32;oldvalue=self.world[field]
        elif field in ('progress','receipts','constraints'):
            task=change['task']
            if type(task)is not int or not 0<=task<self.spec.tasks:raise SCError('INVALID_TARGETS')
            role={'progress':1,'receipts':2,'constraints':3}[field]
            i=4*task+role;column=29+role;oldvalue=self.world[field][task]
        else:raise SCError('UNKNOWN_CHANGE',str(field))
        if oldvalue not in (0,1):raise SCError('INVALID_BINARY_FIELD')
        a=np.frombuffer(self.rows[i],dtype=np.float32).copy()
        a[column]=2*(1-oldvalue)-1
        if not np.isfinite(a).all():raise SCError('NONFINITE_INPUT')
        if field=='freeze':self.world[field]=1-oldvalue
        else:self.world[field][task]=1-oldvalue
        self.rows[i]=a.tobytes();self.versions[i]+=1;self.epoch+=1
        self.events.append({'epoch':self.epoch,'changed':[i],'topology':self.topology})
        self.ingest_bytes+=len(self.rows[i]);self.ingest_seconds+=time.perf_counter()-t0


def stage_forward(block,z,stage):
    """The same SH02 residual/normalization/arithmetic at selected output rows."""
    h,d=block.heads,block.d
    q,k,v=block.qkv(block.norm1(z)).reshape(len(z),3,h,d//h).permute(1,2,0,3).unbind(0)
    a=torch.empty((len(stage.outputs),d),dtype=z.dtype,device=z.device)
    for b in stage.buckets:
        qq=q[:,b['queries'],:].permute(1,0,2,3)
        kk=k[:,b['keys'],:].permute(1,0,2,3)
        vv=v[:,b['keys'],:].permute(1,0,2,3)
        yy=F.scaled_dot_product_attention(qq,kk,vv,attn_mask=b['valid'][:,None,None,:],dropout_p=0.0)
        a[b['outputs'].reshape(-1)]=yy.permute(0,2,1,3).reshape(-1,d)
    z=z[stage.query_indices]+block.proj(a)
    return z+block.ff(block.norm2(z))


class IncrementalWorkspace(Workspace):
    def __init__(self,store,model_id,policy,record_cap,result_cap=32,*,scheduled=False,intermediates=False):
        super().__init__(store,model_id,policy,record_cap,result_cap)
        self.scheduled=scheduled;self.intermediates=intermediates
        self.signature_cache=OrderedDict();self.partial_plan_cache=OrderedDict()
        self.layer_cache=OrderedDict();self.layer_capacity=record_cap
        self._bound_model=None;self._parameter_stamp=None
        self.group_sequence=[];self._group_key=None
    def _closure(self,t):
        if self.graph_topology!=self.store.topology:
            self.signature_cache.clear();self.partial_plan_cache.clear();self.layer_cache.clear()
            self.group_sequence=[];self._group_key=None
        return super()._closure(t)
    def signature(self,task,ids=None):
        ids=self._closure(task)if ids is None else ids
        versions=tuple(self.store.versions[i]for i in ids)
        self.stats['revision_fields_checked']+=len(ids)
        key=(self.store.topology,task,tuple(ids),versions)
        cached=self.signature_cache.get(task)
        if cached and cached[0]==key:
            self.signature_cache.move_to_end(task);self.stats['signature_hits']+=1;return cached[1]
        sig=digest([self.store.identity(),self.store.topology,self.model_id,task,list(zip(ids,versions))])
        self.signature_cache[task]=(key,sig);self.signature_cache.move_to_end(task)
        if len(self.signature_cache)>self.result_cap:self.signature_cache.popitem(last=False)
        return sig
    def _plan(self,targets):
        ts=tuple(sorted(targets));key=(self.store.topology,ts)
        if key in self.plan_cache:
            self.plan_cache.move_to_end(key);self.stats['plan_hits']+=1;return self.plan_cache[key]
        zero=tuple(sorted({i for t in ts for i in self._closure(t)}))
        out=tuple(4*t for t in ts);one=tuple(sorted({i for q in out for i in self.graph[q]}|set(out)))
        p=SlicePlan(self.store.topology,ts,zero,(build_stage(self.graph,zero,one),build_stage(self.graph,one,out)),self.store.spec.positions)
        self.plan_cache[key]=p;self.stats['plans_built']+=1
        if len(self.plan_cache)>16:self.plan_cache.popitem(last=False)
        self.stats['peak_plan_index_bytes']=max(self.stats['peak_plan_index_bytes'],sum(p.index_bytes for p in self.plan_cache.values()))
        return p
    def _packing(self,tasks,greedy):
        remain=list(tasks);groups=[]
        while remain:
            first=remain[0];need=set(self._closure(first))
            if len(need)>self.record_cap:groups.append([first]);remain.pop(0);continue
            group=[first];cands=list(remain[1:])
            while cands:
                if greedy:cands.sort(key=lambda t:(len(set(self._closure(t))-need),t))
                t=cands.pop(0);new=need|set(self._closure(t))
                if len(new)<=self.record_cap:need=new;group.append(t)
                elif not greedy:break
            groups.append(group);gs=set(group);remain=[t for t in remain if t not in gs]
        return groups
    def _packing_score(self,groups):
        rows=sum(len({i for t in g for i in self._closure(t)})for g in groups)
        first=sum(len({i for t in g for i in self.graph[4*t]})for g in groups)
        return (len(groups),rows,first)
    def _select(self,tasks):
        if not self.scheduled:return super()._select(tasks)
        if len(self._closure(tasks[0]))>self.record_cap:return [],tasks[0]
        expected=[t for g in self.group_sequence for t in g]
        if set(tasks)!=set(expected)or self._group_key!=self.store.topology:
            ordinary=self._packing(tasks,False);greedy=self._packing(tasks,True)
            score0=self._packing_score(ordinary);score1=self._packing_score(greedy)
            use_greedy=score1<score0
            self.group_sequence=greedy if use_greedy else ordinary
            self._group_key=self.store.topology
            self.stats['schedule_decisions']+=1;self.stats['greedy_selected']+=int(use_greedy)
        g=self.group_sequence.pop(0)
        return g,None
    def _bind(self,model):
        if self._bound_model is None:
            h=hashlib.sha256()
            for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().cpu().numpy().tobytes())
            if h.hexdigest()!=self.model_id:raise SCError('WRONG_MODEL_REVISION')
            self._bound_model=model
            self._guard=tuple((module,k,v,v._version,v.dtype,v.device)for module in model.modules()for k,v in module._parameters.items()if v is not None)
        elif self._bound_model is not model or any(module._parameters.get(k)is not v or v._version!=ver or v.dtype!=dtype or v.device!=dev for module,k,v,ver,dtype,dev in self._guard):
            raise SCError('MODEL_MUTATED')
    def _run_reader(self,model,x,p):
        if not self.intermediates:return slice_forward(model,x,p)
        if x.shape!=(len(p.input_ids),37)or not torch.isfinite(x).all():raise SCError('INVALID_OR_NONFINITE_SLICE')
        one=p.stages[0].outputs;valid={};missing=[];vkeys={}
        for q in one:
            vers=tuple(self.store.versions[i]for i in self.graph[q]);key=(self.store.topology,vers)
            self.stats['intermediate_version_fields_checked']+=len(vers);vkeys[q]=key
            e=self.layer_cache.get(q)
            if e and e[0]==key:
                valid[q]=e[1];self.layer_cache.move_to_end(q);self.stats['intermediate_hits']+=1
            else:
                if e:del self.layer_cache[q];self.stats['intermediate_invalidations']+=1
                missing.append(q)
        if missing:
            inputs=tuple(sorted({i for q in missing for i in self.graph[q]}|set(missing)))
            key=(self.store.topology,tuple(missing))
            stage=self.partial_plan_cache.get(key)
            if stage is None:
                stage=build_stage(self.graph,inputs,tuple(missing));self.partial_plan_cache[key]=stage
                if len(self.partial_plan_cache)>16:self.partial_plan_cache.popitem(last=False)
                self.stats['partial_plans_built']+=1
            else:self.partial_plan_cache.move_to_end(key)
            imap={q:j for j,q in enumerate(p.input_ids)}
            sx=x[[imap[q]for q in inputs]]
            zz=stage_forward(model.blocks[0],model.enc(sx),stage)
            self.stats['encoded_rows']+=len(inputs);self.stats['first_block_computed_rows']+=len(missing)
            for q,y in zip(missing,zz):
                # clone essential: a view could retain the entire parent tensor.
                y=y.detach().clone();valid[q]=y;self.layer_cache[q]=(vkeys[q],y)
                self.layer_cache.move_to_end(q)
                if len(self.layer_cache)>self.layer_capacity:self.layer_cache.popitem(last=False);self.stats['intermediate_evictions']+=1
            self.stats['peak_intermediate_rows']=max(self.stats['peak_intermediate_rows'],len(self.layer_cache))
        z=torch.stack([valid[q]for q in one])
        z=stage_forward(model.blocks[1],z,p.stages[1])
        return model.head(model.norm(z))
    def snapshot(self):
        # One canonical serialization/digest, not serialize->parse->serialize.
        d={'schema':SCHEMA,'store_identity':self.store.identity(),'model':self.model_id,'policy':self.policy,
           'record_cap':self.record_cap,'result_cap':self.result_cap,'cursor':self.cursor,'topology':self.topology,
           'results':list(self.result_cache.items()),'dirty':sorted(self.dirty),'jobs':self.jobs,'receipts':self.receipts,
           'history':self.history,'stats':dict(self.stats),'trace':self.trace,
           'sc02':{'scheduled':self.scheduled,'intermediates':self.intermediates}}
        raw=canonical({'payload':d,'sha256':digest(d)})
        self.stats['checkpoint_bytes']+=len(raw);self.stats['checkpoints']+=1
        return raw
    @classmethod
    def restore(cls,raw,store,model_id):
        # Reuse the original independent schema, identity and signature validation.
        obj=super().restore(raw,store,model_id)
        flags=json.loads(raw)['payload'].get('sc02',{})
        obj.scheduled=bool(flags.get('scheduled',False));obj.intermediates=bool(flags.get('intermediates',False))
        return obj
    def accounting(self):
        d=super().accounting()
        d['intermediate_tensor_bytes']=sum(y.numel()*y.element_size()for _,y in self.layer_cache.values())
        d['intermediate_version_json_bytes']=len(canonical({str(q):key for q,(key,_)in self.layer_cache.items()}))
        d['signature_cache_json_bytes']=len(canonical(list(self.signature_cache.items())))
        d['partial_plan_index_bytes']=sum(s.query_indices.numel()*8+sum(v.numel()*v.element_size()for b in s.buckets for v in b.values()if isinstance(v,torch.Tensor))for s in self.partial_plan_cache.values())
        return d

    def job(self,job:str,tasks:list[int],model,*,limit_tasks:int|None=None):
        self._bind(model)
        self._sync()
        if len(set(tasks))!=len(tasks):raise SCError('DUPLICATE_JOB_TASK')
        if job in self.jobs and self.jobs[job]['tasks']!=tasks:raise SCError('JOB_ID_COLLISION')
        self.jobs.setdefault(job,{'tasks':list(tasks),'deferred':[]})
        work=[];confirmed=set()
        for t in tasks:
            if type(t)is not int or t<0 or t>=self.store.spec.tasks:raise SCError('INVALID_TARGETS')
            prior=self.receipts.get(f'{job}:{t}')
            if prior and prior['signature']==self.signature(t):
                self.stats['resumed_completed_tasks']+=1;confirmed.add(t);continue
            work.append(t)
        if limit_tasks is not None:work=work[:limit_tasks]
        pending=[]
        for t in work:
            entry=self._valid_result(t)
            if entry:self._commit(job,t,entry['signature'],entry['logits'],'memo');confirmed.add(t)
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
            with torch.no_grad():out=self._run_reader(model,x,p).detach().numpy()
            self.stats['reader_calls']+=1;self.stats['reader_input_rows']+=len(p.input_ids)
            self.stats['block_query_rows']+=sum(len(s.outputs) for s in p.stages)
            self.stats['logical_attention_edges']+=sum(s.edges for s in p.stages)
            for t,yy in zip(p.targets,out):
                ids=self._closure(t);sig=self.signature(t,ids);ls=[float(v) for v in yy]
                self._put_result(t,ls,sig,ids);self._commit(job,t,sig,ls,'reader');confirmed.add(t)
            pending=[t for t in pending if t not in group]
        return {t:self.receipts.get(f'{job}:{t}') if t in confirmed else None for t in tasks}
