"""Explicit local operator CLI; declared identities are NOT authenticated users."""
import argparse
from pathlib import Path
import sys
from .neural_contracts import encoded, read_document
from .permission_executor import ReplayExecutor
from .permission_replay import execute_once, prepare_request
from .permission_store import Permissions
from .qualification_neural import NeuralEvidence
from .qualification_store import Qualifications
from .ledger import Ledger
from .runtime import ContractError, fail


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init'); init.add_argument('--operators', required=True)
    ex = sub.add_parser('init-executor'); ex.add_argument('--executor', required=True)
    for name in ('prepare', 'issue', 'execute'):
        s = sub.add_parser(name)
        for arg in ('qualifications', 'journal', 'data'): s.add_argument('--'+arg, required=True)
        if name == 'prepare':
            for arg in ('qualification-id', 'request-id', 'caller', 'task', 'actions'): s.add_argument('--'+arg, required=True)
        else:
            s.add_argument('--request', required=True)
            if name == 'issue':
                s.add_argument('--issuer', required=True); s.add_argument('--ttl', type=int, default=300)
            else:
                for arg in ('grant-sha256', 'caller', 'executor', 'actions'): s.add_argument('--'+arg, required=True)
    s = sub.add_parser('reconcile')
    for arg in ('request', 'grant-sha256', 'actor', 'executor'): s.add_argument('--'+arg, required=True)
    s = sub.add_parser('revoke')
    for arg in ('request-id', 'grant-sha256', 'actor', 'revocation-id', 'reason'): s.add_argument('--'+arg, required=True)
    s = sub.add_parser('inspect'); s.add_argument('--request-id', required=True)
    sub.add_parser('history'); sub.add_parser('audit')
    args = p.parse_args()
    try:
        if args.command == 'init':
            result = Permissions.create(args.store, read_document(args.operators)).audit()
        elif args.command == 'init-executor':
            result = ReplayExecutor.create(args.executor).audit()
        else:
            store = Permissions(args.store)
            if args.command in ('prepare', 'issue', 'execute'):
                q = Qualifications(args.qualifications); source = NeuralEvidence(args.journal, args.data)
                if args.command in ('prepare', 'execute'):
                    # Never implicitly create an empty action history on a read.
                    if not all((Path(args.actions)/n).is_file() for n in ('ledger.sqlite3', 'mock_world.sqlite3')):
                        fail('RECOVERY_REQUIRED', 'Existing mock action ledger pair is required')
                    ledger = Ledger(args.actions)
                if args.command == 'prepare':
                    result = prepare_request(qualifications=q, source=source, qualification_id=args.qualification_id,
                        request_id=args.request_id, caller_id=args.caller, task_id=args.task, ledger=ledger)
                elif args.command == 'issue':
                    result = store.issue(read_document(args.request), issuer_id=args.issuer,
                        ttl_seconds=args.ttl, qualifications=q, source=source)
                else:
                    result = execute_once(store, read_document(args.request), grant_sha256=args.grant_sha256,
                        caller_id=args.caller, qualifications=q, source=source,
                        executor=ReplayExecutor(args.executor), ledger=ledger)
            elif args.command == 'inspect': result = store.inspect(args.request_id)
            elif args.command == 'audit': result = store.audit()
            elif args.command == 'history': result = store.history()
            elif args.command == 'revoke':
                result = store.revoke(args.request_id, grant_sha256=args.grant_sha256, actor_id=args.actor,
                    revocation_id=args.revocation_id, reason=args.reason)
            else:
                result = store.finish(read_document(args.request), grant_sha256=args.grant_sha256,
                    actor_id=args.actor, executor=ReplayExecutor(args.executor), reconcile=True)
        print(encoded(result).decode()); return 0
    except ContractError as exc:
        print(encoded({'status': exc.code, 'detail': str(exc), 'deployment_authorized': False}).decode(), file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
