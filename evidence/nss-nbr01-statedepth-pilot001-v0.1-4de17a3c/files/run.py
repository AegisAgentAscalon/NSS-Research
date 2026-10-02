#!/usr/bin/env python3
"""Explicit local study actions. No dependency installation, downloads or NSS writes."""
import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent


def manifest():
    path=ROOT/'MANIFEST.sha256'
    if not path.exists():raise RuntimeError('No release manifest')
    count=0
    for line in path.read_text().splitlines():
        sha,relative=line.split('  ',1);p=(ROOT/relative).resolve()
        if not p.is_relative_to(ROOT):raise RuntimeError('Unsafe manifest path')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise RuntimeError(f'Changed file: {relative}')
        count+=1
    print(f'PASS: {count} manifest-covered files match.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('manifest','tests','verify','reproduce'))
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();manifest()
    if args.action=='manifest':return 0
    missing=[n for n in ('torch','numpy','safetensors','psutil') if importlib.util.find_spec(n) is None]
    if missing:
        print('NOT_SUPPORTED: missing optional research dependencies: '+', '.join(missing))
        print('No automatic installation was attempted. See requirements-research.txt and README.md.')
        return 2
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    if args.action=='tests':
        return subprocess.call([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,env=env)
    output=(args.output or ROOT.parent/'NSS_Run_Output'/('NBR01_'+args.action+'_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))).resolve()
    if output.is_relative_to(ROOT):raise RuntimeError('Outputs must be outside the checksum-closed study directory')
    output.mkdir(parents=True,exist_ok=False)
    if args.action=='verify':
        cmd=[sys.executable,'-m','nbr01_pilot.verification','--exhaustive','--output',str(output/'verification.json')]
        with (output/'verification.log').open('w') as log:
            code=subprocess.call(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        print('Verification exit code:',code,'; output:',output)
        return code
    for seed in range(201,206):
        for kind in ('gru','gated','hard_gated','transformer'):
            print(f'Reproduce {kind}, seed{seed},600 CPU steps.',flush=True)
            cmd=[sys.executable,'-m','nbr01_pilot.experiment','--kind',kind,'--seed',str(seed),'--steps','600','--output',str(output)]
            with (output/f'{kind}_seed{seed}.log').open('w') as log:
                code=subprocess.call(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            if code:
                print('Stopped on failure; partial evidence retained at',output);return code
    print('Completed20 training runs. Results:',output)
    print('This reproduction remains a pilot, not a new confirmatory comparison or production update.')
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (RuntimeError,FileExistsError) as error:
        print(str(error),file=sys.stderr);raise SystemExit(2)
