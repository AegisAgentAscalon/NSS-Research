from pathlib import Path
from nbr01_recovery.evaluate import evaluate
for repseed in range(301,306):
 print(evaluate(Path.cwd(),Path('evidence/main'),Path('evidence/results'),repseed,repseed+200),flush=True)
print('MAIN_EVALUATION_COMPLETE',flush=True)
