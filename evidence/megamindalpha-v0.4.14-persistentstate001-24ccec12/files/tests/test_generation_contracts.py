"""Table-driven boundary mutations: case names identify each preserved failure path."""
from copy import deepcopy
from generation_helpers import GenerationCase
from nss_base.generation_contracts import generation, release_request, store_manifest, POLICY_HASH, FORMAT
from nss_base.generation_evidence import check_family, from_evidence
from nss_base.neural_contracts import fingerprint
from nss_base.overlaygenerationmanager001 import OPERATORS
from nss_base.runtime import ContractError


class GenerationContractTests(GenerationCase):
    def test_exact_manifests_accept_and_copy(self):
        for g in self.gs:
            x = generation(g); self.assertEqual(x, g); self.assertIsNot(x, g)

    def test_invalid_generation_documents_fail_typed(self):
        cases = {
            'missing_core': lambda g: g.update(profiles=[p for p in g['profiles'] if p['id']!='CORE']),
            'extra_field': lambda g: g.update(deployment_authorized=True),
            'bool_version': lambda g: g.update(schema_version=True),
            'wrong_shape_members': lambda g: g.update(members={}),
            'duplicate_member': lambda g: g['members'].append(deepcopy(g['members'][0])),
            'wrong_hash': lambda g: g['members'][0].update(sha256='0'*64),
            'wrong_ecid': lambda g: g['profiles'][0].update(ecid='0'*64),
            'profile_outside_generation': lambda g: g.update(members=g['members'][:1]),
            'duplicate_profile': lambda g: g['profiles'].append(deepcopy(g['profiles'][0])),
            'invented_union': lambda g: g['profiles'][0].update(members=['A','B']),
            'unknown_profile': lambda g: g['profiles'][0].update(id='NEW'),
            'unknown_member': lambda g: g['members'][0].update(id='A2'),
            'dependency_missing': lambda g: g['members'][0].update(requires=['B']),
            'cyclic_dependencies': lambda g: [g['members'][0].update(requires=['B']), g['members'][1].update(requires=['A'])],
            'self_dependency': lambda g: g['members'][0].update(requires=['A']),
            'no_return': lambda g: g.update(transitions=[]),
            'reverse_invented': lambda g: g['transitions'][0].update(source='CORE',destination='A'),
            'state_reuse_invented': lambda g: g['transitions'][0].update(state_policy='REUSE_CACHE'),
            'duplicate_transition': lambda g: g['transitions'].append(deepcopy(g['transitions'][0])),
            'tokenizer_changed': lambda g: g['binding'].update(tokenizer='other'),
            'unknown_purpose': lambda g: g.update(purpose='PRODUCTION'),
            'non_json': lambda g: g.update(members=set()),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                g = deepcopy(self.gs[1]); mutate(g)
                with self.assertRaises(ContractError): generation(g)
        for x in (None, [], 'manifest', True):
            with self.subTest(shape=repr(x)), self.assertRaises(ContractError): generation(x)

    def test_restrictive_dependency_is_allowed_only_with_closed_profiles(self):
        g = deepcopy(self.gs[1]); g['members'][1]['requires']=['A']
        self.assertEqual(generation(g),g)

    def test_manifest_preserves_ordered_profile_attachment(self):
        g=deepcopy(self.gs[1]);next(p for p in g['profiles'] if p['id']=='AB')['members'].reverse()
        self.error('VALIDATION_FAILED',generation,g)

    def test_only_core_family_is_supported(self):
        g=from_evidence('core-only-family','fixture-builder',['core'],[],qualifications=self.q)
        self.assertEqual(g['members'],[]);self.assertEqual(len(g['profiles']),1)
        check_family(g,**self.ev)

    def test_no_claim_inference_from_individual_members(self):
        g=deepcopy(self.gs[1]);next(p for p in g['profiles'] if p['id']=='AB')['evidence']=deepcopy(self.gs[0]['profiles'][0]['evidence'])
        with self.assertRaises(ContractError):check_family(g,**self.ev)

    def test_missing_or_wrong_certificate_or_binding_rejected(self):
        for name in ('missing','hash','different_seed','wrong_report'):
            with self.subTest(case=name):
                g=deepcopy(self.gs[0])
                if name=='missing':g['profiles'][0]['evidence']['id']='absent'
                elif name=='hash':g['profiles'][0]['evidence']['sha256']='0'*64
                elif name=='different_seed':g['binding']['trial_seed']=102
                else:g['binding']['report_sha256']='0'*64
                with self.assertRaises(ContractError):check_family(g,**self.ev)

    def test_replay_permission_cannot_be_used_as_release_request(self):
        self.error('VALIDATION_FAILED',release_request,{'operation':'NEURAL_PROBE_REPLAY'})
        r=self.request();r['operation']='NEURAL_PROBE_REPLAY'
        self.error('INCOMPATIBLE_CONFIGURATION',release_request,r)

    def test_release_document_strictness(self):
        for mutate in (lambda r:r.update(schema_version=True),lambda r:r.update(mode='AUTO'),
            lambda r:r['expected_current'].update(epoch=True),lambda r:r.update(extra=1),
            lambda r:r.update(target_sha256='bad'),lambda r:r.update(caller_id='')):
            r=self.request();mutate(r)
            with self.subTest(value=r),self.assertRaises(ContractError):release_request(r)

    def test_store_roles_are_strict_not_inferred(self):
        m={'schema_version':1,'format':FORMAT,'store_id':'store','policy_sha256':POLICY_HASH,'operators':deepcopy(OPERATORS)}
        self.assertEqual(store_manifest(m),m)
        for role in ('EXECUTOR','ADMIN',''):
            x=deepcopy(m);x['operators'][0]['roles']=[role]
            with self.subTest(role=role),self.assertRaises(ContractError):store_manifest(x)

    def test_unqualified_and_missing_manifests_cannot_issue_release(self):
        g=deepcopy(self.gs[0]);g['generation_id']='unreviewed'
        h=self.manager.propose(g,**self.ev)['generation_sha256']
        self.error('INSUFFICIENT_EVIDENCE',self.manager.make_request,h,release_id='x',caller_id='local-runner',mode='BOOTSTRAP',reason='Test')
        self.error('INSUFFICIENT_EVIDENCE',self.manager.inspect_generation,'0'*64)

    def test_producer_cannot_review_even_if_role_is_declared(self):
        from nss_base.generation_store import Generations
        ops=deepcopy(OPERATORS);ops[0]['roles'].append('REVIEWER')
        s=Generations.create(self.root/'roles',ops);h=s.propose(self.gs[0],**self.ev)['generation_sha256']
        self.error('AUTHORIZATION_DENIED',s.qualify,h,reviewer_id='fixture-builder',**self.ev)

    def test_manifest_name_cannot_be_redefined(self):
        g=deepcopy(self.gs[1]);g['generation_id']=self.gs[0]['generation_id']
        self.error('CONSTRAINT_CONFLICT',self.manager.propose,g,**self.ev)

    def test_mutating_returned_record_does_not_change_store(self):
        x=self.manager.inspect_generation(self.hashes[0]);x['manifest']['members'].clear()
        self.assertEqual(self.manager.inspect_generation(self.hashes[0])['manifest'],self.gs[0])
