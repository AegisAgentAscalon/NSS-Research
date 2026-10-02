#!/usr/bin/env python3
"""Check retired tooling references and report code size without rewarding line count.

This is a static maintenance check, not a dead-code proof. Historical manifests and
reports remain immutable. Unique behavior coverage is exercised by the test suite.
"""
import ast
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
RETIRED=['generate_dataset_logic_docs.py','generate_evaluation_logic_docs.py','generate_neural_logic_docs.py',
         'generate_permission_logic_docs.py','generate_qualification_logic_docs.py','update_review_doc.py']


def main():
    problems=[]
    for name in RETIRED:
        if (ROOT/'tools'/name).exists():problems.append('Retired duplicate/tool reintroduced: '+name)
    # Tests that assert removal and immutable audit copies deliberately mention old names.
    for p in (ROOT/'tools').glob('*.py'):
        if p.name=='audit_maintenance.py':continue
        for name in RETIRED:
            if name in p.read_text():problems.append(str(p.relative_to(ROOT))+' still invokes/imports '+name)
    for p in (ROOT/'tests').glob('test_*.py'):
        t=ast.parse(p.read_text())
        if any(isinstance(n,ast.FunctionDef) and n.name=='test_inherited_python_code_and_tests_are_preserved_exactly' for n in ast.walk(t)):
            problems.append('Obsolete perpetual-source-freeze test was reintroduced')
    sizes={}
    for part in ['nss_base','tests','tools']:
        paths=list((ROOT/part).glob('*.py'))
        sizes[part]={'python_files':len(paths),'physical_lines':sum(len(p.read_text().splitlines()) for p in paths),
                     'nonblank_lines':sum(sum(bool(l.strip()) for l in p.read_text().splitlines()) for p in paths)}
    print(json.dumps({'status':'FAIL' if problems else 'PASS','issues':problems,'size':sizes,
        'interpretation':'Test volume is not bloat by itself. Distinct regressions remain; remove stale assertions and duplicate mechanics.'},indent=2))
    return int(bool(problems))
if __name__=='__main__':raise SystemExit(main())
