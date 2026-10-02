"""Post-result audit, separately frozen. No retuning and no historical scoring.
Replay is pure inference except the explicitly metered 4-update suffixes.
"""
from pathlib import Path
import sys,json,time,hashlib,os,traceback
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from candidate import *

def exact_labels(tokens):
 out=np.empty(tokens.shape,np.uint8)
 for n,row in enumerate(tokens):
  done=set()
  for j,e in enumerate(map(int,row)):
   if e<8:done.add(e)
   elif e<16:done.discard(e-8)
   elif e==16:done.clear()
   elif e!=17:raise ValueError('NON_CHECKLIST_EVENT')
   out[n,j]=next((i for i in range(8)if i not in done),8)
 return out

def stable_reference(weights,tokens):
 w={k:v.astype(np.float64)for k,v in weights.items()};h=np.zeros((len(tokens),64));HH=[];ZZ=[]
 extrema=dict(min_gate=0.,max_gate=0.,naive_exp_overflow_sites=0,gate_values=0,exact_saturated_sigmoids=0)
 def sigmoid(x):
  extrema['min_gate']=min(extrema['min_gate'],float(x.min()));extrema['max_gate']=max(extrema['max_gate'],float(x.max()))
  extrema['naive_exp_overflow_sites']+=int((x<-np.log(np.finfo(np.float64).max)).sum());extrema['gate_values']+=x.size
  a=np.empty_like(x);p=x>=0
  a[p]=1/(1+np.exp(-x[p]));ex=np.exp(x[~p]);a[~p]=ex/(1+ex)
  extrema['exact_saturated_sigmoids']+=int(((a==0)|(a==1)).sum());return a
 for j in range(tokens.shape[1]):
  ii=w[MATS[0]][:,tokens[:,j]].T+w[BIASES[0]]
  hh=h@w[MATS[1]].T+w[BIASES[1]]
  ir,iz,inn=np.split(ii,3,-1);hr,hz,hn=np.split(hh,3,-1)
  reset=sigmoid(ir+hr);update=sigmoid(iz+hz);new=np.tanh(inn+reset*hn)
  h=(1-update)*new+update*h;HH.append(h.copy());ZZ.append(h@w[MATS[2]].T+w[BIASES[2]])
 return np.stack(HH,1),np.stack(ZZ,1),extrema

def verify_locks():
 counts={}
 for name in ('MAIN_LOCK.json','ENDPOINT_LOCK.json'):
  d=json.loads((R/'protocol'/name).read_text());n=0
  for rec in d['files']:
   if sha(R/rec['path'])!=rec['sha256']:raise AssertionError('LOCK:'+rec['path'])
   n+=1
  counts[name]=n
 return counts

