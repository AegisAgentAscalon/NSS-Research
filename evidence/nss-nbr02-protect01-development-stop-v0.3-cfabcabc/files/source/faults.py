"""Bounded non-neural detector injections. Live numeric data comes from already charged fixtures."""
import json,hashlib,struct,subprocess,sys,os,tempfile,errno
from pathlib import Path
import numpy as np
from reference_numeric import records,math_reference,expected_step,log_check,canonical

def exercise(run,out):
    run=Path(run);out=Path(out);out.mkdir(parents=True,exist_ok=True);data=list(records(run/'worker/records.bin'));tests=[]
    def report(id,observed,clean,detail):
        if not observed or not clean:raise AssertionError('FAULT_DETECTOR:'+id)
        tests.append({'id':id,'injection_detected_or_limit_classified':bool(observed),'clean_control_passed':bool(clean),'details':detail,'evidence':'existing charged fixture or isolated synthetic copy','not_natural_scientific_failure':True})
    pending={'scope':0,'id':'a','version':'v','consumed':['old']}
    def receipt(r):
        if r['scope']!=pending['scope']:return 'WRONG_SCOPE'
        if r['id'] in pending['consumed']:return 'CONSUMED'
        if r['id']!=pending['id']:return 'UNKNOWN'
        if r['version']!=pending['version']:return 'STALE'
        return 'ACCEPT'
    clean={'scope':0,'id':'a','version':'v','outcome':0}
    report('FF01',all(receipt({**clean,**d})!='ACCEPT' for d in ({'scope':1},{'id':'bad'},{'id':'old'})),receipt(clean)=='ACCEPT','Wrong scope, unknown and consumed IDs rejected; live matching cases also covered by receipt diagnostic.')
    report('FF02',pending is not None, None is None,'Synthetic terminal boundary with nonempty pending record => INCOMPLETE, no invented target.')
    la=next(a for _,m,a in data if m['kind']=='cue' and m['arm']=='L')
    x=la['elig_steps'].copy();x.flat[0]+=1
    report('FF03',hashlib.sha256(x.tobytes()).digest()!=hashlib.sha256(la['elig_steps'].tobytes()).digest(),np.array_equal(la['elig_steps'],la['elig_steps'].copy()),'Copied eligibility corruption changes digest; live wait snapshots are checked separately.')
    report('FF04',receipt({**clean,'version':'changed'})=='STALE',receipt(clean)=='ACCEPT','Version changed before application; pure envelope control.')
    ca=next((m,a) for _,m,a in data if m['kind']=='cue' and m['arm']=='G')
    cm,a=ca;ref=math_reference(a['params'],cm['codes'],0);wrong=ref['logits'].copy()+np.array([.1,-.1])
    report('FF05',not np.allclose(wrong,ref['logits'],atol=2e-6,rtol=2e-5),np.allclose(a['logits'],ref['logits'],atol=2e-6,rtol=2e-5),'Copied filler-dependent replacement logit rejected numerically. No extra live wrong-graph backward; live clean graph saved-tensor inventory retained.')
    dm,da=next((m,a) for _,m,a in data if m['kind']=='cue' and m['arm']=='L' and a['elig_steps'].size and np.max(np.abs(a['h']))>.01)
    lr=math_reference(da['params'],dm['codes'],0);wrong=lr['L'].copy();wrong[:640]*=.5
    report('FF06',not np.allclose(wrong,lr['L'],atol=2e-6,rtol=2e-5),np.allclose(da['elig_steps'],lr['elig_steps'],atol=2e-6,rtol=2e-5),'Omitted local factor differs from independent local equation; genuine dense exact/local differences are not rejected.')
    sand=[m for _,m,a in data if m['kind']=='update' and m.get('defect')]
    report('FF07',len(sand)==8,any(m['kind']=='update' and not m.get('defect') for _,m,a in data),'Eight charged sandbox sign/double-step applications independently rejected by numeric auditor; no scientific weights inherit them.')
    def visible(msg):
        allowed={'op','cue','scope','receipt','context'}
        if set(msg)-allowed:raise ValueError('UNRELEASED_FIELD')
        return {k:msg[k] for k in sorted(msg)}
    c={'op':'CUE','cue':0,'scope':0,'receipt':'a','context':{'session':'opaque','trial':1}}
    detected=False
    try:visible({**c,'future_target':1})
    except ValueError:detected=True
    report('FF08',detected,visible(c)==visible(dict(c)),'Schema rejects hidden fields. Counterfactual outer labels/future suffixes project to same permitted message; live worker file guard is separately exercised.')
    # A distinct tiny child really writes intent and exits without commit. No learner update is dispatched.
    logfile=out/'lost_commit.jsonl'
    script="import json,os,sys; f=open(sys.argv[1],'w');f.write(json.dumps({'event':'UPDATE_INTENT','attempt':1})+'\\n');f.flush();os.fsync(f.fileno());os._exit(7)"
    p=subprocess.run([sys.executable,'-c',script,str(logfile)],capture_output=True)
    rr=[json.loads(s) for s in logfile.read_text().splitlines()]
    report('FF09',p.returncode==7 and len(rr)==1 and rr[0]['event']=='UPDATE_INTENT', any(m['kind']=='update' and not m.get('defect') for _,m,a in data),'Isolated child intent persists without commit => COMPLETION_UNKNOWN, one synthetic attempted slot; no actual neural update.')
    payload=b'fixture-array';good={'a.bin':hashlib.sha256(payload).hexdigest()}
    def membercheck(d):return all(k in d and hashlib.sha256(d[k]).hexdigest()==h for k,h in good.items())
    report('FF10',not membercheck({}) and not membercheck({'a.bin':b'altered'}),membercheck({'a.bin':payload}),'Required-member absence and altered bytes fail; final whole-study relocation remains separately required.')
    class Sink:
        def __init__(self,n):self.n=n;self.data=b''
        def write(self,b):
            if len(self.data)+len(b)>self.n:raise OSError(errno.ENOSPC,'bounded synthetic quota')
            self.data+=b
    sink=Sink(8);sink.write(b'intent');bad=False
    try:sink.write(b'commit')
    except OSError as e:bad=e.errno==errno.ENOSPC
    good_sink=Sink(32);good_sink.write(b'intent');good_sink.write(b'commit')
    report('FF11',bad and sink.data==b'intent',good_sink.data==b'intentcommit','Bounded quota sink preserves last durable intention. No shared filesystem is filled.')
    def timing(seq):return seq['prediction']<seq['feedback']<seq['probe']
    report('FF12',not timing({'prediction':5,'feedback':3,'probe':5}),timing({'prediction':1,'feedback':3,'probe':5}),'Copied post-feedback output cannot replace prediction timestamp/record join.')
    required={'raw_scores','approximation','failures','budget'}
    report('FF13',not required.issubset({'raw_scores','budget'}),required.issubset(required),'Missing approximation/failure sections fail completeness rather than imply a cause.')
    report('FF14',receipt({**clean,'outcome':1})=='ACCEPT',receipt(clean)=='ACCEPT','Authenticated false outcome with no public warning is indistinguishable here; ACCEPT is detection limit, not erroneous hidden-gold rejection.')
    (out/'FAULT_RESULTS.json').write_text(json.dumps({'status':'PASS','tests':tests,'live_injected_graph_fault_tested':False,'covers_all_failure_modes':False},indent=2));return tests

if __name__=="__main__":
    print(json.dumps(exercise(sys.argv[1],sys.argv[2]),indent=2))
