"""Explicit opt-in synthetic catalogue demo; not learned routing or hardware paging."""
import argparse
from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from .catalog_controller import CatalogController, fixture_descriptor
from .catalog_contracts import require_state_identity
from .generation_evidence import from_evidence
from .generation_store import Generations
from .ledger import Ledger
from .neural_contracts import encoded, fingerprint, pairs, read_document
from .neural_records import ProbeRuns
from .overlaygenerationmanager001 import OPERATORS, prepare_generations
from .runtime import ContractError, fail

FIXTURE = Path(__file__).resolve().parents[1]/'fixtures/stagehandoff001'


def prepare_catalog(directory):
    root = Path(directory)
    if root.exists() and any(root.iterdir()): fail('CONSTRAINT_CONFLICT', 'Demo requires an empty directory')
    q, source = prepare_generations(root); ev = {'qualifications': q, 'source': source}
    ledger = Ledger(root/'probe/mock_actions'); original = ProbeRuns(root/'probe/journal').inspect('probe-001')
    manager = Generations.create(root/'generations', OPERATORS)
    g = from_evidence('catalog-family-1', 'fixture-builder', ['core','a','ab'], ['edge','core-return'], qualifications=q)
    h = manager.propose(g, **ev)['generation_sha256']; manager.qualify(h, reviewer_id='generation-reviewer', **ev)
    req = manager.make_request(h, release_id='adopt', caller_id='local-runner', mode='BOOTSTRAP', reason='Scripted catalogue demo')
    issued = manager.issue(req, issuer_id='release-owner', ttl_seconds=600, **ev)
    opts = dict(grant_sha256=fingerprint(issued['grant']), caller_id='local-runner', **ev)
    for f in (manager.prepare, manager.stage, manager.publish): f('adopt', **opts)
    artifacts = manager.inspect_release('adopt')['artifacts']
    declarations = {name: {'capabilities': [label], 'load_units': cost, 'step_units': 1, 'max_pairs': 64}
        for name,label,cost in [('CORE','control',0),('A','solve',2),('AB','interpret',4)]}
    d = fixture_descriptor(g, artifacts, catalog_id='catalog-demo', author_id='fixture-builder', declarations=declarations)
    ctl = CatalogController(manager, ledger=ledger, evidence_root=FIXTURE, **ev)
    ch = ctl.register(d, reviewer_id='generation-reviewer')['catalog_sha256']
    return ctl, ch, h, original


