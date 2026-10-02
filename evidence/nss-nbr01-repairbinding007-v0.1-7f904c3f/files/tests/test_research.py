import unittest,tempfile,json
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from nbr007 import ROOT,repair,snapshot
from nbr007.evaluate import problem,exposure,scores
from nbr006 import data,models,common as c
from nbr006.store import RecordStore

class RepairTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):c.setup(1)
 def setUp(self):
  self.p=problem(8120,b=8);self.k,self.v,self.e,self.q,self.book=data.tensors(self.p)
 def test_nearest_exact_codes(self):self.assertTrue(torch.equal(repair.apply('nearest',self.book,self.book),self.book))
 def test_nearest_rejects_erasure(self):self.assertTrue(torch.equal(repair.apply('nearest',self.q[:,None,:]*0,self.book)[:,0],self.book[:,-1]))
 def test_nearest_small_noise(self):
  x=self.book+torch.randn_like(self.book)*.001;self.assertTrue(torch.equal(repair.apply('nearest',x,self.book),self.book))
 def test_noop_identity(self):self.assertIs(repair.apply('none',self.k,self.book),self.k)
 def test_normalization(self):self.assertTrue(torch.allclose(repair.apply('normalize',self.book*3,self.book).norm(dim=-1),torch.ones(8,17)))
 def test_missing_model(self):
  with self.assertRaises(ValueError):repair.apply('intrinsic_mlp',self.k,self.book)
 def test_unknown_model(self):
  with self.assertRaises(ValueError):repair.make('bad')
 def test_invalid_fields(self):
  with self.assertRaises(ValueError):repair.maintain(self.k,self.v,self.e,self.book,'none',fields='bad')
 def test_empty_mask(self):
  k,v=repair.maintain(self.k,self.v,self.e,self.book,'nearest');self.assertEqual(float(k[~self.e].abs().sum()+v[~self.e].abs().sum()),0)
 def test_keyonly(self):
  k,v=repair.maintain(self.k+.01*self.e[...,None],self.v,self.e,self.book,'nearest',fields='keys');self.assertTrue(torch.equal(v,self.v));self.assertTrue(torch.equal(k,self.k))
 def test_valueonly(self):
  k,v=repair.maintain(self.k,self.v+.01*self.e[...,None],self.e,self.book,'nearest',fields='values');self.assertTrue(torch.equal(k,self.k));self.assertTrue(torch.equal(v,self.v))
 def test_unknown_code_retained(self):self.assertTrue(torch.equal(repair.apply('nearest',self.book[:,-1:],self.book),self.book[:,-1:]))
 def test_dict_permutation_equivariance(self):
  m=repair.make('learned_dictionary');a=m(self.k,self.book);b=m(self.k,self.book.flip(1));self.assertTrue(torch.allclose(a,b,atol=2e-6))
 def test_batch_independence(self):
  m=repair.make('learned_dictionary');self.assertTrue(torch.allclose(m(self.k,self.book)[:1],m(self.k[:1],self.book[:1]),atol=2e-6))
 def test_slot_permutation_equivariance(self):
  m=repair.make('learned_dictionary');self.assertTrue(torch.allclose(m(self.k,self.book).flip(1),m(self.k.flip(1),self.book),atol=2e-6))
 def test_intrinsic_no_book_access(self):
  m=repair.make('intrinsic_mlp');self.assertTrue(torch.equal(m(self.k,self.book),m(self.k,self.book*0)))
 def test_parameters_unchanged(self):
  m=repair.make('learned_dictionary');h=c.weights_hash(m)
  with torch.no_grad():repair.maintain(self.k,self.v,self.e,self.book,'learned_dictionary',m)
  self.assertEqual(h,c.weights_hash(m))
 def test_input_unchanged(self):
  before=[a.clone() for a in (self.k,self.v,self.e,self.book)];repair.maintain(self.k,self.v,self.e,self.book,'nearest')
  self.assertTrue(all(torch.equal(a,b) for a,b in zip(before,(self.k,self.v,self.e,self.book))))
 def test_same_noise_schedule(self):
  k,v=exposure(self.k,self.v,self.e,self.book,'none',{},np.random.default_rng(9),3,.02,'both')
  k2,v2=exposure(self.k,self.v,self.e,self.book,'none',{},np.random.default_rng(9),3,.02,'keys')
  self.assertTrue(torch.equal(k,k2));self.assertTrue(torch.equal(v2,self.v));self.assertFalse(torch.equal(v,v2))
 def test_no_repair_fields(self):
  a=exposure(self.k,self.v,self.e,self.book,'nearest',{},np.random.default_rng(9),3,.02,'both',maintenance_fields='none')
  b=exposure(self.k,self.v,self.e,self.book,'none',{},np.random.default_rng(9),3,.02,'both')
  self.assertTrue(all(torch.equal(x,y) for x,y in zip(a,b)))
 def test_exact_periodic_small_noise(self):
  k,v=exposure(self.k,self.v,self.e,self.book,'nearest',{},np.random.default_rng(9),30,.02,'both');self.assertTrue(torch.equal(k,self.k));self.assertTrue(torch.equal(v,self.v))
 def test_targets_known_missing_balanced(self):self.assertEqual(int((data.oracle_answer(self.p)==16).sum()),4)
 def test_scoring_unresolved_not_unknown(self):
  pred=self.p['query'].copy();r=scores(pred,self.p);self.assertEqual(r['unknown_accuracy'],0);self.assertEqual(r['accuracy'],0)
 def test_no_relations_in_repair_api(self):
  # Shuffling values changes graph edges but not the identity dictionary.
  x=repair.apply('nearest',self.q[:,None,:],self.book)
  self.p['parent'][:]=16;y=repair.apply('nearest',self.q[:,None,:],self.book);self.assertTrue(torch.equal(x,y))

