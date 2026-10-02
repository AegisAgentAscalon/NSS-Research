import copy
import json
from pathlib import Path
import tempfile
import unittest

from nss_base.neural_contracts import (CODEC, encoded, fingerprint, mapping, pairs,
    protocol, read_document, required_updates, validate_pairs, trial_verdict)
from nss_base.runtime import ContractError

ROOT=Path(__file__).resolve().parents[1]

class NeuralContractTests(unittest.TestCase):
    def setUp(self):self.p=read_document(ROOT/'fixtures/neuralprobe001/protocol.json')
    def bad(self,fn,*args):
        with self.assertRaises(ContractError):fn(*args)
    def test_protocol_valid(self):self.assertEqual(protocol(self.p),self.p)
    def test_protocol_extra_fields(self):self.p['callback']='eval';self.bad(protocol,self.p)
    def test_protocol_missing_field(self):del self.p['rank'];self.bad(protocol,self.p)
    def test_version_bool_rejected(self):self.p['schema_version']=True;self.bad(protocol,self.p)
    def test_unknown_architecture(self):self.p['architecture']='arbitrary.py';self.bad(protocol,self.p)
    def test_unknown_codec(self):self.p['codec']='words';self.bad(protocol,self.p)
    def test_unknown_precision(self):self.p['precisions']=['fp16'];self.bad(protocol,self.p)
    def test_duplicate_mode(self):self.p['precisions']=['fp32','fp32'];self.bad(protocol,self.p)
    def test_duplicate_seed(self):self.p['seeds']=[1,1];self.bad(protocol,self.p)
    def test_seed_bool(self):self.p['seeds']=[True];self.bad(protocol,self.p)
    def test_negative_budget(self):self.p['max_optimizer_steps']=-1;self.bad(protocol,self.p)
    def test_excess_budget(self):self.p['max_optimizer_steps']=100001;self.bad(protocol,self.p)
    def test_float_budget(self):self.p['core_steps']=1.2;self.bad(protocol,self.p)
    def test_nan_threshold(self):self.p['minimum_accuracy']=float('nan');self.bad(protocol,self.p)
    def test_infinite_nested(self):self.bad(encoded,{'a':[float('inf')]})
    def test_cycle_rejected(self):v=[];v.append(v);self.bad(encoded,v)
    def test_duplicate_json(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'a.json';f.write_text('{"a":1,"a":2}');self.bad(read_document,f)
    def test_overflow_json_number(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'a.json';f.write_text('{"a":1e999}');self.bad(read_document,f)
    def test_splits_exact_and_disjoint(self):
        a,b,c=[{tuple(p) for p in pairs(s)} for s in ('train','validation','test')]
        self.assertEqual((len(a),len(b),len(c)),(128,64,64));self.assertFalse(a&b or a&c or b&c);self.assertEqual(len(a|b|c),256)
    def test_all_symbols_seen_in_train(self):self.assertEqual({v for row in pairs('train') for v in row},set(range(16)))
    def test_duplicate_pairs(self):self.bad(validate_pairs,[[0,1],[0,1]])
    def test_boolean_symbol(self):self.bad(validate_pairs,[[True,1]])
    def test_wrong_split(self):self.bad(validate_pairs,pairs('test'),'train')
    def test_unknown_mapping(self):self.bad(mapping,[])
    def test_maps_noncommute(self):
        a,b=mapping('A'),mapping('B');self.assertNotEqual([b[x] for x in a],[a[x] for x in b])
        self.assertEqual(mapping('AB'),[b[x] for x in a])
    def test_gen2_only_changes_requested_symbols(self):
        self.assertEqual([i for i,(a,b) in enumerate(zip(mapping('A'),mapping('A2'))) if a!=b],[5,6])
    def test_exact_update_budget(self):self.assertEqual(required_updates(self.p),11940)
    def test_codec_stable(self):self.assertEqual(CODEC['width'],16);self.assertEqual(len(CODEC['symbols']),16)
    def test_fingerprint_key_order(self):self.assertEqual(fingerprint({'x':1,'y':2}),fingerprint({'y':2,'x':1}))
    def test_verdict_missing_required_metric(self):self.bad(trial_verdict,self.p,{})
