"""Replaceable role protocol and explicitly non-neural deterministic test adapters.

The installed test implementations exercise data use, scheduling and persistence.
They neither train language models nor simulate unavailable native capabilities by
repeated prompting. Candidate-step counters test a job interface, not learning.
"""
from abc import ABC, abstractmethod
from copy import deepcopy
from .foundation_contracts import configuration, component
from .neural_contracts import fingerprint, encoded, fields
from .runtime import fail


class RoleAdapter(ABC):
    @abstractmethod
    def descriptor(self):
        """Return the exact pinned component descriptor."""

    @abstractmethod
    def parameter_sha256(self):
        """Inspect serving parameter bytes, not merely return a cached manifest hash."""

    @abstractmethod
    def step(self, request, state):
        """A bounded synchronous operation on copied input/state; no external effects.

        Return exactly payload, record_kind, source_references and state.
        Unsupported operations must raise NOT_SUPPORTED rather than substitute.
        """


class TestAdapter(RoleAdapter):
    __test__ = False

    def __init__(self, role_name, *, primary_generation='test-primary-g1', revision='test-r1',
                 wrong_validator=False):
        self.role = role_name
        self.primary_generation = primary_generation
        self.revision = revision
        self.parameters = {'adapter_role': role_name, 'revision': revision,
                           'wrong_validator': bool(wrong_validator)}
        self.calls = 0  # Diagnostic count, not canonical task state.

    def descriptor(self):
        caps = ['structured', 'text', 'temporal_state']
        if self.role == 'SECONDARY': caps += ['candidate_learning']
        return {'role': self.role, 'component_id': 'test-' + self.role.lower(), 'revision': self.revision,
                'implementation': 'deterministic-test-v1', 'weights_sha256': self.parameter_sha256(),
                'primary_generation': self.primary_generation, 'interface_version': 'exchange-v1',
                'state_schema': 'test-counter-v1', 'codec_version': 'json-v1', 'tokenizer_abi': None,
                'serving_frozen': True, 'capabilities': caps,
                'evidence_class': 'DETERMINISTIC_TEST_ADAPTER_NOT_NEURAL'}

    def parameter_sha256(self):
        return fingerprint(self.parameters)

    def step(self, request, state):
        if request['internal_depth'] != 1:
            fail('NOT_SUPPORTED', 'No native neural refinement in a structural test adapter')
        if request['operation'] == 'candidate_step' and self.role != 'SECONDARY':
            fail('NOT_SUPPORTED', 'No candidate step for this role')
        fields(state, ('calls',)) if state else None
        calls = state.get('calls', 0)
        if type(calls) is not int or calls < 0:
            fail('INCOMPATIBLE_CONFIGURATION', 'Wrong test state representation')
        self.calls += 1
        sources = request['allowed_source_references']
        facts = request['context']['facts']
        exact_value = facts[0]['value'] if facts else None
        if self.role == 'PRIMARY':
            # Evidence, rather than a fallible advisor, determines this simple result.
            payload = {'adapter': 'NON_NEURAL_TEST', 'phase': request['phase'],
                       'exact_value': exact_value,
                       'received_kinds': [m['record_kind'] for m in request['messages']],
                       'auxiliary_payloads': [deepcopy(m['payload']) for m in request['messages']],
                       'advice_is_not_veto': True}
            kind = 'derived'
        elif self.role == 'SECONDARY':
            payload = {'adapter': 'NON_NEURAL_TEST', 'input_received': bool(request['messages']),
                       'task_value': exact_value, 'operation': request['operation'],
                       'candidate_parameter_updates': 0}
            kind = 'derived'
        elif self.role == 'TERTIARY':
            payload = {'adapter': 'NON_NEURAL_TEST', 'hypothesis': 'An untested alternative scenario',
                       'observed_user_event': False}
            kind = 'hypothetical'
        else:
            payload = {'adapter': 'NON_NEURAL_TEST',
                       'relation': 'contradicted' if self.parameters['wrong_validator'] else 'not_established',
                       'challenge': 'Deliberately fallible test advice; not a model qualification result'}
            kind = 'derived'
        return {'payload': payload, 'record_kind': kind,
                'source_references': deepcopy(sources), 'state': {'calls': calls + 1}}


def test_configuration(*, primary_only=False, wrong_validator=False, generation_id='test-package-g1',
                       primary_generation='test-primary-g1', revision='test-r1'):
    adapters = {r: TestAdapter(r, primary_generation=primary_generation, revision=revision,
                             wrong_validator=wrong_validator if r == 'VALIDATOR' else False)
                for r in ('PRIMARY', 'SECONDARY', 'TERTIARY', 'VALIDATOR') if not primary_only or r == 'PRIMARY'}
    cfg = configuration({'schema_version': 1, 'generation_id': generation_id,
        'primary_generation': primary_generation, 'producer_id': 'builder',
        'execution_scope': 'TEST_ADAPTERS_ONLY',
        'components': {r: adapters[r].descriptor() if r in adapters else None
                       for r in ('PRIMARY', 'SECONDARY', 'TERTIARY', 'VALIDATOR')},
        'context_abi': 'scoped-context-v3', 'exchange_abi': 'exchange-v1',
        'limits': {'max_ticks': 100, 'max_state_bytes': 65536,
                   'max_message_bytes': 65536, 'callback_budget_ms': 1000}})
    return cfg, adapters
