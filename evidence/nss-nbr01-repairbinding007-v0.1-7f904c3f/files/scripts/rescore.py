"""Independent NumPy/Python scorer: no model, evaluator or generator imports."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def truth_from_graph(parent,query):
    result=[];n=parent.shape[1]-1
    for edges,start in zip(parent,query):
        u=int(start);visited=set()
        while True:
            if u==n:result.append(n);break
            if u in visited:result.append(n);break
            visited.add(u);v=int(edges[u])
            if u==v:result.append(u);break
            u=v
    return np.array(result)
def rescore(folder,out):
    total=0;count=0;files=[];identities=0
    for path in sorted(Path(folder).glob('pair_*.json')):
        j=json.loads(path.read_text());a=np.load(path.with_suffix('.npz'),allow_pickle=False)
        for r in j['rows']:
            key=r['key'];col=[1,2,4,8].index(r['depth']);pred=a[key+'_'+r['reader']][:,col]
            target=truth_from_graph(a[key+'_parent'],a[key+'_query']);n=a[key+'_parent'].shape[1]-1
            kn=target!=n;hit=pred==target;room=np.any(pred[:,None]==a[key+'_rooms'],axis=1)
            metrics={'accuracy':hit.mean(),'known_accuracy':hit[kn].mean() if kn.any() else None,'unknown_accuracy':hit[~kn].mean() if (~kn).any() else None,'unsupported_room_rate':room[~kn].mean() if (~kn).any() else None,'unresolved_rate':((pred!=n)&~room).mean()}
            for name,v in metrics.items():
                if v is None:assert r[name] is None
                else:assert abs(float(v)-r[name])<1e-12,(path,r,name,v)
            total+=len(pred);count+=1
        for s in j['states']:
            key=s['key'];live=a[key+'_present']
            for field in ('keys','values'):
                if key+'_target_'+field in a:
                    value=(a[key+'_decoded_'+field]==a[key+'_target_'+field])[live].mean()
                    label='key_identity_accuracy' if field=='keys' else 'value_identity_accuracy'
                    assert abs(value-s[label])<1e-12
                    identities+=int(live.sum())
        digest=hashlib.sha256(path.with_suffix('.npz').read_bytes()).hexdigest();assert digest==j['array_sha256']
        files.append({'file':path.name,'rows':len(j['rows']),'states':len(j['states']),'array_hash':digest})
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    receipt={'status':'PASS','configurations':len(files),'rows':count,'answer_evaluations':total,'stored_identity_checks':identities,'files':files,'scope':'Independent scorer over saved targets/predictions, not external replication or new data.'}
    out.write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',default=str(ROOT/'results'));p.add_argument('--out',default=str(ROOT/'evidence/INDEPENDENT_RESCORING.json'));a=p.parse_args();rescore(a.folder,a.out)
