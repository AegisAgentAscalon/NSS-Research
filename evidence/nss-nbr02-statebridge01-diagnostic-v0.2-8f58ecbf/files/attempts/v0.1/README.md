# STATEBRIDGE01 executable / evidence package
Read protocol/PROTOCOL.md first. No historical model is loaded. No learned token curator or tri-core implementation is included.

To execute a NEW explicitly budgeted capture with this source (do not overwrite existing outputs):
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python source/run.py --output /path/to/new_capture`

To re-score retained output without Torch/model inference:
`OPENBLAS_NUM_THREADS=1 python source/score.py --input primary --output /path/to/new_scores --config protocol/CONFIG.json`

A genuine adaptive replay runs source/run.py again from fresh initialization; it is a second complete training workload. Do not confuse rescoring with replay. Check the execution report/status and shared budgets before any new work. This source package is exported before numerical execution, so a source ZIP alone is not completed evidence.
