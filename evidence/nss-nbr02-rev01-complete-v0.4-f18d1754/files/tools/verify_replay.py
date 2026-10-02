"""Inspect all recorded arrays, deterministic metadata and final scores after genuine replay."""
import sys,json,hashlib,itertools,collections,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'source'))
from reference_numeric import records

def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=ROOT/'raw/primary';b=ROOT/'raw/replay';counts={'frames':0,'arrays':0,'elements':0};kinds=collections.Counter();maxnumeric=collections.defaultdict(int)
for left,right in itertools.zip_longest(records(a/'worker/records.bin'),records(b/'worker/records.bin')):
    assert left is not None and right is not None
    ka,ma,aa=left;kb,mb,bb=right;assert ka==kb and ma==mb and aa.keys()==bb.keys()
    counts['frames']+=1;kinds[ma['kind']]+=1;maxnumeric[ma['kind']]=max(maxnumeric[ma['kind']],sum(v.nbytes for v in aa.values()))
    for n,x in aa.items():
        y=bb[n];assert x.dtype==y.dtype and x.shape==y.shape and x.tobytes()==y.tobytes()
        counts['arrays']+=1;counts['elements']+=x.size
stable=['worker/records.bin','worker/events.jsonl','public_messages.jsonl','public_responses.jsonl','private/PLAN.json','A0_AND_GUARDS_LOCK.json','EXACT.json','COUNTERS.json','NOVELTY.json']
checks={n:{'bytes':(a/n).stat().st_size,'sha256':h(a/n),'same':h(a/n)==h(b/n)} for n in stable};assert all(v['same'] for v in checks.values())
cs=[]
for p in (a/'final_audit').iterdir():
    if p.suffix in ('.csv','.json'):
        other=b/'final_audit'/p.name;assert h(p)==h(other);cs.append(p.name)
plan=json.loads((ROOT/'protocol/SCHEMA_ACCOUNTING.json').read_text());assert dict(kinds)==plan['per_pass_record_counts']
for kind,n in maxnumeric.items():assert n<=plan['per_record_numeric_upper_bytes'][kind]
mxh=mxraw=totalraw=0
with open(a/'worker/records.bin','rb') as f:
    while True:
        pre=f.read(40)
        if not pre:break
        n=int.from_bytes(pre[:8],'little');raw=zlib.decompress(f.read(n));hn=int.from_bytes(raw[:4],'little');mxh=max(mxh,hn);mxraw=max(mxraw,len(raw));totalraw+=len(raw)
assert mxh<=65536 and mxraw<=131072
out={'status':'PASS','comparison':counts,'deterministic_files':checks,'final_score_files':cs,'actual_schema':{'record_counts':dict(kinds),'maximum_numeric_bytes':dict(maxnumeric),'max_header':mxh,'max_decoded_frame':mxraw,'total_decoded_envelope_bytes_one_pass':totalraw},'fresh_adaptive_replay_not_new_scientific_samples':True,'timing_and_heartbeat_volatile_files_excluded':True}
(ROOT/'audit/REPLAY_VERIFICATION.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
