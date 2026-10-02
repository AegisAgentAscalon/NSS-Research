from pathlib import Path
import sys,copy,traceback,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from sc01 import Store,Workspace,SCError,canonical,digest,make_plan
from sc02 import IncrementalStore,IncrementalWorkspace
from fixture_factory import episode
from runner import execute
from sh01_common import worlds
from nss_hsa import prepare_worlds,PlanCache
from nss_hsa.hierarchy import HierarchyError
setup();m,mid=load(8801);checks=[]
def check(name,fn):
 try:detail=fn();checks.append({'name':name,'pass':True,'detail':detail})
 except Exception:checks.append({'name':name,'pass':False,'traceback':traceback.format_exc()})
 save(ROOT/'results'/'engineering_progress.json',{'checks':checks,'runtime':runtime()})
def fault(code,fn):
 try:fn()
 except (SCError,HierarchyError)as e:
  assert e.code==code,(code,e.code);return code
 raise AssertionError('Expected '+code)
def equal_store(a,b):
 assert a.rows==b.rows
 assert a.versions==b.versions and a.events==b.events
 assert a.world==b.world and a.topology==b.topology
for n in [8,32,128]:
 for seed in [991601,991602,991603]:
  def publisher(n=n,seed=seed):
   w=worlds(seed+n,1,n)[0];a=Store(w);b=IncrementalStore(w);equal_store(a,b)
   r=np.random.default_rng(seed)
   for k in range(50):
    field=['progress','receipts','constraints','freeze','dependency'][k%5]
    c={'field':field,'task':int(r.integers(n))}
    if field=='dependency':c['value']=r.choice([i for i in range(n)if i!=c['task']],2,replace=False).tolist()
    a.mutate(c);b.mutate(c);equal_store(a,b)
   restored=IncrementalStore.from_dict(json.loads(canonical(b.to_dict())));equal_store(a,restored)
   return {'updates':50,'row_byte_equality':True,'positions':len(a.rows)}
  check(f'publisher_{n}_{seed}',publisher)
for n in [8,32,128]:
 for mode in ['F','P','I']:
  def live(n=n,mode=mode):
   w=worlds(991604+n,1,n)[0];s=IncrementalStore(w);cap={8:40,32:128,128:384}[n]
   a=IncrementalWorkspace(s,mid,'cache'if mode=='F'else'segment',cap,4,scheduled=mode!='F',intermediates=mode=='I')
   total=0;maximum=0
   for j in range(18):
    if j%4==1:s.mutate({'field':'progress','task':j%n})
    if j%4==2:s.mutate({'field':'freeze'})
    if j==11:s.mutate({'field':'dependency','task':0,'value':[n-2,n-1]})
    if j in (5,12):
     raw=a.snapshot();s=IncrementalStore.from_dict(json.loads(canonical(s.to_dict())));a=IncrementalWorkspace.restore(raw,s,mid)
     assert not a.layer_cache
    ts=[(j+k)%n for k in range(min(n,6))]
    out=a.job(f'J{j}',ts,m)
    x,sp=prepare_worlds([s.world]);plan=PlanCache().get(sp)
    with torch.no_grad():ref=m(x,plan).numpy()[0]
    for t,rec in out.items():
     assert rec is not None
     yy=np.asarray(rec['logits'],np.float32);c=compare(yy,ref[t]);assert not c['violations']
     assert yy.argmax()==ref[t].argmax();total+=4;maximum=max(maximum,c['max_abs'])
    assert len(a.layer_cache)<=cap and len(a.result_cache)<=4
    assert a.stats['peak_active_rows']<=cap
   # First layer tensor entries own only their row storage.
   for _,v in a.layer_cache.values():assert v.untyped_storage().nbytes()==v.numel()*v.element_size()
   return {'scalars':total,'max_abs':maximum,'stats':dict(a.stats)}
  check(f'repeated_changes_eviction_restore_{n}_{mode}',live)
# Invalid publication is transactional.
def baddep():
 s=IncrementalStore(worlds(991605,1,8)[0]);before=(canonical(s.world),list(s.rows),list(s.versions),s.epoch)
 fault('INVALID_DEPENDENCY',lambda:s.mutate({'field':'dependency','task':0,'value':[0,1]}))
 assert before==(canonical(s.world),s.rows,s.versions,s.epoch)
 return 'old revision preserved'
check('fault_invalid_dependency_atomic',baddep)
s=IncrementalStore(worlds(991606,1,8)[0]);a=IncrementalWorkspace(s,mid,'segment',40,scheduled=True,intermediates=True)
a.job('J',[0,1],m);raw=a.snapshot()
check('fault_wrong_model_restore',lambda:fault('WRONG_MODEL_REVISION',lambda:IncrementalWorkspace.restore(raw,s,'not-model')))
check('fault_wrong_scope_restore',lambda:fault('WRONG_STORE_OR_SCOPE',lambda:IncrementalWorkspace.restore(raw,IncrementalStore(s.world,'other'),mid)))
check('fault_malformed_snapshot',lambda:fault('MALFORMED_CHECKPOINT',lambda:IncrementalWorkspace.restore(b'{',s,mid)))
def corrupt():
 e=json.loads(raw);e['payload']['receipts']['J:0']['label']=77
 return fault('CORRUPT_CHECKPOINT',lambda:IncrementalWorkspace.restore(canonical(e),s,mid))
