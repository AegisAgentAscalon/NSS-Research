"""Bound a current-turn worker; runtime receipts are not scientific equality targets."""
import subprocess,sys,time,json,os
from pathlib import Path
import psutil
root=Path(sys.argv[1]);label=sys.argv[2];command=sys.argv[3:];start=time.monotonic();a=root/'audit';a.mkdir(exist_ok=True)
with (a/(label+'.stdout')).open('wb') as out,(a/(label+'.stderr')).open('wb') as err:
 p=subprocess.Popen(command,stdout=out,stderr=err,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
 peak=container_peak=output_peak=0;reason=None
 while p.poll() is None:
  try:
   proc=psutil.Process(p.pid);rss=sum(q.memory_info().rss for q in [proc]+proc.children(recursive=True));peak=max(peak,rss)
   cp=Path('/sys/fs/cgroup/memory.current');cm=int(cp.read_text()) if cp.exists() else 0;container_peak=max(container_peak,cm)
   size=sum(q.stat().st_size for q in root.rglob('*') if q.is_file());output_peak=max(output_peak,size)
   if rss>3*1024**3 or cm>3.5*1024**3 or size>256*1024**2 or time.monotonic()-start>3600:reason='RESOURCE_STOP';p.terminate();break
  except (psutil.NoSuchProcess,FileNotFoundError):pass
  time.sleep(.2)
 rc=p.wait()
record={'command':command,'returncode':rc,'elapsed_seconds':time.monotonic()-start,'peak_sampled_rss_bytes':peak,'peak_sampled_container_bytes':container_peak,'peak_physical_output_bytes':output_peak,'sampling_seconds':.2,'stop':reason}
(a/(label+'.resource.json')).write_text(json.dumps(record,indent=2));print(json.dumps(record));sys.exit(rc or bool(reason))
