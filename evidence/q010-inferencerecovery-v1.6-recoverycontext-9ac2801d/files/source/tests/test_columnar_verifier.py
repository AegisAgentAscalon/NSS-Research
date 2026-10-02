"""Regression and adversarial tests of the independent development evidence reader.

Saved inputs are declared development artifacts. No optimizer, no held-out tuning.
"""
from pathlib import Path
import copy,json,shutil,tempfile,unittest
import numpy as np
from q010c.protocol import ROOT
from q010v.verify import verify_frame,verify_capture,read_json,live_ledger,classify,VerificationError,path_in
from q010v.pointer_math import ReaderMathAuditError,verify_captured_pointer_arrays
from matrix_replay import generate_case_catalogue,MatrixReplayError

class ColumnarVerifierTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=ROOT/'results/dev64_attempt01/capture';cls.cap=read_json(cls.root/'CAPTURE.json')
 def frame(self,condition):
  c=next(c for c in self.cap['chunks'] if c['condition']==condition)
  with np.load(self.root/c['file'],allow_pickle=False) as z:raw={k:z[k].copy() for k in z.files}
  return raw,read_json(self.root/c['meta'])
 def test_registered_identity_need_not_have_a_fact(self):
  count=0
  for chunk in self.cap['chunks']:
   meta=read_json(self.root/chunk['meta'])
   for case in meta['cases']:
    tr=case['case_spec'].get('close_identity_transform')
    if tr and int(tr['target_id']) not in dict(case['truth_edges']):
     result=generate_case_catalogue(case['case_spec']);self.assertIn(int(tr['target_id']),result['symbol_ids']);count+=1
  self.assertGreater(count,0)
 def test_unregistered_close_target_is_rejected(self):
  specs=[case['case_spec'] for c in self.cap['chunks'] for case in read_json(self.root/c['meta'])['cases'] if case['case_spec'].get('close_identity_transform')]
  self.assertGreater(len(specs),0);bad=copy.deepcopy(specs[0]);bad['close_identity_transform']['target_id']=99999999
  with self.assertRaises(ValueError):generate_case_catalogue(bad)
 def test_registered_without_fact_stays_unknown(self):
  raw,meta=self.frame('registration_without_fact');rows,_=verify_frame(raw,meta)
  self.assertTrue(all(x['expected']==-1 for x in rows));self.assertTrue(all(x['evidence_class']=='lifecycle_absence' for x in rows))
 def test_future_fact_injection_rejected(self):
  raw,meta=self.frame('registration_without_fact');meta['live_facts']=[meta['cases'][0]['truth_edges']]
  with self.assertRaises(VerificationError):verify_frame(raw,meta)
 def test_no_valid_write_means_no_answer_ledger(self):
  _,meta=self.frame('registration_without_fact');self.assertEqual(live_ledger(meta,meta['cases'][0]),{})
 def test_read_mutation_flag_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');raw['ordinary__state_unchanged'][0,0]=False
  with self.assertRaises(VerificationError):verify_frame(raw,meta)
 def test_duplicate_owner_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');idx=np.flatnonzero(raw['state__present'][0]);self.assertGreater(len(idx),1);raw['state__owner'][0,idx[1]]=raw['state__owner'][0,idx[0]]
  with self.assertRaises(VerificationError):verify_frame(raw,meta)
 def test_selected_row_tamper_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');raw['ordinary__selected_rows'][0,0]=(raw['ordinary__selected_rows'][0,0]+1)%17
  with self.assertRaises(VerificationError):verify_frame(raw,meta)
 def test_arithmetic_tamper_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');raw['ordinary__read_code'][0,0,0]+=.02
  with self.assertRaises((VerificationError,ReaderMathAuditError)):verify_frame(raw,meta)
 def test_exact_control_contract_tamper_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');raw['exact_owner__logits'][0,0,0]+=1
  with self.assertRaises(VerificationError):verify_frame(raw,meta)
 def test_initial_query_tamper_rejected(self):
  raw,meta=self.frame('core_assisted_l04_d04');raw['initial_query'][0,0]+=.01
  for r in meta['readers']:raw[r+'__query'][0,0,0]+=.01
  with self.assertRaisesRegex(VerificationError,'source recipe'):verify_frame(raw,meta)
 def test_classification_does_not_truncate_truth(self):
  self.assertEqual(classify({1:2,2:3},1,2,1),('under_depth',3))
  self.assertEqual(classify({1:2},1,2,1),('unobservable_missing',-1))
  self.assertEqual(classify({1:2},1,2,2),('observable_missing',-1))
 def test_metadata_duplicate_keys_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.json';p.write_text('{"a":1,"a":2}')
   with self.assertRaises(VerificationError):read_json(p)
 def test_artifact_escape_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'root').mkdir();(p/'outside').write_text('x')
   with self.assertRaises(VerificationError):path_in(p/'root','../outside')
 def test_missing_condition_rejected_even_if_totals_altered(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);c=copy.deepcopy(self.cap);dropped=c['chunks'].pop(0);c['cells']=63;c['chains']-=24;c['logical_stage_evaluations']-=24
   (p/'CAPTURE.json').write_text(json.dumps(c));shutil.copyfile(self.root/'START.json',p/'START.json')
   with self.assertRaisesRegex(VerificationError,'declared condition'):verify_capture(p,p/'score')

if __name__=='__main__':unittest.main()
