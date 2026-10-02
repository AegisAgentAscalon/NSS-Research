from pathlib import Path
import argparse,json,subprocess,sys,os
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int);ap.add_argument('--out',default=str(ROOT/'evidence/replay'));a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);receipts=[]
    for seed in ([a.seed] if a.seed else range(901,906)):
        with open(out/f'pair_{seed}.log','w') as log:
            subprocess.run([sys.executable,'-m','nbr007.evaluate','--seed',str(seed),'--out',str(out)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
        src=ROOT/'results'/f'pair_{seed}';dst=out/f'pair_{seed}'
        orig=json.loads(src.with_suffix('.json').read_text());again=json.loads(dst.with_suffix('.json').read_text())
        assert orig['rows']==again['rows'];assert orig['states']==again['states'];assert orig['frozen_weight_hashes']==again['frozen_weight_hashes']
        with np.load(src.with_suffix('.npz'),allow_pickle=False) as x,np.load(dst.with_suffix('.npz'),allow_pickle=False) as y:
            assert set(x.files)==set(y.files)
            for key in x:assert np.array_equal(x[key],y[key]),key
            receipts.append({'seed':seed,'rows':len(orig['rows']),'states':len(orig['states']),'arrays':len(x.files),'exact':True})
    (out/'VERIFIED.json').write_text(json.dumps({'status':'PASS','pairs':receipts},indent=2));print('replay PASS',len(receipts))
if __name__=='__main__':main()
