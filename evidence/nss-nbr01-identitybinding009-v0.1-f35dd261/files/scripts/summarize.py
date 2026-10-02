from pathlib import Path
import sys,json,collections,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import ROOT,dump
import numpy as np
rows=[]
for p in sorted((ROOT/'evidence/results').glob('*_scores.json')):rows.extend(json.loads(p.read_text()))
groups=collections.defaultdict(list)
for r in rows:
 key=tuple(sorted((k,v) for k,v in r.items() if k not in ('pair','n','correct','rate')));groups[key].append(r)
summary=[]
for key,group in groups.items():
 vals=[r['rate'] for r in group];summary.append(dict(key)|{'pairs':len(group),'mean':float(np.mean(vals)),'sample_sd':float(np.std(vals,ddof=1)) if len(vals)>1 else 0,'minimum':min(vals),'maximum':max(vals),'n':sum(r['n'] for r in group),'success_count':sum(r['correct'] for r in group),'per_pair':{r['pair']:r['rate'] for r in group}})
dump(ROOT/'SUMMARY.json',{'status':'RUN','raw_metric_rows':len(rows),'aggregate_rows':len(summary),'groups':summary})

def show(stage,**fil):
 for r in summary:
  if r['stage']==stage and all(r.get(k)==v or (isinstance(v,list) and r.get(k) in v) for k,v in fil.items()):print({k:v for k,v in r.items() if k not in ('per_pair','maximum','minimum')})
if __name__=='__main__':
 print('A close/moderate owner results');show('A',family=['source01','source10'],phase='write_new',reader='store',metric=['all_relations_correct','wrong_owner_commit'],variant=['identity','parent','ordinary','near','guard_near'])
 print('A exact store, frozen reader');show('A',variant='identity',phase='write_new',reader=['record_hop','exact_owner'],metric='answers_joint')
 print('B long cadence');show('B',condition=['long_shared_A_c32','long_internal_A_c32','long_nearest_c32','long_owner_keys_c32','long_recover_values_c32','long_shared_B_c32','long_internal_B_c32'],reader='record_hop',depth=8,metric=['supported','missing'])
 print('CUE');show('CUE',family=['known_q20','near_novel','novel','second_missing','second_conflicting','both_common_noise','novel_both_near'],metric='correct')
