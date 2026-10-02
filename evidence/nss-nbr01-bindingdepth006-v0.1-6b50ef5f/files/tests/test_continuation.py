import unittest,tempfile,json
from pathlib import Path
import numpy as np
import torch
from nbr006 import common as c,data,models
from nbr006.continuation import QueryRunner
from nbr006.verify import truths
from nbr006.exact_eval import ExactReader
c.setup(1)
class TestContinuation(unittest.TestCase):
 def setUp(self):self.p=data.batch(np.random.default_rng(45),4,max_h=8,hops=8);self.a=data.tensors(self.p)
 def test_query_equivalence(self):
  for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']:
   m=models.make(kind);q=QueryRunner(m,kind,*self.a[:4]);direct=m(*self.a[:4],8)
   for j in range(8):self.assertTrue(torch.equal(q.advance(1),direct[:,j]),(kind,j))
 def test_query_resume(self):
  for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']:
   m=models.make(kind);q=QueryRunner(m,kind,*self.a[:4]);q.advance(3)
   with tempfile.TemporaryDirectory() as td:
    path=Path(td)/'s.npz';q.save(path);r=QueryRunner.load(path,m);self.assertTrue(torch.equal(q.advance(5),r.advance(5)))
 def test_query_scope(self):
  m=models.make('record_hop');q=QueryRunner(m,'record_hop',*self.a[:4])
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';q.save(p)
   with self.assertRaises(ValueError):QueryRunner.load(p,m,scope='other')
 def test_query_weights(self):
  m=models.make('record_hop');q=QueryRunner(m,'record_hop',*self.a[:4])
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';q.save(p)
   with torch.no_grad():next(m.parameters()).add_(1)
   with self.assertRaises(ValueError):QueryRunner.load(p,m)
 def test_query_abi(self):
  m=models.make('record_hop');q=QueryRunner(m,'record_hop',*self.a[:4])
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';q.save(p);j=p.with_suffix('.json');v=json.loads(j.read_text());v['abi']='bad';j.write_text(json.dumps(v))
   with self.assertRaises(ValueError):QueryRunner.load(p,m)
 def test_independent_oracle(self):np.testing.assert_array_equal(truths(self.p['parent'],self.p['query']),data.oracle_answer(self.p))
 def test_exact_reader(self):
  m=ExactReader();pred=models.logits(m(*self.a[:4],8),self.a[4]).argmax(-1).numpy()
  np.testing.assert_array_equal(pred,data.targets(self.p,8))
 def test_unknown_after_clear(self):
  m=ExactReader();k,v,e,q,book=self.a
  pred=models.logits(m(k*0,v*0,e&False,q,8),book).argmax(-1).numpy();self.assertTrue((pred==16).all())
 def test_extra_rounds_are_executed_in_cycled_control(self):
  m=models.make('untied_hop4');self.assertEqual(m(*self.a[:4],8,cycle=True).shape,(4,8,17))
 def test_negative_rounds(self):
  q=QueryRunner(models.make('record_hop'),'record_hop',*self.a[:4])
  with self.assertRaises(ValueError):q.advance(-1)
if __name__=='__main__':unittest.main()
