"""Portable entry point for the *tested Linux* repair checks; no main-run dispatch."""
from pathlib import Path
import argparse,os,subprocess,sys
R=Path(__file__).resolve().parents[1];S=R/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0';A=S/'implementation_A';B=S/'verification_B'
p=argparse.ArgumentParser();p.add_argument('check',choices=['tests','rescore','development','resumes']);p.add_argument('--output-name');a=p.parse_args()
env=os.environ.copy();env.update(PYTHONPATH=os.pathsep.join(map(str,[R/'source',A,B])),OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
if a.check=='tests':cmd=[sys.executable,'-m','pytest','-q',str(A/'tests'),str(R/'source/tests')]
else:
 if not a.output_name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.output_name):p.error('new --output-name using letters/numbers/_/- is required')
 if a.check=='rescore':cmd=[sys.executable,str(R/'tools/rescore_capture.py'),str(R/'results/dev64_attempt02/capture'),str(R/'results'/a.output_name)]
 elif a.check=='development':cmd=[sys.executable,str(R/'tools/run_development_capture.py'),'--attempt',a.output_name]
 else:cmd=[sys.executable,str(R/'tools/run_fresh_resumes.py'),a.output_name]
print('Running:',subprocess.list2cmdline(cmd),flush=True);raise SystemExit(subprocess.call(cmd,cwd=R,env=env))
