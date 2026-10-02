"""Run StageHandoff001 locally. No network, model download, or real outside action."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from .artifacts import Bundle
from .ledger import Ledger
from .publication import RecoveryStore, checkpoint_hash
from .recovery import execute
from .serialization import read_json
from .stage_handoff import initialize_task, handoff_stage, finish_stage

FIXTURE=Path(__file__).resolve().parents[1]/'fixtures/stagehandoff001'


def _successful(result):
    if result['status']!='SUCCESS':
        raise RuntimeError(f'StageHandoff001 failed: {result}')
    return result['state']


def run(directory):
    directory=Path(directory)
    bundle=Bundle(FIXTURE/'manifest.json')
    ledger=Ledger(directory/'actions');store=RecoveryStore(directory/'recovery')
    record=read_json(FIXTURE/'task_record.json')
    inputs=read_json(FIXTURE/'input_ref.json')
    state=_successful(initialize_task(bundle,store,ledger,record=record,input_artifact=inputs,authorized=True))
    profiles=[state['profile']]

    def move(stage_id,mode,destination,required):
        current=store.current(record['task_id'])
        request={'schema_version':1,'source_checkpoint_hash':checkpoint_hash(current),
            'next_stage':{'id':stage_id,'mode':mode,'sealed':False,
                'objective':'Demonstrate a source-aware portable handoff.',
                'required_facts':required,'requested_output':'Preserve information and verified receipts.'}}
        result=handoff_stage(bundle,store,ledger,task_id=record['task_id'],destination=destination,
            attempt_id='handoff:'+stage_id,request=request,authorized=True)
        state=_successful(result);profiles.append(state['profile']);return state

    state=move('interpret-specialist','WORK','AB',[])
    marker={'schema_version':1,'task_id':record['task_id'],'key':'demo:action',
        'payload':{'operation':'append_marker','value':'exactly one LOCAL MOCK effect'},
        'status':'PENDING','receipt':None}
    receipt=ledger.perform(marker)
    state=_successful(finish_stage(bundle,store,ledger,task_id=record['task_id'],
        expected_checkpoint_hash=checkpoint_hash(state),new_results=[],
        new_receipts=[{'key':marker['key'],'kind':'mock_action','receipt':receipt}],authorized=True))

    state=move('solver','WORK','A',[{'fact_id':'speed','fields':['value','unit']}])
    solver_state=deepcopy(state)
    clean=execute(bundle,'A',bundle.artifact(inputs,'inputs.schema.json'))
    state=_successful(finish_stage(bundle,store,ledger,task_id=record['task_id'],
        expected_checkpoint_hash=checkpoint_hash(state),new_results=[{
            'id':'integer-check','text':'Rebuilt integer outputs match clean A.',
            'check_ref':'fixture:stagehandoff001:clean-A','producer_ecid':state['ecid'],
            'source_ids':['source-1']}],new_receipts=[],authorized=True))
    state=move('core-control','CONTROL','core',[])
    bundle.verify()
    report={
        'status':'SUCCESS','profile_sequence':profiles,
        'recovered_A':solver_state['cache'],'clean_A':clean,
        'exact_match':solver_state['cache']==clean,
        'unit_before':record['facts'][0]['unit'],
        'unit_after':state['task_record']['facts'][0]['unit'],
        'committed_mock_effects':ledger.effect_count(),
        'receipt_count':len(state['task_record']['receipts']),
        'final_profile':state['profile'],'final_mode':state['task_record']['stage']['mode'],
        'final_task_record_revision':state['task_record']['revision'],
        'scope':'Deterministic software fixtures; no neural Core, learned router/evaluator, production qualification or Nexus authorization.'}
    if not report['exact_match'] or report['unit_after']!='m/s' or report['committed_mock_effects']!=1 or report['final_profile']!='core':
        raise RuntimeError('StageHandoff001 acceptance failed')
    return report


if __name__=='__main__':
    with TemporaryDirectory(prefix='megamind-stagehandoff001-') as directory:
        print(json.dumps(run(directory),indent=2))
