from pathlib import Path
import hashlib,json,datetime,sys,platform,subprocess,os
R=Path(__file__).resolve().parents[1]
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
import numpy as np,torch
assert json.loads((R/'audit/PREFLIGHT.json').read_text())['status']=='PASS'
paths=[]
for folder in ['source','tools','inputs','fixtures','bin']:
 paths.extend(p for p in(R/folder).rglob('*')if p.is_file()and'__pycache__'not in str(p))
paths.extend([R/'protocol/CONFIG.json',R/'protocol/PROTOCOL.md',R/'docs/CANDIDATES.md'])
env=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,numpy=np.__version__,torch=torch.__version__,system=platform.platform(),compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],cgroup_memory=Path('/sys/fs/cgroup/memory.max').read_text().strip(),cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),compiled_flags='-O2 -fno-fast-math -ffp-contract=off -fPIC -shared; gnu11 for _Float16')
(R/'protocol/ENVIRONMENT.json').write_text(json.dumps(env,indent=2));paths.append(R/'protocol/ENVIRONMENT.json')
lock=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),purpose='Before first main optimizer application or main model evaluation',preflight_actual_updates=json.loads((R/'audit/PREFLIGHT.json').read_text())['actual_model_updates'],files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sh(p))for p in sorted(set(paths))])
file=R/'protocol/MAIN_LOCK.json'
if file.exists():raise RuntimeError('NO_LOCK_REPLACEMENT')
file.write_text(json.dumps(lock,indent=2));print('FROZEN',len(lock['files']),'files',sh(file),lock['frozen_utc'])
