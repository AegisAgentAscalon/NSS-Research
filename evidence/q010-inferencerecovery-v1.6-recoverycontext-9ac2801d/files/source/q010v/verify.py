"""Independent streaming verification and scoring of Q010 columnar captures.

No q010r/q010c imports. Source graph generation, pointer arithmetic and decoder
come from separately implemented verifier code. Consumes saved data, never a
producer's correct-answer flag. Development checks are not study qualification.
"""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,datetime
import numpy as np
from matrix_replay import generate_case_catalogue
from reader_math import decode_code
from source_oracle import terminal_truth, first_missing_edge
from integration_verify import _reconstruct_initial_query
from q010v.pointer_math import verify_captured_pointer_arrays

class VerificationError(ValueError):pass

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def read_json(p):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise VerificationError('duplicate JSON key')
   d[k]=v
  return d
 return json.loads(Path(p).read_text(),object_pairs_hook=unique)
def path_in(root,name):
 p=(root/name).resolve()
 if root.resolve() not in p.parents or not p.is_file():raise VerificationError('artifact path escapes or is absent')
 return p

def digest_arrays(arr):
 h=hashlib.sha256()
 for k,v in sorted(arr.items()):
  a=np.ascontiguousarray(v);h.update(k.encode());h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
 return h.hexdigest()

def live_ledger(meta,case):
 """Replay committed operations independently; registry alone cannot create facts."""
 if 'events' not in meta:return dict(case['truth_edges'])
 events=meta['events'];ops=meta['operations'];byid={e['event_id']:e for e in events}
 if len(byid)!=len(events):raise VerificationError('duplicate source event')
 graph=[e for e in events if e.get('kind')=='graph_truth']
 if len(graph)!=1 or dict(graph[0]['truth_edges'])!=dict(case['truth_edges']):raise VerificationError('initial graph mismatch')
 registered=set();facts={};scope=meta['state_scope'];epoch=1;used=set()
 for index,op in enumerate(ops,1):
  if op.get('sequence')!=index or op.get('case_id')!=case['case_id']:raise VerificationError('operation order/case')
  status=op['status'];kind=op['operation'];eid=op.get('truth_event_id')
  if status!='committed':
   if op.get('truth_changed') or eid is not None:raise VerificationError('noncommit changed source truth')
   if status in ('denied','stale') and op['before_map_sha256']!=op['after_map_sha256']:raise VerificationError('denied/stale mutated map')
   continue
  if op.get('qualified') is not True:raise VerificationError('unqualified commit')
  if op.get('requested_scope')!=scope:raise VerificationError('cross-scope commit')
  ev=byid.get(eid) if eid is not None else None
  if eid is not None:
   if ev is None or eid in used:raise VerificationError('missing/reused truth event')
   used.add(eid)
  if kind=='register':
   src=op['source_symbol_id']
   if ev is None or ev.get('kind')!='registration' or ev.get('symbol_id')!=src:raise VerificationError('registration binding')
   if src in registered:raise VerificationError('duplicate committed registration')
   registered.add(src);continue
  if kind=='scope_reset':
   if ev is not None and ev.get('kind')!='scope_reset':raise VerificationError('reset source')
   facts.clear();registered.clear();epoch+=1;continue
  if kind not in ('write','correct','rewrite','clear'):raise VerificationError('unsupported committed operation')
  src=op['source_symbol_id'];dst=op['destination_symbol_id']
  if src not in registered or (kind!='clear' and dst not in registered):raise VerificationError('unregistered write')
  if ev is not None:
   expected={'write':'fact_write','correct':'fact_correction','rewrite':'fact_rewrite','clear':'fact_clear'}[kind]
   if ev.get('kind')!=expected or ev.get('source_symbol_id')!=src or ev.get('destination_symbol_id')!=dst:raise VerificationError('fact source binding')
   if ev.get('previous_destination_symbol_id')!=facts.get(src):raise VerificationError('prior committed fact mismatch')
  elif (kind=='clear' and src in facts) or (kind!='clear' and facts.get(src)!=dst):raise VerificationError('new fact has no source event')
  if kind=='clear':facts.pop(src,None)
  else:facts[src]=dst
 return facts

