from __future__ import annotations
import argparse,datetime,hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
import psutil

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--id',required=True);p.add_argument('--seconds',type=float,default=300);p.add_argument('--rss-mib',type=float,default=2700);p.add_argument('--cwd',type=Path);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
out=a.root/a.id;out.mkdir(parents=True,exist_ok=False)
r={'id':a.id,'command':cmd,'cwd':str(a.cwd or Path.cwd()),'start_utc':utc(),'seconds_cap':a.seconds,'rss_mib_cap':a.rss_mib,'resource_scope':'sum RSS of monitored process plus descendants, sampled0.2s; cgroup also recorded','status':'RUNNING'}
(out/'start.json').write_text(json.dumps(r,indent=2))
t=time.perf_counter();peak=0;reason=None;count=0;cgpeak=0
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
 proc=subprocess.Popen(cmd,cwd=a.cwd,stdout=stdout,stderr=stderr,start_new_session=True);ps=psutil.Process(proc.pid)
 while proc.poll() is None:
  try:
   rss=sum(x.memory_info().rss for x in [ps]+ps.children(recursive=True) if x.is_running());peak=max(peak,rss)
   cgpeak=max(cgpeak,int(Path('/sys/fs/cgroup/memory.current').read_text()))
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  if time.perf_counter()-t>a.seconds:reason='wall_cap'
  if peak>a.rss_mib*2**20:reason='process_tree_rss_cap'
  if reason:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
   break
  time.sleep(.2);count+=1
 rc=proc.wait()
r.update(end_utc=utc(),elapsed_seconds=time.perf_counter()-t,returncode=rc,peak_process_tree_rss_bytes=peak,cgroup_memory_current_peak=cgpeak,samples=count,stop_reason=reason,status='PASS' if rc==0 and reason is None else 'FAILED_OR_STOPPED')
for name in ['stdout.log','stderr.log']:r[name+'_sha256']=hashlib.sha256((out/name).read_bytes()).hexdigest()
(out/'receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
