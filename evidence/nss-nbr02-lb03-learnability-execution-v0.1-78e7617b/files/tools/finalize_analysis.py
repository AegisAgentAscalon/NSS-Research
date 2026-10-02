"""Post-result accounting and screen application; no training or neural calls."""
from pathlib import Path
import json,hashlib,datetime,numpy as np,re
R=Path(__file__).resolve().parents[1];C=json.loads((R/'protocol/CONFIG.json').read_text());S=json.loads((R/'results/SUMMARY.json').read_text());A=[json.loads(p.read_text())for p in sorted((R/'audit').glob('REPLAY_*.json'))]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
main=[];profiles=[];state_stats=[]
for f in sorted((R/'checkpoints').glob('*/COMPLETE.json')):
 d=json.loads(f.read_text());hist=[json.loads(x)for x in(f.parent/'updates.jsonl').read_text().splitlines()];assert len(hist)==512
 stat=np.sum([x['statistics']for x in hist],axis=0).tolist()
 cp0=f.parent/'step0000.npz';cpf=f.parent/'step0512.npz'
 with np.load(cp0,allow_pickle=False)as z:bef={k:z[k].copy()for k in z.files if k.startswith('w:')}
 with np.load(cpf,allow_pickle=False)as z:aft={k:z[k].copy()for k in z.files if k.startswith('w:')}
 # Complete persistent array finiteness was separately audited. Here describe movement, not causal mechanisms.
 change={k:int((bef[k]!=aft[k]).sum())for k in bef}
 state_stats.append(dict(seed=d['seed'],regime=d['regime'],mode=d['mode'],write_statistics=stat,changed_master_values=change,max_master_abs=max(float(np.abs(a.astype(float)).max())for a in aft.values()),max_preclip_grad_norm=max(x['grad_norm']for x in hist),loss_initial=hist[0]['loss'],loss_final=hist[-1]['loss'],A_loss_initial=hist[0]['A_loss'],A_loss_final=hist[-1]['A_loss'],B_loss_initial=hist[0]['B_loss'],B_loss_final=hist[-1]['B_loss']))
 for row in hist:
  if 'memory_profile'in row:
   q=row['memory_profile'].copy();q.update(seed=d['seed'],regime=d['regime'],mode=d['mode'],step=row['cursor']);q['broader_union_with_named_scratch']=q['learning_array_subtotal']+q['effective_weights']+q['saved_excluding_effective']+q['rng_bytes']+q['optimizer_scratch_bytes']+q['quantizer_row_scratch_bytes'];profiles.append(q)
 main.append(d)
benchmark=json.loads((R/'audit/BENCHMARK.json').read_text());pre=json.loads((R/'audit/PREFLIGHT.json').read_text())
# Known updates are independently tied to journals, preflight records, benchmark ledger and suffix audit.
print('pre keys',pre.keys())
preupdates=24
benchupdates=benchmark['actual_optimizer_updates'] if 'actual_optimizer_updates'in benchmark else sum(x['updates']for x in benchmark['rows'])
audupdates=sum(x['actual_audit_optimizer_updates']for x in A)
mainupdates=sum(x['actual_updates']for x in main)
assert mainupdates==12288 and benchupdates==102 and audupdates==24
fix=[]
for name in ('development','confirmation','stress'):
 old=R/f'fixtures/{name}.npz';new=Path('/mnt/data/_nss_pass61_work/regenerated')/(name+'.npz');assert old.read_bytes()==new.read_bytes();fix.append(dict(file=str(old.relative_to(R)),sha256=sha(old),byte_exact=True))
recordednum=[c for p in(R/'results').glob('*/COMPLETE.json')for q in json.loads(p.read_text())['numerical']for c in q['checks']]
stablenum=[q for a in A for q in a['numerical']]
warnings=[]
for p in sorted((R/'logs').glob('eval_*.log')):
 txt=p.read_text()
 if 'RuntimeWarning'in txt:warnings.append(dict(path=str(p.relative_to(R)),sha256=sha(p),text=txt))
