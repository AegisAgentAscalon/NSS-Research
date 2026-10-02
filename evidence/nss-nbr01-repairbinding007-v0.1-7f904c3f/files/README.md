# NSS NBR-01 — RepairBinding007 v0.1

Standalone experiment: compatible representation repair + frozen BindingDepth006
readers. Read REPORT.md for both successful bounded conditions and failure cases.
**No merge.** Extract beside prior studies inside `MegaMind_Alpha_Proto`.
Not a new foundation release, production migration or completed NBR-01.

## Run
Use Python with the libraries in requirements.txt. Nothing auto-installs.

```
python run.py checks
python run.py rescore
python run.py replay-one
python run.py replay-all
```

Replay/rescore outputs go beside the release under `NSS_Run_Output`.
Main training scripts are research tools and refuse to overwrite checkpoints.
Do not launch main.py over this completed result folder. A fresh copy with output
paths chosen explicitly is required to train new artifacts. Offline training is
separate from scored fixed-weight evaluation.

`reference/` contains exact copies of needed Study006 source/checkpoints and three
prior reports. No other studies need to be merged or installed beside it to run.
The generic Forge/Runtime and four-role companion are NOT integrated by this pass.

The identity dictionary is protected symbolic-reference information with a cost.
It does not store graph edges or answers; its use during maintenance is an explicit
additional interface, not free information or neural recovery from total erasure.

Main results: results/, SUMMARY.json; protocol: spec/PROTOCOL.md; hashes:
spec/REGISTRATION.json; logs/replays/rescoring/development: evidence/.
Windows launchers are supplied but Windows execution is NOT_RUN.
