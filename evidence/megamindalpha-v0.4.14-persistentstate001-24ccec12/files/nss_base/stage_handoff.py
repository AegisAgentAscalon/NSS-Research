"""StageHandoff001 public coordinator for one local deterministic execution worker.

Authorization is an explicit simulator flag, NOT Nexus permission. QAPs and edges
are admitted fixtures, NOT independently issued qualification evidence. There is
no action-execution, training, provider, network or learned-routing dependency.
"""
from copy import deepcopy
import re
import sqlite3

from .publication import checkpoint_hash, durable_recover
from .recovery import accept_cache, checkpoint
from .runtime import ContractError, fail
from .task_records import (attach_task_record, validate_task_record, validate_request,
    validate_receipts, prepare_handoff, sealed_revision)


def _identifier(value):
    if type(value) is not str or re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', value) is None:
        fail('VALIDATION_FAILED','Invalid task, attempt or profile identifier')


def _authorized(value):
    if type(value) is not bool:
        fail('VALIDATION_FAILED','Simulated authorization must be an explicit boolean')
    if not value:
        fail('AUTHORIZATION_DENIED','Fresh simulated authorization required')


def _failure(store, task_id, exc):
    code=exc.code if isinstance(exc,ContractError) else 'INTERNAL_FAILURE'
    try:
        current=store.current(task_id)
    except (ContractError, OSError, sqlite3.Error):
        current=None
    return dict(status=code,state=current,attempt=None,replayed=False,historical=False,detail=str(exc))


def handoff_stage(bundle, store, ledger, *, task_id, destination, attempt_id,
                  request, authorized=False, load_ok=True, crash_at=None):
    """Safely enter a stage; exact retries read history without reactivation.

    Returns a typed result. When historical=True, `state` is the immutable old
    result, not a statement about the currently active configuration. Use
    store.current(task_id) for the current state. Stage data and profile/cache
    publish atomically in the existing RecoveryStore transaction.
    """
    try:
        for value in (task_id,destination,attempt_id):_identifier(value)
        if type(load_ok) is not bool or type(authorized) is not bool:
            fail('VALIDATION_FAILED','Simulation flags must be booleans')
        validate_request(request);request=deepcopy(request)
        previous=store.inspect_attempt(attempt_id)
        if previous is not None:
            binding=previous.get('task_handoff')
            if (previous['task_id']!=task_id or previous['target_profile']!=destination
                    or binding is None or binding['request']!=request):
                fail('CONSTRAINT_CONFLICT','Attempt ID is bound to a different exact handoff')
            if previous['status'] in ('PUBLISHED','FAILED'):
                # Immutable history is a read, not new authorization or execution.
                result=durable_recover(bundle,store,ledger,task_id=task_id,
                    destination=destination,attempt_id=attempt_id,authorized=authorized,
                    load_ok=load_ok,task_handoff=binding)
                result['historical']=previous['status']=='PUBLISHED'
                return result
        _authorized(authorized)
        source=store.current(task_id)
        if checkpoint_hash(source)!=request['source_checkpoint_hash']:
            fail('INCOMPATIBLE_CONFIGURATION','Stale handoff request')
        accept_cache(bundle,source,source['profile'])
        bundle.edge(source['profile'],destination)  # No union or inferred reverse.
        binding=prepare_handoff(bundle,source,destination,request,ledger)
        if previous is not None and previous['task_handoff']!=binding:
            fail('CONSTRAINT_CONFLICT','Resumed handoff no longer has the same source-derived record')
        result=durable_recover(bundle,store,ledger,task_id=task_id,destination=destination,
            attempt_id=attempt_id,authorized=authorized,load_ok=load_ok,crash_at=crash_at,
            task_handoff=binding)
        result['historical']=False
        return result
    except (ContractError,OSError,sqlite3.Error) as exc:
        return _failure(store,task_id,exc)


def initialize_task(bundle,store,ledger,*,record,input_artifact,authorized=False,core_profile='core'):
    """Admit a supplied fixture record under a qualified Core-only profile.

    Upstream record content is schema/source-labelled data, not certified truth.
    Exact repeated initialization is idempotent through RecoveryStore.
    """
    task_id=record.get('task_id','invalid') if type(record) is dict else 'invalid'
    try:
        _identifier(task_id);_identifier(core_profile);_authorized(authorized)
        validate_task_record(record)
        if bundle.catalog.profile(core_profile).overlays:
            fail('INCOMPATIBLE_CONFIGURATION','Task initialization must use a Core-only profile')
        validate_receipts(record,ledger)
        source=attach_task_record(checkpoint(bundle,core_profile,task_id,input_artifact),record)
        source['draft']=''
        store.publish_initial(source)
        return dict(status='SUCCESS',state=source,attempt=None,replayed=False,historical=False,detail='')
    except (ContractError,OSError,sqlite3.Error) as exc:
        return _failure(store,task_id,exc)


def finish_stage(bundle,store,ledger,*,task_id,expected_checkpoint_hash,new_results,
                 new_receipts,authorized=False):
    """Seal a stage after upstream computation; append only labelled results/receipts.

    No computation or semantic judging occurs here. producer_ecid and check_ref
    bind declared provenance, not an approval. Only this wrapper checks simulated
    authority; RecoveryStore's revision method is a lower-level storage primitive.
    """
    try:
        _identifier(task_id);_authorized(authorized)
        if type(expected_checkpoint_hash) is not str or re.fullmatch('[0-9a-f]{64}',expected_checkpoint_hash) is None:
            fail('VALIDATION_FAILED','Expected checkpoint hash is invalid')
        current=store.current(task_id)
        if checkpoint_hash(current)!=expected_checkpoint_hash:
            fail('INCOMPATIBLE_CONFIGURATION','Stale stage-finish request')
        accept_cache(bundle,current,current['profile'])
        record=sealed_revision(current,new_results,new_receipts)
        if record['stage']['mode'] in ('CONTROL','EVALUATION') and bundle.catalog.profile(current['profile']).overlays:
            fail('INCOMPATIBLE_CONFIGURATION','Control/evaluation requires Core-only state')
        validate_receipts(record,ledger)
        state=store.publish_task_revision(task_id=task_id,
            expected_checkpoint_hash=expected_checkpoint_hash,task_record=record)
        return dict(status='SUCCESS',state=state,attempt=None,replayed=False,historical=False,detail='')
    except (ContractError,OSError,sqlite3.Error) as exc:
        return _failure(store,task_id,exc)
