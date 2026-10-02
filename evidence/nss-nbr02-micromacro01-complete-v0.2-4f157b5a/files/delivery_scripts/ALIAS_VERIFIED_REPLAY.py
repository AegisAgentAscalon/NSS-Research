import json,hashlib,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'delivery/RESTORATION.json';s=json.loads(p.read_text());check=json.loads((R/'audit/REPLAY_COMPARISON.json').read_text());assert check['status']=='PASS'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
for v in check['matched_files']:
 rel='raw/replay/'+v['file'];q=R/rel
 assert q.stat().st_size==v['bytes'] and sha(q)==v['sha256']
 s['items'].append({'path':rel,'kind':'alias','source':'raw/primary/'+v['file'],'bytes':v['bytes'],'sha256':v['sha256'],'proof':'audit/REPLAY_COMPARISON.json'})
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2,sort_keys=True));os.replace(tmp,p);q.unlink()
s['events'].append({'action':'replay_alias_only_after_full_adaptive_recomputation_and_exact_comparison','count':len(check['matched_files']),'host_epoch':time.time(),'all_bytes_per_side':check['bytes_per_side']});p.write_text(json.dumps(s,indent=2,sort_keys=True))
print(len(check['matched_files']))
