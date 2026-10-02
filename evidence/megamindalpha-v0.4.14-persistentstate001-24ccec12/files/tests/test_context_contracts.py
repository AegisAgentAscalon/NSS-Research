"""Fast malformed-input and pure-planner coverage; no per-case neural setup."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from nss_base.context_contracts import make_request, request
from nss_base.context_plan import EvidenceReader, assemble
from nss_base.neural_contracts import read_document
from nss_base.runtime import ContractError
from nss_base.serialization import decode
ROOT=Path(__file__).resolve().parents[1]


def fixture():
    record=read_document(ROOT/'fixtures/stagehandoff001/task_record.json')
    ticket={'schema_version':1,'store_id':'store','ticket_id':'ticket','caller_id':'operator',
        'configuration':{'epoch':1,'generation_sha256':'b'*64},'profile':'CORE','profile_ecid':'a'*64,'state_reuse':'EXACT_TICKET_ONLY'}
    return {'record':record,'ticket':ticket,'task_state_identity':'c'*64}


class ContextContractsTests(unittest.TestCase):
    def expect(self, fn, *a):
        with self.assertRaises(ContractError) as e:fn(*a)
        self.assertIn(e.exception.code,('VALIDATION_FAILED','INCOMPATIBLE_CONFIGURATION'))

    def test_request_invalid_types_unknown_fields_and_bounds(self):
        r=make_request(fixture(),'operator')
        for key,value in [('schema_version',True),('format','wrong'),('caller_id',None),('required_fact_ids',['a','a']),
                          ('optional_fact_ids',['b','a']),('query_terms',['Speed']),('query_terms',[' speed']),
                          ('experiences',{}),('source_fields',[{'source_id':'s','field_id':[]}])]:
            with self.subTest(key=key):
                x=deepcopy(r);x[key]=value;self.expect(request,x)
        for key,value in [('max_context_bytes',0),('max_context_bytes',131073),('max_evidence_bytes',-1),('max_evidence_bytes',True),('unit','TOKENS')]:
            with self.subTest(budget=key,value=value):
                x=deepcopy(r);x['budget'][key]=value;self.expect(request,x)
        self.expect(request,{**r,'injected_policy':'override'})

    def test_duplicate_field_and_cross_candidate_slice_rejected(self):
        r=make_request(fixture(),'operator');r['source_fields']=[{'source_id':'a','field_id':'b'}]*2;self.expect(request,r)
        r=make_request(fixture(),'operator');r['evidence_slices']=[{'experience_id':'unknown','source_id':'s','source_sha256':'a'*64,'start_byte':0,'end_byte':1}]
        self.expect(request,r)

    def test_required_optional_conflict_and_invalid_archive_binding(self):
        r=make_request(fixture(),'operator');r['required_fact_ids']=r['optional_fact_ids']=['x'];self.expect(request,r)
        r=make_request(fixture(),'operator');r['archive_binding']={'format':'MegaMindAlpha.ExperienceArchive001','schema_version':1,'locator':'file:///x','sha256':'a'*64};self.expect(request,r)

    def test_cyclic_deep_nonfinite_and_duplicate_json_fail_typed(self):
        r={};r['cycle']=r;self.expect(request,r)
        self.expect(request,{'x':float('nan')})
        self.expect(decode,'{"caller_id":"a","caller_id":"b"}')

    def test_pure_plan_preserves_spine_and_is_deterministic(self):
        v=fixture();r=make_request(v,'operator');r['required_fact_ids']=['speed']
        def build():return assemble(r,v,EvidenceReader(ROOT/'fixtures/stagehandoff001',None,v['record'],2097152))
        a=build();self.assertEqual(a,build());self.assertEqual(a[0]['facts'][0]['unit'],'m/s')
        self.assertIsNone(v['record']['facts'][0]['unit'])

    def test_unknown_source_field_and_malformed_fixture_inputs(self):
        from nss_base.task_records import source_document
        from hashlib import sha256
        v=fixture();r=make_request(v,'operator')
        r['source_fields']=[{'source_id':'source-1','field_id':'no-such-field'}]
        with self.assertRaises(ContractError) as e:assemble(r,v,EvidenceReader(ROOT/'fixtures/stagehandoff001',None,v['record'],2097152))
        self.assertEqual(e.exception.code,'INSUFFICIENT_EVIDENCE')
        with tempfile.TemporaryDirectory() as d:
            for raw in [b'{"schema_version":1,"schema_version":1,"fields":[]}',b'\xff',b'{"schema_version":1,"fields":[{"id":"x","value":"v","unit":null},{"id":"x","value":"v","unit":null}]}']:
                Path(d,'x.json').write_bytes(raw);source={'artifact':{'path':'x.json','sha256':sha256(raw).hexdigest()}}
                self.expect(source_document,d,source)

    def test_exact_field_unknown_required_unit_requests_clarification(self):
        from hashlib import sha256
        from nss_base.neural_contracts import encoded
        v=fixture();r=make_request(v,'operator');v['record']['stage']['required_facts']=[{'fact_id':'speed','fields':['unit']}]
        with tempfile.TemporaryDirectory() as d:
            raw=encoded({'schema_version':1,'fields':[{'id':'speed','value':'10','unit':None}]})
            Path(d,'problem.json').write_bytes(raw);v['record']['sources'][0]['artifact']['sha256']=sha256(raw).hexdigest()
            with self.assertRaises(ContractError) as e:assemble(r,v,EvidenceReader(d,None,v['record'],2097152))
            self.assertEqual(e.exception.code,'NEEDS_CLARIFICATION')

    def test_shared_source_reader_root_escape_and_byte_budget(self):
        from nss_base.task_records import source_document
        for path in ('../x','/etc/passwd','x\\y'):
            self.expect(source_document,ROOT,{'artifact':{'path':path,'sha256':'a'*64}})
        with self.assertRaises(ContractError) as e:source_document(ROOT/'fixtures/stagehandoff001',fixture()['record']['sources'][0],byte_limit=0)
        self.assertEqual(e.exception.code,'BUDGET_EXHAUSTED')
