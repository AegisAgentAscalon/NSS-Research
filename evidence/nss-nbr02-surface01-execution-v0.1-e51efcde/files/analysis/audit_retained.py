"""Retained-artifact audit: array rescoring and hashes, zero neural forwards/updates."""
from pathlib import Path
import json, hashlib, numpy as np, torch
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((ROOT/'protocol/EXECUTION_LOCK.json').read_text())
assert all(sha(ROOT/'source'/name)==digest for name,digest in lock['sources'].items())
assert sha(ROOT/'protocol/EXECUTION_PROTOCOL.md')==lock['implementation_protocol_sha256']
out=json.loads((ROOT/'evidence/outcome.json').read_text()); rows=[]
for parent in out['parents']:
    s=parent['seed']; data=np.load(ROOT/f'evidence/admission_{s}.npz');panel=np.load(ROOT/f'fixtures/admission_{s}.npz')
    predictions=np.argmax(data['logits'],axis=2); labels=data['targets']
    for f,name in enumerate(['mixed','idempotent','revision','reset']):
        inds=np.flatnonzero(panel['families']==f); pp=predictions[inds,1:33]; yy=labels[inds,1:33]
        got={'events_correct':int(np.count_nonzero(pp==yy)),'events_total':int(pp.size),
             'whole_correct':sum(bool(np.array_equal(a,b)) for a,b in zip(pp,yy)),
             'histories':len(inds),'false_done':int(np.count_nonzero((pp==8)&(yy!=8)))}
        target=parent['metrics']['32'][name]
        assert all(got[k]==target[k] for k in got)
        rows.append({'seed':s,'family':name,'counts_exact':True})
counts={str(s):sum(1 for _ in open(ROOT/f'logs/parent_{s}_updates.jsonl')) for s in [4101,4102,4103,4104]}
assert all(x==2000 for x in counts.values())
checkpoint_records=[]; parent_bytes=None
for path in sorted((ROOT/'checkpoints').glob('*.pt')):
    p=torch.load(path,map_location='cpu',weights_only=True)
    h=hashlib.sha256()
    for k,v in sorted(p['model'].items()): h.update(k.encode());h.update(v.contiguous().numpy().tobytes())
    assert h.hexdigest()==p['model_hash']
    vals=list(p['model'].values()); model_bytes=sum(v.numel()*v.element_size() for v in vals)
    optimizer_bytes=sum(v.numel()*v.element_size() for state in p['optimizer']['state'].values() for v in state.values() if torch.is_tensor(v)) if p['optimizer'] else 0
    rec={'file':path.name,'sha256':sha(path),'model_tensor_hash_verified':True,'model_parameter_count':sum(v.numel() for v in vals),
         'model_tensor_bytes':model_bytes,'optimizer_tensor_bytes':optimizer_bytes,'checkpoint_file_bytes':path.stat().st_size,'cursor':p['cursor']}
    checkpoint_records.append(rec)
    if path.name=='parent_4103_2000.pt': parent_bytes=rec
assert len(checkpoint_records)==33
confirm=list((ROOT/'fixtures').glob('confirmation*')); assert not confirm
receipt={'status':'PASS','scope':'Retained arrays rescored, source/protocol hashes checked, all retained checkpoint tensor hashes verified. No neural forward or optimizer application.',
         'new_model_forwards':0,'new_optimizer_applications':0,'source_lock_matches':True,'rescore_rows':rows,'parent_update_log_counts':counts,
         'checkpoint_count':len(checkpoint_records),'checkpoints':checkpoint_records,'main_confirmation_files':len(confirm),
         'main_adaptation_checkpoints':len(list((ROOT/'checkpoints').glob('adapt_*'))),'representative_final_parent_memory':parent_bytes,
         'single_task_hidden_state_bytes':64*4,'readout_tensor_bytes':(64*9+9)*4}
(ROOT/'analysis/retained_audit.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['rescore_rows','checkpoints']},indent=2))
