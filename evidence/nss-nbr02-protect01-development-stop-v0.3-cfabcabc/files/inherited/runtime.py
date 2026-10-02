"""REV01 controller. Scientific forward/local derivative follow byte-pinned DC01 source.
No generator, label ledger, seeds, or future event file may be read by the worker.
"""
import os,json,time,copy,sys,struct,zlib
from pathlib import Path
import numpy as np
import torch
from base_runtime import Learner as BaseLearner, Recorder as BaseRecorder, canon,sha,flat,arr,unpack,packframe

class Recorder(BaseRecorder):
    def frame(self,meta,arrays):
        slots={'load':2696,'management_load':0,'cue':10648,'fillers':2112,'update':5400,'frozen_receipt':2696,'query':272,'checkpoint':10248,'fork':10704,'fork_match':2696,'derivative':2696}
        extent=sum(np.asarray(a).nbytes for a in arrays.values())
        if meta['kind'] not in slots or extent>slots[meta['kind']]:raise RuntimeError('NUMERIC_SCHEMA_OVERRUN:'+meta['kind'])
        payload=packframe(meta,arrays,self.array_cache);raw=zlib.decompress(payload);hn=struct.unpack('<I',raw[:4])[0]
        if hn>65536 or len(raw)>131072:raise RuntimeError('FRAME_SCHEMA_OVERRUN')
        off=self.raw.tell();h=sha(payload)
        self.raw.write(struct.pack('<Q',len(payload))+bytes.fromhex(h)+payload);os.fsync(self.raw.fileno());self.rec+=1
        ref={'index':self.rec,'offset':off,'bytes':len(payload)+40,'sha256':h}
        self.emit('EVIDENCE_DURABLE',{'frame':ref,'kind':meta['kind'],'context':meta.get('context')})
        return ref
    def charge(self,kind,n=1):
        self.counts[kind]+=n
        caps={'cell':86424,'head':29008,'backward':1206,'update_attempt':2166}
        if kind in caps and self.counts[kind]>caps[kind]:raise RuntimeError('PER_PASS_CAP:'+kind)

def decide(table,cue,scope,target,used):
    old=table.get(f'{scope}:{cue}')
    return bool(old is not None and old['label']!=target and not used)

def validate(p,consumed,scope,receipt,version,target,pdigest,tdigest):
    if p is None:return 'NO_PENDING'
    if scope!=p['scope']:return 'WRONG_SCOPE'
    if receipt in consumed:return 'CONSUMED_ID'
    if receipt!=p['receipt']:return 'UNKNOWN_ID'
    if version!=p['version'] or pdigest!=p['version']:return 'STALE_VERSION'
    if target not in (0,1):return 'BAD_OUTCOME'
    if tdigest!=p['immutable']:return 'TRACE_MUTATION'
    return None

