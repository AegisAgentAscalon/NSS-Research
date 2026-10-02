"""Opt-in synthetic stage/context/archive integration, not neural attention proof."""
import argparse
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
from .context_contracts import make_request
from .context_plan import unwrap
from .context_service import ContextService
from .experience_store import ExperienceArchive
from .neural_contracts import encoded, fingerprint, pairs, read_document
from .neural_records import ProbeRuns
from .overlaycatalogcontroller001 import prepare_catalog, FIXTURE
from .runtime import ContractError, fail

ACTOR={'id':'context-fixture-reviewer','kind':'HUMAN','version':'scripted-not-authenticated-v1'}
AT='2026-09-11T00:00:00Z'


def reviewed_fixture(archive,id,text, *, sensitivity='ORDINARY'):
    """Self-authored fixture only; no private conversation or downloaded data."""
    src={'id':'fixture-source','kind':'REFERENCE','author':ACTOR,'recorded_at':AT,
        'media_type':'text/plain','sha256':sha256(text.encode()).hexdigest(),'content':text,
        'generator':None,'parent_source_ids':[],'rights_note':'Self-authored test fixture.'}
    unwrap(archive.capture({'schema_version':1,'operation_id':'capture:'+id,'experience_id':id,
        'actor':ACTOR,'at':AT,'family_id':'family:'+id,'sensitivity':sensitivity,
        'observation':{'kind':'EXTERNAL_RECORD','execution':None,'summary':'Context fixture','outcome':'UNKNOWN','check_refs':[]},
        'evidence':[src],'statement':{'text':text,'uncertainty':'LOW','support_ids':[src['id']]}}))
    for action,payload in [('REVIEW',{'decision':'APPROVED'}),('PERMISSION',{'purpose':'retrieval','decision':'ALLOWED','permission_ref':'fixture:read'})]:
        ref=unwrap(archive.inspect(id))['reference']
        unwrap(archive.change({'schema_version':1,'operation_id':action+':'+id,'experience_id':id,
            'expected_revision_hash':ref['sha256'],'actor':ACTOR,'at':AT,'reason':'Scripted local review, not human judgment',
            'action':action,'payload':payload}))
    return unwrap(archive.inspect(id))['reference'],src


