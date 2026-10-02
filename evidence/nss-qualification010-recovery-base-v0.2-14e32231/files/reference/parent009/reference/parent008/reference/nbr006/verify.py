"""Independent NumPy rescoring from saved integer facts, NOT saved target labels.

This verifier does not import the neural evaluator or its metric/oracle routines.
It reconstructs each terminal answer with per-example Python dictionary walks.
"""
from pathlib import Path
import argparse,json
import numpy as np
from . import common as c

def truths(parent,query):
 n=parent.shape[1]-1;out=[]
 for b,start in enumerate(query):
  graph={int(i):int(v) for i,v in enumerate(parent[b,:n]) if int(v)!=n}
  v=int(start);seen=[]
  for _ in range(n+1):
   if v not in graph or v in seen:
    v=n;break
   nxt=graph[v]
   if nxt==v:break
   seen.append(v);v=nxt
  else:v=n
  out.append(v)
 return np.array(out)

def rescore(path):
 path=Path(path);doc=json.loads(path.read_text());npz=path.with_suffix('.npz')
 assert c.sha(npz)==doc['prediction_sha256']
 cells=0;answers=0
 with np.load(npz,allow_pickle=False) as a:
  for row in doc['rows']:
   key=row['key'];p=a[key+'_parent'];q=a[key+'_query'];rooms=a[key+'_rooms'];j=[1,2,4,8].index(row['depth']);pred=a[key+'_pred'][:,j];target=truths(p,q);n=p.shape[1]-1
   known=target!=n;missing=~known;room=np.any(pred[:,None]==rooms,axis=1);unresolved=(pred!=n)&~room
   fields={'answer_accuracy':float(np.mean(pred==target)),'known_accuracy':float(np.mean(pred[known]==target[known])) if known.any() else None,'unknown_accuracy':float(np.mean(pred[missing]==target[missing])) if missing.any() else None,'unsupported_room_rate':float(room[missing].mean()) if missing.any() else None,'unresolved_rate':float(unresolved.mean())}
   for k,v in fields.items():
    if v is None:assert row[k] is None
    else:assert abs(row[k]-v)<1e-12,(path,row,k,v)
   cells+=1;answers+=len(pred)
 return {'file':path.name,'rows':cells,'answer_evaluations':answers,'status':'PASS'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--dir',required=True);p.add_argument('--out',required=True);a=p.parse_args();entries=[rescore(x) for x in sorted(Path(a.dir).glob('*.json'))];c.dump(a.out,{'status':'PASS','configurations':len(entries),'rows':sum(x['rows'] for x in entries),'answer_evaluations':sum(x['answer_evaluations'] for x in entries),'entries':entries});print('PASS',len(entries),'configurations')
