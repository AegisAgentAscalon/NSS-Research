"""Verify every delivered logical payload. Use --physical before restoration."""
from pathlib import Path
import argparse,hashlib,json,sys
R=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--physical',action='store_true');a=p.parse_args()
m=json.loads((R/'MANIFEST.json').read_text());checks=[]
for rel,x in m['files'].items():
 if a.physical and not x['physical']:continue
 f=(R/rel).resolve()
 if not f.is_relative_to(R.resolve()):raise ValueError('UNSAFE_PATH')
 h=hashlib.sha256()
 if f.is_file():
  with open(f,'rb') as z:
   for b in iter(lambda:z.read(1<<20),b''):h.update(b)
 good=f.is_file() and f.stat().st_size==x['bytes'] and h.hexdigest()==x['sha256']
 if not good:checks.append(rel)
if not a.physical:
 sys.path.insert(0,str(R/'source'));import check_lock
print(json.dumps({'status':'PASS' if not checks else 'FAIL','mode':'physical' if a.physical else 'full_logical','checked':sum(not a.physical or x['physical'] for x in m['files'].values()),'mismatches':checks,'new_model_calls':0},indent=2))
if checks:raise SystemExit(2)
