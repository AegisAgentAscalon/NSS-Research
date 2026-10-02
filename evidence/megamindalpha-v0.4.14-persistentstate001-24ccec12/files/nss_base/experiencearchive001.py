"""Connected synthetic demonstration. HUMAN review entries here are test fixtures,
not evidence of real human review or of autonomous curation competence.
"""
from pathlib import Path
import json
from tempfile import TemporaryDirectory

from .artifacts import Bundle
from .experience_intake import capture_stage
from .experience_store import ExperienceArchive
from .ledger import Ledger
from .publication import RecoveryStore, checkpoint_hash
from .stage_handoff import finish_stage
from .stagehandoff001 import run as run_handoffs, FIXTURE

AT='2026-09-10T12:00:00Z'
HUMAN={'id':'synthetic-reviewer','kind':'HUMAN','version':'scripted-test-v1'}


def _ok(result):
    if result['status']!='SUCCESS': raise RuntimeError(f'ExperienceArchive001 failed: {result}')
    return result['data'] if 'data' in result else result['state']


def run(directory):
    root=Path(directory);runtime_root=root/'runtime-demo';runtime_root.mkdir(parents=True,exist_ok=True)
    prior=run_handoffs(runtime_root)
    bundle=Bundle(FIXTURE/'manifest.json');runtime=RecoveryStore(runtime_root/'recovery');ledger=Ledger(runtime_root/'actions')
    state=runtime.current('stage-001')
    sealed=_ok(finish_stage(bundle,runtime,ledger,task_id='stage-001',expected_checkpoint_hash=checkpoint_hash(state),
        new_results=[],new_receipts=[],authorized=True))
    before=checkpoint_hash(sealed)
    archive=ExperienceArchive.create(root/'experience')
    request={'schema_version':1,'operation_id':'capture:demo','experience_id':'demo-experience',
        'actor':{'id':'proposed-learner','kind':'MODEL','version':'scripted-not-neural'},'at':AT,
        'task_id':'stage-001','expected_checkpoint_hash':before,'summary':'Synthetic sealed stage with source-linked unit information.',
        'outcome':'UNKNOWN','check_refs':['fixture:clean-A-equality'],
        'statement':{'text':'Tentative incorrect interpretation: the speed is 10 km/h.','uncertainty':'HIGH','support_ids':['source-1']},
        'family_id':'synthetic-speed-family','sensitivity':'ORDINARY'}
    captured=_ok(capture_stage(archive,bundle,runtime,ledger,request=request))
    source=next(s for s in captured['record']['sources'] if s['id']=='source-1')
    def mutate(op,action,payload):
        current=_ok(archive.inspect('demo-experience'))
        return _ok(archive.change({'schema_version':1,'operation_id':op,'experience_id':'demo-experience',
            'expected_revision_hash':current['reference']['sha256'],'actor':HUMAN,'at':AT,
            'reason':'Scripted synthetic human-review fixture, not a learned judgment.','action':action,'payload':payload}))
    mutate('dispute:demo','DISPUTE',{'conflict_id':'units','support_ids':['source-1'],'evidence':[]})
    mutate('correct:demo','CORRECT',{'statement':{'text':'The source says speed = 10 m/s; do not reinterpret it as km/h.',
        'uncertainty':'LOW','support_ids':['source-1']},'evidence':[]})
    mutate('resolve:demo','RESOLVE',{'conflict_id':'units','support_ids':['source-1'],'evidence':[]})
    mutate('review:demo','REVIEW',{'decision':'APPROVED'})
    allowed=mutate('permission:retrieval','PERMISSION',{'purpose':'retrieval','decision':'ALLOWED',
        'permission_ref':'synthetic-owner:retrieval-only'})
    ref=allowed['reference']['sha256']
    retrieval=archive.read_for_use('demo-experience',purpose='retrieval',expected_revision_hash=ref)
    training=archive.read_for_use('demo-experience',purpose='training',expected_revision_hash=ref)
    _ok(retrieval)
    archive=ExperienceArchive(root/'experience')
    after_reopen=_ok(archive.inspect('demo-experience'))
    _ok(archive.revoke_source({'schema_version':1,'operation_id':'revoke:demo','actor':HUMAN,'at':AT,
        'reason':'Synthetic source permission withdrawn.','permission_ref':'synthetic-owner:revocation',
        'source_sha256':source['sha256'],'purpose':'retrieval'}))
    blocked=archive.read_for_use('demo-experience',purpose='retrieval',expected_revision_hash=ref)
    raw_original=_ok(archive.inspect_source(source['sha256']))['content']
    report={'status':'SUCCESS','scope':'Deterministic local software and scripted review fixtures. No neural learning or authenticated reviewer.',
        'handoff_profiles':prior['profile_sequence'],'initial_review':captured['record']['review']['status'],
        'current_statement':after_reopen['record']['statement']['text'],
        'raw_source_preserved':'m/s' in raw_original,'initial_interpretation_preserved':
            _ok(archive.inspect('demo-experience',revision_hash=captured['reference']['sha256']))['record']['statement']['text']==request['statement']['text'],
        'retrieval_after_explicit_review_and_permission':retrieval['status'],
        'training_without_permission':training['status'],'retrieval_after_source_revocation':blocked['status'],
        'reopen_kept_exact_revision':after_reopen['reference']==allowed['reference'],
        'runtime_checkpoint_unchanged':runtime.current_hash('stage-001')==before,
        'committed_mock_effects':ledger.effect_count(),'archive_audit':_ok(archive.audit())}
    if not all(report[k] for k in ('raw_source_preserved','initial_interpretation_preserved','reopen_kept_exact_revision','runtime_checkpoint_unchanged')):
        raise RuntimeError('Archive demo lost required evidence or runtime isolation')
    if training['status']!='TRAINING_RESTRICTED' or blocked['status']!='TRAINING_RESTRICTED' or report['committed_mock_effects']!=1:
        raise RuntimeError('Archive demo did not enforce required boundaries')
    return report


if __name__=='__main__':
    with TemporaryDirectory(prefix='megamind-experiencearchive001-') as root:
        print(json.dumps(run(root),indent=2))