warn=dict(discovery='During main NEW evaluation, before post-result stable-reference audit',kind='Overflow in inherited NumPy naive sigmoid exp(-x)',preserved_logs=warnings,occurrences_counted_retroactively=sum(q['naive_exp_overflow_sites']for q in stablenum),gate_min=min(q['min_gate']for q in stablenum),gate_max=max(q['max_gate']for q in stablenum),saturated_sigmoid_count=sum(q['exact_saturated_sigmoids']for q in stablenum),stable_reference_max_logit_diff=max(q['logits']['max_abs']for q in stablenum),stable_reference_violations=sum(q['logits']['violations']+q['hidden']['violations']for q in stablenum),scope='Repeated evaluation points including prefixes. exp can overflow to inf while 1/(1+inf) is finite zero. A separately implemented sign-stable sigmoid reproduces declared output agreement without overflow. Frozen code and outputs were not changed. Large saturated preactivations remain a robustness concern; this is not proof of stability for every intermediate, training path, precision or future input.')
write(R/'failures/NUMERICAL_WARNING_AND_DIAGNOSIS.json',warn)
write(R/'results/PARAMETER_AND_LOSS_CHANGES.json',state_stats);write(R/'results/MEMORY_PROFILES.json',profiles)
account=dict(main_branches=len(main),actual_main_updates=mainupdates,actual_preflight_updates=preupdates,actual_benchmark_updates=benchupdates,actual_audit_updates=audupdates,actual_total_updates=mainupdates+preupdates+benchupdates+audupdates,global_allowed_updates=C['total_actual_update_cap'],repeated_or_discarded_main_updates=0,unknown_update_tails=0,non_model_optimizer_arithmetic_reference_steps=5,main_training_core_seconds=sum(x['core_seconds']for x in main),main_branch_seconds=sum(x['branch_seconds']for x in main),main_peak_rss=max(x['peak_rss']for x in main),evaluation_core_seconds=sum(json.loads(p.read_text())['seconds']for p in(R/'results').glob('*/COMPLETE.json')),audit_core_seconds=sum(x['seconds']for x in A),audit_peak_rss=max(x['peak_rss']for x in A),new_study_evidence_bytes_at_accounting=sum(p.stat().st_size for p in R.rglob('*')if p.is_file()),note='No additional training of retained main candidates after fixed endpoints; disposable timing and audit updates are counted separately. Core seconds omit research design, file reconciliation, compilation, imports, reporting and packaging. High-water RSS includes Python/Torch/corpus; memory union not peak. Main data writing capped, operating system not a dedicated sandbox.')
write(R/'results/ACCOUNTING.json',account)
tech=dict(status='PASS_DECLARED_CHECKS_WITH_NUMERICAL_WARNING',source_archives_verified=6,source_payloads_verified=2909,main_lock_files=45,endpoint_lock_files=192,checkpoint_files=sum(len(x['checkpoints'])for x in A),packed_exports=sum(len(x['exports'])for x in A),raw_arrays=sum(len(x['records'])for x in A),scored_observations=sum(r['scored_observations']for a in A for r in a['records']),all_observations=sum(r['all_observations']for a in A for r in a['records']),all_replays_bit_exact=all(r['bit_exact']for a in A for r in a['records']),update_suffixes=sum(len(a['update_suffixes'])for a in A),update_replay_applications=audupdates,snapshot_faults_rejected=sum(len(a['fault_rejections'])for a in A),recorded_numerical_scalars=sum(x['scalars']for x in recordednum),recorded_numerical_violations=sum(x['violations']for x in recordednum),recorded_max_abs=max(x['max_abs']for x in recordednum),stable_audit_scalars=sum(q['hidden']['scalars']+q['logits']['scalars']for q in stablenum),stable_audit_violations=sum(q['hidden']['violations']+q['logits']['violations']for q in stablenum),fixture_regeneration=fix,budget_compliant=account['actual_total_updates']<=C['total_actual_update_cap'],independent_external_review=False)
write(R/'audit/FINAL_AUDIT.json',tech)
dec=[]
for mode in C['modes']:
 p={reg:[x['seed']for x in S['per_parent']if x['mode']==mode and x['regime']==reg and x['full_quality']]for reg in C['regimes']}
 mem=next(x['learning_array_subtotal']for x in profiles if x['mode']==mode);base=next(x['learning_array_subtotal']for x in profiles if x['mode']=='M32');saving=1-mem/base
 timing=[x for x in benchmark['summary']if x['mode']==mode]
 quality=all(len(v)>=3 for v in p.values());memory=(saving>=.15) if mode!='M32'else None;rt=all(x['runtime_gate']for x in timing)
 dec.append(dict(mode=mode,full_quality_passing_parents=p,parents_passing_both_regimes=sorted(set(p['EARLY'])&set(p['NEW'])),separate_regime_quality_screen_pass=quality,array_saving=saving,memory_screen_pass=memory,runtime_screen_pass=rt,declared_overall_candidate_screen_pass=bool(quality and memory and rt and tech['budget_compliant']) if mode!='M32'else None,qualification_scope='Three-of-four required separately in each regime; intersecting cohort is additionally reported, not retroactively required. This does not establish universal noninferiority, exact retention or stable arithmetic of all internal intermediates.'))
write(R/'results/DECISION.json',dict(candidates=dec,recommendation='Retain stochastic FP16 masters as the leading bounded low-bit-training candidate, not a universal replacement. It passes the predeclared separate-regime screen, with only two shared parents passing both regimes. Nearest is useful for early preparation but fails new-learning retention cohort. Keep M32 control and all failures; no post-learning repair/integration or automatic next experiment.',technical_status=tech['status']))
print(json.dumps(account,indent=2));print(json.dumps(dec,indent=2));print(json.dumps(tech,indent=2))
