from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
from nbr009.train import fit
from nbr009.context import calibrate
setup()
for pair in range(1,6):
    for kind in ('ordinary','near'):
        fit(pair,kind,1100+pair,1200,ROOT/'checkpoints'/f'binder_{kind}_{1100+pair}.safetensors')
    calibrate(pair,ROOT/'checkpoints'/f'cue_calibration_{pair}.npz')
