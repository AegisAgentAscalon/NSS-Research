"""Post-result audit: independent target/count reconstruction and exact replay.
No new training, checkpoint selection, or new evaluation fixtures.
"""
import sys,json,time,hashlib,gzip
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
import cap02 as C
C.setup();start=time.perf_counter();data=C.read_gzip(ROOT/'fixtures/confirmation.json.gz')
summary=[];perparent=[];mismatch=[];failures=[];files=0;rowcount=0;storeddec=0;preds={}
def label(w):
 p=np.asarray(w['progress'],dtype=bool);deps=np.asarray(w['deps'],dtype=int)
 y=np.where(p,1,np.where(p[deps].all(axis=1),2,3))
 return np.zeros(len(p),dtype=np.int64) if w['freeze'] else y.astype(np.int64)
def metrics(y,p):
 y=np.asarray(y,dtype=np.int64);p=np.asarray(p,dtype=np.int64);cm=np.zeros((4,4),dtype=np.int64)
 np.add.at(cm,(y.ravel(),p.ravel()),1);tot=cm.sum(1);represented=tot>0
 return {'correct':int((p==y).sum()),'total':y.size,'accuracy':float((p==y).mean()),'whole_correct':int((p==y).all(1).sum()),
 'jobs':len(y),'whole_accuracy':float((p==y).all(1).mean()),'confusion':cm.tolist(),
 'macro_recall':float((np.diag(cm)[represented]/tot[represented]).mean()),
 'false_complete':int(((p==1)&(y!=1)).sum()),'false_ready':int(((p==2)&(y!=2)).sum())}
for seed in C.SEEDS:
 for mode in C.MODES:
  for arm in ['U','S','M']:
   path=ROOT/f'results/PRED_{seed}_{mode}_{arm}.npz';meta=json.loads((ROOT/f'results/EVAL_{seed}_{mode}_{arm}.json').read_text());arr=np.load(path);files+=1
   for r,record in zip(data,meta['worlds']):
    rid=r['id'];logits=arr[rid+'_logits'];y=label(r['world']);sel=np.asarray(r['targets']);p=logits.argmax(-1)
    assert np.array_equal(arr[rid+'_target'],y) and np.array_equal(arr[rid+'_selected'],sel)
    check={'selected_correct':int((p[sel]==y[sel]).sum()),'selected_total':len(sel),'whole_selected_correct':bool(np.array_equal(p[sel],y[sel])),
      'all_correct':int((p==y).sum()),'all_total':len(y),'all_world_correct':bool(np.array_equal(p,y)),
      'false_complete':int(((p[sel]==1)&(y[sel]!=1)).sum()),'false_ready':int(((p[sel]==2)&(y[sel]!=2)).sum())}
    for k,v in check.items():
     if record[k]!=v:mismatch.append([seed,mode,arm,rid,k,record[k],v])
    preds[(seed,mode,arm,rid)]=(p,y,sel);rowcount+=1;storeddec+=len(y)
    for task in sel[p[sel]!=y[sel]]:
     t=int(task);a,b=r['world']['deps'][t]
     failures.append({'seed':seed,'mode':mode,'arm':arm,'world':rid,'identity':r['identity'],'n':r['n'],'task':t,
       'actual':int(y[t]),'predicted':int(p[t]),'logits':logits[t].tolist(),'progress':r['world']['progress'][t],
       'dependencies':[a,b],'dependency_progress':[r['world']['progress'][a],r['world']['progress'][b]],'frozen':r['frozen']})
   for n in [8,32,128,512]:
    for frozen in [False,True]:
     subset=[r for r in data if r['n']==n and r['frozen']==frozen]
     ys=[];ps=[];ya=[];pa=[]
     for r in subset:
      p,y,sel=preds[(seed,mode,arm,r['id'])];ys.append(y[sel]);ps.append(p[sel]);ya.append(y);pa.append(p)
     row={'seed':seed,'mode':mode,'arm':arm,'n':n,'frozen':frozen,'selected':metrics(ys,ps),'all_tasks':metrics(ya,pa)}
     perparent.append(row)
   arr.close()
for mode in C.MODES:
 for arm in ['U','S','M']:
  for n in [8,32,128,512]:
   for frozen in [False,True]:
    subset=[r for r in data if r['n']==n and r['frozen']==frozen];ys=[];ps=[];ya=[];pa=[]
    for seed in C.SEEDS:
     for r in subset:
      p,y,sel=preds[(seed,mode,arm,r['id'])];ys.append(y[sel]);ps.append(p[sel]);ya.append(y);pa.append(p)
    row={'mode':mode,'arm':arm,'n':n,'frozen':frozen,'selected':metrics(ys,ps),'all_tasks':metrics(ya,pa)}
    row['working_point_met']=row['selected']['accuracy']>=.95 and row['selected']['macro_recall']>=.90 and row['selected']['whole_accuracy']>=.90
    summary.append(row)
