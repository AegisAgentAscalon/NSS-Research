"""PROTECT01 causal controller. Extends locked REV01 forward and local rule.
No access to label ledger, future streams, seeds or scorer. Exact buffer protection
is intentionally hybrid work for L; P/S each compute it independently.
"""
import copy,json,os,struct,zlib,time
from pathlib import Path
import numpy as np
import torch
from base_runtime import Learner as BareLearner, Recorder as BareRecorder,canon,sha,flat,arr,unpack,packframe
from rev_runtime import Learner as PriorLearner,decide,validate
from projection import solve,apply_pair

CAPS={'cell':120000,'head':37500,'backward':4000,'old_backward':2250,'local':2000,'update_attempt':3500,'qp':300,'support':76800,'svd':76800}
SCHEMA={'load':2696,'management_load':0,'cue':10648,'fillers':2112,'update':5392+8+2696,'frozen_receipt':2696,'query':272,'checkpoint':11000,'fork':10704,'fork_match':2696,'derivative':2696,'old_derivative':6000,'protection':196608,'solver_fixture':196608,'solver_failure':196608,'buffer_import':0}

def entry(cue,scope,label,receipt,pre,post,sequence,origin='validated_receipt'):
    codes=[22,20+scope,cue]
    return {'schema':1,'scope':scope,'cue':cue,'codes':codes,'feature_hash':sha(np.eye(23,dtype='f4')[codes].tobytes()),'label':int(label),'receipt':receipt,'pre_version':pre,'post_version':post,'receipt_sequence':int(sequence),'validity':'VALID','origin':origin}

def valid_buffer(table):
    result=[]
    for c in range(8):
        sc=0 if c<4 else 1;r=table.get(f'{sc}:{c}')
        if r is None or r.get('validity')!='VALID' or r.get('scope')!=sc or r.get('cue')!=c or r.get('label') not in (0,1):raise RuntimeError('OLD_PROTECTION_SET_UNAVAILABLE')
        if r['codes']!=[22,20+sc,c] or r['feature_hash']!=sha(np.eye(23,dtype='f4')[r['codes']].tobytes()):raise RuntimeError('OLD_FEATURE_AUTHORITY')
        if not isinstance(r['receipt'],str) or len(r['receipt'])!=16 or r['receipt']=='0'*16 or any(x not in '0123456789abcdef' for x in r['receipt']):raise RuntimeError('OLD_RECEIPT_AUTHORITY')
        result.append(copy.deepcopy(r))
    return result

class Recorder(BareRecorder):
    def __init__(self,out):
        super().__init__(out)
        for k in CAPS:self.counts.setdefault(k,0)
        self.kindstats={}
    def charge(self,kind,n=1):
        self.counts[kind]=self.counts.get(kind,0)+n
        if kind in CAPS and self.counts[kind]>CAPS[kind]:raise RuntimeError('PER_PASS_CAP:'+kind)
    def frame(self,meta,arrays):
        extent=sum(np.asarray(a).nbytes for a in arrays.values());kind=meta['kind']
        if kind not in SCHEMA or extent>SCHEMA[kind]:raise RuntimeError('NUMERIC_SCHEMA_OVERRUN:'+kind+':'+str(extent))
        payload=packframe(meta,arrays,self.array_cache);raw=zlib.decompress(payload);hn=struct.unpack('<I',raw[:4])[0]
        if hn>65536 or len(raw)>524288:raise RuntimeError('FRAME_SCHEMA_OVERRUN:'+kind)
        st=self.kindstats.setdefault(kind,{'count':0,'numeric_logical':0,'encoded':0,'header':0,'max_numeric':0,'max_header':0});st['count']+=1;st['numeric_logical']+=extent;st['encoded']+=len(payload)+40;st['header']+=hn;st['max_numeric']=max(st['max_numeric'],extent);st['max_header']=max(st['max_header'],hn)
        off=self.raw.tell();h=sha(payload);self.raw.write(struct.pack('<Q',len(payload))+bytes.fromhex(h)+payload);os.fsync(self.raw.fileno());self.rec+=1
        ref={'index':self.rec,'offset':off,'bytes':len(payload)+40,'sha256':h}
        self.emit('EVIDENCE_DURABLE',{'frame':ref,'kind':kind,'context':meta.get('context')});return ref
    def close(self):
        (self.out/'SCHEMA_OBSERVED.json').write_text(json.dumps(self.kindstats,indent=2));super().close()

