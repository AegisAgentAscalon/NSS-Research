from pathlib import Path
import tempfile,json,unittest
import torch
from nbr01_recovery.models import Representation,Repair,FastSlow,Candidate,MODES,D,KEYS
from nbr01_recovery.data import training_batch,fault,labels
from nbr01_recovery.evaluate import iterate
from nbr01_recovery.state import Session
from nbr01_recovery.util import setup,digest_tensors,sha
ROOT=Path(__file__).resolve().parents[1]

class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup();cls.rep=Representation(ROOT/'reference/soft_slots_wide_seed141.safetensors')
    def setUp(self):
        torch.manual_seed(55);self.repair=Repair().eval();self.fs=FastSlow().eval()
        self.y=torch.tensor([[0,1,8,3],[4,8,6,7]])
    def c(self,mode):return Candidate(self.rep,mode,self.repair,self.fs)
    def test_frozen_rep(self):self.assertFalse(any(p.requires_grad for p in self.rep.parameters()))
    def test_source_clean_competence(self):self.assertTrue(torch.equal(self.rep(self.rep.codes).argmax(-1),torch.arange(9)))
    def test_unknown_code_zero(self):self.assertTrue(torch.equal(self.rep.codes[8],torch.zeros(D)))
    def test_replica_bytes(self):self.assertEqual(self.c('fast_slow').active_state_bytes_per_stream(),512)
    def test_single_bytes(self):self.assertEqual(self.c('recurrent').active_state_bytes_per_stream(),256)
    def test_exact_zero_one(self):self.assertTrue(torch.equal(self.repair(torch.zeros(D)),torch.zeros(D)))
    def test_exact_zero_mixed_batch(self):
        x=torch.randn(17,D);x[3]=0;self.assertTrue(torch.equal(self.repair(x)[3],torch.zeros(D)))
    def test_exact_zero_repeated(self):
        z=torch.zeros(1,KEYS,D)
        with torch.no_grad():
            for _ in range(4096):z=self.repair(z)
        self.assertTrue(torch.equal(z,torch.zeros_like(z)))
    def test_fastslow_equal_lanes_invariant(self):
        x=torch.randn(2,KEYS,D);f,s=self.fs(x,x)
        self.assertTrue(torch.allclose(x,f,atol=1e-6));self.assertTrue(torch.allclose(x,s,atol=1e-6))
    def test_fastslow_simultaneous(self):
        f=torch.ones(2,KEYS,D);s=torch.zeros_like(f);a,b,g=self.fs.rates();ff,ss=self.fs(f,s)
        self.assertTrue(torch.allclose(ff,1-b));self.assertTrue(torch.allclose(ss,g))
    def test_fastslow_mean_collapse(self):
        x=torch.randn(2,KEYS,D);y=torch.randn_like(x);a,b=self.fs(x,y,equal=True)
        self.assertTrue(torch.allclose(a+b,x+y,atol=1e-6))
    def test_hold_noop(self):
        c=self.c('hold');s=c.state(self.y);self.assertIs(s,c.step(s))
    def test_off_equivalence(self):
        c=self.c('recurrent_off');s=c.state(self.y);self.assertIs(s,c.step(s))
    def test_read_only_unchanged(self):
        c=self.c('readout_repair');s=c.state(self.y);before=[x.clone() for x in s];c.predict(s)
        self.assertTrue(all(torch.equal(x,y) for x,y in zip(s,before)))
    def test_projection_idempotent(self):
        c=self.c('nearest_maintenance');s=(torch.randn(2,KEYS,D),)
        self.assertTrue(torch.equal(c.step(s)[0],c.step(c.step(s))[0]))
    def test_full_erasure_identical(self):
        c=self.c('recurrent');a=fault(c.state(self.y),'erase_all',1.,torch.Generator(),self.rep.codes,self.y)
        self.assertTrue(torch.equal(a[0],torch.zeros_like(a[0])))
    def test_fast_damage_protects_only_named_lane(self):
        c=self.c('fast_slow');s=c.state(self.y);t=fault(s,'erase_fast',1.,torch.Generator(),self.rep.codes,self.y)
        self.assertTrue(torch.equal(s[1],t[1]));self.assertTrue(torch.equal(t[0],torch.zeros_like(t[0])))
    def test_common_damage_identical_copies(self):
        c=self.c('fast_slow');s=c.state(self.y);t=fault(s,'common_gaussian',1.,torch.Generator(),self.rep.codes,self.y)
        self.assertTrue(torch.equal(t[0],t[1]))
    def test_rng_paired_first_lane(self):
        a=fault(self.c('hold').state(self.y),'gaussian',1.,torch.Generator().manual_seed(8),self.rep.codes,self.y)
        b=fault(self.c('fast_slow').state(self.y),'gaussian',1.,torch.Generator().manual_seed(8),self.rep.codes,self.y)
        self.assertTrue(torch.equal(a[0],b[0]))
    def test_training_deterministic(self):
        a=training_batch(self.rep,torch.Generator().manual_seed(4));b=training_batch(self.rep,torch.Generator().manual_seed(4))
        for k in a:self.assertTrue(torch.equal(a[k],b[k]) if torch.is_tensor(a[k]) else a[k]==b[k])
    def test_labels_include_unknown(self):self.assertEqual(set(labels(torch.Generator(),9).flatten().tolist()),set(range(9)))
    def test_exact_archive_requires_explicit_data(self):
        with self.assertRaises(ValueError):self.c('exact_archive').predict((torch.zeros(2,KEYS,D),))
    def test_archive_has_no_query_label_access(self):
        c=self.c('exact_archive');s=c.state(self.y)
        damaged=tuple(torch.zeros_like(x) for x in s)
        self.assertTrue(torch.equal(c.predict(damaged),self.y))
        new=(self.y+1).remainder(8);mask=torch.zeros_like(new,dtype=torch.bool);mask[:,0]=True
        damaged=c.write(damaged,new,mask)
        expected=self.y.clone();expected[:,0]=new[:,0]
        self.assertTrue(torch.equal(c.predict(damaged),expected))
        c.reset(damaged);self.assertTrue(torch.equal(c.predict(damaged),torch.full_like(self.y,8)))
    def test_no_state(self):
        c=self.c('state_off');self.assertTrue(torch.equal(c.predict(c.state(self.y)),torch.full_like(self.y,8)))
    def test_fastforward_identity(self):
        c=self.c('hold');s=c.state(self.y);x=list(iterate(c,s,[0,4,4096]));self.assertEqual([a[0] for a in x],[0,4,4096]);self.assertEqual(x[-1][-1],1)
    def test_fastforward_vs_explicit(self):
        c=self.c('recurrent');s=c.state(self.y)
        with torch.no_grad():
            a=list(iterate(c,s,[32]))[-1][1][0]
            for _ in range(32):s=c.step(s)
        self.assertTrue(torch.equal(a,s[0]))
    def test_session_rejected_write(self):
        s=Session(self.c('hold'),'x','v1');s.event(0,2,.49);self.assertEqual(s.read()[0,0],8)
    def test_session_boundary_write(self):
        s=Session(self.c('hold'),'x','v1');s.event(0,2,.5);self.assertEqual(s.read()[0,0],2)
    def test_session_scope_isolation(self):
        s=Session(self.c('hold'),'x','v1');s.event(0,2,.7);self.assertEqual(s.read()[0,1],8)
    def test_session_read_no_tick(self):
        s=Session(self.c('recurrent'),'x','v1');s.event(0,2,.7);before=(s.events,s.rounds);s.read();s.read();self.assertEqual(before,(s.events,s.rounds))
    def test_reset_dual(self):
        s=Session(self.c('fast_slow'),'x','v1');s.event(0,2,.7);s.clear()
        self.assertTrue(all(torch.equal(x,torch.zeros_like(x)) for x in s.state))
    def test_snapshot_continue(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(self.c('recurrent'),'x','v1');s.event(0,2,.7);s.maintain(4);s.save(Path(tmp)/'snap')
            r=Session(self.c('recurrent'),'x','v1');r.restore(Path(tmp)/'snap');s.maintain(8);r.maintain(8)
            self.assertTrue(torch.equal(s.state[0],r.state[0]));self.assertEqual(s.rounds,r.rounds)
    def test_snapshot_scope_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(self.c('hold'),'x','v1');s.save(Path(tmp)/'snap')
            with self.assertRaises(ValueError):Session(self.c('hold'),'y','v1').restore(Path(tmp)/'snap')
    def test_snapshot_revision_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(self.c('hold'),'x','v1');s.save(Path(tmp)/'snap')
            with self.assertRaises(ValueError):Session(self.c('hold'),'x','v2').restore(Path(tmp)/'snap')
    def test_snapshot_mode_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(self.c('hold'),'x','v1');s.save(Path(tmp)/'snap')
            with self.assertRaises(ValueError):Session(self.c('recurrent'),'x','v1').restore(Path(tmp)/'snap')
    def test_snapshot_tamper_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Session(self.c('hold'),'x','v1');p=Path(tmp)/'snap';s.save(p)
            f=p/'state.safetensors';f.write_bytes(f.read_bytes()+b'X')
            with self.assertRaises(ValueError):s.restore(p)
    def test_invalid_inputs(self):
        s=Session(self.c('hold'),'x','v1')
        for args in [(-1,1,.7),(0,9,.7),(0,1,float('nan'))]:
            with self.assertRaises(ValueError):s.event(*args)
    def test_weights_unchanged_on_inference(self):
        c=self.c('recurrent');b=digest_tensors(self.repair.state_dict())
        with torch.no_grad():list(iterate(c,c.state(self.y),[128]))
        self.assertEqual(b,digest_tensors(self.repair.state_dict()))

if __name__=='__main__':unittest.main()
