from pathlib import Path
import json,sys,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from cap01 import write_json,file_sha
rows=[json.loads(p.read_text()) for p in (ROOT/'results/cases').glob('*.json')]
assert len(rows)==488

def stats(vs):
    cm=np.zeros((4,4),dtype=np.int64)
    for v in vs:
        for a,b in zip(v['targets_y'],v['predictions']):cm[a,b]+=1
    rc=cm.diagonal()[cm.sum(1)>0]/cm.sum(1)[cm.sum(1)>0]
    return {'jobs':len(vs),'decisions':int(cm.sum()),'correct':int(cm.trace()),'accuracy':float(cm.trace()/cm.sum()),
            'whole_correct':sum(x['whole_correct'] for x in vs),'whole_accuracy':sum(x['whole_correct'] for x in vs)/len(vs),
            'macro_recall_represented':float(rc.mean()),'confusion':cm.tolist(),
            'false_complete':sum(x['false_complete'] for x in vs),'false_ready':sum(x['false_ready'] for x in vs),
            'resident_admitted':sum(x['resident_admitted'] for x in vs)}
summary={'cases':len(rows),'statuses':dict(collections.Counter(x['status'] for x in rows)),
 'task_observations':sum(len(x['predictions']) for x in rows),
 'comparison_scalars':sum(c['scalars'] for x in rows for c in x['comparisons'].values()),
 'numerical_violations':sum(c['violations'] for x in rows for c in x['comparisons'].values()),
 'max_abs_difference':max(c['max_abs'] for x in rows for c in x['comparisons'].values()),
 'max_tolerance_fraction':max(c['max_tolerance_fraction'] for x in rows for c in x['comparisons'].values()),
 'class_parity_failures':sum(not x['class_parity'] for x in rows),
 'paused_cases':sum(x['paused'] for x in rows),'stale_checkpoint_rejections':sum(x['stale_resume_rejected'] is not None for x in rows),
 'main_core_seconds':sum(x['core_seconds'] for x in rows),'peak_process_rss_bytes':max(x['process_peak_rss_bytes'] for x in rows),
 'optimizer_applications':0,'source_fits_added':0,'tables':{},'parent_tables':{},'cost_rows':[]}
for stratum in ['primary','stress','tile_sensitivity']:
 for n in [8,32,128,512]:
  for mode in ['dense','hsa']:
   for cap in [16,32,64]:
    vs=[x for x in rows if x['case']['stratum']==stratum and x['n']==n and x['case']['mode']==mode and x['case']['policy']=='ordinary' and x['case']['cap']==cap]
    if not vs:continue
    key=f'{stratum}_n{n}_{mode}_c{cap}'
    summary['tables'][key]={'all':stats(vs),'unfrozen':stats([x for x in vs if x['freeze']==0])}
    for seed in sorted({x['case']['seed'] for x in vs}):summary['parent_tables'][key+f'_s{seed}']=stats([x for x in vs if x['case']['seed']==seed and not x['freeze']])
for n in [8,32,128,512]:
 for mode in ['dense','hsa']:
  vs=sorted([x for x in rows if x['n']==n and x['case']['mode']==mode and x['case']['policy']=='segmented' and x['case']['cap']==32 and x['case']['seed']==8801 and x['case']['rev']==0 and x['family']=='dispersed'],key=lambda x:x['case']['id'])
  x=vs[0];summary['cost_rows'].append({'n':n,'mode':mode,'case':x['case']['id'],'core_seconds':x['core_seconds'],'stats':x['stats']})
summary['archive_sizes']={}
for n in [8,32,128,512]:
 vs=[x for x in rows if x['n']==n and x['case']['mode']=='hsa' and x['case']['cap']==32]
 summary['archive_sizes'][str(n)]={'positions':vs[0]['positions'],'closure_min':min(min(x['resident_target_closures']) for x in vs),
 'closure_max':max(max(x['resident_target_closures']) for x in vs),'spool_bytes':max(x['stats']['external_array_bytes'] for x in vs),
 'visible_attention_payload_peak':max(x['stats']['named_attention_tensor_payload_peak'] for x in vs)}
replays=[x for f in (ROOT/'results').glob('REPLAY_*.json') for x in json.loads(f.read_text())['results']]
resumes=[x for f in (ROOT/'results').glob('RESUME_AUDIT_*.json') for x in json.loads(f.read_text())['results']]
summary['audit']={'recount_cases':488,'policy_pairs':244,'fresh_replays':len(replays),'bit_exact_replays':sum(x['bit_exact'] for x in replays),
                  'saved_resumes':len(resumes),'bit_exact_resumes':sum(x['bit_exact'] for x in resumes)}
summary['runner_seconds']=sum(json.loads(p.read_text())['seconds'] for p in (ROOT/'results').glob('RUN_RECEIPT*.json'))
summary['runtime']=json.loads((ROOT/'SOURCE_FIXTURE_LOCK.json').read_text())['runtime']
write_json(ROOT/'results/SUMMARY.json',summary)
failures=[]
for x in rows:
 if x['case']['policy']!='ordinary':continue
 if x['correct']==8:continue
 e=json.loads((ROOT/'fixtures'/f"{x['case']['fixture']}.json").read_text())['episode'];w=e['worlds'][x['case']['rev']]
 for j,(t,a,b) in enumerate(zip(x['targets'],x['targets_y'],x['predictions'])):
  if a!=b:failures.append({'case':x['case']['id'],'model':x['case']['seed'],'mode':x['case']['mode'],'n':x['n'],
                         'task':t,'expected':a,'predicted':b,'progress':w['progress'][t],'dependencies':w['deps'][t],
                         'dependency_progress':[w['progress'][k] for k in w['deps'][t]],'freeze':w['freeze'],
                         'logits':x['logits'][j],'full_reference_logits':x['reference_logits'][j],'source_sha256':x['world_sha256']})
write_json(ROOT/'failures/BEHAVIORAL_CASES.json',{'note':'Includes repeated source scenarios and tile conditions; not independent failure events. No post-result repair applied.','observations':failures})
print(json.dumps({k:v for k,v in summary.items() if k not in ['tables','parent_tables','cost_rows','runtime']},indent=2))
