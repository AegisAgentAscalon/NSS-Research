"""Post-result descriptive aggregation; no policy rerun, fitting or candidate mutation."""
import csv,json,collections,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False)
rows=list(csv.DictReader((root/'results/primary/CANDIDATE_DECISIONS.csv').open()))
def write(name,rs):
 if not rs:return
 with (out/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
pooled=[]
for prof in ['CAUTIOUS','MODERATE','PERMISSIVE']:
 for pol in ['FIXED_LOW','TARGETED','FIXED_HIGH','FULL_PANEL','ACCEPT_ALL','NEVER_ADOPT']:
  rs=[r for r in rows if r['phase']=='heldout' and r['profile']==prof and r['policy']==pol];n=len(rs)
  x={'profile':prof,'policy':pol,'candidate_snapshots':n}
  for k in ['accepted','full_eligible','acceptable_retained','unacceptable_adopted','acceptable_deferred','focal_available_correct','chosen_old_class_errors']:x[k]=sum(int(r[k]) for r in rs)
  for k in ['acceptable_potential_gain','acceptable_retained_gain','retained_net_probability_gain','chosen_old_p_drop','chosen_mean_logloss_gain']:x['sum_'+k]=sum(float(r[k]) for r in rs)
  x['acceptable_recall']=x['acceptable_retained']/x['full_eligible'] if x['full_eligible'] else None
  x['bad_adoption_per_candidate']=x['unacceptable_adopted']/n
  x['retained_acceptable_gain_fraction']=x['sum_acceptable_retained_gain']/x['sum_acceptable_potential_gain'] if x['sum_acceptable_potential_gain'] else None
  pooled.append(x)
write('POOLED_DESCRIPTIVE.csv',pooled)
errors=[]
for prof in ['CAUTIOUS','MODERATE','PERMISSIVE']:
 for pol in ['FIXED_LOW','TARGETED','FIXED_HIGH']:
  for tag in ['unacceptable_adopted','acceptable_deferred']:
   rs=[r for r in rows if r['phase']=='heldout' and r['profile']==prof and r['policy']==pol and int(r[tag])]
   counter=collections.Counter(r['full_reasons'] if tag=='unacceptable_adopted' else r['panel_reasons'] for r in rs)
   for reason,n in counter.items():errors.append({'profile':prof,'policy':pol,'error':tag,'reason_set':reason,'count':n,'with_old_class_error':sum(int(r['chosen_old_class_errors'])>0 for r in rs) if tag=='unacceptable_adopted' else ''})
write('ERROR_REASONS.csv',errors)
comparisons=[]
for src in ['REV01','TIMING01']:
 for m in ['G','L']:
  rs=[r for r in rows if r['phase']=='heldout' and r['profile']=='MODERATE' and r['source']==src and r['method']==m]
  by={(r['candidate'],r['policy']):r for r in rs};ids=sorted({r['candidate'] for r in rs})
  for direction in ['target_rejects_fixed_accepts','target_accepts_fixed_rejects']:
   events=[]
   for i in ids:
    t=by[i,'TARGETED'];f=by[i,'FIXED_LOW'];take=(int(t['accepted'])==0 and int(f['accepted'])==1) if direction.startswith('target_rejects') else (int(t['accepted'])==1 and int(f['accepted'])==0)
    if take:events.append(t)
   comparisons.append({'source':src,'method':m,'direction':direction,'changed_decisions':len(events),'full_acceptable':sum(int(r['full_eligible']) for r in events),'full_unacceptable':sum(1-int(r['full_eligible']) for r in events)})
write('POLICY_SWITCHES.csv',comparisons)
# Source-relative boundary interpretation; this is not a cumulative served trajectory.
summary={'cohort':'exposed historical held-out; two separate studies pooled descriptively only','n':1472,'independent_tasks_not_claimed':True,'moderate':{x['policy']:x for x in pooled if x['profile']=='MODERATE'},'changed_decision_breakdown':comparisons}
(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
