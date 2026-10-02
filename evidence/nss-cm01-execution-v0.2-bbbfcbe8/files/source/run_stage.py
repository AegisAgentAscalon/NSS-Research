"""Synchronous stage supervisor with shared elapsed-time and process-tree RSS caps."""
from __future__ import annotations
import argparse,os,subprocess,sys,time,traceback
from pathlib import Path
import psutil
from common import ROOT,dump,load
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
if not a.command:raise ValueError('command required')
start=load(ROOT/'audit/SESSION_START.json')['budget_start_epoch'];t0=time.time();cap=4*1024**3
log=ROOT/'logs'/f'{a.name}.log';err=ROOT/'logs'/f'{a.name}.stderr.log'
if log.exists():raise FileExistsError('stage must have a new name; retain earlier failures')
peak=0;reason=None
with log.open('w') as out,err.open('w') as stderr:
    env=dict(os.environ,OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    child=subprocess.Popen(a.command,stdout=out,stderr=stderr,env=env,cwd=ROOT)
    while child.poll() is None:
        try:
            procs=[psutil.Process(child.pid)]+psutil.Process(child.pid).children(recursive=True)
            rss=sum(p.memory_info().rss for p in procs if p.is_running())+psutil.Process(os.getpid()).memory_info().rss
            peak=max(peak,rss)
        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
        if peak>cap:reason='4GiB_process_tree_RSS_cap'
        if time.time()-start>7200:reason='two_hour_shared_clock_cap'
        if reason:
            for proc in reversed(procs):
                try:proc.kill()
                except psutil.NoSuchProcess:pass
            break
        time.sleep(.1)
    code=child.wait()
receipt={'name':a.name,'command':a.command,'returncode':code,'status':'PASS' if code==0 and reason is None else 'FAIL','stop_reason':reason,
         'started_epoch':t0,'ended_epoch':time.time(),'stage_seconds':time.time()-t0,'shared_elapsed_seconds':time.time()-start,
         'peak_sampled_process_tree_rss_bytes':peak,'sampling_interval_seconds':.1,'optimizer_updates':0}
dump(ROOT/'audit'/f'{a.name}.json',receipt)
print(log.read_text()[-20000:]);print(err.read_text()[-12000:]);print(receipt,flush=True)
if code!=0 or reason:raise SystemExit(code if code else 1)
