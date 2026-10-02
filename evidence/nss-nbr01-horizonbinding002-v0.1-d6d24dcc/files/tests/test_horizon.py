import inspect, tempfile, unittest
from pathlib import Path
import torch
from nbr01_horizon.data import *
from nbr01_horizon.models import MemoryModel, KINDS, WIDTH
from nbr01_horizon.util import weights_digest
from nbr01_horizon.state import Session
from nbr01_horizon.evaluate import calibrate


def fixture():
    return torch.tensor([[[0,2,.8],[1,3,.9],[0,7,.1],[0,4,.8],[2,6,.4]]],dtype=torch.float32)


class DataTests(unittest.TestCase):
    def test_expected_latest(self):self.assertEqual(labels_loop(fixture()).tolist(),[[4,3,8,8]])
    def test_exact_independent(self):self.assertEqual(exact_latest(fixture())[0].tolist(),[[4,3,8,8]])
    def test_empty(self):self.assertEqual(exact_latest(torch.empty(2,0,3))[0].tolist(),[[8]*4]*2)
    def test_boundary(self):
        x=torch.tensor([[[0,2,.4999],[1,3,.5],[2,4,.5001]]]);self.assertEqual(labels_loop(x).tolist(),[[8,3,4,8]])
    def test_reset(self):
        x=torch.cat((fixture(),torch.tensor([[[4,0,0.],[3,7,.8]]])),1)
        self.assertEqual(labels_loop(x).tolist(),[[8,8,8,7]]);self.assertTrue(torch.equal(labels_loop(x),exact_latest(x)[0]))
    def test_no_labels_in_exact_api(self):self.assertEqual(list(inspect.signature(exact_latest).parameters),['x'])
    def test_invalid_address(self):
        x=fixture();x[0,0,0]=9
        with self.assertRaises(ValueError):validate(x)
    def test_nonfinite(self):
        x=fixture();x[0,0,2]=float('nan')
        with self.assertRaises(ValueError):validate(x)
    def test_type(self):
        with self.assertRaises(ValueError):validate(fixture().double())
    def test_budget(self):
        with self.assertRaises(ValueError):validate(torch.zeros(1,4201,3))
    def test_score_range(self):
        x=fixture();x[0,0,2]=1.5
        with self.assertRaises(ValueError):validate(x)
    def test_fractional_key(self):
        x=fixture();x[0,0,0]=1.5
        with self.assertRaises(ValueError):validate(x)
    def test_train_determinism(self):
        a=training_batch(torch.Generator().manual_seed(9),16,32);b=training_batch(torch.Generator().manual_seed(9),16,32)
        self.assertTrue(all(torch.equal(x,y) for x,y in zip(a,b)))
    def test_eval_determinism_and_exact(self):
        for c in CONDITIONS:
            x,y,_=evaluation_batch(77,c,64,16);a,b,_=evaluation_batch(77,c,64,16)
            self.assertTrue(torch.equal(x,a));self.assertTrue(torch.equal(y,b))
            if c!='noisy_observation':self.assertTrue(torch.equal(y,exact_latest(x)[0]))
    def test_missing_count(self):
        for c in ['mixed_unknown','reset']:
            _,y,_=evaluation_batch(77,c,64,16);self.assertTrue(((y==8).sum(1)==2).all())
    def test_retained_all_known(self):
        _,y,_=evaluation_batch(77,'retain',64,16);self.assertTrue((y<8).all())
    def test_source_records(self):
        x=fixture();y,r=exact_latest(x)
        for k in range(4):
            if y[0,k]<8:self.assertTrue(any(torch.equal(e,r[0,k]) for e in x[0]))
    def test_noise_uses_hidden_truth_only_for_targets(self):
        x,y,_=evaluation_batch(77,'noisy_observation',256,64)
        self.assertFalse(torch.equal(y,exact_latest(x)[0]))


