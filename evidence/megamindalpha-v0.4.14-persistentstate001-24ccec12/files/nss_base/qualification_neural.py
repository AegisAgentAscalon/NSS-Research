"""Narrow built-in qualification evidence adapter for NeuralProbe001.

Optional PyTorch is imported only when neural evidence is opened. No caller-supplied
scores, backend names, callbacks or code are accepted. Source owners are accessed
through their public APIs; this adapter owns no database and never trains anything.
"""
from copy import deepcopy
from pathlib import Path
import os

from .neural_contracts import CHECKER, encoded, fingerprint, pairs
from .qualification_contracts import POLICY, POLICY_HASH, binding, claim, request, verification
from .runtime import fail

LIMITS = [
    'Developer-visible, factorized linear toy tasks; not protected generalization evidence.',
    'Repeated inference of fixed checkpoints, not independent retraining or a new learned judge.',
    'Separate local reviewer workflow, not authentication, PKI or adversarial store protection.',
    'No deployment permission, native low-bit efficiency, general intelligence or model identity claim.',
    'Source eligibility is checked at points in time; no cross-store lease or exported-data recall.',
    'Transition evidence is restricted to its named input fixture, not arbitrary task states.',
]


def _api():
    try:
        import torch
        from .neuralprobe001 import check_current, verify_numerics
        from .neural_data import ProbeData
        from .neural_records import ProbeRuns
        from .neural_execution import NeuralSession
        from .neural_backend import deterministic_cpu
        from .ledger import Ledger
    except ImportError:
        fail('CAPABILITY_UNAVAILABLE', 'Neural qualification requires optional PyTorch')
    return torch, check_current, verify_numerics, ProbeData, ProbeRuns, NeuralSession, deterministic_cpu, Ledger


