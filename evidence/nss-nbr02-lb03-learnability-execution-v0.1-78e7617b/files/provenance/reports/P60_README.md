# NSS LB01-Q2-PACK v0.1
## Can the working two-bit model be stored more tightly without changing it?

**Result:** Yes, lossless Huffman coding reduces the matrix-code stream to 1.789–1.830 bits/entry. Complete files are 4.46–5.53% smaller than a matched raw container. All evaluated weights, trajectories and answers remain exact. The simple decoder is 7.56–8.23x slower, so it is **not the default runtime**. Keep the direct Q2 reference.

This is one small, reproducible research pass—not a new foundation model, a novel compression algorithm, or a 20B-model claim. No training, backward passes, real tools, network model calls or post-learning repair are used. The four archived models retain all four quantization levels; a shorter average code is not ternary weights.

## Start here
- `docs/REPORT.md` and the Word report: question, methods, every model result, interpretation and decision.
- `protocol/PROTOCOL.md`: local prospectively fixed comparison and decision rule.
- `results/SUMMARY.json`: machine-readable decision; `results/PARENT_*.json`: every measurement.
- `results/BENCHMARK.json`: every timed repetition.
- `docs/ALL_TESTS.jsonl`, `docs/TESTS_AND_ANSWERS.md`, `results/*.npz`: exact tests and raw answers.
- `docs/FORMAT.md`: binary container/decoder contract.
- `docs/REPRODUCTION_VERIFICATION.md`: extra end-to-end reproduction, its caller interruption, and exact recovery checks.
- `docs/RESEARCH_LIBRARY_ADDENDUM.md`: connection to the prior59-pass master and the new60-entry index.
- `docs/RESEARCH_PRACTICES.md`: research procedure and review etiquette.
- `docs/MODEL_AND_DATA_CARD.md`, `ATTRIBUTION.md`, `LICENSE_DECISION_REQUIRED.md`: scope and release boundaries.

## Local requirements
Tested: Linux x86-64, Python 3.13.5, NumPy 2.3.5, GCC 14.2.0, zlib 1.3.1. A C compiler and zlib headers/library are needed. The retained `results/BUILD.json` gives exact compiler commands. No PyTorch, pretrained download, API key or pickle loading is needed. Other platforms are unvalidated. The simple C entry point is an internal API: the Python loader must validate a model before passing it to C.

## Run without overwriting evidence
From the unpacked package:

```bash
python tools/verify_package.py
python tools/reproduce.py --output ../q2-pack-smoke --smoke
```

For full producer execution and independent internal audit:

```bash
python tools/reproduce.py --output ../q2-pack-reproduction --full
```

The output directory must not already exist. The script copies only the frozen source, tests, inputs and provenance needed for a fresh run; then compiles, executes the synthetic preflight, all four model comparisons, the timing study, and the fresh-process audit. It does not update the original archive. Runtime and binary bytes can differ across environments; compare canonical models and decoded arrays, not ZIP timestamps or elapsed time. `--full` runs the actual neural inference workload, not just a file check.

Manual command equivalents are in `docs/REPRODUCTION.md`. The full package contains the original inputs and current raw results. A compact review package deliberately omits the larger arrays and must not be advertised as self-sufficient execution evidence.

## What is and is not low-memory
C execution decodes one 256-byte packed row group at a time. No full expanded weights are retained in that path. Initial Python load validation DOES transiently decode the whole numerical body. The named-buffer accounting is not total RAM: Python, libraries, call frames, input/output arrays and validation matter. Whole-file zlib compression is an archive control, not a running-RAM reduction.

## Publication boundary
This is a repository-shaped **publication candidate**. No repository has been uploaded and no license has been imposed on inherited material. Resolve `LICENSE_DECISION_REQUIRED.md`, inspect source/provenance for publication, and complete an independent review before treating this as an openly licensed public release. Preserve negative results and old failed gates. Do not overwrite this study when extending it.
