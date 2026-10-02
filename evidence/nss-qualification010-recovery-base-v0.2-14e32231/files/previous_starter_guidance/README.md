# Qualification010 recovery starter v0.1

**Status: verified recovery inputs and proposed work order. Qualification010 reconstruction/training/requalification NOT_RUN.**

The lost archive is `NSS_NBR01_Qualification010_v0.1.zip`. Its surviving historical receipt names 302,820,867 bytes and SHA256 `0d8a0e01cc89e9b221a16939a7ebaacd58fd3ed02cbf3fe0e8e64b7429f2d5fe`. That checksum identifies a recovered original; it cannot regenerate missing bytes.

There is better news: the full Study009 parent ZIP survives. Its archive hash and all 501 manifest-covered files were verified afresh, and its 45 research tests passed on a fresh extraction. This starter contains an exact, useful source/checkpoint/calibration/test subset of that parent, not its 243 MB of complete evidence. The inherited readers, binders and relevant dependencies are therefore available. It does not contain the lost Study010-specific implementations, 15 new main checkpoints, full protocol, raw main arrays, or old main source lock.

## Use

Extract into its own folder inside `MegaMind_Alpha_Proto`. Do not merge with any old study or foundation. Read `CODEX_START_HERE.md`; use that as the starting work order in your chosen local Codex project. It does not launch an agent or authorize cloud spend by itself.

With Python available:

```text
python -B verify_recovery.py
python -B verify_recovery.py --parent-tests --probe-checkpoints
```

The first command uses the standard library. The optional checks require the already-installed dependencies in `reference/parent009/requirements.txt`; they do not install packages or access the network. Reference verification and parent tests are not Qualification010 requalification. This starter was checked on Linux CPU; Windows execution has not been tested.

## Contents

- `historical_qualification010/`: the three user-supplied surviving files, copied unchanged. Their PASS status and performance numbers describe the old study only.
- `reference/parent009/`: byte-identical selected source, trained checkpoint and calibration files plus the 45-test suite. See the subset inventory; this is not a full parent-study replay pack.
- `RECOVERY_SPEC.md`: reported facts versus missing details; staged reconstruction, comparison and evidence requirements.
- `TEAM_WORKFLOW.md`: proposed coordination, review, ownership and storage plan.
- `CODEX_START_HERE.md` and `AGENTS.md`: a concrete initial task and project-specific rules.
- `audit/`: fresh checks and provenance, clearly separate from historical receipts.

A reconstructed release should use a new identity such as `NSS_NBR01_Qualification010_Reconstruction_v0.2`. No result inherits qualification merely by reproducing a heading or an old summary table. NBR-02 remains paused until an executable reference is recovered and checked.
