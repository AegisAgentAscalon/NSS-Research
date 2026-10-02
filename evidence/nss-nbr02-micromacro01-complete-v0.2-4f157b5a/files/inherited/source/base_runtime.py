"""DC01 deterministic runtime and durable record codec. No task labels or generators."""
import os,sys,json,hashlib,struct,zlib,time,math
from pathlib import Path
import numpy as np
import torch

NAMES=('W','U','b','V','a'); SHAPES=((16,23),(16,16),(16,),(2,16),(2,))
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def flat(ps):return torch.cat([p.detach().reshape(-1) for p in ps])
def arr(t):return t.detach().cpu().numpy().copy()
def unpack(v,grad=False):
    out=[];k=0
    for sh in SHAPES:
        n=math.prod(sh);t=torch.tensor(np.asarray(v[k:k+n]).reshape(sh),dtype=torch.float32,requires_grad=grad);out.append(t);k+=n
    assert k==674
    return out

def packframe(meta,arrays,cache):
    data=[];desc={};pos=0
    for key in sorted(arrays):
        a=np.ascontiguousarray(arrays[key]);b=a.tobytes();h=sha(b);identity=sha(canon({'dtype':a.dtype.str,'shape':list(a.shape),'sha256':h}))
        d={'dtype':a.dtype.str,'shape':list(a.shape),'bytes':len(b),'sha256':h,'identity':identity}
        if identity in cache:
            if cache[identity]!=b:raise RuntimeError('CONTENT_HASH_COLLISION')
            d['alias']=identity
        else:
            cache[identity]=b;d['offset']=pos;data.append(b);pos+=len(b)
        desc[key]=d
    h=canon({'metadata':meta,'arrays':desc});raw=struct.pack('<I',len(h))+h+b''.join(data)
    return zlib.compress(raw,6)

class Recorder:
    def __init__(self,out):
        self.out=Path(out);self.out.mkdir(parents=True,exist_ok=True)
        self.raw=open(self.out/'records.bin','ab',buffering=0);self.log=open(self.out/'events.jsonl','ab',buffering=0)
        self.seq=0;self.rec=0;self.attempt=0;self.prev='0'*64;self.array_cache={}
        self.counts={'cell':0,'head':0,'backward':0,'update_attempt':0,'update_commit':0}
        self.emit('WORKER_START',{})
    def emit(self,event,details):
        self.seq+=1;o={'sequence':self.seq,'event':event,'previous':self.prev,**details};b=canon(o);self.prev=sha(b)
        self.log.write(canon({'record':o,'sha256':self.prev})+b'\n');os.fsync(self.log.fileno())
        (self.out/'heartbeat.json').write_text(json.dumps({'wall_epoch':time.time(),'sequence':self.seq,'last_record':self.rec,'counts':self.counts}))
        return self.seq
    def charge(self,kind,n=1):
        self.counts[kind]+=n
        limits={'cell':199420,'head':29860,'backward':2436,'update_attempt':4780} # Prior v0.4 half-ledger remains charged
        if kind in limits and self.counts[kind]>limits[kind]:raise RuntimeError('PER_PASS_LIMIT:'+kind)
    def frame(self,meta,arrays):
        payload=packframe(meta,arrays,self.array_cache);off=self.raw.tell();h=sha(payload)
        self.raw.write(struct.pack('<Q',len(payload))+bytes.fromhex(h)+payload);os.fsync(self.raw.fileno());self.rec+=1
        ref={'index':self.rec,'offset':off,'bytes':len(payload)+40,'sha256':h}
        self.emit('EVIDENCE_DURABLE',{'frame':ref,'kind':meta['kind'],'context':meta.get('context')})
        return ref
    def close(self):
        self.emit('WORKER_FINISH',{'counts':self.counts});self.raw.close();self.log.close()

