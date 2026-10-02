from pathlib import Path
from nbr01_recovery.train import train
for repseed in range(301,306):
 for kind in ('readout_repair','recurrent','fast_slow'):
  train(Path.cwd(),Path('evidence/main'),kind,repseed,repseed+200,1800)
print('MAIN_TRAINING_COMPLETE',flush=True)
