from pathlib import Path
import argparse,sys,json,subprocess,time,os
import numpy as np
from result_io import open_result
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import ROOT,dump,sha,utc

def compare(old,new):
    with open_result(old) as a,open_result(new) as b:
        assert set(a.files)==set(b.files),(old,'array set')
        for k in a.files:
            assert np.array_equal(a[k],b[k]),(old,k,'prediction/state/feature replay mismatch')
        return len(a.files)

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',required=True);a.add_argument('--pairs',default='1,2,3,4,5');p=a.parse_args();out=Path(p.out);out.mkdir(parents=True,exist_ok=True);records=[];start=time.perf_counter()
    for pair in map(int,p.pairs.split(',')):
        for module,prefix in [('membership_eval','membership'),('evaluate','state')]:
            with (out/f'{prefix}_{pair}.log').open('w') as f:
                rc=subprocess.run([sys.executable,'-m','nbr008.'+module,'--pair',str(pair),'--out',str(out)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=600).returncode
            if rc:raise RuntimeError('Replay subprocess failed '+prefix)
            file=f'{prefix}_pair{pair}.npz';n=compare(ROOT/'results'/file,out/file)
            original=json.loads((ROOT/'results'/file).with_suffix('.json').read_text());replayed=json.loads((out/file).with_suffix('.json').read_text());assert original['rows']==replayed['rows']
            records.append({'pair':pair,'module':module,'arrays_exact':n,'rows':len(original['rows'])});dump(out/'REPLAY_PROGRESS.json',{'records':records,'seconds':time.perf_counter()-start})
            print('REPLAYED',pair,module,n,flush=True)
    dump(out/'REPLAY_VERIFICATION.json',{'status':'PASS','records':records,'seconds':time.perf_counter()-start,'utc':utc()})
if __name__=='__main__':main()