class ModelTests(unittest.TestCase):
    def test_finite_real_learning_all_arms(self):
        x,y=training_batch(torch.Generator().manual_seed(123),16,16)
        for kind in KINDS:
            torch.manual_seed(19);m=MemoryModel(kind);old=weights_digest(m)
            opt=torch.optim.AdamW(m.parameters(),lr=.003);z=m(x)
            loss=torch.nn.functional.cross_entropy(z.reshape(-1,9),y.flatten());loss.backward()
            self.assertTrue(all(torch.isfinite(p.grad).all() for p in m.parameters() if p.grad is not None))
            opt.step();self.assertNotEqual(old,weights_digest(m))
    def test_empty_all(self):
        for k in KINDS:self.assertTrue(torch.isfinite(MemoryModel(k)(torch.empty(2,0,3))).all())
    def test_affine_against_sequential(self):
        x,_=training_batch(torch.Generator().manual_seed(4),8,32)
        for kind in ['soft_slots','hard_slots']:
            for mode in ['native','hard','close_low']:
                m=MemoryModel(kind);h=torch.zeros(8,4,WIDTH);g=m.gates(x)
                if mode=='hard' or kind=='hard_slots' and mode=='native':g=(g>=.5).float()
                if mode=='close_low':g=torch.where(g>=.5,g,0.)
                val=m.value(x[:,:,1].long())
                for t in range(x.shape[1]):
                    key=x[:,t,0].long()
                    for b in range(len(x)):
                        if key[b]==4:h[b]=0
                        else:h[b,key[b]]=(1-g[b,t])*h[b,key[b]]+g[b,t]*val[b,t]
                self.assertTrue(torch.allclose(h,m.encode(x,mode=mode),atol=2e-6,rtol=1e-5))
    def test_gru_pack_against_cell(self):
        x,_=training_batch(torch.Generator().manual_seed(5),8,32)
        m=MemoryModel('gru_slots');cell=torch.nn.GRUCell(WIDTH+1,WIDTH)
        cell.load_state_dict({n:getattr(m.cell,n+'_l0') for n in ['weight_ih','weight_hh','bias_ih','bias_hh']})
        h=torch.zeros(8,4,WIDTH);vals=m.value(x[:,:,1].long())
        for t in range(32):
            for b in range(8):
                k=int(x[b,t,0])
                if k==4:h[b]=0
                else:h[b,k]=cell(torch.cat((vals[b,t],x[b,t,2:3])),h[b,k])
        self.assertTrue(torch.allclose(h,m.encode(x),atol=2e-6,rtol=1e-5))
    def test_encoding_chunks(self):
        x,_=training_batch(torch.Generator().manual_seed(6),8,32)
        for k in KINDS[:-1]:
            m=MemoryModel(k);a=m.encode(x);b=m.encode(x[:,17:],m.encode(x[:,:17]))
            self.assertTrue(torch.allclose(a,b,atol=2e-6,rtol=1e-5))
    def test_weights_fixed_during_eval(self):
        for k in KINDS:
            m=MemoryModel(k);old=weights_digest(m);m.predict_chunked(fixture());self.assertEqual(old,weights_digest(m))
    def test_wrong_mode(self):
        with self.assertRaises(ValueError):MemoryModel('soft_slots').encode(fixture(),mode='invented')
    def test_calibration_does_not_train(self):
        m=MemoryModel('soft_slots');old=weights_digest(m);a=calibrate(m,141);b=calibrate(m,141)
        self.assertEqual(a,b);self.assertEqual(old,weights_digest(m));self.assertEqual(a['labelled_events'],2048)


class SnapshotTests(unittest.TestCase):
    def test_roundtrip_continue_all(self):
        for kind in KINDS:
            m=MemoryModel(kind).eval();s=Session(m,'a');x=fixture();s.observe(x[:,:3])
            with tempfile.TemporaryDirectory() as td:
                s.save(Path(td)/'state');r=Session.restore(Path(td)/'state',m,'a')
                self.assertTrue(torch.equal(s.state,r.state));self.assertTrue(torch.equal(s.predict(),r.predict()))
                s.observe(x[:,3:]);r.observe(x[:,3:]);self.assertTrue(torch.equal(s.state,r.state))
    def test_no_query_mutation(self):
        m=MemoryModel('soft_slots');s=Session(m,'a');s.observe(fixture());a=s.state.clone();clock=s.events
        s.predict();s.predict();self.assertTrue(torch.equal(a,s.state));self.assertEqual(clock,s.events)
    def test_incompatible_scopes_policies_weights(self):
        m=MemoryModel('soft_slots');s=Session(m,'a');s.observe(fixture())
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'state';s.save(p)
            with self.assertRaises(ValueError):Session.restore(p,m,'b')
            with self.assertRaises(ValueError):Session.restore(p,m,'a','hard')
            with self.assertRaises(ValueError):Session.restore(p,m,'a',threshold=.7)
            with torch.no_grad():next(m.parameters()).add_(.01)
            with self.assertRaises(ValueError):Session.restore(p,m,'a')
    def test_corrupt_tensor(self):
        m=MemoryModel('soft_slots');s=Session(m,'a')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'state';s.save(p);f=p/'state.safetensors';f.write_bytes(f.read_bytes()+b'bad')
            with self.assertRaises(ValueError):Session.restore(p,m,'a')
    def test_refuse_overwrite(self):
        m=MemoryModel('soft_slots');s=Session(m,'a')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'state';s.save(p)
            with self.assertRaises(FileExistsError):s.save(p)
    def test_explicit_reset(self):
        m=MemoryModel('gru_slots');s=Session(m,'a');s.observe(fixture());s.reset('b')
        self.assertEqual(s.events,0);self.assertTrue(torch.equal(s.predict(),Session(m,'b').predict()))
    def test_session_batch_rejected(self):
        with self.assertRaises(ValueError):Session(MemoryModel('soft_slots'),'a').observe(fixture().expand(2,-1,-1))

if __name__=='__main__':unittest.main()
