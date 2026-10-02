# CM-02 reference continuity and freshness — proposed protocol v0.2

**Status: protocol review only.** No experiment implementation, case generation, model loading, inference or training has occurred. This document makes proposed design choices; it is not user execution authorization or an executable source lock. It replaces the Codex v0.1 *proposal*, not CM-01/Q010 evidence. See REVIEW.md for the substantive critique and changes.

## 1. Question and boundary

Does a small resident public-reference workspace preserve the appropriate task binding across an evolving catalogue, and what does it cost relative to an ordinary maintained selection index? Distinguish reference retention, safe stale-reference detection, current-content retrieval, and hidden-intent correctness. These frozen readers have no native persistent learned hidden state. There is no nominal “state-off” arm, learned token interpretation, new training, Forge/Runtime integration or NSS role replacement.

The participating frozen Primary, task/learning Secondary, predictive/reflection Tertiary with Secondary/Tertiary mutual exclusion, and frozen fallible advisory Validator remain architectural background, not implemented experimental participants. The deterministic experiment manager is not a replacement Validator.

## 2. Inputs, host and numerical boundary

SOURCE_IDENTITIES.json binds the supplied Codex proposal, CM-01 v0.2 and Q010 v1.6 recovery archives. Both historical dependency archives are present and their complete manifest payloads were hashed in this review: 628 CM-01 and 5,449 Q010 entries. This is integrity checking, not experimental replication. FROZEN_EXPORT_IDENTITIES.json identifies all fifteen unchanged exports; only the five near readers (1201–1205) participate in future inference. The retained loader may materialize other roles during its original export-binding audit; they receive no experimental forward calls. Do not alter its scientific binding checks merely to avoid that overhead.

Keep float32 K/V/Q, bool validity, the one-stage reader, catalogue-assisted resolver/decoder, and frozen Q010 thresholds unchanged. Preserve the frozen verifier and the separately reconstructed underflow amendment (final probability bound adds 2^-126). Historical original-v2 source/failed-row, optimizer/RNG and raw training-trace gaps remain gaps. The compact recovery is not full original raw evidence.

Observed review host: Linux x86-64; Python 3.13.5; NumPy 2.3.5; CPU-only PyTorch 2.10.0; five visible/affinity CPUs but four CPU-equivalents of cgroup quota; **4 GiB container-wide memory limit**. No GPU is assumed. No torch runtime, model or project experiment module was imported in this review. Numerical compatibility remains for a future authorized fixture, not inferred from package versions. ENVIRONMENT.json records the exact observation.

## 3. Arms and state semantics

| Arm | Retained information and operation |
|---|---|
| **W — workspace** | Full observed journal, current-record and binding archives, current task/scope, and exactly two 56-byte UTF8_BYTE_V1 packets, one per task. Store task ID → 56-character ASCII string; no uncounted shadow structured/latest-selection table. Decode transiently and count its peak cost. |
| **I — maintained index** | The same journal, archive and task/scope, with a two-entry dictionary from task ID to an immutable six-field tuple `(version, scope, handle, revision, binding_event, operation)`. These are the same semantic fields, not a verbose explanatory dictionary. No serialized packet. Count its actual representation and updates. |
| **O — no retained selection** | Current numerical K/V/valid, resolver catalogue, Q and public current task/scope. It deliberately discards selection history; use the unchanged original-Q path. It is an information-removal ablation, not an equal-information competitor. |

W/I observe and update at every committed event. Selection/correction updates only the addressed task. A switch preserves both task entries. A conflict marks that task unresolved (H); it does not silently choose a winner. Revision/deletion updates the shared record/archive but does **not** rewrite a selected packet/table entry. At a query, an R reference validates current task/scope, its binding event, active record and exact revision. Valid => previously observed canonical key. Stale/deleted/cross-scope/detectably inconsistent => management abstention. Unselected/unresolved => original Q. No route supplies an expected answer to the learned reader. Queries never refresh or invalidate the entries; this fixes the next-query semantics. W and I must agree on all routes, not just successful queries.

All state starts empty before each sequence's public registration prelude; no state carries between sequences/families. There is **no interruption/reset intervention inside these sequences**. Each saved model seed starts from the same captured public history; there is no model state to preserve between endpoints. Replay starts from empty controller states and an empty inference cache. Any real learned-state removal experiment needs a separate defined architecture.

## 4. Non-neural controls and an important policy distinction