class Learner(BaseLearner):
    def __init__(self,rec):
        super().__init__(rec);self.table={};self.used=False;self.branch='COMMON';self.candidate=False
    def load(self,weights,arm,context,table=None,candidate=False,branch='COMMON',used=False,consumed=None):
        self.table=copy.deepcopy(table or {});self.used=used;self.branch=branch;self.candidate=candidate
        super().load(weights,arm,{**context,'branch':branch})
        self.consumed=set(consumed or [])
        self.rec.frame({'kind':'management_load','context':self.context,'arm':arm,'table':self.table,'used':used,'candidate':candidate,'consumed':sorted(self.consumed)}, {})
    def start_cue(self,cue,scope,receipt,context,reconstructed=False,original_sequence=None,original_ref=None):
        # Copied scientific sequence from BaseLearner.start_cue. Only event provenance differs.
        if self.pending is not None:raise RuntimeError('SECOND_PENDING')
        expected_scope=0 if cue in (0,1,2,3,8,9,12,13,14,15) else 1
        if not 0<=cue<20 or scope!=expected_scope:raise RuntimeError('BAD_CUE_SCOPE')
        self.context={**context,'branch':self.branch};pre=arr(flat(self.ps));digest=sha(pre.tobytes());codes=[22,20+scope,cue]
        h,z,p,states,E,saved=self.forward(codes,grad=self.arm=='G',elig=self.arm=='L')
        self.live=h.detach().clone();ep=torch.tensor(E[-1]) if self.arm=='L' else None
        self.pending={'scope':scope,'receipt':receipt,'version':digest,'codes':codes,'h':h,'z':z,'p':p,'elig':ep,'V':self.ps[3].detach().clone(),'saved':saved,'pre':pre,'states':states,'trace_steps':E}
        self.pending['immutable']=self.pending_digest()
        ref=self.rec.frame({'kind':'cue','context':self.context,'arm':self.arm,'scope':scope,'cue':cue,'receipt':receipt,'version':digest,'codes':codes,'saved_tensor_inventory':saved,'cost':self.measure(),'table':self.table,'used':self.used,'reconstructed':reconstructed,'original_cue_ref':original_ref},
          {'params':pre,'h':states,'elig_steps':E,'logits':arr(z),'probabilities':arr(p)})
        self.pending['cue_ref']=ref
        seq=self.rec.emit('RECONSTRUCTED_AT_FORK' if reconstructed else 'PREDICTION_BEFORE_FEEDBACK',{'context':self.context,'receipt':receipt,'prediction':int(z.argmax()),'cue_frame':ref,'original_prediction_sequence':original_sequence})
        self.pending['prediction_sequence']=original_sequence if reconstructed else seq
        return {'prediction':int(z.argmax()),'logits':arr(z).tolist(),'version':digest,'pending_digest':self.pending['immutable']}
    def rejection(self,scope,receipt,version,target):
        return validate(self.pending,self.consumed,scope,receipt,version,target,self.pdigest(),self.pending_digest())
    def prepare(self,target,clip,defect=None):
        p=self.pending
        if p is None:raise RuntimeError('PREPARE_NO_PENDING')
        self.rec.emit('FEEDBACK_RELEASED',{'context':self.context,'receipt':p['receipt'],'outcome':target,'prediction_sequence':p['prediction_sequence']})
        learn=self.arm in ('G','L');raw=None;attempt=None
        if learn:
            self.rec.charge('update_attempt');attempt=self.rec.counts['update_attempt']
            self.rec.emit('UPDATE_INTENT',{'attempt':attempt,'context':self.context,'receipt':p['receipt'],'pre_digest':p['version'],'clip':clip,'rule':self.arm,'defect':defect})
            if self.arm=='G':
                self.rec.charge('backward');loss=torch.nn.functional.cross_entropy(p['z'].reshape(1,2),torch.tensor([target]));gr=torch.autograd.grad(loss,self.ps);raw=torch.cat([g.reshape(-1) for g in gr]).detach()
            else:
                with torch.no_grad():
                    q=p['p'].clone();q[target]-=1.;delta=p['V'].T@q;E=p['elig'];ew=E[:368].reshape(16,23);eu=E[368:624].reshape(16,16);eb=E[624:]
                    raw=torch.cat(((delta[:,None]*ew).reshape(-1),(delta[:,None]*eu).reshape(-1),delta*eb,torch.outer(q,p['h']).reshape(-1),q))
            if not torch.isfinite(raw).all():raise RuntimeError('NONFINITE_GRADIENT')
        return {'raw':raw,'attempt':attempt,'target':target,'clip':clip,'defect':defect}
    def apply(self,prepared,changed=False):
        p=self.pending;raw=prepared['raw'];clip=prepared['clip'];target=prepared['target'];defect=prepared['defect'];pretable=copy.deepcopy(self.table)
        norm=factor=None;learn=raw is not None
        if learn:
            norm=torch.linalg.vector_norm(raw);factor=torch.minimum(torch.ones(()),clip/norm) if norm>0 else torch.ones(())
            with torch.no_grad():
                step=raw*factor
                if defect=='sign':step=-step
                elif defect=='double':step=step*2
                k=0
                for t in self.ps:
                    n=t.numel();t.sub_(step[k:k+n].reshape(t.shape));k+=n
            if not torch.isfinite(flat(self.ps)).all():raise RuntimeError('NONFINITE_POSTSTATE')
        self.table[f"{p['scope']}:{p['codes'][-1]}"]={'label':target,'receipt':p['receipt'],'pre_version':p['version'],'post_version':self.pdigest()}
        self.used=self.used or changed;self.live=torch.zeros(16);self.consumed.add(p['receipt'])
        arrays={'post':arr(flat(self.ps))}
        if learn:arrays.update({'raw_gradient':arr(raw),'norm_factor':np.array([float(norm),float(factor)],dtype=np.float32)})
        meta={'kind':'update' if learn else 'frozen_receipt','context':self.context,'arm':self.arm,'target':target,'receipt':p['receipt'],'pre_digest':p['version'],'cue_ref':p['cue_ref'],'prediction_sequence':p['prediction_sequence'],'defect':defect,'intended_injection':defect is not None,'post_digest':self.pdigest(),'ephemeral_reset':True,'clip':clip,'changed':changed,'used':self.used,'table_before':pretable,'table_after':copy.deepcopy(self.table)}
        ref=self.rec.frame(meta,arrays);self.pending=None
        if learn:
            self.rec.counts['update_commit']+=1;self.rec.emit('UPDATE_COMMIT',{'attempt':prepared['attempt'],'context':self.context,'receipt':p['receipt'],'evidence':ref,'post_digest':self.pdigest(),'ephemeral_digest':self.pending_digest()})
        else:self.rec.emit('FROZEN_RECEIPT_COMMIT',{'context':self.context,'receipt':p['receipt'],'evidence':ref})
        return {'updated':learn,'post_digest':self.pdigest(),'counts':dict(self.rec.counts),'branch':self.branch}
    def checkpoint(self,meta):
        before=canon(self.table);ans=super().checkpoint({**meta,'table':self.table,'used':self.used,'branch':self.branch,'consumed':sorted(self.consumed)})
        assert before==canon(self.table)
        return {**ans,'table':copy.deepcopy(self.table),'used':self.used,'consumed':sorted(self.consumed)}
    def query(self,cue,scope,meta):
        before=canon((self.table,self.used,sorted(self.consumed)));ans=super().query(cue,scope,meta)
        if before!=canon((self.table,self.used,sorted(self.consumed))):raise RuntimeError('QUERY_MUTATES_MANAGEMENT')
        return ans

