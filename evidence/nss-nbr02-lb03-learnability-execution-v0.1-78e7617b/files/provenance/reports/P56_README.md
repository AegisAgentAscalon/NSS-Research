# NSS LB01-TERNARY v0.1

A first bounded ternary-weight study, not an accepted NSS serving replacement.

**Read REPORT.md first.** Direct ternarization severely damaged the known checklist model. Ternary-aware continuation recovered most event accuracy but not reliable whole tasks. Packed code storage and actual packed execution work. Total low-memory training and a speed gain have NOT been demonstrated.

## Requirements and boundaries
The measured host used Python 3.13.5, NumPy 2.3.5, PyTorch 2.10.0+cpu and Linux x86-64. `provenance/ENVIRONMENT.json` gives the full binding. The compiled `bin/ternary.so` is platform-specific. Training and audit source is included for inspection/reproduction. Native Windows and other processor/OS combinations are untested; use a separately bound compatible Linux/WSL environment rather than assume portability.

## Safe archive verification (standard library only)
From the extracted package root:

```sh
python tools/verify_package.py
```

The verifier checks files only. It never trains or runs a model. Added user files outside the manifest will be reported; work in a separate directory. Python bytecode caches are ignored.

## Offline packed inference demo
Requires NumPy/PyTorch and a compatible shared library:

```sh
python tools/demo_packed.py --parent 4101 --history 4
```

The demo runs one already-exposed retained history. It prints the raw expected/predicted next-item sequence and the 6,717-byte packed numerical payload. It does NOT fix the model's wrong answers. No private data, network request or real external action occurs. This helper was added after the scientific audit; its smoke receipt is separate.

The packed C backend reads ternary codes directly. Floating recurrent/gate arithmetic and scaling remain. The Python module imports PyTorch even when the packed backend is used, so process memory is not comparable to a tiny native embedded executable.

## Building the C kernel elsewhere
Source is `source/ternary.c`. The measured build used:

```sh
gcc -O3 -shared -fPIC -fno-fast-math -ffp-contract=off source/ternary.c -o bin/ternary.so -lm
```

First verify the original package, then rebuild only in a separate working copy and record the new source/binary/runtime identities. A rebuild may change the binary hash. Do not edit the original source lock to claim an unchanged experiment; numerical and behavioral comparisons are required under the new runtime.

## Research drivers
`source/prepare.py`, `preflight.py`, `study.py` and `audit.py` are the actual retained executors. The scientific artifacts contain original path-bound checkpoint receipts. They require deliberate output-directory and path rebinding for complete relocated reruns. Do not blindly launch a driver on this read-only evidence archive or overwrite its checkpoints. A fresh reproduction is new work, not an archive-integrity check. Inspect `protocol/PROTOCOL.md` for the exact budgets and stages.

## Main contents
- `inputs/parents/`: all four original float32 parent arrays.
- `inputs/replay/`: all selected old replay batches actually used.
- `fixtures/`: the public event sequences and scorer-only expected labels/masks.
- `checkpoints/`: 40 model/optimizer/RNG/cursor files and every update journal.
- `exports/`: all effective arrays and 20 packed ternary exports.
- `results/`: all 200 raw evaluated trajectory files, decisions, costs and numerical receipts.
- `failures/`: first observed incorrect trajectory captures. A failed prediction remains a failure.
- `audit/`: fresh-process recount/replay and byte/precision checks.
- `docs/`: public test/answer examples, source-grounded interpretation and Codex handoff.

No low-bit working point is declared. User-requested low-bit inference and learning remain the exclusive next focus; unrelated NSS research stays on hold.

`CONFIG.json` is the original prospective configuration. Its zero setup counter `actual_optimizer_steps` is not the execution ledger; the update journals and `audit/AUDIT.json` record all 4,608 main applications. The one post-result convenience demo is separately recorded in `audit/DEMO_SMOKE.json` and is not new confirmation.
