# TIMING01 completed research evidence

Start with REPORT.md and STATUS.json. Completed numerical experiment, not a full-trajectory scientific pass. All data are new for this study; old stopped archives remain separate historical references.

## Read and reproduce

Reports, protocol, scores, analysis tables and program notes are directly readable after extracting the ZIP. Original large logs and numerical frames use lossless encoding; identical fresh-replay files use verified aliases.

```text
python RESTORE_EVIDENCE.py
python VERIFY_STUDY.py
python RESCORE.py --output /a/new/empty/rescore-directory
python tools/ANALYZE_RESULTS.py --output /a/new/empty/analysis-directory
```

Restoration uses Python's gzip/lzma/zlib and source/envelope_codec.py; exact frame-byte reconstruction requires zlib1.3.1. No network, old archives or model forward calls are needed to restore. Re-scoring needs NumPy (tested2.3.5). Full fresh learning replay additionally needs the pinned CPU PyTorch environment and explicit approval for new work. `REPLAY_STUDY.py --help` describes it; this optional helper was syntax/CLI checked, not used for another run in this delivery.

The 64MiB cap applies to the delivered ZIP and256MiB to encoded retained live evidence during the experiment. Restoring every byte-identical duplicate into files produces a larger working copy; allow at least500MB free for extraction/restoration/rescoring. The exact total is in MANIFEST.json and the external delivery receipt. Do not mistake archive compression for neural-state memory savings.

## Verification scope

MANIFEST.json lists each physical or restored/aliased payload and original hash. `VERIFY_STUDY.py --physical` checks only direct delivered payloads before restoration. The manifest does not self-hash; the external archive SHA256 identifies it and every ZIP member. All source/protocol locks were fixed before generation. Numerical replay genuinely recalculated all adaptation; restoration merely recreates those already-verified bytes.

G/L mathematics, task labels, first-correction error counts, confidence limits and every raw negative remain unchanged by packaging. Read audit/INCIDENTS.md for the measured storage-layout forecast shortfall and lossless remedy.

The screenshot paper is listed only in program/TRAINING_PAPER_BACKLOG.md as deferred external research. No generator, pretraining code, Transformer or dream mechanism from it was implemented here.
