"""Finite contract and data-access regression fixtures, not neural task cases."""
import copy,json,math
from pathlib import Path
import policy
from run_review import EvidenceAPI

def run(root):
 old=[{'cue':i,'scope':i//4,'target':(i%4)//2,'logits':[3.,-3.] if (i%4)//2==0 else [-3.,3.],'receipt':{'receipt':str(i)},'record_id':str(i)} for i in range(8)]
 pub={'id':'test','permitted':True,'source_bound':True,'completed':True,'parent_version':'a','anchor_version':'a','candidate_version':'b','target':1,'focal_cue':9,'current_receipt':{'receipt':'new'},'parent_focal_logits':[3.,-3.],'old_reference':old}
 measured=[{**r,'kind':'old','parameter_version':'b'} for r in old]+[{'cue':9,'scope':0,'target':1,'kind':'focal','logits':[-2.,2.],'parameter_version':'b','record_id':'f'}]
 cfg=json.loads((root/'protocol/CONFIG.json').read_text())['profiles']['MODERATE'];rows=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,StopIteration) as e:rows.append({'test':name,'pass':True,'caught':str(e)});return
  raise AssertionError(name+' not rejected')
 for flag in ('permitted','source_bound','completed'):
  x=copy.deepcopy(pub);x[flag]='false';reject('strict_boolean_'+flag,lambda:policy.select(x,'FIXED_LOW'))
 x=copy.deepcopy(pub);x['anchor_version']='wrong';reject('anchor_mismatch',lambda:policy.select(x,'TARGETED'))
 x=copy.deepcopy(pub);x['old_reference'][0]['logits']=[float('nan'),0.];reject('nonfinite',lambda:policy.select(x,'TARGETED'))
 x=copy.deepcopy(pub);x['old_reference'][0]['receipt']={};reject('missing_receipt',lambda:policy.select(x,'FIXED_LOW'))
 assert policy.select(pub,'FIXED_LOW')==[0,2,4,6];assert policy.select(pub,'FIXED_HIGH')==[1,3,5,7]
 rows.append({'test':'balanced_budget_panels','pass':True})
 pan=policy.select(pub,'TARGETED');m=[r for r in measured if r['kind']=='focal' or r['cue'] in pan]
 assert policy.decide(pub,m,cfg,'TARGETED')['accept'];rows.append({'test':'lawful_correction_reinterprets_parent','pass':True})
 bad=copy.deepcopy(m);bad[0]['parameter_version']='old';reject('measured_wrong_version',lambda:policy.decide(pub,bad,cfg,'TARGETED'))
 reject('missing_measurement',lambda:policy.decide(pub,m[:-1],cfg,'TARGETED'))
 case={'old':measured[:-1],'focal':measured[-1]};api=EvidenceAPI(case,pan+['FOCAL']);api.get(pan[0]);reject('duplicate_lookup',lambda:api.get(pan[0]));outside=next(i for i in range(8) if i not in pan);reject('outside_budget',lambda:api.get(outside))
 # Impossible-to-observe alteration remains absent from operational evidence.
 other=copy.deepcopy(case);other['old'][outside]['logits']=[100.,-100.]
 a=EvidenceAPI(case,pan+['FOCAL']);b=EvidenceAPI(other,pan+['FOCAL'])
 ea=[a.get(i) for i in pan+['FOCAL']];eb=[b.get(i) for i in pan+['FOCAL']]
 assert ea==eb and policy.decide(pub,ea,cfg,'TARGETED')==policy.decide(pub,eb,cfg,'TARGETED');rows.append({'test':'unrequested_data_isolation','pass':True})
 # Allow moderate small confidence movement, and do not accept no-new-learning.
 x=copy.deepcopy(m);x[-1]['logits']=pub['parent_focal_logits'];assert not policy.decide(pub,x,cfg,'TARGETED')['accept'];rows.append({'test':'no_learning_not_success','pass':True})
 (root/'audit/FIXTURES.json').write_text(json.dumps({'fixtures':rows,'count':len(rows),'model_calls':0,'synthetic':True},indent=2));print('fixture checks',len(rows))
if __name__=='__main__':import sys;run(Path(sys.argv[1]))
