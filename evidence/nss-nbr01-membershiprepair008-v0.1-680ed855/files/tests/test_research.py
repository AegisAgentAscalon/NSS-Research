import copy,json,tempfile,unittest
from pathlib import Path
import numpy as np
import torch
from nbr008.common import setup,parents,model_hashes,sha,dump
from nbr008.resolver import Resolver,features,MatchHead,ABI
from nbr008.pipeline import make_problem,install,read,init_query,step_query
from nbr008.state import State
from nbr008.samples import sample
from nbr008.config import contract

class ResearchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):setup(7);cls.models=parents(1)
 def setUp(self):
  self.p=make_problem(12345,4,8,n=12);self.r=Resolver('A_nearest',{'distance':.5,'margin':.03},restorer=self.models['dictionary']);self.s=install(self.p,self.models['binder'])
 def newcode(self):
  x=torch.zeros(8,17);x[:,:16]=torch.nn.functional.normalize(torch.randn(8,16),dim=-1);return x
 def test_clean_member(self):
  d=self.r(self.s.book[:,:1],self.s.book,self.s.active);self.assertTrue(d.accept.all())
 def test_zero_rejected(self):
  d=self.r(torch.zeros(8,1,17),self.s.book,self.s.active);self.assertFalse(d.accept.any())
 def test_sentinel_rejected(self):
  x=torch.zeros(8,1,17);x[:,:,-1]=1;self.assertFalse(self.r(x,self.s.book,self.s.active).accept.any())
 def test_soft_null_competitor(self):
  x=torch.ones(8,1,17)*.001;x[:,:,-1]=.999
  for kind in ('nearest','A_nearest','learned'):
   r=Resolver(kind,self.r.params,restorer=self.models['dictionary']);self.assertFalse(r(x,self.s.book,self.s.active).accept.any())
 def test_bad_dimensions(self):
  with self.assertRaises(ValueError):self.r(torch.zeros(8,1,16),self.s.book,self.s.active)
 def test_nonfinite_input(self):
  x=torch.zeros(8,1,17);x[0,0,0]=float('nan')
  with self.assertRaises(ValueError):self.r(x,self.s.book,self.s.active)
 def test_nonfinite_reference(self):
  b=self.s.book.clone();b[0,0,0]=float('inf')
  with self.assertRaises(ValueError):State(b,self.s.active,self.models['binder'])
 def test_inactive_future_code_rejected(self):
  b=self.s.book.clone();b[:,12]=self.newcode()
  with self.assertRaises(ValueError):State(b,self.s.active,self.models['binder'])
 def test_inactive_never_selected(self):
  d=self.r(self.newcode()[:,None],self.s.book,self.s.active);self.assertFalse((d.index>=12).any())
 def test_mask_permutation(self):
  x=torch.from_numpy(self.p['q'])[:,None];perm=torch.randperm(16)
  a=self.r(x,self.s.book,self.s.active);b=self.r(x,self.s.book[:,perm],self.s.active[:,perm]);self.assertTrue(torch.equal(a.value,b.value));self.assertTrue(torch.equal(a.accept,b.accept))
 def test_no_active_reference(self):
  self.s.clear_scope();self.assertFalse(self.r(self.newcode()[:,None],self.s.book,self.s.active).accept.any())
 def test_register_changes_membership_not_relations(self):
  before=self.s.present.clone();self.s.register(self.newcode());self.assertTrue(torch.equal(self.s.present,before));self.assertTrue(self.s.active[:,12].all())
 def test_no_hidden_future_before_register(self):self.assertTrue((self.s.book[:,12:]==0).all())
 def test_denied_register(self):
  h=self.s.signature();self.s.register(self.newcode(),False);self.assertEqual(h,self.s.signature())
 def test_wrong_scope_register(self):
  h=self.s.signature();self.s.register(self.newcode(),True,'other');self.assertEqual(h,self.s.signature())
 def test_duplicate_register(self):
  h=self.s.signature();r=self.s.register(self.s.book[:,0].clone());self.assertTrue(r['duplicate'].all());self.assertEqual(h,self.s.signature())
 def test_near_duplicate_not_silently_merged(self):
  x=torch.nn.functional.normalize(self.s.book[:,0]+self.newcode()*.001,dim=-1);x[:,-1]=0
  r=self.s.register(x);self.assertTrue(r['added'].all());self.assertTrue(self.s.active[:,12].all())
 def test_capacity_no_overwrite(self):
  for _ in range(4):self.s.register(self.newcode())
  h=self.s.signature();rc=self.s.register(self.newcode());self.assertTrue(rc['full'].all());self.assertEqual(h,self.s.signature())
 def test_noncanonical_registration(self):
  with self.assertRaises(ValueError):self.s.register(self.newcode()*2)
 def test_query_does_not_register(self):
  h=self.s.signature();read(self.s,self.models['record_hop'],self.r,self.newcode());self.assertEqual(h,self.s.signature())
 def test_repeated_query_no_fake_evidence(self):
  q=self.newcode();a=read(self.s,self.models['record_hop'],self.r,q);b=read(self.s,self.models['record_hop'],self.r,q);self.assertTrue(torch.equal(a['pred'],b['pred']))
 def test_gate_uses_raw(self):
  x=self.s.book[:,0,None]*2;d=self.r(x,self.s.book,self.s.active);self.assertFalse(d.accept.any());self.assertTrue(torch.equal(d.value,x))
 def test_declined_field_stays_present_raw(self):
  k=self.s.store.keys;live=self.s.present;self.s.store.keys[live]*=5;before=k.clone();self.s.maintain(self.r,'keys');self.assertTrue(torch.equal(before,k));self.assertTrue(self.s.present.any());self.assertFalse(self.s.kr[live].any())
 def test_quarantine_does_not_become_absent(self):
  self.s.store.vals[self.s.present]=0;p=self.s.present.clone();self.s.maintain(self.r,'values');self.assertTrue(torch.equal(p,self.s.present));self.assertFalse(self.s.vr[p].any())
 def test_unreadable_is_sticky(self):
  self.s.vr.zero_();before=self.s.store.vals.clone();self.s.maintain(self.r);self.assertFalse(self.s.vr.any());self.assertTrue(torch.equal(before,self.s.store.vals))
 def test_empty_store_reads_unknown(self):
  self.s.store.clear_all();self.s.kr.zero_();self.s.vr.zero_();o=read(self.s,self.models['record_hop'],self.r,torch.from_numpy(self.p['q']));self.assertTrue((o['pred']==16).all())
 def test_register_then_missing_relation(self):
  x=self.newcode();self.s.register(x);o=read(self.s,self.models['record_hop'],self.r,x);self.assertTrue((o['pred'][:,-1]==16).all())
 def test_explicit_write_after_register(self):
  x=self.newcode();self.s.register(x);dest=torch.from_numpy(self.p['codes'][np.arange(8),self.p['rooms'][:,0]])
  rc=self.s.event(x,dest,1,self.r);self.assertTrue(rc['written'].all());o=read(self.s,self.models['record_hop'],self.r,x);self.assertTrue(torch.equal(o['pred'][:,-1],torch.from_numpy(self.p['rooms'][:,0])))
 def test_clear_and_rewrite(self):
  x=self.newcode();self.s.register(x);dest=torch.from_numpy(self.p['codes'][np.arange(8),self.p['rooms'][:,0]]);self.s.event(x,dest,1,self.r);self.s.event(x,dest,-1,self.r)
  o=read(self.s,self.models['record_hop'],self.r,x);self.assertTrue((o['pred'][:,-1]==16).all());self.s.event(x,dest,1,self.r);o=read(self.s,self.models['record_hop'],self.r,x);self.assertTrue(torch.equal(o['pred'][:,-1],torch.from_numpy(self.p['rooms'][:,0])))
 def test_denied_write_no_mutation(self):
  h=self.s.signature();self.s.event(self.s.book[:,0],self.s.book[:,1],1,self.r,False);self.assertEqual(h,self.s.signature())
 def test_wrong_scope_write_no_mutation(self):
  h=self.s.signature();self.s.event(self.s.book[:,0],self.s.book[:,1],1,self.r,True,'other');self.assertEqual(h,self.s.signature())
 def test_reject_all_cannot_pass_usefulness(self):
  r=Resolver('reject_all');o=read(self.s,self.models['record_hop'],r,torch.from_numpy(self.p['q']));self.assertTrue((o['pred']==16).all())
 def test_reset_clears_identities_and_relations(self):
  self.s.clear_scope();self.assertFalse(self.s.active.any());self.assertFalse(self.s.present.any());self.assertTrue((self.s.book==0).all())
 def test_weights_fixed(self):
  before=model_hashes(self.models);read(self.s,self.models['gated_hop'],self.r,torch.from_numpy(self.p['q']));self.s.maintain(self.r);self.assertEqual(before,model_hashes(self.models))
 def test_state_roundtrip(self):
  rng=np.random.default_rng(8)
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(path,rng,c);s,g,q=State.load(path,self.models['binder'],c);self.assertEqual(s.signature(),self.s.signature());self.assertEqual(g.bit_generator.state,rng.bit_generator.state)
 def test_bad_contract_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(p,np.random.default_rng(8),c)
   with self.assertRaises(ValueError):State.load(p,self.models['binder'],{'bad':1})
 def test_old_abi_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(p,np.random.default_rng(8),c);m=json.loads(p.with_suffix('.json').read_text());m['abi']='nbr006-record-v1';dump(p.with_suffix('.json'),m)
   with self.assertRaises(ValueError):State.load(p,self.models['binder'],c)
 def test_wrong_scope_snapshot_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(p,np.random.default_rng(8),c)
   with self.assertRaises(ValueError):State.load(p,self.models['binder'],c,'other')
 def test_snapshot_integrity(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(p,np.random.default_rng(8),c);p.write_bytes(p.read_bytes()+b'x')
   with self.assertRaises(ValueError):State.load(p,self.models['binder'],c)
 def test_midquery_resume(self):
  qs=init_query(torch.from_numpy(self.p['q']));qs,_=step_query(self.s,self.models['record_hop'],self.r,qs)
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'s.npz';c=contract(self.r,self.models);self.s.save(p,np.random.default_rng(8),c,qs);s,g,q=State.load(p,self.models['binder'],c)
   a=read(self.s,self.models['record_hop'],self.r,qs['h'],4,qs=qs);b=read(s,self.models['record_hop'],self.r,q['h'],4,qs=q);self.assertTrue(torch.equal(a['pred'],b['pred']))
 def test_stale_reference_rejected(self):
  old=self.s.revision.copy();self.s.register(self.newcode())
  with self.assertRaises(ValueError):read(self.s,self.models['record_hop'],self.r,torch.from_numpy(self.p['q']),expected_revision=old)
 def test_wrong_query_scope_rejected(self):
  with self.assertRaises(ValueError):read(self.s,self.models['record_hop'],self.r,torch.from_numpy(self.p['q']),scope='other')
 def test_same_observable_same_decision(self):
  a=self.newcode()[:,None];d=self.r(a,self.s.book,self.s.active);e=self.r(a.clone(),self.s.book.clone(),self.s.active.clone());self.assertTrue(torch.equal(d.accept,e.accept))
 def test_removed_identity_mask(self):
  a=sample(np.random.default_rng(1),64,'removed');self.assertTrue((a['active'].sum(-1)==15).all());self.assertTrue((a['book'][~a['active']]==0).all())
 def test_different_origin_not_input_feature(self):
  a=sample(np.random.default_rng(3),64,'novel');self.assertTrue((a['x'][:,:,-1]==0).all());self.assertTrue(np.allclose(np.linalg.norm(a['x'],axis=-1),1))

if __name__=='__main__':unittest.main(verbosity=2)
