"""Non-neural deterministic authority/reducer tests. No model/gradient operations."""
import numpy as np,copy,json,hashlib
from runtime import entry,valid_buffer,validate_record,reduce_batch,decide,validate

def run_checks(rec):
    checks=[]
    def ok(name,fn):fn();checks.append({'name':name,'pass':True})
    def must_fail(fn):
        try:fn()
        except (RuntimeError,ValueError,KeyError):return
        raise AssertionError('BAD_CASE_ACCEPTED')
    table={f'{int(c>=4)}:{c}':entry(c,int(c>=4),[0,1,0,1,1,0,1,0][c],f'{c+1:016x}','a'*64,'b'*64,c+1) for c in range(8)}
    ok('complete_valid_buffer',lambda: (len(valid_buffer(table))==8) or (_ for _ in ()).throw(AssertionError()))
    for fault in ('MISSING','REVOKED','CONFLICT','SCOPE','STALE_FEATURE','ID','UNRELEASED'):
        tt=copy.deepcopy(table)
        if fault=='MISSING':del tt['0:0']
        elif fault in ('REVOKED','CONFLICT'):tt['0:0']['validity']=fault
        elif fault=='SCOPE':tt['0:0']['scope']=1
        elif fault=='STALE_FEATURE':tt['0:0']['feature_hash']='0'*64
        elif fault=='ID':tt['0:0']['receipt']='x'*16
        else:tt['0:0']['receipt_sequence']=0
        ok('reject_'+fault,lambda t=tt:must_fail(lambda:valid_buffer(t)))
    def reducer_cases():
        a=np.zeros((8,674),'f4');a[:,0]=.125;a[:,1]=-.25
        _,_,m=reduce_batch(a);assert np.array_equal(m,a[0])
        a[:]=0;a[:4,0]=2;a[4:,0]=-2;assert not np.any(reduce_batch(a)[2])
        a[:]=0;a[:4,0]=2;a[4:,1]=1;m=reduce_batch(a)[2];assert m[0]==1 and m[1]==.5
        individually=np.array([g/min(1e30,max(1.,float(np.linalg.norm(g)))) for g in a]);assert not np.allclose(individually.mean(0),m/np.linalg.norm(m))
        small=np.nextafter(np.float32(0),np.float32(1));a[:]=0;a[:,0]=small;a[:,1]=-small;assert np.array_equal(reduce_batch(a)[2],a[0])
        a[:]=0;a[0,0]=np.inf;must_fail(lambda:reduce_batch(a));must_fail(lambda:reduce_batch(np.zeros((7,674),'f4')))
    ok('reducer_repeat_cancel_clip_subnormal_nonfinite_shape',reducer_cases)
    def admission():
        def good(old,mixed,acq,recovered,final):return old==8 and mixed>=16 and acq==4 and recovered==4 and final==4
        assert good(8,16,4,4,4) and not good(8,15,4,4,4)
        for x in [(7,20,4,4,4),(8,20,3,4,4),(8,20,4,3,4),(8,20,4,4,3)]:assert not good(*x)
        assert sum([good(8,16,4,4,4)]*3+[False])==3
    ok('prospective_basic_competence',admission)
    def timing_rules():
        from timing_policy import advance
        empty={'correction':None,'ready':False,'spent':False}
        e=advance(empty,'E',8,0,1,'a',True);late=advance(empty,'LATE',8,0,1,'a',True)
        assert e['ready'] and not late['ready']
        assert advance(late,'LATE',4,1,0,'b',False)==late
        assert advance(late,'LATE',8,0,1,'a',False)==late
        assert advance(late,'LATE',8,0,1,'c',False)['ready']
        must_fail(lambda:advance(late,'LATE',8,0,0,'c',False))
        spent={**late,'ready':False,'spent':True}
        assert advance(spent,'LATE',8,0,1,'d',False)==spent
        # A missing follow-up leaves the unspent late slot pending: no replacement or fabricated replay.
        assert not late['ready'] and not late['spent']
    ok('public_timing_missing_wrong_duplicate_followup',timing_rules)
    def receipts():
        p={'scope':0,'receipt':'1'*16,'version':'a'*64,'immutable':'b'*64}
        assert validate(p,set(),0,'1'*16,'a'*64,0,'a'*64,'b'*64) is None
        for sc,rid,ver,y,pd,td in [(1,'1'*16,'a'*64,0,'a'*64,'b'*64),(0,'2'*16,'a'*64,0,'a'*64,'b'*64),(0,'1'*16,'c'*64,0,'a'*64,'b'*64),(0,'1'*16,'a'*64,2,'a'*64,'b'*64),(0,'1'*16,'a'*64,0,'a'*64,'c'*64)]:assert validate(p,set(),sc,rid,ver,y,pd,td) is not None
        assert validate(p,{'1'*16},0,'1'*16,'a'*64,0,'a'*64,'b'*64)=='CONSUMED_ID'
        assert decide(table,0,0,1,False) and not decide(table,0,0,1,True)
        # The same publicly authenticated false target cannot be detected from hidden scoring truth.
        assert validate(p,set(),0,'1'*16,'a'*64,1,'a'*64,'b'*64) is None
    ok('receipt_identity_single_consumption_public_change_false_label_limit',receipts)
    result={'status':'PASS','tests':checks,'model_calls':0,'optimizer_updates':0,'synthetic_only':True}
    rec.emit('STATIC_FIXTURES',result);return result