class Learner(PriorLearner):
    def prepare(self,target,clip,defect=None):
        if self.arm=='L':self.rec.charge('local')
        return super().prepare(target,clip,defect)
    def apply(self,prepared,changed=False):
        # Same float32 clip-product-subtraction as REV01 for B1/B2 and ordinary tails.
        p=self.pending;raw=prepared['raw'];clip=prepared['clip'];target=prepared['target'];defect=prepared['defect'];pretable=copy.deepcopy(self.table)
        norm=factor=None;learn=raw is not None
        if learn:
            norm=torch.linalg.vector_norm(raw);factor=torch.minimum(torch.ones(()),clip/norm) if norm>0 else torch.ones(())
            with torch.no_grad():
                step=raw*factor
                if defect=='sign':step=-step
                elif defect=='double':step=step*2
                if 'protected_post' in prepared:
                    vv=prepared['protected_post'];k=0
                    for t in self.ps:n=t.numel();t.copy_(torch.from_numpy(vv[k:k+n].copy()).reshape(t.shape));k+=n
                else:
                    k=0
                    for t in self.ps:n=t.numel();t.sub_(step[k:k+n].reshape(t.shape));k+=n
            if not torch.isfinite(flat(self.ps)).all():raise RuntimeError('NONFINITE_POSTSTATE')
        self.table[f"{p['scope']}:{p['codes'][-1]}"]=entry(p['codes'][-1],p['scope'],target,p['receipt'],p['version'],self.pdigest(),self.rec.seq)
        self.used=self.used or changed;self.live=torch.zeros(16);self.consumed.add(p['receipt'])
        arrays={'post':arr(flat(self.ps))}
        if learn:arrays.update({'raw_gradient':arr(raw),'norm_factor':np.array([float(norm),float(factor)],dtype='f4'),'proposed_clip_product':arr(raw*factor)})
        meta={'kind':'update' if learn else 'frozen_receipt','context':self.context,'arm':self.arm,'target':target,'receipt':p['receipt'],'pre_digest':p['version'],'cue_ref':p['cue_ref'],'prediction_sequence':p['prediction_sequence'],'defect':defect,'intended_injection':defect is not None,'post_digest':self.pdigest(),'ephemeral_reset':True,'clip':clip,'changed':changed,'used':self.used,'table_before':pretable,'table_after':copy.deepcopy(self.table),'protection_ref':prepared.get('protection_ref')}
        ref=self.rec.frame(meta,arrays);self.pending=None
        if learn:
            self.rec.counts['update_commit']+=1;self.rec.emit('UPDATE_COMMIT',{'attempt':prepared['attempt'],'context':self.context,'receipt':p['receipt'],'evidence':ref,'post_digest':self.pdigest(),'ephemeral_digest':self.pending_digest()})
        else:self.rec.emit('FROZEN_RECEIPT_COMMIT',{'context':self.context,'receipt':p['receipt'],'evidence':ref})
        return {'updated':learn,'post_digest':self.pdigest(),'counts':dict(self.rec.counts),'branch':self.branch}
    def derivative(self,target):
        if self.arm=='L':self.rec.charge('local')
        return super().derivative(target)
    def old_gradient(self,pre,codes,target):
        temp=BareLearner(self.rec);temp.ps=unpack(pre,True)
        h,z,p,hs,es,saved=temp.forward(codes,grad=True)
        self.rec.charge('backward');self.rec.charge('old_backward')
        gg=torch.autograd.grad(z[target]-z[1-target],temp.ps)
        row=arr(torch.cat([g.reshape(-1) for g in gg]));return row,arr(z),hs
    def margin_fixture(self,cue,scope,target):
        pre=arr(flat(self.ps));g,z,h=self.old_gradient(pre,[22,20+scope,cue],target)
        self.rec.frame({'kind':'old_derivative','context':self.context,'arm':self.arm,'cue':cue,'scope':scope,'target':target},{'params':pre,'raw_gradient':g,'logits':z,'h':h});return {'checked':True}
    def protect(self,prepared):
        p=self.pending;raw=prepared['raw'];records=valid_buffer(self.table);pre=arr(flat(self.ps));version=self.pdigest();pd=self.pending_digest()
        rows=[];zs=[];hs=[]
        for rec in records:
            r,z,h=self.old_gradient(pre,rec['codes'],rec['label']);rows.append(r);zs.append(z);hs.append(h)
        if self.pdigest()!=version or self.pending_digest()!=pd:raise RuntimeError('PROTECT_MUTATED_PENDING')
        A=np.array(rows,dtype='f4');norm=torch.linalg.vector_norm(raw);fac=torch.minimum(torch.ones(()),2./norm) if norm>0 else torch.ones(())
        product=arr(raw*fac);d2=-product.astype('f8')
        try:sol=solve(A,d2,self.rec.charge)
        except Exception as exc:
            if hasattr(exc,'evidence'):self.rec.frame({'kind':'solver_failure','context':self.context,'arm':self.arm,'reason':str(exc)},exc.evidence)
            raise
        pair=apply_pair(pre,d2,product,sol)
        arrays={'params':pre,'A':A,'old_logits':np.array(zs,dtype='f4'),'old_h':np.array(hs,dtype='f4'),'d2':d2,**sol,**pair}
        ref=self.rec.frame({'kind':'protection','context':self.context,'arm':self.arm,'buffer':records,'pre_digest':version,'pending_digest':pd,'selected_step':self.branch,'exact_old_derivatives':True,'hybrid':self.arm=='L'},arrays)
        prepared['protection_ref']=ref;prepared['protected_post']=pair['thetaP' if self.branch=='P' else 'thetaS']
        return arrays

