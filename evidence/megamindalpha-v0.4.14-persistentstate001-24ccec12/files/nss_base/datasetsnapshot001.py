"""Stage -> archive -> explicit human-attested permission -> dataset snapshot.
All records and HUMAN entries are synthetic/scripted software-test fixtures.
No trained learner, real reviewer, tokenizer execution, training or network.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from .dataset_store import DatasetSnapshots
from .experience_store import ExperienceArchive
from .experiencearchive001 import run as run_archive
from .ledger import Ledger
from .publication import RecoveryStore
from .serialization import read_json

FIXTURE=Path(__file__).resolve().parents[1]/'fixtures/datasetsnapshot001'
AT='2026-09-10T13:00:00Z'
HUMAN={'id':'synthetic-dataset-reviewer','kind':'HUMAN','version':'scripted-v1'}


def _ok(result):
    if result['status']!='SUCCESS':raise RuntimeError(f'DatasetSnapshot001: {result}')
    return result['data']


def run(directory):
    root=Path(directory);root.mkdir(parents=True,exist_ok=True)
    prior=run_archive(root/'source-demo')
    archive=ExperienceArchive(root/'source-demo'/'experience')
    runtime=RecoveryStore(root/'source-demo'/'runtime-demo'/'recovery')
    ledger=Ledger(root/'source-demo'/'runtime-demo'/'actions')
    checkpoint=runtime.current_hash('stage-001')
    token_path=root/'tokenizer_identity.json';token_path.write_bytes((FIXTURE/'tokenizer_identity.json').read_bytes())
    token={'id':'fixture-tokenizer','version':'1','sha256':sha256(token_path.read_bytes()).hexdigest()}
    def edit(id,action,payload,op):
        ref=_ok(archive.inspect(id))['reference']
        return _ok(archive.change({'schema_version':1,'experience_id':id,'operation_id':op,
            'expected_revision_hash':ref['sha256'],'actor':HUMAN,'at':AT,
            'reason':'Scripted synthetic operator decision, not automatic or authenticated review.',
            'action':action,'payload':payload}))
    def permit(id,op):
        return edit(id,'PERMISSION',{'purpose':'training','decision':'ALLOWED',
            'permission_ref':'synthetic:training-rights'},op)['reference']
    train_ref=permit('demo-experience','snapshot-demo:grant:train')
    _ok(archive.capture(read_json(FIXTURE/'capture_validation.json')))
    edit('validation-example','REVIEW',{'decision':'APPROVED'},'snapshot-demo:review:validation')
    val_ref=permit('validation-example','snapshot-demo:grant:validation')
    store=DatasetSnapshots.create(root/'snapshots',archive=archive)
    request={'schema_version':1,'operation_id':'snapshot:build:1','snapshot_id':'dataset-v1',
        'actor':HUMAN,'at':AT,'reason':'Explicit selection of synthetic reviewed records.',
        'purpose':'training','transform':'curated_text_v1','tokenizer':token,
        'members':[{**train_ref,'split':'train'},{**val_ref,'split':'validation'}]}
    receipt=_ok(store.build(request,archive=archive,tokenizer_path=token_path))
    original=_ok(store.inspect('dataset-v1'))
    def read(r):return store.read_for_use(r['snapshot_id'],expected_manifest_hash=r['sha256'],
        purpose='training',split='train',archive=archive,tokenizer_path=token_path)
    original_examples=_ok(read(receipt))['examples']
    # Only an explicit source-backed correction changes the approved interpretation.
    edit('demo-experience','CORRECT',{'statement':{'text':'The exact fixture source uses m/s. Preserve that unit without conversion.',
        'uncertainty':'LOW','support_ids':['source-1']},'evidence':[]},'snapshot-demo:correct')
    old_after_correction=read(receipt)
    edit('demo-experience','REVIEW',{'decision':'APPROVED'},'snapshot-demo:review:correction')
    new_ref=permit('demo-experience','snapshot-demo:grant:correction')
    request2=deepcopy(request);request2.update(operation_id='snapshot:build:2',snapshot_id='dataset-v2')
    request2['members'][0]={**new_ref,'split':'train'}
    rebuilt=_ok(store.build(request2,archive=archive,tokenizer_path=token_path))
    rebuilt_examples=_ok(read(rebuilt))['examples']
    source=next(s for s in _ok(archive.inspect('demo-experience'))['record']['sources'] if s['id']=='source-1')
    _ok(archive.revoke_source({'schema_version':1,'operation_id':'snapshot-demo:revoke-training',
        'actor':HUMAN,'at':AT,'reason':'Synthetic rights withdrawal after materialization.',
        'permission_ref':'synthetic:withdraw-training','source_sha256':source['sha256'],'purpose':'training'}))
    archive=ExperienceArchive(root/'source-demo'/'experience');store=DatasetSnapshots(root/'snapshots')
    blocked=read(rebuilt);retry=store.build(request2,archive=archive,tokenizer_path=token_path)
    report={'status':'SUCCESS','scope':'Local deterministic storage/selection checks with scripted HUMAN fixtures. No neural training.',
        'upstream_archive_status':prior['status'],'handoff_profiles':prior['handoff_profiles'],
        'original_snapshot':receipt,'rebuilt_snapshot':rebuilt,'original_examples':original_examples,
        'rebuilt_examples':rebuilt_examples,'read_old_after_correction':old_after_correction['status'],
        'read_rebuilt_after_revocation':blocked['status'],'retry_after_revocation_historical':retry['historical'],
        'old_manifest_unchanged':original==_ok(store.inspect('dataset-v1')),
        'runtime_checkpoint_unchanged':checkpoint==runtime.current_hash('stage-001'),
        'committed_mock_effects':ledger.effect_count(),'snapshot_audit':_ok(store.audit()),
        'archive_audit':_ok(archive.audit())}
    if (not report['old_manifest_unchanged'] or not report['runtime_checkpoint_unchanged']
            or report['committed_mock_effects']!=1 or old_after_correction['status']!='CONSTRAINT_CONFLICT'
            or blocked['status']!='TRAINING_RESTRICTED' or not retry['historical']):
        raise RuntimeError('DatasetSnapshot001 violated isolation, immutability or current-use gating')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',help='Preserve the synthetic demo in a new/empty directory; otherwise use temporary storage')
    args=p.parse_args()
    if args.directory:
        directory=Path(args.directory)
        if directory.exists() and any(directory.iterdir()):p.error('--directory must be empty/new')
        print(json.dumps(run(directory),indent=2))
    else:
        with TemporaryDirectory(prefix='megamind-datasetsnapshot001-') as directory:print(json.dumps(run(directory),indent=2))
