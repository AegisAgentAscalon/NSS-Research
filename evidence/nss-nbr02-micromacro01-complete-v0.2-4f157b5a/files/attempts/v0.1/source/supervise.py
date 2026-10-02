"""Independent parent monitor. Counts memory/time/output and preserves abnormal termination."""
import os,sys,time,json,subprocess,signal
from pathlib import Path
import psutil
root=Path(__file__).resolve().parent.parent
name=sys.argv[1];stage_dir=root/'audit'/('supervisor_'+name);stage_dir.mkdir(exist_ok=True)
start=json.loads((root/'audit/START.json').read_text())['epoch'];reserve=root/'audit/emergency_status.bin'
if not reserve.exists():reserve.write_bytes(b'\0'*1048576)
log=open(stage_dir/'samples.jsonl','w');stdout=open(stage_dir/'stdout.log','w');stderr=open(stage_dir/'stderr.log','w')
env={**os.environ,'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
p=subprocess.Popen([sys.executable,str(root/'source/driver.py'),name],stdout=stdout,stderr=stderr,env=env,start_new_session=True)
peak=0;cp=0;reason=None;lastbytes=0;t0=time.time();ticks=0
while p.poll() is None:
    now=time.time();ticks+=1
    try:
        parent=psutil.Process(p.pid);procs=[parent]+parent.children(recursive=True);rss=sum(q.memory_info().rss for q in procs if q.is_running())
    except psutil.Error:rss=0
    try:cur=int(Path('/sys/fs/cgroup/memory.current').read_text())
    except Exception:cur=0
    if ticks%10==1:lastbytes=sum(x.stat().st_size for x in root.rglob('*') if x.is_file())
    peak=max(peak,rss);cp=max(cp,cur)
    s={'epoch':now,'elapsed_shared':now-start,'process_tree_rss':rss,'container_current':cur,'output_bytes':lastbytes};log.write(json.dumps(s)+'\n');log.flush()
    if now-start>7200:reason='WALL_CAP'
    elif rss>3*1024**3:reason='RSS_CAP'
    elif cur>int(3.5*1024**3):reason='CONTAINER_CAP'
    elif lastbytes>512*1024**2:reason='RAW_CAP'
    hb=root/'raw'/name/'worker/heartbeat.json'
    if hb.exists() and now-hb.stat().st_mtime>240:reason='HEARTBEAT_STALLED'
    if reason:
        incident={'reason':reason,'sample':s,'action':'terminate process group; inspect unmatched intents'}
        reserve.write_bytes(json.dumps(incident).encode().ljust(1048576,b'\0'));os.killpg(p.pid,signal.SIGTERM);break
    time.sleep(.1)
try:code=p.wait(timeout=10)
except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait()
result={'returncode':code,'stop_reason':reason,'peak_process_tree_rss':peak,'peak_container_current':cp,'stage_seconds':time.time()-t0,'shared_seconds':time.time()-start,'sampling_seconds':.1,'pre_supervisor_not_continuously_measured':True}
(stage_dir/'RESULT.json').write_text(json.dumps(result,indent=2));log.close();stdout.close();stderr.close();print(json.dumps(result),flush=True)
