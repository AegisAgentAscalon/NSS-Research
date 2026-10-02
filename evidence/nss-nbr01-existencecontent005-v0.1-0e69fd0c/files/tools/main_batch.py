"""Run bounded jobs in fresh interpreters; completed artifacts are immutable."""
import sys,subprocess,concurrent.futures,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def job(args,log):
    with open(log,'w') as f:
        r=subprocess.run([sys.executable,*args],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError(f'Worker failed: {args}; see {log}')
    return str(log)
if __name__=='__main__':
    stage=sys.argv[1];jobs=[]
    if stage=='train':
        for rep in range(301,306):
            for kind in ['split1','split4','coupled17']:
                jobs.append(([str(ROOT/'tools/train_worker.py'),kind,str(rep),str(rep+400),'--out',str(ROOT/'evidence/main')],ROOT/'evidence/main'/f'{kind}_rep{rep}.log'))
    elif stage=='eval':
        for rep in range(301,306):
            for mode in ['historical','protected','nearest','split1','split4','coupled17','fixed1','fixed4','hold1']:
                jobs.append(([str(ROOT/'tools/eval_worker.py'),mode,str(rep),'--out',str(ROOT/'evidence/results')],ROOT/'evidence/results'/f'{mode}_rep{rep}.log'))
    else:raise ValueError(stage)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(lambda pair:job(*pair),jobs):print(result,flush=True)
