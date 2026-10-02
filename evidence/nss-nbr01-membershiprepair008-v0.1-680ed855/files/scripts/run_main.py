"""Run fresh confirmatory evaluations only against the local sealed registration."""
from pathlib import Path
import sys,json,subprocess,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import ROOT,sha,dump,utc

def main():
    lock=json.loads((ROOT/'spec/EXECUTION_LOCK.json').read_text())
    for path,digest in lock['files'].items():
        if sha(ROOT/path)!=digest:raise RuntimeError('Execution lock mismatch: '+path)
    start=time.perf_counter();runs=[]
    for pair in range(1,6):
        for module in ('membership_eval','evaluate'):
            log=ROOT/'evidence'/f'MAIN_{module}_{pair}.log'
            cmd=[sys.executable,'-m','nbr008.'+module,'--pair',str(pair),'--out',str(ROOT/'results')]
            with log.open('w') as f:r=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=600)
            runs.append({'pair':pair,'module':module,'returncode':r.returncode,'log':str(log.relative_to(ROOT))})
            dump(ROOT/'evidence/MAIN_PROGRESS.json',{'utc':utc(),'runs':runs,'seconds':time.perf_counter()-start})
            if r.returncode:raise RuntimeError('Main failed; retain partial logs: '+str(log))
            print('FINISHED',pair,module,round(time.perf_counter()-start,2),flush=True)
    dump(ROOT/'evidence/MAIN_COMPLETE.json',{'utc':utc(),'runs':runs,'seconds':time.perf_counter()-start,'lock_sha256':sha(ROOT/'spec/EXECUTION_LOCK.json')})
if __name__=='__main__':main()
