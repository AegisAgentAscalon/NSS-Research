from pathlib import Path
import sys,subprocess,os,json,time,datetime
from q010c.protocol import ROOT,STAGING as S
name=sys.argv[1];out=ROOT/'results'/name;out.mkdir(exist_ok=False);commands=[]
for kind in ('transaction','rng','maintenance','record','attention','lifecycle'):
 for phase in ('prepare','restore'):
  cmd=[sys.executable,str(ROOT/'tools/fresh_resume_worker.py'),phase,kind,'--attempt',name]
  st=time.monotonic()
  with (out/f'{kind}-{phase}.log').open('x') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=240,env=os.environ)
  commands.append({'command':cmd,'rc':r.returncode,'seconds':time.monotonic()-st,'log':f'{kind}-{phase}.log'})
  (out/'COMMANDS.json').write_text(json.dumps(commands,indent=2))
  if r.returncode:raise SystemExit(f'{kind}/{phase} failed; retained log')
results=[json.loads((S/'plan/runtime_tmp'/name/k/'PASS.json').read_text()) for k in ('transaction','rng','maintenance','record','attention','lifecycle')]
(out/'RESUME_VERIFICATION.json').write_text(json.dumps({'status':'PASS','cases':results,'new_optimizer_updates':0,'scope':'Six fresh-interpreter disposable-network real operation-boundary checks, not main study'},indent=2));print('PASS',len(results))
