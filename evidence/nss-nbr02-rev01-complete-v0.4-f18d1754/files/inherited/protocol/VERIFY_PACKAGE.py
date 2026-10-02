"""Verify this proposal's bytes and arithmetic. Does not execute any learner."""
from pathlib import Path
import hashlib,json,math
from fractions import Fraction
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
checks=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
for row in manifest['files']:
    p=root/row['path']
    check('exists:'+row['path'],p.is_file())
    b=p.read_bytes()
    check('size:'+row['path'],len(b)==row['bytes'])
    check('hash:'+row['path'],hashlib.sha256(b).hexdigest()==row['sha256'])
p=json.loads((root/'PROTOCOL.json').read_text()); l=json.loads((root/'CALL_AND_RESOURCE_LEDGER.json').read_text()); s=json.loads((root/'SEED_RECIPE.json').read_text())
check('proposal_only',not p['execution_authorized'])
check('dense_parameter_count',16*23+16*16+16+2*16+2==p['model']['parameters'])
check('weight_bytes',p['model']['parameters']*4==2696)
check('eligibility_floats',16*23+16*16+16==640)
check('pending_payload',(640+16+2+32)*4==2760)
check('updates_per_pass',sum(l['per_pass_updates'].values())==4424==l['per_pass_update_total'])
check('update_both',4424*2==8848==l['all_pass_update_total'])
check('update_cap',8848<=9800 and 4424<=4900)
check('reserve',9800-8848==952==l['unallocated_update_reserve'])
check('cell_per_pass',sum(v['cell_examples'] for v in l['per_pass_forwards'].values())==165292)
check('head_per_pass',sum(v['head_vectors'] for v in l['per_pass_forwards'].values())==24196)
check('cell_total',165292*2==330584==l['all_pass_cell_total'])
check('head_total',24196*2==48392==l['all_pass_head_total'])
check('fwd_caps',330584<=400000 and 48392<=60000)
check('backwards',4424+8<=l['backward_cap'] and l['L_autograd_backward_total']==0)
check('raw_allowances',sum(l['uncompressed_component_allowances_MiB'].values())==209 and 209+47==256)
check('heldout_count',8*3*2*5==240)
check('dev_count',4*2*5==40)
check('main_conditions',12*3*2==72)
check('known_new_disjoint',not (set(p['old_cues'])&set(p['development_cues']) or set(p['old_cues'])&set(p['heldout_cues']) or set(p['development_cues'])&set(p['heldout_cues'])))
check('seed_count',len(s['seeds'])==120 and len(set(s['seeds'].values()))==120)
for k,v in s['seeds'].items():
    assert v==int.from_bytes(hashlib.sha256((s['namespace']+'|'+k).encode()).digest()[:8],'big')
check('seed_derivations',True)
check('witness_exact_norm',Fraction(1,4)**2*2+Fraction(1,8)**2+Fraction(1,4)**2+Fraction(1,2)**2+Fraction(1,2)**2+Fraction(7,8)**2==Fraction(47,32))
check('witness_difference',2*Fraction(1,4)**2+Fraction(1,2)**2==Fraction(3,8))
check('witness_ratio',Fraction(3,8)/Fraction(47,32)==Fraction(12,47))
check('witness_threshold',math.sqrt(12/47)>.05 and math.sqrt(47/32)>.001)
check('schema_valid',isinstance(json.loads((root/'FAILURE_RECORD.schema.json').read_text()),dict))
print(json.dumps({'status':'DOCUMENT_BYTES_AND_STATIC_ARITHMETIC_PASS','files':len(manifest['files']),'checks':len(checks),'experiment_executed':False},indent=2))
