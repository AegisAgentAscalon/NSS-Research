"""Opt-in synthetic integrated generation demo, not a production model server.

Reuses one trained family to release progressively wider qualified catalogues. No
new weights are trained by the manager and no new neural advantage is asserted.
"""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
from .generation_evidence import from_evidence
from .generation_store import Generations
from .ledger import Ledger
from .localnexuspermissions002 import prepare_fixture
from .neural_contracts import encoded, fingerprint, pairs
from .neural_records import ProbeRuns
from .qualificationevidence002 import AT, review_for
from .runtime import ContractError, fail

OPERATORS = [{'id': 'fixture-builder', 'roles': ['PRODUCER']},
             {'id': 'generation-reviewer', 'roles': ['REVIEWER']},
             {'id': 'release-owner', 'roles': ['ISSUER']},
             {'id': 'local-runner', 'roles': ['OPERATOR']}]


def prepare_generations(root):
    q, source = prepare_fixture(root)
    req = source.propose(run_id='probe-001', seed=101, precision='fp32',
        scope={'kind': 'TRANSITION', 'source': 'A', 'destination': 'CORE', 'mode': 'replay'},
        producer_id='fixture-builder', request_id='core-return', at=AT, prerequisites=['core','a'])
    q.prepare(req, source=source)
    if q.decide(review_for(req), source=source)['verdict'] != 'QUALIFIED':
        fail('VALIDATION_FAILED', 'Return-to-Core fixture did not qualify')
    return q, source


def run(directory):
    root = Path(directory)
    if root.exists() and any(root.iterdir()): fail('CONSTRAINT_CONFLICT', 'Demo needs an empty directory')
    q, source = prepare_generations(root); ev = {'qualifications': q, 'source': source}
    baseline = ProbeRuns(root/'probe/journal').inspect('probe-001')
    ledger = Ledger(root/'probe/mock_actions')
    manager = Generations.create(root/'generations', OPERATORS)
    def candidate(name, profiles, edges):
        g = from_evidence(name, 'fixture-builder', profiles, edges, qualifications=q)
        h = manager.propose(g, **ev)['generation_sha256']
        manager.qualify(h, reviewer_id='generation-reviewer', **ev)
        return h
    first = candidate('G1-overlays-1', ['core','a'], ['core-return'])
    second = candidate('G1-overlays-2', ['core','a','ab'], ['edge','core-return'])
    def grant(h, name, mode):
        r = manager.make_request(h, release_id=name, caller_id='local-runner', mode=mode,
                                 reason='Scripted local generation demonstration')
        s = manager.issue(r, issuer_id='release-owner', ttl_seconds=600, **ev)
        return {'grant_sha256': fingerprint(s['grant']), 'caller_id':'local-runner', **ev}
    opts = grant(first, 'bootstrap', 'BOOTSTRAP')
    for fn in (manager.prepare, manager.stage, manager.publish): fn('bootstrap', **opts)
    old = manager.inspect()['current']
    update = grant(second, 'update', 'UPDATE')
    manager.prepare('update', **update); manager.stage('update', **update)
    source_stays_current = manager.inspect()['current'] == old
    ticket = manager.pin_stage('stage-before-update', profile='A', caller_id='local-runner', **ev)
    read = manager.read_stage(ticket, caller_id='local-runner', **ev)
    try: manager.publish('update', **update)
    except ContractError as e: busy = e.code
    else: busy = 'NOT_BLOCKED'
    manager.close_stage(ticket, caller_id='local-runner')
    released = manager.publish('update', **update)
    try: manager.read_stage(ticket, caller_id='local-runner', **ev)
    except ContractError as e: stale = e.code
    else: stale = 'NOT_BLOCKED'
    t = manager.pin_stage('stage-after-update', profile='AB', caller_id='local-runner', **ev)
    active = manager.read_stage(t, caller_id='local-runner', **ev)
    # A real forward pass consumes only the registered profile's staged bytes.
    from .neural_backend import deterministic_cpu, load_checkpoint, encode_pairs
    with deterministic_cpu(101):
        import torch
        modules = {k: load_checkpoint(v, fingerprint(v)) for k,v in active['artifacts'].items()}
        with torch.no_grad(): values = modules['core'](encode_pairs(pairs('test')[:4]), a=modules['A'], b=modules['B'])
    manager.close_stage(t, caller_id='local-runner')
    back = grant(first, 'rollback', 'ROLLBACK')
    for fn in (manager.prepare, manager.stage, manager.publish): fn('rollback', **back)
    after = manager.inspect()['current']
    historical = manager.publish('update', **update)
    no_republish = manager.inspect()['current'] == after
    manager.revoke(first, kind='QUALIFICATION', actor_id='generation-reviewer', reason='Scripted release qualification withdrawal')
    try: manager.pin_stage('after-withdrawal', profile='CORE', caller_id='local-runner', **ev)
    except ContractError as e: blocked = e.code
    else: blocked = 'NOT_BLOCKED'
    summary = {'status': 'SUCCESS', 'scope': 'LOCAL_CATALOG_PUBLICATION_WITH_REAL_ARTIFACTS',
        'source_current_until_publish': source_stays_current, 'busy_publication': busy,
        'stale_ticket': stale, 'generation_epochs': [old['epoch'], released['receipt']['current']['epoch'], after['epoch']],
        'rollback_exact_generation': after['generation_sha256'] == first,
        'retry_is_history_without_republish': historical['historical'] and no_republish,
        'current_withdrawal_blocks_new_stages': blocked, 'forward_shape': list(values.shape),
        'active_artifact_roles': sorted(active['artifacts']), 'old_stage_artifact_roles': sorted(read['artifacts']),
        'mock_external_effect_count': ledger.effect_count(),
        'original_neural_report_unchanged': baseline == ProbeRuns(root/'probe/journal').inspect('probe-001'),
        'audit': manager.audit(), 'runtime_execution_permit': False, 'production_deployment_authorized': False}
    if not (source_stays_current and busy == 'RECOVERY_REQUIRED' and stale == 'INCOMPATIBLE_CONFIGURATION'
            and blocked == 'AUTHORIZATION_DENIED' and summary['rollback_exact_generation']
            and summary['retry_is_history_without_republish'] and summary['mock_external_effect_count'] == 1
            and summary['original_neural_report_unchanged']):
        fail('VALIDATION_FAILED', 'Generation demo invariant failed')
    (root/'summary.json').write_bytes(encoded(summary)); return summary


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--directory'); a = p.parse_args()
    try:
        if a.directory: r = run(a.directory)
        else:
            with TemporaryDirectory(prefix='megamind-generation-') as d: r = run(d)
        print(encoded(r).decode()); return 0
    except ContractError as e:
        print(encoded({'status': e.code, 'detail': str(e)}).decode(), file=sys.stderr); return 1


if __name__ == '__main__': raise SystemExit(main())