**X_W and X_I** fetch the observed payload only when W/I's pinned-revision binding validates; otherwise UNKNOWN, with no fuzzy fallback. **X_S** reconstructs records and selection state from the complete *observed prefix* without retaining a latest-selection index, then applies the same pinned policy and exact read. The scan is a route/cost reference, not the primary competing retrieval arm. Charge its scan visits and transient reconstruction memory.

**Review addition: X_latest**, a separately labelled stronger retrieval-policy diagnostic. A selection identifies a continuing entity for a *current-content* question. Its maintained public index may follow a contiguous observed revision chain for that same scope/handle, provided the entity was not deleted, its key is unchanged, and no later selection/conflict supersedes the binding. It may then return the current observed payload. Deletion => UNKNOWN; unresolved selection/conflict => UNKNOWN. It cannot repair a change of intended entity without a public correction. It uses exactly the same public events, no hidden ledger, and all its indexing/validation costs count.

This control does **not** change W/I's symmetric pinned-revision policy. It exposes the cost of that conservative policy: at F:16, a refusal by W/I is safe under their version contract but loses a known current answer that the observed revision may make available to ordinary retrieval. Report current-entity and pinned-revision policies separately; neither policy difference nor X_latest's result is evidence of neural superiority. No privileged exact-owner control is added in this pass.

## 5. Chronological data and exact checkpoints

Use three development and five held-out families, **four sequences per family**, each with one distinct sixteen-record catalogue and two task scopes. Families stay intact across the split. Every sequence has a charged prelude of 16 registrations plus one activation of task A, followed by **events 0–64 inclusive**. Queries occur **after** events 0, 8, 16, 32, 48 and 64. There are 32 sequences / 192 query occasions: development 12/72; held out 20/120. Five model seeds repeat these observations; they do not create 960 independent episodes.

EVENT_TEMPLATES.json gives all 65 symbolic event positions for each template. It contains no generated catalogue, handle, Q or episode input. The principal checkpoints are:

| Template | 0 | 8 | 16 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|
| **D: delay/switch** | Select/query A | Query B | Query A | Query B | Query A | Query A after 64 post-selection transitions |
| **F: freshness** | Select/query A | Query B | Revise A; pinned binding stale, current answer exists | Explicitly reselect current A | Delete A; correct UNKNOWN | Correct selection to replacement C |
| **C: correction/conflict** | Select/query A | Query B | Correct to C | Conflict C/D; original-Q fallback | Resolve to D | Query D after further events |
| **N: no-cue intent** | Select/query A | Query B | Publicly select A-decoy; hidden intent remains A | Same wrong public binding | Observable correction to A | Query corrected A |

Common switches and other-task reselections are explicitly listed in the JSON. All remaining positions revise a rotating *non-target* background record. D never changes or reselects A after event 0. Sequences therefore do not combine an unchanged-target long-delay claim with an incompatible target mutation. Each event commits before a query. The current task/scope follows only observed switch/activation events, not hidden query labels.

**Absence allocation:** F:48 is the eight main deleted-target occasions (five held out). Revised records at F:16 are still known. Conflict does not magically make an existing intended record absent. There are no genuinely novel/unregistered main-query strata in this protocol; do not extrapolate to them.

**No-cue diagnostics:** N:16 and N:32 have a scorer-only alternate intent A-decoy under byte-identical public input, in addition to main intent A. Initial payloads for A and A-decoy must be different by the frozen construction. These 16 main alternate-label records reuse outputs; they are not new query occasions. Report semantic intent errors separately from valid public binding. For two equally weighted distinct answer labels on identical inputs, a deterministic single answer cannot get both right; do not assume a reader necessarily returns either label.

## 6. Catalogue and query recipe (a new CM-02 source contract)

Use the pinned Q010 `make_case` source once per sequence, path_length=allowed_depth=1, missing=False, near_treatment=False. Preserve its seeded physical row order and base truth edges. This reuses a generator primitive, not Q010's old evaluation contract.

Role A is the generated source slot; A-decoy is its reserved unrelated decoy slot. Choose C, C-decoy, D, D-decoy and B in that order from ascending remaining slots. The other nine slots are the background pool. A/C/D and their decoys share task-A scope. B and the background pool share task-B scope. Both scopes live in one sixteen-record numerical catalogue. This uneven namespace allocation is intentional; do not describe it as a balanced scope benchmark.

Before registration, place each A/C/D decoy at normalized(anchor + Gaussian sigma 0.01), using its separately allocated close seed; all affected keys/values are recomputed consistently from the same book. B is an unmodified-code control, not a guaranteed distance-separated sample. No norm/distance selection is allowed after generation. An exact code/identifier collision or nonfinite input stops preparation rather than silently resampling. All decoy payload relationships initially retain the Q010 graph's destinations; A and A-decoy destinations are distinct in that source.