def audit_seed(seed):
 out=R/f'audit/REPLAY_{seed}.json'
 if out.exists():raise RuntimeError('AUDIT_NO_OVERWRITE')
 start=time.perf_counter();locks=verify_locks();records=[];checkpoints=[];exports=[];update_suffixes=[];faults=[];num=[];nupdates=0
 updatejournal=R/f'audit/UPDATES_{seed}.jsonl'
 if updatejournal.exists():raise RuntimeError('AUDIT_UPDATE_LOG_ALREADY_EXISTS')
 faultdir=R/f'audit/faults_{seed}';faultdir.mkdir(exist_ok=True)
 for regime in C['regimes']:
  for mode in C['modes']:
   folder=R/f'checkpoints/{seed}_{regime}_{mode}';rdir=R/f'results/{seed}_{regime}_{mode}'
   receipt=json.loads((folder/'COMPLETE.json').read_text());history=[json.loads(x)for x in (folder/'updates.jsonl').read_text().splitlines()]
   assert len(history)==512 and [x['cursor']for x in history]==list(range(1,513))
   assert receipt['actual_updates']==512 and not (folder/'INFLIGHT.json').exists() and not (folder/'STOP.json').exists()
   for q in receipt['checkpoints']:
    cp=R/q['path'];assert sha(cp)==q['sha256'];state=Candidate.load(cp)
    assert state.hash()==q['state_hash'] and state.cursor==q['cursor']
    if state.cursor:assert state.hash()==history[state.cursor-1]['state_hash']
    for a in state.arrays().values():assert np.isfinite(a).all()
    checkpoints.append(dict(file=q['path'],sha256=sha(cp),state_hash=state.hash(),cursor=state.cursor))
   evalrec=json.loads((rdir/'COMPLETE.json').read_text())
   for stage in C['dev_steps']:
    cp=folder/f'step{stage:04d}.npz';s=Candidate.load(cp);eff=s.effective();pf=rdir/f'step{stage:04d}.q2.npz';pd,meta=load_packed(pf)
    for k in MATS:
     codes=((pd[k+':code'][:,None].astype(np.uint16)>>np.array([0,2,4,6]))&3).astype(np.uint8).ravel()[:np.prod(SHAPES[k])].reshape(SHAPES[k])
     q,sc,zero,decoded=q_numpy(s.master[k])
     assert np.array_equal(q,codes)and np.array_equal(sc,pd[k+':scale'])and np.array_equal(zero,pd[k+':zero'])
     d=(codes.astype(np.int16)-pd[k+':zero'][:,None]).astype(np.float32)*pd[k+':scale'][:,None]
     assert np.array_equal(d,eff[k])
    for k in BIASES:assert np.array_equal(pd[k],eff[k])
    exports.append(dict(file=str(pf.relative_to(R)),sha256=sha(pf),matrix_entries=17856,exact=True))
    for rr in evalrec['records']:
     if rr['step']!=stage:continue
     f=R/rr['file'];assert sha(f)==rr['sha256']
     with np.load(f,allow_pickle=False)as z:a={k:z[k].copy()for k in z.files}
     t=a['tokens'];h,logit=packed_file_roll(pf,t);rh,rz,rangeinfo=stable_reference(eff,t)
     if rr['panel']=='B':
      logit=logit[:,0];expected=np.array(C['old_B']if regime=='EARLY'else C['new_B'],np.uint8)
      target=C['old_B']if regime=='EARLY'else C['new_B'];p=np.exp(logit-logit.max(1,keepdims=True));p/=p.sum(1,keepdims=True)
      assert np.array_equal(p,a['probabilities']);assert np.array_equal(p[np.arange(8),target],a['target_probabilities'])
      recount=dict(correct=int((logit.argmax(1)==expected).sum()),total=8,min_probability=float(p[np.arange(8),target].min()))
      cmpz=comparison(logit,rz[:,0]);suffix=8;events=8
     else:
      expected=exact_labels(t);prefix=json.loads(a['meta'].tobytes())['prefix'];recount=metrics(logit[:,prefix:],expected[:,prefix:]);cmpz=comparison(logit,rz);suffix=int(t[:,prefix:].size);events=int(t.size)
     cmph=comparison(h,rh)
     assert np.array_equal(expected,a['labels'])and np.array_equal(a['predictions'],logit.argmax(-1))
     assert np.array_equal(logit,a['logits'])and np.array_equal(h[:,-1],a['final_hidden'])
     assert all(recount[k]==rr[k]for k in recount)
     assert cmph['finite']and cmpz['finite']and not cmph['violations']and not cmpz['violations']
     assert np.array_equal((rz[:,0]if rr['panel']=='B'else rz).argmax(-1),a['predictions'])
     records.append(dict(file=rr['file'],sha256=sha(f),scored_observations=suffix,all_observations=events,recount=recount,bit_exact=True))
     num.append(dict(regime=regime,mode=mode,step=stage,panel=rr['panel'],hidden=cmph,logits=cmpz,**rangeinfo))
   # Only source4101 receives the predeclared four-update suffix replay.
   if seed==4101:
    s=Candidate.load(folder/'step0064.npz')
    with np.load(R/f'inputs/replay/{seed}.npz',allow_pickle=False)as z:ts=z['tokens'];ys=z['labels']
    matches=[]
    for i in range(64,68):
     with updatejournal.open('ab')as f:f.write(canon(dict(event='INTENT',seed=seed,mode=mode,regime=regime,cursor=i+1))+b'\n');f.flush();os.fsync(f.fileno())
     row=s.step(ts[i%64],ys[i%64],lr_at(i));nupdates+=1
     with updatejournal.open('ab')as f:f.write(canon(dict(event='COMMITTED',seed=seed,mode=mode,regime=regime,cursor=i+1,state_hash=s.hash()))+b'\n');f.flush();os.fsync(f.fileno())
     stablekeys=set(row)-{'seconds','peak_rss'}
     differences=[k for k in stablekeys if row[k]!=history[i][k]]
     if differences:raise AssertionError('UPDATE_REPLAY:'+str(differences))
     matches.append(dict(cursor=i+1,state_hash=s.hash(),gradient_hash=row['gradient_hash']))
    update_suffixes.append(dict(regime=regime,mode=mode,replayed_updates=4,matches=matches))
    with np.load(folder/'step0064.npz',allow_pickle=False)as z:base={k:z[k].copy()for k in z.files}
    for kind in ('changed_weight','wrong_source','wrong_dtype','inconsistent_cursor'):
     dat={k:v.copy()for k,v in base.items()};md=json.loads(dat['meta'].tobytes())
     if kind=='changed_weight':
      a=dat['w:'+MATS[0]];a.flat[0]=np.nextafter(a.flat[0],np.array(np.inf,dtype=a.dtype),dtype=a.dtype)
     elif kind=='wrong_source':md['source']='0'*64
     elif kind=='wrong_dtype':dat['w:'+MATS[0]]=dat['w:'+MATS[0]].astype(np.float64)
     else:md['optstep']+=1
     dat['meta']=np.frombuffer(canon(md),np.uint8);fp=faultdir/f'{regime}_{mode}_{kind}.npz';np.savez_compressed(fp,**dat)
     try:Candidate.load(fp)
     except(ValueError,AssertionError)as e:faults.append(dict(file=str(fp.relative_to(R)),kind=kind,rejection=str(e),sha256=sha(fp)))
     else:raise AssertionError('UNREJECTED_FAULT:'+kind)
 locks2=verify_locks();assert locks==locks2
 write(out,dict(seed=seed,status='PASS',locks=locks,records=records,checkpoints=checkpoints,exports=exports,numerical=num,update_suffixes=update_suffixes,actual_audit_optimizer_updates=nupdates,fault_rejections=faults,seconds=time.perf_counter()-start,peak_rss=rss(),scope='Internal fresh-process replay and independent stable-equation/label check; no third-party replication. Stable reference is retrospective diagnosis, does not replace historical naive-reference warnings or frozen output gates.'))
 print(seed,len(records),'arrays',len(exports),'exports',nupdates,'audit updates',flush=True)
if __name__=='__main__':audit_seed(int(sys.argv[1]))
