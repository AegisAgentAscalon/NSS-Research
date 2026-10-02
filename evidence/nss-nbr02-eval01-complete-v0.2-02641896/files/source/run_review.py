"""One fixed-candidate budgeted-review pass. No candidate learning or live adoption."""
from pathlib import Path
import argparse, gzip, hashlib, json, os, time, resource
import policy

def jb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(jb(x)).hexdigest()
def public_view(c):
 fields=('cue','scope','target','logits','receipt','record_id')
 return {'id':c['id'],'permitted':True,'source_bound':True,'completed':True,
 'parent_version':c['parent_version'],'anchor_version':c['anchor_version'],'candidate_version':c['parameter_version'],
 'target':c['focal']['target'],'focal_cue':c['focal']['cue'],'current_receipt':c['focal']['receipt'],
 'parent_focal_logits':c['parent_focal']['logits'],'old_reference':[{f:r[f] for f in fields} for r in c['parent_old']]}

class EvidenceAPI:
 def __init__(self,c,allowed):self.c=c;self.allowed=set(allowed);self.seen=set();self.requests=[]
 def get(self,key):
  if key not in self.allowed:raise ValueError('UNAUTHORIZED_MEASUREMENT')
  if key in self.seen:raise ValueError('DUPLICATE_MEASUREMENT')
  self.seen.add(key);r=self.c['focal'] if key=='FOCAL' else next(r for r in self.c['old'] if r['cue']==key)
  v={k:r[k] for k in ('cue','scope','target','logits','parameter_version','record_id','kind')}
  self.requests.append({'key':key,'record_id':r['record_id'],'response_sha256':h(v),'response':v});return v

class Journal:
 def __init__(self,p):self.f=p.open('wb');self.last='0'*64;self.seq=0
 def add(self,event):
  self.seq+=1;r={'sequence':self.seq,'prev':self.last,'event':event};self.last=h(r);r['sha256']=self.last
  self.f.write(jb(r)+b'\n');self.f.flush();os.fsync(self.f.fileno())
 def close(self):self.f.close();return {'count':self.seq,'sha256':self.last}

def compress(p):
 raw=p.read_bytes();gz=p.with_suffix(p.suffix+'.gz');gz.write_bytes(gzip.compress(raw,compresslevel=6,mtime=0));p.unlink()
 return {'file':gz.name,'decoded_bytes':len(raw),'decoded_sha256':hashlib.sha256(raw).hexdigest()}

def run(root,out):
 t=time.monotonic();out.mkdir(parents=True,exist_ok=False)
 cases=json.loads((root/'inputs/CANDIDATES.json').read_text());cfg=json.loads((root/'protocol/CONFIG.json').read_text())
 j=Journal(out/'JOURNAL.jsonl');df=(out/'DECISIONS.jsonl').open('wb');ef=(out/'EVIDENCE.jsonl').open('wb')
 lookup=decisions=reference_records=0;emitted=0
 try:
  for c in cases:
   pub=public_view(c);reference_records+=9
   for pol in cfg['policies']:
    panel=policy.select(pub,pol);keys=panel+(['FOCAL'] if pol not in ('ACCEPT_ALL','NEVER_ADOPT') else [])
    api=EvidenceAPI(c,keys);e=[api.get(k) for k in keys];lookup+=len(e)
    erec={'candidate':c['id'],'policy':pol,'public_sha256':h(pub),'panel':panel,'requests':api.requests}
    eid=h(erec);ef.write(jb(erec)+b'\n');emitted+=1
    for pname,pcfg in cfg['profiles'].items():
     request={'candidate':c['id'],'policy':pol,'profile':pname,'evidence_sha256':eid,'public_sha256':h(pub)}
     j.add({'type':'REVIEW_INTENT',**request});result=policy.decide(pub,e,pcfg,pol);decisions+=1
     row={**request,'panel':panel,**result};df.write(jb(row)+b'\n');df.flush();os.fsync(df.fileno())
     j.add({'type':'REVIEW_COMPLETE',**request,'result_sha256':h(row)})
     if decisions>cfg['caps']['review_evaluations']//2 or lookup>cfg['caps']['measurement_lookups']//2:raise RuntimeError('WORK_CAP')
  terminal=j.close();df.close();ef.close()
  files=[compress(out/n) for n in ('JOURNAL.jsonl','DECISIONS.jsonl','EVIDENCE.jsonl')]
  counts={'candidates':len(cases),'review_evaluations':decisions,'candidate_measurement_lookups':lookup,'reference_records_per_standalone_candidate':reference_records,'reference_records_per_isolated_policy':reference_records*len(cfg['policies']),'candidate_evidence_bundles':emitted,'model_calls':0,'derivatives':0,'updates':0,'neural_replay':False,'journal_terminal':terminal,'closed_files':files}
  (out/'COUNTS.json').write_bytes(jb(counts)+b'\n')
  (out/'RESOURCE.json').write_text(json.dumps({'wall_seconds':time.monotonic()-t,'maxrss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'interpretation':'Python policy replay only; source neural and deployment latencies not measured'},indent=2))
  print(json.dumps(counts,indent=2))
 except BaseException as ex:
  try:df.close();ef.close();j.f.close()
  except Exception:pass
  (out/'FAILURE.json').write_text(json.dumps({'type':type(ex).__name__,'error':str(ex),'completed_reviews':decisions,'measurement_lookups':lookup},indent=2));raise

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.root,a.out)
