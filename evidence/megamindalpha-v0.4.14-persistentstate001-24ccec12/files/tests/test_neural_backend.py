import copy
from pathlib import Path
import tempfile
import unittest
try:
    import torch
    from nss_base.neural_backend import (Core,Overlay,assert_frozen,checkpoint,deterministic_cpu,
        encode_pairs,freeze,load_checkpoint,metric,train_trial)
    from nss_base.neural_execution import NeuralSession,recovery_check
    HAVE_TORCH=True
except ImportError:HAVE_TORCH=False
from nss_base.neural_contracts import fingerprint,pairs,read_document
from nss_base.ledger import Ledger
from nss_base.runtime import ContractError
ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(HAVE_TORCH,'optional PyTorch backend not installed')
class NeuralBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=read_document(ROOT/'fixtures/neuralprobe001/protocol.json')
        p.update(seeds=[101],precisions=['ternary_core_reference'],core_steps=40,overlay_steps=80)
        cls.p=p;cls.result,cls.artifacts=train_trial(p,101,'ternary_core_reference',pairs('train'),pairs('test'),lambda:None)
    def bad(self,fn,*args,**kw):
        with self.assertRaises(ContractError):fn(*args,**kw)
    def session(self):return NeuralSession(copy.deepcopy(self.artifacts),'test-implementation')
    def test_core_actually_trained(self):self.assertTrue(self.result['invariants']['core_trained'])
    def test_core_frozen_after_fit(self):
        c=load_checkpoint(self.artifacts['core'],fingerprint(self.artifacts['core']));assert_frozen(c,fingerprint(self.artifacts['core']))
    def test_ternary_forward_values(self):self.assertTrue(set(self.result['effective_core_values'])<= {-1.,0.,1.})
    def test_overlays_not_claimed_ternary(self):self.assertEqual(self.result['overlay_precision'],'float32')
    def test_equal_parameter_control(self):self.assertEqual(self.result['parameters']['modular_total'],self.result['parameters']['joint'])
    def test_equal_token_presentations(self):
        t=self.result['training'];self.assertEqual(t['A']['train_input_tokens']+t['B']['train_input_tokens'],t['joint']['train_input_tokens'])
    def test_joint_steps_accounted(self):self.assertEqual(self.result['training']['joint']['updates'],160)
    def test_blank_overlay_noop(self):
        with deterministic_cpu(1):
            c=freeze(Core('fp32'));x=encode_pairs([[1,2]]);a=Overlay(4)
            self.assertTrue(torch.equal(c(x),c(x,a=a)))
    def test_candidate_gradient_flows_through_frozen_core(self):
        with deterministic_cpu(1):
            c=freeze(Core('fp32'));a=Overlay(4);x=encode_pairs([[1,2]])
            loss=(c(x,a=a)-x).square().mean();loss.backward()
            self.assertTrue(torch.count_nonzero(a.up.grad)>0)
            self.assertTrue(all(p.grad is None for p in c.parameters()))
    def test_checkpoint_roundtrip(self):
        for obj in self.artifacts.values():self.assertEqual(checkpoint(load_checkpoint(obj,fingerprint(obj))),obj)
    def test_wrong_checkpoint_hash(self):self.bad(load_checkpoint,self.artifacts['core'],'0'*64)
    def test_pickle_like_checkpoint_rejected(self):self.bad(load_checkpoint,{'pickle':'arbitrary'},fingerprint({'pickle':'arbitrary'}))
    def test_wrong_tensor_shape(self):
        c=copy.deepcopy(self.artifacts['A']);c['tensors']['up']['shape']=[1,2];self.bad(load_checkpoint,c,fingerprint(c))
    def test_nonfinite_tensor(self):
        c=copy.deepcopy(self.artifacts['A']);c['tensors']['up']['values'][0]=float('nan');self.bad(load_checkpoint,c,'0'*64)
    def test_float64_unrepresentable_value(self):
        c=copy.deepcopy(self.artifacts['A']);c['tensors']['up']['values'][0]=1.00000000001;self.bad(load_checkpoint,c,fingerprint(c))
    def test_role_substitution(self):
        c=copy.deepcopy(self.artifacts);c['core']=c['A'];self.bad(NeuralSession,c,'test')
    def test_core_mutation_detected(self):
        s=self.session()
        with torch.no_grad():s.modules['core'].w1[0,0]+=1
        self.bad(s.predict,'A',[[1,2]])
    def test_accept_valid_state(self):
        with deterministic_cpu(1):
            s=self.session();state=s.state('AB',[[1,2]],'task');self.assertTrue(torch.equal(s.accept(state,'AB','task'),state['cache']))
    def test_stale_state_rejected(self):
        s=self.session();state=s.state('AB',[[1,2]],'task');self.bad(s.accept,state,'A','task')
    def test_cross_task_rejected(self):
        s=self.session();state=s.state('A',[[1,2]],'task');self.bad(s.accept,state,'A','other')
    def test_cache_mutation_rejected(self):
        s=self.session();state=s.state('A',[[1,2]],'task');state['cache'][0,0,0]+=1;self.bad(s.accept,state,'A','task')
    def test_input_replacement_even_with_recomputed_hash_rejected(self):
        s=self.session();state=s.state('A',[[1,2]],'task');state['inputs']=[[3,4]];state['input_sha256']=fingerprint(state['inputs']);state['cache']=s.predict('A',state['inputs'])
        self.bad(s.accept,state,'A','task')
    def test_same_task_second_inputs_rejected(self):
        s=self.session();s.state('A',[[1,2]],'task');self.bad(s.state,'A',[[3,4]],'task')
    def test_unknown_profile(self):self.bad(self.session().predict,'BA',[[1,2]])
    def test_recovery_and_no_duplicate_mock_effect(self):
        with tempfile.TemporaryDirectory() as d,deterministic_cpu(1):
            l=Ledger(d);l.perform({'schema_version':1,'key':'one','task_id':'task','payload':{'operation':'append_marker','value':'once'},'status':'PENDING','receipt':None})
            r=recovery_check(self.artifacts,[[1,2]],'test',l,'task',1e-6,1e-6)
            self.assertTrue(r['recovered_equals_clean_exact']);self.assertEqual(r['committed_mock_effects'],1)
    def test_denial_preserves_state(self):
        with tempfile.TemporaryDirectory() as d:
            s=self.session();state=s.state('AB',[[1,2]],'task');r=s.recover(state,'A','task',Ledger(d))
            self.assertEqual(r['status'],'AUTHORIZATION_DENIED');self.assertIs(r['state'],state)
    def test_failed_load_preserves_state(self):
        with tempfile.TemporaryDirectory() as d:
            s=self.session();state=s.state('AB',[[1,2]],'task');r=s.recover(state,'A','task',Ledger(d),authorized=True,load_ok=False)
            self.assertEqual(r['status'],'INTERNAL_FAILURE');self.assertIs(r['state'],state)
    def test_random_state_restored(self):
        torch.manual_seed(77);before=torch.random.get_rng_state();threads=torch.get_num_threads()
        with deterministic_cpu(4):torch.randn(10)
        self.assertTrue(torch.equal(before,torch.random.get_rng_state()));self.assertEqual(threads,torch.get_num_threads())
    def test_repeat_training_is_deterministic(self):
        a,b=train_trial(self.p,101,'ternary_core_reference',pairs('train'),pairs('test'),lambda:None)
        self.assertEqual(b,self.artifacts);self.assertEqual(a['metrics'],self.result['metrics'])
    def test_gate_failure_stops_training(self):
        def denied():raise ContractError('TRAINING_RESTRICTED','fixture')
        with self.assertRaises(ContractError) as e:train_trial(self.p,101,'ternary_core_reference',pairs('train'),pairs('test'),denied)
        self.assertEqual(e.exception.code,'TRAINING_RESTRICTED')
