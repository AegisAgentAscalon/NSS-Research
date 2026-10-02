"""Post-result analysis of retained arrays only: no model forwards or updates."""
from pathlib import Path
import hashlib, json, csv, platform
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def write(name,obj): (ROOT/'analysis'/name).write_text(json.dumps(obj,indent=2)+'\n')
def tok(e):
    e=int(e)
    return f'SET({e})' if e<8 else f'CLEAR({e-8})' if e<16 else 'RESET' if e==16 else 'NOOP'
out=json.loads((ROOT/'evidence/outcome.json').read_text())
rows=[]
for parent in out['parents']:
    for family,x in parent['metrics']['32'].items():
        rows.append({'seed':parent['seed'],'family':family,**{k:x[k] for k in ['events_correct','events_total','event_accuracy','whole_correct','histories','whole_rate','false_done','boundary_correct']},'parent_pass':parent['competence_pass']})
with (ROOT/'analysis/parent_family_results.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
pooled={'correct_events':sum(x['events_correct'] for x in rows),'events':sum(x['events_total'] for x in rows),
        'whole_correct':sum(x['whole_correct'] for x in rows),'histories':sum(x['histories'] for x in rows),
        'false_done':sum(x['false_done'] for x in rows),'independent_parents':4,'passed_parents':sum(p['competence_pass'] for p in out['parents']),
        'pooling_warning':'Descriptive counts only; nested events and histories are not independent replications.'}
pooled['event_accuracy']=pooled['correct_events']/pooled['events']; write('pooled_descriptive.json',pooled)
failure=np.load(ROOT/'failures/parent_4103_idempotent_first.npz'); meta=json.loads((ROOT/'failures/parent_4103_idempotent_first.json').read_text())
z=failure['logits'].astype(np.float64);z-=z.max(-1,keepdims=True);p=np.exp(z);p/=p.sum(-1,keepdims=True)
pred=p.argmax(-1); mask=0; events=[]
for i,e in enumerate(failure['tokens']):
    prev=mask; e=int(e)
    if e<8: mask|=1<<e
    elif e<16:mask &= ~(1<<(e-8))
    elif e==16:mask=0
    y=int(failure['targets'][i])
    events.append({'absolute_event':i+1,'suffix_event':i+1-meta['prefix_length'],'token':tok(e),'mask_before':prev,'mask_after':mask,
                   'semantics_unchanged':prev==mask,'target':y,'prediction':int(pred[i]),'correct':int(pred[i])==y,
                   'p_true':float(p[i,y]),'p_DONE':float(p[i,8]),'hidden_l2_change':float(np.linalg.norm(failure['hidden'][i]-failure['hidden'][i-1])) if i else None})
with (ROOT/'analysis/failure_4103_events.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
training=np.load(ROOT/'fixtures/training_4103.npz'); masks=training['masks']; tokens=training['tokens']; labels=training['labels']
prev=np.concatenate([np.zeros(masks.shape[:-1]+(1,),dtype=masks.dtype),masks[...,:-1]],-1)
key=(prev==223)&(masks==223)&(tokens==1)
error_indices=[i for i,e in enumerate(events) if not e['correct']]
summary={'status':'RETROSPECTIVE_RETAINED_ARRAY_ANALYSIS','new_optimizer_applications':0,'new_model_forwards':0,
         'failed_seed':4103,'family':'idempotent','original_panel_row':meta['row'],'prefix_length':meta['prefix_length'],
         'error_absolute_events':[events[i]['absolute_event'] for i in error_indices],
         'error_suffix_events':[events[i]['suffix_event'] for i in error_indices],
         'error_commands':[events[i]['token'] for i in error_indices],
         'required_class':5,'predicted_error_class':8,'mask_during_errors':223,'all_error_commands_leave_exact_mask_unchanged':all(events[i]['semantics_unchanged'] for i in error_indices),
         'before_first_error':events[error_indices[0]-1], 'first_error':events[error_indices[0]],'last_error':events[error_indices[-1]],
         'next_event':events[error_indices[-1]+1],
         'error_is_within_original_training_length_32':max(events[i]['absolute_event'] for i in error_indices)<=32,
         'training_seed4103_total_events':int(labels.size),'training_class_counts':np.bincount(labels.ravel(),minlength=9).tolist(),
         'training_mask_223_exposures':int((masks==223).sum()),'training_idempotent_SET1_at_mask223_exposures':int(key.sum()),
         'all_four_training_coverage':{str(s):json.loads((ROOT/f'fixtures/training_{s}_coverage.json').read_text()) for s in [4101,4102,4103,4104]},
         'interpretation':'Behavioral failure of semantic stability during idempotent operations with fixed weights. Capacity, objective, optimization and history-dependent representation remain unresolved causes. Counts of exact masks do not establish adequate exposure to every relevant history.',
         'no_repair_or_qualification_change':True}
write('failure_analysis.json',summary)
checks=[]
for s in [4101,4102,4103,4104]:
    for group in json.loads((ROOT/f'evidence/admission_{s}_numerical.json').read_text()): checks.extend(group['checks'])
write('numerical_summary.json',{'admission_hidden_and_logit_coordinates':sum(c['coordinates'] for c in checks),
       'failed_coordinates':sum(c['bad_coordinates'] for c in checks),'max_abs':max(c['max_abs'] for c in checks),
       'max_scaled':max(c['max_scaled'] for c in checks),'all_classes_agree':all(x['numerical_pass'] for x in out['parents']),
       'envelope':'2e-6 + 2e-5 * abs(reference)','thresholds_changed':False})
print(json.dumps(pooled,indent=2));print(json.dumps(summary,indent=2))
