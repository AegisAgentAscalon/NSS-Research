# REHEARSE01 execution v0.2

**STOPPED_AT_A0.** Complete evidence for the actually executed preflight, initial/development learning and fresh adaptive replay; not a full held-out study. Start with REPORT.md, STATUS.json and CHAT_PROMPT.md.

This archive is self-contained for verifying and independently re-scoring the new numerical evidence. Historical models/archives are not duplicated or required. Their provenance limitations remain.

After extraction:

```text
python RESTORE_EVIDENCE.py
python VERIFY_STUDY.py
python RESCORE.py --output /path/to/new_rescore_directory
```

RESTORE_EVIDENCE.py reverses a lossless encoding and copies an exact verified replay alias. It does not run a model or synthesize missing measurements. The original two record streams were genuinely computed independently and byte-matched before deduplication. The exact framed-byte restoration uses the pinned zlib1.3.1 encoder; another encoder version is not promised to reproduce byte-identical compressed frames. Standard Python plus NumPy are needed for restoration/rescoring; rescore does not import Torch or train.

source/ contains the frozen scientific implementation and independent scorer. protocol/ contains the unchanged reviewed design plus explicitly fixed implementation details. raw/primary and raw/replay contain messages, source truth/receipts, every numerical frame, outputs, gates, checkpoint/RNG/cursor records and audit results. analysis/ contains new descriptive development summaries, labelled exploratory. Failed or incorrect cases are not removed.

The original shared attempt ledger is closed at 3,576 updates, 1,788 per pass. No held-out maps were generated. Do not dispatch source/driver.py as a continuation of this run or silently reset the archived budget. A future adaptive reproduction requires a new output root, an explicitly approved new work ledger/clock, and preservation of all source/protocol identities. It is not the same as RESCORE.py, which performs no learning.

No automatic NBR-stage advance, NBR01 reopening, dreamtraining or retuning follows. See program/USER_RETURN_PLAN.md and RETURN_TICKETS.md.
