# STATEBRIDGE01 v0.2 — diagnostic study, not qualified

Start with REPORT.md and STATUS.json. Main capture and adaptive replay completed; the original whole-prefix numerical tolerance remains failed, and the repair adequacy screens also failed. Supplementary one-step/class checks do not waive these results.

After extraction:
```
python RESTORE_EVIDENCE.py
python VERIFY_STUDY.py
OPENBLAS_NUM_THREADS=1 python RESCORE.py --output /path/to/new_diagnostic_scores
```

Restoration uses NumPy and standard Python; it rebuilds recorded NPZ files exactly and copies genuinely verified replay aliases. It performs no model operation. Exact compressed byte restoration was checked with NumPy2.3.5 and Python3.13.5; different compression/library versions may reproduce arrays but fail exact byte checks. Do not silently rewrite the manifest for that situation.

RESCORE explicitly produces diagnostic tables while preserving the original numerical failures. The unchanged original strict command is:
```
OPENBLAS_NUM_THREADS=1 python source/score.py --input primary --output /path/to/new_strict_scores --config protocol/CONFIG.json
```
That original command is expected to raise the recorded whole-trajectory tolerance failure. A successful integrity verifier is not scientific qualification.

Raw initial fitting gradients/activation graphs are not all retained. Input and parameter hashes, losses/norms, fullperiodicAdam/RNG/cursorcheckpoints andexactadaptive replay are retained. Online/repair gradients and state traces are captured. Historical study archives are not dependencies for these data.

Never execute source/run.py casually to rescore: it trains fresh models and incurs a complete new workload. No additional run is authorized by files in this archive.
