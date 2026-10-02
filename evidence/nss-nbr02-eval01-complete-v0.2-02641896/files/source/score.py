"""Independent retained-evidence adjudicator. Does not import policy, runner or extractor.
Recomputes softmax/loss from raw recorded logits; no neural model or learning.
"""
from pathlib import Path
import argparse,collections,csv,gzip,hashlib,json,math
import numpy as np

def jb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def hd(x):return hashlib.sha256(jb(x)).hexdigest()
def readlines(p):
 with gzip.open(p,'rt') as f:
  for l in f:yield json.loads(l)
def cp(z,y):
 a=np.asarray(z,dtype=np.float64);a-=a.max();v=np.exp(a);return float(v[y]/v.sum())
def nll(z,y):return float(np.logaddexp(0.,float(z[1-y])-float(z[y])))
def evaluate(c,indices,limits):
 fo=c['focal'];pf=c['parent_focal'];g=cp(fo['logits'],fo['target'])-cp(pf['logits'],fo['target'])
 old={r['cue']:r for r in c['old']};parent={r['cue']:r for r in c['parent_old']};ds=[];ps=[];lost=0
 for i in indices:
  r=old[i];p=parent[i];ps.append(cp(r['logits'],r['target']));ds.append(ps[-1]-cp(p['logits'],p['target']))
  lost+=int(np.argmax(p['logits'])==p['target'] and np.argmax(r['logits'])!=r['target'])
 mean=sum(ds)/len(ds);fp=cp(fo['logits'],fo['target']);metrics={'focal_probability':fp,'focal_gain':g,'old_mean_drop':-mean,'old_worst_drop':max([-d for d in ds]),'old_min_probability':min(ps),'old_class_loss_rate':lost/len(ds),'net_probability_gain':(8*mean+g)/9}
 predicates=[('FOCAL_FLOOR',fp>=limits['focal_floor']),('FOCAL_GAIN',g>=limits['focal_gain']),('OLD_MEAN_DROP',-mean<=limits['old_mean_drop']),('OLD_WORST_DROP',metrics['old_worst_drop']<=limits['old_worst_drop']),('OLD_FLOOR',min(ps)>=limits['old_floor']),('OLD_CLASS_LOSS',lost/len(ds)<=limits['old_error_rate']),('NO_NET_GAIN',metrics['net_probability_gain']>0)]
 reasons=[k for k,v in predicates if not v];return not reasons,reasons,metrics

def expected_panel(c,name):
 if name in ('ACCEPT_ALL','NEVER_ADOPT'):return []
 if name=='FULL_PANEL':return list(range(8))
 buckets=collections.defaultdict(list)
 for r in c['parent_old']:buckets[r['scope'],r['target']].append(r)
 result=[]
 for (s,y),b in sorted(buckets.items()):
  if name=='FIXED_HIGH':result.append(max(r['cue'] for r in b));continue
  if name=='TARGETED' and y!=c['focal']['target']:b=sorted(b,key=lambda r:(cp(r['logits'],y),r['cue']))
  else:b=sorted(b,key=lambda r:r['cue'])
  result.append(b[0]['cue'])
 return sorted(result)

