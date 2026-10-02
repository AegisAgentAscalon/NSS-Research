# Recovery Experiments 001A/001B contracts

## Serialized boundaries

The shipped JSON Schemas specify manifest, artifact descriptor, overlay, profile, directed transition, integer operation, portable inputs, action record, checkpoint, and recovery-attempt structures. Fields are required and unknown fields are rejected. Duplicate JSON keys, non-finite numbers, wrong types including bool-as-integer, invalid enums/hashes, missing evidence references, duplicate IDs, dependency/exclusion violations, and unqualified combinations fail validation.

`Bundle` reads the manifest, checks semantic relationships, then reads artifact bytes and checks SHA-256 before parsing their operation schema. Artifact paths must resolve within the fixture directory. Used artifact bytes are checked again during computation, so later file tampering is detected. This is local integrity checking, not signature validation or protection against a privileged actor editing code/manifests together.

Every generation has a Core-only profile. Overlay execution order is explicit; dependencies must precede dependents. The 001A/001B ECID hashes the full validated manifest plus selected profile and ECID schema ID. This conservatively changes ECID even for inactive-manifest changes. It binds ordered composition, Core/overlay byte hashes, profile/transition definitions, ABI labels, and the declared runtime version. It does not hash the Python interpreter or runtime source code; those remain trusted versioned implementation inputs.

## Deterministic computation and replay

Core computes `2*x + 1`; A computes `3*x + 4`; B adds 7. B requires A. For portable inputs `[-3, 0, 2, 11]`, AB produces `[-4, 14, 26, 80]`, A produces `[-11, 7, 19, 73]`, and Core-only produces `[-5, 1, 5, 23]`.

Checkpoint JSON carries task ID, profile, ECID, hashed portable input descriptor, cached values, and unfinished draft. Cache acceptance checks governing ECID/profile and recomputes expected values to detect poisoned cache contents. Recovery validates source state, a qualified directed edge, simulated authorization, unresolved action records, and target load before producing target state. Replay reads portable inputs and computes from scratch; the abandoned draft is cleared.

Transition fixtures explicitly contain source, destination, state-reuse policy, invalidation fields, replay requirement, failure destination, and test evidence reference. `AB -> A` and `A -> core` replay; `A -> A` reuses identical state. Reverse transitions and direct `AB -> core` are not implicit.

## Durable local action protocol

One runner owns a ledger directory; do not open a second live runner until the first has exited. SQLite transactions with `synchronous=FULL` store action JSON; a separate SQLite mock-world file stores effect receipts. The inserted mock-world row IS the external effect modeled here. There are no real external tools.

- `PENDING`: intent is durably recorded; no effect is yet confirmed.
- `UNCERTAIN`: written before invoking the mock executor, and retained if the process exits before confirmation. Abandoned PENDING rows become UNCERTAIN on restart.
- `COMMITTED`: confirmed receipt is durably recorded; subsequent requests with the same key/task/payload return it without calling the executor.

The key is globally unique within a ledger. Reusing it with a different task or payload is a conflict. Replay-safe verification now requires all task actions to be COMMITTED, the ledger receipt to equal the deterministic expected receipt, and the authoritative mock-world receipt to exist and match. Missing or contradictory evidence fails closed.

Explicit reconciliation consults authoritative mock receipts: an existing receipt commits the ledger record; proven absence resets it to PENDING for an explicit retry. Reconciliation alone does not execute the action. Unknown real-world outcomes would have to remain uncertain; absence is authoritative only in this controlled local mock.

## 001B durable recovery-attempt and publication protocol

`RecoveryStore` is also single-runner. It stores:
- immutable content-addressed checkpoint bodies keyed by canonical checkpoint SHA-256;
- a per-task `current` pointer to the published checkpoint;
- durable recovery-attempt records.

An attempt binds:
- `attempt_id` and `task_id`;
- source checkpoint hash, source profile, and source ECID;
- target profile and target ECID;
- the portable input artifact descriptor;
- the sorted verified committed action keys present when the attempt is prepared;
- PREPARED / STAGED / PUBLISHED / FAILED status and checkpoint/failure references.

Publication sequence:
1. Validate current source, qualified directed edge, authorization, target ECID, portable inputs, and replay-safe committed action evidence.
2. Persist PREPARED attempt while source remains current.
3. Compute the target from portable inputs. A process crash here leaves PREPARED; restart recomputes.
4. Persist target checkpoint content-addressed and mark attempt STAGED. Source remains current. A process crash here resumes from staged state after semantic revalidation.
5. In one SQLite transaction, compare current source hash with the attempt's source hash, update current pointer to staged target, and mark attempt PUBLISHED. A crash after commit observes both target-current and PUBLISHED; it does not observe only one.

Before recompute or publish, the runtime rechecks the exact source hash/ECID/profile, portable input descriptor, target ECID, authorization, and verified committed action-key set. If the published source or task action set changed, the attempt fails rather than overwriting newer state. A failed attempt never changes the current pointer.

The 001B store fails closed if a surviving non-empty recovery directory is missing its database, if stored checkpoint hash/body disagree, if attempt semantics are invalid, or if SQLite data is corrupt. Total loss of an entire directory/device remains outside this local experiment.

## Proof boundary

001A tests process termination after durable action PENDING, after UNCERTAIN but before effect, after effect but before ledger commit, and after ledger commit.

001B additionally tests process termination after recovery PREPARED, after target computation but before staging, after durable STAGED, and after atomic PUBLISHED commit. Tests verify source retention before publication, exact clean-run equality after recovery, current-pointer compare-and-swap, action-set binding, authorization on resume, receipt integrity, and no duplicate committed mock effect.

`authorized` and `load_ok` remain simulation inputs. Metadata/test evidence is not neural qualification. No neural modules, training, real deployment, memory subsystem, HSA/MSA, recurrent depth, DARP, multi-runner fencing, or real external executor was added.

## 0.4.1 recovery boundary corrections

Unpublished recovery resumes recheck directed qualification, exact source/target identities, current source, inputs, action set and target load before publication. A failed STAGED load retains current source. A successful reuse reports `replayed=False`; a replay transition reports its replay policy. Re-reading PUBLISHED returns that historical immutable checkpoint with `replayed=False`, leaves the current pointer unchanged, and does not constitute fresh activation or fresh authorization.

The public durable-recovery boundary returns typed ContractError outcomes, with current state when readable or None when missing/corrupt. Low-level RecoveryStore methods are storage primitives, not authorization APIs. Current pointers must refer to the same task; prepared inputs must equal source inputs; staged task/profile/ECID/input bindings are rechecked before publication. Arbitrary SQLite/OS exceptions and adversarial database rewriting are outside this modeled guarantee.

Atlas schema v2 adds implementation status and allowed terminal outcome lists. Success terminals allow only SUCCESS; failure sinks preserve the actual declared non-success code. TRY unwraps only successful child results; helper failures are implicit exits. Structural complexity E - N + T + 1 excludes those implicit exits and is not an implementation bound. Forbidden-edge strings are design constraints, not executable dependency checks.


## StageHandoff001 / v0.4.2 additive extension
Use `docs/STAGE_HANDOFF_001.md` for checkpoint/attempt v2 and portable TaskRecord
semantics. Version-1 default APIs remain compatible. CONTROL/EVALUATION stages
require Core-only. Current TaskRecord and configuration share the same checkpoint
publication transaction; no independent record-current pointer exists.