check('fault_snapshot_checksum',corrupt)
check('fault_job_identity',lambda:fault('JOB_ID_COLLISION',lambda:a.job('J',[2],m)))
check('fault_duplicate_target',lambda:fault('DUPLICATE_JOB_TASK',lambda:a.job('dup',[1,1],m)))
check('fault_out_of_range',lambda:fault('INVALID_TARGETS',lambda:a.job('bad',[999],m)))
def eventgap():
 ss=IncrementalStore(s.world);w=IncrementalWorkspace(ss,mid,'segment',40,intermediates=True);w.job('a',[0],m)
 ss.mutate({'field':'freeze'});ss.events=[]
 return fault('MISSING_REVISION_EVENT',lambda:w.job('b',[0],m))
check('fault_event_gap',eventgap)
def modelmutation():
 mm=copy.deepcopy(m);w=IncrementalWorkspace(IncrementalStore(s.world),mid,'segment',40,intermediates=True);w.job('a',[0],mm)
 with torch.no_grad():next(mm.parameters()).add_(0.001)
 return fault('MODEL_MUTATED',lambda:w.job('b',[0],mm))
check('fault_weight_mutation',modelmutation)
def replacement():
 mm=copy.deepcopy(m);w=IncrementalWorkspace(IncrementalStore(s.world),mid,'segment',40,intermediates=True);w.job('a',[0],mm)
 mm.head.weight=torch.nn.Parameter(mm.head.weight.clone())
 return fault('MODEL_MUTATED',lambda:w.job('b',[0],mm))
check('fault_parameter_replacement',replacement)
def stale_intermediate():
 ss=IncrementalStore(s.world);w=IncrementalWorkspace(ss,mid,'segment',40,intermediates=True);w.job('a',list(range(8)),m)
 # Revise a direct first-layer dependency. Its stored version must fail and recompute.
 ss.mutate({'field':'progress','task':0});out=w.job('b',list(range(8)),m)
 x,sp=prepare_worlds([ss.world])
 with torch.no_grad():ref=m(x,PlanCache().get(sp)).numpy()[0]
 assert w.stats['intermediate_invalidations']>0
 for t,rec in out.items():assert compare(np.asarray(rec['logits'],np.float32),ref[t])['violations']==0
 return {'invalidated_intermediates':w.stats['intermediate_invalidations']}
check('stale_intermediate_recomputed',stale_intermediate)
def stale_signature():
 ss=IncrementalStore(s.world);w=IncrementalWorkspace(ss,mid,'cache',40);old=w.signature(0)
 ss.mutate({'field':'freeze'});new=w.signature(0);assert old!=new
 ref=Workspace(ss,mid,'cache',40);assert new==ref.signature(0)
 return 'changed complete version fingerprint'
check('stale_signature_recomputed',stale_signature)
def sizecontrol():
 w=IncrementalWorkspace(IncrementalStore(s.world),mid,'segment',16,intermediates=True,scheduled=True)
 out=w.job('small',list(range(8)),m);assert all(v is None for v in out.values())
 assert not w.layer_cache and not w.receipts
 return {'deferrals':w.stats['budget_deferrals']}
check('insufficient_budget_honest',sizecontrol)
def isolated():
 b=IncrementalWorkspace.restore(raw,s,mid);b.jobs['J']['tasks'][0]=5;assert a.jobs['J']['tasks'][0]==0
 assert not b.layer_cache and not b.signature_cache or b.layer_cache==OrderedDict()
 return 'isolated ledger and cold numerical cache'
from collections import OrderedDict
check('snapshot_isolation',isolated)
def nan():
 w=copy.deepcopy(s.world);w['nuisance'][0][0]=float('nan')
 # canonical JSON may reject before the feature compiler; either is an explicit rejection.
 try:IncrementalStore(w)
 except (ValueError,HierarchyError):return 'nonfinite rejected'
 raise AssertionError('nonfinite admitted')
check('fault_nonfinite_record',nan)
out={'status':'PASS'if all(c['pass']for c in checks)else'FAIL','checks':checks,'runtime':runtime(),'optimizer_applications':0}
save(ROOT/'results'/'engineering.json',out)
print(out['status'],len(checks),'checks',flush=True)
for c in checks:
 if not c['pass']:print(c['name'],c['traceback'])
raise SystemExit(0 if out['status']=='PASS'else 1)
