"""Real neural cache checks under the existing Catalog and mock Ledger contracts.

Owns only ephemeral EXPERIMENT states. Does not publish neural tensors through the
integer RecoveryStore or claim durable native runtime/cache integration.
"""
from copy import deepcopy
import torch

from .neural_backend import assert_frozen, checkpoint, encode_pairs, load_checkpoint
from .neural_contracts import fingerprint, validate_pairs
from .runtime import Catalog, ContractError, Overlay, Profile, Transition, fail


class FrozenSlotSession:
    """Shared ephemeral prediction/state/recovery mechanics, not a release authority."""
    def predict(self,profile,inputs):
        p=self.catalog.profile(profile)
        for k in self.modules:assert_frozen(self.modules[k],self.hashes[k])
        with torch.no_grad():
            return self.modules['core'](encode_pairs(inputs),
                a=self.modules[self.first] if self.first in p.overlays else None,
                b=self.modules['B'] if 'B' in p.overlays else None)

    def state(self,profile,inputs,task_id):
        values=validate_pairs(inputs)
        if type(task_id) is not str or not task_id:fail('VALIDATION_FAILED','Missing task ID')
        h=fingerprint(values)
        if task_id in self.input_bindings and self.input_bindings[task_id]!=h:
            fail('CONSTRAINT_CONFLICT','Task replay input identity was substituted')
        self.input_bindings[task_id]=h
        return {'task_id':task_id,'profile':profile,'ecid':self.catalog.ecid(profile),
                'input_sha256':fingerprint(values),'inputs':values,
                'cache':self.predict(profile,values),'draft':'unpublished neural probe draft'}

    def accept(self,state,profile,task_id):
        if (type(state) is not dict or set(state)!= {'task_id','profile','ecid','input_sha256','inputs','cache','draft'}):
            fail('VALIDATION_FAILED','Malformed neural state')
        if state['task_id']!=task_id or state['profile']!=profile or state['ecid']!=self.catalog.ecid(profile):
            fail('INCOMPATIBLE_CONFIGURATION','Stale or cross-task neural state')
        inputs=validate_pairs(state['inputs'])
        if fingerprint(inputs)!=state['input_sha256'] or self.input_bindings.get(task_id)!=state['input_sha256']:fail('VALIDATION_FAILED','Replay inputs changed')
        expected=self.predict(profile,inputs);cache=state['cache']
        if (type(cache) is not torch.Tensor or cache.shape!=expected.shape or cache.dtype!=expected.dtype
                or cache.device.type!='cpu' or not torch.equal(cache,expected)):
            fail('VALIDATION_FAILED','Corrupted neural cache')
        return cache.clone()

    def recover(self,state,destination,task_id,ledger,*,authorized=False,load_ok=True):
        """Failed recovery returns source unchanged; no action executor call exists."""
        try:
            self.accept(state,state.get('profile') if type(state) is dict else None,task_id)
            self.catalog.profile(destination)
            if not authorized:fail('AUTHORIZATION_DENIED','Explicit SIMULATED grant required')
            edge=next((e for e in self.catalog.transitions if (e.source,e.target)==(state['profile'],destination)),None)
            if edge is None:fail('INCOMPATIBLE_CONFIGURATION','Unapproved directed transition')
            ledger.ensure_replay_safe(task_id)
            if not load_ok:fail('INTERNAL_FAILURE','Simulated loading failure')
            target=self.state(destination,state['inputs'],task_id);target['draft']=''
            return {'status':'SUCCESS','state':target,'replayed':True}
        except ContractError as exc:
            return {'status':exc.code,'state':state,'replayed':False}


class NeuralSession(FrozenSlotSession):
    def __init__(self,artifacts,identity):
        if set(artifacts)!= {'core','A','B','joint','A2'}:fail('VALIDATION_FAILED','Wrong artifact family')
        self.hashes={k:fingerprint(v) for k,v in artifacts.items()}
        self.modules={k:load_checkpoint(v,self.hashes[k]) for k,v in artifacts.items()}
        if type(self.modules['core']).__name__!='Core' or any(type(self.modules[k]).__name__!='Overlay' or self.modules[k].rank!=(8 if k=='joint' else 4) for k in ('A','B','joint','A2')):
            fail('VALIDATION_FAILED','Checkpoint roles differ from the declared attachment scheme')
        self.first='A'
        self.input_bindings={}  # task input identity, not a production active pointer
        self.catalog=Catalog(self.hashes['core'],'neural-probe-G1','one_hot_16_pair_v1',
            'symbol-state-v1','two-linear-slots-v1',identity,
            (Overlay('A',self.hashes['A']),Overlay('B',self.hashes['B'])),
            tuple(Profile(n,tuple(v),'SIMULATED_APPROVAL_NOT_AUTHORITY') for n,v in
                [('CORE',[]),('A',['A']),('B',['B']),('AB',['A','B'])]),
            (Transition('AB','A','replay','SIMULATED_APPROVAL'),
             Transition('A','CORE','replay','SIMULATED_APPROVAL')))



