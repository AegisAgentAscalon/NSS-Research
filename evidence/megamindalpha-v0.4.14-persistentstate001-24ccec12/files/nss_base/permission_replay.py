"""Narrow coordinator joining qualification, local grants and an experimental executor.

No generic Runtime permits are minted and no legacy simulator flags are redefined.
The adapter translates a validated consumed local grant to the existing probe's
explicit authorized=True fixture only at the fixed executor boundary.
"""
from .neural_contracts import fingerprint, pairs
from .permission_contracts import OPERATION, POLICY_HASH, request
from .permission_executor import action_receipts, require_executor, source_state, state_digest
from .permission_journal import fault
from .permission_store import Permissions
from .qualification_sources import require_source
from .qualification_store import Qualifications
from .runtime import ContractError, fail


def prepare_request(*, qualifications, source, qualification_id, request_id, caller_id, task_id, ledger):
    from .neural_backend import deterministic_cpu
    from .neural_execution import NeuralSession
    if type(qualifications) is not Qualifications:
        fail('VALIDATION_FAILED', 'Qualified evidence owner required')
    source = require_source(source)
    s = qualifications.inspect(qualification_id)
    if s['status'] != 'QUALIFIED' or s['request']['claim']['kind'] != 'TRANSITION':
        fail('INSUFFICIENT_EVIDENCE', 'An exact accepted transition is required')
    b = s['request']['binding']; c = s['request']['claim']; h = fingerprint(s['certificate'])
    qualifications.check_use(qualification_id, certificate_sha256=h, expected_claim=c, expected_binding=b, source=source)
    view = source.view(b['run_id'], b['trial_seed'], b['precision'])
    if view[4] != b: fail('INCOMPATIBLE_CONFIGURATION', 'Qualification source changed')
    with deterministic_cpu(b['trial_seed']):
        session = NeuralSession(view[1]['artifacts'], b['runtime_sha256'])
        state = session.state(c['source'], pairs('test')[:4], task_id)
    return request({'schema_version': 1, 'request_id': request_id, 'caller_id': caller_id,
        'task_id': task_id, 'operation': OPERATION, 'policy_sha256': POLICY_HASH,
        'qualification_id': qualification_id, 'certificate_sha256': h, 'claim': c, 'binding': b,
        'inputs': pairs('test')[:4], 'source_state_sha256': state_digest(state),
        'action_receipts': action_receipts(ledger, task_id)})


def execute_once(permissions, document, *, grant_sha256, caller_id, qualifications, source, executor, ledger, fault_at=None):
    if type(permissions) is not Permissions:
        fail('VALIDATION_FAILED', 'Permission owner required')
    executor = require_executor(executor); req = request(document)
    allowed = (None, 'before_consume_commit', 'after_consume_commit', 'after_dispatch_check',
               'before_executor_commit', 'after_executor_commit', 'before_completion_commit', 'after_completion_commit')
    if fault_at not in allowed: fail('VALIDATION_FAILED', 'Unknown dispatch fault point')
    begin_fault = fault_at if fault_at in ('before_consume_commit', 'after_consume_commit') else None
    begun = permissions.begin(req, grant_sha256=grant_sha256, caller_id=caller_id,
        qualifications=qualifications, source=source, fault_at=begin_fault)
    if begun['status'] == 'COMMITTED':
        # Validate authoritative receipt instead of trusting a COMMITTED label.
        return permissions.finish(req, grant_sha256=grant_sha256, actor_id=caller_id, executor=executor)
    try:
        # Check real source/action state BEFORE the last live authorization check.
        source_state(req, source, ledger)
        permissions.check_dispatch(req, grant_sha256=grant_sha256, caller_id=caller_id,
                                   qualifications=qualifications, source=source)
        fault(fault_at, 'after_dispatch_check')
        executor.perform(req, grant_sha256, source=source, ledger=ledger,
            fault_at=fault_at if fault_at in ('before_executor_commit', 'after_executor_commit') else None)
        return permissions.finish(req, grant_sha256=grant_sha256, actor_id=caller_id, executor=executor,
            fault_at=fault_at if fault_at in ('before_completion_commit', 'after_completion_commit') else None)
    except ContractError as exc:
        permissions.mark_uncertain(req['request_id'], grant_sha256, exc.code)
        raise
