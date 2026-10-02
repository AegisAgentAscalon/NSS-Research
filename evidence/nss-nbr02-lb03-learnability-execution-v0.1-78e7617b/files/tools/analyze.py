"""Frozen deterministic scoring/decision code. It does not execute models."""
from pathlib import Path
import json,numpy as np,math
R=Path(__file__).resolve().parents[1];C=json.loads((R/'protocol/CONFIG.json').read_text());G=C['gates']
def write(p,o):p.write_text(json.dumps(o,indent=2,allow_nan=False)+'\n')
def load():
 rec=[]
 for f in sorted((R/'results').glob('*/COMPLETE.json')):rec+=json.loads(f.read_text())['records']
 return rec

def main():
 rec=load();D={(x['seed'],x['mode'],x['regime'],x['step'],x['panel']):x for x in rec}
 agg=[]
 for reg in C['regimes']:
  for mode in C['modes']:
   for step in C['dev_steps']:
    for panel in ('development','confirmation','stress','B'):
     rows=[D[s,mode,reg,step,panel] for s in C['parents'] if(s,mode,reg,step,panel)in D]
     if not rows:continue
     r=dict(regime=reg,mode=mode,step=step,panel=panel,parents=len(rows))
     for k in ('correct','total','whole','histories','false_done','changed_correct','unchanged_correct'):
      if k in rows[0]:r[k]=sum(q[k]for q in rows)
     r['accuracy']=r['correct']/r['total']
     if 'whole'in r:r['whole_accuracy']=r['whole']/r['histories']
     if panel=='B':r['min_probability']=min(q['min_probability']for q in rows)
     agg.append(r)
 decisions=[];pairs=[]
 for seed in C['parents']:
  for reg in C['regimes']:
   for mode in C['modes']:
    i=D[seed,mode,reg,0,'confirmation'];f=D[seed,mode,reg,512,'confirmation'];b=D[seed,mode,reg,512,'B'];ib=D[seed,mode,reg,0,'B'];ctrl=D[seed,'M32',reg,512,'confirmation']
    with np.load(R/i['file'],allow_pickle=False)as z:p0=z['predictions'][:,i['prefix']:];y=z['labels'][:,i['prefix']:]
    with np.load(R/f['file'],allow_pickle=False)as z:pf=z['predictions'][:,f['prefix']:]
    with np.load(R/ctrl['file'],allow_pickle=False)as z:pc=z['predictions'][:,ctrl['prefix']:]
    initial_errors=i['total']-i['correct'];final_errors=f['total']-f['correct'];reduction=(initial_errors-final_errors)/initial_errors if initial_errors else None
    fa=f['correct']/f['total'];fw=f['whole']/f['histories'];ia=i['correct']/i['total'];iw=i['whole']/i['histories'];ca=ctrl['correct']/ctrl['total'];cw=ctrl['whole']/ctrl['histories']
    newfd=int(((pf==8)&(y!=8)&(p0!=8)).sum());gains=int(((p0!=y)&(pf==y)).sum());losses=int(((p0==y)&(pf!=y)).sum())
    gate=dict(absolute_event=fa>=G['same_task_event_floor'],absolute_whole=fw>=G['same_task_whole_floor'],all_cues=b['correct']==8 and b['min_probability']>=G['new_B_probability_floor'],paired_event=fa>=ca-G['event_loss_vs_control_max'],paired_whole=fw>=cw-G['whole_loss_vs_control_max'],paired_false_done=f['false_done']<=ctrl['false_done']+G['extra_false_done_vs_control_max'])
    if reg=='EARLY':
     gate['substantial_early_gain']=reduction is not None and reduction>=G['early_net_error_reduction_floor']
     learned=gate['absolute_event']and gate['absolute_whole']and gate['all_cues']and gate['substantial_early_gain'];retention=None
    else:
     gate['genuinely_new']=ib['changed_correct']==0
     gate['retained_event']=fa>=ia-G['retained_event_loss_vs_start_max'];gate['retained_whole']=fw>=iw-G['retained_whole_loss_vs_start_max'];gate['retained_false_done']=newfd<=G['new_false_done_vs_start_max']
     learned=gate['all_cues']and gate['genuinely_new'];retention=gate['absolute_event']and gate['absolute_whole']and gate['retained_event']and gate['retained_whole']and gate['retained_false_done']
    paired=all(gate[k]for k in ['paired_event','paired_whole','paired_false_done'])
    decisions.append(dict(seed=seed,mode=mode,regime=reg,initial=i,final=f,B_final=b,B_initial=ib,early_net_error_reduction=reduction,new_false_done=newfd,gains=gains,losses=losses,gates=gate,learned=learned,retained_prior=retention,paired_quality=paired,full_quality=(learned and paired and(retention is not False))))
    pairs.append(dict(seed=seed,mode=mode,regime=reg,vs_M32_gains=int(((pc!=y)&(pf==y)).sum()),vs_M32_losses=int(((pc==y)&(pf!=y)).sum()),event_delta=fa-ca,whole_delta=fw-cw))
 cohort=[]
 for mode in C['modes']:
  data=[x for x in decisions if x['mode']==mode]
  cohort.append(dict(mode=mode,EARLY_learning=sum(x['learned']for x in data if x['regime']=='EARLY'),NEW_learning=sum(x['learned']for x in data if x['regime']=='NEW'),NEW_retention=sum(x['retained_prior']for x in data if x['regime']=='NEW'),EARLY_full_quality=sum(x['full_quality']for x in data if x['regime']=='EARLY'),NEW_full_quality=sum(x['full_quality']for x in data if x['regime']=='NEW')))
 write(R/'results/SUMMARY.json',dict(aggregate=agg,per_parent=decisions,paired=pairs,cohort=cohort,scope='Raw primary metrics and predeclared quality gates. Resource, technical and baseline gates applied in final decision; no post-hoc threshold changes.'))
 print(json.dumps(cohort))
if __name__=='__main__':main()
