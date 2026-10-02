from pathlib import Path
import sys,copy,json,hashlib,collections,argparse,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from runner import execute
from sc02 import IncrementalStore,IncrementalWorkspace

def recount():
 checks=[];policy_groups=collections.defaultdict(dict);totals=collections.Counter();largest=0.
 for p in sorted((ROOT/'results/episodes').glob('*.json')):
  r=json.loads(p.read_text());ep=json.loads((ROOT/'fixtures'/f'{r["episode"]}.json').read_text());w=copy.deepcopy(ep['world']);truth={}
  for j,e in enumerate(ep['events']):
   if e['op']=='change':
    c=e['change'];f=c['field']
    if f=='freeze':w[f]=1-w[f]
    elif f=='dependency':w['deps'][c['task']]=c['value']
    else:w[f][c['task']]=1-w[f][c['task']]
   if e['op']=='job':
    for t in e['tasks']:
     if w['freeze']:v=0
     elif w['progress'][t]:v=1
     elif all(w['progress'][k]for k in w['deps'][t]):v=2
     else:v=3
     truth[(j,t)]=v
  counts=collections.Counter();simplified=[]
  for obs in r['observations']:
   key=(obs['event'],obs['task'])
   if obs['status']=='ANSWER':
    y=np.asarray(obs['logits'],dtype=np.float32);ref=np.asarray(obs['full_logits'],dtype=np.float32)
    pred=int(np.argmax(y));target=truth[key];err=np.abs(y-ref);viol=int(((err>2e-5+2e-5*np.abs(ref))|~np.isfinite(y)).sum())
    assert pred==obs['pred']and target==obs['target']
    counts['answers']+=1;counts['correct']+=int(pred==target);counts['changed_classes']+=int(pred!=np.argmax(ref));counts['numeric_violations']+=viol
    counts['numeric_scalars']+=len(y);counts['false_complete']+=int(pred==1 and target!=1)
    largest=max(largest,float(err.max()));simplified.append((key,obs['status'],pred,obs['signature']))
   else:counts['unresolved_positions']+=1;simplified.append((key,obs['status'],None,None))
  for k,v in counts.items():assert r[k]==v,(p.name,k,r[k],v)
  signatures=[(t['job'],t['task'],t['signature'])for t in r['trace']if 'signature'in t]
  assert len(signatures)==len(set(signatures));assert r['stats'].get('peak_active_rows',0)<=r['record_cap']
  policy_groups[(r['episode'],r['model_seed'])][r['policy']]=simplified
  checks.append(p.name);totals.update(counts)
 policy_matches=0
 for key,group in policy_groups.items():
  assert set(group)==set('CSFPI')
  for v in 'SFPI':assert group[v]==group['C'],(key,v);policy_matches+=1
 lock=json.loads((ROOT/'SOURCE_LOCK.json').read_text());n=0
 for f,meta in lock['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==meta['sha256'];n+=1
 fixtures=json.loads((ROOT/'FIXTURE_LOCK.json').read_text())['fixtures']
 for row in fixtures:assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256']
 save(ROOT/'results/audit_recount.json',{'status':'PASS','files':len(checks),'source_files_verified':n,'fixtures_verified':len(fixtures),'policy_matches':policy_matches,'counts':dict(totals),'max_abs':largest,'zero_optimizer_applications':True})
 print('recount PASS',len(checks),policy_matches,dict(totals),flush=True)

def replay(n):
 setup();rows=[];start=time.perf_counter()
 for ms in [8801,8802,8804]:
  m,mid=load(ms)
  for fam in ['resume','revisions']:
   ep=json.loads((ROOT/'fixtures'/f'n{n}_s942201_{fam}.json').read_text())
   for v in ['P','I']:
    old=json.loads((ROOT/'results/episodes'/f'{ep["id"]}_m{ms}_{v}.json').read_text())
    out=execute(ep,m,mid,v,audit=True)
    assert out['observations']==old['observations'],(n,ms,fam,v,'observations')
    assert out['trace']==old['trace'],(n,ms,fam,v,'trace')
    rows.append({'file':f'{ep["id"]}_m{ms}_{v}.json','observations_bit_exact':True,'trace_bit_exact':True,'model_hash':mid})
 save(ROOT/'results'/f'audit_replay_n{n}.json',{'status':'PASS','rows':rows,'elapsed_seconds':time.perf_counter()-start,'runtime':runtime(),'optimizer_applications':0})
 print('replay',n,'PASS',len(rows),flush=True)

def snapshots():
 setup();m,mid=load(8801);rows=[]
 for p in sorted((ROOT/'results/snapshots').glob('*.json')):
  if p.name.endswith('.store.json'):continue
  ep_id,variant,event=p.stem.rsplit('_',2);ep=json.loads((ROOT/'fixtures'/f'{ep_id}.json').read_text())
  store=IncrementalStore.from_dict(json.loads(p.with_suffix('.store.json').read_text()))
  ws=IncrementalWorkspace.restore(p.read_bytes(),store,mid)
  assert not ws.layer_cache
  for e in ep['events'][int(event)+1:]:
   if e['op']=='change':store.mutate(e['change'])
   elif e['op']=='checkpoint':
    raw=ws.snapshot();store=IncrementalStore.from_dict(json.loads(canonical(store.to_dict())));ws=IncrementalWorkspace.restore(raw,store,mid)
   elif e['op']=='job':ws.job(e['id'],e['tasks'],m,limit_tasks=e.get('limit_tasks'))
  old=json.loads((ROOT/'results/episodes'/f'{ep_id}_m8801_{variant}.json').read_text())
  assert ws.trace==old['trace'],p.name
  rows.append({'snapshot':p.name,'final_trace_bit_exact':True})
 save(ROOT/'results/audit_snapshots.json',{'status':'PASS','rows':rows,'runtime':runtime(),'optimizer_applications':0})
 print('snapshots PASS',len(rows),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--recount',action='store_true');p.add_argument('--replay',type=int);p.add_argument('--snapshots',action='store_true');a=p.parse_args()
 if a.recount:recount()
 if a.replay:replay(a.replay)
 if a.snapshots:snapshots()
