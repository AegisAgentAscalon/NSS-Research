from pathlib import Path
import json,zipfile,hashlib,time,datetime
BASE=Path('/mnt/data');WORK=BASE/'_nss_pass61_work/reconciled';OUT=BASE/'NSS_LB03_LEARNABILITY_v0.1/provenance'
STUDIES=[(55,'BRIDGE01','Prototype'),(56,'LB01_TERNARY','Execution'),(57,'LB02_Q2_TRAIN','Execution'),(58,'LB02_MASTER16','Execution'),(59,'LB01_T3_TARGET','Execution'),(60,'LB01_Q2_PACK','Execution')]
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def candidates(o):
 if isinstance(o,dict):
  if 'sha256'in o:yield o
  for v in o.values():yield from candidates(v)
 elif isinstance(o,list):
  for v in o:yield from candidates(v)
def kind(r):
 if r.startswith(('checkpoints/','parents/','models/')) or ('/parents/'in r):return 'checkpoint_or_model'
 if r.startswith('source/') or r.startswith('tools/'):return 'source_code'
 if r.startswith('protocol/'):return 'protocol_lock_environment'
 if r.startswith('failures/'):return 'failure_evidence'
 if r.startswith('audit/') or 'AUDIT'in r or 'PREFLIGHT'in r:return 'audit_receipt'
 if r.startswith('results/'):return 'raw_results_and_summaries'
 if r.startswith(('fixtures/','inputs/','data/')):return 'input_fixture_or_lineage'
 return 'documentation_or_other'
summary=[];inventory=[]
for number,tag,suffix in STUDIES:
 start=time.perf_counter();f=BASE/f'NSS_NBR02_{tag}_{suffix}_v0.1.zip';rf=BASE/f'NSS_NBR02_{tag}_Delivery_v0.1.json';receipt=json.loads(rf.read_text())
 expected=next(x for x in candidates(receipt) if Path(str(x.get('file',x.get('filename',x.get('path',''))))).name==f.name)
 actual=digest(f);assert actual==expected['sha256'],f.name
 z=zipfile.ZipFile(f);assert z.testzip() is None
 mpath=next(x for x in z.namelist() if x.count('/')==1 and x.endswith('/MANIFEST.json'));root=mpath.rsplit('/',1)[0]
 mb=z.read(mpath);assert sha(mb)==expected['manifest_sha256']; manifest=json.loads(mb)
 declared={root+'/'+r['path'] for r in manifest['files']};actualmembers={x for x in z.namelist() if not x.endswith('/')};extra={mpath}
 if root+'/MANIFEST.sha256' in actualmembers:extra.add(root+'/MANIFEST.sha256')
 assert declared|extra==actualmembers
 cats={};dest=WORK/root
 for r in manifest['files']:
  rel=r['path'];assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
  b=z.read(root+'/'+rel);assert len(b)==r['bytes'] and sha(b)==r['sha256'],rel
  destp=dest/rel;destp.parent.mkdir(parents=True,exist_ok=True);destp.write_bytes(b)
  k=kind(rel);cats[k]=cats.get(k,0)+1
  inventory.append(dict(pass_number=number,study=tag,archive=f.name,archive_sha256=actual,member=root+'/'+rel,relative=rel,category=k,bytes=len(b),sha256=r['sha256']))
 for x in extra:(dest/Path(x).name).write_bytes(z.read(x))
 (OUT/f'pass{number}_MANIFEST.json').write_bytes(mb);(OUT/f'pass{number}_DELIVERY.json').write_bytes(rf.read_bytes())
 row=dict(pass_number=number,study=tag,archive=f.name,bytes=f.stat().st_size,sha256=actual,root=root,manifest_sha256=sha(mb),payloads=len(manifest['files']),payload_bytes=sum(r['bytes']for r in manifest['files']),categories=cats,CRC='PASS',all_hashes='PASS',exact_membership='PASS',seconds=time.perf_counter()-start)
 summary.append(row);print(row,flush=True)
(OUT/'SOURCE_ARCHIVE_VERIFICATION.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Archive bytes, contents and receipts verified; no old training/inference executed.',archives=summary,total_payloads=len(inventory)),indent=2))
(OUT/'COMPLETE_RECORD_INVENTORY.json').write_text(json.dumps(inventory,indent=2))
