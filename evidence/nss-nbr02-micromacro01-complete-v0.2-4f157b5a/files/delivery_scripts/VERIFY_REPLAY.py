"""Post-run byte comparison, schema counts and all-attempt work checks; no neural work."""
import hashlib,json,math,struct,zlib,collections,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
for phase in ['primary','replay']:
 assert json.loads((R/f'audit/supervisor_{phase}/RESULT.json').read_text())['returncode']==0
m=json.loads((R/'audit/SEALED_PRIMARY_IDENTITIES.json').read_text())['files'];matches=[];diff=[];excluded=[]
for rel,x in m.items():
 suffix=rel.removeprefix('raw/primary/');q=R/'raw/replay'/suffix
 if suffix in ['COST_ADMISSION.json','worker/heartbeat.json']:
  excluded.append({'file':suffix,'reason':'measured cost timing/forecast or heartbeat timestamp'});continue
 if not q.is_file():diff.append({'file':suffix,'reason':'missing'});continue
 yy={'bytes':q.stat().st_size,'sha256':sha(q)}
 if yy!=x:diff.append({'file':suffix,'reason':'bytes differ','primary':x,'replay':yy})
 else:matches.append({'file':suffix,**x})
# The only nonidentical fields permitted in cost admission are measured times; all structural/numeric forecasts match.
a=json.loads((R/'raw/primary/COST_ADMISSION.json').read_text());b=json.loads((R/'raw/replay/COST_ADMISSION.json').read_text())
skip={'probe_seconds_including_audit','projected_shared_seconds'}
for k in a:
 if k not in skip:assert a[k]==b[k],('cost-derived field differs',k)
if diff:raise RuntimeError(json.dumps({'unanticipated_differences':diff},indent=2))
# Count descriptors of the genuinely recomputed replay file. Scientific independent audits already check each array digest.
fcount=acount=elements=payload=0;kinds=collections.Counter();arrbytes=0;maxnumeric=collections.defaultdict(int);maxheader=collections.defaultdict(int)
with open(R/'raw/replay/worker/records.bin','rb') as f:
 while True:
  hdr=f.read(40)
  if not hdr:break
  assert len(hdr)==40
  n=struct.unpack('<Q',hdr[:8])[0];z=f.read(n);assert hashlib.sha256(z).digest()==hdr[8:]
  e=zlib.decompress(z);nh=struct.unpack('<I',e[:4])[0];head=json.loads(e[4:4+nh]);meta=head['metadata'];a=head['arrays'];kind=meta['kind'];kinds[kind]+=1;fcount+=1;acount+=len(a);payload+=len(e)-4-nh
  elements+=sum(math.prod(x['shape']) for x in a.values());ab=sum(x['bytes'] for x in a.values());arrbytes+=ab;maxnumeric[kind]=max(maxnumeric[kind],ab);maxheader[kind]=max(maxheader[kind],nh)
ledger=json.loads((R/'protocol/WORK_LEDGER.json').read_text());assert dict(kinds)==ledger['frames_per_pass']
counts={k:ledger['prior_completed_prefix_counts'].get(k,0) for k in ledger['global_caps']}
receipts=[]
for ph in ['primary','replay']:
 c=json.loads((R/f'raw/{ph}/COUNTERS.json').read_text())['counts'];assert c['update_attempt']==c['update_commit'];assert all(c[k]==v for k,v in ledger['per_pass'].items());receipts.append({'pass':ph,'counts':c})
 for k in counts:counts[k]+=c[k]
assert counts==ledger['all_attempts_planned'];assert all(counts[k]<=v for k,v in ledger['global_caps'].items())
result={'status':'PASS','host_epoch':time.time(),'deterministic_file_comparisons':len(matches),'bytes_per_side':sum(x['bytes'] for x in matches),'matched_files':matches,'excluded':excluded,'cost_field_exclusions':sorted(skip),'numeric_frames':fcount,'array_occurrences':acount,'numeric_elements':elements,'numeric_logical_array_bytes':arrbytes,'stored_envelope_numeric_bytes_excluding_aliases':payload,'record_kinds':dict(kinds),'max_observed_numeric_by_kind':dict(maxnumeric),'max_observed_header_by_kind':dict(maxheader),'actual_all_attempts':counts,'caps':ledger['global_caps'],'adaptive_replay':True,'no_model_computations_in_this_comparison':True}
(R/'audit/REPLAY_COMPARISON.json').write_text(json.dumps(result,indent=2,sort_keys=True));print(json.dumps({k:v for k,v in result.items() if k not in ['matched_files','record_kinds','max_observed_numeric_by_kind','max_observed_header_by_kind']},indent=2))
