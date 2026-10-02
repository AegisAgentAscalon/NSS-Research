# NeuralProbe001 — public contract and operating guide

## Public entry points
`neural_contracts.protocol(document)` validates a fixed, bounded numerical plan.
`ProbeData.create(path)` explicitly constructs synthetic archive/review/snapshot
fixtures; `gate()` checks exact current source/codec/selection; `read(split)` returns
actual pair training data through the public DatasetSnapshots consumer.
`train_trial(protocol,seed,precision,train_pairs,test_pairs,gate)` trains the bounded
model and returns measurements and JSON tensors, never deployment permission.
`ProbeRuns.prepare(id,plan)` and `finalize(id,report)` journal local evidence.
`execute(store,id,plan,data,ledger)` enforces identity, current use and bounded run.
`verify_numerics(record,data)` recomputes scores from exact checkpoint tensors.
`NeuralSession` checks real activation caches and rebuilds only through prescribed
Catalog transitions and Ledger.ensure_replay_safe. The native runtime is not replaced.

## Schemas and failure semantics
All JSON is finite, bounded2MiB, max nesting20, exact known fields; duplicate keys
are rejected by the existing strict decoder. Checkpoints have schema1, fixed
architecture ID, kind, mode/rank metadata, float32 tensor shape/value arrays. No
pickle/importable code. Numeric schema uses the new pure validator, not the older
integer-only checker. Entire backend is a reviewed hardcoded implementation.

Plan binds protocol, dataset manifest, exact codec/test bytes, all installed
nss_base source hashes, Python/PyTorch/platform and CPU numerical policy. Record ID
binds one immutable plan. Report binds all Core/overlay/joint/A2 artifacts, seeds,
training losses/update counts, metrics, numerical recovery results, limits and NONE
authority. FINALIZED report+receipt is atomic. PREPARED has neither verdict nor score.
An exact retry after source withdrawal returns historical evidence; current-use
validation still fails. Resume from PREPARED reruns training from scratch using
pinned seeds/inputs after fresh permission and implementation checks.

ContractError codes include VALIDATION_FAILED, INCOMPATIBLE_CONFIGURATION,
CONSTRAINT_CONFLICT, TRAINING_RESTRICTED, RECOVERY_REQUIRED, INSUFFICIENT_EVIDENCE,
AUTHORIZATION_DENIED, INTERNAL_FAILURE and BUDGET_EXHAUSTED. A valid numerical
outcome can be PASS, FAIL or INCONCLUSIVE. An I/O/contract/permission error does not
invent a numerical verdict. No claim is made that training always improves a task.

## Exact task and controls
16 symbols, sequence length2, one-hot codec. 128train/64validation/64test disjoint
pairs partitioned by (i+j)%4. Every atomic symbol is present in training; this is
combinatorial pair holdout with a strong factorized inductive bias, not unseen
concepts. Training uses full-batch MSE, no validation-driven stopping or seed selection.
Core learns identity; auxiliary block identity loss anchors the interface.
A swaps0/1 and2/3 at block1. B swaps1/2 and3/4 at block2. Combined target is B(A(x)).
A2 adds swap5/6; old B unchanged. Retention checks exclude5/6 deliberately changed
by the new intended behavior. Exact old artifacts are preserved rather than rewritten.

Core:512parameters; A and B:128 each, rank4. One rank8 joint control:256parameters,
700updates versus350+350, identical input presentations but direct composed labels.
Matching params/steps/examples does not match supervision, FLOPs or wall-clock cost.
Comparison demonstrates a control works; no advantage is inferred from a tie.
Thresholds: >=95% pair accuracy for Core/A/B/AB/joint/A2B/retained domain, AB at least
10percentage points above each single-overlay/disabled ablation. Stored metrics
are recomputed by the same implementation, not a separate learned/independent judge.

## Numerical precision and reproducibility
CPUfloat32; single thread; deterministic PyTorch; fixed seeds. RNG/thread/determinism
settings are restored. Ternary Core forward uses unit-scale clamp+round with an STE;
float32 master weights, overlays and arithmetic remain. No packing, BitLinear,
activation quantization, 1.58bit memory or energy claim. Fresh Core initialization
and two losses distinguish this from manually installing the answer in its weights.
Architecture still deliberately supplies a simple identity-friendly factorization.

Neural recovery tags real output activations, not Transformer KV. AB->A invalidates
source cache and draft, rebuilds bound inputs, compares clean A, then A->CORE.
Reverse A->AB is not implicitly granted. Denial and load failure retain source.
Neural state is ephemeral; durable publication applies to experiment reports, while
existing001B retains its own integer/state publication tests. Native neural state
publication requires another explicit backend contract.

## Limitations
Local single worker; CPU-only test. No autonomous Builder, learned evaluator/router,
real protected benchmark, signed/authenticated Nexus authority, released generations,
production hot/cold paging, generalized context/memory retrieval, privacy/security
sandbox, concurrency, language/personality, DARP/recurrence/HSA/MSA or multimodal model.
Data rights are explicit fixture attestations, not a legal review. Permission checks
are point in time, not leases. Already used/exported bytes and learned weights cannot
be recalled by revoking a source. No model/dataset downloads or private data used.

## Primary reference material
Implementation uses local PyTorch2.10.0+cpu. Reference patterns, not unearned claims:
- PyTorch autograd mechanics: https://docs.pytorch.org/docs/2.10/notes/autograd.html
- PyTorch reproducibility limits: https://docs.pytorch.org/docs/2.10/notes/randomness.html
- LoRA initialization/frozen base: https://huggingface.co/docs/peft/en/package_reference/lora
- Native ternary differs from this reference: https://arxiv.org/abs/2402.17764

No assertion here relies on this probe reproducing those papers' results.
