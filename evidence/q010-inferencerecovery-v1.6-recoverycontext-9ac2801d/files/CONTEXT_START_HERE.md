# Compact Q010 recovery context

This is a review and inference-regeneration bundle, **not the full raw-evidence archive**.
Read REPORT.md and CONTEXT_SCOPE.json. The original README describes both delivery variants; its restore/dedup commands apply only to the complete ZIP.

Run `python VERIFY_CONTEXT.py` to verify this context bundle. All selected files are physically present; no alias restoration is needed. The `recovery/worker.py` inference-only commands in README work with new output paths and the recorded numerical dependencies. The complete ZIP named in CONTEXT_SCOPE.json contains the raw main captures/replays and original uploads.

Do not run old training drivers. All fifteen main models remain fixed, and absent raw training traces and full optimizer/RNG checkpoints remain absent.
