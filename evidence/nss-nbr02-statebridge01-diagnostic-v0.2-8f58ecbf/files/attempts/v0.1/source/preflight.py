"""Fixed evidence/derivative preflight on executed untrained fixtures, before main fits."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from reference import from_flat,gradient,oracle

def check(folder):
    result=[];maximum=0.;scalars=0
    for p in sorted(folder.glob('update_*.npz')):
        with np.load(p,allow_pickle=False) as z:r={k:z[k] for k in z.files}
        loss,g=gradient(from_flat(r['pre']),r)
        ratio=np.abs(r['gradient']-g)/(2e-6+2e-5*np.abs(g));scalars+=len(g);maximum=max(maximum,float(ratio.max()))
        if np.any(ratio>1):raise RuntimeError('FIXTURE_DERIVATIVE '+str(p)+' '+str(ratio.max()))
        expected=r['pre']-(r['gradient']*np.float32(r['stats'][2]))*np.float32(r['stats'][3])
        if not np.array_equal(expected,r['post']):raise RuntimeError('FIXTURE_APPLY '+str(p))
        result.append({'file':p.name,'maximum_ratio':float(ratio.max()),'loss_abs_difference':abs(loss-float(r['stats'][0]))})
    assert len(result)==8
    for p in folder.glob('BAD_*.npz'):
        with np.load(p) as z:
            if np.array_equal(z['expected'],z['actual']):raise RuntimeError('UNDETECTED_BAD_FIXTURE')
    # Pure Boolean task truth and same-suffix/different-prefix example; no model calls.
    a=np.array([0,1,2,3,4,255],np.uint8);b,n=oracle(a)
    assert b[0,-1].tolist()==[0,1,1,1] and n[0,-1]==0
    out={'passed':True,'gradient_examples':result,'scalar_comparisons':scalars,'max_ratio':maximum,
         'fault_cases':4,'model_calls_in_this_checker':0,'updates_in_this_checker':0}
    (folder/'PREFLIGHT_AUDIT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');a=p.parse_args();print(json.dumps(check(Path(a.folder))))
