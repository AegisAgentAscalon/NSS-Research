"""Local DatasetSnapshot001 commands. No network, neural training or auto-review.

prepare-build is a request editor, not permission or publication. inspect/list/
audit/receipt are administrative, not training access. read rechecks permissions
and returns a bounded split as JSON; redirecting it exports bytes that cannot be
recalled by later revocation. Non-success exits 2.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys

from .dataset_contracts import MAX_MANIFEST_BYTES, MAX_TOKENIZER_BYTES, normalize_request
from .dataset_store import DatasetSnapshots
from .experience_contracts import bounded_copy
from .experience_store import ExperienceArchive
from .runtime import ContractError, fail
from .serialization import decode


def read_request(path):
    try:
        with Path(path).open('rb') as f: raw=f.read(MAX_MANIFEST_BYTES+1)
        if len(raw)>MAX_MANIFEST_BYTES:fail('VALIDATION_FAILED','Request file exceeds byte budget')
        return bounded_copy(decode(raw.decode('utf-8')))
    except (OSError, UnicodeError, RecursionError):
        fail('VALIDATION_FAILED','Unreadable, invalid UTF-8 or excessively nested request')


def _ok(result):
    if result['status']!='SUCCESS':fail(result['status'],result['detail'])
    return result['data']


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store',required=True,help='Local snapshot directory')
    p.add_argument('--archive',help='Bound local archive, required for init/build/prepare/read')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('init');sub.add_parser('audit')
    q=sub.add_parser('build');q.add_argument('request');q.add_argument('--tokenizer',required=True)
    q=sub.add_parser('inspect');q.add_argument('snapshot_id')
    q=sub.add_parser('receipt');q.add_argument('operation_id')
    q=sub.add_parser('list');q.add_argument('--limit',type=int,default=100);q.add_argument('--after')
    q=sub.add_parser('read');q.add_argument('snapshot_id');q.add_argument('--expected',required=True)
    q.add_argument('--tokenizer',required=True);q.add_argument('--split',choices=('train','validation'),required=True)
    q.add_argument('--purpose',default='training')
    q=sub.add_parser('prepare-build',help='Select exact refs into a request, without granting use or creating a snapshot')
    for name in ('snapshot-id','operation-id','reviewer','reason','tokenizer','tokenizer-id','tokenizer-version'):
        q.add_argument('--'+name,required=True)
    q.add_argument('--train',action='append',required=True,help='Explicit experience ID; repeat for more members')
    q.add_argument('--validation',action='append',default=[])
    q.add_argument('--transform',default='curated_text_v1',choices=('curated_text_v1','normalize_newlines_v1'))
    q.add_argument('--at',help='UTC timestamp; defaults to current time')
    args=p.parse_args(argv)
    try:
        archive=None
        if args.command in ('init','build','read','prepare-build'):
            if not args.archive:fail('VALIDATION_FAILED','An explicit archive is required')
            archive=ExperienceArchive(args.archive)
        if args.command=='prepare-build':
            members=[]
            for split,ids in (('train',args.train),('validation',args.validation)):
                for id in ids:
                    # Administrative selection is NOT permission to build/use.
                    ref=_ok(archive.inspect(id))['reference']
                    members.append({**ref,'split':split})
            try:
                with Path(args.tokenizer).open('rb') as f:raw=f.read(MAX_TOKENIZER_BYTES+1)
            except OSError:fail('INSUFFICIENT_EVIDENCE','Tokenizer identity artifact unavailable')
            if len(raw)>MAX_TOKENIZER_BYTES:fail('BUDGET_EXHAUSTED','Tokenizer exceeds local byte budget')
            request=normalize_request({'schema_version':1,'operation_id':args.operation_id,'snapshot_id':args.snapshot_id,
                'actor':{'id':args.reviewer,'kind':'HUMAN','version':'local-cli-v1'},
                'at':args.at or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'reason':args.reason,'purpose':'training','transform':args.transform,
                'tokenizer':{'id':args.tokenizer_id,'version':args.tokenizer_version,'sha256':sha256(raw).hexdigest()},
                'members':members})
            print(json.dumps(request,indent=2,ensure_ascii=True));return 0
        store=DatasetSnapshots.create(args.store,archive=archive) if args.command=='init' else DatasetSnapshots(args.store)
        if args.command in ('init','audit'):result=store.audit()
        elif args.command=='build':result=store.build(read_request(args.request),archive=archive,tokenizer_path=args.tokenizer)
        elif args.command=='inspect':result=store.inspect(args.snapshot_id)
        elif args.command=='receipt':result=store.operation_receipt(args.operation_id)
        elif args.command=='list':result=store.list_snapshots(limit=args.limit,after=args.after)
        else:result=store.read_for_use(args.snapshot_id,expected_manifest_hash=args.expected,
            purpose=args.purpose,split=args.split,archive=archive,tokenizer_path=args.tokenizer)
        print(json.dumps(result,indent=2,ensure_ascii=True))
        return 0 if result['status']=='SUCCESS' else 2
    except ContractError as exc:
        print(json.dumps({'status':exc.code,'data':None,'detail':str(exc)},ensure_ascii=True));return 2


if __name__=='__main__':sys.exit(main())