def classify(edges,source,length,depth,*,life=False):
 expected=terminal_truth(edges,source,length,-1)
 missing=first_missing_edge(edges,source,length,-1)
 if life and not edges:return 'lifecycle_absence',expected
 if expected!=-1:return ('under_depth' if depth<length else 'supported'),expected
 if missing==0:return 'preexisting_unknown',expected
 return ('observable_missing' if missing<=depth else 'unobservable_missing'),expected

def verify_frame(raw,meta):
 b=len(meta['cases']);depth=int(meta['depth']);readers=meta['readers'];rows=[];audits=0
 if meta['feedback_mode']=='direct' and depth!=1:raise VerificationError('direct depth')
 state={k[7:]:v for k,v in raw.items() if k.startswith('state__')}
 required={'book','active','keys','vals','present','kr','vr','owner','owner_epoch','row_revision','allocation','epoch','catalogue_revision','state_revision'}
 if set(state)!=required:raise VerificationError('state field closure')
 valid=state['present']&state['kr']&state['vr'];values=np.where(valid[:,:,None],state['vals'],np.float32(0))
 keys=np.where(valid[:,:,None],state['keys'],np.float32(0))
 regenerated=[];ledgers=[];map_ok=[]
 for i,c in enumerate(meta['cases']):
  catalogue=generate_case_catalogue(c['case_spec']);regenerated.append(catalogue)
  if catalogue['facts']!=dict(c['truth_edges']) or catalogue['truth_graph_sha256']!=c['truth_graph_hash']:raise VerificationError('case truth differs from independent generator')
  if not np.array_equal(catalogue['symbols' if 'symbols' in catalogue else 'symbol_ids'],np.array(c['symbol_ids_by_book_slot'])):raise VerificationError('symbol generator mismatch')
  active=state['active'][i]
  if 'events' not in meta:
   # State-off legitimately has no active identities, but no hidden clean store.
   if active.any() and not np.array_equal(state['book'][i],catalogue['book']):raise VerificationError('protected catalogue changed')
  symbol_ids=np.asarray(catalogue['symbol_ids'],np.int64)
  source=int(raw['initial_source_ids'][i]);recipe=meta['queries'][i]
  expected_catalogue_digest=digest_arrays({'book':catalogue['book'],'symbols':symbol_ids,'active':np.ones(16,dtype=np.bool_)})
  if recipe['source_catalogue_sha256']!=expected_catalogue_digest:raise VerificationError('query source catalogue not bound')
  sample={'split':meta['split'],'seed_pair_id':meta['seed'],'condition_id':meta['condition_id'],'episode_id':meta['episode_ids'][i],'stage_index':0}
  actual_handles={str(int(sid)):int(h) for h,sid in enumerate(raw['symbols'][i]) if sid>=0 and active[h]}
  rebuilt_query=_reconstruct_initial_query(recipe,source_symbol_id=source if source>=0 else 'UNKNOWN',sample=sample,book=state['book'][i:i+1],symbol_to_handle=actual_handles,catalogue_book=catalogue['book'],catalogue_symbol_to_slot={str(int(sid)):int(j) for j,sid in enumerate(symbol_ids)})
  if not np.array_equal(rebuilt_query,raw['initial_query'][i]):raise VerificationError('query differs from independent source recipe')
  edges=live_ledger(meta,c);ledgers.append(edges)
  if 'live_facts' in meta and edges!=dict(meta['live_facts'][i]):raise VerificationError('producer live ledger disagrees with event replay')
  owners=state['owner'][i,state['present'][i]]
  if len(set(owners.tolist()))!=len(owners) or np.any(owners<0) or np.any(owners>=16):raise VerificationError('duplicate/invalid owner')
  actual={}
  for row in np.flatnonzero(state['present'][i]):
   owner=int(state['owner'][i,row]);src=int(raw['symbols'][i,owner])
   if not active[owner] or state['owner_epoch'][i,row]!=state['epoch'][i]:raise VerificationError('stale owner')
   decision=decode_code(state['vals'][i,row],state['book'][i],active,raw['symbols'][i])
   dst=-1 if decision.symbol_id=='UNKNOWN' else int(decision.symbol_id)
   actual[src]=dst if valid[i,row] else -1
  map_ok.append(actual==edges)
  # Never infer the gold label from actual or repaired memory.
 for reader in readers:
  prefix=reader+'__'
  for field,shape in {'query':(b,depth,17),'logits':(b,depth,17),'weights':(b,depth,17),'weighted_code':(b,depth,17),'read_code':(b,depth,17),'clean_code':(b,depth,17),'resolved_ids':(b,depth),'source_ids':(b,depth),'selected_rows':(b,depth),'state_unchanged':(b,depth)}.items():
   a=raw.get(prefix+field)
   if a is None or a.shape!=shape or a.dtype.hasobject:raise VerificationError('trace shape/field mismatch '+reader+field)
  if not raw[prefix+'state_unchanged'].all():raise VerificationError('read mutation')
  if not np.array_equal(raw[prefix+'query'][:,0],raw['initial_query']):raise VerificationError('initial query mismatch')
  if not np.array_equal(raw[prefix+'source_ids'][:,0],raw['initial_source_ids']):raise VerificationError('initial source mismatch')
  for step in range(depth):
   logits=raw[prefix+'logits'][:,step]
   if reader!='exact_owner' and np.any(logits[:,:16][~valid]!=np.float32(-1e4)):raise VerificationError('invalid neural logits leaked')
   if reader=='exact_owner':
    expected_logits=np.full((b,17),-20,dtype=np.float32)
    for i,src in enumerate(raw[prefix+'source_ids'][:,step]):
     row=16
     match=np.flatnonzero(raw['symbols'][i]==src) if src>=0 else []
     if len(match) and state['active'][i,match[0]]:
      rs=np.flatnonzero(state['present'][i]&(state['owner'][i]==match[0])&(state['owner_epoch'][i]==state['epoch'][i]))
      if len(rs) and valid[i,rs[0]]:row=int(rs[0])
     expected_logits[i,row]=20
    if not np.array_equal(logits,expected_logits):raise VerificationError('exact-owner control logits differ')
   verify_captured_pointer_arrays(logits,values,valid,captured_read_code=raw[prefix+'read_code'][:,step],captured_weights=raw[prefix+'weights'][:,step],captured_pre_norm=raw[prefix+'weighted_code'][:,step]);audits+=b
   if not np.array_equal(np.argmax(logits,axis=-1),raw[prefix+'selected_rows'][:,step]):raise VerificationError('selected rows inconsistent')
   for i in range(b):
    dec=decode_code(raw[prefix+'read_code'][i,step],state['book'][i],state['active'][i],raw['symbols'][i]);sid=-1 if dec.symbol_id=='UNKNOWN' else int(dec.symbol_id)
    if sid!=int(raw[prefix+'resolved_ids'][i,step]) or not np.array_equal(dec.clean_code,raw[prefix+'clean_code'][i,step]):raise VerificationError('independent decoder mismatch')
   if step:
    if not np.array_equal(raw[prefix+'query'][:,step],raw[prefix+'clean_code'][:,step-1]) or not np.array_equal(raw[prefix+'source_ids'][:,step],raw[prefix+'resolved_ids'][:,step-1]):raise VerificationError('feedback not bound to preceding actual result')
  for i,c in enumerate(meta['cases']):
   cls,expected=classify(ledgers[i],int(raw['initial_source_ids'][i]),int(c['path_length']),depth,life='events' in meta)
   predicted=int(raw[prefix+'resolved_ids'][i,-1]);rows.append(dict(seed=meta['seed'],condition=meta['condition_id'],checkpoint=meta['checkpoint'],case_id=c['case_id'],episode_id=meta['episode_ids'][i],reader=reader,evidence_class=cls,expected=expected,predicted=predicted,correct=predicted==expected,whole_map_correct=map_ok[i],depth=depth))
 return rows,audits

