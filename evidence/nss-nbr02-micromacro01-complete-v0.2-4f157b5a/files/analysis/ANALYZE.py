"""Descriptive summaries of already captured scores. No model, optimizer, source generator or policy call."""
import csv,json,sys,collections,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
 with open(ROOT/'raw/primary/final_audit'/f'{name}.csv',newline='') as f:return list(csv.DictReader(f))
def avg(x):return sum(x)/len(x) if x else None
def w(out,name,rows):
 with open(out/(name+'.csv'),'w',newline='') as f:
  z=csv.DictWriter(f,list(rows[0]) if rows else ['empty']);z.writeheader();z.writerows(rows)
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 cc=read('CYCLE_CONTEXTS');oo=read('OPERATION_METRICS');st=read('STAGE_METRICS');old=read('OLD_RECORDS');q=read('QUERY_ROWS');ba=read('BATCH_UPDATES');
 d=json.loads((ROOT/'raw/primary/final_audit/DECISIONS.json').read_text())
 w(out,'FEASIBILITY',[{k:v for k,v in r.items() if k!='by_fit'} for r in d['results']])
 sr=[];paired=[];risk=[];fails=[];norms=[];full=[]
 for method in ['G','L']:
  for branch in ['B1','U','D','B4','F4']:
   cycles=[r for r in cc if r['method']==method and r['branch']==branch and r['phase']=='heldout' and r['profile']=='primary']
   ops=[r for r in oo if r['method']==method and r['branch']==branch and r['phase']=='heldout'];end=[r for r in st if r['method']==method and r['branch']==branch and r['phase']=='heldout']
   olds=[r for r in old if r['method']==method and r['branch']==branch and r['phase']=='heldout']
   bad=[r for r in olds if int(r['correct'])==0];distinct={(r['fit'],r['base'],r['cue']) for r in bad}
   risk.append({'method':method,'branch':branch,'cycles':len(cycles),'complete_cycles':sum(int(r['cycle_pass']) for r in cycles),'old_actual_observations':len(olds),'old_actual_wrong':len(bad),'old_distinct_model_base_cue_wrong':len(distinct),'minimum_old_probability':min(float(r['probability']) for r in olds),'mean_context_peak_old_loss':avg([float(r['peak_actual_old_loss']) for r in cycles]),'mean_context_stage_old_loss':avg([float(r['stage_mean_old_loss']) for r in cycles]),'max_single_old_drop':max(float(r['probability_drop']) for r in olds),'mean_final_old_drop':avg([float(r['final_old_mean_drop']) for r in cycles]),'mean_final_joint_gain':avg([float(r['final_joint_probability_gain']) for r in cycles])})
   for tr in range(3,9):
    x=[r for r in end if int(r['trial'])==tr];assert len(x)==32
    sr.append({'method':method,'branch':branch,'trial':tr,'contexts':32,'focal_correct':sum(int(r['focal_correct']) for r in x),'old_correct':sum(int(r['old_correct']) for r in x),'old_observations':256,'old_mean_loss':avg([float(r['mean_old_loss']) for r in x]),'old_mean_drop':avg([float(r['old_mean_drop']) for r in x]),'focal_mean_loss':avg([float(r['focal_loss']) for r in x]),'joint_mean_probability_gain':avg([float(r['joint_probability_gain']) for r in x])})
   for r in ops:
    reasons=[]
    if float(r['old_mean_drop'])>.10:reasons.append('MEAN_TRANSIENT_DROP')
    if float(r['old_worst_drop'])>.35:reasons.append('SINGLE_TRANSIENT_DROP')
    if int(r['old_correct'])<7:reasons.append('TRANSIENT_CLASS')
    if reasons:fails.append({k:r[k] for k in ['session','method','fit','base','phase','branch','trial','stage','old_mean_drop','old_worst_drop','old_correct','old_min_probability']}|{'violations':'|'.join(reasons)})
   z=[r for r in ba if r['phase']=='heldout' and r['method']==method and r['branch']==branch]
   if z:
    norms.append({'method':method,'branch':branch,'batches':len(z),'raw_mean_norm':avg([float(r['gradient_norm']) for r in z]),'raw_max_norm':max(float(r['gradient_norm']) for r in z),'clipped':sum(float(r['clip_factor'])<1 for r in z),'sum_actual_step_norm':sum(float(r['actual_step_norm']) for r in z),'mean_actual_step_norm':avg([float(r['actual_step_norm']) for r in z]),'mean_coefficient':avg([float(r['coefficient']) for r in z])})
  for other in ['U','B4','F4']:
   aa={(r['fit'],r['base']):r for r in cc if r['method']==method and r['branch']=='D' and r['phase']=='heldout' and r['profile']=='primary'}
   bb={(r['fit'],r['base']):r for r in cc if r['method']==method and r['branch']==other and r['phase']=='heldout' and r['profile']=='primary'}
   assert aa.keys()==bb.keys() and len(aa)==32
   for metric in ['final_old_loss','peak_actual_old_loss','stage_mean_old_loss','final_focal_loss','final_joint_probability_gain']:
    ds=[float(aa[k][metric])-float(bb[k][metric]) for k in aa]
    paired.append({'method':method,'contrast':'D_minus_'+other,'metric':metric,'contexts':32,'lower':sum(v<0 for v in ds),'equal':sum(v==0 for v in ds),'higher':sum(v>0 for v in ds),'mean_difference':avg(ds),'median_difference':statistics.median(ds)})
 bad=collections.Counter((r['phase'],r['method'],r['arm'],r['branch'],r['kind'],r['stage']) for r in q if not int(r['correct']))
 neg=[dict(zip(['phase','method','arm','branch','kind','stage'],k),incorrect=v) for k,v in sorted(bad.items())]
 for name,rows in [('STAGE_TRAJECTORY',sr),('PAIRED_CONTRASTS',paired),('RISK_SUMMARY',risk),('TRANSIENT_VIOLATIONS',fails),('BATCH_COST_MAGNITUDES',norms),('FAILURE_COUNTS',neg)]:w(out,name,rows)
 cycneg=[r for r in cc if r['profile']=='primary' and not int(r['cycle_pass'])];w(out,'FAILED_PRIMARY_CYCLES',cycneg)
 b1=[r for r in q if r['phase']=='heldout' and r['arm'] in ('G','L') and r['kind']=='focal' and r['stage']=='post_real' and r['branch']=='B1' and int(r['trial'])==3]
 eq=read('EXACT_ROWS')
 summary={'scope':'post-result descriptive audit, no new model computations or altered criteria','query_rows':len(q),'incorrect_query_rows':sum(not int(r['correct']) for r in q),'heldout_query_rows':sum(r['phase']=='heldout' for r in q),'heldout_incorrect_rows':sum(r['phase']=='heldout' and not int(r['correct']) for r in q),'heldout_learned_postfeedback_incorrect':sum(r['phase']=='heldout' and r['arm'] in ('G','L') and r['kind']!='raw_pre' and not int(r['correct']) for r in q),'heldout_b1_first_errors':sum(not int(r['correct']) for r in b1),'heldout_primary_cycle_failures':sum(r['phase']=='heldout' and r['profile']=='primary' and not int(r['cycle_pass']) for r in cc),'exact_heldout_rows':sum(r['phase']=='heldout' for r in eq),'exact_columns':list(eq[0]) if eq else [],'raw_update_negative_rows_retained':True,'repeated_observations_not_independent':True}
 (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True));print(json.dumps(summary,indent=2))
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else ROOT/'analysis/tables')
