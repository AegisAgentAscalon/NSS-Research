import gzip,lzma,json,hashlib,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'delivery';p=D/'RESTORATION.json';s=json.loads(p.read_text())
# Pure lossless coding; original decoded identities must remain identical.
for v in s['items']:
 if v['kind']!='gzip':continue
 src=R/v['encoded'];out=src.with_suffix('.xz');co=lzma.LZMACompressor(preset=6)
 with gzip.open(src,'rb') as f,open(out,'wb') as g:
  for b in iter(lambda:f.read(1<<20),b''):g.write(co.compress(b))
  g.write(co.flush())
 h=hashlib.sha256();n=0
 with lzma.open(out,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b);n+=len(b)
 assert h.hexdigest()==v['sha256'] and n==v['bytes']
 s['events'].append({'action':'reencode_closed_text_gzip_to_xz','target':v['path'],'old_encoded_sha256':v['encoded_sha256'],'old_encoded_bytes':v['encoded_bytes'],'new_encoded_bytes':out.stat().st_size,'original_decoded_identity_verified':True,'host_epoch':time.time()})
 v.update(kind='xz',encoded=str(out.relative_to(R)),encoded_bytes=out.stat().st_size,encoded_sha256=hashlib.sha256(out.read_bytes()).hexdigest());tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2,sort_keys=True));os.replace(tmp,p);src.unlink();print(v['path'],n,v['encoded_bytes'],flush=True)
# Earlier completed numeric prefix reproduced exactly by current run. Preserve as a tested prefix, never recompute it on restoration.
proof=json.loads((R/'audit/PRIOR_PREFIX_COMPARISON.json').read_text());assert proof['byte_identical_completed_prefix']
oldrel='attempts/v0.1/raw/primary/worker/records.bin';old=R/oldrel
assert hashlib.sha256(old.read_bytes()).hexdigest()==proof['old_sha256']
s['items'].append({'path':oldrel,'kind':'prefix','source':'raw/primary/worker/records.bin','bytes':proof['old_bytes'],'sha256':proof['old_sha256'],'proof':'audit/PRIOR_PREFIX_COMPARISON.json'})
tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2,sort_keys=True));os.replace(tmp,p);old.unlink()
# Check prefix identity of the predecessor's public/event logs against the actual new logs.
checks=[]
for name in ['public_messages.jsonl','public_responses.jsonl','worker/events.jsonl']:
 rel='attempts/v0.1/raw/primary/'+name;old=R/rel;cur='raw/primary/'+name
 if not old.exists():continue
 desc=next(x for x in s['items'] if x['path']==cur);b=old.read_bytes();h=hashlib.sha256(b).hexdigest()
 with lzma.open(R/desc['encoded'],'rb') as f:match=f.read(len(b))==b
 checks.append({'source':cur,'target':rel,'bytes':len(b),'sha256':h,'identical_prefix':match})
 if match:
  s['items'].append({'path':rel,'kind':'prefix','source':cur,'bytes':len(b),'sha256':h});tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2,sort_keys=True));os.replace(tmp,p);old.unlink()
(R/'audit/PRIOR_LOG_PREFIX_COMPARISON.json').write_text(json.dumps(checks,indent=2))
print('DONE',flush=True)
