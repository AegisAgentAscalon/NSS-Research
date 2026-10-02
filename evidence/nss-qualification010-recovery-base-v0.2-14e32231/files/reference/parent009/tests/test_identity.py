import unittest,tempfile,json
from pathlib import Path
import numpy as np
import torch
from nbr009.common import *
from nbr009.state import *
from nbr009.episodes import paired,build_state
from nbr009.readout import neural_read,exact_owner_read
from nbr009.stage_b import maintain
from nbr009.context import sample,decide
from nbr009.train import batch

class IdentityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  setup();cls.ms,cls.head,cls.cfg=load_pair(1)
  cls.rs={k:make_resolver(k,cls.ms,cls.head,cls.cfg) for k in ('nearest','A_nearest','B_nearest')}
 def setUp(self):
  self.p=paired(71999001,4,'source01');self.s=build_state(self.p,self.ms['binder']);self.r=np.arange(4)
  self.old=self.p['ids'][:,0];self.new=self.p['ids'][:,1];self.room=self.p['ids'][:,2]
 def val(self,ids):return torch.from_numpy(self.p['codes'][self.r,ids])
 def reg(self):return self.s.register(self.val(self.new))
 def test_denied_unchanged(self):
  a=self.s.signature();self.s.event(self.old,self.val(self.room),1,False);self.assertEqual(a,self.s.signature())
 def test_wrong_scope_unchanged(self):
  a=self.s.signature();self.s.event(self.old,self.val(self.room),1,True,'other');self.assertEqual(a,self.s.signature())
 def test_noop_unchanged(self):
  a=self.s.signature();self.s.event(self.old,self.val(self.room),0);self.assertEqual(a,self.s.signature())
 def test_registration_no_relation(self):
  keys=self.s.keys.clone();vals=self.s.vals.clone();present=self.s.present.clone();rg=self.reg();self.assertTrue(rg['added'].all());self.assertTrue(torch.equal(keys,self.s.keys));self.assertTrue(torch.equal(vals,self.s.vals));self.assertTrue(torch.equal(present,self.s.present))
 def test_duplicate_registration(self):
  self.reg();a=self.s.signature();rg=self.reg();self.assertTrue(rg['duplicate'].all());self.assertEqual(a,self.s.signature())
 def test_denied_registration(self):
  a=self.s.signature();self.s.register(self.val(self.new),False);self.assertEqual(a,self.s.signature())
 def test_full_registry(self):
  self.reg();q=torch.randn(4,17);q[:,-1]=0;q=torch.nn.functional.normalize(q,dim=-1);a=self.s.signature();rg=self.s.register(q);self.assertTrue(rg['full'].all());self.assertEqual(a,self.s.signature())
 def test_near_distinct_owner(self):
  rg=self.reg();keys=self.s.keys.clone();vals=self.s.vals.clone();pres=self.s.present.clone();rec=self.s.event(rg['handle'],self.val(self.room),1,epoch=rg['epoch']);self.assertTrue(rec['written'].all());self.assertFalse(rec['wrong_owner_commit'].any());self.assertTrue(torch.equal(vals[pres],self.s.vals[pres]));self.assertTrue(torch.equal(keys[pres],self.s.keys[pres]))
 def test_correction_owner(self):
  rg=self.reg();self.s.event(rg['handle'],self.val(self.room));target=(self.s.owner==rg['handle'][:,None]).long().argmax(-1);self.s.event(rg['handle'],self.val(self.p['ids'][:,3]));self.assertTrue(torch.equal(self.s.vals[torch.arange(4),target],self.val(self.p['ids'][:,3])))
 def test_clear_keeps_identity(self):
  rg=self.reg();self.s.event(rg['handle'],self.val(self.room));self.s.event(rg['handle'],self.val(self.room),-1);self.assertTrue(self.s.active[torch.arange(4),rg['handle']].all());self.assertFalse(((self.s.owner==rg['handle'][:,None])&self.s.present).any())
 def test_clear_then_rewrite(self):
  rg=self.reg();self.s.event(rg['handle'],self.val(self.room));self.s.event(rg['handle'],self.val(self.room),-1);rec=self.s.event(rg['handle'],self.val(self.room));self.assertTrue(rec['written'].all())
 def test_stale_handle(self):
  rg=self.reg();self.s.clear_scope();self.s.register(self.val(self.new));a=self.s.signature();rec=self.s.event(rg['handle'],self.val(self.room),epoch=rg['epoch']);self.assertFalse(rec['written'].any());self.assertEqual(a,self.s.signature())
 def test_stale_transaction(self):
  tx=self.s.prepare(self.old,self.val(self.room));self.s.event(self.old,self.val(self.p['ids'][:,3]));a=self.s.signature();rec=self.s.commit(tx);self.assertTrue(rec['stale'].all());self.assertEqual(a,self.s.signature())
 def test_registration_invalidates_transaction(self):
  tx=self.s.prepare(self.old,self.val(self.room));self.reg();a=self.s.signature();rec=self.s.commit(tx);self.assertTrue(rec['stale'].all());self.assertEqual(a,self.s.signature())
 def test_prepare_read_only(self):
  a=self.s.signature();self.s.prepare(self.old,self.val(self.room));self.assertEqual(a,self.s.signature())
 def test_invalid_operation(self):
  with self.assertRaises(ValueError):self.s.event(self.old,self.val(self.room),3)
 def test_nonfinite_value(self):
  v=self.val(self.room);v[0,0]=float('nan')
  with self.assertRaises(ValueError):self.s.event(self.old,v)
 def test_bad_registration_norm(self):
  with self.assertRaises(ValueError):self.s.register(self.val(self.new)*2)
 def test_hidden_future_code(self):
  bad=torch.from_numpy(self.p['codes'][:,:16]);active=torch.from_numpy(self.p['active'])
  with self.assertRaises(ValueError):OwnedState(bad,active,self.ms['binder'])
 def test_bad_allocation(self):
  with self.assertRaises(ValueError):OwnedState(self.s.book,self.s.active,self.ms['binder'],allocation=torch.zeros_like(self.s.allocation))
 def test_snapshot_roundtrip(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';rng=np.random.default_rng(9);self.s.save(p,rng,{'test':1});s,r,_,_=OwnedState.load(p,self.ms['binder'],{'test':1});self.assertEqual(s.signature(),self.s.signature());self.assertTrue(np.array_equal(r.normal(size=20),rng.normal(size=20)))
 def test_snapshot_contract(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(9),{'test':1})
   with self.assertRaises(ValueError):OwnedState.load(p,self.ms['binder'],{'test':2})
 def test_snapshot_scope(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(9),{})
   with self.assertRaises(ValueError):OwnedState.load(p,self.ms['binder'],{},'other')
 def test_snapshot_corruption(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(9),{});p.write_bytes(p.read_bytes()+b'bad')
   with self.assertRaises(ValueError):OwnedState.load(p,self.ms['binder'],{})
 def test_snapshot_transaction(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';tx=self.s.prepare(self.old,self.val(self.room));self.s.save(p,np.random.default_rng(9),{},transaction=tx);ss,_,_,tt=OwnedState.load(p,self.ms['binder'],{});self.s.commit(tx);ss.commit(tt);self.assertEqual(self.s.signature(),ss.signature())
 def test_parent_mismatch_snapshot(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'s.npz';self.s.save(p,np.random.default_rng(9),{});other=load_binder(2,'parent')
   with self.assertRaises(ValueError):OwnedState.load(p,other,{})
 def test_absence_not_repaired(self):
  self.s.clear_scope();self.s.register(self.val(self.old));maintain(self.s,'internal_A',self.rs);self.assertFalse(self.s.present.any());self.assertEqual(self.s.vals.abs().sum(),0)
 def test_rehydrate_key_not_value(self):
  present=self.s.present.clone();raw=torch.randn_like(self.s.vals);self.s.vals.copy_(raw);self.s.keys.add_(torch.randn_like(self.s.keys)*present[...,None]);self.s.maintain(self.rs['A_nearest'],'internal','keys');self.assertTrue(torch.equal(self.s.vals,raw));expected=self.s.book[torch.arange(4)[:,None],self.s.owner.clamp(0,15)];self.assertTrue(torch.equal(self.s.keys[present],expected[present]))
 def test_erasure_not_recovered(self):
  self.s.vals.zero_();maintain(self.s,'internal_A',self.rs);self.assertFalse(self.s.vr.any());self.assertTrue(self.s.present.any())
 def test_wrong_valid_value_survives(self):
  slot=self.s.present.long().argmax(-1);self.s.vals[torch.arange(4),slot]=self.val(self.p['ids'][:,4]);maintain(self.s,'internal_A',self.rs);self.assertTrue(torch.equal(self.s.vals[torch.arange(4),slot],self.val(self.p['ids'][:,4])))
 def test_invalid_owner_epoch(self):
  self.s.owner_epoch[self.s.present]+=1
  with self.assertRaises(ValueError):self.s.validate()
 def test_repair_refuses_invalid_owner(self):
  self.s.owner_epoch[self.s.present]+=1
  with self.assertRaises(ValueError):maintain(self.s,'internal_A',self.rs)
 def test_query_readonly(self):
  a=self.s.signature();neural_read(self.s,self.ms['record_hop'],self.rs['nearest'],self.val(self.old),8);self.assertEqual(a,self.s.signature())
 def test_queries_cannot_register(self):
  a=self.s.active.clone();neural_read(self.s,self.ms['record_hop'],self.rs['B_nearest'],self.val(self.new),8);self.assertTrue(torch.equal(a,self.s.active))
 def test_revision_check(self):
  rev=self.s.revision.copy();self.reg()
  with self.assertRaises(ValueError):self.s.validate(rev)
 def test_reset_separates_scope(self):
  self.s.clear_scope();self.assertFalse(self.s.active.any());self.assertFalse(self.s.present.any());self.assertTrue((self.s.owner==-1).all())
 def test_noise_same_draws(self):
  a=self.s.clone();b=self.s.clone();r1=np.random.default_rng(7);r2=np.random.default_rng(7);a.add_noise(r1,.02,'keys');b.add_noise(r2,.02,'both');self.assertTrue(torch.equal(a.keys,b.keys));self.assertEqual(r1.bit_generator.state,r2.bit_generator.state)
 def test_guard_no_cross_owner(self):
  s=build_state(self.p,self.ms['binder'],mode='guarded');rg=s.register(self.val(self.new));a=s.signature();rec=s.event(rg['handle'],self.val(self.room));self.assertFalse(rec['wrong_owner_commit'].any());self.assertTrue(rec['veto'].any())
 def test_unguarded_reports_cross_owner(self):
  s=build_state(self.p,self.ms['binder'],mode='learned');rg=s.register(self.val(self.new));rec=s.event(rg['handle'],self.val(self.room));self.assertTrue(rec['wrong_owner_commit'].any())
 def test_independent_registration_keeps_book(self):
  active=self.s.active.clone();book=self.s.book.clone();self.reg();self.assertTrue(torch.equal(self.s.book[active],book[active]))
 def test_bytes_include_metadata(self):
  self.assertGreater(self.s.bytes(),sum(x.numel()*x.element_size() for x in (self.s.keys,self.s.vals,self.s.book)))
 def test_matched_training_rng(self):
  a=np.random.default_rng(3);b=np.random.default_rng(3);batch(a,32,False);batch(b,32,True);self.assertEqual(a.bit_generator.state,b.bit_generator.state)
 def test_parent_weights_fixed(self):
  before=weights_hash(self.ms['binder']);self.reg();self.s.event(self.new,self.val(self.room));self.assertEqual(before,weights_hash(self.ms['binder']))
 def test_context_identical_evidence(self):
  a=sample(71998000,32,'identical_known');b=sample(71998000,32,'identical_novel')
  for k in ('a','z','big','x','y','w'):self.assertTrue(np.array_equal(a[k],b[k]))
  for m in ('single16','duplicate32','independent32','single32'):self.assertTrue(np.array_equal(decide(a,m,{'distance':.6,'margin':.04})[0],decide(b,m,{'distance':.6,'margin':.04})[0]))
 def test_duplicate_context_same_rule(self):
  p=sample(71998001,32,'known_q20');x=decide(p,'single16',{'distance':.6,'margin':.04})[0];y=decide(p,'duplicate32',{'distance':.6,'margin':.04})[0];self.assertTrue(np.array_equal(x,y))

if __name__=='__main__':unittest.main()
