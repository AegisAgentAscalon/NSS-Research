"""Local EvaluationRun001 operator CLI. No training, authority or dynamic plugins."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from .dataset_store import DatasetSnapshots
from .evaluation_contracts import MAX_FILE_BYTES, catalog, normalize_plan, relative_path
from .evaluation_inputs import implementation_identity, local_path
from .evaluation_store import EvaluationRuns
from .experience_store import ExperienceArchive
from .runtime import ContractError, digest, fail
from .serialization import decode, read_json


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store',default='./evaluations');p.add_argument('--root',default='.')
    p.add_argument('--snapshots');p.add_argument('--archive');p.add_argument('--tokenizer')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('identity');sub.add_parser('init');sub.add_parser('audit')
    make=sub.add_parser('prepare-plan')
    for key in ('run-id','candidate','suite','profile','operator','reason'):make.add_argument('--'+key,required=True)
    make.add_argument('--at');make.add_argument('--repeats',type=int,default=2);make.add_argument('--max-evaluations',type=int,default=160)
    make.add_argument('--development-snapshot');make.add_argument('--snapshot-sha256')
    for name in ('prepare','execute'):
        q=sub.add_parser(name);q.add_argument('plan')
    for name in ('inspect','verify-current'):
        q=sub.add_parser(name);q.add_argument('run_id')
        if name=='verify-current':q.add_argument('--expected-report-sha256',required=True)
    q=sub.add_parser('compare');q.add_argument('left');q.add_argument('right')
    q=sub.add_parser('list');q.add_argument('--limit',type=int,default=100);q.add_argument('--after')
    args=p.parse_args(argv)
    try:
        if args.command=='identity':result={'status':'SUCCESS','data':implementation_identity(),'authorizes_deployment':False}
        elif args.command=='prepare-plan':
            root=local_path(args.root)
            def ref(name):
                name=relative_path(name);path=(root/name).resolve()
                if not path.is_relative_to(root):fail('VALIDATION_FAILED','Artifact escapes root')
                with path.open('rb') as f:raw=f.read(MAX_FILE_BYTES+1)
                if len(raw)>MAX_FILE_BYTES:fail('BUDGET_EXHAUSTED','Artifact is oversized')
                return {'path':name,'sha256':sha256(raw).hexdigest()},decode(raw.decode('utf-8'))
            candidate,doc=ref(args.candidate);catalog(doc).profile(args.profile);suite,_=ref(args.suite)
            dataset=None
            if args.development_snapshot or args.snapshot_sha256:
                dataset={'snapshot_id':args.development_snapshot,'sha256':args.snapshot_sha256,'split':'validation'}
            result=normalize_plan({'schema_version':1,'run_id':args.run_id,
                'actor':{'id':args.operator,'kind':'HUMAN','version':'local-operator-attestation-v1'},
                'at':args.at or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'reason':args.reason,
                'candidate':{'manifest':candidate,'profile':args.profile,'expected_ecid':digest({'ecid_schema':'001A-1','manifest':doc,'active_profile':args.profile})},
                'suite':suite,'implementation_sha256':implementation_identity()['sha256'],
                'repeats':args.repeats,'max_evaluations':args.max_evaluations,'development_snapshot':dataset})
            # Merely writes a proposed plan. Does not create a store or claim permission.
        elif args.command=='init':
            store=EvaluationRuns.create(args.store);result=store.audit()
        else:
            store=EvaluationRuns(args.store)
            if args.command in ('prepare','execute','verify-current'):
                kw={'root':args.root}
                if args.snapshots or args.archive or args.tokenizer:
                    if not all((args.snapshots,args.archive,args.tokenizer)):
                        fail('VALIDATION_FAILED','Development reads need --snapshots, --archive and --tokenizer')
                    kw.update(snapshots=DatasetSnapshots(args.snapshots),archive=ExperienceArchive(args.archive),tokenizer_path=args.tokenizer)
                if args.command=='verify-current':result=store.verify_current(args.run_id,expected_report_sha256=args.expected_report_sha256,**kw)
                else:
                    with Path(args.plan).open('rb') as f:raw=f.read(4*1024*1024+1)
                    if len(raw)>4*1024*1024:fail('VALIDATION_FAILED','Plan is oversized')
                    plan=decode(raw.decode('utf-8'))
                    result=getattr(store,args.command)(plan,**kw)
            elif args.command=='inspect':result=store.inspect(args.run_id)
            elif args.command=='compare':result=store.compare(args.left,args.right)
            elif args.command=='list':result=store.list_runs(limit=args.limit,after=args.after)
            else:result=store.audit()
    except ContractError as exc:result={'status':exc.code,'data':None,'detail':str(exc),'authorizes_deployment':False}
    except (OSError,UnicodeError,RecursionError):result={'status':'VALIDATION_FAILED','data':None,'detail':'Unreadable local request/input','authorizes_deployment':False}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result.get('status','SUCCESS')!='SUCCESS':return 2
    if args.command=='execute' and result['data']['verdict']!='PASS':return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
