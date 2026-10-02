#!/usr/bin/env python3
"""Explicit, separately logged new execution of the successful scientific version.
This file was syntax-checked, NOT executed during delivery. It does not repeat the old storage stop.
"""
import os,sys,json,time,shutil,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=3 or sys.argv[1]!='--authorize-new-run':
 raise SystemExit('Usage: python REPRODUCE.py --authorize-new-run /new/study/directory\nThis launches fresh training and adaptive replay; it does not alter the delivered study.')
dst=Path(sys.argv[2]).resolve()
if dst.exists():raise SystemExit('Destination already exists; choose an unused path.')
dst.mkdir(parents=True);(dst/'audit').mkdir();(dst/'raw').mkdir();(dst/'attempts').mkdir()
for group in ('source','protocol','program'):shutil.copytree(ROOT/group,dst/group)
for name in ('SOURCE_LOCK.json','HISTORICAL_SUMMARY.json'):
 shutil.copy2(ROOT/'audit'/name,dst/'audit'/name)
now=time.time();(dst/'audit/START.json').write_text(json.dumps({'epoch':now,'started_epoch':now,'started_host_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(now)),'scope':'separate reproduction of successful version; original ledger remains closed'},indent=2))
(dst/'REPRODUCTION_IDENTITY.json').write_text(json.dumps({'source_package':str(ROOT),'source_lock_sha256':hashlib.sha256((ROOT/'audit/SOURCE_LOCK.json').read_bytes()).hexdigest(),'original_preflight_stop_repeated':False,'new_execution_not_extension':True},indent=2))
env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
# Sealed evidence may need lossless compression before replay for this 512MiB live ceiling.
# This launcher deliberately does not waive caps or delete evidence. A recorded resource stop is possible.
for stage in ('primary','replay'):
 p=subprocess.run([sys.executable,str(dst/'source/supervise.py'),stage],env=env)
 receipt=json.loads((dst/f'audit/supervisor_{stage}/RESULT.json').read_text())
 if receipt['returncode']!=0:raise SystemExit('Recorded stop: '+json.dumps(receipt))
print('Two passes completed; independently compare and package their evidence. No qualification is inferred by this launcher.')
