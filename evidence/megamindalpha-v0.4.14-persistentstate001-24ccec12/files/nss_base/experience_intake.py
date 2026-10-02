"""Explicit one-way StageHandoff -> Experience Archive submission.

Reads a sealed checkpoint through public APIs. Never updates runtime state,
executes actions, or captures private conversations by default. No cross-store
transaction: a successful archive operation has a durable ID and can be retried.
"""
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from .experience_contracts import MAX_SOURCE_BYTES, bounded_copy, timestamp
from .publication import checkpoint_hash
from .recovery import accept_cache
from .runtime import ContractError, digest, fail
from .serialization import validate
from .task_records import validate_checkpoint, validate_receipts

SNAPSHOT_ID = '__task_snapshot__'


def _value(result):
    if result['status']!='SUCCESS': fail(result['status'],result['detail'])
    return result['data']


def capture_stage(archive, bundle, recovery_store, ledger, *, request):
    """Capture an exact sealed runtime stage, or read the result of an exact retry.

    Incoming outcome/check_refs/interpretation are caller assertions, not a learned
    evaluator result. Source authorship absent from TaskRecord is explicitly UNKNOWN.
    Actual origin timestamps, rights and semantic truth remain human-review work.
    """
    try:
        request=bounded_copy(request);validate(request,'experience_stage_capture.schema.json');timestamp(request['at'])
        previous=_value(archive.operation_receipt(request['operation_id']))
        if previous is not None:
            execution=previous['request'].get('observation',{}).get('execution')
            if (previous['kind']!='CAPTURE' or execution is None
                    or execution.get('capture_request_sha256')!=digest(request)
                    or previous['request']['experience_id']!=request['experience_id']):
                fail('CONSTRAINT_CONFLICT','Operation ID binds a different intake request')
            result=archive.inspect(request['experience_id'],revision_hash=previous['result_sha256'])
            if result['status']=='SUCCESS':result['replayed']=True
            return result
        state=recovery_store.current(request['task_id'])
        validate_checkpoint(state)
        if checkpoint_hash(state)!=request['expected_checkpoint_hash']:
            fail('CONSTRAINT_CONFLICT','Capture request no longer matches published checkpoint')
        if state['schema_version']!=2 or not state['task_record']['stage']['sealed']:
            fail('CONSTRAINT_CONFLICT','Experience capture requires an explicitly sealed TaskRecord stage')
        accept_cache(bundle,state,state['profile'])
        record=state['task_record'];validate_receipts(record,ledger)
        if any(s['id']==SNAPSHOT_ID for s in record['sources']):
            fail('VALIDATION_FAILED','Task source collides with reserved snapshot evidence ID')
        sources=[]
        for source in record['sources']:
            relative=Path(source['artifact']['path']);path=(bundle.root/relative).resolve()
            if relative.is_absolute() or not path.is_relative_to(bundle.root):
                fail('VALIDATION_FAILED','Task source escapes admitted fixture root')
            try:
                with path.open('rb') as handle: raw=handle.read(MAX_SOURCE_BYTES+1)
            except OSError: fail('INSUFFICIENT_EVIDENCE','Exact task source is unavailable')
            if len(raw)>MAX_SOURCE_BYTES:fail('VALIDATION_FAILED','Task evidence exceeds capture budget')
            if sha256(raw).hexdigest()!=source['artifact']['sha256']:
                fail('INCOMPATIBLE_CONFIGURATION','Task source differs from referenced bytes')
            try:content=raw.decode('utf-8')
            except UnicodeError:fail('VALIDATION_FAILED','This archive intake requires UTF-8 evidence')
            # Preserve source kind without inventing a personal author from a role label.
            kind={'user':'USER_REPORT','policy':'POLICY','retrieved':'REFERENCE','model':'MODEL_OUTPUT'}.get(source['kind'],'REFERENCE')
            sources.append({'id':source['id'],'kind':kind,
                'author':{'id':'unattributed:'+digest({'source_id':source['id']})[:40],'kind':'UNKNOWN','version':'unresolved'},
                'recorded_at':request['at'],'media_type':'application/json',
                'sha256':source['artifact']['sha256'],'content':content,'generator':None,'parent_source_ids':[],
                'rights_note':'TaskRecord source reference only; authorship and usage permission are unverified. Human review required.'})
        portable=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True)
        sources.append({'id':SNAPSHOT_ID,'kind':'TASK_SNAPSHOT',
            'author':{'id':'stagehandoff-capture','kind':'SYSTEM','version':'ExperienceArchive001-v1'},
            'recorded_at':request['at'],'media_type':'application/json','sha256':digest(record),
            'content':portable,'generator':None,'parent_source_ids':[s['id'] for s in record['sources']],
            'rights_note':'Local portable task snapshot. No automatic retrieval, training, or redistribution permission.'})
        command={k:request[k] for k in ('schema_version','operation_id','experience_id','actor','at','family_id','sensitivity','statement')}
        command['evidence']=sources
        command['observation']={'kind':'TASK_STAGE','execution':{
            'task_id':state['task_id'],'stage_id':record['stage']['id'],
            'checkpoint_sha256':checkpoint_hash(state),'ecid':state['ecid'],'profile':state['profile'],
            'core_generation':bundle.document['generation'],'core_sha256':bundle.document['core']['sha256'],
            'task_record_sha256':digest(record),'capture_request_sha256':digest(request)},
            'summary':request['summary'],'outcome':request['outcome'],'check_refs':request['check_refs']}
        return archive.capture(command)
    except ContractError as exc:
        return {'status':exc.code,'data':None,'detail':str(exc),'replayed':False,'historical':False}
    except (OSError,sqlite3.Error):
        return {'status':'INTERNAL_FAILURE','data':None,'detail':'Experience intake storage failure; runtime was not changed.',
                'replayed':False,'historical':False}
