"""New recovery-adapter tests; not the absent original Study010 test suite."""
import unittest,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'reference/parent009'))
import torch,numpy as np
from nbr009.common import load_pair,setup,weights_hash,data
from recovery.cap_variant import CapOnlyRecordHop
class RecoveryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  setup();cls.ms,cls.head,cls.cfg=load_pair(1);cls.base=cls.ms['record_hop']
  cls.p=data.batch(np.random.default_rng(9180123),b=8,max_h=8)
  cls.args=tuple(torch.from_numpy(cls.p[k]) for k in ('keys','vals','present','q'))
 def test_real_parameter_count(self):self.assertEqual(sum(p.numel() for p in self.base.parameters()),818)
 def test_cap_preserves_actual_weights(self):self.assertEqual(weights_hash(self.base),weights_hash(CapOnlyRecordHop(self.base)))
 def test_exact_old_forward_at_cap80(self):
  with torch.no_grad():
   a=self.base(*self.args,8);b=CapOnlyRecordHop(self.base,80)(*self.args,8)
  self.assertTrue(torch.equal(a,b))
 def test_cap_parameter_budget_unchanged(self):self.assertEqual(sum(p.numel() for p in CapOnlyRecordHop(self.base).parameters()),818)
 def test_no_training_enabled(self):self.assertFalse(any(p.requires_grad for p in CapOnlyRecordHop(self.base).parameters()))
 def test_bad_cap_rejected(self):
  for c in [0,-1,float('inf'),float('nan')]:
   with self.assertRaises(ValueError):CapOnlyRecordHop(self.base,c)
 def test_wrong_reader_rejected(self):
  with self.assertRaises(ValueError):CapOnlyRecordHop(self.ms['gated_hop'])
 def test_bad_depth_rejected(self):
  with self.assertRaises(ValueError):CapOnlyRecordHop(self.base)(*self.args,0)
 def test_forward_no_weight_change(self):
  h=weights_hash(self.base);m=CapOnlyRecordHop(self.base)
  with torch.no_grad():out=m(*self.args,8)
  self.assertTrue(torch.isfinite(out).all());self.assertEqual(h,weights_hash(self.base));self.assertEqual(h,weights_hash(m))
 def test_new_main_weights_explicitly_missing(self):
  obj=json.loads((ROOT/'spec/RECONSTRUCTION_JOB_LEDGER.json').read_text())
  self.assertEqual(len(obj['main_jobs']),15)
  self.assertTrue(all(j['output_checkpoint'] is None and j['expected_result'] is None for j in obj['main_jobs']))
if __name__=='__main__':unittest.main()
