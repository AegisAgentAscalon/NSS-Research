"""Local command-line review interface. This is not an authenticated service.

Usage: python -m nss_base.experience_cli --archive ./my-archive init
Use capture/apply/revoke-source with explicit JSON request files. Exact files can
be retried using their original operation IDs. All non-success exits use code 2.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from .experience_contracts import MAX_COMMAND_BYTES, bounded_copy
from .experience_store import ExperienceArchive
from .runtime import ContractError, fail
from .serialization import decode


def read_request(path):
    try:
        with Path(path).open('rb') as source: raw=source.read(MAX_COMMAND_BYTES+1)
        if len(raw)>MAX_COMMAND_BYTES:fail('VALIDATION_FAILED','Request file exceeds byte budget')
        return bounded_copy(decode(raw.decode('utf-8')))
    except (OSError,UnicodeError,RecursionError):
        fail('VALIDATION_FAILED','Request is unreadable, invalid UTF-8, or excessively nested')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',required=True,help='Local archive directory (no networking)')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('init');sub.add_parser('audit')
    for name in ('capture','apply','revoke-source'):
        p=sub.add_parser(name);p.add_argument('request',help='Exact JSON request file')
    p=sub.add_parser('list');p.add_argument('--limit',type=int,default=100);p.add_argument('--after')
    p=sub.add_parser('show');p.add_argument('id');p.add_argument('--revision')
    p=sub.add_parser('history');p.add_argument('id')
    p=sub.add_parser('source');p.add_argument('sha256')
    p=sub.add_parser('use');p.add_argument('id');p.add_argument('--purpose',required=True);p.add_argument('--expected',required=True)
    p=sub.add_parser('prepare-review',help='Write a review request to stdout; does not approve anything')
    p.add_argument('id');p.add_argument('--decision',choices=('APPROVED','REJECTED'),required=True)
    p.add_argument('--reviewer',required=True);p.add_argument('--operation-id',required=True)
    p.add_argument('--reason',required=True);p.add_argument('--at',help='UTC timestamp; defaults to now')
    args=parser.parse_args(argv)
    try:
        store=ExperienceArchive.create(args.archive) if args.command=='init' else ExperienceArchive(args.archive)
        if args.command in ('init','audit'):result=store.audit()
        elif args.command=='capture':result=store.capture(read_request(args.request))
        elif args.command=='apply':result=store.change(read_request(args.request))
        elif args.command=='revoke-source':result=store.revoke_source(read_request(args.request))
        elif args.command=='list':result=store.list_records(limit=args.limit,after=args.after)
        elif args.command=='show':result=store.inspect(args.id,revision_hash=args.revision)
        elif args.command=='history':result=store.history(args.id)
        elif args.command=='source':result=store.inspect_source(args.sha256)
        elif args.command=='use':result=store.read_for_use(args.id,purpose=args.purpose,expected_revision_hash=args.expected)
        else:
            result=store.inspect(args.id)
            if result['status']=='SUCCESS':
                request={'schema_version':1,'operation_id':args.operation_id,'experience_id':args.id,
                    'expected_revision_hash':result['data']['reference']['sha256'],
                    'actor':{'id':args.reviewer,'kind':'HUMAN','version':'local-cli-v1'},
                    'at':args.at or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'reason':args.reason,'action':'REVIEW','payload':{'decision':args.decision}}
                # Validate before writing a usable request; preparation does not mutate.
                from .experience_contracts import normalize
                normalize(request,'CHANGE')
                print(json.dumps(request,indent=2,ensure_ascii=True))
                return 0
        print(json.dumps(result,indent=2,ensure_ascii=True))
        return 0 if result['status']=='SUCCESS' else 2
    except ContractError as exc:
        print(json.dumps({'status':exc.code,'data':None,'detail':str(exc)},ensure_ascii=True))
        return 2


if __name__=='__main__':sys.exit(main())
