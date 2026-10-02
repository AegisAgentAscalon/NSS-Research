"""Independent scoring from the declared SOURCE EVENTS, plus optional full replay.
Does not trust stored target arrays or precomputed accuracy totals.
"""
import sys,json,argparse,tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.util import write_json,sha,array_digest

def golden(row,n=64):
    base=np.arange(n)%8;y=np.full((n,4),8,dtype=np.uint8);y[:,1]=base;y[:,2]=(base+3)%8
    case=row['case']
    if case=='lifecycle':
        phase=row['phase']
        if phase in ['first_write','correction','rewritten']:y[:,0]=(base+{'first_write':1,'correction':2,'rewritten':4}[phase])%8
    elif case=='global_clear':y[:]=8
    elif case=='extended_write':y[:,0]=(base+2)%8
    elif case in ['presence_chronic_rewrite','fault_repaired_by_events']:y[:,1]=(base+5)%8
    elif case=='write_delivery':y[:,0]=(base+1)%8
    elif case not in ['extended_empty','presence_chronic','state_fault']:raise ValueError(case)
    return y

def verify_file(path):
    d=json.loads(path.read_text());npz=path.with_suffix('.npz');count=0;trace_answers=0
    with np.load(npz,allow_pickle=False) as z:
        assert d['array_digest']==array_digest(*[z[k] for k in sorted(z.files)])
        for row in d['rows']:
            key=row['prediction_key'];p=z[key];y=golden(row,len(p));e=z[key+'_exist'].astype(bool)
            assert np.array_equal(y,z[key+'_target']),(path,key,'target is not source-consistent')
            expected={}
            for name,mask in [('known',y<8),('unknown',y==8)]:
                expected[name+'_n']=int(mask.sum());expected[name+'_accuracy']=float((p[mask]==y[mask]).mean()) if mask.any() else None
            expected['focus_accuracy']=float((p[:,0]==y[:,0]).mean());expected['existence_accuracy']=float((e==(y<8)).mean())
            expected['present_unreadable_fraction']=float((e&(p==8)).mean())
            for k,v in expected.items():
                assert (v is None and row[k] is None) or abs(v-row[k])<1e-12,(path,key,k,v,row[k])
            count+=p.size
            if row['case']=='lifecycle' and row['round']>0:
                phase_idx=['empty','first_write','correction','cleared','rewritten'].index(row['phase']);ok=np.ones(len(p),dtype=bool)
                for ph in range(phase_idx+1):
                    k=f'trace_life_{int(row["sigma"]*1000)}_{ph}';phase=['empty','first_write','correction','cleared','rewritten'][ph]
                    target=golden({'case':'lifecycle','phase':phase},len(p));a=z[k];ex=z[k+'_exist'].astype(bool)
                    if ph==phase_idx:a=a[:row['round']+1];ex=ex[:row['round']+1]
                    ok&=((a==target[None])&(ex==(target<8)[None])).all(axis=(0,2))
                assert abs(ok.mean()-row['all_read_stream_success'])<1e-12
        for tr in d['traces']:
            a=z[tr['key']];y=golden(tr,a.shape[1]);e=z[tr['key']+'_exist'].astype(bool)
            assert np.array_equal(y,z[tr['key']+'_target'])
            exact=float(((a==y[None])&(e==(y<8)[None])).all(axis=(0,2)).mean())
            assert abs(exact-tr['every_read_stream_success'])<1e-12
            assert abs(float((a==y[None]).all(axis=(0,2)).mean())-tr['answer_only_stream_success'])<1e-12
            trace_answers+=a.size
        assert count+trace_answers==d['saved_answer_evaluations']
    return dict(file=path.name,rows=len(d['rows']),snapshot_answers=count,trace_answers=trace_answers,all_targets_rebuilt_from_events=True,npz_sha256=sha(npz))

def replay_one(path,out):
    from nbr01_exist.evaluate import evaluate_one
    d=json.loads(path.read_text());fresh=evaluate_one(ROOT,out,d['seed'],d['mode'])
    for key in ['rows','traces','array_digest','model_digests','local_dynamics','metric_rows','saved_answer_evaluations','raw_state_bytes_per_stream']:
        assert fresh[key]==d[key],(path.name,key)
    with np.load(path.with_suffix('.npz'),allow_pickle=False) as a,np.load(Path(out)/path.with_suffix('.npz').name,allow_pickle=False) as b:
        assert set(a.files)==set(b.files)
        for k in a.files:assert np.array_equal(a[k],b[k]),(path.name,k)
    return path.name

def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--file');p.add_argument('--out',type=Path);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
    paths=[ROOT/'evidence/results'/a.file] if a.file else sorted((ROOT/'evidence/results').glob('*.json'))
    checks=[verify_file(f) for f in paths];replayed=[]
    if a.replay:
        if a.out is None:raise ValueError('Replay output directory required')
        for f in paths:replayed.append(replay_one(f,a.out))
    write_json(a.receipt,dict(status='PASS',configurations=len(paths),checks=checks,replayed=replayed,all_every_read_arrays_scored=True,
        scope='Fresh internal verification, not independent external replication'))
    print('PASS',len(paths),'files;',len(replayed),'full replays')
if __name__=='__main__':main()
