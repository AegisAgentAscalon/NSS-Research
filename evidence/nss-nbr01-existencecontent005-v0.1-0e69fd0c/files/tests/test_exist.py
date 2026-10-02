import unittest,tempfile,json,sys,math
from pathlib import Path
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.models import *
from nbr01_exist.util import setup,digest_tensors,sha,write_json
from nbr01_exist.evaluate import generators,noisy_step
from nbr01_exist.snapshot import save,restore

class ExistenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup();cls.rep,cls.old,_=load_components(ROOT,301,'historical')
    def mem(self,mode='fixed4',n=8,scope='study'):
        return Memory(self.rep,mode,self.old,Presence(1 if mode=='split1' else 4) if mode in ('split1','split4') else Coupled(self.old) if mode=='coupled17' else None,n,scope)
    def test_empty_start(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                m=self.mem(mode);self.assertTrue((m.read()==8).all());self.assertFalse(m.existence().any())
    def test_initial_known_zero_symbol(self):
        m=self.mem();m.event('write',0,0);self.assertTrue((m.read()[:,0]==0).all());self.assertTrue(m.existence()[:,0].all())
    def test_complete_write(self):
        for mode in MODES:
            m=self.mem(mode);self.assertTrue(m.event('write',0,2,.5001));self.assertTrue((m.read()[:,0]==2).all())
    def test_correction(self):
        m=self.mem();m.event('write',0,2);m.event('write',0,3);self.assertTrue((m.read()[:,0]==3).all())
    def test_clear_then_rewrite(self):
        for mode in MODES:
            m=self.mem(mode);m.event('write',0,2);m.event('clear',0);self.assertFalse(m.existence()[:,0].any());m.event('write',0,7);self.assertTrue((m.read()[:,0]==7).all())
    def test_clear_all(self):
        m=self.mem();m.event('write',0,2);m.event('write',3,7);m.event('clear_all');self.assertTrue((m.read()==8).all())
    def test_scope(self):
        m=self.mem();z=m.z.clone();p=m.p.clone();self.assertFalse(m.event('write',0,2,scope='other'));self.assertTrue(torch.equal(z,m.z));self.assertTrue(torch.equal(p,m.p))
    def test_low_score(self):
        m=self.mem();self.assertFalse(m.event('write',0,2,.4999));self.assertTrue((m.read()==8).all())
    def test_boundary(self):
        m=self.mem();self.assertTrue(m.event('write',0,2,.5));self.assertTrue((m.read()[:,0]==2).all())
    def test_noop(self):
        m=self.mem();z=m.z.clone();p=m.p.clone();self.assertFalse(m.event('noop'));self.assertTrue(torch.equal(z,m.z));self.assertTrue(torch.equal(p,m.p))
    def test_neighbors(self):
        m=self.mem();m.event('write',1,2);m.event('write',0,3);m.event('clear',0);self.assertTrue((m.read()[:,1]==2).all())
    def test_read_pure(self):
        m=self.mem();m.event('write',0,2);a=m.z.clone();b=m.p.clone();m.read();m.existence();m.read_status();self.assertTrue(torch.equal(m.z,a));self.assertTrue(torch.equal(m.p,b))
    def test_absence_vs_unreadable(self):
        m=self.mem();m.event('write',0,2);m.z[:,0]=0;self.assertTrue((m.read_status()[:,0]==2).all());self.assertTrue((m.read_status()[:,1]==0).all())
    def test_invalid_score(self):
        for x in [True,None,float('nan'),float('inf'),-1,2]:
            with self.assertRaises(ValueError):self.mem().event('write',0,1,x)
    def test_invalid_address(self):
        for x in [-1,4,False,'0']:
            with self.assertRaises(ValueError):self.mem().event('write',x,1)
    def test_invalid_value(self):
        for x in [-1,8,False,1.,torch.zeros(8),torch.zeros(7,dtype=torch.long)]:
            with self.assertRaises(ValueError):self.mem().event('write',0,x)
    def test_invalid_op(self):
        with self.assertRaises(ValueError):self.mem().event('guess')
    def test_invalid_batch(self):
        for n in [0,4097,True,1.5]:
            with self.assertRaises(ValueError):self.mem(n=n)
    def test_invalid_scope(self):
        for s in ['',None,'x'*201]:
            with self.assertRaises(ValueError):self.mem(scope=s)
    def test_invalid_mode(self):
        with self.assertRaises(ValueError):self.mem('unknown')
    def test_invalid_presence_width(self):
        with self.assertRaises(ValueError):Presence(3)
    def test_missing_model(self):
        with self.assertRaises(ValueError):Memory(self.rep,'split1',self.old,None)
    def test_state_bytes(self):
        sizes={'historical':256,'protected':260,'nearest':256,'split1':272,'split4':320,'coupled17':272,'fixed1':272,'fixed4':320,'hold1':272}
        for mode,size in sizes.items():self.assertEqual(self.mem(mode).raw_state_bytes(),size*8)
    def test_no_protected_neural_flag(self):
        for mode in ('split1','split4','coupled17'):self.assertIsNone(self.mem(mode).flag)
    def test_noise_shape(self):
        with self.assertRaises(ValueError):self.mem().maintain(torch.zeros(1))
    def test_noise_dtype(self):
        m=self.mem()
        with self.assertRaises(ValueError):m.maintain(torch.zeros_like(m.z,dtype=torch.float64))
    def test_noise_nan(self):
        m=self.mem()
        with self.assertRaises(ValueError):m.maintain(torch.full_like(m.z,float('nan')))
    def test_presence_noise_validation_atomic(self):
        m=self.mem();z=m.z.clone()
        with self.assertRaises(ValueError):m.maintain(torch.ones_like(m.z),torch.ones(1))
        self.assertTrue(torch.equal(z,m.z))
    def test_noise_exposes_presence(self):
        m=self.mem();m.event('write',0,2);noise=torch.zeros_like(m.p);noise[:,0]=-3;m.maintain(torch.zeros_like(m.z),noise);self.assertFalse(m.existence()[:,0].any())
    def test_noise_protected_flag(self):
        m=self.mem('protected');m.event('write',0,2);m.maintain(torch.randn_like(m.z));self.assertTrue(m.existence()[:,0].all())
    def test_population_one_flip(self):
        m=self.mem();m.event('write',0,2);m.p[:,0,0]*=-1;m.maintain();self.assertTrue(m.existence()[:,0].all())
    def test_population_all_flip(self):
        m=self.mem();m.event('write',0,2);m.p[:,0]*=-1;m.maintain();self.assertFalse(m.existence()[:,0].any())
    def test_mean_zero_is_absent(self):
        m=self.mem();m.p[:]=0;self.assertFalse(m.existence().any())
    def test_new_write_changes_presence_first(self):
        m=self.mem();m.event('write',0,2);m.maintain();self.assertTrue((m.read()[:,0]==2).all())
    def test_matched_noise_widths(self):
        a=self.mem('fixed1');b=self.mem('fixed4');g1,g2=generators(301,1);h1,h2=generators(301,1)
        noisy_step(a,g1,g2,.15);noisy_step(b,h1,h2,.15);self.assertTrue(torch.equal(g1.get_state(),h1.get_state()));self.assertTrue(torch.equal(g2.get_state(),h2.get_state()))
    def test_snapshot_roundtrip(self):
        a=self.mem();a.event('write',0,2);gc,gp=generators(1,2);noisy_step(a,gc,gp,.15)
        with tempfile.TemporaryDirectory() as t:
            save(a,gc,gp,Path(t)/'s');b=self.mem();bc,bp=generators(0,0);restore(b,bc,bp,Path(t)/'s')
            self.assertTrue(torch.equal(a.z,b.z));self.assertTrue(torch.equal(a.p,b.p));self.assertTrue(torch.equal(gc.get_state(),bc.get_state()))
    def test_snapshot_scope_rejected(self):
        a=self.mem();gc,gp=generators(1,2)
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'s';save(a,gc,gp,s)
            with self.assertRaises(ValueError):restore(self.mem(scope='other'),gc,gp,s)
    def test_snapshot_mode_rejected(self):
        a=self.mem();gc,gp=generators(1,2)
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'s';save(a,gc,gp,s)
            with self.assertRaises(ValueError):restore(self.mem('fixed1'),gc,gp,s)
    def test_snapshot_corruption_rejected(self):
        a=self.mem();gc,gp=generators(1,2)
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'s';save(a,gc,gp,s);(s/'state.safetensors').write_bytes(b'bad')
            with self.assertRaises(ValueError):restore(a,gc,gp,s)
    def test_snapshot_immutable(self):
        a=self.mem();gc,gp=generators(1,2)
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'s';save(a,gc,gp,s)
            with self.assertRaises(FileExistsError):save(a,gc,gp,s)
    def test_snapshot_weights_rejected(self):
        a=self.mem('split1');gc,gp=generators(1,2)
        with tempfile.TemporaryDirectory() as t:
            s=Path(t)/'s';save(a,gc,gp,s)
            with self.assertRaises(ValueError):restore(self.mem('split1'),gc,gp,s)
    def test_weight_forward_unchanged(self):
        for mode in MODES:
            m=self.mem(mode);before=digest_tensors(m.old.state_dict());m.maintain();self.assertEqual(before,digest_tensors(m.old.state_dict()))
    def test_parameter_counts(self):
        self.assertEqual(sum(p.numel() for p in Presence(1).parameters()),49)
        self.assertEqual(sum(p.numel() for p in Presence(4).parameters()),148)
        self.assertEqual(sum(p.numel() for p in Coupled().parameters()),2257)
    def test_no_future_record_cache(self):
        m=self.mem('split4');self.assertEqual(set(vars(m)),{'rep','mode','old','new','scope','z','width','p','flag','events','rounds'})

if __name__=='__main__':unittest.main()