class Engine:
    def __init__(self,rec):self.rec=rec;self.models={};self.active=None
    @property
    def model(self):return self.models[self.active]
    def load(self,**kwargs):
        if any(m.pending is not None for m in self.models.values()):raise RuntimeError('LOAD_WITH_PENDING')
        m=Learner(self.rec);m.load(**kwargs);self.models={m.branch:m};self.active=m.branch
        return {'loaded':True}
    def select(self,branch):
        if self.model.pending is not None:raise RuntimeError('SWITCH_WITH_PENDING')
        if branch not in self.models:raise RuntimeError('MISSING_BRANCH')
        self.active=branch;self.rec.emit('BRANCH_SELECTED',{'context':self.model.context,'branch':branch})
        return {'branch':branch}
    def receipt(self,scope,receipt,version,target,defect=None):
        m=self.model;reason=m.rejection(scope,receipt,version,target)
        if reason:
            before=m.pending_digest();self.rec.emit('RECEIPT_REJECT',{'context':m.context,'reason':reason,'receipt':receipt,'pending_before':before,'pending_after':m.pending_digest(),'table_digest':sha(canon(m.table))})
            return {'rejected':reason,'pending_unchanged':True}
        p=m.pending;changed=decide(m.table,p['codes'][-1],scope,target,m.used)
        if changed and m.candidate and m.arm in ('G','L'):
            if m.branch!='COMMON':raise RuntimeError('SECOND_BRANCH_CREATION')
            common_context=dict(m.context);common_ref=p['cue_ref'];common_seq=p['prediction_sequence']
            self.rec.emit('VALIDATED_CHANGED_RECEIPT',{'context':common_context,'receipt':receipt,'outcome':target,'previous_public_label':m.table[f'{scope}:{p["codes"][-1]}']['label']})
            self.rec.frame({'kind':'fork','context':common_context,'arm':m.arm,'receipt':receipt,'target':target,'table':m.table,'used':m.used,'cue_ref':common_ref,'prediction_sequence':common_seq}, {'params':p['pre'],'pending_h':p['states'],'pending_probabilities':arr(p['p']),'pending_trace':p['trace_steps'],'live_filler':arr(m.live)})
            other=Learner(self.rec);other.load(p['pre'],m.arm,common_context,table=m.table,candidate=True,branch='B2',used=False,consumed=m.consumed)
            other.start_cue(p['codes'][-1],scope,receipt,common_context,reconstructed=True,original_sequence=common_seq,original_ref=common_ref)
            other.live=m.live.detach().clone()
            for key in ('states','trace_steps'):
                if not np.array_equal(p[key],other.pending[key]):raise RuntimeError('FORK_FORWARD_MISMATCH:'+key)
            for key in ('h','z','p','V'):
                if not torch.equal(p[key],other.pending[key]):raise RuntimeError('FORK_TENSOR_MISMATCH:'+key)
            if any(t.untyped_storage().data_ptr()==u.untyped_storage().data_ptr() for t,u in zip(m.ps,other.ps)):raise RuntimeError('FORK_MUTABLE_ALIAS')
            m.branch='B1';m.context={**common_context,'branch':'B1'}
            prep1=m.prepare(target,1.,defect);prep2=other.prepare(target,2.,defect)
            if not torch.equal(prep1['raw'],prep2['raw']):raise RuntimeError('FORK_GRADIENT_MISMATCH')
            self.rec.frame({'kind':'fork_match','context':common_context,'arm':m.arm,'receipt':receipt,'bitwise_forward_gradient':True,'distinct_mutable_storage':True}, {'raw_gradient':arr(prep1['raw'])})
            r1=m.apply(prep1,True);r2=other.apply(prep2,True)
            self.models={'B1':m,'B2':other};self.active='B1'
            return {'forked':True,'branches':[r1,r2]}
        prep=m.prepare(target,1.,defect);return {**m.apply(prep,changed),'forked':False}
