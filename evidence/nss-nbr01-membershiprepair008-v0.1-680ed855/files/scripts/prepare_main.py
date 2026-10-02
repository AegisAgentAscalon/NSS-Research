from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import *
from nbr008.prepare import fit,calibrate
from nbr008.config import MAIN_SEEDS

def main():
    start=time.perf_counter();runs=[]
    for seed in MAIN_SEEDS:
        m,info=fit(seed,1200,ROOT/'checkpoints');cal=calibrate(seed,m,ROOT/'checkpoints',4096);runs.append({'fit':info,'calibration':cal})
    dump(ROOT/'evidence/PREPARATION_SUMMARY.json',{'runs':runs,'seconds':time.perf_counter()-start})
if __name__=='__main__':main()
