"""Bounded current-role execution controller. One cooperative local worker.

No network, action execution, model download, backend import by name or deployment.
OS locking excludes concurrent callbacks; the Generations reservation survives a
crash. A failed callback never commits partial state or silently replays a job.
"""
from copy import deepcopy
from time import perf_counter_ns
from .foundation_adapters import RoleAdapter
from .foundation_contracts import (AUXILIARY, PHASES, integer, choice, state_envelope,
                                   validate_state_envelope, exchange, validate_exchange)
from .foundation_lock import worker_lock
from .neural_contracts import fields, fingerprint, encoded
from .qualification_contracts import identifier, digest_value
from .context_contracts import packet
from .context_plan import unwrap
from .local_journal import fault
from .runtime import ContractError, fail


class CycleRunner:
    def __init__(self, generations, context_service, adapters):
        from .generation_store import Generations
        from .context_service import ContextService
        if type(generations) is not Generations or type(context_service) is not ContextService or not context_service.current_roles:
            fail('VALIDATION_FAILED', 'Use current-role installed generation/context owners')
        if context_service.controller.generations.journal.path != generations.journal.path:
            fail('INCOMPATIBLE_CONFIGURATION', 'Context and execution must share the same Generations owner')
        self.store = generations; self.context = context_service; self.adapters = dict(adapters)
        self._verify_adapters(generations.foundation_snapshot()['configuration'])

    def _verify_adapters(self, cfg):
        wanted = {r for r,c in cfg['components'].items() if c is not None}
        if set(self.adapters) != wanted:
            fail('INCOMPATIBLE_CONFIGURATION', 'Exactly the configured role adapters must be supplied')
        for r, adapter in self.adapters.items():
            if not isinstance(adapter, RoleAdapter): fail('VALIDATION_FAILED', 'Installed RoleAdapter required')
            if adapter.descriptor() != cfg['components'][r] or adapter.parameter_sha256() != cfg['components'][r]['weights_sha256']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Adapter descriptor or actual serving parameters differ')

    def run_tick(self, context_packet, *, operation_id, phase, experience_cutoff, observation=None,
                 internal_depth=1, fault_at=None):
        identifier(operation_id); choice(phase, PHASES, 'phase'); integer(experience_cutoff)
        integer(internal_depth, 1, 64)
        if fault_at not in (None, 'after_begin', 'after_primary_pre', 'after_auxiliary',
                             'before_f_complete_commit', 'after_complete_commit'):
            fail('VALIDATION_FAILED', 'Unknown installed test fault hook')
        p = packet(context_packet)
        if p['schema_version'] != 3: fail('INCOMPATIBLE_CONFIGURATION', 'Current-role context v3 required')
        req = p['request']; obs = {} if observation is None else deepcopy(observation)
        if type(obs) is not dict or len(encoded(obs)) > 16384:
            fail('BUDGET_EXHAUSTED', 'Bounded structured event input required')
        input_sha = fingerprint({'observation': obs, 'internal_depth': internal_depth})
        with worker_lock(self.store.journal.path.parent):
            snap = self.store.foundation_snapshot(); cfg = snap['configuration']
            # An exact retry is a receipt, not a second model call or a renewed
            # right to disclose a cached answer after source withdrawal.
            try:
                previous = self.store.foundation_operation(operation_id, caller_id=req['caller_id'], owner_scope=req['state_scope'])
            except ContractError as e:
                if e.code != 'INSUFFICIENT_EVIDENCE': raise
                previous = None
            if previous is not None:
                expected = (previous['context_sha256'], previous['input_sha256'], previous['phase'], previous['experience_cutoff'])
                if expected != (fingerprint(p), input_sha, phase, experience_cutoff):
                    fail('CONSTRAINT_CONFLICT', 'Operation ID already binds different input')
                if previous['status'] != 'COMMITTED':
                    fail('RECOVERY_REQUIRED', 'Interrupted IDs are history; resume with a new operation ID')
                return {'status': 'ALREADY_COMMITTED', 'historical': True, 'operation_id': operation_id,
                        'output': None, 'model_calls': 0, 'runtime_execution_permit': False}
            if snap['busy'] is not None:
                fail('RECOVERY_REQUIRED', 'Previous uncommitted tick needs explicit recovery')
            self._verify_adapters(cfg)
            aux = AUXILIARY[phase]
            if aux and cfg['components'][aux] is None:
                fail('NOT_SUPPORTED', 'Missing auxiliary; Primary-only must be explicitly selected')
            for r in ['PRIMARY'] + ([aux] if aux else []):
                if internal_depth != 1 and 'native_refinement' not in cfg['components'][r]['capabilities']:
                    fail('NOT_SUPPORTED', 'Native refinement is unavailable; no repeated-prompt substitute')
            if phase == 'LEARN' and 'candidate_learning' not in cfg['components']['SECONDARY']['capabilities']:
                fail('NOT_SUPPORTED', 'Inference endpoint does not supply a learning interface')
            consumed = unwrap(self.context.consume(p, caller_id=req['caller_id'], expected_packet_sha256=fingerprint(p)))
            view = self.context.controller.read_context(req, archive=self.context.archive)
            sources = sorted({s['artifact']['sha256'] for s in consumed['payload']['sources']} |
                             {e['reference']['sha256'] for e in consumed['payload']['experiences']})
            job = {'operation_id':operation_id,'task_id':req['task_id'],'caller_id':req['caller_id'],
                'scope':deepcopy(req['state_scope']),'phase':phase,'experience_cutoff':experience_cutoff,
                'expected_tick':view['ticks'],'record_sha256':fingerprint(view['record']),
                'context_sha256':fingerprint(p),'source_references':sources,'input_sha256':input_sha}
            self.store._foundation_event('F_BEGIN', job)
            fault(fault_at,'after_begin')
            states=deepcopy(view['states']); candidates=deepcopy(view['candidate_states'])
            messages=[]; receipts=[]

            def invoke(r, incoming, stage):
                lane='candidate' if phase=='LEARN' and r=='SECONDARY' else 'temporal'
                target=candidates if lane=='candidate' else states
                env=target.get(r); prior={}
                if env is not None:
                    validate_state_envelope(env,role_name=r,config=cfg,task=view,lane=lane)
                    prior=deepcopy(env['payload'])
                for message in incoming: validate_exchange(message,config=cfg,task=view)
                call={'phase':phase,'stage':stage,'operation':'candidate_step' if lane=='candidate' else 'infer',
                    'task_id':req['task_id'],'owner_scope':deepcopy(req['state_scope']),
                    'context':deepcopy(consumed['payload']),'messages':deepcopy(incoming),
                    'observation':deepcopy(obs),'allowed_source_references':deepcopy(sources),
                    'experience_cutoff':experience_cutoff,'internal_depth':internal_depth}
                adapter=self.adapters[r]; before=adapter.parameter_sha256()
                if before!=cfg['components'][r]['weights_sha256']:
                    fail('INCOMPATIBLE_CONFIGURATION','Serving parameters changed before callback')
                start=perf_counter_ns()
                result=adapter.step(deepcopy(call),prior)
                elapsed=(perf_counter_ns()-start)//1000
                after=adapter.parameter_sha256()
                if after!=before:
                    fail('INCOMPATIBLE_CONFIGURATION','Frozen serving parameters changed during callback')
                if elapsed > cfg['limits']['callback_budget_ms']*1000:
                    fail('BUDGET_EXHAUSTED','Callback overran cooperative budget; no partial state committed')
                fields(result,('payload','record_kind','source_references','state'));encoded(result)
                if type(result['payload']) is not dict or type(result['state']) is not dict:
                    fail('VALIDATION_FAILED','Structured output and state required')
                choice(result['record_kind'],('derived','hypothetical','proposed_action'),'generated evidence status')
                if type(result['source_references']) is not list or len(result['source_references']) > 256:
                    fail('VALIDATION_FAILED', 'Bounded exact-source reference list required')
                for ref in result['source_references']: digest_value(ref)
                if not set(result['source_references']) <= set(sources):
                    fail('INSUFFICIENT_EVIDENCE','Adapter invented evidence references')
                if len(encoded(result['payload'])) > cfg['limits']['max_message_bytes']:
                    fail('BUDGET_EXHAUSTED','Adapter output exceeds explicit limit')
                rev=(env['state_revision'] if env else 0)+1
                target[r]=state_envelope(result['state'],role_name=r,config=cfg,task=view,
                    event_id=operation_id,cutoff=experience_cutoff,revision=rev,lane=lane)
                receipts.append({'role':r,'call_index':len(receipts),'operation':call['operation'],
                    'input_sha256':fingerprint(call),'result_sha256':fingerprint(result),
                    'weights_before':before,'weights_after':after,'elapsed_us':elapsed})
                return result,rev

            pre,prev=invoke('PRIMARY',[],'begin')
            fault(fault_at,'after_primary_pre')
            if aux:
                to_aux=exchange(pre['payload'],config=cfg,task=view,sender='PRIMARY',receiver=aux,
                    event_id=operation_id,message_id=operation_id+':p-aux',cutoff=experience_cutoff,
                    state_revision=prev,record_kind=pre['record_kind'],source_references=pre['source_references'])
                messages.append(to_aux)
                result,rev=invoke(aux,[to_aux],'auxiliary')
                fault(fault_at,'after_auxiliary')
                messages.append(exchange(result['payload'],config=cfg,task=view,sender=aux,receiver='PRIMARY',
                    event_id=operation_id,message_id=operation_id+':aux-p',cutoff=experience_cutoff,
                    state_revision=rev,record_kind=result['record_kind'],source_references=result['source_references']))
            final,_=invoke('PRIMARY',messages[-1:] if aux else [],'finish')
            self._verify_adapters(cfg)
            # Source rights and task identity are revalidated after callbacks, not
            # treated as renewable authority from a once-correct context hash.
            unwrap(self.context.consume(p,caller_id=req['caller_id'],expected_packet_sha256=fingerprint(p)))
            self.store._foundation_event('F_COMPLETE',{'operation_id':operation_id,'states':states,
                'candidate_states':candidates,'messages':messages,'receipts':receipts,
                'output':{k:deepcopy(final[k]) for k in ('record_kind','payload','source_references')}},fault_at=fault_at)
            fault(fault_at,'after_complete_commit')
            return self.store.foundation_operation(operation_id,caller_id=req['caller_id'],owner_scope=req['state_scope'])
