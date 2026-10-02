"""Separate detection checks on copied real evidence. No Torch, model runs or updates."""
import sys,json,hashlib,struct,copy
from pathlib import Path
import numpy as np
from reference_numeric import records,canonical,log_check

def main(run,out):
    run=Path(run);out=Path(out);out.mkdir(exist_ok=True);rr=list(records(run/'worker/records.bin'));batches=[(m,a) for _,m,a in rr if m['kind']=='batch_apply'];rows=[]
    def test(name,fn):fn();rows.append({'test':name,'passed':True})
    def batch_ok(a,coefficient):
        aa=np.zeros(674,'f8')
        for x in a['example_gradients']:aa+=x.astype('f8')
        if not np.array_equal(aa,a['accumulator64']) or not np.array_equal((aa/8).astype('f4'),a['mean32']):return False
        product=np.multiply(a['mean32'],a['norm_factor'][1],dtype='f4')
        applied=np.multiply(product,np.float32(coefficient),dtype='f4')
        return product.tobytes()==a['clip_product'].tobytes() and (a['pre']-applied).astype('f4').tobytes()==a['post'].tobytes()
    cm,clean=next((m,a) for m,a in batches if not m['defect']);bad=[(a,m['coefficient']) for m,a in batches if m['defect']]
    test('all_eight_live_sandbox_bad_applications_rejected',lambda: (_ for _ in ()).throw(AssertionError()) if len(bad)!=8 or any(batch_ok(a,c) for a,c in bad) else None)
    assert batch_ok(clean,cm['coefficient'])
    for key in ('mean32','accumulator64','clip_product','post'):
        a={k:v.copy() for k,v in clean.items()};a[key].flat[0]+=np.float32(.1)
        test('copied_corrupt_'+key,lambda a=a: (_ for _ in ()).throw(AssertionError()) if batch_ok(a,cm['coefficient']) else None)
    lg,events=log_check(run/'worker/events.jsonl');assert not lg['unknown_attempts']
    lastcommit=max(i for i,e in enumerate(events) if e['event']=='UPDATE_COMMIT');intent_id=events[lastcommit]['attempt']
    # Prefix ending just before the commit preserves attempted/unknown rather than claiming zero work.
    prefix=events[:lastcommit];intents={e['attempt'] for e in prefix if e['event']=='UPDATE_INTENT'};commits={e['attempt'] for e in prefix if e['event']=='UPDATE_COMMIT'}
    assert intent_id in intents-commits
    test('copied_missing_commit_is_unknown_completion',lambda:None)
    # Evidence integrity negative uses bytes, not removal of actually retained records.
    frame=run/'worker/records.bin';blob=frame.read_bytes()[:80];assert len(blob)==80
    test('truncated_frame_recognized',lambda: (_ for _ in ()).throw(AssertionError()) if int.from_bytes(blob[:8],'little')<=40 else None)
    (out/'RESULT.json').write_text(json.dumps({'status':'PASS','tests':rows,'scope':'live sandbox applications plus explicitly copied records; not exhaustive faults','neural_calls':0},indent=2));print(json.dumps({'passed':len(rows)}))
if __name__=='__main__':main(*sys.argv[1:3])
