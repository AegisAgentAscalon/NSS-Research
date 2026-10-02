"""Independent scorer: no candidate, dataset generator or evaluator imports."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from result_io import open_result,result_sha

def oracle(parent,start):
    answer=[]
    for edges,node in zip(parent,start):
        seen=set();node=int(node)
        while node!=16:
            if node in seen:node=16;break
            seen.add(node);nxt=int(edges[node])
            if nxt==node:break
            node=nxt
        answer.append(node)
    return np.array(answer)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def rescore(root,out):
    root=Path(root);records=[];membership_rows=state_rows=answers=0
    for path in sorted(root.glob('membership_pair*.json')):
        info=json.loads(path.read_text());npz=path.with_suffix('.npz')
        assert result_sha(npz)==info['array_sha256']
        with open_result(npz) as a:
            for r in info['rows']:
                k=r['key'];prefix=k+'_'+r['method'];pred=a[prefix+'_index'];ac=a[prefix+'_accept'];target=a[k+'_target']
                assert int(ac.sum())==r['accept_n'];assert float((pred==target).mean())==r['correct_identity'];assert float(ac.mean())==r['accepted']
                if r['false_accept'] is not None:assert float(ac.mean())==r['false_accept']
                membership_rows+=1
        records.append({'path':path.name,'rows':len(info['rows']),'sha256':result_sha(npz)})
    for path in sorted(root.glob('state_pair*.json')):
        info=json.loads(path.read_text());npz=path.with_suffix('.npz');assert result_sha(npz)==info['array_sha256']
        with open_result(npz) as a:
            for r in info['rows']:
                k=r['key'];truth=oracle(a[k+'_parent'],a[k+'_query']);known=truth!=16
                pred=a[k+'_'+r['reader']+'_pred'][:,r['depth']-1];room=(pred[:,None]==a[k+'_rooms']).any(-1);hit=pred==truth
                checks={'n':len(pred),'known_n':int(known.sum()),'unknown_n':int((~known).sum()),'correct_n':int(hit.sum()),'known_correct_n':int(hit[known].sum()),'unknown_correct_n':int(hit[~known].sum()),'unsupported_room_n':int(room[~known].sum())}
                for x,v in checks.items():assert r[x]==v,(path,r,x,v)
                state_rows+=1;answers+=len(pred)
            # The inactive-code contract is rechecked against every saved state.
            for case in info['cases']:
                k=case['key'];assert (a[k+'_book'][~a[k+'_active']]==0).all()
                assert not (a[k+'_kr']&~a[k+'_present']).any();assert not (a[k+'_vr']&~a[k+'_present']).any()
        records.append({'path':path.name,'rows':len(info['rows']),'sha256':result_sha(npz)})
    result={'status':'PASS','membership_rows':membership_rows,'state_rows':state_rows,'scored_state_answers':answers,'records':records,'method':'separate graph walk and count checks; no candidate imports; per-hop outputs are correlated'}
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'}));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--out',required=True);a=p.parse_args();rescore(a.results,a.out)
