"""Portable launcher without modifying the main-run-locked training source.
On platforms lacking POSIX resource, peak RSS is explicitly null, not invented.
Windows execution remains NOT_RUN for this delivery.
"""
import sys,types,runpy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
try:import resource
except ImportError:
 resource=types.ModuleType('resource');resource.RUSAGE_SELF=0
 resource.getrusage=lambda _:types.SimpleNamespace(ru_maxrss=None)
 sys.modules['resource']=resource
 print('POSIX peak RSS unavailable; resource field will be null. No estimate substituted.',flush=True)
runpy.run_module('nbr006.train',run_name='__main__')