def run(directory):
    root = Path(directory); ctl, ch, h, original = prepare_catalog(root)
    manager = ctl.generations; ledger = ctl.inputs['ledger']; task = 'neural-probe-replay'
    def request(label, stage, mode='WORK'):
        return {'schema_version':1, 'catalog_sha256':ch, 'expected_current':manager.inspect()['current'],
            'task_id':task, 'stage':{'id':stage,'mode':mode,'sealed':False,'objective':'Source-aware local fixture',
                'required_facts':[], 'requested_output':'Preserve work without repeating effects'},
            'capabilities':[label], 'pairs':pairs('test')[:4], 'budget':{'max_document_bytes':1000000,'max_cost_units':1000}}
    start = request('interpret','interpret')
    record = read_document(FIXTURE/'task_record.json');record.update(task_id=task,stage=start['stage'])
    record['receipts'] = [{'key': k, 'kind':'mock_action','receipt':ledger.inspect(k)['receipt']} for k in ledger.action_keys(task)]
    command = {'schema_version':1,'operation_id':'start','caller_id':'local-runner','action':'START',
        'request':start,'ticket_id':'ticket-interpret','record':record}
    ctl.apply(command);sequence=['AB']
    def view():
        state=ctl.inspect(task)
        return ctl.read(state['ticket'],caller_id='local-runner',expected_record_sha256=fingerprint(state['work']['record']))
    def act(kind, **extras):
        state=ctl.inspect(task)
        c={'schema_version':1,'operation_id':kind.lower()+':'+state['ticket']['ticket_id'],
            'caller_id':'local-runner','action':kind,'source_ticket':state['ticket'],
            'expected_record_sha256':fingerprint(state['work']['record'])}
        c.update(extras);return ctl.apply(c)
    from .neural_backend import deterministic_cpu, load_checkpoint, encode_pairs
    def predict(v):
        with deterministic_cpu(101):
            import torch
            modules={k:load_checkpoint(a,fingerprint(a)) for k,a in v['artifacts'].items()}
            with torch.no_grad():return modules['core'](encode_pairs(v['pairs']),a=modules.get('A'),b=modules.get('B')).clone()
    first=view();ab=predict(first);ab_before=ab.clone()
    act('FINISH', results=[], receipts=[])
    move=request('solve','solve');move['stage']['required_facts']=[{'fact_id':'speed','fields':['value','unit']}]
    act('MOVE', request=move,ticket_id='ticket-solve');sequence.append('A');second=view()
    try: require_state_identity(first['task_state_identity'],second)
    except ContractError as e: stale=e.code
    else: stale='NOT_REJECTED'
    result=predict(second);fresh=deepcopy(second);clean=predict(fresh)
    act('FINISH',results=[{'id':'check-A','text':'Fresh A agrees with the selected-stage forward pass.',
        'check_ref':'demo:clean-A','producer_ecid':second['ticket']['profile_ecid'],'source_ids':['source-1']}],receipts=[])
    act('MOVE',request=request('control','evaluate','EVALUATION'),ticket_id='ticket-core');sequence.append('CORE')
    last=view();act('FINISH',results=[],receipts=[]);act('CLOSE')
    retry=ctl.apply(command)
    # A changed catalogue source blocks new admission, never changes history.
    manager.revoke(h,kind='QUALIFICATION',actor_id='generation-reviewer',reason='Demo withdrawal')
    invalid=request('control','fresh','CONTROL');invalid['task_id']='new-task'
    try:ctl.select(invalid,caller_id='local-runner')
    except ContractError as e:withdrawal=e.code
    else:withdrawal='NOT_BLOCKED'
    import torch
    summary={'status':'SUCCESS','scope':'DETERMINISTIC_CATALOGUE_WITH_REAL_NEURAL_ARTIFACTS',
        'profile_sequence':sequence,'stale_cache_identity':stale,'recovered_equals_fresh_A':torch.equal(result,clean),
        'source_AB_activations_unchanged':torch.equal(ab,ab_before),
        'unit_after_handoff':last['record']['facts'][0]['unit'],
        'final_core_only':set(last['artifacts'])=={'core'},'history_did_not_reopen':retry['historical'] and ctl.inspect(task)['closed'],
        'current_withdrawal':withdrawal,'open_stages':manager.inspect()['open_stages'],
        'mock_external_effect_count':ledger.effect_count(),
        'original_neural_report_unchanged':original==ProbeRuns(root/'probe/journal').inspect('probe-001'),
        'runtime_execution_permit':False,'learned_router':False,'actual_VRAM_paging':False}
    if not (summary['recovered_equals_fresh_A'] and summary['source_AB_activations_unchanged'] and
            stale=='INCOMPATIBLE_CONFIGURATION' and summary['unit_after_handoff']=='m/s' and
            summary['final_core_only'] and summary['history_did_not_reopen'] and withdrawal=='AUTHORIZATION_DENIED' and
            summary['mock_external_effect_count']==1 and summary['open_stages']==0 and summary['original_neural_report_unchanged']):
        fail('VALIDATION_FAILED','Catalogue demo invariant failed')
    (root/'summary.json').write_bytes(encoded(summary));return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory');a=p.parse_args()
    try:
        if a.directory:r=run(a.directory)
        else:
            with TemporaryDirectory(prefix='megamind-catalogue-') as d:r=run(d)
        print(encoded(r).decode());return 0
    except ContractError as e:
        print(encoded({'status':e.code,'detail':str(e)}).decode(),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