class SnapshotTests(unittest.TestCase):
 def setUp(self):
  c.setup(1);self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'s.npz'
  p=problem(881,b=8);self.k,self.v,self.e,self.q,self.book=data.tensors(p);self.ids={'reader':'a','binder':'b','repair':'c','dictionary_schema':'identity17-v1'}
  self.rng=np.random.default_rng(91)
  snapshot.save(self.path,self.k,self.v,self.e,self.book,self.q,self.rng,self.ids,'scope',2)
 def tearDown(self):self.tmp.cleanup()
 def test_roundtrip(self):
  a,r,d=snapshot.load(self.path,self.ids,'scope');self.assertEqual(d,2);self.assertTrue(all(torch.equal(x,y) for x,y in zip(a,(self.k,self.v,self.e,self.book,self.q))));self.assertEqual(r.random(),self.rng.random())
 def test_scope_rejection(self):
  with self.assertRaises(ValueError):snapshot.load(self.path,self.ids,'other')
 def test_weight_rejection(self):
  with self.assertRaises(ValueError):snapshot.load(self.path,{**self.ids,'repair':'new'},'scope')
 def test_damage_rejection(self):
  self.path.write_bytes(self.path.read_bytes()+b'x')
  with self.assertRaises(ValueError):snapshot.load(self.path,self.ids,'scope')
 def test_abi_rejection(self):
  p=self.path.with_suffix('.json');m=json.loads(p.read_text());m['abi']='old';p.write_text(json.dumps(m))
  with self.assertRaises(ValueError):snapshot.load(self.path,self.ids,'scope')
 def test_nonfinite_rejection(self):
  self.k[0,0,0]=float('nan')
  with self.assertRaises(ValueError):snapshot.save(self.path,self.k,self.v,self.e,self.book,self.q,self.rng,self.ids,'scope')
 def test_dtype_rejection(self):
  with self.assertRaises(ValueError):snapshot.save(self.path,self.k.double(),self.v,self.e,self.book,self.q,self.rng,self.ids,'scope')
 def test_shape_rejection(self):
  with self.assertRaises(ValueError):snapshot.save(self.path,self.k,self.v[:,:,:16],self.e,self.book,self.q,self.rng,self.ids,'scope')
 def test_dirty_empty_rejection(self):
  self.k[~self.e]=1
  with self.assertRaises(ValueError):snapshot.save(self.path,self.k,self.v,self.e,self.book,self.q,self.rng,self.ids,'scope')
 def test_round_rejection(self):
  with self.assertRaises(ValueError):snapshot.save(self.path,self.k,self.v,self.e,self.book,self.q,self.rng,self.ids,'scope',9)
if __name__=='__main__':unittest.main()
