from pathlib import Path
import tempfile,unittest,json,copy
from unittest.mock import patch
import numpy as np,torch
from q010r.conditions import condition_cells
from q010r.models import load_parent_reader,PublicInput,compose_read
from q010r.store import OwnedRecordStore,STORE_ARRAY_NAMES
from q010r import evaluation as ev
from q010c.batch_core import *
from q010c.protocol import build_criteria,counts_for,SEEDS

class BatchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):torch.set_num_threads(1)
 def cases(self,c):
  allcases=prepare_cases(c,9004,split='development');return [allcases[0],allcases[64]]
 def same(self,bs,sc,i):
  for n in STORE_ARRAY_NAMES:
   np.testing.assert_array_equal(getattr(bs.state,n)[i:i+1].numpy(),getattr(sc.state,n).numpy(),err_msg=n)
 def test_parent_state_initialization_supported_and_missing(self):
  for length in (1,4,8):
   c=next(x for x in condition_cells() if x.condition_id==f'core_assisted_l{length:02d}_d08');cases=self.cases(c);bs=BatchStore.initialize(cases)
   for i,g in enumerate(cases):self.same(bs,OwnedRecordStore.from_case(g,run_id='x',protocol_id='x',model_id='x'),i)
 def test_declared_faults_exact_source_parity(self):
  seen=[]
  for cell in condition_cells():
   if cell.factors.get('fault') in (None,'none'):continue
   seen.append(cell.condition_id);cases=self.cases(cell);bs=BatchStore.initialize(cases);bs.fault(cell,9004,'development')
   for i,g in enumerate(cases):
    sc=OwnedRecordStore.from_case(g,run_id='x',protocol_id='x',model_id='x');ev._apply_declared_fault(cell,g,sc,paired_seed=9004,episode_index=case_index(g));self.same(bs,sc,i)
  self.assertEqual(len(seen),7)
 def test_noise_maintenance_write_exact_scalar_state(self):
  cell=next(c for c in condition_cells() if c.condition_id=='durability_sigma02_cadence08_livewrite64');cases=self.cases(cell);bs=BatchStore.initialize(cases);scalars=[OwnedRecordStore.from_case(c,run_id='x',protocol_id='x',model_id='x') for c in cases]
  for event in range(1,65):
   seeds=bs.noise_event(cell,9004,event,'development')
   for sc,seed in zip(scalars,seeds):sc.inject_noise(np.random.default_rng(int(seed)),.02,fields='both',operation_id=f'e{event}')
   if event%8==0:
    bs.maintain()
    for sc in scalars:sc.maintain(ev._maintenance_resolver,policy='internal',fields='both',value_restorer=ev._maintenance_resolver)
   if event%64==0:
    bs.unrelated_write()
    for c,sc in zip(cases,scalars):sc.correct(int(c.displaced_decoy_id),dict(c.truth_edges)[int(c.displaced_decoy_id)],transaction_id=f'w{event}')
   for i,sc in enumerate(scalars):self.same(bs,sc,i)
 def test_raw_nearest_feedback_no_golden_target(self):
  cell=next(c for c in condition_cells() if c.condition_id=='core_assisted_l08_d08');cases=self.cases(cell);bs=BatchStore.initialize(cases);q,ids,_=prepare_queries(cases,cell,9004,split='development');m,_=load_parent_reader(801);got=read_batch(bs.state,bs.symbols,q,ids,m,depth=8,feedback_mode='assisted',reader_id='inherited_801')
  self.assertEqual(got['query'].shape,(2,8,17));self.assertTrue(got['state_unchanged'].all())
  np.testing.assert_array_equal(got['query'][:,1:],got['clean_code'][:,:-1])
  # UNKNOWN remains a complete eight-stage chain, not truncated execution.
  self.assertEqual(got['read_code'].shape[1],8)
 def test_exact_owner_logits_match_supplied_control(self):
  cell=condition_cells()[0];cases=self.cases(cell);bs=BatchStore.initialize(cases)
  ids=np.array([c.query_symbol_id for c in cases]);logits=exact_logits(bs.state,bs.symbols,ids)
  for i,c in enumerate(cases):
   sc=OwnedRecordStore.from_case(c,run_id='x',protocol_id='x',model_id='x');m=ev.ExactOwnerControlReader(sc);m.bind_source(int(ids[i]));out=m.forward_step(sc.public_input(c.query),0);np.testing.assert_array_equal(logits[i].numpy(),out.selection_logits[0].numpy())
 def test_close_identity_matches_generator(self):
  seen=[]
  for cell in condition_cells():
   if 'identity_role' not in cell.factors:continue
   seen.append(cell.condition_id)
   for c in self.cases(cell):
    i=case_index(c);base=ev.make_condition_case(cell,paired_seed=9004,episode_index=i,arm='paired_eval',split='development')
    expected=ev.make_close_identity_case(base,role=cell.factors['identity_role'],paired_seed=9004,sigma=.01)
    np.testing.assert_array_equal(c.book,expected.book)
    self.assertFalse(np.array_equal(c.book,base.book))
  self.assertEqual(len(seen),3)
 def test_lifecycle_actual_actions_do_not_invent_live_facts(self):
  col=collect_lifecycle(9004);self.assertEqual(len(col.frames),12)
  for f in col.frames:
   self.assertEqual(f['condition_id']=='pre_registration_query' and len(f['facts'])>0,False)
  for name in ('pre_registration_query','registration_without_fact','clear','scope_reset'):
   f=next(x for x in col.frames if x['condition_id']==name);self.assertNotIn(f['source_id'],f['facts'])
 def test_criteria_original_independent_schema_and_exact_workload(self):
  c=build_criteria();self.assertEqual(len(c['conditions']),64);total=sum(sum(sum(rs.values()) for rs in seed.values()) for seed in c['coverage']['chains_per_condition_seed_reader'].values());self.assertEqual(total,449640)
  cells=condition_cells();stages=sum(cell.episodes_per_seed*(len(cell.factors.get('evaluation_checkpoints',[0])))*(1 if cell.stratum=='lifecycle' or cell.factors.get('feedback_mode')=='direct' else cell.factors.get('allowed_depth',min(cell.factors.get('path_length',3),4)))*30 for cell in cells);self.assertEqual(stages,3045480)

if __name__=='__main__':unittest.main()
