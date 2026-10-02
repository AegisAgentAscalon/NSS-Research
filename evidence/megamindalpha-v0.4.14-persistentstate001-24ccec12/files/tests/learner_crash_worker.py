"""Real process death at opt-in learner boundaries; never used by runtime dispatch."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nss_base.learner_cli import open_learner
from nss_base.neural_contracts import read_document
co=open_learner(read_document(sys.argv[1]),clock=lambda:int(sys.argv[4]))
plan=read_document(sys.argv[2]);point=sys.argv[3]
if point=='after_plan_commit':co.prepare(plan,crash_at=point)
else:co.advance(plan['cycle_id'],caller_id=plan['producer_id'],crash_at=point)
raise SystemExit('Expected fault boundary was not reached')
