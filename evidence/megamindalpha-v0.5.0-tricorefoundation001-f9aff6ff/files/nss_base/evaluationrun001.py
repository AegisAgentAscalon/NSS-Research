"""Connected synthetic demonstration; no model quality or deployment authority."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from .artifacts import Bundle
from .dataset_store import DatasetSnapshots
from .datasetsnapshot001 import run as run_snapshot
from .evaluation_inputs import implementation_identity
from .evaluation_store import EvaluationRuns
from .experience_store import ExperienceArchive
from .ledger import Ledger
from .publication import RecoveryStore
from .serialization import read_json

FIXTURE=Path(__file__).resolve().parents[1]/'fixtures/evaluationrun001'
AT='2026-09-10T14:00:00Z'
HUMAN={'id':'scripted-evaluation-operator','kind':'HUMAN','version':'fixture-v1'}


def _ok(result):
    if result['status']!='SUCCESS':raise RuntimeError('EvaluationRun001: '+str(result))
    return result['data']


def plan_for(root,run_id,*,profile='A',snapshot=None,budget=160):
    """Convenience for synthetic demo plans, not an automatic evaluation policy."""
    root=Path(root);b=Bundle(root/'candidate/manifest.json')
    return {'schema_version':1,'run_id':run_id,'actor':deepcopy(HUMAN),'at':AT,
        'reason':'Scripted synthetic development comparison, not model qualification.',
        'candidate':{'manifest':{'path':'candidate/manifest.json','sha256':sha256((root/'candidate/manifest.json').read_bytes()).hexdigest()},
                     'profile':profile,'expected_ecid':b.ecid(profile)},
        'suite':{'path':'suite.json','sha256':sha256((root/'suite.json').read_bytes()).hexdigest()},
        'implementation_sha256':implementation_identity()['sha256'],'repeats':2,
        'max_evaluations':budget,'development_snapshot':snapshot}


def run(directory):
    root=Path(directory);root.mkdir(parents=True,exist_ok=True)
    upstream=run_snapshot(root/'upstream')
    archive=ExperienceArchive(root/'upstream/source-demo/experience')
    snapshots=DatasetSnapshots(root/'upstream/snapshots')
    runtime=RecoveryStore(root/'upstream/source-demo/runtime-demo/recovery')
    ledger=Ledger(root/'upstream/source-demo/runtime-demo/actions')
    before=runtime.current_hash('stage-001'); refs=[]
    for kind in ('train','validation'):
        id='evaluation-'+kind;_ok(archive.capture(read_json(FIXTURE/f'experience_{kind}.json')))
        for action,payload in [('REVIEW',{'decision':'APPROVED'}),
            ('PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fixture:self-authored-development-data'})]:
            ref=_ok(archive.inspect(id))['reference']
            _ok(archive.change({'schema_version':1,'operation_id':id+':'+action,'experience_id':id,
                'expected_revision_hash':ref['sha256'],'actor':HUMAN,'at':AT,'reason':'Scripted human-attested development fixture.',
                'action':action,'payload':payload}))
        refs.append({**_ok(archive.inspect(id))['reference'],'split':kind})
    token_path=root/'upstream/tokenizer_identity.json'
    snap=_ok(snapshots.build({'schema_version':1,'operation_id':'evaluation:build-devdata','snapshot_id':'evaluation-devdata',
        'actor':HUMAN,'at':AT,'reason':'Fresh independent development records; old revocations remain in force.',
        'purpose':'training','transform':'curated_text_v1',
        'tokenizer':{'id':'fixture-tokenizer','version':'1','sha256':sha256(token_path.read_bytes()).hexdigest()},'members':refs},
        archive=archive,tokenizer_path=token_path))
    inputs=root/'inputs';shutil.copytree(FIXTURE,inputs)
    store=EvaluationRuns.create(root/'evaluations')
    kw={'root':inputs,'snapshots':snapshots,'archive':archive,'tokenizer_path':token_path}
    data_ref={k:snap[k] for k in ('snapshot_id','sha256')};data_ref['split']='validation'
    a=plan_for(inputs,'run-A',snapshot=data_ref);ab=plan_for(inputs,'run-AB',profile='AB',snapshot=data_ref)
    low=plan_for(inputs,'run-limited',snapshot=data_ref,budget=1)
    results=[_ok(store.execute(p,**kw)) for p in (a,ab,low)]
    _ok(store.verify_current('run-A',expected_report_sha256=results[0]['report_sha256'],**kw));historical=_ok(store.inspect('run-A'))
    comparison=_ok(store.compare('run-A','run-AB'))
    source=_ok(archive.inspect('evaluation-validation'))['record']['sources'][0]['sha256']
    _ok(archive.revoke_source({'schema_version':1,'operation_id':'evaluation:withdraw-development-data',
        'actor':HUMAN,'at':AT,'reason':'Synthetic withdrawal after evaluation.',
        'permission_ref':'fixture:withdraw-development-use','source_sha256':source,'purpose':'training'}))
    store=EvaluationRuns(root/'evaluations')
    blocked=store.verify_current('run-A',expected_report_sha256=results[0]['report_sha256'],**kw);retry=store.execute(a,**kw)
    new=deepcopy(a);new['run_id']='run-after-withdrawal';new_result=store.execute(new,**kw)
    report={'status':'SUCCESS','scope':'Local synthetic checker/storage results only. No neural training, judging, qualification or deployment.',
        'upstream_status':upstream['status'],'results':results,'comparison':comparison,
        'repeat_reproducible':historical['report']['reproducible'],
        'historical_report_unchanged':historical==_ok(store.inspect('run-A')),
        'verify_after_revocation':blocked['status'],'new_run_after_revocation':new_result['status'],
        'exact_retry_is_historical':retry['historical'],'runtime_checkpoint_unchanged':runtime.current_hash('stage-001')==before,
        'committed_mock_effects':ledger.effect_count(),'audit':_ok(store.audit()),'authorizes_deployment':False}
    if ([x['verdict'] for x in results]!=['PASS','FAIL','INCONCLUSIVE'] or report['committed_mock_effects']!=1
            or not report['repeat_reproducible'] or not report['historical_report_unchanged']
            or not report['runtime_checkpoint_unchanged'] or not retry['historical']
            or blocked['status']!='TRAINING_RESTRICTED' or new_result['status']!='TRAINING_RESTRICTED'):
        raise RuntimeError('EvaluationRun001 failed a required acceptance condition: '+str(report))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory');args=p.parse_args()
    if args.directory:
        root=Path(args.directory)
        if root.exists() and any(root.iterdir()):p.error('--directory must be empty/new')
        print(json.dumps(run(root),indent=2))
    else:
        with TemporaryDirectory(prefix='megamind-evaluationrun001-') as root:print(json.dumps(run(root),indent=2))
