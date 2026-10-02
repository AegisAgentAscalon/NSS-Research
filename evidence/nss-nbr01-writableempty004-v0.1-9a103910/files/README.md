# NSS NBR-01 / WritableEmpty004 v0.1

Standalone synthetic research. Not a cumulative MegaMind Alpha source release,
not a patch, and not a trained tri-core companion.

Place this directory **beside** the foundation and earlier studies inside
`MegaMind_Alpha_Proto`. Do not merge any of their contents. The earlier ZIPs and
v0.5.0 foundation have not been modified.

Read **REPORT.md** for results, their failures and interpretation. **SUMMARY.json**
contains the complete five-seed summaries. The code, trained weights, input
provenance, registered protocol, failed development runs and replay evidence
are included.

## Commands

From this directory, with Python, PyTorch, NumPy and safetensors available:

```
python run.py checks
python run.py verify
python run.py resume
python run.py reproduce-one
```

`checks` verifies the manifest and runs the44 research unit tests. `verify`
replays every main case, checks source hashes, independently rebuilds the
expected record values and recomputes answer scores. It can take several
minutes on CPU. `resume` checks80 saved state/RNG continuations. `reproduce-one`
repeats one complete1,800-step training trajectory.

These entrypoints keep packaged files unchanged. The latter commands run in a
temporary copy and place new receipts/logs beside the package under a uniquely
named run-output directory. Direct developer scripts under `tools/` may write
into their own copy; use `run.py` for normal verification.

To explicitly repeat all15 tiny-model fits in a NEW directory:

```
python run.py train --output ../WritableEmpty004_my_reproduction
```

Existing completed runs will not be overwritten. `psutil` is also required for
training resource sampling. No command installs dependencies, downloads a
model, uploads data, accesses an account, changes a repository, or deploys a
candidate. `requirements-recorded.txt` records this run's environment, not a
claim of tested compatibility with every version or Windows.

Windows launchers call `py -3` or `python`; their Windows execution is NOT_RUN.
Linux CPU execution was tested. Generic Forge/Runtime remain unconnected.

## Scope

Four explicit addresses, eight finite learned values and UNKNOWN. Exact clean
write qualification and full-code insertion are supplied operations. Neural
weights are fixed during scoring. The existence-field controls have separately
protected boolean metadata; vector faults do not damage it unless explicitly
requested in the metadata-fault challenge. The local empty-region candidate has
no such field, but uses the declared EMPTY=0 coordinate convention.

A small successful controlled memory is not a generally competent Secondary.
The exact archive, tri-core roles, advisory Validator, and no-overlay direction
remain unchanged. NBR-01 as a whole is OPEN; this is not recurrent reasoning,
delayed-credit learning, low-bit training or biological simulation.
