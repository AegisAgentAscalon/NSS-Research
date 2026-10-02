# NSS LB01-T3-TARGET v0.1
A completed model-quantization experiment. Read `docs/REPORT.md` first. This package preserves evidence; no command should be interpreted as authorizing another study.

## Environment
Linux x86_64, Python3 with NumPy and CPU PyTorch, gcc for the supplied C sources. See the recorded protocol environment; no portability claim for other operating systems or library versions. `torch.load(weights_only=True)` is used, but run only code/artifacts you have reviewed. No network connection or external model is needed.

Rebuild platform-specific shared libraries when necessary, from package root:
```bash
gcc -O2 -std=c99 -shared -fPIC source/kernels.c -o bin/kernels.so -lm
gcc -O2 -std=c99 -shared -fPIC source/ternary.c -o bin/ternary.so -lm
```
Compiler changes require checking numeric behavior; rebuilding may change artifact hashes. Preserve originals first.

## Inspect before executing
`results/SUMMARY.json` and `audit/FINAL_AUDIT.json` give retained results. `docs/TESTS_AND_ANSWERS.md` contains actual prompts (event streams) and answers. Archives have a manifest verified at delivery. `python source/verify_archive.py <execution.zip>` performs bytes-only ZIP verification, no models.

## Reproduce the recorded model outputs
On a COPY of this directory, with compatible dependencies and after recording that this is new audit work:
```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python source/audit_target.py 4101
python source/audit_target.py 4102
python source/audit_target.py 4103
python source/audit_target.py 4104
```
These calls redo inference, overwrite replay receipts in that copy, and perform zero optimizer applications. They are not third-party replication until an independent party actually runs/reports them.

## Training entry point — not required for verification
`source/train_target.py SEED ARM 1024` handles one arm. `source/evaluate_target.py SEED REFERENCES` or `SEED ARM` writes fresh profile results and refuses an existing result file. Do NOT run these over the delivered evidence. For an authorized rerun, create an isolated copy with a new run identity, preserve original inputs/locks, remove only the COPY's generated checkpoints/results/exports, then register a new budget. The delivered latest checkpoints are already complete; invoking their trainer is not evidence of newly reproduced training. Original fixed model and task are documented in the protocol.

No automatic next phase, no optimization of training memory, no post-learning repair or changed associations. Q2 interim remains useful; this ternary working point failed.
