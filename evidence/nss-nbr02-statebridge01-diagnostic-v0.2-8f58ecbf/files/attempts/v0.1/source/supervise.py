"""Bounded foreground child with periodically sampled process and container resources."""
import argparse,json,os,subprocess,time
from pathlib import Path
import psutil
P=argparse.ArgumentParser();P.add_argument('--name',required=True);P.add_argument('cmd',nargs=argparse.REMAINDER);a=P.parse_args()
root=Path(__file__).resolve().parents[1];cfg=json.loads((root/'protocol/CONFIG.json').read_text())
origin=json.loads((root/'audit/ORIGIN.json').read_text())['unix_time'];cmd=a.cmd[1:] if a.cmd[:1]==['--'] else a.cmd
log=open(root/'logs'/f'{a.name}.log','wb');p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','PYTHONHASHSEED':'0'})
peak=0;cmpeak=0;reason=None;sample=open(root/'audit'/f'{a.name}_resources.jsonl','w');tick=0
while p.poll() is None:
    try:
        ps=psutil.Process(p.pid);rss=ps.memory_info().rss+sum(c.memory_info().rss for c in ps.children(recursive=True) if c.is_running());peak=max(peak,rss)
    except psutil.Error:rss=0
    try:cm=int(Path('/sys/fs/cgroup/memory.current').read_text());cmpeak=max(cmpeak,cm)
    except OSError:cm=0
    age=time.time()-origin
    if rss>cfg['process_rss_cap']:reason='PROCESS_RSS_LIMIT'
    if cm>cfg['container_cap']:reason='CONTAINER_MEMORY_LIMIT'
    if age>cfg['time_cap_seconds']:reason='SHARED_TIME_LIMIT'
    if tick%5==0:
        total=sum(q.stat().st_size for d in ['primary','replay'] for q in (root/d).rglob('*') if q.is_file())
        if total>cfg['retained_bytes_cap']:reason='RETAINED_BYTES_LIMIT'
        sample.write(json.dumps({'elapsed':age,'rss':rss,'container':cm,'run_bytes':total})+'\n');sample.flush()
    if reason:
        for c in psutil.Process(p.pid).children(recursive=True):c.terminate()
        p.terminate();break
    tick+=1;time.sleep(.2)
rc=p.wait();sample.close();log.close()
receipt={'command':cmd,'returncode':rc,'stop':reason,'peak_sampled_process_rss':peak,'peak_sampled_container':cmpeak,'elapsed_since_origin':time.time()-origin,'sampling_seconds':.2}
(root/'audit'/f'{a.name}_supervisor.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
raise SystemExit(rc if rc else (2 if reason else 0))
