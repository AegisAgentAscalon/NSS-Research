"""Portable research checks. No automatic installs, downloads or deployments."""
from pathlib import Path
import argparse,subprocess,sys,datetime
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('mode',choices=['checks','rescore','replay-one','replay-all']);a=p.parse_args()
if a.mode=='checks':cmd=[sys.executable,'-m','unittest','discover','-s','tests','-v']
elif a.mode=='rescore':cmd=[sys.executable,'scripts/rescore.py','--out',str(ROOT.parent/'NSS_Run_Output'/'RepairBinding007_rescore.json')]
else:
 out=ROOT.parent/'NSS_Run_Output'/('RepairBinding007_replay_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
 cmd=[sys.executable,'scripts/replay.py','--out',str(out)]
 if a.mode=='replay-one':cmd+=['--seed','901']
raise SystemExit(subprocess.run(cmd,cwd=ROOT).returncode)
