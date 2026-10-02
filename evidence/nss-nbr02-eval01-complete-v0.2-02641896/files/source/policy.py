"""Operational evaluator/reviewer: only public parent data and requested measurements.
No model, source-archive, candidate pool, or research-scorer access in this module.
"""
import math

def probability(z,y):
 if type(y) is not int or y not in (0,1):raise ValueError('TARGET_TYPE')
 if not isinstance(z,list) or len(z)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in z):raise ValueError('NONFINITE_OR_MALFORMED_LOGITS')
 m=z[y]-z[1-y]
 return 1/(1+math.exp(-m)) if m>=0 else math.exp(m)/(1+math.exp(m))

def validate(public):
 for field in ('permitted','source_bound','completed'):
  if type(public.get(field)) is not bool:raise ValueError('BOOLEAN_TYPE:'+field)
  if not public[field]:raise ValueError('UNESTABLISHED:'+field)
 if public['parent_version']!=public['anchor_version']:raise ValueError('UNSUPPORTED_ROLLING_PARENT')
 if len(public['old_reference'])!=8:raise ValueError('OLD_REFERENCE_COVERAGE')
 for r in public['old_reference']:
  probability(r['logits'],r['target'])
  if type(r['cue']) is not int or r['cue'] not in range(8):raise ValueError('CUE_TYPE')
  if type(r['scope']) is not int or r['scope'] not in (0,1):raise ValueError('SCOPE_TYPE')
  if not r['receipt'].get('receipt'):raise ValueError('MISSING_RECEIPT')
 probability(public['parent_focal_logits'],public['target'])

def select(public,kind):
 validate(public)
 if kind in ('ACCEPT_ALL','NEVER_ADOPT'):return []
 if kind=='FULL_PANEL':return list(range(8))
 groups={}
 for row in public['old_reference']:groups.setdefault((row['scope'],row['target']),[]).append(row)
 if len(groups)!=4 or any(len(rs)!=2 for rs in groups.values()):raise ValueError('UNBALANCED_CELLS')
 chosen=[]
 for (scope,label),rs in sorted(groups.items()):
  if kind=='FIXED_LOW':r=min(rs,key=lambda x:x['cue'])
  elif kind=='FIXED_HIGH':r=max(rs,key=lambda x:x['cue'])
  elif kind=='TARGETED':
   r=min(rs,key=(lambda x:(probability(x['logits'],x['target']),x['cue']))) if label!=public['target'] else min(rs,key=lambda x:x['cue'])
  else:raise ValueError('UNKNOWN_POLICY')
  chosen.append(r['cue'])
 if len(set(chosen))!=4:raise ValueError('DUPLICATE_PANEL')
 return sorted(chosen)

def decide(public,measurements,cfg,kind):
 validate(public)
 if kind=='ACCEPT_ALL':return {'accept':True,'reasons':[],'metrics':{},'coverage':'no_candidate_checks'}
 if kind=='NEVER_ADOPT':return {'accept':False,'reasons':['STATIC_PARENT'],'metrics':{},'coverage':'no_candidate_checks'}
 old=[r for r in measurements if r['kind']=='old'];fs=[r for r in measurements if r['kind']=='focal']
 n=8 if kind=='FULL_PANEL' else 4
 if len(old)!=n or len(fs)!=1 or len(set(r['cue'] for r in old))!=n:raise ValueError('MEASUREMENT_COUNT')
 refs={r['cue']:r for r in public['old_reference']};deltas=[];ps=[];lost=0
 for r in measurements:
  if r['parameter_version']!=public['candidate_version']:raise ValueError('MEASUREMENT_VERSION')
  if r['kind']=='old' and (r['target']!=refs[r['cue']]['target'] or r['scope']!=refs[r['cue']]['scope']):raise ValueError('TARGET_VERSION')
 for r in old:
  ref=refs[r['cue']];p=probability(r['logits'],r['target']);p0=probability(ref['logits'],ref['target']);deltas.append(p-p0);ps.append(p)
  lost+=int(int(ref['logits'][1]>ref['logits'][0])==r['target'] and int(r['logits'][1]>r['logits'][0])!=r['target'])
 f=fs[0]
 if f['target']!=public['target'] or f['cue']!=public['focal_cue']:raise ValueError('FOCAL_TARGET')
 pf=probability(f['logits'],public['target']);pf0=probability(public['parent_focal_logits'],public['target']);fg=pf-pf0
 avg=sum(deltas)/n
 stats={'focal_probability':pf,'focal_gain':fg,'old_mean_drop':-avg,'old_worst_drop':max(-x for x in deltas),'old_min_probability':min(ps),'old_class_loss_rate':lost/n,'net_probability_gain':(8*avg+fg)/9}
 reasons=[]
 if pf<cfg['focal_floor']:reasons.append('FOCAL_FLOOR')
 if fg<cfg['focal_gain']:reasons.append('FOCAL_GAIN')
 if -avg>cfg['old_mean_drop']:reasons.append('OLD_MEAN_DROP')
 if max(-x for x in deltas)>cfg['old_worst_drop']:reasons.append('OLD_WORST_DROP')
 if min(ps)<cfg['old_floor']:reasons.append('OLD_FLOOR')
 if lost/n>cfg['old_error_rate']:reasons.append('OLD_CLASS_LOSS')
 if stats['net_probability_gain']<=0:reasons.append('NO_NET_GAIN')
 return {'accept':not reasons,'reasons':reasons,'metrics':stats,'coverage':f'{n}/8_old_plus_focal'}
