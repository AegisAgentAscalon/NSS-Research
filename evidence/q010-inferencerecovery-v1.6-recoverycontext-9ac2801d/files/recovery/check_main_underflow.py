from pathlib import Path
import sys,json,hashlib
import numpy as np,torch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from q010v.pointer_math import replay_and_audit_pointer_read as amended
from q010v.pointer_math_frozen import replay_and_audit_pointer_read as frozen, ReaderMathAuditError

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
torch.set_num_threads(1);torch.set_num_interop_threads(1)
root=R/'results/main/seed1201/capture';found=None
for cell in ['durability_sigma02_no_maintenance_livewrite64','ablation_no_maintenance']:
    cap=json.loads((root/'CAPTURE.json').read_text())
    for ch in reversed([x for x in cap['chunks'] if x['condition']==cell]):
        p=root/ch['file'];meta=json.loads((root/ch['meta']).read_text())
        with np.load(p,allow_pickle=False) as z:raw={k:z[k] for k in z.files}
        valid=raw['state__present']&raw['state__kr']&raw['state__vr'];values=np.where(valid[:,:,None],raw['state__vals'],np.float32(0))
        for role in ['ordinary','near','attention']:
            for step in range(meta['depth']):
                args=(raw[role+'__logits'][:,step],values,valid);kw={'captured_weights':raw[role+'__weights'][:,step],'captured_pre_norm':raw[role+'__weighted_code'][:,step],'captured_read_code':raw[role+'__read_code'][:,step]}
                try:frozen(*args,**kw)
                except ReaderMathAuditError as e:
                    new=amended(*args,**kw)
                    target=R/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz'
                    np.savez_compressed(target,logits=args[0],values=values,valid=valid,**kw)
                    found={'status':'PASS_FROZEN_REJECTION_REPRODUCED_ON_FRESH_MAIN_AND_AMENDED_ACCEPTANCE','seed':1201,'condition':cell,'checkpoint':meta['checkpoint'],'reader':role,'step_zero_based':step,'frozen_rejection':str(e),'unchanged_raw_capture':str(p.relative_to(R)),'unchanged_capture_sha256':sha(p),'fresh_fixture_sha256':sha(target),'batch_size':len(valid),'exact_cpu_replay_unchanged':True,'original_historical_row_recovered':False,'note':'Full128-case batch retained to preserve CPU reduction layout. This is newly regenerated evidence, not the absent historical raw row.'};break
            if found:break
        if found:break
    if found:break
if not found:raise AssertionError('no frozen underflow rejection found in declared main search')
(R/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.json').write_text(json.dumps(found,indent=2)+'\n');print(json.dumps(found,indent=2))
