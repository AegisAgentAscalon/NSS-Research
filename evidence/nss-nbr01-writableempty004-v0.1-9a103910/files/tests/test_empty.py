from pathlib import Path
import sys,unittest,tempfile,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import torch
from safetensors.torch import load_file,save_file
from nbr01_empty.models import *
from nbr01_empty.snapshot import save,restore
from nbr01_empty.util import setup,sha,digest_tensors
from nbr01_empty.train import batch
setup()
class TestWritableEmpty(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rep=Representation(ROOT/'reference/soft_slots_wide_seed301.safetensors')
  cls.repair=Repair();cls.repair.load_state_dict(load_file(str(ROOT/'reference/recurrent_rep301_seed501.safetensors')));cls.repair.eval()
 def mem(self,mode='presence_historical'):return Memory(self.rep,mode,self.repair,batch=4,scope='a')
 def test_empty_read(self):self.assertTrue((self.mem().read()==8).all())
 def test_first_write(self):
  m=self.mem();m.event('write',0,3);m.maintain();self.assertTrue((m.read()[:,0]==3).all())
 def test_low_qualified_score(self):
  m=self.mem();m.event('write',0,2,score=.5001);self.assertTrue(m.presence[:,0].all());self.assertTrue((m.read()[:,0]==2).all())
 def test_boundary_qualified(self):self.assertTrue(self.mem().event('write',0,2,score=.5))
 def test_boundary_rejected(self):
  m=self.mem();self.assertFalse(m.event('write',0,2,score=.4999));self.assertFalse(m.presence.any());self.assertTrue((m.z==0).all())
 def test_update(self):
  m=self.mem();m.event('write',0,3);m.event('write',0,4);self.assertTrue((m.read()[:,0]==4).all())
 def test_clear(self):
  m=self.mem();m.event('write',0,3);m.event('clear',0);self.assertFalse(m.presence[:,0].any());self.assertTrue((m.z[:,0]==0).all())
 def test_rewrite_after_clear(self):
  m=self.mem();m.event('write',0,3);m.event('clear',0);m.event('write',0,4);m.maintain();self.assertTrue((m.read()[:,0]==4).all())
 def test_neighbors_untouched_on_write(self):
  m=self.mem();m.event('write',1,2);a=m.z[:,1:].clone();m.event('write',0,4);self.assertTrue(torch.equal(a,m.z[:,1:]))
 def test_neighbors_untouched_on_clear(self):
  m=self.mem();m.event('write',1,2);a=m.z[:,1:].clone();m.event('clear',0);self.assertTrue(torch.equal(a,m.z[:,1:]))
 def test_global_clear(self):
  m=self.mem();m.event('write',1,2);m.event('clear_all');self.assertTrue((m.z==0).all());self.assertFalse(m.presence.any())
 def test_wrong_scope(self):
  m=self.mem();self.assertFalse(m.event('write',0,3,scope='b'));self.assertTrue((m.read()==8).all())
 def test_noop(self):
  m=self.mem();a=m.z.clone();self.assertFalse(m.event('noop'));self.assertTrue(torch.equal(a,m.z))
 def test_presence_protection(self):
  m=self.mem();m.maintain(torch.ones_like(m.z));self.assertTrue((m.z==0).all())
 def test_no_presence_in_native(self):self.assertIsNone(self.mem('historical').presence)
 def test_native_bytes(self):self.assertEqual(self.mem('historical').raw_state_bytes(),4*256)
 def test_presence_bytes(self):self.assertEqual(self.mem().raw_state_bytes(),4*260)
 def test_zero_value_not_empty(self):
  m=self.mem();m.event('write',0,0);self.assertTrue(m.presence[:,0].all());self.assertTrue((m.read()[:,0]==0).all())
 def test_invalid_key(self):
  with self.assertRaises(ValueError):self.mem().event('write',4,0)
 def test_invalid_value(self):
  with self.assertRaises(ValueError):self.mem().event('write',0,8)
 def test_invalid_score_nan(self):
  with self.assertRaises(ValueError):self.mem().event('write',0,3,score=float('nan'))
 def test_invalid_score_range(self):
  with self.assertRaises(ValueError):self.mem().event('write',0,3,score=1.1)
 def test_invalid_bool_key(self):
  with self.assertRaises(ValueError):self.mem().event('write',True,3)
 def test_invalid_tensor_shape(self):
  with self.assertRaises(ValueError):self.mem().event('write',0,torch.zeros(3,dtype=torch.long))
 def test_invalid_op(self):
  with self.assertRaises(ValueError):self.mem().event('promote')
 def test_invalid_noise(self):
  with self.assertRaises(ValueError):self.mem().maintain(torch.zeros(1))
 def test_nonfinite_noise(self):
  m=self.mem()
  with self.assertRaises(ValueError):m.maintain(torch.full_like(m.z,float('nan')))
 def test_read_pure(self):
  m=self.mem();a=m.z.clone();p=m.presence.clone();m.read();m.read();self.assertTrue(torch.equal(a,m.z));self.assertTrue(torch.equal(p,m.presence))
 def test_repair_parameters(self):self.assertEqual(sum(p.numel() for p in Repair().parameters()),2128)
 def test_local_parameters(self):
  m=LocalEmpty();self.assertEqual(sum(p.numel() for p in m.parameters()),2129);self.assertEqual(sum(p.numel() for p in m.parameters() if p.requires_grad),1)
 def test_local_zero(self):self.assertTrue((LocalEmpty()(torch.zeros(4,16))==0).all())
 def test_local_nonbinary(self):
  m=LocalEmpty();z=torch.ones(4,16)*.2;out=m(z);self.assertGreater(float(out.abs().sum()),0);self.assertFalse((out==1).all())
 def test_training_paired(self):
  a=batch(self.rep,torch.Generator().manual_seed(123));b=batch(self.rep,torch.Generator().manual_seed(123));self.assertTrue(all(torch.equal(x,y) for x,y in zip(a,b)))
 def test_training_disjoint_operations(self):
  x=batch(self.rep,torch.Generator().manual_seed(123));self.assertFalse((x[3]&x[4]).any())
 def test_snapshot_roundtrip(self):
  m=self.mem();m.event('write',0,2);g=torch.Generator().manual_seed(4)
  with tempfile.TemporaryDirectory() as d:
   save(m,g,Path(d)/'snap');n=self.mem();h=torch.Generator();restore(n,h,Path(d)/'snap');self.assertTrue(torch.equal(n.z,m.z));self.assertTrue(torch.equal(n.presence,m.presence));self.assertTrue(torch.equal(g.get_state(),h.get_state()))
 def test_snapshot_immutable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';save(self.mem(),torch.Generator(),p)
   with self.assertRaises(FileExistsError):save(self.mem(),torch.Generator(),p)
 def test_snapshot_scope(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';m=self.mem();save(m,torch.Generator(),p);m.scope='other'
   with self.assertRaises(ValueError):restore(m,torch.Generator(),p)
 def test_snapshot_mode(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';save(self.mem(),torch.Generator(),p)
   with self.assertRaises(ValueError):restore(self.mem('historical'),torch.Generator(),p)
 def test_snapshot_corruption(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';m=self.mem();save(m,torch.Generator(),p);f=p/'state.safetensors';data=f.read_bytes();f.write_bytes(data[:-1]+bytes([data[-1]^1]))
   with self.assertRaises(ValueError):restore(m,torch.Generator(),p)
 def test_snapshot_schema(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';m=self.mem();save(m,torch.Generator(),p);f=p/'metadata.json';x=json.loads(f.read_text());x['identity']['schema']='wrong';f.write_text(json.dumps(x))
   with self.assertRaises(ValueError):restore(m,torch.Generator(),p)
 def test_snapshot_dtype(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';m=self.mem();save(m,torch.Generator(),p);f=p/'state.safetensors';x=load_file(str(f));x['presence']=x['presence'].long();save_file(x,str(f));meta=p/'metadata.json';a=json.loads(meta.read_text());a['sha256']=sha(f);meta.write_text(json.dumps(a))
   with self.assertRaises(ValueError):restore(m,torch.Generator(),p)
 def test_snapshot_clock(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'snap';m=self.mem();save(m,torch.Generator(),p);meta=p/'metadata.json';a=json.loads(meta.read_text());a['rounds']=-1;meta.write_text(json.dumps(a))
   with self.assertRaises(ValueError):restore(m,torch.Generator(),p)
 def test_weight_identity(self):
  m=self.mem();before=digest_tensors(m.repair.state_dict());m.event('write',0,3);m.maintain();m.read();self.assertEqual(before,digest_tensors(m.repair.state_dict()))
 def test_nearest_control(self):
  m=self.mem('nearest');m.event('write',0,3);m.maintain(torch.full_like(m.z,.001));self.assertTrue((m.read()[:,0]==3).all());self.assertTrue((m.read()[:,1:]==8).all())
if __name__=='__main__':unittest.main()
