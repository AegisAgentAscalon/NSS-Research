import json
from pathlib import Path
import tempfile
import unittest

import torch
from nbr01_pilot.core import (RecallModel, Session, batch, oracle, exact_memory_tape,
                             parameter_digest, KINDS, digest_bytes, canonical)
from nbr01_pilot.experiment import configure

configure()

class DataTests(unittest.TestCase):
    def test_exact_overwrite(self):
        x=torch.tensor([[2,12,4,10],[13,14,15,9]])
        self.assertEqual(oracle(x).tolist(),[4,8])
    def test_distractors_not_writes(self):
        self.assertEqual(oracle(torch.tensor([[1,9,11,13]])).item(),1)
    def test_unknown(self):
        self.assertEqual(oracle(torch.empty(1,0,dtype=torch.int64)).item(),8)
    def test_seed_determinism(self):
        a=batch(torch.Generator().manual_seed(1),64,16)
        b=batch(torch.Generator().manual_seed(1),64,16)
        self.assertTrue(all(torch.equal(x,y) for x,y in zip(a,b)))
    def test_control_observations_only(self):
        x=torch.tensor([[2,12,4,10],[13,14,15,9]])
        self.assertEqual(exact_memory_tape(x).tolist(),[[4],[16]])
    def test_train_label_oracle(self):
        for d in (0,4,16,64,128):
            x,y=batch(torch.Generator().manual_seed(d),128,d,'overwrite')
            self.assertTrue(torch.equal(oracle(x),y))
    def test_bad_data_bounds(self):
        with self.assertRaises(ValueError):batch(torch.Generator(),64,129)
    def test_no_negative_tokens(self):
        with self.assertRaises(ValueError):oracle(torch.tensor([[-1]]))
    def test_no_float_tokens(self):
        with self.assertRaises(ValueError):oracle(torch.tensor([[1.0]]))

class ModelTests(unittest.TestCase):
    def test_parameters_really_train(self):
        for kind in KINDS:
            torch.manual_seed(7);m=RecallModel(kind);before=parameter_digest(m)
            x,y=batch(torch.Generator().manual_seed(5),16,4)
            o=torch.optim.AdamW(m.parameters(),lr=.003)
            loss=torch.nn.functional.cross_entropy(m(x,2),y);loss.backward()
            self.assertTrue(all(torch.isfinite(p.grad).all() for p in m.parameters() if p.grad is not None))
            o.step();self.assertNotEqual(before,parameter_digest(m))
    def test_depth_not_event_count(self):
        for kind in KINDS:
            s=Session(RecallModel(kind).eval(),'scope');s.observe(torch.tensor([[2,12,13]]))
            before=s.state.clone()
            for d in (1,2,4,8):
                self.assertEqual(s.predict(d).shape,(1,9))
                self.assertTrue(torch.equal(before,s.state));self.assertEqual(s.events,3)
    def test_state_off_no_information(self):
        for kind in KINDS:
            model=RecallModel(kind).eval();s=Session(model,'scope',False)
            s.observe(torch.tensor([[3,13,15]]))
            fresh=Session(model,'scope',False)
            self.assertTrue(torch.equal(s.predict(4),fresh.predict(4)))
    def test_wrong_depth(self):
        with self.assertRaises(ValueError):RecallModel('gru')(torch.tensor([[1]]),3)
    def test_unknown_kind(self):
        with self.assertRaises(ValueError):RecallModel('not-model')
    def test_budget_refusal_no_state_change(self):
        s=Session(RecallModel('gru'),'scope');before=s.state.clone()
        with self.assertRaises(ValueError):s.observe(torch.ones(1,161,dtype=torch.int64))
        self.assertTrue(torch.equal(before,s.state));self.assertEqual(s.events,0)
    def test_no_query_as_temporal(self):
        s=Session(RecallModel('gru'),'scope')
        with self.assertRaises(ValueError):s.observe(torch.tensor([[16]]))
    def test_exact_carry_hardgate(self):
        m=RecallModel('hard_gated').eval()
        with torch.no_grad():m.gate.weight.zero_();m.gate.bias.fill_(-100)
        h=torch.randn(1,1,32)
        updated=m.encode(torch.tensor([[2,13,4,15]]),h)
        self.assertTrue(torch.equal(h,updated))
    def test_hard_gate_gradients(self):
        m=RecallModel('hard_gated');x,y=batch(torch.Generator().manual_seed(10),16,4)
        torch.nn.functional.cross_entropy(m(x),y).backward()
        self.assertGreater(float(m.gate.weight.grad.abs().sum()),0)
    def test_reset_isolation(self):
        for kind in KINDS:
            m=RecallModel(kind).eval();old=Session(m,'old');old.observe(torch.tensor([[2,10,4]]))
            new=Session(m,'new');self.assertEqual(new.events,0)
            self.assertTrue(torch.equal(new.predict(),m(torch.empty(1,0,dtype=torch.int64))))

class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def make(self,kind='gru'):
        m=RecallModel(kind).eval();s=Session(m,'scope');s.observe(torch.tensor([[2,12,4]]))
        path=self.root/kind;s.checkpoint(path);return m,s,path
    def test_roundtrip_all(self):
        for kind in KINDS:
            m,s,p=self.make(kind);r=Session.restore(p,m,'scope')
            self.assertTrue(torch.equal(s.state,r.state));self.assertEqual(s.events,r.events)
            for d in (1,2,4,8):self.assertTrue(torch.equal(s.predict(d),r.predict(d)))
    def test_resume_all(self):
        for kind in KINDS:
            m,s,p=self.make(kind);r=Session.restore(p,m,'scope')
            tail=torch.tensor([[15,7,10]])
            s.observe(tail);r.observe(tail);self.assertTrue(torch.equal(s.predict(4),r.predict(4)))
    def test_refuse_overwrite(self):
        m,s,p=self.make()
        with self.assertRaises(FileExistsError):s.checkpoint(p)
    def test_scope(self):
        m,s,p=self.make()
        with self.assertRaises(ValueError):Session.restore(p,m,'different')
    def test_model(self):
        m,s,p=self.make()
        with torch.no_grad():next(m.parameters()).view(-1)[0].add_(1)
        with self.assertRaises(ValueError):Session.restore(p,m,'scope')
    def test_policy(self):
        m,s,p=self.make()
        with self.assertRaises(ValueError):Session.restore(p,m,'scope',False)
    def test_bad_checksum(self):
        m,s,p=self.make();a=p/'metadata.json';v=json.loads(a.read_text());v['events']=4;a.write_text(json.dumps(v))
        with self.assertRaises(ValueError):Session.restore(p,m,'scope')
    def test_bad_payload(self):
        m,s,p=self.make();a=p/'state.safetensors';a.write_bytes(a.read_bytes()+b'X')
        with self.assertRaises(ValueError):Session.restore(p,m,'scope')
    def test_bool_schema_refused(self):
        m,s,p=self.make();a=p/'metadata.json';v=json.loads(a.read_text());v.pop('metadata_sha256');v['schema']=True
        v['metadata_sha256']=digest_bytes(canonical(v));a.write_text(json.dumps(v))
        with self.assertRaises(ValueError):Session.restore(p,m,'scope')

if __name__=='__main__':unittest.main()
