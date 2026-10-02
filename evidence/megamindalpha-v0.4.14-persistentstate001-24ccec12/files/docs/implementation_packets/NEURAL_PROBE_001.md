# NeuralProbe001: approved bounded experiment contract

## Scope and explicit opt-in
User requested the next actual neural experiment. v0.4.5 permitted this ONLY with
a separate backend/checker contract. This document defines that boundary. Do not
reinterpret the integer evaluation checker or claim its scores judge neural weights.

## Experimental question and prescribed topology
Can two trained low-rank parameter additions to a frozen, trained two-block neural
transducer execute a prescribed composition on held-out pairs, preserve old artifacts,
and reject/rebuild configuration-specific neural state? This deliberately favorable
LINEAR, token-wise task is a wiring/training smoke test, NOT an LLM, reasoning,
learned routing, task decomposition, learned evaluator, neural novelty or scalability proof.
Width 16; input two one-hot symbols; two learned 16x16 blocks, no bias/activation.
The Core learns the identity map, with intermediate identity supervision to anchor
the interface. A rank-4 update attaches to block 1; B rank-4 to block 2.
A learns swaps (0,1),(2,3); B learns (1,2),(3,4). AB must implement B(A(x)); order
matters. Gen2 adds swap (5,6) to A, retaining B exactly. New A is trained from scratch.
Core training is allowed only before freeze; all accepted weights stay immutable.

## Data / evaluation
All 256 ordered pairs of 16 symbols: test when (i+j)%4=0, validation when =1,
training otherwise. No exact input pair crosses splits; ALL individual symbols
are seen in training. This strongly factorized task supports easy generalization;
held-out pairs do not demonstrate new concepts. Data generator/targets are source
code, not a protected exam. Validation is not used for early stopping or selection.
One joint rank-8 adapter at block 2 is trained directly on AB for twice as many
updates as each specialist. It matches total trainable parameters, update count
and input-token presentations, but receives DIRECT COMPOSED TARGETS whereas A/B
see separate targets. It is a diagnostic baseline, not a causal comparison of
training methods or FLOPs. No result is called a modular performance advantage.

## Numerical policy
CPU float32 and single-thread deterministic PyTorch. Ternary mode uses clamp+round
with a straight-through gradient on the Core, fixed scale 1; overlays remain fp32.
This is a NUMERICAL TERNARY REFERENCE, NOT BitNet, NOT all-ternary overlays, NOT a
packed kernel or low-energy demonstration. Stored trainable master matrices remain
float32. A float32 control isolates numerical failures. Tolerances pinned in protocol.
Zero-up initialization must be a no-op. Frozen state hashes include every tensor.
No torch.load/pickle, remote code, callbacks, model/dataset downloads or arbitrary
backend names. Checkpoints are bounded JSON tensors for a hard-coded architecture.

## Owners / forbidden edges
neural_contracts: bounded pure contracts, deterministic data/mapping definitions.
neural_backend: optional torch, model/training/checkpoint logic only; no SQL/tools.
neural_data: public ExperienceArchive/DatasetSnapshots intake and current-use reads.
neural_execution: experimental cache/configuration checks; existing Catalog/Ledger.
neural_records: own local numerical experiment journal/artifacts, no runtime pointer.
neuralprobe001: explicit CLI/lab coordination; never deploys or mutates runtime.
Every new import is declared; no inherited module may depend on the probe.

## Inputs / outputs / invariants
Exact protocol + code fingerprint + CPU/library environment + codec + fixed dataset
manifest; outputs frozen Core/overlay/joint/gen2 JSON artifacts, exact metrics,
training-update accounting, numerical verdict and historical receipt. PASS means
ONLY declared smoke-test criteria. All results have authority NONE.
Public errors are ContractError codes; inaccessible or changed training data stop
the run without a fabricated score. Pure replay is from pinned seeds/inputs, not
re-execution of an external action. PREPARED attempts may restart training from
scratch after crash; FINALIZED retries return history, not permission to reuse data.
Runtime stage state and integer evaluation records must remain unchanged.

## Acceptance and failure cases
Structural: zero no-op; core/old overlays byte unchanged; only optimizer-owned
candidate parameters update; exact pair split; one profile per forward execution;
no arbitrary profile union; explicit directed transitions; stale cache rejected;
clean target equivalence under declared tolerances; committed action count remains1.
Numerical: >=95% Core-only, A, B, AB, joint and Gen2 accuracy; AB ablation gap>=10pp;
retained-domain Gen2 >=95%. Report measurements even if criteria FAIL. Exhausted
predeclared optimizer budget produces INCONCLUSIVE, not passing reduced work.
Current data gate before/between phases, every 25 updates and before final publish.
This is point-in-time revocation, not an asynchronous lease or model unlearning.

## Evidence discipline
Pilot used seeds11,29,47 to test feasibility; those are not reported confirmation
seeds. Final protocol uses101,211,307 and is pinned before confirmation. The task
and thresholds are developer-designed, not externally preregistered/blinded.
No test-count inflation is evidence of neural generality. No new native Runtime,
protected evaluator, qualification issuer, trained policy or self-training claim.
