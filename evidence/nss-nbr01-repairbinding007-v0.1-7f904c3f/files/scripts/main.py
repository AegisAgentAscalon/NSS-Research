"""Run the registered fits/evaluations without mutating inherited sources."""
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def run(cmd,log):
    with open(ROOT/log,'w') as f:
        subprocess.run([sys.executable,*cmd],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,check=True,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
if __name__=='__main__':
    for seed in range(901,906):
        for kind in ('intrinsic_mlp','learned_dictionary'):
            run(['-m','nbr007.train','--kind',kind,'--seed',str(seed),'--steps','1800'],f'evidence/train_{kind}_{seed}.log')
        run(['-m','nbr007.evaluate','--seed',str(seed)],f'evidence/eval_{seed}.log')
