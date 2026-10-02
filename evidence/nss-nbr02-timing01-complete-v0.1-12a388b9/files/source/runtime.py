"""TIMING01 causal learner. No seeds, future input, hidden scores, or task generator.
Inherited DC01/REV01 forward and single-example arithmetic are unchanged.
"""
import copy,json,os,struct,zlib,time
from pathlib import Path
import numpy as np
import torch
from base_runtime import Learner as BareLearner, Recorder as BareRecorder,canon,sha,flat,arr,unpack,packframe
from rev_runtime import Learner as PriorLearner,decide,validate
CAPS={'cell':130000,'head':40000,'backward':3000,'local':3000,'update_attempt':3500,'replay_fetch':2400}
SCHEMA={'load':2696,'management_load':0,'cue':10648,'fillers':2112,'update':8096,'frozen_receipt':2696,'query':272,'checkpoint':12000,'fork':10704,'fork_match':2696,'derivative':2696,'buffer_import':0,'batch_example':13344,'batch_apply':50000,'post_strong_match':0}

def entry(cue,scope,label,receipt,pre,post,sequence,origin='validated_receipt'):
    codes=[22,20+scope,cue]
    return {'schema':1,'scope':scope,'cue':cue,'codes':codes,'feature_hash':sha(np.eye(23,dtype='f4')[codes].tobytes()),'label':int(label),'receipt':receipt,'pre_version':pre,'post_version':post,'receipt_sequence':int(sequence),'validity':'VALID','origin':origin}
def validate_record(r,c,sc):
    if r is None or r.get('schema')!=1 or r.get('validity')!='VALID' or r.get('scope')!=sc or r.get('cue')!=c or r.get('label') not in (0,1):raise RuntimeError('BUFFER_INVALID')
    if r.get('codes')!=[22,20+sc,c] or r.get('feature_hash')!=sha(np.eye(23,dtype='f4')[r['codes']].tobytes()):raise RuntimeError('FEATURE_AUTHORITY')
    if not isinstance(r.get('receipt'),str) or len(r['receipt'])!=16 or r['receipt']=='0'*16 or any(x not in '0123456789abcdef' for x in r['receipt']):raise RuntimeError('RECEIPT_AUTHORITY')
    if r['origin'] not in ('validated_receipt','fixture_prior_receipt') or r['receipt_sequence']<=0:raise RuntimeError('UNRELEASED_SOURCE')
    return copy.deepcopy(r)
def valid_buffer(table):return [validate_record(table.get(f'{int(c>=4)}:{c}'),c,int(c>=4)) for c in range(8)]
def reduce_batch(raws):
    a=np.asarray(raws)
    if a.dtype!=np.float32 or a.shape!=(8,674) or not np.isfinite(a).all():raise RuntimeError('BATCH_SHAPE_OR_FINITE')
    acc=np.zeros(674,dtype='f8')
    for i in range(8):acc+=a[i].astype('f8')
    mean64=acc/8.;return acc,mean64,mean64.astype('f4')
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
        if hn>65536 or len(raw)>262144:raise RuntimeError('FRAME_SCHEMA_OVERRUN:'+kind)
        st=self.kindstats.setdefault(kind,{'count':0,'numeric_logical':0,'encoded':0,'header':0,'max_numeric':0,'max_header':0})
        st['count']+=1;st['numeric_logical']+=extent;st['encoded']+=len(payload)+40;st['header']+=hn;st['max_numeric']=max(st['max_numeric'],extent);st['max_header']=max(st['max_header'],hn)
        off=self.raw.tell();h=sha(payload);self.raw.write(struct.pack('<Q',len(payload))+bytes.fromhex(h)+payload);os.fsync(self.raw.fileno());self.rec+=1
        ref={'index':self.rec,'offset':off,'bytes':len(payload)+40,'sha256':h}
        self.emit('EVIDENCE_DURABLE',{'frame':ref,'kind':kind,'context':meta.get('context')});return ref
    def close(self):
        (self.out/'SCHEMA_OBSERVED.json').write_text(json.dumps(self.kindstats,indent=2));super().close()
