# REV01 complete study — start here

Read REPORT.md and STATUS.json. The result is **effective first-correction improvement with failed old-knowledge retention qualification**, not an omnibus pass. Dream-linked maintenance is separately documented and unexecuted.

## Restore and verify

After extracting the complete ZIP:

```
python RESTORE_EVIDENCE.py
python VERIFY_STUDY.py
```

Restoration losslessly recreates captured frames from an XZ header/numeric-byte-lane container and restores verified duplicate files. It performs no model arithmetic. zlib1.3.1 produced the captured frame bytes; any byte mismatch on a different compressor is reported, not silently accepted. The compact handoff has no raw evidence to restore and is not a numerical replication package.

## Independent scoring

```
python RESCORE.py --output /new/directory/rev01-rescore
```

This uses Python and NumPy to reconstruct input labels, tables, gradient formulas and the scored outputs from captured arrays. It performs no Torch forward/backward or optimizer updates. The source scorer never imports producer/model/controller modules. It reproduces only the retained evidence, not a second training run.

## Separate adaptive reproduction

The delivered execution ledger is closed. The optional wrapper

```
python REPLAY_STUDY.py --output /new/directory/rev01-independent-run
```

creates a separately charged reproduction with the pinned source and fresh initialized models. It does not overwrite or extend the delivered study. The wrapper's syntax/help are checked; it was not used to run a third complete reproduction during delivery. The actual delivered replay is raw/replay and its receipt is audit/REPLAY_VERIFICATION.json.

Pinned numerical runtime: Python3.13.5, NumPy2.3.5, PyTorch2.10.0+cpu, deterministic single-thread float32. Cross-device/version exact equality is not established. Source has no need for old neural weight archives; historical source and compact mapping evidence are retained for provenance and overlap checks.

## Evidence layout

* `protocol/`: reviewed proposal, original choices and pre-generation execution completions/amendment. Historical PROPOSED wording in source documents is not the current execution status.
* `source/`: locked actor, data driver, independent scorer, recorder, fault/contract tests, supervisor and storage codec.
* `raw/primary` and `raw/replay`: genuine separate learning executions, each with public message stream, private generator/score ledger, all numerical frames, receipts, checkpoints and independently scored results.
* `attempts/v0.3`: complete preserved storage-gated prefix, source/locks and failure receipts. No main fit occurred in that attempt.
* `reports/`: analyst-derived summaries and complete negative index; these do not change locked scores or gates.
* `architecture/`, DREAM_MAINTENANCE.md and RETURN_TICKETS.md: architecture-linked outcome and future-maintenance notes.
* `audit/`: hashes, mathematical/replay checks, state-machine tests, monitored resource/call evidence and delivery prechecks.

No historical Q010/TS01/TS02/TS03/DC01 model was loaded or modified; no old raw archive is duplicated as a hidden numerical dependency. NBR-01 bounded closure, NBR-02 active status, parked workspace ticket and post03 foundation return are preserved. Every G01–G22 question is in PROGRAM_CONTEXT_CURRENT.md.
