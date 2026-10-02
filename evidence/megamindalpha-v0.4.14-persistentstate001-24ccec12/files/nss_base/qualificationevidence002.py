"""Connected, explicitly scripted local review demo; no real operator authentication."""
import argparse
from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from .neural_contracts import encoded, fingerprint, read_document
from .qualification_contracts import POLICY
from .qualification_neural import NeuralEvidence
from .qualification_store import Qualifications
from .runtime import ContractError, fail

OPERATORS = [{'id': 'fixture-builder', 'roles': ['PRODUCER']},
             {'id': 'fixture-reviewer', 'roles': ['REVIEWER']},
             {'id': 'fixture-both', 'roles': ['PRODUCER', 'REVIEWER']}]
AT = '2026-09-11T12:00:00Z'


def review_for(req, recommendation='ACCEPT', reviewer='fixture-reviewer'):
    return {'schema_version': 1, 'operation_id': 'review:'+req['request_id'],
        'request_id': req['request_id'], 'request_sha256': fingerprint(req),
        'reviewer_id': reviewer, 'at': AT, 'recommendation': recommendation,
        'reason': 'Scripted trusted-local review of the exact synthetic development claim only.'}


def run(directory):
    # Explicit demo coordination is the ONLY place in this subsystem calling training.
    from .neuralprobe001 import run as run_probe, DEFAULT
    from .neural_data import ProbeData
    from .neural_records import ProbeRuns
    from .ledger import Ledger
    root = Path(directory)
    if root.exists() and any(root.iterdir()):
        fail('CONSTRAINT_CONFLICT', 'Demo requires a new/empty directory')
    root.mkdir(parents=True, exist_ok=True)
    p = read_document(DEFAULT); p['seeds'] = [101]; p['precisions'] = ['fp32']
    run_probe(root/'probe', p, withdraw=False)
    source = NeuralEvidence(root/'probe/journal', root/'probe/data')
    original = ProbeRuns(root/'probe/journal').inspect('probe-001')
    q = Qualifications.create(root/'qualification', OPERATORS)
    prepared = {}; receipts = {}
    def add(identity, scope, prerequisites=(), recommendation='ACCEPT'):
        req = source.propose(run_id='probe-001', seed=101, precision='fp32', scope=scope,
            producer_id='fixture-builder', request_id=identity, at=AT, prerequisites=prerequisites)
        q.prepare(req, source=source); prepared[identity] = req
        receipts[identity] = q.decide(review_for(req, recommendation), source=source)
        return req
    add('core', {'kind': 'PROFILE', 'profile': 'CORE'})
    add('a', {'kind': 'PROFILE', 'profile': 'A'}, ['core'])
    add('ab', {'kind': 'PROFILE', 'profile': 'AB'}, ['core'])
    add('ab-to-a', {'kind': 'TRANSITION', 'source': 'AB', 'destination': 'A', 'mode': 'replay'}, ['core', 'ab', 'a'])
    add('a-to-core', {'kind': 'TRANSITION', 'source': 'A', 'destination': 'CORE', 'mode': 'replay'}, ['a', 'core'])
    def use(key, scope=None):
        req = prepared[key]
        return q.check_use(key, certificate_sha256=receipts[key]['certificate_sha256'],
            expected_claim=scope or req['claim'], expected_binding=req['binding'], source=source)
    checks = {k: use(k)['status'] for k in prepared}
    blocked = {}
    try:
        use('ab', {'kind': 'PROFILE', 'profile': 'A'})
    except ContractError as exc:
        blocked['subset_inference'] = exc.code
    try:
        use('ab-to-a', {'kind': 'TRANSITION', 'source': 'A', 'destination': 'AB', 'mode': 'replay'})
    except ContractError as exc:
        blocked['reverse_inference'] = exc.code
    req = add('human-reject', {'kind': 'PROFILE', 'profile': 'CORE'}, recommendation='REJECT')
    add('human-inconclusive', {'kind': 'PROFILE', 'profile': 'CORE'}, recommendation='INCONCLUSIVE')
    self_req = source.propose(run_id='probe-001', seed=101, precision='fp32', scope={'kind': 'PROFILE', 'profile': 'CORE'},
        producer_id='fixture-both', request_id='self-review', at=AT)
    q.prepare(self_req, source=source)
    try:
        q.decide(review_for(self_req, reviewer='fixture-both'), source=source)
    except ContractError as exc:
        blocked['self_review'] = exc.code
    before = q.inspect('ab-to-a')
    q.revoke({'schema_version': 1, 'operation_id': 'revoke-core', 'request_id': 'core',
        'certificate_sha256': receipts['core']['certificate_sha256'], 'reviewer_id': 'fixture-reviewer',
        'at': AT, 'reason': 'Scripted check of dependency-safe withdrawal.'})
    try:
        use('ab-to-a')
    except ContractError as exc:
        blocked['revoked_prerequisite'] = exc.code
    history_retry = q.decide(review_for(prepared['ab-to-a']), source=source)
    # Independent fresh Core claim lets the demo distinguish data revocation from dependency revocation.
    add('core-data-check', {'kind': 'PROFILE', 'profile': 'CORE'})
    ProbeData(root/'probe/data').revoke_for_test()
    try:
        use('core-data-check')
    except ContractError as exc:
        blocked['source_training_revoked'] = exc.code
    expected = {'subset_inference': 'INCOMPATIBLE_CONFIGURATION', 'reverse_inference': 'INCOMPATIBLE_CONFIGURATION',
                'self_review': 'AUTHORIZATION_DENIED', 'revoked_prerequisite': 'AUTHORIZATION_DENIED',
                'source_training_revoked': 'TRAINING_RESTRICTED'}
    if blocked != expected or q.inspect('ab-to-a') != before or not history_retry['historical']:
        fail('VALIDATION_FAILED', 'Qualification boundary demo failed')
    unchanged = ProbeRuns(root/'probe/journal').inspect('probe-001') == original
    effects = Ledger(root/'probe/mock_actions').effect_count()
    if not unchanged or effects != 1:
        fail('VALIDATION_FAILED', 'Qualification mutated source evidence or repeated its effect')
    summary = {'status': 'SUCCESS', 'scope': POLICY['scope'], 'qualified_checks': checks,
        'blocked': blocked, 'historical_retry': history_retry['historical'],
        'source_report_unchanged': unchanged, 'source_mock_effect_count': effects,
        'stored_evidence_audit': q.audit(), 'deployment_authorized': False,
        'roles': 'SCRIPTED_LOCAL_OPERATOR_ATTESTATIONS_NOT_AUTHENTICATED_PEOPLE'}
    (root/'qualification_summary.json').write_bytes(encoded(summary))
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--directory'); args = p.parse_args()
    try:
        if args.directory:
            result = run(args.directory)
        else:
            with TemporaryDirectory(prefix='megamind-qualification002-') as d:
                result = run(d)
        print(encoded(result).decode()); return 0
    except ContractError as exc:
        print(encoded({'status': exc.code, 'detail': str(exc), 'deployment_authorized': False}).decode(), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
