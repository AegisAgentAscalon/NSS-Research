"""Verify this documentation bundle only. No ML/numerical experiment imports."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text()); checked=0
for name,rec in m['files'].items():
 p=root/name
 if not p.is_file():raise SystemExit('Missing payload: '+name)
 b=p.read_bytes()
 if len(b)!=rec['bytes'] or hashlib.sha256(b).hexdigest()!=rec['sha256']:raise SystemExit('Changed payload: '+name)
 checked+=1
l=json.loads((root/'WORK_LEDGER.json').read_text()); checks=[]
def require(name,condition):
 if not condition:raise SystemExit('Static check failed: '+name)
 checks.append(name)
require('contexts',sum(l['contexts_per_pass'].values())==112)
require('applications',sum(l['update_components'].values())==2852==l['updates_per_pass'])
require('heads',sum(l['heads_per_pass_components'].values())==29676==l['heads_per_pass'])
require('fillers',l['filler_only_cells_per_pass']==3360)
require('cells',3*l['heads_per_pass']+l['filler_only_cells_per_pass']==92388==l['cells_per_pass'])
require('backwards',l['G_update_reverse_calls_per_pass']+l['G_diagnostic_reverse_calls_per_pass']+l['old_margin_reverse_calls_per_pass']==3230)
require('QPs',l['qp_learning_and_protection_calls_per_pass']+l['qp_algebraic_fixture_calls_per_pass']==240)
require('support',l['max_support_candidates_per_pass']==l['qp_calls_per_pass']*256)
for name,one in [('updates',l['updates_per_pass']),('cells',l['cells_per_pass']),('heads',l['heads_per_pass']),('reverse_calls',l['all_reverse_calls_per_pass']),('old_margin_reverse_calls',l['old_margin_reverse_calls_per_pass']),('L_focal_gradients',l['L_focal_gradient_evaluations_per_pass']),('qp_calls',l['qp_calls_per_pass'])]:
 require('replay_'+name,l['planned_capture_plus_adaptive_replay'][name]==2*one)
 require('cap_'+name,2*one<=l['proposed_global_hard_caps'][name])
for name,key in [('support_candidates_max','support_candidates'),('svd_calls_max','svd_calls')]:
 require('cap_'+key,l['planned_capture_plus_adaptive_replay'][name]<=l['proposed_global_hard_caps'][key])
s=json.loads((root/'SEED_PLAN.json').read_text());seen=[]
for a in s['allocations']:
 expected=int.from_bytes(hashlib.sha256(('NSS-NBR02-PROTECT01-REVIEW-v0.2/'+a['label']).encode('ascii')).digest()[:8],'big')
 require('seed_'+a['label'],expected==a['seed_uint64'] and expected!=0)
 seen.append(expected)
require('seed_unique',len(seen)==len(set(seen))==s['count']==33)
st=json.loads((root/'STATUS.json').read_text())
require('proposal_only',st['status']=='PROPOSED_FOR_FINAL_REVIEW' and not st['user_execution_authorized'])
for k in ['new_model_loads','new_model_initializations','new_task_stimulus_draws','new_neural_forwards','new_gradients','new_qp_executions','new_optimizer_applications','new_adaptive_replays']:
 require(k,st[k]==0)
require('no_parent_change',not st['parent_architecture_modified'])
for x in json.loads((root/'SOURCE_IDENTITIES.json').read_text())['included_members']:
 b=(root/x['included_as']).read_bytes()
 require('sourcecopy_'+x['included_as'],len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'])
print(json.dumps({'status':'DOCUMENT_CHECKS_PASS','manifest_payloads':checked,'static_checks':len(checks),'scope':'Bytes, integer plans and seed identifiers only; no numerical experiment, solver or feasibility checks'},indent=2))
