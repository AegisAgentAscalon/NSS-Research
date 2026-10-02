from pathlib import Path
import sys,json,time,os,traceback,datetime
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from candidate import *

def verify_lock():
 d=json.loads((R/'protocol/MAIN_LOCK.json').read_text())
 for x in d['files']:
  if sha(R/x['path'])!=x['sha256']:raise RuntimeError('LOCK:'+x['path'])
 return sha(R/'protocol/MAIN_LOCK.json')
def evidence_size():return sum(p.stat().st_size for p in R.rglob('*')if p.is_file())
def existing_steps():
 total=0
 for p in (R/'checkpoints').glob('*/updates.jsonl'):
  total+=sum(1 for l in p.read_text().splitlines()if l.strip())
 return total

def run(seed,mode,regime):
 locksha=verify_lock();folder=R/f'checkpoints/{seed}_{regime}_{mode}';folder.mkdir(parents=True,exist_ok=True)
 if (folder/'START.json').exists():raise RuntimeError('EXISTING_START_NO_AUTOMATIC_RERUN')
 if existing_steps()+C['updates_per_branch']>C['total_main_updates']:raise RuntimeError('MAIN_UPDATE_CAP')
 previous_core=sum(json.loads(line)['seconds'] for p in (R/'checkpoints').glob('*/updates.jsonl') for line in p.read_text().splitlines() if line.strip())
 s=Candidate(seed,mode,regime);start=time.perf_counter()
 write(folder/'START.json',dict(seed=seed,mode=mode,regime=regime,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=s.source_file_sha,lock_sha=locksha,allowed_actual_updates=512))
 cps=[s.save(folder/'step0000.npz')];journal=folder/'updates.jsonl';total=0
 with np.load(R/f'inputs/replay/{seed}.npz',allow_pickle=False)as z:t=z['tokens'];y=z['labels']
 try:
  with journal.open('ab')as log:
   for i in range(C['updates_per_branch']):
    if rss()>C['max_rss_bytes'] or time.perf_counter()-start>C['branch_wall_limit_seconds']:raise RuntimeError('RESOURCE_CAP')
    write(folder/'INFLIGHT.json',dict(cursor=i+1,previous_state=s.hash(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    row=s.step(t[i%64],y[i%64],lr_at(i),profile=(i in (0,511)));total+=row['seconds']
    log.write(canon(row)+b'\n');log.flush();os.fsync(log.fileno())
    if previous_core+total>C['total_training_core_limit_seconds']:raise RuntimeError('GLOBAL_TRAINING_CORE_CAP')
    (folder/'INFLIGHT.json').unlink()
    if s.cursor in C['branch_checkpoint_steps']:
     if evidence_size()+300000>C['evidence_bytes']:raise RuntimeError('EVIDENCE_CAP')
     cps.append(s.save(folder/f'step{s.cursor:04d}.npz'))
    if rss()>C['max_rss_bytes'] or time.perf_counter()-start>C['branch_wall_limit_seconds']:raise RuntimeError('RESOURCE_CAP_AFTER_UPDATE')
  write(folder/'COMPLETE.json',dict(seed=seed,mode=mode,regime=regime,actual_updates=s.cursor,core_seconds=total,branch_seconds=time.perf_counter()-start,peak_rss=rss(),checkpoints=cps,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_inputs_still_match=verify_lock()==locksha))
  print(json.dumps(json.loads((folder/'COMPLETE.json').read_text())),flush=True)
 except BaseException as e:
  write(folder/'STOP.json',dict(exception=repr(e),traceback=traceback.format_exc(),in_process_known_completed_cursor=s.cursor,inflight_exists=(folder/'INFLIGHT.json').exists(),seconds=time.perf_counter()-start,rule='Stop. No automatic repetition of unknown tail.'))
  raise
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('seed',type=int);a.add_argument('mode',choices=C['modes']);a.add_argument('regime',choices=C['regimes']);v=a.parse_args();run(v.seed,v.mode,v.regime)
