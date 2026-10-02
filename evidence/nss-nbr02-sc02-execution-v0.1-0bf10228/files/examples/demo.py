"""Read-only inference example. Run from an unpacked execution package."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from support import setup,load
from fixture_factory import episode
from runner import execute
setup();model,identity=load(8801)
fixture=episode(32,932101,'churn')
for arm in ('C','S','F','P','I'):
    out=execute(fixture,model,identity,arm,audit=True)
    print(json.dumps({'arm':arm,'available_answers':out['answers'],
          'reference_class_differences':out['changed_classes'],
          'numerical_violations':out['numeric_violations'],
          'single_run_core_ms':1000*out['core_seconds']}))
# Single demo timings are not a benchmark and do not replace retained results.