class Learner:
    def __init__(self,rec):self.rec=rec;self.ps=None;self.pending=None;self.live=torch.zeros(16);self.consumed=set();self.context={};self.arm='G'
    def load(self,weights,arm,context):
        if self.pending is not None:raise RuntimeError('LOAD_WHILE_PENDING')
        self.ps=unpack(weights,arm=='G');self.arm=arm;self.live=torch.zeros(16);self.context=dict(context);self.consumed=set()
        self.rec.frame({'kind':'load','context':self.context,'arm':arm},{'params':arr(flat(self.ps))})
    def pdigest(self):return sha(arr(flat(self.ps)).tobytes())
    def measure(self):
        seen=set();storages={}
        def visit(o):
            oid=id(o)
            if oid in seen:return 0
            seen.add(oid);n=sys.getsizeof(o)
            if torch.is_tensor(o):
                s=o.untyped_storage();storages[s.data_ptr()]=s.nbytes()
            elif isinstance(o,dict):n+=sum(visit(k)+visit(v) for k,v in o.items())
            elif isinstance(o,(list,tuple,set)):n+=sum(visit(x) for x in o)
            return n
        py=visit((self.ps,self.live,self.pending,self.consumed,self.context));return {'python_object_inventory':py,'unique_tensor_storage_bytes':sum(storages.values()),'tensor_storages':len(storages),'not_native_allocator_measurement':True}
    def forward(self,codes,grad=False,elig=False,initial=None):
        W,U,b,V,a=self.ps;h=torch.zeros(16) if initial is None else initial
        hs=[arr(h)];traces=[];EW=torch.zeros_like(W);EU=torch.zeros_like(U);Eb=torch.zeros_like(b);saved=[]
        def save(t):
            saved.append({'shape':list(t.shape),'dtype':str(t.dtype),'logical_bytes':t.numel()*t.element_size(),'storage_bytes':t.untyped_storage().nbytes(),'storage_id':t.untyped_storage().data_ptr(),'digest':sha(arr(t).tobytes())});return t
        def retrieve(t):return t
        cm=torch.enable_grad() if grad else torch.no_grad()
        with cm:
            with torch.autograd.graph.saved_tensors_hooks(save,retrieve) if grad else __import__('contextlib').nullcontext():
                for code in codes:
                    x=torch.zeros(23);x[int(code)]=1.;old=h
                    self.rec.charge('cell');h=torch.tanh(W@x+U@old+b);hs.append(arr(h))
                    if elig:
                        d=1-h*h;u=torch.diagonal(U)
                        EW=d[:,None]*(x[None,:]+u[:,None]*EW)
                        EU=d[:,None]*(old[None,:]+u[:,None]*EU)
                        Eb=d*(1+u*Eb)
                        traces.append(arr(torch.cat((EW.reshape(-1),EU.reshape(-1),Eb))))
                self.rec.charge('head');z=V@h+a;p=torch.softmax(z,dim=0)
        # Replace pointer addresses with local equality-class numbers; keep raw addresses out of deterministic evidence.
        ids={}
        for item in saved:
            ptr=item.pop('storage_id');item['storage_group']=ids.setdefault(ptr,len(ids))
        return h,z,p,np.array(hs,dtype=np.float32),np.array(traces,dtype=np.float32).reshape(-1,640),saved
    def start_cue(self,cue,scope,receipt,context):
        if self.pending is not None:raise RuntimeError('SECOND_PENDING')
        expected_scope=0 if cue in (0,1,2,3,8,9,12,13,14,15) else 1
        if not 0<=cue<20 or scope!=expected_scope:raise RuntimeError('BAD_CUE_SCOPE')
        self.context=dict(context);pre=arr(flat(self.ps));digest=sha(pre.tobytes());codes=[22,20+scope,cue]
        h,z,p,states,E,saved=self.forward(codes,grad=self.arm=='G',elig=self.arm=='L')
        self.live=h.detach().clone()
        ep=torch.tensor(E[-1]) if self.arm=='L' else None
        # Gradient graph saved before fillers; snapshot tensors are never reused as live filler buffers.
        self.pending={'scope':scope,'receipt':receipt,'version':digest,'codes':codes,'h':h,'z':z,'p':p,'elig':ep,'V':self.ps[3].detach().clone(),'saved':saved,'pre':pre,'states':states,'trace_steps':E}
        self.pending['immutable']=self.pending_digest()
        ref=self.rec.frame({'kind':'cue','context':self.context,'arm':self.arm,'scope':scope,'cue':cue,'receipt':receipt,'version':digest,'codes':codes,'saved_tensor_inventory':saved,'cost':self.measure()},
             {'params':pre,'h':states,'elig_steps':E,'logits':arr(z),'probabilities':arr(p)})
        self.pending['cue_ref']=ref
        seq=self.rec.emit('PREDICTION_BEFORE_FEEDBACK',{'context':self.context,'receipt':receipt,'prediction':int(z.argmax()),'cue_frame':ref})
        self.pending['prediction_sequence']=seq
        return {'prediction':int(z.argmax()),'logits':arr(z).tolist(),'version':digest,'pending_digest':self.pending['immutable']}
    def pending_digest(self):
        if self.pending is None:return sha(b'EMPTY')
        p=self.pending;parts=[canon({k:p[k] for k in ('scope','receipt','version','codes')}),arr(p['h']).tobytes(),arr(p['z']).tobytes(),arr(p['p']).tobytes(),arr(p['V']).tobytes()]
        if p['elig'] is not None:parts.append(arr(p['elig']).tobytes())
        return sha(b''.join(parts))
    def fillers(self,codes):
        if self.pending is None:raise RuntimeError('FILLER_WITHOUT_PENDING')
        W,U,b,V,a=self.ps;states=[arr(self.live)];before=self.pending_digest()
        with torch.no_grad():
            for code in codes:
                if not 0<=code<8:raise RuntimeError('FILLER_LEAK')
                x=torch.zeros(23);x[code]=1.;self.rec.charge('cell');self.live=torch.tanh(W@x+U@self.live+b);states.append(arr(self.live))
                if self.pending_digest()!=before or self.pdigest()!=self.pending['version']:raise RuntimeError('RETENTION_MUTATION')
        self.rec.frame({'kind':'fillers','context':self.context,'arm':self.arm,'codes':codes,'pending_unchanged':self.pending_digest()==before,'parameter_version':self.pdigest()}, {'h':np.array(states,dtype=np.float32)})
        return {'count':len(codes),'pending_unchanged':True}
    def receipt(self,scope,receipt,version,target,defect=None):
        p=self.pending;before=self.pending_digest()
        reason=None
        if p is None:reason='NO_PENDING'
        elif scope!=p['scope']:reason='WRONG_SCOPE'
        elif receipt in self.consumed:reason='CONSUMED_ID'
        elif receipt!=p['receipt']:reason='UNKNOWN_ID'
        elif version!=p['version'] or self.pdigest()!=p['version']:reason='STALE_VERSION'
        elif target not in (0,1):reason='BAD_OUTCOME'
        elif self.pending_digest()!=p['immutable']:reason='TRACE_MUTATION'
        if reason:
            self.rec.emit('RECEIPT_REJECT',{'context':self.context,'reason':reason,'receipt':receipt,'pending_before':before,'pending_after':self.pending_digest()});return {'rejected':reason,'pending_unchanged':before==self.pending_digest()}
        # No hidden target is available until this function receives the outcome.
        self.rec.emit('FEEDBACK_RELEASED',{'context':self.context,'receipt':receipt,'outcome':target,'prediction_sequence':p['prediction_sequence']})
        raw=None;factor=None;norm=None;learn=self.arm in ('G','L')
        if learn:
            self.rec.charge('update_attempt');attempt=self.rec.counts['update_attempt']
            self.rec.emit('UPDATE_INTENT',{'attempt':attempt,'context':self.context,'receipt':receipt,'pre_digest':p['version'],'rule':self.arm,'expected_evidence':'next update frame'})
            if self.arm=='G':
                self.rec.charge('backward');loss=torch.nn.functional.cross_entropy(p['z'].reshape(1,2),torch.tensor([target]));gr=torch.autograd.grad(loss,self.ps);raw=torch.cat([g.reshape(-1) for g in gr]).detach()
            else:
                with torch.no_grad():
                    q=p['p'].clone();q[target]-=1.;delta=p['V'].T@q;E=p['elig'];ew=E[:368].reshape(16,23);eu=E[368:624].reshape(16,16);eb=E[624:]
                    raw=torch.cat(((delta[:,None]*ew).reshape(-1),(delta[:,None]*eu).reshape(-1),delta*eb,torch.outer(q,p['h']).reshape(-1),q))
            if not torch.isfinite(raw).all():raise RuntimeError('NONFINITE_GRADIENT')
            norm=torch.linalg.vector_norm(raw);factor=torch.minimum(torch.ones(()),1/norm) if norm>0 else torch.ones(())
            with torch.no_grad():
                step=raw*factor
                if defect=='sign':step=-step
                elif defect=='double':step=step*2
                k=0
                for t in self.ps:
                    n=t.numel();t.sub_(step[k:k+n].reshape(t.shape));k+=n
            if not torch.isfinite(flat(self.ps)).all():raise RuntimeError('NONFINITE_POSTSTATE')
        self.live=torch.zeros(16);self.consumed.add(receipt)
        arrays={'post':arr(flat(self.ps))}
        if raw is not None:arrays.update({'raw_gradient':arr(raw),'norm_factor':np.array([float(norm),float(factor)],dtype=np.float32)})
        meta={'kind':'update' if learn else 'frozen_receipt','context':self.context,'arm':self.arm,'target':target,'receipt':receipt,'pre_digest':p['version'],'cue_ref':p['cue_ref'],'prediction_sequence':p['prediction_sequence'],'defect':defect,'intended_injection':defect is not None,'post_digest':self.pdigest(),'ephemeral_reset':True}
        ref=self.rec.frame(meta,arrays);self.pending=None
        if learn:
            self.rec.counts['update_commit']+=1;self.rec.emit('UPDATE_COMMIT',{'attempt':attempt,'context':self.context,'receipt':receipt,'evidence':ref,'post_digest':self.pdigest(),'ephemeral_digest':self.pending_digest()})
        else:self.rec.emit('FROZEN_RECEIPT_COMMIT',{'context':self.context,'receipt':receipt,'evidence':ref})
        return {'updated':learn,'post_digest':self.pdigest(),'counts':dict(self.rec.counts)}
    def query(self,cue,scope,meta):
        if self.pending is not None:raise RuntimeError('QUERY_WITH_PENDING')
        before=self.pdigest();live=arr(self.live).tobytes();h,z,p,states,E,saved=self.forward([22,20+scope,cue])
        assert before==self.pdigest() and live==arr(self.live).tobytes()
        self.rec.frame({'kind':'query','context':self.context,'arm':self.arm,'cue':cue,'scope':scope,'codes':[22,20+scope,cue],'parameter_version':before,'query':meta,'readonly':True}, {'h':states,'logits':arr(z),'probabilities':arr(p)})
        return {'prediction':int(z.argmax()),'logits':arr(z).tolist(),'readonly':True}
    def derivative(self,target):
        p=self.pending
        if p is None:raise RuntimeError('NO_PENDING')
        if self.arm=='G':
            self.rec.charge('backward');loss=torch.nn.functional.cross_entropy(p['z'].reshape(1,2),torch.tensor([target]));gr=torch.autograd.grad(loss,self.ps);raw=torch.cat([g.reshape(-1) for g in gr]).detach()
        else:
            with torch.no_grad():
                q=p['p'].clone();q[target]-=1;dl=p['V'].T@q;E=p['elig'];raw=torch.cat(((dl[:,None]*E[:368].reshape(16,23)).reshape(-1),(dl[:,None]*E[368:624].reshape(16,16)).reshape(-1),dl*E[624:],torch.outer(q,p['h']).reshape(-1),q))
        self.rec.frame({'kind':'derivative','context':self.context,'arm':self.arm,'target':target,'cue_ref':p['cue_ref']},{'raw_gradient':arr(raw)})
        self.pending=None;self.live=torch.zeros(16)
        return {'raw_gradient':arr(raw).tolist()}
    def checkpoint(self,meta):
        if self.pending is not None:raise RuntimeError('CHECKPOINT_PENDING')
        import random
        nr=np.random.get_state()
        self.rec.frame({'kind':'checkpoint','context':self.context,'arm':self.arm,'cursor':meta,'python_rng':random.getstate(),'numpy_runtime':{'kind':nr[0],'pos':nr[2],'has_gauss':nr[3],'cached_gaussian':nr[4]},'sgd':{'momentum':0,'slots':{},'learning_rate':1,'clip_norm':1},'parameter_digest':self.pdigest(),'ephemeral_empty':True},
         {'params':arr(flat(self.ps)),'torch_rng':arr(torch.get_rng_state()),'numpy_rng':nr[1]})
        return {'weights':arr(flat(self.ps)).tolist(),'digest':self.pdigest()}
