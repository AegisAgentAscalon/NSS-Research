"""Exact fresh-process replay comparator; timing/allocator sizes are not byte invariants."""
from pathlib import Path
import argparse,numpy as np
from common import arrays,load,dump,sha,read_lines,canonical,check_lock
p=argparse.ArgumentParser();p.add_argument('--left',type=Path,required=True);p.add_argument('--right',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
check_lock();n=elements=0;files=0
for rel in ['inputs/inputs.npz']+['capture/'+r['file'] for r in load(a.left/'capture/CAPTURE.json')['chunks']]:
    x,y=arrays(a.left/rel),arrays(a.right/rel)
    if list(x)!=list(y):raise AssertionError('array keys differ '+rel)
    for k in x:
        u,v=x[k],y[k]
        if u.shape!=v.shape or u.dtype!=v.dtype or u.tobytes()!=v.tobytes():raise AssertionError(f'replay mismatch {rel}/{k}')
        n+=1;elements+=u.size
    files+=1
for rel in ['inputs/public.jsonl','inputs/protected.jsonl','inputs/GENERATION.json','capture/routing.jsonl','capture/public_control.jsonl','capture/CAPTURE.json','capture/ATTEMPTS.json']:
    if sha(a.left/rel)!=sha(a.right/rel):raise AssertionError('metadata replay mismatch '+rel)
# Runtime measurements are deliberately fresh; compare only deterministic cost fields.
x=read_lines(a.left/'capture/costs.jsonl');y=read_lines(a.right/'capture/costs.jsonl')
exclude={'route_pair_nanoseconds','python_workspace_bytes','python_string_bytes','python_parsed_fields_bytes','python_journal_bytes','python_directory_and_binding_bytes'}
for u,v in zip(x,y,strict=True):
    if {k:z for k,z in u.items() if k not in exclude}!={k:z for k,z in v.items() if k not in exclude}:raise AssertionError('traffic count replay mismatch')
dump(a.output,{'status':'PASS_EXACT_FRESH_PROCESS_REPLAY','arrays':n,'elements':elements,'array_files':files,'case_event_decision_metadata_exact':True,'noninvariant_cost_fields':sorted(exclude),'replay_is_not_new_sample':True})
print(f'EXACT_REPLAY arrays={n} elements={elements}',flush=True)
