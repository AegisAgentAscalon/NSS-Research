"""CAP01: exact multi-pass attention with a bounded active-record tile.

No learned segmentation or new task semantics are supplied. The retained reader
is unchanged; partial softmax state is continued over key segments. Source and
intermediate arrays are external, file-backed study artifacts, NOT free memory.
"""
from __future__ import annotations
import base64, copy, hashlib, json, math, os, time
from collections import defaultdict
from pathlib import Path
from typing import Any
import numpy as np
import torch
from retained_common import Reader, compile_world, model_hash
from nss_hsa.hierarchy import Hierarchy

SCHEMA = 'nss.cap01.stream.v1'
ATOL, RTOL = 2e-5, 2e-5

def canonical(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(x: Any) -> str:
    return hashlib.sha256(canonical(x)).hexdigest()

def file_sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def write_json(p: Path, x: Any) -> None:
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp'); tmp.write_bytes(canonical(x)); os.replace(tmp,p)

class CapError(ValueError):
    def __init__(self,code: str,detail: str=''):
        self.code=code;super().__init__(f'{code}: {detail}')

def encode_tensor(x):
    if x is None:return None
    a=x.detach().cpu().numpy().copy();raw=a.tobytes()
    return {'shape':list(a.shape),'dtype':a.dtype.str,'sha256':hashlib.sha256(raw).hexdigest(),
            'bytes_b64':base64.b64encode(raw).decode()}

def decode_tensor(d):
    if d is None:return None
    raw=base64.b64decode(d['bytes_b64'],validate=True)
    if hashlib.sha256(raw).hexdigest()!=d['sha256']:raise CapError('CORRUPT_ACCUMULATOR')
    a=np.frombuffer(raw,dtype=np.dtype(d['dtype'])).copy().reshape(d['shape'])
    return torch.from_numpy(a)

def graph_and_closure(world,targets,mode):
    spec=Hierarchy.from_dependencies(world['deps'])
    if mode=='dense':
        shared=tuple(range(spec.positions));graph=(shared,)*spec.positions
    elif mode=='hsa':graph=spec.rows()
    else:raise CapError('MODE')
    final=tuple(4*t for t in sorted(targets))
    first=tuple(sorted({k for q in final for k in graph[q]}|set(final)))
    initial=tuple(sorted({k for q in first for k in graph[q]}|set(first)))
    return spec,graph,(initial,first,final)

def query_groups(outputs,graph,policy,qwidth=4):
    if policy=='ordinary':
        return [tuple(outputs[i:i+qwidth]) for i in range(0,len(outputs),qwidth)]
    if policy!='segmented':raise CapError('POLICY')
    groups=defaultdict(list)
    for q in outputs:groups[graph[q]].append(q)
    return [tuple(v[i:i+qwidth]) for v in groups.values() for i in range(0,len(v),qwidth)]

def compare(a,b):
    a=np.asarray(a,dtype=np.float64);b=np.asarray(b,dtype=np.float64)
    if a.shape!=b.shape:raise CapError('COMPARISON_SHAPE')
    diff=np.abs(a-b);tol=ATOL+RTOL*np.abs(b)
    finite=bool(np.isfinite(a).all() and np.isfinite(b).all())
    return {'scalars':int(a.size),'violations':int((diff>tol).sum()) if finite else int(a.size),
            'finite':finite,'max_abs':float(diff.max(initial=0)),'max_tolerance_fraction':float((diff/tol).max(initial=0))}

@torch.inference_mode()
def full_reference(model,world,mode,targets):
    """Full same-weight computation. Outside the capped execution and its timer."""
    x,idx,valid=compile_world(world)
    x=torch.from_numpy(x)[None];idx=torch.from_numpy(idx)[None];valid=torch.from_numpy(valid)[None]
    z=model.enc(x);stages=[]
    for b in model.blocks:
        z=b(z,idx,valid,mode);stages.append(z[0].numpy().copy())
    logits=model.head(model.norm(z[:,0:4*len(world['progress']):4]))[0]
    return {'stage1':stages[0],'stage2':stages[1], 'all_logits':logits.numpy().copy(),
            'logits':logits[sorted(targets)].numpy().copy()}

class StreamExecutor:
    """Partial attention state has the same lifecycle as an unfinished computation.

    cap limits simultaneous query/key *record positions*, not all allocated bytes.
    Model arrays, metadata, output spool, accumulators and tensor temporaries are
    separately accounted. No all-context neural tensor is loaded by advance().
    """
    def __init__(self,model,world,targets,mode,policy,cap,root,scope='CAP01'):
        if type(cap)is not int or cap<8:raise CapError('INSUFFICIENT_TILE_BUDGET')
        n=len(world['progress'])
        if not targets or len(set(targets))!=len(targets) or any(type(t)is not int or not 0<=t<n for t in targets):
            raise CapError('INVALID_TARGETS')
        self.model=model;self.world=copy.deepcopy(world);self.targets=sorted(targets)
        self.mode=mode;self.policy=policy;self.cap=cap;self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.spec,self.graph,self.closure=graph_and_closure(world,targets,mode)
        self.groups=[query_groups(self.closure[1],self.graph,policy),query_groups(self.closure[2],self.graph,policy)]
        self.binding={'schema':SCHEMA,'world':digest(world),'model':model_hash(model),'mode':mode,
                      'policy':policy,'cap':cap,'scope':scope,'targets':self.targets,'topology':self.spec.identity}
        self.stats=defaultdict(int);self.stage=0;self.gi=0;self.ki=0
        self.m=self.l=self.acc=None;self.done=False;self.saved_origin=None
        self.input_file=self.root/'input.npy';self.h0_file=self.root/'embedding.npy'
        self.h1_file=self.root/'block1.npy';self.h2_file=self.root/'block2.npy'
        self._prepare()
    @torch.inference_mode()
    def _prepare(self):
        start=time.perf_counter()
        x,_,_=compile_world(self.world)
        if not np.isfinite(x).all():raise CapError('NONFINITE_SOURCE')
        np.save(self.input_file,x);del x
        raw=np.load(self.input_file,mmap_mode='r')
        h0=np.lib.format.open_memmap(self.h0_file,mode='w+',dtype=np.float32,shape=(self.spec.positions,32));h0[:]=np.nan
        ids=self.closure[0]
        for i in range(0,len(ids),self.cap):
            batch=list(ids[i:i+self.cap]);t=torch.from_numpy(np.asarray(raw[batch]).copy())
            z=self.model.enc(t);h0[batch]=z.numpy()
            self.stats['source_rows_encoded']+=len(batch)
            self.stats['peak_selected_positions']=max(self.stats['peak_selected_positions'],len(batch))
            self.stats['encoder_tensor_payload_peak']=max(self.stats['encoder_tensor_payload_peak'],t.numel()*t.element_size()+z.numel()*z.element_size())
        h0.flush();del raw,h0
        for p in [self.h1_file,self.h2_file]:
            mm=np.lib.format.open_memmap(p,mode='w+',dtype=np.float32,shape=(self.spec.positions,32));mm[:]=np.nan;mm.flush();del mm
        self.stats['prepare_ns']=int((time.perf_counter()-start)*1e9)
        self.stats['external_array_bytes']=sum(p.stat().st_size for p in self.files())
        self.stats['graph_index_entries']=sum(len(x) for x in self.graph)
    def files(self):return [self.input_file,self.h0_file,self.h1_file,self.h2_file]
    @property
    def completed(self):return self.done
    def _read(self,arr,ids):
        t=torch.from_numpy(np.asarray(arr[list(ids)]).copy())
        if not torch.isfinite(t).all():raise CapError('MISSING_OR_NONFINITE_INTERMEDIATE',str(list(ids)[:8]))
        self.stats['stage_rows_read']+=len(ids);self.stats['stage_bytes_read']+=t.numel()*t.element_size()
        return t
    @torch.inference_mode()
    def advance(self,limit_tiles=None):
        if self.done:return True
        used=0
        while self.stage<2:
            block=self.model.blocks[self.stage];heads=block.heads;d=block.d;dh=d//heads
            arr=np.load(self.h0_file if self.stage==0 else self.h1_file,mmap_mode='r')
            dest=np.load(self.h1_file if self.stage==0 else self.h2_file,mmap_mode='r+')
            while self.gi<len(self.groups[self.stage]):
                qs=self.groups[self.stage][self.gi];qn=len(qs);keys=tuple(sorted({k for q in qs for k in self.graph[q]}))
                keywidth=self.cap-qn
                allowed=[set(self.graph[qid]) for qid in qs] if self.mode=='hsa' else None
                qbase=self._read(arr,qs)
                qproject=block.qkv(block.norm1(qbase)).reshape(qn,3,heads,dh)
                q=qproject[:,0].permute(1,0,2).contiguous();del qproject
                if self.m is None:
                    self.m=torch.full((heads,qn),float('-inf'));self.l=torch.zeros((heads,qn));self.acc=torch.zeros((heads,qn,dh))
                while self.ki<len(keys):
                    ids=keys[self.ki:self.ki+keywidth];kn=len(ids)
                    if qn+kn>self.cap:raise CapError('ACTIVE_CAP_BREACH')
                    self.stats['peak_selected_positions']=max(self.stats['peak_selected_positions'],qn+kn)
                    keybase=self._read(arr,ids)
                    proj=block.qkv(block.norm1(keybase)).reshape(kn,3,heads,dh)
                    k=proj[:,1].permute(1,0,2);v=proj[:,2].permute(1,0,2)
                    mask=(torch.ones((qn,kn),dtype=torch.bool) if allowed is None else
                          torch.tensor([[key in row for key in ids] for row in allowed],dtype=torch.bool))
                    scores=(q@k.transpose(-2,-1))/math.sqrt(dh)
                    scores=scores.masked_fill(~mask[None],float('-inf'))
                    newer=torch.maximum(self.m,scores.max(-1).values)
                    safe=torch.where(torch.isfinite(newer),newer,torch.zeros_like(newer))
                    scale=torch.exp(self.m-safe)
                    p=torch.exp(scores-safe[:,:,None])
                    self.acc=self.acc*scale[:,:,None]+p@v
                    self.l=self.l*scale+p.sum(-1);self.m=newer
                    self.stats['tiles']+=1;self.stats['attention_score_cells']+=heads*qn*kn
                    self.stats['allowed_attention_edges']+=int(mask.sum())
                    # Named visible tensors only: not total peak allocator memory.
                    tensors=[qbase,q,keybase,proj,mask,scores,newer,safe,scale,p,self.acc,self.l,self.m]
                    payload=sum(t.numel()*t.element_size() for t in tensors)
                    self.stats['named_attention_tensor_payload_peak']=max(self.stats['named_attention_tensor_payload_peak'],payload)
                    self.ki+=kn;used+=1
                    del keybase,proj,k,v,mask,scores,newer,safe,scale,p,tensors
                    if limit_tiles is not None and used>=limit_tiles:
                        dest.flush();return False
                if not torch.isfinite(self.l).all() or (self.l<=0).any():raise CapError('SOFTMAX_DENOMINATOR')
                attention=(self.acc/self.l[:,:,None]).transpose(0,1).reshape(qn,d)
                zz=qbase+block.proj(attention);zz=zz+block.ff(block.norm2(zz))
                if not torch.isfinite(zz).all():raise CapError('NONFINITE_OUTPUT')
                dest[list(qs)]=zz.numpy();self.stats['stage_rows_written']+=qn
                self.gi+=1;self.ki=0;self.m=self.l=self.acc=None
            dest.flush();del arr,dest;self.stage+=1;self.gi=0
        self.done=True;return True
    @torch.inference_mode()
    def logits(self):
        if not self.done:raise CapError('INCOMPLETE_COMPUTATION')
        a=np.load(self.h2_file,mmap_mode='r');out=[]
        # Final heads remain tile bounded too.
        for i in range(0,len(self.targets),4):
            ids=[4*t for t in self.targets[i:i+4]]
            z=self._read(a,ids);out.append(self.model.head(self.model.norm(z)).numpy())
        return np.concatenate(out,axis=0)
    def snapshot(self,path):
        payload={'binding':self.binding,'stage':self.stage,'group':self.gi,'key_offset':self.ki,
                 'm':encode_tensor(self.m),'normalizer':encode_tensor(self.l),'weighted_values':encode_tensor(self.acc),
                 'done':self.done,'stats':dict(self.stats),'files':{p.name:file_sha(p) for p in self.files()}}
        write_json(Path(path),{'payload':payload,'sha256':digest(payload)})
        self.saved_origin=Path(path);return payload
    @classmethod
    def restore(cls,path,model,world,targets,mode,policy,cap,scope='CAP01'):
        path=Path(path)
        try:
            env=json.loads(path.read_text());p=env['payload']
            if digest(p)!=env['sha256']:raise CapError('CORRUPT_SNAPSHOT')
            spec,graph,closure=graph_and_closure(world,targets,mode)
            expected={'schema':SCHEMA,'world':digest(world),'model':model_hash(model),'mode':mode,
                      'policy':policy,'cap':cap,'scope':scope,'targets':sorted(targets),'topology':spec.identity}
            if p['binding']!=expected:raise CapError('STALE_OR_MISBOUND_SNAPSHOT')
            root=path.parent
            for name,sha in p['files'].items():
                if name not in ['input.npy','embedding.npy','block1.npy','block2.npy']:raise CapError('UNEXPECTED_SPOOL')
                if not (root/name).is_file() or file_sha(root/name)!=sha:raise CapError('CORRUPT_SPOOL',name)
            self=cls.__new__(cls);self.model=model;self.world=copy.deepcopy(world);self.targets=sorted(targets)
            self.mode=mode;self.policy=policy;self.cap=cap;self.root=root;self.spec=spec;self.graph=graph;self.closure=closure
            self.binding=expected;self.groups=[query_groups(closure[1],graph,policy),query_groups(closure[2],graph,policy)]
            self.input_file=root/'input.npy';self.h0_file=root/'embedding.npy';self.h1_file=root/'block1.npy';self.h2_file=root/'block2.npy'
            self.stage=p['stage'];self.gi=p['group'];self.ki=p['key_offset'];self.done=p['done'];self.stats=defaultdict(int,p['stats'])
            if not 0<=self.stage<=2:raise CapError('INVALID_CURSOR')
            if self.stage<2 and not 0<=self.gi<len(self.groups[self.stage]):raise CapError('INVALID_CURSOR')
            self.m=decode_tensor(p['m']);self.l=decode_tensor(p['normalizer']);self.acc=decode_tensor(p['weighted_values'])
            if self.stage<2:
                qs=self.groups[self.stage][self.gi];keys=set(k for q in qs for k in graph[q])
                if not 0<=self.ki<=len(keys):raise CapError('INVALID_CURSOR')
                if self.m is not None:
                    if tuple(self.m.shape)!=(2,len(qs)) or tuple(self.l.shape)!=(2,len(qs)) or tuple(self.acc.shape)!=(2,len(qs),16):raise CapError('INVALID_ACCUMULATOR_SHAPE')
            self.saved_origin=path;return self
        except CapError:raise
        except Exception as e:raise CapError('MALFORMED_SNAPSHOT',repr(e)) from e
