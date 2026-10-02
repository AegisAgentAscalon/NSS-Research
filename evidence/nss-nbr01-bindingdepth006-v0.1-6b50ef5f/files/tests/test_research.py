import copy,json,tempfile,unittest
from pathlib import Path
import numpy as np
import torch
from torch import nn
from nbr006 import data,models,common as c
from nbr006.store import RecordStore
from nbr006.eval import metrics
c.setup(1)

class DotMatcher(nn.Module):
 def __init__(self):super().__init__();self.register_buffer('scale',torch.tensor(1.))
 def forward(self,q,k,e):
  sim=torch.einsum('bd,bnd->bn',q,k)*self.scale
  sim=sim.masked_fill(~e,-100)
  return torch.cat([sim,torch.full_like(sim[:,:1],.9)],-1)

class TestData(unittest.TestCase):
 def setUp(self):self.p=data.batch(np.random.default_rng(90),32,max_h=4)
 def test_oracle_matches_long_targets(self):np.testing.assert_array_equal(data.oracle_answer(self.p),data.targets(self.p,20)[:,-1])
 def test_known_exact_hops(self):
  for h in [1,2,4,8]:
   p=data.batch(np.random.default_rng(h),32,max_h=h,hops=h,missing=False)
   np.testing.assert_array_equal(data.targets(p,h)[:,-1],data.oracle_answer(p))
 def test_missing_returns_unknown(self):
  p=data.batch(np.random.default_rng(9),32,max_h=8,hops=8,missing=True)
  self.assertTrue((data.oracle_answer(p)==16).all())
 def test_fresh_codes(self):self.assertFalse(np.array_equal(self.p['codes'],data.batch(np.random.default_rng(91),32)['codes']))
 def test_room_self_facts(self):
  r=np.arange(32)[:,None];np.testing.assert_array_equal(self.p['parent'][r,self.p['rooms']],self.p['rooms'])
 def test_masked_rows_empty(self):self.assertTrue((self.p['keys'][~self.p['present']]==0).all())
 def test_determinism(self):np.testing.assert_array_equal(self.p['parent'],data.batch(np.random.default_rng(90),32,max_h=4)['parent'])
 def test_capacity_shape(self):self.assertEqual(data.batch(np.random.default_rng(9),2,n=32,max_h=8)['keys'].shape,(2,32,17))
 def test_bad_graph_size(self):
  with self.assertRaises(ValueError):data.batch(np.random.default_rng(1),2,n=4,max_h=8)
 def test_no_integer_ids_in_neural_args(self):
  a=data.tensors(self.p);self.assertEqual(len(a),5);self.assertTrue(all(x.dtype in (torch.float32,torch.bool) for x in a))