Each revision increments that record's revision by one and replaces its destination with (old destination + 1) mod 16; its key/handle do not change. Delete clears the readable row, leaving the code catalogue available to the unchanged decoder; no handle reuse or resurrection. Numerical snapshots must be derived from observed registration/revision/deletion facts, with a public-key-to-row mapping charged to the shared store. Protected owner/origin arrays cannot be used by reference selection.

For a known query, normalize its declared anchor's first 16 coordinates plus Gaussian noise; append a zero final coordinate, retaining float32 as in CM-01. For a deleted target use its same retained identity code but score UNKNOWN. At each checkpoint, sigma is 0.01 when (family_index + template_index + checkpoint_index) is even, otherwise 0.2. Development indices are 0–2; held-out 3–7; template indices D/F/C/N = 0/1/2/3; checkpoint indices 0–5. This gives 12 low/12 high occasions in each family, with both levels at every checkpoint across templates. Individual held-out cells may be 2/3 rather than evenly split; publish exact denominators. A-family queries are deliberately close-key cases; B provides the unmodified controls. Do not claim a fully factorial geometry-by-event study.

IDs are opaque and independent of answers. Define identifier digest input as ASCII `CM02-ID-v0.2|{identifiers_seed:016x}|{domain}|{ordinal:04d}`, with domains `scope`, `task`, and `handle`. Scope/task ordinals 0/1 designate A/B. Sort catalogue slots by SHA256 of ASCII `CM02-ORDER-v0.2|{identifiers_seed:016x}|{slot:04d}` for prelude order; allocate handle ordinal j to the jth registered record, never from its destination label. Event IDs use SHA256 of ASCII `CM02-EVT-v0.2|{event_ids_seed:016x}|{ordinal:04d}`: prelude ordinals 0–16, stream event e ordinal 17+e. Interpret the first four digest bytes for scopes and first eight for all other IDs, unsigned big-endian. Zero or in-sequence collisions stop rather than retry. All normal draws use NumPy PCG64 with the allocated component seed and pinned code/version. Query seeds are separate per checkpoint. Actual byte recipes and source files must be locked before any future fixture or main generation; a changed recipe needs a new proposal version.

## 7. Seeds and causal isolation

SEEDS.json fixes **477 numeric allocations**: nine family roots plus four sequence templates × thirteen components × nine families (including fixture). Derivation is the first eight SHA256 bytes of `NSS-CM02-PROPOSED-v0.2/label`, unsigned big-endian. No random draws were made to allocate them.

| Family | Root seed |
|---|---:|
| CM02FIX-00 | 5284268149507718224 |
| CM02DEV-01 | 17041418255721657702 |
| CM02DEV-02 | 12423799792484694887 |
| CM02DEV-03 | 17092062939750857967 |
| CM02EVAL-01 | 16182677361569377033 |
| CM02EVAL-02 | 12910080344494802580 |
| CM02EVAL-03 | 4717430182628008674 |
| CM02EVAL-04 | 13591005417275647016 |
| CM02EVAL-05 | 9240015711776059539 |

The audit scanned 5,217 available text/source/record members, including both historical dependencies, current/older plans and Q010-P1 reservations; no proposed numeric seed or namespace collision was found. Missing historical RNG histories and unmaterialized derived seeds cannot be audited. Different seeds alone do not prove PRNG independence or future dataset disjointness. Retain the audit scope and check actual generated catalogue/public-stream identities against available earlier evidence in future preparation; do not reject difficult outcomes.

Only the generator/scorer may read templates, seeds, source identity, future events and expected answers. Controllers/readers receive an opaque episode identity, current numerical input, public context and events through the current prefix. Keep future prefixes and protected metadata outside their input files/process interface. Changing a future suffix or hidden intent while retaining the observed prefix must leave W/I/O routing and past outputs unchanged. These are testable isolation checks, not a claimed formal security proof. A canonical reference must trace to an already observed event, not the expected answer.

## 8. Evaluation rules and cost interpretation

An independent scorer reconstructs the chronological store and task-binding truth without importing producer/manager logic. Score separately: observable binding validity/relevance; hidden-intent binding; exact content; management abstention on known (safe-but-lost recall); correct deletion UNKNOWN; and whole-map integrity. Learned answer errors, no-cue hidden-intent errors and expected conservative refusals remain complete negative evidence.

