"""NBR-01 protocol/preflight and a non-neural harness self-test.

No trained recurrent or Transformer candidate is supplied in this foundation release.
The estimator below diagnoses separated event/depth clocks; it is not a neural model,
a replacement for a strong Transformer-with-memory control, or a completed NBR study.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import struct
from nss_base.neural_contracts import fingerprint, fields
from nss_base.runtime import fail

PROTOCOL = {
    'schema_version':1,'study_id':'NBR-01','status':'NOT_RUN',
    'source_baseline':'0.5.0-tricore-foundation001',
    'question':'Separate persistent event state from additional internal processing with learning fixed.',
    'factors':{'temporal_state':[False,True],'internal_depth':[1,2,4,8]},
    'required_controls':['competent_transformer_with_equivalent_memory_and_tools',
                         'explicit_state_estimator','trained_recurrent_candidate'],
    'held_out_axes':['delay','processing_depth','distractors','perturbations','scope_reset','restart'],
    'measures':['task_quality','retention','wrong_convergence','state_bytes','temporary_peak_bytes',
                'total_compute','wall_time','foundation_training_cost','restore_correctness'],
    'phase':'PILOT_PROTOCOL_NOT_CONFIRMATORY',
    'confirmatory_thresholds':None,
    'confirmatory_gate':'Run development pilot, set useful quality/resource margins, lock before independent episodes.',
    'independent_seeds_target':5,
    'fairness':'Same observations/evidence/tools; report matched-resource and best-tuned comparisons separately.',
    'learning':'No per-arm parameter updates during state/depth evaluation. Count preparation separately.',
    'language_and_memory_product_baseline':'NOT_ESTABLISHED',
    'research_candidates':{
        'explicit_estimator_harness':'AVAILABLE_FOR_DIAGNOSTIC_SELF_TEST_ONLY',
        'trained_recurrent':'NOT_IMPLEMENTED',
        'competent_transformer':'CHECKPOINT_AND_BACKEND_NOT_SELECTED'},
    'architecture_acceptance':False,
}


def preflight():
    return {'status':'BLOCKED_FOR_FULL_NBR01','protocol_sha256':fingerprint(PROTOCOL),
        'protocol':PROTOCOL,'harness_available':True,
        'missing':['competent task-matched Transformer control','trained recurrent candidate',
                   'measured target-device budget','pilot-selected confirmatory criteria'],
        'forge_status':'NOT_CONNECTED','runtime_status':'NOT_CONNECTED',
        'model_downloads':0,'parameter_updates':0}


@dataclass
class ClockEstimator:
    """Engineered cue memory plus explicit query refinement; NOT learned recurrence.

    The compact state is an optional cue and an external event count. Refinement
    operates on a local z variable; changing depth never increments the event clock.
    Exact JSON wrapping adds metadata bytes beyond the 8-byte numerical state.
    """
    owner_scope: str
    keep_temporal_state: bool = True
    cue: int = -1
    event_count: int = 0

    def __post_init__(self):
        if (type(self.owner_scope) is not str or not 1 <= len(self.owner_scope) <= 96 or
            type(self.keep_temporal_state) is not bool or type(self.cue) is not int or
            not -1 <= self.cue <= 1000 or type(self.event_count) is not int or not 0 <= self.event_count <= 1000000):
            fail('VALIDATION_FAILED', 'Invalid estimator scope or state')

    def observe(self, cue=None):
        if cue is not None and (type(cue) is not int or not 0 <= cue <= 1000):
            fail('VALIDATION_FAILED','Bounded cue required')
        if self.event_count >= 1000000: fail('BUDGET_EXHAUSTED','Event budget exhausted')
        self.event_count += 1
        self.cue = (cue if cue is not None else self.cue) if self.keep_temporal_state else -1

    def refine(self, *, depth, required_steps):
        if type(depth) is not int or not 1 <= depth <= 64 or type(required_steps) is not int or not 1 <= required_steps <= 64:
            fail('VALIDATION_FAILED','Bounded explicit iteration budget required')
        z = self.cue
        for k in range(depth):
            if z >= 0 and k < required_steps: z += 1
        return {'answer':z,'internal_steps':depth,'external_events':self.event_count,
                'control':'HAND_ENGINEERED_NOT_NEURAL'}

    def checkpoint(self):
        raw=struct.pack('<ii',self.cue,self.event_count)
        body={'schema_version':1,'algorithm':'clock-estimator-v1','owner_scope':self.owner_scope,
              'keep_temporal_state':self.keep_temporal_state,'codec':'int32-le-pair',
              'raw_hex':raw.hex(),'raw_bytes':len(raw)}
        return {**body,'sha256':fingerprint(body)}

    @classmethod
    def restore(cls, value, *, owner_scope):
        fields(value,('schema_version','algorithm','owner_scope','keep_temporal_state','codec','raw_hex','raw_bytes','sha256'))
        body={k:v for k,v in value.items() if k!='sha256'}
        if (fingerprint(body)!=value['sha256'] or type(value['schema_version']) is not int or value['schema_version']!=1 or
            value['algorithm']!='clock-estimator-v1' or value['codec']!='int32-le-pair' or
            value['owner_scope']!=owner_scope or type(value['keep_temporal_state']) is not bool):
            fail('INCOMPATIBLE_CONFIGURATION','Estimator state scope/codec/integrity differs')
        try: raw=bytes.fromhex(value['raw_hex']);cue,count=struct.unpack('<ii',raw)
        except (ValueError,TypeError,struct.error): fail('VALIDATION_FAILED','Malformed numerical state')
        if type(value['raw_bytes']) is not int or value['raw_bytes']!=8 or not -1<=cue<=1000 or not 0<=count<=1000000:
            fail('VALIDATION_FAILED','Invalid numerical state bounds')
        if not value['keep_temporal_state'] and cue!=-1:
            fail('INCOMPATIBLE_CONFIGURATION','State-off arm cannot retain a cue')
        return cls(owner_scope,value['keep_temporal_state'],cue,count)


def harness_smoke():
    cases=[]
    for keep in (False,True):
        for depth in (1,2,4,8):
            for delay in (0,4,32):
                estimator=ClockEstimator('smoke',keep)
                estimator.observe(7)
                for _ in range(delay):estimator.observe()
                original=estimator.checkpoint();events=estimator.event_count
                out=estimator.refine(depth=depth,required_steps=4)
                if not (estimator.checkpoint()==original and estimator.event_count==events): fail('VALIDATION_FAILED', 'NBR01 harness invariant failed')
                resumed=ClockEstimator.restore(original,owner_scope='smoke')
                if not (resumed.refine(depth=depth,required_steps=4)==out): fail('VALIDATION_FAILED', 'NBR01 harness invariant failed')
                if not (out['answer']==(7+min(depth,4) if keep else -1)): fail('VALIDATION_FAILED', 'NBR01 harness invariant failed')
                if not (ClockEstimator('new-scope',keep).cue==-1): fail('VALIDATION_FAILED', 'NBR01 harness invariant failed')
                cases.append({'state':keep,'depth':depth,'delay':delay,'status':'HARNESS_CHECK_PASS'})
    return {'status':'HARNESS_SMOKE_PASS','study_status':'NOT_RUN',
            'scope':'ENGINEERED_CLOCK_CONTROL_ONLY_NOT_A_COGNITIVE_COMPARISON',
            'cases':cases,'case_count':len(cases),'raw_numeric_state_bytes':8,
            'checkpoint_metadata_bytes':'ADDITIONAL_NOT_INCLUDED_IN_RAW_8_BYTES',
            'learned_parameters':0,'training_steps':0,'neural_conclusions':None}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--preflight',action='store_true');g.add_argument('--harness-smoke',action='store_true')
    p.add_argument('--output',type=Path,help='New JSON path; refuses to overwrite')
    args=p.parse_args();result=preflight() if args.preflight else harness_smoke()
    raw=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f:f.write(raw)
    print(raw,end='')
    return 0


if __name__=='__main__':raise SystemExit(main())