def verify_capture(root:Path,out:Path):
 root=root.resolve();out.mkdir(parents=True,exist_ok=False)
 cap=read_json(root/'CAPTURE.json');start=read_json(root/'START.json');counts=defaultdict(lambda:[0,0]);allrows=[];audits=0;seen=set();clocks={}
 matrix_path=Path(__file__).resolve().parents[2]/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0/plan/condition_matrix.json'
 matrix=read_json(matrix_path);definitions={x['condition_id']:x for x in matrix['cells']}
 requested=set(start['selected_cells']) if start.get('selected_cells') is not None else set(definitions)
 if not requested or not requested.issubset(definitions):raise VerificationError('unknown/empty declared condition set')
 if set(c['condition'] for c in cap['chunks'])!=requested or cap['cells']!=len(requested):raise VerificationError('missing or extra declared condition')
 if len(start['readers'])!=6 or not {'cap_only','ordinary','near','attention','exact_owner'}.issubset(start['readers']):raise VerificationError('six-role development roster incomplete')

 for chunk in cap['chunks']:
  p=path_in(root,chunk['file']);m=path_in(root,chunk['meta'])
  if sha(p)!=chunk['sha256'] or sha(m)!=chunk['meta_sha256']:raise VerificationError('artifact checksum mismatch')
  with np.load(p,allow_pickle=False) as z:raw={k:z[k].copy() for k in z.files}
  if digest_arrays(raw)!=chunk['array_digest'] or set(raw)!=set(chunk['arrays']):raise VerificationError('array closure/digest mismatch')
  for k,a in raw.items():
   if list(a.shape)!=chunk['arrays'][k]['shape'] or a.dtype.str!=chunk['arrays'][k]['dtype']:raise VerificationError('array metadata mismatch')
  meta=read_json(m)
  if meta['condition_id']!=chunk['condition'] or meta['seed']!=cap['seed']:raise VerificationError('metadata identity mismatch')
  if set(meta['readers'])!=set(start['readers']) or len(meta['readers'])!=len(start['readers']):raise VerificationError('roster changed')
  definition=definitions[meta['condition_id']];factors=definition['factors']
  depth=1 if definition['stratum']=='lifecycle' or factors.get('feedback_mode')=='direct' else int(factors.get('allowed_depth',min(int(factors.get('path_length',3)),4)))
  if meta['depth']!=depth:raise VerificationError('condition processing depth changed')
  want_n=1 if definition['stratum']=='lifecycle' else (start.get('development_count') or definition['episodes_per_seed'])
  if len(meta['cases'])!=want_n or len(meta['episode_ids'])!=want_n:raise VerificationError('case count differs from declared development/main scope')
  if meta['checkpoint'] is not None:
   if meta.get('event_count')!=meta['checkpoint']:raise VerificationError('workload clock differs from durability checkpoint')
   expected_prefix=(want_n,meta['checkpoint'])
   if raw.get('event_seed_prefix',np.empty(0)).shape!=expected_prefix:raise VerificationError('event prefix omitted')
  rows,n=verify_frame(raw,meta);audits+=n
  for row in rows:
   key=tuple(row[k] for k in ('seed','condition','checkpoint','case_id','reader'))
   if key in seen:raise VerificationError('duplicate query chain')
   seen.add(key);counts[(row['condition'],row['reader'],row['evidence_class'])][0]+=int(row['correct']);counts[(row['condition'],row['reader'],row['evidence_class'])][1]+=1
  allrows.extend(rows)
  if meta['checkpoint'] is not None:clocks.setdefault(meta['condition_id'],[]).append(meta['checkpoint'])
 for name,cps in clocks.items():
  want=[0,1024] if name=='ablation_no_maintenance' else list(range(0,1025,64))
  if cps!=want:raise VerificationError('durability checkpoints omitted/duplicated')
 if len(allrows)!=cap['chains'] or sum(r['depth'] for r in allrows)!=cap['logical_stage_evaluations']:raise VerificationError('declared workload differs')
 if cap['weights_before']!=cap['weights_after']:raise VerificationError('weight mutation reported')
 with (out/'QUERY_SCORES.csv').open('x',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
 summary=dict(status='PASS_DEVELOPMENT_EVIDENCE_VERIFICATION_NOT_QUALIFICATION',capture_sha256=sha(root/'CAPTURE.json'),start_sha256=sha(root/'START.json'),seed=cap['seed'],conditions=len({r['condition'] for r in allrows}),chunks=len(cap['chunks']),query_chains=len(allrows),stage_arithmetic_audits=audits,query_scores_sha256=sha(out/'QUERY_SCORES.csv'),metrics=[dict(condition=k[0],reader=k[1],evidence_class=k[2],correct=v[0],total=v[1]) for k,v in sorted(counts.items())],scope='source-generation/event-ledger truth and independent pointer arithmetic/decoding; full model/state replay recorded separately; no main fit',utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (out/'VERIFICATION.json').write_bytes(json.dumps(summary,indent=2,sort_keys=True).encode());print(json.dumps({k:v for k,v in summary.items() if k!='metrics'}));return summary
