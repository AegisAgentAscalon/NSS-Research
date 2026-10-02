"""Bounded synchronous study supervisor; preserves every worker log and failed output."""
from pathlib import Path
import os,sys,json,time,subprocess,datetime,concurrent.futures,threading
import psutil
ROOT=Path(__file__).resolve().parents[1]; LOCK=(ROOT/'protocol/RECOVERY_SOURCE_LOCK.sha256').read_text().strip();WORK=ROOT/'recovery/worker.py'; ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
def run(name,args):
    cmd=[sys.executable,str(WORK),*map(str,args),'--source-lock',LOCK];d=ROOT/'logs'/name;d.mkdir(exist_ok=False);t=time.monotonic();started=utc();peak=0
    with (d/'stdout.log').open('x') as out,(d/'stderr.log').open('x') as err:
        p=subprocess.Popen(cmd,stdout=out,stderr=err,cwd=ROOT,env=ENV)
        write(d/'START.json',{'utc':started,'pid':p.pid,'command':cmd,'source_lock_sha256':LOCK})
        while p.poll() is None:
            try:
                proc=psutil.Process(p.pid);rss=sum(x.memory_info().rss for x in [proc,*proc.children(recursive=True)] if x.is_running());peak=max(peak,rss)
                if rss>1879048192 or time.monotonic()-t>3600:p.kill();raise RuntimeError('worker resource ceiling '+name)
            except psutil.NoSuchProcess:pass
            time.sleep(1)
        code=p.returncode
    receipt={'name':name,'exit_code':code,'pid':p.pid,'start_utc':started,'end_utc':utc(),'wall_seconds':time.monotonic()-t,'sampled_peak_process_tree_rss_bytes':peak,'new_optimizer_updates':0}
    write(d/'END.json',receipt);print(json.dumps(receipt),flush=True)
    if code:raise RuntimeError('worker failed '+name+'; see retained stderr/output')
    return receipt

def pool(jobs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures=[ex.submit(run,name,args) for name,args in jobs]
        return [f.result() for f in futures]

start=time.monotonic(); stages=[]
try:
    f=ROOT/'results/integration_fixture';f.mkdir(exist_ok=False)
    stages.append(run('fixture_capture',['capture','--seed',1201,'--fixture','--output',f/'capture']))
    stages.append(run('fixture_score',['score','--input',f/'capture','--output',f/'score']))
    stages.append(run('fixture_replay',['capture','--seed',1201,'--fixture','--output',f/'replay']))
    stages.append(run('fixture_compare',['compare','--input',f/'capture','--right',f/'replay','--output',f/'EXACT_REPLAY.json']))
    cap=json.loads((f/'capture/CAPTURE.json').read_text());sv=json.loads((f/'score/VERIFICATION.json').read_text())
    write(f/'INTEGRATION_PASS.json',{'status':'PASS_END_TO_END_INTEGRATION','conditions':cap['cells'],'frames':len(cap['chunks']),'query_chains':cap['chains'],'logical_stage_evaluations':cap['logical_stage_evaluations'],'seed':1201,'split':'development','cases_per_non_lifecycle_condition':4,'readers':'saved main seed1201 exports plus inherited and exact controls','source_lock_sha256':LOCK,'not_added_to_main_workload':True,'new_optimizer_updates':0})
    for phase in ['capture','score','replay','compare']:
        t=time.monotonic();jobs=[]
        for seed in range(1201,1206):
            base=ROOT/'results/main'/f'seed{seed}';base.mkdir(parents=True,exist_ok=True)
            if phase in ['capture','replay']:args=['capture','--seed',seed,'--output',base/phase]
            elif phase=='score':args=['score','--input',base/'capture','--output',base/'score']
            else:args=['compare','--input',base/'capture','--right',base/'replay','--output',base/'EXACT_REPLAY.json']
            jobs.append((f'{phase}_{seed}',args))
        receipts=pool(jobs);stages.extend(receipts)
        write(ROOT/'results'/f'PHASE_{phase.upper()}.json',{'status':'PASS','phase':phase,'utc':utc(),'wall_seconds':time.monotonic()-t,'workers':receipts,'concurrency_limit':2})
    write(ROOT/'results/EXECUTION_COMPLETE.json',{'status':'ALL_FIVE_MAIN_CAPTURES_SCORED_AND_REPLAYED','start_elapsed_seconds':time.monotonic()-start,'end_utc':utc(),'new_optimizer_updates':0,'source_lock_sha256':LOCK,'worker_receipts':stages})
except BaseException as e:
    import traceback
    write(ROOT/'failures/SUPERVISOR_FAILURE.json',{'utc':utc(),'error':repr(e),'traceback':traceback.format_exc(),'wall_seconds':time.monotonic()-start,'completed_worker_receipts':stages});raise