For this bounded engineering screen, require zero observable invalid-binding acceptances, zero W/I route/context disagreements, zero pinned-policy scan disagreements, zero prefix/label isolation errors and exact fresh replay. An unexpected failure stops the run and makes it incomplete—not a pass on the remaining denominator. No-cue hidden disagreement is **not** an observable-safety stop. Emit the failure before stopping and retain all completed records. No post-held-out fix-and-continue under the same version.

Report every sequence/family/seed/checkpoint, then within-family paired W–I and W–O differences. No new recall-gain threshold is fitted, and CM-01's +27 points is not a target. W–O differences measure retained-information benefit only. Keep the five held-out families as the generalization units; no IID confidence interval over repeated models/checkpoints.

There is no blanket efficiency PASS. At complete route/safety parity, a particular integer resource metric lower for W than I in at least four of five held-out family summaries supports only an implementation-specific improvement in that named metric. Report magnitudes and all opposing cost changes. Runtime is descriptive, not a speedup qualification in this small sample. A tie or index advantage is valid and does not invalidate the general supporting-context idea.

Account for persistent and peak transient memory, journal, current records, historical bindings, task entries, store row mapping, K/V, catalogue, Q, controller metadata and cache. Report the **whole unique object graph once per arm** alongside canonical serialized bytes and packed semantic-field lower bounds; do not sum separately measured objects that share memory. The experimental inference cache is audit machinery, not free deployed memory. Charge prelude construction, every event update, query decode, index reads, record validation, scan reconstruction, exact lookup, returned bytes and bytes rewritten. Do not charge W's neural miss and I's identical cache hit as evidence that I computes faster: report equal numerical-work requirements and shared physical execution separately. Use a fixed W/I/O order rotated by query ordinal; do not use favourable timing selection.

## 9. Fixture, replay, resources and artifacts

After separate user authorization and source lock, run four fresh fixture sequences (one per template) with seed 1201: 24 occasions, 72 interface decisions, at most 48 distinct forwards, plus independent scoring and a fresh replay. The fixture also requires non-neural malformed-ID, wrong-scope, missing-binding, conflict, revision, deletion, prefix-isolation and cache-key tests. No such tests were implemented or run in this review.

Main: 192 occasions × 5 readers × 3 arms = **2,880 learned-interface decisions**. W/I exact parity permits at most two distinct Q variants: **1,920 main forwards**. Fixture plus main and one full independent replay need at most **3,936 distinct forwards**; the conservative no-cross-arm-reuse bound is 5,904. The hard limit is **6,000 attempted one-stage forwards**, including failures. Physical batches, logical requests, cache hits and all diagnostic/control rows are separate (CALL_LEDGER.json). Four non-neural exact-control paths add 768 main and 96 fixture decisions per pass. Replay reprocesses events and re-computes distinct model inputs with an empty cache; never reuse producer outputs.

Proposed future hard limits: two hours including implementation/preflight after execution authorization; 3 GiB process-tree RSS; abort also at 3.5 GiB container current memory, leaving headroom below this host's 4 GiB hard limit; 256 MiB total new uncompressed output; 64 MiB single delivery ZIP. Preserve partial evidence if a cap is reached; do not omit raw negatives to fit. Review/audit time is logged separately, not claimed as execution time. Recheck the actual future host and give a revised proposal if these bounds are infeasible. No GPU or throughput forecast is assumed.

Required future delivery: source/protocol/seed and export locks; all public event/input prefixes and isolated scoring ledger; every routing/validation/update decision; all distinct model outputs; exact controls and paired diagnostic overlays; per-arm memory/work/latency ledger; independent scored per-query/per-sequence/family results; every error/negative; fixture and fresh replay receipts; environment and resource receipts; package manifest and limitations. Do not copy old archives/models or imply missing historical training evidence has been restored.

## 10. Remaining gates, not hidden experiments

The design and seed allocations are fixed *as a proposal* in this bundle. No raw future input hashes or new implementation hashes exist yet. The **X_latest current-entity contract is a reviewer-proposed addition that still requires acceptance**, not an inherited Codex/user approval. Its proposed semantics and counts are explicit rather than silently applied to W/I. User authorization, a concrete source implementation and independent scorer, pre-generation source lock, runtime-compatible fixture, and generated-input identity checks remain mandatory. Any unresolved implementation choice that changes observations, stochastic construction, transitions, costs or scoring requires a new protocol version before main evaluation. This package is not an executable study and contains no new experimental results.