class Engine:
    def __init__(self,rec):self.rec=rec;self.models={};self.active=None;self.allowed_tables={sha(canon({}))}
    @property
    def model(self):return self.models[self.active]
    def load(self,**kwargs):
        if any(m.pending is not None for m in self.models.values()):raise RuntimeError('LOAD_WITH_PENDING')
        if sha(canon(kwargs.get('table') or {})) not in self.allowed_tables:raise RuntimeError('UNOBSERVED_BUFFER_LOAD')
        m=Learner(self.rec);m.load(**kwargs);self.models={m.branch:m};self.active=m.branch;return {'loaded':True}
    def select(self,branch):
        if self.model.pending is not None:raise RuntimeError('SWITCH_WITH_PENDING')
        if branch not in self.models:raise RuntimeError('MISSING_BRANCH')
        self.active=branch;self.rec.emit('BRANCH_SELECTED',{'context':self.model.context,'branch':branch});return {'branch':branch}
    def import_fixture(self,observations):
        m=self.model
        if m.pending is not None or m.table or len(observations)!=8:raise RuntimeError('BAD_FIXTURE_IMPORT')
        for r in observations:
            c=r['cue'];sc=r['scope']
            if c not in range(8) or sc!=(c>=4) or r['target'] not in (0,1):raise RuntimeError('BAD_FIXTURE_RECORD')
            m.table[f'{sc}:{c}']=entry(c,sc,r['target'],r['receipt'],'OBSERVED_FIXTURE_HISTORY','OBSERVED_FIXTURE_HISTORY',r['sequence'],'fixture_prior_receipt')
        valid_buffer(m.table);self.rec.frame({'kind':'buffer_import','context':m.context,'arm':m.arm,'observations':observations,'table':m.table},{})
        self.allowed_tables.add(sha(canon(m.table)));return {'imported':8,'table':copy.deepcopy(m.table)}
    def receipt(self,scope,receipt,version,target,defect=None):
        m=self.model;reason=m.rejection(scope,receipt,version,target)
        if reason:
            before=m.pending_digest();self.rec.emit('RECEIPT_REJECT',{'context':m.context,'reason':reason,'receipt':receipt,'pending_before':before,'pending_after':m.pending_digest(),'table_digest':sha(canon(m.table))});return {'rejected':reason,'pending_unchanged':True}
        p=m.pending;changed=decide(m.table,p['codes'][-1],scope,target,m.used)
        if changed and m.candidate and m.arm in ('G','L'):
            if m.branch!='COMMON':raise RuntimeError('SECOND_BRANCH_CREATION')
            cc=dict(m.context);common_ref=p['cue_ref'];common_seq=p['prediction_sequence']
            self.rec.emit('VALIDATED_CHANGED_RECEIPT',{'context':cc,'receipt':receipt,'outcome':target,'previous_public_label':m.table[f'{scope}:{p["codes"][-1]}']['label']})
            self.rec.frame({'kind':'fork','context':cc,'arm':m.arm,'receipt':receipt,'target':target,'table':m.table,'used':m.used,'cue_ref':common_ref,'prediction_sequence':common_seq},{'params':p['pre'],'pending_h':p['states'],'pending_probabilities':arr(p['p']),'pending_trace':p['trace_steps'],'live_filler':arr(m.live)})
            copies={'B1':m}
            for branch in ('B2','P','S'):
                other=Learner(self.rec);other.load(p['pre'],m.arm,cc,table=m.table,candidate=True,branch=branch,used=False,consumed=m.consumed)
                other.start_cue(p['codes'][-1],scope,receipt,cc,reconstructed=True,original_sequence=common_seq,original_ref=common_ref);other.live=m.live.detach().clone()
                for k in ('states','trace_steps'):
                    if not np.array_equal(p[k],other.pending[k]):raise RuntimeError('FORK_FORWARD_MISMATCH:'+k)
                for k in ('h','z','p','V'):
                    if not torch.equal(p[k],other.pending[k]):raise RuntimeError('FORK_TENSOR_MISMATCH:'+k)
                copies[branch]=other
            storages=[t.untyped_storage().data_ptr() for mm in copies.values() for t in mm.ps]
            if len(set(storages))!=20:raise RuntimeError('FORK_MUTABLE_ALIAS')
            m.branch='B1';m.context={**cc,'branch':'B1'}
            prepared={b:mm.prepare(target,1. if b=='B1' else 2.,defect) for b,mm in copies.items()}
            if not all(torch.equal(prepared['B1']['raw'],x['raw']) for x in prepared.values()):raise RuntimeError('FORK_GRADIENT_MISMATCH')
            self.rec.frame({'kind':'fork_match','context':cc,'arm':m.arm,'receipt':receipt,'bitwise_forward_gradient':True,'distinct_mutable_storage':True},{'raw_gradient':arr(prepared['B1']['raw'])})
            pa=copies['P'].protect(prepared['P']);sa=copies['S'].protect(prepared['S'])
            for key in pa:
                if not np.array_equal(pa[key],sa[key]):raise RuntimeError('P_S_PROTECTION_MISMATCH:'+key)
            # All calculations/steps are fixed before any branch answers are observed.
            outs=[]
            for b,mm in copies.items():
                outs.append(mm.apply(prepared[b],True));self.allowed_tables.add(sha(canon(mm.table)))
            self.models=copies;self.active='B1';return {'forked':True,'branches':outs}
        prep=m.prepare(target,1.,defect);ans=m.apply(prep,changed);self.allowed_tables.add(sha(canon(m.table)));return {**ans,'forked':False}
