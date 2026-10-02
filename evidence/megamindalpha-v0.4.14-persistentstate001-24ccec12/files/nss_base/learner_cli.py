"""Explicit local learner operations. Operators are declarations, not authentication.

Opening never creates/repairs owners. init creates only the three new empty journals.
Historical inspection gives no current-use permission. No candidate is auto-deployed.
"""
import argparse
from pathlib import Path
import sys
import time
from .candidate_records import CandidateRuns, CandidateEvaluations
from .dataset_store import DatasetSnapshots
from .experience_store import ExperienceArchive
from .learner_coordinator import LearnerCoordinator
from .learner_store import LearningCycles
from .neural_contracts import encoded, fields, read_document
from .qualification_neural import NeuralEvidence
from .qualification_store import Qualifications
from .runtime import ContractError, fail

from .learner_contracts import owner_paths as paths


def open_learner(config,*,clock=None):
    p=paths(config)
    return LearnerCoordinator(LearningCycles(p['cycles']),archive=ExperienceArchive(p['archive']),
        snapshots=DatasetSnapshots(p['snapshots']),tokenizer_path=p['tokenizer'],
        source=NeuralEvidence(p['parent_journal'],p['parent_data']),qualifications=Qualifications(p['qualifications']),
        training=CandidateRuns(p['candidates']),evaluations=CandidateEvaluations(p['evaluations']),clock=clock)


def initialize(config,operators):
    p=paths(config)
    targets=[p[k] for k in ('cycles','candidates','evaluations')]
    if len(set(targets))!=3 or any(a!=b and (a.is_relative_to(b) or b.is_relative_to(a)) for a in targets for b in targets):
        fail('VALIDATION_FAILED','Separate non-nested owner directories required')
    for path in targets:
        if path.exists() and (not path.is_dir() or any(path.iterdir())):
            fail('CONSTRAINT_CONFLICT','Initialization requires empty new journals')
    LearningCycles.create(p['cycles'],operators);CandidateRuns.create(p['candidates']);CandidateEvaluations.create(p['evaluations'])
    return {'status':'SUCCESS','authority':'NONE','scope':'Created journals only, not approval'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',required=True)
    sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('init');c.add_argument('--operators',required=True)
    c=sub.add_parser('prepare');c.add_argument('--plan',required=True)
    for cmd in ('inspect','advance','approve','cancel','withdraw','check-proposal'):
        c=sub.add_parser(cmd);c.add_argument('--cycle',required=True)
        if cmd=='advance':c.add_argument('--caller',required=True)
        if cmd in ('approve','cancel','withdraw'):c.add_argument('--actor',required=True)
        if cmd=='approve':c.add_argument('--expires-at',type=int,required=True)
        if cmd in ('cancel','withdraw'):c.add_argument('--reason',required=True)
    a=p.parse_args(argv)
    try:
        config=read_document(a.config);now=int(time.time())
        if a.command=='init':r=initialize(config,read_document(a.operators))
        elif a.command in ('inspect','approve','cancel','withdraw'):
            j=LearningCycles(paths(config)['cycles'])
            if a.command=='inspect':r=j.inspect(a.cycle)
            elif a.command=='approve':r=j.approve(a.cycle,approver_id=a.actor,expires_at=a.expires_at,at=now)
            else:r=getattr(j,a.command)(a.cycle,actor_id=a.actor,reason=a.reason,at=now)
        else:
            co=open_learner(config)
            if a.command=='prepare':r=co.prepare(read_document(a.plan))
            elif a.command=='advance':r=co.advance(a.cycle,caller_id=a.caller)
            else:r=co.check_proposal(a.cycle)
        print(encoded(r).decode());return 2 if r.get('status')=='INSUFFICIENT_EVIDENCE' else 0
    except (ContractError,OSError) as e:
        print(encoded({'status':getattr(e,'code','INTERNAL_FAILURE'),'detail':str(e),'authority':'NONE'}).decode(),file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
