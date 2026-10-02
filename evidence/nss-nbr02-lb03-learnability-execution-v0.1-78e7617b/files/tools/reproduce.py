"""Explicit fresh-directory replay/training. Never overwrite original research.
--audit-inference reruns saved outputs and verification. audit_pass.py also replays
24 optimizer updates on disposable copies; they are charged and noted.
--train is a new 12,288-update experiment plus 24 preflight updates.
This entry point itself was smoke-tested for construction/help; whole training
rerun is not claimed as part of the original evidence.
"""
from pathlib import Path
import argparse,shutil,subprocess,sys,json,hashlib,datetime
R=Path(__file__).resolve().parents[1]
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def call(d,args):subprocess.run([sys.executable,*map(str,args)],cwd=d,check=True)
def build(d):
 for src,out,extra in [('master16.c','master16.so',['-std=gnu11']),('kernels.c','kernels.so',[])]:
  subprocess.run(['gcc','-O2','-fno-fast-math','-ffp-contract=off','-fPIC','-shared',*extra,str(d/'source'/src),'-lm','-o',str(d/'bin'/out)],check=True)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--audit',action='store_true');g.add_argument('--train',action='store_true');a=p.parse_args();d=a.destination.resolve()
 if d.exists():raise SystemExit('Destination must not exist. Use a new path; no overwriting.')
 d.mkdir(parents=True)
 dirs=['source','tools','inputs','fixtures','protocol','bin','docs']+(['results','checkpoints']if a.audit else [])
 for n in dirs:shutil.copytree(R/n,d/n,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for n in ['audit','logs','failures','checkpoints','results','provenance']:(d/n).mkdir(exist_ok=True)
 c=json.loads((d/'protocol/CONFIG.json').read_text())
 if a.audit:
  # Archived binaries/source/config must match original lock; rebuilding is a distinct environment.
  for s in c['parents']:call(d,[d/'tools/audit_pass.py',s])
 else:
  for name in ['MAIN_LOCK.json','ENDPOINT_LOCK.json']:
   path=d/'protocol'/name
   if path.exists():shutil.move(path,d/'provenance'/('ORIGINAL_'+name))
  build(d);call(d,[d/'tools/preflight.py']);call(d,[d/'tools/freeze.py'])
  for i,s in enumerate(c['parents']):
   for j,r in enumerate(c['regimes']):
    modes=c['modes'];order=modes[(i+j)%3:]+modes[:(i+j)%3]
    for m in order:call(d,[d/'tools/run_one.py',s,m,r])
  paths=sorted(x for x in(d/'checkpoints').rglob('*')if x.is_file())
  (d/'protocol/ENDPOINT_LOCK.json').write_text(json.dumps({'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All reproduction endpoints before confirmation','files':[{'path':str(x.relative_to(d)),'bytes':x.stat().st_size,'sha256':sh(x)}for x in paths]},indent=2))
  for s in c['parents']:
   for r in c['regimes']:
    for m in c['modes']:call(d,[d/'tools/evaluate_one.py',s,m,r])
  call(d,[d/'tools/analyze.py'])
 print('Finished new reproduction directory:',d)
if __name__=='__main__':main()