def writecsv(path,rows):
 rows=list(rows)
 if not rows:path.write_text('empty\n');return
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(root,raw,out):
 out.mkdir(parents=True,exist_ok=False);cases=json.loads((root/'inputs/CANDIDATES.json').read_text());lookup={c['id']:c for c in cases};cfg=json.loads((root/'protocol/CONFIG.json').read_text())
 evidence={};requests=0
 for e in readlines(raw/'EVIDENCE.jsonl.gz'):
  c=lookup[e['candidate']];p=expected_panel(c,e['policy']);assert e['panel']==p,'PANEL_SELECTION';keys=p+(['FOCAL'] if e['policy'] not in ('ACCEPT_ALL','NEVER_ADOPT') else [])
  assert [r['key'] for r in e['requests']]==keys
  for r in e['requests']:
   cr=c['focal'] if r['key']=='FOCAL' else next(v for v in c['old'] if v['cue']==r['key'])
   assert r['response']=={k:cr[k] for k in ('cue','scope','target','logits','parameter_version','record_id','kind')};assert hd(r['response'])==r['response_sha256'];requests+=1
  evidence[c['id'],e['policy']]=e
 completed={};intents={};last='0'*64;seq=0
 for row in readlines(raw/'JOURNAL.jsonl.gz'):
  seq+=1;digest=row.pop('sha256');assert row['prev']==last and row['sequence']==seq and hd(row)==digest,'JOURNAL_CHAIN';last=digest
  ev=row['event'];key=(ev['candidate'],ev['policy'],ev['profile'])
  if ev['type']=='REVIEW_INTENT':assert key not in intents;intents[key]=ev
  else:assert key in intents and key not in completed;completed[key]=ev
 counts=json.loads((raw/'COUNTS.json').read_text());assert counts['journal_terminal']=={'count':seq,'sha256':last}
 scored=[];norms=0.;scorelookup={}
 for row in readlines(raw/'DECISIONS.jsonl.gz'):
  c=lookup[row['candidate']];pol=row['policy'];lim=cfg['profiles'][row['profile']];key=(c['id'],pol,row['profile'])
  assert completed[key]['result_sha256']==hd(row);assert row['evidence_sha256']==hd(evidence[c['id'],pol])
  if pol=='ACCEPT_ALL':want=True;reasons=[];metrics={}
  elif pol=='NEVER_ADOPT':want=False;reasons=['STATIC_PARENT'];metrics={}
  else:want,reasons,metrics=evaluate(c,row['panel'],lim)
  assert row['accept']==want and row['reasons']==reasons,('DECISION',key)
  for k,v in metrics.items():norms=max(norms,abs(row['metrics'][k]-v));assert abs(row['metrics'][k]-v)<2e-14,(key,k)
  ok,why,full=evaluate(c,list(range(8)),lim);taken=row['accept'];pfo=c['parent_focal'];fo=c['focal'];cur=fo['target']
  selected=fo if taken else pfo;fcorrect=int(np.argmax(selected['logits'])==cur);old=c['old'] if taken else c['parent_old']
  selectedoldp=sum(cp(r['logits'],r['target']) for r in old)/8;parentoldp=sum(cp(r['logits'],r['target']) for r in c['parent_old'])/8
  loggain=(nll(pfo['logits'],cur)-nll(fo['logits'],cur)+sum(nll(a['logits'],a['target'])-nll(b['logits'],b['target']) for a,b in zip(c['parent_old'],c['old'])))/9
  rec={'candidate':c['id'],'source':c['source'],'phase':c['phase'],'method':c['method'],'fit':c['fit'],'base':c['base'],'session':c['session'],'profile':row['profile'],'policy':pol,'accepted':int(taken),'full_eligible':int(ok),'acceptable_retained':int(taken and ok),'unacceptable_adopted':int(taken and not ok),'acceptable_deferred':int(not taken and ok),'appropriate_defer':int(not taken and not ok),'full_reasons':'|'.join(why),'panel_reasons':'|'.join(reasons),'panel':','.join(map(str,row['panel'])),'candidate_net_probability_gain':full['net_probability_gain'],'retained_net_probability_gain':full['net_probability_gain'] if taken else 0.,'acceptable_potential_gain':full['net_probability_gain'] if ok else 0.,'acceptable_retained_gain':full['net_probability_gain'] if taken and ok else 0.,'missed_acceptable_gain':full['net_probability_gain'] if not taken and ok else 0.,'focal_available_correct':fcorrect,'candidate_focal_p':full['focal_probability'],'chosen_focal_p':cp(selected['logits'],cur),'chosen_old_mean_p':selectedoldp,'chosen_old_p_drop':parentoldp-selectedoldp,'chosen_old_class_errors':sum(int(np.argmax(r['logits'])!=r['target']) for r in old),'chosen_mean_logloss_gain':loggain if taken else 0.,'full_old_mean_drop':full['old_mean_drop'],'full_old_worst_drop':full['old_worst_drop'],'full_old_min_p':full['old_min_probability'],'aliases':len(c['aliases'])}
  scored.append(rec);scorelookup[key]=rec
 assert len(scored)==counts['review_evaluations']==len(completed)==len(intents);assert requests==counts['candidate_measurement_lookups']
 # Per-source/per-method, all finite-panel errors and true positives remain available.
 groups=collections.defaultdict(list)
 for r in scored:groups[(r['source'],r['phase'],r['method'],r['profile'],r['policy'])].append(r)
 summaries=[]
 for k,rs in sorted(groups.items()):
  n=len(rs);s=dict(zip(('source','phase','method','profile','policy'),k));s['proposals']=n;s['contexts']=len(set(r['session'] for r in rs));s['bases']=len(set(r['base'] for r in rs))
  for f in ('accepted','full_eligible','acceptable_retained','unacceptable_adopted','acceptable_deferred','appropriate_defer','focal_available_correct','chosen_old_class_errors'):s[f]=sum(r[f] for r in rs)
  for f in ('retained_net_probability_gain','acceptable_potential_gain','acceptable_retained_gain','missed_acceptable_gain','chosen_focal_p','chosen_old_p_drop','chosen_mean_logloss_gain'):s['mean_'+f]=sum(r[f] for r in rs)/n
  s['false_adoption_per_proposal']=s['unacceptable_adopted']/n;s['missed_acceptable_per_proposal']=s['acceptable_deferred']/n;s['miss_rate_among_acceptable']=s['acceptable_deferred']/s['full_eligible'] if s['full_eligible'] else ''
  summaries.append(s)
 paired=[];sg={tuple(s[f] for f in ('source','phase','method','profile','policy')):s for s in summaries}
 for key,s in sorted(sg.items()):
  if key[-1]!='TARGETED':continue
  for opp in ('FIXED_LOW','FIXED_HIGH'):
   b=sg[key[:-1]+(opp,)];harm=s['false_adoption_per_proposal']-b['false_adoption_per_proposal'];miss=s['missed_acceptable_per_proposal']-b['missed_acceptable_per_proposal'];v=s['mean_acceptable_retained_gain'];v0=b['mean_acceptable_retained_gain'];ratio=v/v0 if v0>0 else None
   paired.append({**dict(zip(('source','phase','method','profile'),key[:-1])),'opponent':opp,'change_false_adoption_rate':harm,'change_missed_acceptable_rate':miss,'retained_acceptable_gain_ratio':ratio,'focal_availability_difference':(s['focal_available_correct']-b['focal_available_correct'])/s['proposals'],'usefulness_signal':bool(harm<0 and miss<=.05 and v>=.95*v0)})
 writecsv(out/'CANDIDATE_DECISIONS.csv',scored)
 writecsv(out/'SUMMARY.csv',summaries);writecsv(out/'PAIRED_POLICY_EFFECTS.csv',paired)
 writecsv(out/'FAILURES.csv',[r for r in scored if r['unacceptable_adopted'] or r['acceptable_deferred']])
 # Publish source-stage offers, keeping genuine repeated versions as alias rows, not extra independent proposals.
 stage=[]
 for c in cases:
  for alias in c['aliases']:
   for pol in cfg['policies']:
    r=scorelookup[c['id'],pol,'MODERATE'];stage.append({k:r[k] for k in ('candidate','source','phase','method','fit','base','session','policy','accepted','full_eligible','unacceptable_adopted','acceptable_deferred','focal_available_correct','retained_net_probability_gain')}|{'branch':alias['branch'],'trial':alias['trial'],'stage':alias['stage']})
 writecsv(out/'STAGE_OFFERS.csv',stage)
 offergroups=collections.defaultdict(list)
 for r in stage:offergroups[(r['source'],r['phase'],r['method'],r['fit'],r['base'],r['session'],r['branch'],r['policy'])].append(r)
 latency=[]
 for key,rs in sorted(offergroups.items()):
  offered=[r['trial'] for r in rs if r['accepted'] and r['full_eligible']];earliest=min(offered) if offered else None
  latency.append(dict(zip(('source','phase','method','fit','base','session','branch','policy'),key))|{'first_acceptable_offer_receipt':earliest,'available_by_receipt4':int(earliest is not None and earliest<=4),'never_acceptable_in_recorded_offers':int(earliest is None),'not_a_closed_loop_adoption_trajectory':True})
 writecsv(out/'OFFER_AVAILABILITY.csv',latency)
 baseg=collections.defaultdict(list)
 for r in scored:baseg[(r['source'],r['phase'],r['method'],r['base'],r['profile'],r['policy'])].append(r)
 baserows=[]
 for key,rs in sorted(baseg.items()):baserows.append(dict(zip(('source','phase','method','base','profile','policy'),key))|{'proposals':len(rs),'bad_adoptions':sum(r['unacceptable_adopted'] for r in rs),'acceptable_missed':sum(r['acceptable_deferred'] for r in rs),'focal_available':sum(r['focal_available_correct'] for r in rs),'mean_retained_gain':sum(r['retained_net_probability_gain'] for r in rs)/len(rs)})
 writecsv(out/'BASE_RESULTS.csv',baserows)
 (out/'AUDIT.json').write_text(json.dumps({'status':'PASS','candidate_count':len(cases),'decisions_independently_checked':len(scored),'requested_records_checked':requests,'journal_events':seq,'max_numeric_discrepancy':norms,'false_or_missed_rows_preserved':sum(r['unacceptable_adopted']+r['acceptable_deferred'] for r in scored),'no_import_of_producer_or_policy':True,'neural_calls':0,'optimizer_updates':0},sort_keys=True,indent=2)+'\n')
 print((out/'AUDIT.json').read_text())

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--raw',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.root,a.raw,a.out)