def run(directory):
    root=Path(directory);ctl,ch,_,original=prepare_catalog(root)
    manager=ctl.generations;ledger=ctl.inputs['ledger'];task='neural-probe-replay'
    archive=ExperienceArchive.create(root/'context-archive');service=ContextService(ctl,archive=archive)
    speed,src=reviewed_fixture(archive,'speed-notes','Speed must retain its unit; source says 10 m/s.')
    garden,_=reviewed_fixture(archive,'garden-notes','Garden flowers are yellow.')
    def req(label,stage,mode='WORK'):
        return {'schema_version':1,'catalog_sha256':ch,'expected_current':manager.inspect()['current'],
            'task_id':task,'stage':{'id':stage,'mode':mode,'sealed':False,'objective':'Build exact bounded context',
            'required_facts':[],'requested_output':'Keep task constraints and sources'},
            'capabilities':[label],'pairs':pairs('test')[:4],'budget':{'max_document_bytes':1000000,'max_cost_units':1000}}
    r=req('interpret','interpret');record=read_document(FIXTURE/'task_record.json')
    record.update(task_id=task,stage=r['stage'])
    record['receipts']=[{'key':k,'kind':'mock_action','receipt':ledger.inspect(k)['receipt']} for k in ledger.action_keys(task)]
    ctl.apply({'schema_version':1,'operation_id':'context-start','caller_id':'local-runner','action':'START',
               'request':r,'ticket_id':'context-interpret','record':record})
    def view():
        v=ctl.inspect(task);return ctl.read(v['ticket'],caller_id='local-runner',expected_record_sha256=fingerprint(v['work']['record']))
    def act(action,**extra):
        v=ctl.inspect(task);return ctl.apply({'schema_version':1,'operation_id':action+':'+v['ticket']['ticket_id'],
            'caller_id':'local-runner','action':action,'source_ticket':v['ticket'],
            'expected_record_sha256':fingerprint(v['work']['record']),**extra})
    v=view();proposal=make_request(v,'local-runner');proposal['required_fact_ids']=['speed'];proposal['query_terms']=['speed']
    proposal['archive_binding']=unwrap(archive.binding())
    proposal['experiences']=[{'reference':ref,'required':False,'priority':0} for ref in (garden,speed)]
    before=ctl.inspect(task);archive_before=unwrap(archive.audit());p=unwrap(service.build(proposal))
    unwrap(service.consume(p,caller_id='local-runner',expected_packet_sha256=fingerprint(p)))
    expanded=unwrap(service.rehydrate(p,caller_id='local-runner',expected_packet_sha256=fingerprint(p),selector={
        'kind':'EXPERIENCE_SLICE','experience_id':'speed-notes','source_id':src['id'],
        'source_sha256':src['sha256'],'start_byte':0,'end_byte':len(src['content'].encode())}))
    too_small=deepcopy(proposal);too_small['budget']['max_context_bytes']=1
    overflow=service.build(too_small)
    read_only=before==ctl.inspect(task) and archive_before==unwrap(archive.audit())
    unwrap(archive.revoke_source({'schema_version':1,'operation_id':'withdraw-speed','actor':ACTOR,'at':AT,
        'reason':'Demonstrate retrieval withdrawal','permission_ref':'fixture:withdraw','source_sha256':src['sha256'],'purpose':'retrieval'}))
    revoked=service.consume(p,caller_id='local-runner',expected_packet_sha256=fingerprint(p))
    act('FINISH',results=[],receipts=[])
    next_stage=req('solve','solve');next_stage['stage']['required_facts']=[{'fact_id':'speed','fields':['value','unit']}]
    act('MOVE',request=next_stage,ticket_id='context-solve')
    stale=service.consume(p,caller_id='local-runner',expected_packet_sha256=fingerprint(p))
    a=unwrap(service.build(make_request(view(),'local-runner')))
    act('FINISH',results=[],receipts=[]);act('MOVE',request=req('control','evaluate','EVALUATION'),ticket_id='context-core')
    core=unwrap(service.build(make_request(view(),'local-runner')))
    act('FINISH',results=[],receipts=[]);act('CLOSE')
    summary={'status':'SUCCESS','scope':'DETERMINISTIC_BYTE_BOUNDED_CONTEXT_NOT_NATIVE_ATTENTION',
        'selected_experiences':[e['reference']['experience_id'] for e in p['payload']['experiences']],
        'irrelevant_experience_omitted':any(o['id']=='garden-notes' and o['reason']=='IRRELEVANT' for o in p['omissions']),
        'rehydrated_unit':p['payload']['facts'][0]['unit'],
        'exact_evidence_rehydrated':expanded['payload']['evidence_slices'][0]['text']==src['content'],
        'context_bytes':p['usage']['context_bytes'],'context_byte_limit':p['request']['budget']['max_context_bytes'],
        'mandatory_overflow':overflow['status'],'revoked_packet_rejected':revoked['status'],
        'stale_stage_rejected':stale['status'],'profile_sequence':['AB',a['request']['ticket']['profile'],core['request']['ticket']['profile']],
        'context_reads_preserved_owner_state':read_only,'mock_external_effect_count':ledger.effect_count(),
        'original_neural_report_unchanged':original==ProbeRuns(root/'probe/journal').inspect('probe-001'),
        'new_training_or_deployment_authority':False,'task_closed':ctl.inspect(task)['closed']}
    if not (summary['selected_experiences']==['speed-notes'] and summary['irrelevant_experience_omitted']
        and summary['rehydrated_unit']=='m/s' and summary['exact_evidence_rehydrated'] and read_only
        and overflow['status']=='BUDGET_EXHAUSTED' and revoked['status']=='INCOMPATIBLE_CONFIGURATION'
        and stale['status']=='INCOMPATIBLE_CONFIGURATION' and summary['profile_sequence']==['AB','A','CORE']
        and summary['mock_external_effect_count']==1 and summary['original_neural_report_unchanged'] and summary['task_closed']):
        fail('VALIDATION_FAILED','Context demonstration invariant failed')
    (root/'example-request.json').write_bytes(encoded(proposal));(root/'historical-packet.json').write_bytes(encoded(p))
    (root/'summary.json').write_bytes(encoded(summary));return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--directory');a=parser.parse_args()
    try:
        if a.directory:r=run(a.directory)
        else:
            with TemporaryDirectory(prefix='megamind-context-') as d:r=run(d)
        print(encoded(r).decode());return 0
    except ContractError as e:
        print(encoded({'status':e.code,'detail':str(e)}).decode(),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
