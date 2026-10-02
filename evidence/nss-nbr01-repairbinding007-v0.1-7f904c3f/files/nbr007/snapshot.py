"""Complete research snapshots; not a production multi-file crash transaction."""
import json
from pathlib import Path
import numpy as np
import torch
from nbr006 import common as c
ABI='nbr007-compatible-records-v1'
FIELDS=('keys','values','present','book','query')
def save(path,keys,values,present,book,query,rng,identities,scope,rounds=0):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    arrays=dict(zip(FIELDS,[x.detach().cpu().numpy() for x in (keys,values,present,book,query)]))
    validate(arrays)
    if not scope or not isinstance(rounds,int) or not 0<=rounds<=8:raise ValueError('Invalid scope/round')
    np.savez_compressed(p,**arrays)
    c.dump(p.with_suffix('.json'),{'abi':ABI,'scope':scope,'rounds':rounds,'identities':identities,'rng':rng.bit_generator.state,'sha256':c.sha(p)})
def validate(a):
    k,v,e,b,q=[a[n] for n in FIELDS]
    if k.ndim!=3 or k.shape[-1]!=17 or v.shape!=k.shape or e.shape!=k.shape[:2] or b.ndim!=3 or b.shape[0]!=len(k) or b.shape[-1]!=17 or q.shape!=(len(k),17):raise ValueError('Incompatible shapes')
    if e.dtype!=np.bool_ or any(x.dtype!=np.float32 for x in (k,v,b,q)):raise ValueError('Incompatible dtype')
    if any(not np.isfinite(x).all() for x in (k,v,b,q)):raise ValueError('Nonfinite state')
    if np.any(k[~e]) or np.any(v[~e]):raise ValueError('Empty slot is not cleared')
def load(path,identities,scope):
    p=Path(path);m=json.loads(p.with_suffix('.json').read_text())
    if m['abi']!=ABI or m['scope']!=scope or m['identities']!=identities or m['sha256']!=c.sha(p):raise ValueError('Snapshot compatibility/integrity mismatch')
    if not isinstance(m['rounds'],int) or not 0<=m['rounds']<=8:raise ValueError('Invalid round')
    with np.load(p,allow_pickle=False) as z:a={n:z[n].copy() for n in FIELDS}
    validate(a);rng=np.random.default_rng();rng.bit_generator.state=m['rng']
    return tuple(torch.from_numpy(a[n]) for n in FIELDS),rng,m['rounds']