paired=[]
for seed in C.SEEDS:
 for mode in C.MODES:
  for arm in ['S','M']:
   for n in [8,32,128,512]:
    fixed=lost=retained=bothwrong=newfr=newfc=0
    for r in data:
     if r['n']!=n or r['frozen']:continue
     pu,y,sel=preds[(seed,mode,'U',r['id'])];pc,_,_=preds[(seed,mode,arm,r['id'])]
     u=pu[sel]==y[sel];c=pc[sel]==y[sel]
     fixed+=int((~u&c).sum());lost+=int((u&~c).sum());retained+=int((u&c).sum());bothwrong+=int((~u&~c).sum())
     newfr+=int((u&(pc[sel]==2)&(y[sel]!=2)).sum());newfc+=int((u&(pc[sel]==1)&(y[sel]!=1)).sum())
    ru=next(x for x in perparent if x['seed']==seed and x['mode']==mode and x['arm']=='U' and x['n']==n and not x['frozen'])
    rc=next(x for x in perparent if x['seed']==seed and x['mode']==mode and x['arm']==arm and x['n']==n and not x['frozen'])
    paired.append({'seed':seed,'mode':mode,'arm':arm,'n':n,'repaired':fixed,'new_errors':lost,'retained_correct':retained,
      'both_wrong':bothwrong,'new_false_ready':newfr,'new_false_complete':newfc,
      'decision_delta_pp':100*(rc['selected']['accuracy']-ru['selected']['accuracy']),
      'whole_job_delta_pp':100*(rc['selected']['whole_accuracy']-ru['selected']['whole_accuracy']),
      'small_retention_flag': n==8 and (rc['selected']['accuracy']<ru['selected']['accuracy']-.01 or rc['selected']['whole_accuracy']<ru['selected']['whole_accuracy']-.01)})
C.write_json(ROOT/'results/SUMMARY.json',{'pooled':summary,'per_parent':perparent,'paired_changes':paired})
C.write_gzip(ROOT/'failures/SELECTED_BEHAVIORAL_ERRORS.json.gz',failures)
# Every saved parent and all 60 continuation checkpoint parameter identities.
checks=[]
for path in sorted((ROOT/'checkpoints').glob('*.pt')):
 cp=torch.load(path,weights_only=False,map_location='cpu');m=C.new_model(cp['seed'],cp['mode']);m.load_state_dict(cp['model']);h=C.model_hash(m)
 assert h==cp['model_hash'];assert cp['parent_file_sha256']==C.fsha(ROOT/'parents'/f"{cp['seed']}_{cp['mode']}.pt")
 checks.append({'file':str(path.relative_to(ROOT)),'model_hash':h,'step':cp['completed_updates'],'match':True})
# Full endpoint replay from saved inputs in this fresh process, preserving original arrays.
prepared=[C.batchify([r]) for r in data];replays=[]
for seed in C.SEEDS:
 for mode in C.MODES:
  for arm in ['U','S','M']:
   m=C.new_model(seed,mode,arm).eval();bad=0;scalars=0;maximum=0.
   with np.load(ROOT/f'results/PRED_{seed}_{mode}_{arm}.npz') as arr,torch.inference_mode():
    for r,(x,plan,_,_) in zip(data,prepared):
     new=C.forward(m,x,plan,mode)[0].numpy();old=arr[r['id']+'_logits'];bad+=int(not np.array_equal(new,old));scalars+=new.size
     maximum=max(maximum,float(np.max(np.abs(new-old))))
   replays.append({'seed':seed,'mode':mode,'arm':arm,'worlds':len(data),'non_bitexact_worlds':bad,'scalars':scalars,'max_abs':maximum})
C.write_json(ROOT/'results/AUDIT.json',{'prediction_files':files,'world_rows_recounted':rowcount,'all_task_prediction_observations':storeddec,
 'mismatches':mismatch,'checkpoint_hashes':checks,'replays':replays,'source_lock_entries':C.verify_lock(),
 'seconds':time.perf_counter()-start,'peak_rss_bytes':__import__('resource').getrusage(__import__('resource').RUSAGE_SELF).ru_maxrss*1024})
print('audit:',files,'files;',rowcount,'world rows;',len(checks),'checkpoints;',sum(r['non_bitexact_worlds'] for r in replays),'replay mismatches')
for row in summary:
 if row['mode']=='hsa' and row['arm']=='M' and not row['frozen']:print('HSA M',row['n'],row['selected'])
