"""Scripted, connected, trusted-local permission demo. No production authority."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

from .ledger import Ledger
from .neural_contracts import encoded, fingerprint, read_document
from .permission_executor import ReplayExecutor
from .permission_replay import prepare_request, execute_once
from .permission_store import Permissions
from .qualification_neural import NeuralEvidence
from .qualification_store import Qualifications
from .qualificationevidence002 import OPERATORS as REVIEW_OPERATORS, AT, review_for
from .runtime import ContractError, fail

OPERATORS = [{'id': 'local-owner', 'roles': ['ISSUER', 'RECONCILER']},
             {'id': 'local-runner', 'roles': ['EXECUTOR']},
             {'id': 'other-runner', 'roles': ['EXECUTOR']}]


def prepare_fixture(root):
    # Explicit opt-in demo setup only, not a permission-owner training capability.
    from .neuralprobe001 import DEFAULT, run as run_probe
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    p = read_document(DEFAULT); p['seeds'] = [101]; p['precisions'] = ['fp32']
    run_probe(root/'probe', p, withdraw=False)
    q = Qualifications.create(root/'qualification', REVIEW_OPERATORS)
    source = NeuralEvidence(root/'probe/journal', root/'probe/data')
    for key, scope, deps in [
        ('core', {'kind': 'PROFILE', 'profile': 'CORE'}, []),
        ('a', {'kind': 'PROFILE', 'profile': 'A'}, ['core']),
        ('ab', {'kind': 'PROFILE', 'profile': 'AB'}, ['core']),
        ('edge', {'kind': 'TRANSITION', 'source': 'AB', 'destination': 'A', 'mode': 'replay'}, ['core','ab','a'])]:
        req = source.propose(run_id='probe-001', seed=101, precision='fp32', scope=scope,
            producer_id='fixture-builder', request_id=key, at=AT, prerequisites=deps)
        q.prepare(req, source=source)
        decision = q.decide(review_for(req), source=source)
        if decision['verdict'] != 'QUALIFIED': fail('VALIDATION_FAILED', 'Fixture claim did not qualify')
    return q, source


def run(directory):
    from .neural_data import ProbeData
    from .neural_records import ProbeRuns
    root = Path(directory)
    if root.exists() and any(root.iterdir()): fail('CONSTRAINT_CONFLICT', 'Demo requires an empty directory')
    q, source = prepare_fixture(root)
    original = ProbeRuns(root/'probe/journal').inspect('probe-001')
    ledger = Ledger(root/'probe/mock_actions')
    permits = Permissions.create(root/'permissions', OPERATORS)
    executor = ReplayExecutor.create(root/'executor')
    def req(key):
        return prepare_request(qualifications=q, source=source, qualification_id='edge',
            request_id=key, caller_id='local-runner', task_id='neural-probe-replay', ledger=ledger)
    def issue(r):
        return permits.issue(r, issuer_id='local-owner', ttl_seconds=300, qualifications=q, source=source)
    def execute(r, h, caller='local-runner'):
        return execute_once(permits, r, grant_sha256=h, caller_id=caller, qualifications=q,
                            source=source, executor=executor, ledger=ledger)
    a = req('permitted-replay'); granted = issue(a); h = fingerprint(granted['grant'])
    denied = None
    try: execute(a, h, 'other-runner')
    except ContractError as exc: denied = exc.code
    done = execute(a, h); retry = execute(a, h)
    b = req('withdrawn-grant'); bh = fingerprint(issue(b)['grant'])
    permits.revoke(b['request_id'], grant_sha256=bh, actor_id='local-owner', revocation_id='withdraw-1', reason='Scripted operator withdrawal')
    revoked = None
    try: execute(b, bh)
    except ContractError as exc: revoked = exc.code
    c = req('qualification-withdrawn'); ch = fingerprint(issue(c)['grant'])
    core = q.inspect('core')
    q.revoke({'schema_version': 1, 'operation_id': 'withdraw-core', 'request_id': 'core',
              'certificate_sha256': fingerprint(core['certificate']), 'reviewer_id': 'fixture-reviewer',
              'at': AT, 'reason': 'Scripted prerequisite withdrawal'})
    qblocked = None
    try: execute(c, ch)
    except ContractError as exc: qblocked = exc.code
    ProbeData(root/'probe/data').revoke_for_test()
    old = execute(a, h)
    result = {'status': 'SUCCESS', 'scope': 'BOUNDED_TRUSTED_LOCAL_REPLAY_PERMISSION_DEMO',
        'wrong_caller': denied, 'committed': done['status'], 'retry_is_history': retry['historical'],
        'revoked_grant': revoked, 'revoked_qualification': qblocked,
        'expired_or_revoked_history_is_not_new_execution': old['historical'],
        'executor_results': executor.audit()['committed_results'], 'mock_external_effect_count': ledger.effect_count(),
        'original_report_unchanged': ProbeRuns(root/'probe/journal').inspect('probe-001') == original,
        'permissions_audit': permits.audit(), 'authenticated_identity': False,
        'runtime_execution_permit': False, 'deployment_authorized': False}
    if not (denied == revoked == qblocked == 'AUTHORIZATION_DENIED' and done['status'] == 'COMMITTED'
            and retry['historical'] and old['historical'] and result['executor_results'] == 1
            and result['mock_external_effect_count'] == 1 and result['original_report_unchanged']):
        fail('VALIDATION_FAILED', 'Connected permission invariants failed')
    (root/'summary.json').write_bytes(encoded(result)); return result


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--directory'); args = p.parse_args()
    try:
        if args.directory: result = run(args.directory)
        else:
            with TemporaryDirectory(prefix='megamind-permissions-') as d: result = run(d)
        print(encoded(result).decode()); return 0
    except ContractError as exc:
        print(encoded({'status': exc.code, 'detail': str(exc)}).decode(), file=sys.stderr); return 1


if __name__ == '__main__': raise SystemExit(main())