class TestStore(unittest.TestCase):
 def setUp(self):
  self.m=DotMatcher();self.s=RecordStore(2,3,self.m);self.src=torch.zeros(2,17);self.src[:,0]=1;self.val=torch.zeros(2,17);self.val[:,1]=1
 def test_empty(self):self.assertFalse(self.s.present.any())
 def test_first_write(self):self.s.event(self.src,self.val,1);self.assertEqual(int(self.s.present.sum()),2)
 def test_same_record_update(self):
  self.s.event(self.src,self.val,1);self.s.event(self.src,self.val*2,1);self.assertEqual(int(self.s.present.sum()),2);self.assertTrue((self.s.vals[:,0]==self.val*2).all())
 def test_clear_rewrite(self):
  self.s.event(self.src,self.val,1);self.s.event(self.src,self.val,-1);self.assertFalse(self.s.present.any());self.s.event(self.src,self.val,1);self.assertTrue(self.s.present[:,0].all())
 def test_absent_clear_noop(self):self.s.event(self.src,self.val,-1);self.assertFalse(self.s.present.any())
 def test_wrong_scope(self):self.s.event(self.src,self.val,1,scope='bad');self.assertFalse(self.s.present.any())
 def test_denied(self):self.s.event(self.src,self.val,1,qualified=False);self.assertFalse(self.s.present.any())
 def test_noop(self):self.s.event(self.src,self.val,0);self.assertFalse(self.s.present.any())
 def test_weight_frozen(self):
  h=c.weights_hash(self.m);self.s.event(self.src,self.val,1);self.assertEqual(h,c.weights_hash(self.m))
 def test_neighbour_untouched(self):
  self.s.event(self.src,self.val,1);self.s.event(self.val,self.src,1);self.assertTrue((self.s.vals[:,0]==self.val).all())
 def test_exhausted_capacity(self):
  s=RecordStore(2,1,self.m);s.event(self.src,self.val,1);r=s.event(self.val,self.src,1);self.assertTrue(r['capacity_rejected'].all());self.assertTrue((s.vals[:,0]==self.val).all())
 def test_global_clear(self):self.s.event(self.src,self.val,1);self.s.clear_all();self.assertFalse(self.s.present.any());self.assertEqual(float(self.s.keys.abs().sum()),0)
 def test_noop_has_no_array_effect(self):
  self.s.event(self.src,self.val,1);before=self.s.snapshot();self.s.event(self.val,self.src,1,scope='bad');self.assertTrue(all(torch.equal(x,y) for x,y in zip(before,self.s.snapshot())))
 def test_bad_op(self):
  with self.assertRaises(ValueError):self.s.event(self.src,self.val,2)
 def test_nonfinite(self):
  with self.assertRaises(ValueError):self.s.event(self.src*float('nan'),self.val,1)
 def test_state_bytes(self):self.assertEqual(self.s.bytes,2*3*(17*8+1))
 def test_state_noise_only_populated(self):self.s.perturb(np.random.default_rng(1),1);self.assertEqual(float(self.s.keys.abs().sum()),0)
 def test_restore_rng(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';rng=np.random.default_rng(2);self.s.event(self.src,self.val,1);self.s.save(p,rng);s,r=RecordStore.load(p,self.m);np.testing.assert_array_equal(rng.normal(size=20),r.normal(size=20));self.assertTrue(torch.equal(s.vals,self.s.vals))
 def test_restore_scope(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(1))
   with self.assertRaises(ValueError):RecordStore.load(p,self.m,scope='bad')
 def test_restore_revision(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(1));self.m.scale.add_(1)
   with self.assertRaises(ValueError):RecordStore.load(p,self.m)
 def test_restore_hash(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(1));p.write_bytes(p.read_bytes()+b'bad')
   with self.assertRaises(ValueError):RecordStore.load(p,self.m)
 def test_restore_abi(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(1));j=p.with_suffix('.json');obj=json.loads(j.read_text());obj['abi']='bad';j.write_text(json.dumps(obj))
   with self.assertRaises(ValueError):RecordStore.load(p,self.m)

class TestReaders(unittest.TestCase):
 def setUp(self):self.p=data.batch(np.random.default_rng(95),4);self.a=data.tensors(self.p)
 def test_shapes(self):
  for kind in ['record_hop','gated_hop','tied_aligned','fixed_aligned4','flat_gru']:
   m=models.make(kind);o=m(*self.a[:4],8);self.assertEqual(o.shape,(4,8,17));self.assertTrue(torch.isfinite(o).all())
 def test_fixed_cap(self):
  m=models.make('fixed_aligned4');o=m(*self.a[:4],8);self.assertTrue(torch.equal(o[:,3],o[:,7]))
 def test_shared_has_less_parameters(self):self.assertLess(sum(p.numel() for p in models.make('tied_aligned').parameters()),sum(p.numel() for p in models.make('fixed_aligned4').parameters()))
 def test_no_eval_weight_change(self):
  m=models.make('record_hop');h=c.weights_hash(m)
  with torch.no_grad():m(*self.a[:4],8)
  self.assertEqual(h,c.weights_hash(m))
 def test_gradients_exist(self):
  m=models.make('gated_hop');o=m(*self.a[:4],4);loss=models.logits(o,self.a[4]).square().mean();loss.backward();self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in m.parameters()))
 def test_permutation_equivariance(self):
  for kind in ['record_hop','gated_hop','tied_aligned','fixed_aligned4']:
   m=models.make(kind);k,v,e,q=self.a[:4]
   with torch.no_grad():a=m(k,v,e,q,4);b=m(k.flip(1),v.flip(1),e.flip(1),q,4)
   self.assertTrue(torch.allclose(a,b,atol=1e-5))
 def test_empty_record_hop(self):
  m=models.make('record_hop');k,v,e,q=self.a[:4];o=m(k*0,v*0,e&False,q,4)
  self.assertTrue((models.logits(o,self.a[4]).argmax(-1)==16).all())
 def test_parameters_random_not_oracle(self):
  m=models.make('record_hop');k,v,e,q=self.a[:4]
  self.assertFalse(torch.equal(m.match.q.weight,m.match.k.weight))
 def test_unknown_not_unresolved(self):
  p=data.batch(np.random.default_rng(8),8,max_h=4,hops=4,missing=True);r=metrics(np.full(8,16),p,4,'record_hop');self.assertEqual(r['unknown_accuracy'],1);self.assertEqual(r['unresolved_rate'],0)
 def test_nonterminal_is_unresolved(self):
  p=data.batch(np.random.default_rng(8),8,max_h=4,hops=4,missing=False);r=metrics(p['query'],p,1,'record_hop');self.assertEqual(r['unresolved_rate'],1);self.assertEqual(r['known_accuracy'],0)

if __name__=='__main__':unittest.main()