class CandidateSession(FrozenSlotSession):
    """Exact new A2/B artifacts and names; never aliases candidate A2 to old A."""
    def __init__(self, artifacts, identity):
        if type(artifacts) is not dict or set(artifacts) != {'core','A','B','A2'}:
            fail('VALIDATION_FAILED', 'Expected the installed candidate artifact family')
        self.hashes={k:fingerprint(v) for k,v in artifacts.items()}
        self.modules={k:load_checkpoint(v,self.hashes[k]) for k,v in artifacts.items()}
        if type(self.modules['core']).__name__!='Core' or any(type(self.modules[k]).__name__!='Overlay'
                or self.modules[k].rank!=4 for k in ('A','B','A2')):
            fail('VALIDATION_FAILED', 'Candidate roles differ from the fixed slot contract')
        self.first='A2'; self.input_bindings={}
        self.catalog=Catalog(self.hashes['core'],'neural-probe-G1','one_hot_16_pair_v1',
            'symbol-state-v1','two-linear-slots-v1',identity,
            (Overlay('A2',self.hashes['A2']),Overlay('B',self.hashes['B'])),
            tuple(Profile(n,tuple(v),'NUMERICAL_FIXTURE_NOT_AUTHORITY') for n,v in
                [('CORE',[]),('A2',['A2']),('A2B',['A2','B'])]),
            (Transition('A2B','A2','replay','NUMERICAL_FIXTURE'),
             Transition('A2','CORE','replay','NUMERICAL_FIXTURE')))

def recovery_check(artifacts,inputs,identity,ledger,task_id,atol,rtol):
    session=NeuralSession(artifacts,identity);state=session.state('AB',inputs,task_id)
    original=state['cache'].clone()
    try:session.accept(state,'A',task_id)
    except ContractError as exc:stale_rejected=exc.code=='INCOMPATIBLE_CONFIGURATION'
    else:stale_rejected=False
    recovered=session.recover(state,'A',task_id,ledger,authorized=True)
    if recovered['status']!='SUCCESS':fail(recovered['status'],'Neural replay blocked')
    target=recovered['state'];clean=session.predict('A',inputs)
    # Independently reconstructed checkpoint instance, not the same cached output.
    fresh=NeuralSession(artifacts,identity);clean_fresh=fresh.predict('A',inputs)
    denied=session.recover(state,'A',task_id,ledger,authorized=False)
    reverse=session.recover(target,'AB',task_id,ledger,authorized=True)
    core=session.recover(target,'CORE',task_id,ledger,authorized=True)
    report={'stale_cache_rejected':stale_rejected,'source_cache_unchanged':torch.equal(state['cache'],original),
        'recovered_equals_clean_exact':torch.equal(target['cache'],clean_fresh),
        'recovered_within_tolerance':torch.allclose(target['cache'],clean_fresh,atol=atol,rtol=rtol),
        'max_absolute_error':float((target['cache']-clean_fresh).abs().max()),
        'draft_cleared':target['draft']=='','denied_status':denied['status'],
        'reverse_status':reverse['status'],'core_only_return':core['status'],
        'committed_mock_effects':ledger.effect_count(),
        'ecids':{n:session.catalog.ecid(n) for n in ('CORE','A','B','AB')},
        'state_kind':'real fp32 neural activations, NOT transformer KV',
        'approval_kind':'explicit deterministic simulator fixtures, NOT independent qualification'}
    if not all([stale_rejected,report['source_cache_unchanged'],report['recovered_within_tolerance'],
                report['draft_cleared'],core['status']=='SUCCESS',denied['status']=='AUTHORIZATION_DENIED',
                reverse['status']=='INCOMPATIBLE_CONFIGURATION']):
        fail('VALIDATION_FAILED','Neural recovery invariant failed')
    return report
