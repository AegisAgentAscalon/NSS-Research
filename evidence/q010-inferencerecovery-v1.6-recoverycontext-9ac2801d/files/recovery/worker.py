from pathlib import Path
import sys,os,time,json,traceback,datetime,resource,argparse
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
sys.path[:0]=[str(ROOT/'recovery'),str(ROOT/'source'),str(STAGE/'implementation_A'),str(STAGE/'verification_B')]
from inference_loader import sha,read,deny_training,inspect_exports,load_readers

def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
def verify_source_lock(expected):
    p=ROOT/'protocol/RECOVERY_SOURCE_LOCK.json'
    if sha(p)!=expected:raise ValueError('recovery source lock digest mismatch')
    for name,h in read(p)['files'].items():
        if sha(ROOT/name)!=h:raise ValueError('recovery source drift: '+name)

p=argparse.ArgumentParser();p.add_argument('mode',choices=['audit','capture','score','compare']);p.add_argument('--seed',type=int);p.add_argument('--input',type=Path);p.add_argument('--right',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--fixture',action='store_true');p.add_argument('--source-lock',required=True);a=p.parse_args()
t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    verify_source_lock(a.source_lock)
    import torch,numpy as np
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);deny_training()
    if a.mode=='audit':write(a.output,inspect_exports())
    elif a.mode=='capture':
        from q010c.evaluate import capture_seed
        models,identities=load_readers(a.seed)
        with torch.no_grad():
            result=capture_seed(a.seed,models,identities,a.output,split='development' if a.fixture else 'heldout',development_count=4 if a.fixture else None)
        if not a.fixture and (result['cells']!=64 or result['chains']!=89928 or result['logical_stage_evaluations']!=609096):raise ValueError('full workload mismatch')
    elif a.mode=='score':
        # Producer/trainer implementations are deliberately not imported by scoring.
        from q010v.verify import verify_capture
        result=verify_capture(a.input,a.output)
        if any(x in sys.modules for x in ['q010c.evaluate','q010c.batch_core','q010r.evaluation','q010r.models','q010r.training']):raise ValueError('independent scorer imported producer')
        write(a.output/'INDEPENDENCE.json',{'status':'PASS','producer_modules_imported':False,'new_optimizer_updates':0,'source_lock_sha256':a.source_lock,'underflow_amendment_sha256':sha(ROOT/'source/q010v/pointer_math.py'),'scope_note':'Inherited verifier status text says DEVELOPMENT; exact actual main/development scope is bound in CAPTURE START and external recovery receipts.'})
    elif a.mode=='compare':
        left=read(a.input/'CAPTURE.json');right=read(a.right/'CAPTURE.json');arrays=elements=0
        if len(left['chunks'])!=len(right['chunks']):raise ValueError('replay frame count mismatch')
        for l,r in zip(left['chunks'],right['chunks'],strict=True):
            if (l['condition'],l['file'])!=(r['condition'],r['file']):raise ValueError('replay frame identity mismatch')
            with np.load(a.input/l['file'],allow_pickle=False) as za,np.load(a.right/r['file'],allow_pickle=False) as zb:
                if za.files!=zb.files:raise ValueError('replay array membership mismatch')
                for key in za.files:
                    u,v=za[key],zb[key]
                    if u.shape!=v.shape or u.dtype!=v.dtype or u.tobytes()!=v.tobytes():raise ValueError('replay array mismatch: '+l['file']+' '+key)
                    arrays+=1;elements+=u.size
            if read(a.input/l['meta'])!=read(a.right/r['meta']):raise ValueError('replay source/metadata mismatch')
        if left['weights_before']!=right['weights_before'] or left['weights_after']!=right['weights_after']:raise ValueError('replay weight identity mismatch')
        write(a.output,{'status':'PASS_EXACT_LOCAL_FRESH_PROCESS_REPLAY','seed':left['seed'],'frames':len(left['chunks']),'arrays_exact':arrays,'elements_exact':elements,'all_metadata_exact':True,'capture_sha256':sha(a.input/'CAPTURE.json'),'replay_sha256':sha(a.right/'CAPTURE.json'),'scope':'Fresh regeneration of every model/state/query/event array; not independent new samples or cross-host replication.'})
    print(json.dumps({'status':'WORKER_PASS','mode':a.mode,'pid':os.getpid(),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-t,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'new_optimizer_updates':0}),flush=True)
except BaseException as e:
    fail=ROOT/'failures'/f'{a.mode}_{a.seed}_{os.getpid()}.json'
    write(fail,{'error':repr(e),'traceback':traceback.format_exc(),'args':vars(a)|{'input':str(a.input),'right':str(a.right),'output':str(a.output)},'start_utc':start,'elapsed_seconds':time.monotonic()-t})
    raise
