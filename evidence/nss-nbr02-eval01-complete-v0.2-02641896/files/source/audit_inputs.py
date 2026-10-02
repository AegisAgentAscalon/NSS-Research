"""Supplemental independent provenance audit on extracted retained inputs.
This is verification of saved evidence, not model inference or learning replay.
"""
from pathlib import Path
import csv,gzip,hashlib,io,json,struct,sys
r=Path(sys.argv[1])
def load(p):
 p=Path(p)
 if p.exists():return json.loads(p.read_text())
 return json.loads(gzip.decompress(p.with_name(p.name+'.gz').read_bytes()))
def sha(x):return hashlib.sha256(x).hexdigest()
cs=load(r/'inputs/CANDIDATES.json');byid={};casekeys=set();report={}
for source in ['REV01','TIMING01']:
 d=r/'inputs'/source;ms=load(d/'MEASUREMENTS.json');proofs={p['frame']:p for p in load(d/'RAW_QUERY_PROOFS.json')};releases=load(d/'RELEASE_RECORDS.json');receipts={}
 for rel in releases:
  md=rel['metadata'];rid=md.get('receipt');target=md.get('target')
  for coord,v in md.get('table_after',{}).items():
   if v.get('receipt')==rid and v.get('label')==target:
    key=(rid,v.get('post_version'),target)
    receipts.setdefault(key,[]).append(rel['frame'])
 check=0
 for m in ms:
  pr=proofs[m['frame']];raw=bytes.fromhex(pr['logits_hex']);z=list(struct.unpack('<2f',raw));h=pr['header'];md=h['metadata']
  assert sha(raw)==h['arrays']['logits']['sha256']==m['array_sha256']
  assert z==m['logits'] and md['parameter_version']==m['parameter_version']
  assert md['context']['session']==m['session'] and md['context']['branch']==m['branch'] and md['context']['trial']==m['trial']
  receipt=m['receipt'];key=(receipt['receipt'],receipt.get('post_version'),m['target'])
  assert key in receipts and min(receipts[key])<m['frame'],('UNRELEASED',source,m['record_id'],key)
  assert m['target']==receipt['label'];byid[m['record_id']]=m;check+=1
 report[source]={'retained_measurements_checked':check,'raw_logits_exact':True,'current_target_release_precedes_measurement':True,'source_frames_preserved':len(proofs)}
seen=set()
for c in cs:
 for f in ('old','parent_old'):
  for m in c[f]:assert m==byid[m['record_id']]
 for f in ('focal','parent_focal'):assert c[f]==byid[c[f]['record_id']]
 assert c['parent_version']==c['parent_focal']['parameter_version']==c['anchor_version']
 assert c['parameter_version']==c['focal']['parameter_version']
 assert len(c['aliases'])>=1
 key=(c['source'],c['session'],c['parameter_version'],c['focal']['target']);assert key not in seen;seen.add(key)
 expected=sha(json.dumps(list(key),sort_keys=True,separators=(',',':'),allow_nan=False).encode());assert expected==c['id']
 for a in c['aliases']:
  assert a['trial']>=3
  for frame in a['frames']:
   rec=byid[f"{c['source']}:frame:{frame}"]
   assert rec['parameter_version']==c['parameter_version'] and rec['session']==c['session']
report['candidate_records']=len(cs);report['all_candidate_and_parent_fields_match_source_measurements']=True;report['source_authentication_limitation']='Stored source-hash and receipt-record conformance, not a live cryptographic authority service'
(r/'audit/INDEPENDENT_INPUT_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
