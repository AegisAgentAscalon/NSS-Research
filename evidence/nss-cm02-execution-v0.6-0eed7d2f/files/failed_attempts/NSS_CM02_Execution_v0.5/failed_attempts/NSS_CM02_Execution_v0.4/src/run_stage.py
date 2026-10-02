"""Resource-supervised synchronous subprocess runner. Hard stops retain logs and receipts."""
from __future__ import annotations
import argparse,os,subprocess,sys,time
from pathlib import Path
import psutil
from io_utils import ROOT,load,dump

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('command',nargs=argparse.REMAINDER);a=ap.parse_args()
    command=a.command[1:] if a.command and a.command[0]=='--' else a.command
    start=load(ROOT/'audit/SESSION_START.json')['budget_start_unix'];stage=time.time();root=psutil.Process();env=dict(os.environ,PYTHONHASHSEED='0',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    (ROOT/'logs').mkdir(exist_ok=True);failure=None;peak=0;cgpeak=0;steps=0
    with (ROOT/'logs'/f'{a.name}.stdout.log').open('w') as out,(ROOT/'logs'/f'{a.name}.stderr.log').open('w') as err:
        p=subprocess.Popen(command,stdout=out,stderr=err,env=env)
        while p.poll() is None:
            try:processes=[root]+root.children(recursive=True);rss=sum(x.memory_info().rss for x in processes if x.is_running())
            except (psutil.NoSuchProcess,psutil.AccessDenied):rss=0
            cg=int(Path('/sys/fs/cgroup/memory.current').read_text()) if Path('/sys/fs/cgroup/memory.current').exists() else 0
            peak=max(peak,rss);cgpeak=max(cgpeak,cg);steps+=1
            if time.time()-start>7200:failure='two_hour_wall_cap'
            elif rss>3*2**30:failure='process_tree_3_GiB_cap'
            elif cg>int(3.5*2**30):failure='container_3.5_GiB_cap'
            if steps%20==0:
                size=sum(x.stat().st_size for x in ROOT.rglob('*') if x.is_file())
                if size>256*2**20:failure='output_256_MiB_cap'
            if failure:
                for child in root.children(recursive=True):
                    try:child.kill()
                    except psutil.NoSuchProcess:pass
                break
            time.sleep(.05)
        code=p.wait()
    totalattempt=0
    for f in list((ROOT/'raw').rglob('ATTEMPTS.json'))+list((ROOT/'failed_attempts').rglob('ATTEMPTS.json')):
        try:totalattempt+=load(f).get('attempted',0)
        except (ValueError,OSError):pass
    if totalattempt>6000:failure='attempted_forward_6000_cap'
    receipt={'stage':a.name,'command':command,'returncode':code,'status':'PASS' if not failure and code==0 else 'FAILED_STOP','failure':failure,
          'stage_wall_seconds':time.time()-stage,'shared_wall_seconds':time.time()-start,'sampled_process_tree_peak_rss_bytes':peak,'sampled_cgroup_peak_bytes':cgpeak,
          'poll_interval_seconds':.05,'samples':steps,'total_recorded_attempted_forwards':totalattempt,'thread_environment':{k:env[k] for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','PYTHONHASHSEED')}}
    dump(ROOT/'audit'/f'{a.name}.json',receipt);print(receipt,flush=True)
    print((ROOT/'logs'/f'{a.name}.stdout.log').read_text()[-15000:]);error=(ROOT/'logs'/f'{a.name}.stderr.log').read_text()
    if error:print(error[-16000:],file=sys.stderr)
    if code!=0 or failure:sys.exit(1)
if __name__=='__main__':main()
