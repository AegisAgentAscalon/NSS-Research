from pathlib import Path
import json,math,collections,statistics,sys
ROOT=Path(__file__).resolve().parents[1]
def stats(v):
 v=[x for x in v if x is not None]
 return {'mean':statistics.mean(v) if v else None,'sd':statistics.stdev(v) if len(v)>1 else 0.,'min':min(v) if v else None,'max':max(v) if v else None,'pairs':v}
def wilson(k,n):
 if not n:return None
 z=1.959963984540054;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return [center-half,center+half]
def main():
 membership=[];state=[];configs=[]
 for pair in range(1,6):
  a=json.loads((ROOT/f'results/membership_pair{pair}.json').read_text());b=json.loads((ROOT/f'results/state_pair{pair}.json').read_text());membership+=a['rows'];state+=b['rows'];configs.append({'pair':pair,'state_cases':b['n_cases'],'state_rows':b['n_rows'],'state_seconds':b['seconds'],'max_rss_kib':b['environment']['max_rss_kib']})
 mg=collections.defaultdict(list);sg=collections.defaultdict(list)
 for r in membership:mg[(r['family'],r['count'],r['method'])].append(r)
 for r in state:sg[(r['case'],r['method'],r['reader'],r['depth'])].append(r)
 mrows=[];srows=[]
 for (f,c,m),rs in sorted(mg.items()):
  mrows.append({'family':f,'count':c,'method':m,**{key:stats([r[key] for r in rs]) for key in ['correct_identity','accepted','false_accept','wrong_known']},'false_accept_intervals':[{'pair':r['pair'],'k':r['accept_n'],'n':r['n'],'wilson95':wilson(r['accept_n'],r['n'])} for r in rs] if rs[0]['false_accept'] is not None else None})
 for (case,m,reader,d),rs in sorted(sg.items()):
  srows.append({'case':case,'method':m,'reader':reader,'depth':d,**{key:stats([r[key] for r in rs]) for key in ['known_accuracy','unknown_accuracy','unsupported_room_rate','accuracy']}})
 # Keep the original screens. Heavy query20 failures cannot be hidden by overall averages.
 decisions=[]
 for pair in range(1,6):
  for m in ('A_nearest','A_learned','B_nearest','B_learned'):
   mr=[r for r in membership if r['pair']==pair and r['method']==m and r['count']==16]
   known_ok=all(r['correct_identity']>=.95 for r in mr if r['family'] in ('known_exact','known_q05','known_q20','known_raw02','known_raw08'))
   novel_ok=all(r['false_accept']<=.01 for r in mr if r['family'] in ('novel','novel_noisy20'))
   core=[r for r in state if r['pair']==pair and r['method']==m and r['reader']=='record_hop' and r['depth']==8 and ((r['case'].startswith('storage/') and '08_' not in r['case']) or r['case'] in ('query/known_q05','query/known_q20'))]
   retrieval_ok=all(r['known_accuracy'] is None or r['known_accuracy']>=.95 for r in core)
   missing_ok=all(r['unknown_accuracy'] is None or r['unknown_accuracy']>=.95 for r in core)
   novel_answer=[r for r in state if r['pair']==pair and r['method']==m and r['reader']=='record_hop' and r['depth']==8 and r['case']=='query/novel'][0]['unsupported_room_rate']<=.01
   life=[r for r in state if r['pair']==pair and r['method']==m and r['reader']=='record_hop' and r['depth']==8 and r['case'].startswith(('registration/','neighbor/'))]
   life_ok=all(r['accuracy']>=.95 for r in life)
   refmethod='learned' if m.endswith('learned') else 'nearest';regression=[]
   for r in core:
    base=next(z for z in state if z['pair']==pair and z['method']==refmethod and z['reader']=='record_hop' and z['depth']==8 and z['case']==r['case'])
    if r['known_accuracy'] is not None:regression.append(base['known_accuracy']-r['known_accuracy'])
   regression_ok=max(regression)<=.01
   decisions.append({'pair':pair,'method':m,'identity_known95':known_ok,'identity_novel1':novel_ok,'core_retrieval95':retrieval_ok,'core_missing95':missing_ok,'novel_terminal1':novel_answer,'lifecycle95':life_ok,'regression1pp':regression_ok,'joint_pass':all([known_ok,novel_ok,retrieval_ok,missing_ok,novel_answer,life_ok,regression_ok])})
 output={'membership':mrows,'state':srows,'screens':decisions,'counts':{'pairs':5,'new_fits':5,'membership_rows':len(membership),'membership_answer_evaluations':sum(r['n'] for r in membership),'state_rows':len(state),'state_answer_evaluations':sum(r['n'] for r in state),'state_cases':sum(c['state_cases'] for c in configs)},'configurations':configs}
 (ROOT/'SUMMARY.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output['counts']));print('joint passes',sum(x['joint_pass'] for x in decisions))
if __name__=='__main__':main()
