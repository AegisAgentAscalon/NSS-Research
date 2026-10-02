"""Explicit local operator CLI. No automatic training, model download or deployment."""
import argparse
import sys
from .generation_store import Generations
from .neural_contracts import encoded, read_document
from .qualification_sources import add_source_arguments, source_from_args
from .qualification_store import Qualifications
from .runtime import ContractError


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('create'); c.add_argument('--operators', required=True)
    sub.add_parser('inspect'); sub.add_parser('audit')
    c = sub.add_parser('inspect-release'); c.add_argument('--release', required=True)
    c = sub.add_parser('inspect-stage'); c.add_argument('--ticket-id', required=True)
    c = sub.add_parser('propose'); c.add_argument('--manifest', required=True)
    c = sub.add_parser('qualify'); c.add_argument('--generation', required=True); c.add_argument('--reviewer', required=True)
    c = sub.add_parser('request'); c.add_argument('--generation', required=True); c.add_argument('--release', required=True)
    c.add_argument('--caller', required=True); c.add_argument('--mode', choices=['BOOTSTRAP','UPDATE','ROLLBACK'], required=True); c.add_argument('--reason', required=True)
    c = sub.add_parser('issue'); c.add_argument('--request', required=True); c.add_argument('--issuer', required=True); c.add_argument('--ttl', type=int, default=300)
    for cmd in ('prepare', 'stage', 'publish'):
        c = sub.add_parser(cmd); c.add_argument('--release', required=True); c.add_argument('--grant-hash', required=True); c.add_argument('--caller', required=True)
    c = sub.add_parser('abandon'); c.add_argument('--release', required=True); c.add_argument('--caller', required=True); c.add_argument('--reason', required=True)
    c = sub.add_parser('revoke'); c.add_argument('--identity', required=True); c.add_argument('--kind', choices=['RELEASE','QUALIFICATION'], required=True); c.add_argument('--actor', required=True); c.add_argument('--reason', required=True)
    c = sub.add_parser('pin-stage'); c.add_argument('--ticket-id', required=True); c.add_argument('--profile', required=True); c.add_argument('--caller', required=True)
    for cmd in ('read-stage', 'close-stage'):
        c = sub.add_parser(cmd); c.add_argument('--ticket', required=True); c.add_argument('--caller', required=True)
    for name in ('propose','qualify','issue','prepare','stage','publish','pin-stage','read-stage'):
        c = sub.choices[name]; c.add_argument('--qualification', required=True); add_source_arguments(c)
    a = p.parse_args(argv)
    try:
        if a.command == 'create':
            result = Generations.create(a.store, read_document(a.operators)).inspect()
        else:
            store = Generations(a.store); evidence = {}
            if hasattr(a, 'qualification'):
                evidence = {'qualifications': Qualifications(a.qualification), 'source': source_from_args(a)}
            cmd = a.command
            if cmd == 'inspect': result = store.inspect()
            elif cmd == 'audit': result = store.audit()
            elif cmd == 'inspect-release': result = store.inspect_release(a.release)
            elif cmd == 'inspect-stage': result = store.inspect_stage(a.ticket_id)
            elif cmd == 'propose': result = store.propose(read_document(a.manifest), **evidence)
            elif cmd == 'qualify': result = store.qualify(a.generation, reviewer_id=a.reviewer, **evidence)
            elif cmd == 'request': result = store.make_request(a.generation, release_id=a.release, caller_id=a.caller, mode=a.mode, reason=a.reason)
            elif cmd == 'issue': result = store.issue(read_document(a.request), issuer_id=a.issuer, ttl_seconds=a.ttl, **evidence)
            elif cmd in ('prepare','stage','publish'): result = getattr(store,cmd)(a.release, grant_sha256=a.grant_hash, caller_id=a.caller, **evidence)
            elif cmd == 'abandon': result = store.abandon(a.release, caller_id=a.caller, reason=a.reason)
            elif cmd == 'revoke': result = store.revoke(a.identity, kind=a.kind, actor_id=a.actor, reason=a.reason)
            elif cmd == 'pin-stage': result = store.pin_stage(a.ticket_id, profile=a.profile, caller_id=a.caller, **evidence)
            elif cmd == 'read-stage': result = store.read_stage(read_document(a.ticket), caller_id=a.caller, **evidence)
            else: result = store.close_stage(read_document(a.ticket), caller_id=a.caller)
        print(encoded(result).decode()); return 0
    except (ContractError, OSError) as e:
        print(encoded({'status': getattr(e, 'code','RECOVERY_REQUIRED'), 'detail': str(e)}).decode(), file=sys.stderr); return 1


if __name__ == '__main__': raise SystemExit(main())
