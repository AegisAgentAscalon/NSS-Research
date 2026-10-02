from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from nss_base.neural_contracts import read_document
from nss_base.permission_contracts import POLICY, POLICY_HASH, epoch, manifest, request, grant
from nss_base.permission_store import Permissions
from nss_base.permission_executor import ReplayExecutor
from nss_base.localnexuspermissions002 import OPERATORS
from nss_base.runtime import ContractError
from permission_helpers import PermissionCase


class PermissionPureTests(unittest.TestCase):
    def test_epoch_rejects_bad_types_bounds(self):
        for value in (True,-1,1.5,'1',None,253402300800):
            with self.subTest(value=value), self.assertRaises(ContractError): epoch(value)
    def test_missing_store_not_recreated(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ContractError): Permissions(Path(d)/'missing')
            self.assertFalse((Path(d)/'missing').exists())
    def test_missing_executor_not_recreated(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ContractError): ReplayExecutor(Path(d)/'missing')
            self.assertFalse((Path(d)/'missing').exists())
    def test_create_existing_store_refused(self):
        with tempfile.TemporaryDirectory() as d:
            Permissions.create(d,OPERATORS)
            with self.assertRaises(ContractError): Permissions.create(d,OPERATORS)
    def test_create_existing_executor_refused(self):
        with tempfile.TemporaryDirectory() as d:
            ReplayExecutor.create(d)
            with self.assertRaises(ContractError): ReplayExecutor.create(d)
    def test_operator_roles_bounded_distinct(self):
        bads=[[],[{'id':'one','roles':['ISSUER','EXECUTOR','RECONCILER']}],OPERATORS+[OPERATORS[0]],
              [{'id':'a','roles':['ROOT']},OPERATORS[1]],
              [{'id':'a','roles':['ISSUER','ISSUER']},OPERATORS[1]],
              [{'id':'a','roles':['ISSUER']},OPERATORS[1]]]
        for value in bads:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as d, self.assertRaises(ContractError):
                Permissions.create(d,value)
    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('{"caller_id":"a","caller_id":"b"}')
            with self.assertRaises(ContractError): read_document(p)
    def test_nonfinite_and_overdeep_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for content in ('{"x":1e999}','['*40+'1'+']'*40):
                p=Path(d)/'x';p.write_text(content)
                with self.assertRaises(ContractError): read_document(p)


class PermissionContractTests(PermissionCase):
    def test_exact_request_roundtrip(self): self.assertEqual(request(self.operation),self.operation)
    def test_extra_field_rejected(self):
        r=deepcopy(self.operation);r['approve_all']=True;self.error('VALIDATION_FAILED',request,r)
    def test_missing_field_rejected(self):
        for k in self.operation:
            with self.subTest(field=k):
                r=deepcopy(self.operation);del r[k];self.error('VALIDATION_FAILED',request,r)
    def test_unsupported_operation(self):
        for op in ('DEPLOY','RUN_TOOL','TRAIN','NEURAL_PROBE_REPLAY_ALL',None,{}):
            with self.subTest(operation=op):
                r=deepcopy(self.operation);r['operation']=op;self.error('INCOMPATIBLE_CONFIGURATION',request,r)
    def test_request_schema_bool_or_unknown(self):
        for version in (True,0,2,'1'):
            r=deepcopy(self.operation);r['schema_version']=version;self.error('INCOMPATIBLE_CONFIGURATION',request,r)
    def test_profile_claim_not_operation_authority(self):
        r=deepcopy(self.operation);r['claim']={'kind':'PROFILE','profile':'AB'}
        self.error('INCOMPATIBLE_CONFIGURATION',request,r)
    def test_unqualified_reverse_rejected(self):
        r=deepcopy(self.operation);r['claim']['source']='A';r['claim']['destination']='AB'
        self.error('INCOMPATIBLE_CONFIGURATION',request,r)
    def test_input_scope_not_widened(self):
        for inp in ([],[[1,2]],self.operation['inputs']*2):
            r=deepcopy(self.operation);r['inputs']=inp;self.error('INCOMPATIBLE_CONFIGURATION',request,r)
    def test_boolean_symbols_rejected(self):
        r=deepcopy(self.operation);r['inputs'][0][0]=False;self.error('VALIDATION_FAILED',request,r)
    def test_bad_state_certificate_hash(self):
        for k in ('source_state_sha256','certificate_sha256'):
            r=deepcopy(self.operation);r[k]='not-sha256';self.error('VALIDATION_FAILED',request,r)
    def test_duplicate_action_receipts(self):
        r=deepcopy(self.operation);r['action_receipts']*=2;self.error('VALIDATION_FAILED',request,r)
    def test_invalid_ttl_does_not_issue(self):
        for value in (True,0,-1,901,1.5):
            self.error('VALIDATION_FAILED',self.issue,ttl_seconds=value)
        self.assertEqual(self.permits.audit()['grants'],0)
    def test_mutated_policy_fails_closed(self):
        old=POLICY['max_uses']
        try:
            POLICY['max_uses']=2;self.error('INCOMPATIBLE_CONFIGURATION',self.issue)
        finally: POLICY['max_uses']=old
    def test_returned_request_cannot_mutate_store(self):
        s=self.issue();s['request']['inputs'].clear();self.assertEqual(self.permits.inspect('permission-1')['request'],self.operation)
