#!/usr/bin/env python3
"""Start a NEW local CM-01 reproduction using the frozen protocol; never train.

The original bundle already contains exact replay evidence. This optional driver
was CLI/static checked, not used for an additional full inference run during delivery.
"""
from __future__ import annotations
import argparse,json,os,subprocess,sys,time
from pathlib import Path

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True,help='Extracted Q010_InferenceRecovery_v1.6 folder containing VERIFY_CONTEXT.py')
    p.add_argument('--output',type=Path,required=True,help='New empty output path; existing paths are refused')
    a=p.parse_args();root=Path(__file__).resolve().parent;baseline=a.baseline.resolve(strict=True);out=a.output.resolve()
    if out.exists():raise FileExistsError('Output already exists; preserve earlier evidence and use a new path')
    if not (baseline/'VERIFY_CONTEXT.py').is_file():raise FileNotFoundError('Wrong recovery baseline folder')
    from VERIFY_STUDY import verify
    verify(root)
    import psutil
    out.mkdir(parents=True);start=time.time();receipts=[]
    env=dict(os.environ,CM01_BASELINE=str(baseline),OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    def run(name,*args):
        if time.time()-start>7200:raise TimeoutError('New reproduction two-hour cap')
        peak=0;t=time.time();reason=None
        with (out/(name+'.stdout.log')).open('w') as stdout,(out/(name+'.stderr.log')).open('w') as stderr:
            child=subprocess.Popen([sys.executable,*map(str,args)],stdout=stdout,stderr=stderr,env=env)
            while child.poll() is None:
                processes=[]
                try:
                    parent=psutil.Process(child.pid);processes=[parent]+parent.children(recursive=True)
                    rss=sum(x.memory_info().rss for x in processes if x.is_running())+psutil.Process().memory_info().rss;peak=max(peak,rss)
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                if peak>4*1024**3:reason='4GiB process-tree cap'
                if time.time()-start>7200:reason='two-hour cap'
                if reason:
                    for x in reversed(processes):
                        try:x.kill()
                        except psutil.NoSuchProcess:pass
                    child.kill();break
                time.sleep(.1)
            code=child.wait()
        receipts.append({'stage':name,'returncode':code,'seconds':time.time()-t,'peak_sampled_process_tree_rss_bytes':peak,'stop_reason':reason})
        (out/'REPRODUCTION_STAGES.json').write_text(json.dumps(receipts,indent=2)+'\n')
        if code or reason:raise RuntimeError(f'{name} failed; see retained logs in {out}')
    run('baseline_integrity',baseline/'VERIFY_CONTEXT.py')
    run('contract_tests',root/'source/test_contract.py')
    for kind in ('fixture','main'):
        work=out/kind;work.mkdir()
        run(kind+'_generate',root/'source/generate.py','--kind',kind,'--output',work/'inputs')
        extra=['--fixture'] if kind=='fixture' else []
        run(kind+'_capture',root/'source/capture.py','--input',work/'inputs','--output',work/'capture',*extra)
        run(kind+'_score',root/'source/score.py','--input',work/'inputs','--capture',work/'capture','--output',work/'scores')
        run(kind+'_compare',root/'source/compare.py','--left',root/'raw'/kind/'capture_run','--right',work,'--output',work/'EXACT_REPLAY.json')
    (out/'REPRODUCTION_COMPLETE.json').write_text(json.dumps({'status':'PASS_NEW_LOCAL_REPRODUCTION','elapsed_seconds':time.time()-start,'logical_model_calls':10593,'new_optimizer_updates':0,'not_new_scientific_samples':True},indent=2)+'\n')
    print('Reproduction passed. Evidence:',out)
if __name__=='__main__':main()
