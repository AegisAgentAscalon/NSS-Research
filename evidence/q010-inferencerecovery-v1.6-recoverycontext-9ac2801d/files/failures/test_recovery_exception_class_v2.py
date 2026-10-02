from pathlib import Path
import sys,json,tempfile,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
sys.path[:0]=[str(ROOT/'recovery'),str(ROOT/'source'),str(STAGE/'implementation_A'),str(STAGE/'verification_B')]
import numpy as np,torch
from inference_loader import inspect_exports,load_readers,deny_training,sha,read
from q010v.pointer_math import replay_and_audit_pointer_read as amended
from q010v.pointer_math_frozen import replay_and_audit_pointer_read as frozen
from q010v.pointer_math import ReaderMathAuditError

torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);deny_training()
rows=[]
def rejected(name,fn):
    try:fn()
    except (ValueError,RuntimeError,FileNotFoundError,ReaderMathAuditError) as e:rows.append({'test':name,'status':'PASS_EXPECTED_REJECTION','error':str(e)});return
    raise AssertionError('negative case accepted: '+name)
audit=inspect_exports();assert len(audit['models'])==15
(ROOT/'audit/SAVED15_CURRENT.json').write_text(json.dumps(audit,indent=2)+'\n')
for seed in range(1201,1206):
    models,ids=load_readers(seed);assert len(models)==6 and all(not p.requires_grad for m in models.values() if m is not None for p in m.parameters())
rows.append({'test':'all15_plus_inherited_readers_loaded_frozen','status':'PASS'})
rejected('unknown_main_seed',lambda:load_readers(91401))
rejected('optimizer_construction_forbidden',lambda:torch.optim.AdamW([torch.tensor([1.])]))
rejected('backpropagation_forbidden',lambda:torch.autograd.backward(torch.tensor(1.)))

with tempfile.TemporaryDirectory(prefix='q010_neg_') as temp:
    base=Path(temp)
    for test in ['missing_export','duplicate_export','swapped_weights','public_as_strict','recorded_cursor','symlink_export','development_as_main','changed_protocol']:
        root=base/test
        for sub in ['protocol','provenance/saved_main_exports','provenance/saved_main_records']:shutil.copytree(ROOT/sub,root/sub)
        em=root/'provenance/saved_main_exports/WEIGHTS_MANIFEST.json'; manifest=read(em); first=manifest['files'][0];ep=em.parent/first['file']
        if test=='missing_export':ep.unlink()
        elif test=='duplicate_export':manifest['files'][-1]=manifest['files'][0];em.write_text(json.dumps(manifest))
        elif test=='swapped_weights':ep.write_bytes((em.parent/manifest['files'][1]['file']).read_bytes())
        elif test=='public_as_strict':first['strict_sha256']=first['public_sha256'];em.write_text(json.dumps(manifest))
        elif test=='recorded_cursor':
            lp=root/'protocol/ORIGINAL_CHECKPOINT_ROSTER_LOCK.json';lock=read(lp);lr=next(r for r in lock['rows'] if (r['seed'],r['role'])==(first['seed'],first['role']))
            f=root/'provenance/saved_main_records'/lr['manifest'];m=read(f);m['completed_steps']=5999;f.write_text(json.dumps(m));lr['manifest_sha256']=sha(f);lp.write_text(json.dumps(lock))
        elif test=='symlink_export':ep.unlink();ep.symlink_to(ROOT/'provenance/saved_main_exports'/first['file'])
        elif test=='development_as_main':
            lp=root/'protocol/ORIGINAL_CHECKPOINT_ROSTER_LOCK.json';lock=read(lp);lr=next(r for r in lock['rows'] if (r['seed'],r['role'])==(first['seed'],first['role']))
            f=root/'provenance/saved_main_records'/lr['manifest'];m=read(f);m['identity']['config']['fit_role']='development';f.write_text(json.dumps(m));lr['manifest_sha256']=sha(f);lp.write_text(json.dumps(lock))
        elif test=='changed_protocol':
            p=root/'protocol/ORIGINAL_FROZEN_PROTOCOL.json';v=read(p);v['id']='VALIDATION';p.write_text(json.dumps(v))
        rejected(test,lambda root=root:inspect_exports(root))