class Learner(PriorLearner):
    def __init__(self,rec):
        super().__init__(rec);self.rehearsed=False;self.last_online_attempt=None;self.last_receipt=None;self.timing={'correction':None,'ready':False,'spent':False}
    def rejection(self,scope,receipt,version,target):
        if type(scope)!=int or scope not in (0,1):return 'BAD_SCOPE_TYPE'
        if not isinstance(receipt,str) or len(receipt)!=16 or receipt=='0'*16 or any(c not in '0123456789abcdef' for c in receipt):return 'BAD_RECEIPT_ID'
        if not isinstance(version,str) or len(version)!=64 or any(c not in '0123456789abcdef' for c in version):return 'BAD_VERSION_ID'
        if type(target)!=int or target not in (0,1):return 'BAD_OUTCOME'
        return super().rejection(scope,receipt,version,target)
    def prepare(self,target,clip,defect=None):
        if self.arm=='L':self.rec.charge('local')
        return super().prepare(target,clip,defect)
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
                for t in self.ps:n=t.numel();t.sub_(step[k:k+n].reshape(t.shape));k+=n
            if not torch.isfinite(flat(self.ps)).all():raise RuntimeError('NONFINITE_POSTSTATE')
        self.table[f"{p['scope']}:{p['codes'][-1]}"]=entry(p['codes'][-1],p['scope'],target,p['receipt'],p['version'],self.pdigest(),self.rec.seq)
        self.used=self.used or changed;self.live=torch.zeros(16);self.consumed.add(p['receipt'])
        from timing_policy import advance
        self.timing=advance(self.timing,self.branch,p['codes'][-1],p['scope'],target,p['receipt'],changed)
        arrays={'post':arr(flat(self.ps))}
        if learn:arrays.update({'raw_gradient':arr(raw),'norm_factor':np.array([float(norm),float(factor)],dtype='f4'),'proposed_clip_product':arr(raw*factor)})
        meta={'kind':'update' if learn else 'frozen_receipt','context':self.context,'arm':self.arm,'target':target,'receipt':p['receipt'],'pre_digest':p['version'],'cue_ref':p['cue_ref'],'prediction_sequence':p['prediction_sequence'],'defect':defect,'intended_injection':defect is not None,'post_digest':self.pdigest(),'ephemeral_reset':True,'clip':clip,'changed':changed,'used':self.used,'table_before':pretable,'table_after':copy.deepcopy(self.table),'timing':copy.deepcopy(self.timing)}
        ref=self.rec.frame(meta,arrays);self.pending=None;self.last_online_attempt=prepared['attempt'];self.last_receipt=p['receipt']
        if learn:
            self.rec.counts['update_commit']+=1;self.rec.emit('UPDATE_COMMIT',{'attempt':prepared['attempt'],'context':self.context,'receipt':p['receipt'],'evidence':ref,'post_digest':self.pdigest(),'ephemeral_digest':self.pending_digest()})
        else:self.rec.emit('FROZEN_RECEIPT_COMMIT',{'context':self.context,'receipt':p['receipt'],'evidence':ref})
        return {'updated':learn,'post_digest':self.pdigest(),'counts':dict(self.rec.counts),'branch':self.branch}
    def derivative(self,target):
        if self.arm=='L':self.rec.charge('local')
        return super().derivative(target)
    def batch(self,role,focal=None,defect=None):
        if self.pending is not None or self.rehearsed:raise RuntimeError('BATCH_PENDING_OR_REPEATED')
        if self.arm not in ('G','L'):raise RuntimeError('BATCH_ON_FROZEN')
        fault=defect is not None
        if not fault and (self.branch not in ('E','LATE') or role!='OLD' or not self.used or self.last_online_attempt is None or not self.timing['ready'] or self.timing['spent']):raise RuntimeError('BATCH_NOT_AUTHORIZED')
        if role=='OLD':src=valid_buffer(self.table)
        elif role=='F':
            if focal is None:raise RuntimeError('NO_FOCAL_REFERENCE')
            sc=0 if focal in (0,1,2,3,8,9,12,13,14,15) else 1
            r=validate_record(self.table.get(f'{sc}:{focal}'),focal,sc);src=[copy.deepcopy(r) for _ in range(8)]
        else:raise RuntimeError('UNKNOWN_BATCH_ROLE')
        if not fault and role=='F' and src[0]['receipt']!=self.last_receipt:raise RuntimeError('STALE_FOCAL_REPLAY')
        if not fault and role=='OLD' and any(r['cue']==focal for r in src):raise RuntimeError('FOCAL_IN_OLD_BUFFER')
        pre=arr(flat(self.ps));ver=self.pdigest();tb=copy.deepcopy(self.table);cons=set(self.consumed);live=arr(self.live)
        operation=sha(canon({'schema':'REHEARSAL_v1','learner_namespace':self.context['session'],'branch':self.branch,'parent_online_application':self.last_online_attempt if not fault else 'SYNTHETIC_PRIOR_RECEIPT','batch_ordinal':0,'sources':[r['receipt'] for r in src]}))
        self.rec.charge('update_attempt');attempt=self.rec.counts['update_attempt']
        self.rec.emit('UPDATE_INTENT',{'attempt':attempt,'operation':'REHEARSAL','context':self.context,'application_id':operation,'pre_digest':ver,'parent_online_attempt':self.last_online_attempt,'defect':defect})
        rawlist=[];refs=[]
        for i,r in enumerate(src):
            self.rec.charge('replay_fetch')
            current=validate_record(self.table.get(f'{r["scope"]}:{r["cue"]}'),r['cue'],r['scope'])
            if current!=r or self.pdigest()!=ver:raise RuntimeError('BATCH_SOURCE_OR_PRESTATE_CHANGED')
            h,z,p,hs,E,saved=self.forward(r['codes'],grad=self.arm=='G',elig=self.arm=='L')
            if self.arm=='G':
                self.rec.charge('backward');loss=torch.nn.functional.cross_entropy(z.reshape(1,2),torch.tensor([r['label']]));gs=torch.autograd.grad(loss,self.ps);raw=torch.cat([g.reshape(-1) for g in gs]).detach()
            else:
                self.rec.charge('local')
                with torch.no_grad():
                    q=p.clone();q[r['label']]-=1;delta=self.ps[3].T@q;e=torch.tensor(E[-1]);raw=torch.cat(((delta[:,None]*e[:368].reshape(16,23)).reshape(-1),(delta[:,None]*e[368:624].reshape(16,16)).reshape(-1),delta*e[624:],torch.outer(q,h).reshape(-1),q))
            if not torch.isfinite(raw).all():raise RuntimeError('NONFINITE_BATCH_GRADIENT')
            gg=arr(raw);rawlist.append(gg)
            refs.append(self.rec.frame({'kind':'batch_example','context':self.context,'arm':self.arm,'role':role,'application_id':operation,'ordinal':i,'source':r,'pre_digest':ver,'state_reset':True,'saved_tensor_inventory':saved,'source_hash':sha(canon(r))},{'params':pre,'h':hs,'elig_steps':E,'logits':arr(z),'probabilities':arr(p),'raw_gradient':gg}))
        rawarray=np.asarray(rawlist,dtype='f4');acc,mean64,mean32=reduce_batch(rawarray)
        if role=='F' and (not np.array_equal(rawarray,np.repeat(rawarray[:1],8,axis=0)) or not np.array_equal(mean32,rawarray[0])):raise RuntimeError('FOCAL_REPEAT_MEAN')
        if self.pdigest()!=ver or self.table!=tb or self.consumed!=cons or not np.array_equal(arr(self.live),live):raise RuntimeError('BATCH_PREMUTATION')
        raw=torch.from_numpy(mean32.copy());norm=torch.linalg.vector_norm(raw);factor=torch.minimum(torch.ones(()),1./norm) if norm>0 else torch.ones(());product=raw*factor;applied=product.clone()
        if defect=='sign':applied=-applied
        elif defect=='double':applied=applied*2
        with torch.no_grad():
            k=0
            for t in self.ps:n=t.numel();t.sub_(applied[k:k+n].reshape(t.shape));k+=n
        if not torch.isfinite(flat(self.ps)).all():raise RuntimeError('NONFINITE_BATCH_POSTSTATE')
        self.live=torch.zeros(16);self.rehearsed=True
        self.timing={**self.timing,'ready':False,'spent':True}
        arrays={'pre':pre,'post':arr(flat(self.ps)),'example_gradients':rawarray,'accumulator64':acc,'mean64':mean64,'mean32':mean32,'norm_factor':np.array([float(norm),float(factor)],dtype='f4'),'clip_product':arr(product),'applied_product':arr(applied)}
        ref=self.rec.frame({'kind':'batch_apply','context':self.context,'arm':self.arm,'role':role,'application_id':operation,'sources':src,'examples':refs,'pre_digest':ver,'post_digest':self.pdigest(),'table_unchanged':self.table==tb,'consumed_unchanged':self.consumed==cons,'parent_online_attempt':self.last_online_attempt,'ephemeral_reset':True,'defect':defect,'expected_injection':fault,'timing':copy.deepcopy(self.timing)},arrays)
        self.rec.counts['update_commit']+=1;self.rec.emit('UPDATE_COMMIT',{'attempt':attempt,'operation':'REHEARSAL','context':self.context,'application_id':operation,'evidence':ref,'post_digest':self.pdigest(),'ephemeral_digest':self.pending_digest()})
        return {'rehearsed':True,'post_digest':self.pdigest(),'counts':dict(self.rec.counts)}
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
            if c not in range(8) or sc!=int(c>=4) or r['target'] not in (0,1) or f'{sc}:{c}' in m.table:raise RuntimeError('BAD_FIXTURE_RECORD')
            m.table[f'{sc}:{c}']=entry(c,sc,r['target'],r['receipt'],'OBSERVED_FIXTURE_HISTORY','OBSERVED_FIXTURE_HISTORY',r['sequence'],'fixture_prior_receipt')
        valid_buffer(m.table);self.rec.frame({'kind':'buffer_import','context':m.context,'arm':m.arm,'observations':observations,'table':m.table},{})
        self.allowed_tables.add(sha(canon(m.table)));return {'imported':8,'table':copy.deepcopy(m.table)}
    def receipt(self,scope,receipt,version,target,defect=None):
        m=self.model;reason=m.rejection(scope,receipt,version,target)
        if reason:
            before=m.pending_digest();self.rec.emit('RECEIPT_REJECT',{'context':m.context,'reason':reason,'receipt':receipt,'pending_before':before,'pending_after':m.pending_digest(),'table_digest':sha(canon(m.table))});return {'rejected':reason,'pending_unchanged':True}
        if defect is not None:raise RuntimeError('REAL_RECEIPT_DEFECT_NOT_ALLOWED')
        p=m.pending;changed=decide(m.table,p['codes'][-1],scope,target,m.used)
        if changed and m.candidate and m.arm in ('G','L'):
            if m.branch!='COMMON':raise RuntimeError('SECOND_BRANCH_CREATION')
            cc=dict(m.context);common_ref=p['cue_ref'];common_seq=p['prediction_sequence']
            self.rec.emit('VALIDATED_CHANGED_RECEIPT',{'context':cc,'receipt':receipt,'outcome':target,'previous_public_label':m.table[f'{scope}:{p["codes"][-1]}']['label']})
            self.rec.frame({'kind':'fork','context':cc,'arm':m.arm,'receipt':receipt,'target':target,'table':m.table,'used':m.used,'cue_ref':common_ref,'prediction_sequence':common_seq},{'params':p['pre'],'pending_h':p['states'],'pending_probabilities':arr(p['p']),'pending_trace':p['trace_steps'],'live_filler':arr(m.live)})
            copies={'B1':m}
            for branch in ('U','E','LATE'):
                other=Learner(self.rec);other.load(p['pre'],m.arm,cc,table=m.table,candidate=True,branch=branch,used=False,consumed=m.consumed)
                other.start_cue(p['codes'][-1],scope,receipt,cc,reconstructed=True,original_sequence=common_seq,original_ref=common_ref);other.live=m.live.detach().clone()
                for k in ('states','trace_steps'):
                    if not np.array_equal(p[k],other.pending[k]):raise RuntimeError('FORK_FORWARD_MISMATCH:'+k)
                for k in ('h','z','p','V'):
                    if not torch.equal(p[k],other.pending[k]):raise RuntimeError('FORK_TENSOR_MISMATCH:'+k)
                copies[branch]=other
            ptrs=[t.untyped_storage().data_ptr() for mm in copies.values() for t in mm.ps]
            if len(set(ptrs))!=20:raise RuntimeError('FORK_MUTABLE_ALIAS')
            m.branch='B1';m.context={**cc,'branch':'B1'}
            prepared={b:mm.prepare(target,1. if b=='B1' else 2.) for b,mm in copies.items()}
            if not all(torch.equal(prepared['B1']['raw'],x['raw']) for x in prepared.values()):raise RuntimeError('FORK_GRADIENT_MISMATCH')
            self.rec.frame({'kind':'fork_match','context':cc,'arm':m.arm,'receipt':receipt,'bitwise_forward_gradient':True,'distinct_mutable_storage':True},{'raw_gradient':arr(prepared['B1']['raw'])})
            outs=[]
            for b,mm in copies.items():outs.append(mm.apply(prepared[b],True));self.allowed_tables.add(sha(canon(mm.table)))
            if not all(copies[b].pdigest()==copies['U'].pdigest() for b in ('E','LATE')):raise RuntimeError('POST_STRONG_WEIGHTS')
            # Per-record release sequence differs by branch; semantic source/label identity and parameter versions match.
            sem=lambda t:{k:{x:v for x,v in r.items() if x!='receipt_sequence'} for k,r in t.items()}
            if not all(sem(copies[b].table)==sem(copies['U'].table) for b in ('E','LATE')):raise RuntimeError('POST_STRONG_AUTHORITY')
            self.rec.frame({'kind':'post_strong_match','context':cc,'arm':m.arm,'branches':['U','E','LATE'],'parameter_hash':copies['U'].pdigest(),'semantic_authority_equal':True},{})
            self.models=copies;self.active='B1';return {'forked':True,'branches':outs}
        prep=m.prepare(target,1.);ans=m.apply(prep,changed);self.allowed_tables.add(sha(canon(m.table)));return {**ans,'forked':False}