class NeuralEvidence:
    """Paths select existing owners; construction does not create or repair them."""
    def __init__(self, journal, data):
        if not all(isinstance(p, (str, os.PathLike)) for p in (journal, data)):
            fail('VALIDATION_FAILED', 'Expected local source-owner directories')
        self.journal = Path(journal)
        self.data_path = Path(data)

    def view(self, run_id, seed, precision, *, current=True):
        torch, check_current, _, Data, Runs, Session, _, _ = _api()
        stored = Runs(self.journal).inspect(run_id)
        if stored['status'] != 'FINALIZED':
            fail('INSUFFICIENT_EVIDENCE', 'A prepared experiment is not evaluation evidence')
        if stored['report']['verdict'] == 'INCONCLUSIVE':
            fail('INSUFFICIENT_EVIDENCE', 'Incomplete experiment has no qualifying artifact trial')
        data = Data(self.data_path)
        if current:
            check_current(stored['plan'], data)
        rows = [r for r in stored['report']['trials']
                if type(seed) is int and r['result']['seed'] == seed and r['result']['precision'] == precision]
        if len(rows) != 1:
            fail('INSUFFICIENT_EVIDENCE', 'Requested exact seed/precision is not in the report')
        row = rows[0]; plan = stored['plan']
        identity = fingerprint({'environment': plan['environment'], 'implementation': plan['code_sha256']})
        session = Session(row['artifacts'], identity)
        ecids = {p: session.catalog.ecid(p) for p in ('CORE', 'A', 'B', 'AB')}
        if row['recovery']['ecids'] != ecids:
            fail('VALIDATION_FAILED', 'Reported execution identities do not match exact artifacts')
        b = binding({
            'run_id': run_id, 'plan_sha256': fingerprint(plan),
            'report_sha256': fingerprint(stored['report']), 'trial_seed': seed, 'precision': precision,
            'checkpoint_hashes': deepcopy(row['result']['checkpoint_hashes']),
            'core_generation': session.catalog.generation, 'tokenizer': session.catalog.tokenizer,
            'context_abi': session.catalog.context_abi, 'overlay_abi': session.catalog.overlay_abi,
            'profile_ecids': ecids, 'runtime_sha256': identity, 'code_sha256': plan['code_sha256'],
            'environment_sha256': fingerprint(plan['environment']),
            'data_binding_sha256': fingerprint(plan['data_binding']),
            'test_pairs_sha256': fingerprint(pairs('test')),
            'transition_pairs_sha256': fingerprint(pairs('test')[:4]),
            'protocol_sha256': fingerprint(plan['protocol']), 'checker': CHECKER,
        })
        checker = {'name': 'qualification_neural_v1', 'code_sha256': plan['code_sha256'],
                   'numerical_backend_sha256': fingerprint({'torch': str(torch.__version__),
                       'build': torch.__config__.show(), 'cpu_capability': torch.backends.cpu.get_cpu_capability()})}
        return stored, row, data, session, b, checker

    def propose(self, *, run_id, seed, precision, scope, producer_id, request_id, at, prerequisites=()):
        _, _, _, _, b, _ = self.view(run_id, seed, precision)
        claim(scope, source_format=b.get('source_format'))
        return request({'schema_version': 1, 'request_id': request_id, 'producer_id': producer_id,
                        'at': at, 'claim': deepcopy(scope), 'binding': b,
                        'prerequisites': list(prerequisites), 'policy_sha256': POLICY_HASH,
                        'purpose': 'LOCAL_DEVELOPMENT_QUALIFICATION'})

    def guard(self, req):
        req = request(req); b = req['binding']
        view = self.view(b['run_id'], b['trial_seed'], b['precision'])
        if view[4] != b:
            fail('INCOMPATIBLE_CONFIGURATION', 'Current evidence differs from the frozen request')
        return view

    def verify(self, req):
        req = request(req)
        torch, _, verify_numerics, _, _, Session, deterministic, Ledger = _api()
        stored, row, data, session, b, checker = self.guard(req)
        out = {'schema_version': 1, 'request_sha256': fingerprint(req),
               'binding_sha256': fingerprint(b), 'claim': req['claim'], 'policy_sha256': POLICY_HASH,
               'verdict': 'INCONCLUSIVE', 'checks': [], 'repeats': [],
               'checker_identity': checker, 'limits': list(LIMITS), 'deployment_authorized': False}
        if stored['report']['verdict'] != 'PASS':
            out['verdict'] = 'FAIL'
            out['checks'] = [{'id': 'upstream_pass', 'passed': False,
                              'observed': stored['report']['verdict'], 'requirement': 'Completed upstream PASS'}]
            return verification(out)
        p = stored['plan']['protocol']; c = req['claim']
        if p['recovery_atol'] > POLICY['recovery_atol_max'] or p['recovery_rtol'] > POLICY['recovery_rtol_max']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Recovery tolerances exceed this claim policy')
        for repeat in range(POLICY['verification_repeats']):
            self.guard(req)
            # Public numerical verifier rejects fabricated scores and malformed checkpoints.
            verify_numerics(stored, data, current=True)
            observations = {'core_accuracy': row['result']['metrics']['core']['pair_accuracy']}
            if c['kind'] == 'PROFILE':
                key = 'core' if c['profile'] == 'CORE' else c['profile']
                observations['profile_accuracy'] = row['result']['metrics'][key]['pair_accuracy']
                if c['profile'] == 'AB':
                    m = row['result']['metrics']
                    observations['ablation_gap'] = m['AB']['pair_accuracy'] - max(m[k]['pair_accuracy'] for k in ('ablation_A', 'ablation_B', 'ablation_core'))
            else:
                from .neural_checks import replay_observations
                observations.update(replay_observations(Session, row['artifacts'], b, c,
                    atol=p['recovery_atol'], rtol=p['recovery_rtol']))
            out['repeats'].append(observations)
        checks = []
        def check(name, passed, observed, requirement):
            checks.append({'id': name, 'passed': bool(passed), 'observed': observed, 'requirement': requirement})
        o = out['repeats'][0]
        floor = max(POLICY['minimum_accuracy'], p['minimum_accuracy'])
        check('core_only', o['core_accuracy'] >= floor, o['core_accuracy'], f'Core-only pair accuracy >= {floor}')
        if c['kind'] == 'PROFILE':
            check('profile_accuracy', o['profile_accuracy'] >= floor, o['profile_accuracy'], f'Exact profile pair accuracy >= {floor}')
            if c['profile'] == 'AB':
                gap = max(POLICY['minimum_ablation_gap'], p['minimum_ablation_gap'])
                check('contribution_needed', o['ablation_gap'] >= gap, o['ablation_gap'], f'AB ablation gap >= {gap}')
        else:
            for name in ('stale_rejected', 'source_unchanged', 'tolerance_match', 'draft_cleared', 'denial_preserved', 'reverse_rejected'):
                check(name, o[name] is True, o[name], 'True in the exact directed transition fixture')
            check('one_checker_effect', o['checker_mock_effect_count'] == 1, o['checker_mock_effect_count'], 'Exactly one isolated checker effect')
        same = out['repeats'][0] == out['repeats'][1]
        check('repeatability', same, same, 'Two executions of the same checkpoints agree in this process/backend')
        out['checks'] = checks
        out['verdict'] = 'PASS' if all(v['passed'] for v in checks) else 'FAIL'
        self.guard(req)
        return verification(out)