# Formula-derived test: numerator near the observed subnormal regime, denominator
# close to the documented ratio. Not falsely labelled the absent original raw row.
logits=np.full((1,17),np.float32(-1e4),np.float32);logits[0,0]=0.;logits[0,1]=np.float32(np.log(8.2264172e-46/4.3673753e-46-1.));logits[0,2]=np.float32(np.log(8.2264172e-46))
valid=np.ones((1,16),bool);values=np.zeros((1,16,17),np.float32);values[0,:16,:16]=np.eye(16,dtype=np.float32)
r=amended(logits,values,valid)
old_failure=None
try:frozen(logits,values,valid,captured_weights=r['weights'],captured_pre_norm=r['pre_norm'],captured_read_code=r['read_code'])
except ReaderMathAuditError as e:old_failure=str(e)
if old_failure is None:
    # Search a predeclared grid of subnormal logits/denominators, not task scores.
    for denom in np.linspace(.01,.99,33):
        for z in np.linspace(-103.,-105.,129):
            logits[0,1]=np.float32(np.log(denom));logits[0,2]=np.float32(z)
            r=amended(logits,values,valid)
            try:frozen(logits,values,valid,captured_weights=r['weights'],captured_pre_norm=r['pre_norm'],captured_read_code=r['read_code'])
            except ReaderMathAuditError as e:old_failure=str(e);break
        if old_failure:break
assert old_failure is not None,'failed to reproduce old underflow rejection'
np.savez_compressed(ROOT/'audit/UNDERFLOW_REPRODUCED_FIXTURE.npz',logits=logits,values=values,valid=valid,weights=r['weights'],pre_norm=r['pre_norm'],read_code=r['read_code'])
rows.append({'test':'frozen_rejects_amended_accepts_same_exact_arithmetic','status':'PASS','frozen_rejection':old_failure,'scope':'fresh synthetic reproduction, not the missing original captured row'})
for b in [1,2,7,128]:
    for scale in [0.,1e-8,1.,1e8]:
        l=np.repeat(logits,b,axis=0);v=np.repeat(values*scale,b,axis=0);m=np.repeat(valid,b,axis=0)
        rr=amended(l,v,m);amended(l,v,m,captured_weights=rr['weights'],captured_pre_norm=rr['pre_norm'],captured_read_code=rr['read_code'])
rows.append({'test':'underflow_4_layouts_4_value_scales','status':'PASS','cases':16})
# Near-boundary grid in one batched layout.
grid=np.linspace(-80.,-120.,129,dtype=np.float32);l=np.repeat(logits,len(grid),axis=0);l[:,2]=grid
amended(l,np.repeat(values,len(grid),axis=0),np.repeat(valid,len(grid),axis=0))
rows.append({'test':'underflow_logit_grid','status':'PASS','cases':129})
for name,key in [('weights','weights'),('weighted_values','pre_norm'),('normalized_output','read_code')]:
    kwargs={'captured_weights':r['weights'].copy(),'captured_pre_norm':r['pre_norm'].copy(),'captured_read_code':r['read_code'].copy()}
    dest={'weights':'captured_weights','pre_norm':'captured_pre_norm','read_code':'captured_read_code'}[key];kwargs[dest][0,0]+=np.float32(.001)
    rejected('corrupt_'+name,lambda kw=kwargs:amended(logits,values,valid,**kw))
report={'status':'PASS','checks':len(rows),'rows':rows,'original_raw_rejected_row_available':False,'original_v2_verifier_source_available':False,'prior_rationale_preserved_sha256':sha(ROOT/'protocol/UNDERFLOW_AMENDMENT_ORIGINAL.md'),'frozen_verifier_sha256':sha(ROOT/'source/q010v/pointer_math_frozen.py'),'reconstructed_amended_verifier_sha256':sha(ROOT/'source/q010v/pointer_math.py'),'new_optimizer_updates':0}
(ROOT/'audit/RECOVERY_TESTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
