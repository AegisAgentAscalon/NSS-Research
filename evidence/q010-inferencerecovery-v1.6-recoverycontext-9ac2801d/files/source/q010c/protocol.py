"""Predeclared scientific scope and host budget for a new Q010 execution identity."""
from __future__ import annotations
import hashlib,json,sys,datetime
from pathlib import Path
from typing import Any
from q010r.conditions import condition_cells
from q010r import evaluation as ev,training
import scoring
VERSION='NSS_NBR01_Q010_InfrastructureRepair_v1.3'
ROOT=Path(__file__).resolve().parents[2]
STAGING=ROOT/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
ARMS=(('ordinary','ordinary_continuation'),('near','close_identity_continuation'),('attention','task_adapted_attention'))
SEEDS=tuple(range(1201,1206))
CLASSES=('supported','under_depth','observable_missing','unobservable_missing','lifecycle_absence','preexisting_unknown')
ROLES=('inherited','cap_only','ordinary','near','attention','exact_owner')
CHECKPOINTS=tuple(range(0,1025,64))
ABSENT_PHASES={'pre_registration_query','registration_without_fact','clear','scope_reset'}

def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()

def canonical(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(v:Any)->str:return hashlib.sha256(canonical(v)).hexdigest()
def roster(seed:int)->dict[str,str]:return {f'inherited_{seed-400}':'inherited','cap_only':'cap_only','ordinary':'ordinary','near':'near','attention':'attention','exact_owner':'exact_owner'}
def seed_plan(seed:int,arm:str)->dict[str,int|None]:
 def d(purpose,arm_tag):return training.derive_seed(protocol_version=VERSION,split='training',purpose=purpose,paired_seed=seed,arm=arm_tag)
 return {'sampler_seed':d('sampler',''),'training_torch_seed':d('training_torch',arm),'model_init_seed':d('model_init',arm) if arm=='task_adapted_attention' else None,'global_torch_seed':d('global_torch',arm)}

def counts_for(cell)->dict[str,int]:
 counts={k:0 for k in CLASSES};f=cell.factors
 if cell.stratum=='lifecycle':counts['lifecycle_absence' if cell.condition_id in ABSENT_PHASES else 'supported']=1;return counts
 n=cell.episodes_per_seed;length=int(f.get('path_length',3));depth=int(f.get('allowed_depth',min(length,4)))
 if f.get('feedback_mode','assisted')=='direct':depth=1
 mult=len(f.get('evaluation_checkpoints',[0]))
 if f.get('query_kind') in ('novel','near_novel'):counts['preexisting_unknown']=n*mult;return counts
 n_supported=int(cell.balance.get('supported',cell.balance.get('known',n)))
 counts['supported' if depth>=length else 'under_depth']=n_supported*mult
 for i in range(n_supported,n):counts['observable_missing' if (i-n_supported)%length+1<=depth else 'unobservable_missing']+=mult
 return counts

def build_criteria()->dict[str,Any]:
 cells=condition_cells();matrix=STAGING/'plan/condition_matrix.json';out={'schema_version':2,'criteria_id':VERSION+'-criteria-v1','status':'frozen','matrix_sha256':sha(matrix),'coverage':{'condition_ids':[c.condition_id for c in cells],'paired_seed_ids':list(SEEDS),'reader_roles_by_seed':{str(s):roster(s) for s in SEEDS},'chains_per_condition_seed_reader':{}},'conditions':{}}
 for c in cells:
  checkpoints=list(c.factors.get('evaluation_checkpoints',[]));n=c.episodes_per_seed*max(1,len(checkpoints));counts=counts_for(c)
  out['coverage']['chains_per_condition_seed_reader'][c.condition_id]={str(s):{r:n for r in roster(s)} for s in SEEDS}
  role_rules={}
  for role in ROLES:
   role_rules[role]={}
   for cls in CLASSES:
    threshold=scoring._expected_threshold(c.condition_id,role,cls)
    role_rules[role][cls]={'disposition':'diagnostic_only'} if threshold is None else {'disposition':'accuracy','metric':'accuracy','operator':'>=','threshold':threshold}
  rule={'answer_contract':'live_facts' if c.stratum=='lifecycle' else 'task_truth','feedback_mode':'direct' if c.stratum=='lifecycle' or c.condition_id=='core_direct_visible_fact' else 'assisted','role_rules':role_rules,'expected_class_counts_by_seed_reader':{str(s):{r:dict(counts) for r in roster(s)} for s in SEEDS}}
  if checkpoints:
   one={k:v//len(checkpoints) for k,v in counts.items()}
   rule['checkpoint_grid']={'checkpoint_values':checkpoints,'streams_per_checkpoint':128,'stream_ids_by_seed':{str(s):[ev._case_id(c.condition_id,s,i,'paired_eval') for i in range(128)] for s in SEEDS},'expected_class_counts_by_seed_reader_checkpoint':{str(s):{r:{str(cp):dict(one) for cp in checkpoints} for r in roster(s)} for s in SEEDS}}
  out['conditions'][c.condition_id]=rule
 scoring._validate_criteria(out,condition_matrix_sha256=sha(matrix));return out

def protocol_spec()->dict[str,Any]:
 return {'id':VERSION,'status':'PREDECLARATION','input_archive_sha256':'40b3081fc63153c84e758cae950c5756a89b323d85cf3a9b28cc0dd3d18a9aaa','reconstruction_not_original':True,'hypotheses':{'H1':'Fixed-parameter iterative readers combine retained relationships when permitted sufficient stages; state removal and insufficient depth should reduce supported answers.','H2':'Ordinary continuation and task-adapted attention can be judged against fixed core/direct/durability criteria; no candidate is required to pass for an otherwise complete experiment.','H3':'Close-identity preparation may trade supported retrieval against missing-information performance. Report the tradeoff and every seed; no historical outcome is a target.','H4':'Whole-map degradation can occur without a queried answer failure. Count source/map/operation invariants separately from answer accuracy.'},'arms':dict(ARMS),'main_seeds':list(SEEDS),'main_steps_per_fit':6000,'main_fit_count':15,'main_updates':90000,'verification_retraining':{'fits':3,'steps_each':6000,'paired_seed':1201,'same_start_data_rng':True,'artifact_names_distinct':True,'compare':'Exact final tensors, optimizer arrays, per-update losses/gradients/input digests/RNG; wall times and attempt identifiers excluded from numerical equality, raw files retained.'},'batch_size':64,'stages_training':8,'teacher_forcing':'updates1..1000 plus every fourth one-based update thereafter','optimizer':'unchanged q010r.training AdamW/cosine settings','loss':'mean of 8 stage cross-entropy +0.5 mean squared code sum','data':'unchanged graph stream and main_data_recipe; fresh per-update, domain-separated development/training/heldout; near changes32/64 reserved decoys only','rng':{str(s):{role:seed_plan(s,arm) for role,arm in ARMS} for s in SEEDS},'evaluation':{'matrix_cells':64,'readers_per_seed':6,'logical_query_chains':449640,'logical_stage_evaluations':3045480,'stage_count':'full allowed depth including UNKNOWN; direct exactly1','durability_checkpoints':list(CHECKPOINTS),'streams_per_durability_checkpoint':128,'parameters_fixed':True,'batching':'independent cases batched128, lifecyclebatch1; saved full stage arrays, typed reference states, immutable source cases and noise seeds. Lossless columnar storage replaces duplicated scalar NPZ files. Same scientific case/seed/scope, not a reduced study.','local_arithmetic':'CPUfloat32 same-batch eager PyTorch exact replay plus independently implemented float64 error-bound audit; cross-host historical bit equality not assumed.','novel_queries':'source UNKNOWN stays scorer truth; nearest identity resolution is an observed decision, not proof of registration','conditions_provenance':'original source conditions and graph/query recipes unchanged; raw original inputs included'},'criteria':'same approved0.90 core,0.95 direct,0.90 each cadence08checkpoint, pooled5seeds per candidate/class with all per-seed results; all stress and scientific negatives retained','resources':{'device':'cpu','torch_threads_per_worker':1,'torch_interop_threads':1,'maximum_concurrent_fits':2,'per_fit_wall_hard_seconds':1800,'main_fits_phase_wall_hard_seconds':10800,'verification_retraining_phase_wall_seconds':5400,'evaluation_and_verification_wall_seconds_each':3600,'maximum_worker_rss_bytes':1879048192,'aggregate_cgroup_soft_bytes':3650722201,'minimum_free_disk_bytes':2147483648,'maximum_new_output_bytes':17179869184,'checkpoint_every_updates':1000,'resource_sample_every_updates':50,'external_monitor_period_seconds':1,'checkpoint_serialization_exclusive_lock':True},'stop_rules':['Stop a fit on nonfinite loss/gradient/state, source identity drift, unexpected data/seed/checkpoint binding, or measured resource ceiling. Preserve failure and last joint checkpoint.','No silent restarts, seed exclusions, fewer updates, omitted conditions, or replacing new weights with pilot weights. Any repaired rerun uses a new attempt ID and retains the failed attempt.','A complete negative scientific result is allowed; failed coverage/scoring/verifier or missing checkpoints prevent complete-study status.','Do not change numerical thresholds based on heldout outcomes. Development corrections and deviations have dated source diffs.'],'retention':{'original_archive':'byte unchanged, included','development':'all current reports, checkpoints and partial/failure evidence retained','successful_main':'final full optimizer/stream/RNG checkpoint with complete trace retained losslessly, plus independent manifest and logs; intermediate successful checkpoints may be removed only after final reload and hash checks and recorded in retention ledger','failed_or_partial':'retain every actual partial checkpoint and failure receipt','compression':'lossless XZ/ZIP, not neural-state quantization'},'limitations':['New reconstruction, not recovered original Q010 numerical experiment.','Known supplied identity catalogue, exact owner metadata, qualified write decisions.','No target-device Windows/GPU validation, integrated tri-core deployment, online/delayed learning or low-bit study.','Agent-independent scoring/reimplementation and fresh execution are internal verification, not third-party replication.']}
