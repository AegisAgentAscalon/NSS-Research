"""Local trusted-operator qualification CLI; it never deploys or executes a permit."""
import argparse
import sys

from .neural_contracts import encoded, read_document
from .qualification_sources import add_source_arguments, source_from_args
from .qualification_store import Qualifications
from .runtime import ContractError


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init'); init.add_argument('--operators', required=True)
    prop = sub.add_parser('propose')
    for k in ('run-id', 'precision', 'claim', 'producer', 'request-id', 'at'):
        prop.add_argument('--'+k, required=True)
    add_source_arguments(prop)
    prop.add_argument('--seed', type=int, required=True)
    prop.add_argument('--prerequisite', action='append', default=[])
    prep = sub.add_parser('prepare'); prep.add_argument('--request', required=True)
    review = sub.add_parser('review'); review.add_argument('--decision', required=True)
    use = sub.add_parser('check'); use.add_argument('--request', required=True); use.add_argument('--certificate-sha256', required=True)
    for parser in (prep, use):
        add_source_arguments(parser)
    add_source_arguments(review)
    rev = sub.add_parser('revoke'); rev.add_argument('--revocation', required=True)
    for name in ('inspect', 'history'):
        cmd = sub.add_parser(name); cmd.add_argument('--request-id', required=True)
    sub.add_parser('audit')
    args = p.parse_args(argv)
    try:
        if args.command == 'init':
            result = Qualifications.create(args.store, read_document(args.operators)).audit()
        elif args.command == 'propose':
            result = source_from_args(args).propose(run_id=args.run_id, seed=args.seed,
                precision=args.precision, scope=read_document(args.claim), producer_id=args.producer,
                request_id=args.request_id, at=args.at, prerequisites=args.prerequisite)
        else:
            store = Qualifications(args.store)
            source = source_from_args(args, optional=True)
            if args.command == 'prepare':
                result = store.prepare(read_document(args.request), source=source)
            elif args.command == 'review':
                result = store.decide(read_document(args.decision), source=source)
            elif args.command == 'check':
                req = read_document(args.request)
                result = store.check_use(req['request_id'], certificate_sha256=args.certificate_sha256,
                    expected_claim=req['claim'], expected_binding=req['binding'], source=source)
            elif args.command == 'revoke':
                result = store.revoke(read_document(args.revocation))
            elif args.command == 'inspect':
                result = store.inspect(args.request_id)
            elif args.command == 'history':
                result = store.history(args.request_id)
            else:
                result = store.audit()
        print(encoded(result).decode())
        return 0
    except ContractError as exc:
        print(encoded({'status': exc.code, 'detail': str(exc), 'deployment_authorized': False}).decode(), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
