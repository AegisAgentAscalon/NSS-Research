# Local audit — Recovery Experiment 001B

## Audit scope

Independent review of the uploaded `0.2.0-recovery001a` handoff before implementing the bounded follow-up described in `NEXT_STEPS.md`. Review covered serialized schemas, artifact hashing, ECID/profile semantics, replay behavior, action-ledger crash handling, tests, and the proposed durable publication boundary.

## Defects found in the inherited repo

### 1. Historical v0.1 profile order could be treated as equivalent

The retained in-memory `Catalog` compared overlay sets for `reuse` and sorted artifacts when building its ECID. Because the simulator's operations are ordered, `A,B` and `B,A` must not be treated as the same computation. The 001A serialized `Bundle` path already enforced exact order, so this did not invalidate 001A results; the historical regression path was corrected and a regression test added.

### 2. Initial 001B resume path needed authorization re-check

During development of 001B, a PREPARED/STAGED attempt could have been resumed after a crash without rechecking the simulated `authorized` flag. This was corrected before handoff. Any unpublished attempt now requires authorization on resume; PUBLISHED state is read-only/idempotent.

### 3. COMMITTED status alone was weaker than the recovery claim

The inherited action replay gate rejected PENDING/UNCERTAIN but did not prove a COMMITTED row's receipt matched the deterministic request receipt and local mock-world evidence. Recovery-safe verification now checks both ledger receipt content and the authoritative mock-world receipt.

### 4. Development-only 001B demo included an unrelated mock action

An early 001B demo run produced `effect_count = 2` because it also executed the historical 001A marker. That unrelated action was removed. The final 001B demo contains one task-local mock action and reports `effect_count = 1`.

## 001B invariants reviewed

- Source checkpoint remains the published current state while an attempt is PREPARED or STAGED.
- A staged checkpoint is content-addressed and hash/body validated before use.
- Target publication and attempt PUBLISHED state are committed in one SQLite transaction.
- The publication transaction compares the current source hash with the attempt's prepared source hash before switching.
- Recovery binds source hash/ECID/profile, target ECID/profile, portable input descriptor, and verified committed task action keys.
- Changes to the task action-key set after PREPARED fail the attempt rather than silently changing replay assumptions.
- Unresolved actions block attempt preparation/recovery.
- Failed attempts leave the source current pointer unchanged.
- Process crashes after prepare, after compute, after stage, and after publish have explicit restart behavior.
- Already committed mock effects are not executed twice by recovery or repeated action submission.

## Verification performed

- Full `unittest` discovery: 56/56 pass.
- 001A demo: PASS.
- 001B demo: PASS.
- Four action-ledger child-process crash windows retained from 001A.
- Four durable-publication child-process crash windows added in 001B.
- Clean extracted handoff ZIP is tested again before delivery.

## Claims deliberately not made

This audit does not establish multi-runner concurrency safety, arbitrary power-loss durability, real external exactly-once actions, hostile privileged-tamper resistance, signed qualification evidence, neural overlay compatibility, model quality, identity continuity, HSA/MSA, recurrent depth, or DARP behavior.

## Verdict

**PASS for the bounded single-runner deterministic 001B simulator and its stated process-crash model.** The repo remains a contract/recovery implementation seed, not a neural NSS runtime.
