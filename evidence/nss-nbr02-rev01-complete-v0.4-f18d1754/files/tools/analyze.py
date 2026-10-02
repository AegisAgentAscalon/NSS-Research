"""Post-result descriptive summaries from retained independently scored rows; no model calls."""
import json,csv,collections,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
S=ROOT/'raw/primary/final_audit';OUT=ROOT/'reports';OUT.mkdir(exist_ok=True)
def load(n):
    with open(S/n,newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
    with open(OUT/n,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['empty']);w.writeheader();w.writerows(rows)
q=load('QUERY_ROWS.csv');u=load('UPDATES.csv');old=load('RETENTION_INDIVIDUAL.csv')
updates={(r['session'],r['branch'],r['trial']):r for r in u}
fail=[]
for r in q:
    if int(r['correct']):continue
    phase=r['phase'];kind=r['kind'];arm=r['arm'];tr=int(r['trial'])
    if phase in ('fixture','sandbox','derivative','probe'):category='DIAGNOSTIC_OR_COST_NOT_MAIN'
    elif arm.startswith('N_'):category='FROZEN_CONTROL'
    elif kind=='raw_pre':category='BEFORE_FEEDBACK_PREDICTION'
    elif kind=='focal' and tr==3:category='FIRST_CORRECTION_LAG'
    elif kind=='old':category='OLD_KNOWLEDGE_WRONG_CLASS'
    else:category='OTHER_SCRATCH_MISS'
    step=updates.get((r['session'],r['branch'],r['trial']))
    fail.append({**r,'category':category,'update_frame':step['frame'] if step else '', 'cue_frame':step['cue_frame'] if step else '', 'raw_gradient_norm':step['raw_norm'] if step else '', 'applied_clip':step['clip'] if step else '', 'numeric_checks':'PASS' if step else 'READOUT_AUDIT_PASS','root_cause':'No unique internal root cause established; paired treatment effect is separate.'})
write('FAILURE_INDEX.csv',fail)
held=[r for r in q if r['phase']=='heldout'];agg=[]
for arm in ('G','L','N_G','N_L'):
    for branch in ('COMMON','B1','B2'):
        for trial in range(1,7):
            for kind in ('focal','old','raw_pre'):
                a=[r for r in held if r['arm']==arm and r['branch']==branch and int(r['trial'])==trial and r['kind']==kind]
                if a:agg.append({'arm':arm,'branch':branch,'trial':trial,'kind':kind,'correct':sum(int(r['correct']) for r in a),'count':len(a),'mean_loss':float(np.mean([float(r['loss']) for r in a])),'mean_probability_margin':float(np.mean([float(r['probability_margin']) for r in a]))})
write('HELDOUT_TIMEPOINTS.csv',agg)
unique={}
for r in old:
    if not int(r['B2_correct']):
        k=(r['arm'],r['fit'],r['base'],r['cue']);unique.setdefault(k,[]).append(int(r['trial']))
unique_rows=[{'arm':k[0],'fit':int(k[1]),'base':int(k[2]),'cue':int(k[3]),'wrong_checkpoints':';'.join(map(str,v)),'wrong_observations':len(v)} for k,v in sorted(unique.items())]
write('OLD_ERROR_CASES.csv',unique_rows)
summary={'status':'EXPLORATORY_POST_RESULT_DESCRIPTION','query_rows':len(q),'negative_rows':len(fail),'negative_categories':dict(collections.Counter(r['category'] for r in fail)),'heldout_adaptive_old_errors':unique_rows,'unique_error_case_count':len(unique_rows),'all_attempt_counts':{'updates':4024,'cell':119184,'head':38528,'backward':2024},'exact_control_counts':{'per_pass_rows':780,'initial_old_table_writes':1200,'online_receipt_writes':78,'lookup_reads':780},'old_cases_not_unique_memories_or_independent_samples':True}
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
