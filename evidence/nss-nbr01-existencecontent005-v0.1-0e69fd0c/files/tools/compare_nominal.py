"""Post-analysis equality checks over already registered test arrays."""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.util import write_json
rows=[]
for seed in range(301,306):
 with np.load(ROOT/'evidence/results'/f'protected_rep{seed}.npz',allow_pickle=False) as ref:
  for mode in ['split1','split4','fixed1','fixed4']:
   with np.load(ROOT/'evidence/results'/f'{mode}_rep{seed}.npz',allow_pickle=False) as cur:
    keys=[f'trace_life_150_{p}{suffix}' for p in range(5) for suffix in ['', '_exist']]
    flags={k:np.array_equal(ref[k],cur[k]) for k in keys}
    rows.append(dict(seed=seed,mode=mode,equal=all(flags.values()),keys=flags))
rare=[]
for seed in range(301,306):
 with np.load(ROOT/'evidence/results'/f'split1_rep{seed}.npz',allow_pickle=False) as f:
  k='trace_presence_150_0';p=f[k];e=f[k+'_exist'].astype(bool);y=f[k+'_target']
  mask=(p==8)&(y[None]==8)&e
  rare.append(dict(seed=seed,masked_false_presence_read_positions=int(mask.sum()),affected_streams=int(mask.any(axis=(0,2)).sum())))
write_json(ROOT/'evidence/NOMINAL_EQUALITY_DIAGNOSTIC.json',dict(status='CHECKED',timing='Post-analysis of registered stored outputs, not a newly tuned test',
    nominal_equality_to_protected=rows,all_nominal_arrays_equal=all(r['equal'] for r in rows),additional_scalar_presence_only_masked_errors=rare))
print('All nominal equality checks:',all(r['equal'] for r in rows),'masked-error streams:',sum(r['affected_streams'] for r in rare))
