"""Convenience commands; no network, installs, source overwrites or deployment."""
from pathlib import Path
import argparse,subprocess,sys,datetime,uuid
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['checks','rescore','replay']);p.add_argument('--pair',type=int,choices=range(1,6),default=1);a=p.parse_args()
 if a.mode=='checks':
  subprocess.run([sys.executable,'scripts/check_integrity.py'],cwd=ROOT,check=True)
  return subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT).returncode
 if a.mode=='replay' and sys.platform=='win32':
  print('Full replay currently targets Linux resource telemetry. Windows replay is NOT_SUPPORTED in this release; checks/rescore are separate, unvalidated Windows paths.');return 2
 out=ROOT.parent/'NSS_Run_Output'/('MembershipRepair008_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8]);out.mkdir(parents=True)
 if a.mode=='rescore':cmd=[sys.executable,'scripts/rescore.py','--results',str(ROOT/'results'),'--out',str(out/'RESCORE.json')]
 else:cmd=[sys.executable,'scripts/replay.py','--out',str(out),'--pairs',str(a.pair)]
 code=subprocess.run(cmd,cwd=ROOT).returncode;print('Output:',out);return code
if __name__=='__main__':raise SystemExit(main())
