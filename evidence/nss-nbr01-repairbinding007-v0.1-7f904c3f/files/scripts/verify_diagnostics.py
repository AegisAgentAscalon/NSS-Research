from pathlib import Path
import sys,json,subprocess,os
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from rescore import truth_from_graph

def check(folder):
    folder=Path(folder);j=json.loads((folder/'RESULTS.json').read_text());a=np.load(folder/'arrays.npz',allow_pickle=False);count=0
    for r in j['rows']:
        key=r['key'];pred=a[key+'_'+r['reader']][:,[1,2,4,8].index(r['depth'])]
        target=truth_from_graph(a[key+'_parent'],a[key+'_query']);kn=target!=16;hit=pred==target;room=(pred[:,None]==a[key+'_rooms']).any(-1)
        for name,val in {'accuracy':hit.mean(),'known_accuracy':hit[kn].mean() if kn.any() else None,'unknown_accuracy':hit[~kn].mean() if (~kn).any() else None,'unsupported_room_rate':room[~kn].mean() if (~kn).any() else None}.items():
            assert (r[name] is None and val is None) or (val is not None and abs(val-r[name])<1e-12)
        count+=len(pred)
    return j,count
if __name__=='__main__':
    src=ROOT/'evidence/diagnostics';j,count=check(src)
    replay=ROOT/'evidence/diagnostics_replay'
    with open(ROOT/'evidence/DIAGNOSTIC_REPLAY.log','w') as log:
        subprocess.run([sys.executable,'scripts/diagnostics.py',str(replay)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
    r,n=check(replay);assert j['rows']==r['rows']
    with np.load(src/'arrays.npz',allow_pickle=False) as a,np.load(replay/'arrays.npz',allow_pickle=False) as b:
        assert set(a.files)==set(b.files)
        for name in a:assert np.array_equal(a[name],b[name])
    (ROOT/'evidence/DIAGNOSTICS_VERIFICATION.json').write_text(json.dumps({'status':'PASS','rows':len(j['rows']),'answer_evaluations':count,'state_configurations':j['state_configurations'],'fresh_replay':True,'exploratory':True},indent=2));print('diagnostic replay PASS')
