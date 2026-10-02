"""Verify recovered bytes; optionally run tests and replay the NEW limited smoke.

Never trains, installs packages, launches agents, deploys, or qualifies Study010.
"""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def digest(p:Path)->str:
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def local(rel:str)->Path:
    pos=PurePosixPath(rel)
    if pos.is_absolute() or '..' in pos.parts or '\\' in rel:raise ValueError('Unsafe path: '+rel)
    p=ROOT.joinpath(*pos.parts)
    if p.is_symlink() or ROOT.resolve() not in p.resolve().parents:raise ValueError('Unsafe target: '+rel)
    return p

def verify():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())['files']
    for rel,h in manifest.items():
        p=local(rel)
        if not p.is_file() or digest(p)!=h:raise RuntimeError('Missing/changed file: '+rel)
    subset=json.loads((ROOT/'provenance/PARENT_SUBSET.json').read_text())['selected_files']
    original=json.loads((ROOT/'reference/parent009/MANIFEST.json').read_text())['files']
    for rel,info in subset.items():
        p=local('reference/parent009/'+rel)
        if digest(p)!=info['sha256']:raise RuntimeError('Parent changed: '+rel)
        if rel!='MANIFEST.json' and info['sha256']!=original.get(rel):raise RuntimeError('Parent source mismatch: '+rel)
    return {'status':'PASS','manifest_files':len(manifest),'exact_parent_files':len(subset),
            'scope':'RECOVERY_BASE_ONLY_NOT_RECONSTRUCTED_010'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parent-tests',action='store_true');p.add_argument('--recovery-tests',action='store_true')
    p.add_argument('--replay-smoke',action='store_true');a=p.parse_args()
    print(json.dumps(verify(),indent=2),flush=True)
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    if a.parent_tests:
        subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=ROOT/'reference/parent009',env=env,check=True)
    if a.recovery_tests:
        subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=ROOT,env=env,check=True)
    if a.replay_smoke:
        import numpy as np
        with tempfile.TemporaryDirectory(prefix='nss_recovery_smoke_') as tmp:
            out=Path(tmp)/'run'
            subprocess.run([sys.executable,'-B',str(ROOT/'scripts/recovery_smoke.py'),'--out',str(out)],cwd=ROOT,env=env,check=True)
            with np.load(out/'SMOKE_ARRAYS.npz',allow_pickle=False) as new, np.load(ROOT/'audit/reference_smoke/SMOKE_ARRAYS.npz',allow_pickle=False) as old:
                if set(new.files)!=set(old.files):raise RuntimeError('Smoke array keys differ')
                for k in old.files:
                    if new[k].dtype!=old[k].dtype or new[k].shape!=old[k].shape or not np.array_equal(new[k],old[k]):raise RuntimeError('Smoke replay mismatch: '+k)
                n=len(old.files)
            nres=json.loads((out/'SMOKE_RESULTS.json').read_text());ores=json.loads((ROOT/'audit/reference_smoke/SMOKE_RESULTS.json').read_text())
            if nres['cases']!=ores['cases'] or nres['pairs']!=ores['pairs']:raise RuntimeError('Smoke metadata/metrics mismatch')
            print(json.dumps({'fresh_smoke_replay':'PASS','arrays':n,'cases':len(nres['cases']),'qualification010_replay':False}),flush=True)
    print(json.dumps(verify(),indent=2),flush=True)

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,RuntimeError,subprocess.CalledProcessError) as exc:
        print('Recovery validation failed: '+str(exc),file=sys.stderr);raise SystemExit(1)
