# NeuralProbe001 — implementation and experimental audit

## Scope / source
Input: complete0.4.5 EvaluationRun001 ZIP; SHA256
be2778e6daf79d166df82ca10b847460d25cfbdddc5b083fc6ffd58b91441b6e.
Reproduced all13 inherited gates (404 tests) before changes. All28 inherited runtime
Python files and27 inherited test files remain byte-identical. Six new owned modules
and three new test files implement the optional numerical probe. Docs, dependency
allowlist, release checks, protocol and three subordinate logic diagrams were added.
Parent25-flow Atlas and historical DOCX artifacts remain unchanged.

## Reviewed boundaries
- Trained Core tensors freeze before candidate training. Optimizers receive only
  intended candidate parameters. No-op initialization and gradient flow through
  frozen downstream weights are tested. Core/old A/B exact hashes are rechecked.
- Generation2 is a new A2 candidate with exact B reuse; no Core successor, production
  generation manager, qualification authority or deployment occurs.
- Actual synthetic training pairs flow through public ExperienceArchive and
  DatasetSnapshots reads. Review permissions stay separate. Current gates recur
  during training and before finalization; history remains inspectable after withdrawal.
- Numerical schema/checker is separate from integer evaluation. Data-only bounded
  JSON checkpoints use a fixed architecture/shape whitelist; no pickle, eval, torch.load,
  remote executable models or arbitrary callbacks in JSON.
- Real activation states carry profile, code/environment-bound ECID, task and input
  identity. Stale caches are rejected. Allowed transitions use existing Catalog rules.
  Same task cannot adopt substituted inputs even with a new digest/cache.
- Existing Ledger checks keep committed effects single-use. No replay executor is
  called by neural recovery. Explicit simulated approval is NOT Nexus authority.
- Numerical journal owns reports, not a runtime active pointer. PREPARED/FINALIZED
  and report/receipt publication are transactional. Historical retries grant no use.
- Inherited reference tests are not edited to increase success rates. New negative
  tests exercise malformed plans, tensors, identity, ownership, permission, scores,
  receipts, attempts, recovery, source substitution and numerical budget exhaustion.

## Tests and experiments actually run before packaging
498 tests PASS =404 inherited +94 new. Four new child-process crash/restart tests:
after preparation, after neural training, before publication commit, after commit.
All crash continuations preserve attempt semantics and one mock effect.

Six confirmation trials, seeds101/211/307 × fp32/ternary_core_reference. All pass the
frozen protocol. Core-only identity, A, B, AB, joint baseline, A2B and retained domain
reach100% pair accuracy on their relevant held-out cases. On the AB task, removing A
reduces accuracy to56.25%; removing B to57.8125%; removing both to48.4375%. All neural
recovery comparisons equal clean-target inference exactly locally (max abs error0).
Exact raw protocol/plan/metrics/checkpoint tensors are attached; RESULTS.md explains
what those percentages do and do not establish. Local elapsed time is recorded,
not advertised as an energy or execution-speed advantage.

## Scientific and implementation limitations
The task is token-wise linear and every atomic symbol appears in training; only
pairs are held out. The prescribed slots/auxiliary identity targets make composition
particularly easy. The joint baseline also100%; no modular advantage is established.
Three seeds × two numerical modes are NOT broad independent benchmark evidence.

Ternary reference uses quantized Core values but fp32 math/master weights/overlays.
Not BitNet, a packed1.58bit backend, language intelligence, a personality Core, learned
routing/evaluation, native recurrent reasoning or a scalable memory demonstration.
No end-to-end production hot/cold loading, concurrency or independent authority.

Neural state recovery is ephemeral. Durable existing001B remains an integer backend;
only the new numerical evidence is durably published. A native neural RecoveryStore
adapter requires a separate versioned contract, not a hidden schema reinterpretation.

Local trusted operator, scripted human attestations, source hashes—not authenticity
or legal rights proof. Current use checks are point-in-time, not a cross-store lease.
They cannot recall exported/previously consumed data or remove learned weights.
Journal hashes detect mismatches but not hostile rewriting of the entire evidence
store. Numerical score recomputation uses the same local implementation, not an
independent learned judge. Dependency checking is static, not a security sandbox.

Existing SQLite fixture ResourceWarning is still visible in the full inherited suite.
New numerical corruption tests explicitly close their connections. The release is
not described as warning-free. Read final fresh-extracted verification outside the
ZIP for actual gate results; packaging alone is not a conceptual "PASS" for NSS.

## Status
Software: tested bounded numerical laboratory; source-compatible inherited services.
Neural evidence: positive prescribed linear-composition smoke test, no scale claim.
Production readiness, qualification/authorization and full NSS: NOT established.
See SYSTEM_INVENTORY.md and NEXT_STEPS.md for separately scoped remaining work.
