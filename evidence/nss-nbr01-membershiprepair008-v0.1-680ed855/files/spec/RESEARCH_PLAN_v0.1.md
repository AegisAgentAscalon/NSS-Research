# NBR-01 / MembershipRepair008
## Familiarity-aware repair and writable novelty
**Research plan v0.1 | 21 September 2026 | DRAFT — NOT_RUN**

### Decision brief
RepairBinding007 combined compatible identity restoration with frozen relationship readers. Its next exposed failure was different: cleanup could force an unregistered identity into a familiar code and then retrieve an unrelated relationship. [S1, §§3–6]

**Target:** distinguish a recoverably damaged familiar identity from an input with no sufficiently supported match, while preserving legitimate registration, writes, corrections, clears, and multi-step reasoning.

**Recommended comparison:** a calibrated geometric match/reject rule versus a small learned match/reject mechanism, using the same reference information and the existing frozen readers. Retain no-repair and unconditional-repair controls. A better-prepared robust reader is a conditional comparison, not an automatic additional project.

**Useful result:** fewer unsupported matches and answers without solving the problem by rejecting almost everything, destroying repair benefits, or refusing to admit new identities.

### What is established versus proposed
| Source finding | Consequence for this plan |
|---|---|
| Learned and nearest-code repair both reached 100% established and missing-chain accuracy on the specified nominal corruption tests. [S1, §3] | Preserve the successful repair-and-reader combination as the reference. |
| Unregistered queries produced unsupported room answers in 47.81% of learned-repair cases and 62.81% of nearest-repair cases. [S1, §6] | Measure false identity matches as well as final answers. |
| Wrong valid relationships and erased values were not recovered by the identity dictionary. [S1, §7] | Do not confuse identity restoration with factual verification or reconstruction of lost edges. |
| Nearest repair was substantially cheaper in the measured implementation. [S1, §8] | A learned candidate must justify its cost, not merely match a simple rule. |

The mechanisms, stages, thresholds, and outcome rules below are new proposals. This document records no new model training, benchmark, independent replication, or accepted architecture change.

### Scope boundary
Remain inside NBR-01: working-state retention, recurrent processing, stability, representation/binding, and their interfaces. Candidate training and calibration occur before scored evaluation. Learned parameters remain fixed during evaluation. Registration changes explicit scoped records and the active identity reference, not model weights. [S2, pp. 7–9, 20–21]

No delayed-credit study, reinforcement learning, Titans-style test-time parameter updates, low-bit learning-state test, neural-role redesign, model download, repository merge, or deployment is part of this pass. The Primary/Secondary/Tertiary/Validator requirements remain unchanged. The proposed experiment name does not rename the architecture.

<!-- PAGE_BREAK -->

## 1. Questions, hypotheses, and retained machinery

### Questions we need to answer
**Q1 — Membership:** can the resolver accept altered known identities and decline unsupported matches, including unfamiliar identities close to familiar ones?

**Q2 — Consequences:** does better identity handling improve full-chain answers without damaging missing-relation behavior or clean competence?

**Q3 — Writable novelty:** can a genuinely new identity remain unresolved before an explicit registration event, become addressable afterward, and still have no known relationship until one is written?

**Q4 — Reliability and cost:** do the gains survive time, increased processing depth, interruptions, and reasonable reference-set variation at an acceptable cost?

### Testable hypotheses
**H1:** absolute match quality plus the gap between competing identities will outperform unconditional snapping on the joint familiar/unfamiliar task.

**H2:** a learned match/reject mechanism may improve that tradeoff over a calibrated simple rule. This is not assumed; equality or a simple-rule win is useful evidence.

**H3:** separating identity registration from relation presence will support new records without allowing a query or a rejected match to create one.

**H4:** some severe distortions and near-collisions will be ambiguous from the supplied vector alone. The experiment should locate this boundary rather than hide it with generator labels.

### Freeze what already works
Reuse both Study006 reader variants and its binder as preserved in Study007, across all five existing parent pairs. Reuse the Study007 compatible learned and exact restorers as references. Do not retrain the reader while claiming to isolate a new matching mechanism. [S1, §§1–2]

Keep the 17-coordinate identity representation: 16 identity coordinates plus the existing UNKNOWN coordinate. Preserve separate relation-presence flags, full-vector qualified writes, scope checks, and the bounded record store. Study005's learned existence maps are not silently added; Study007 used protected Boolean relation presence. [S1, §1; S3, §§2–3]

**Compatibility change:** the proposed active-identity mask, resolver status, enrollment events, and snapshot metadata require a named interface revision. Validate it; do not label old and new snapshots interchangeable because their vector dimensions match.

### What the resolver may see
It may receive the current numerical vector, the active codebook and mask, operation type, scope/version metadata, and declared numerical match features. All competitive arms receive the same information.

It must not receive the true identity index, whether a sample was generated as familiar or unfamiliar, the original clean vector, corruption strength, a correct record slot, the hidden relationship graph, or the expected room answer. Those belong to data generation and scoring only.

The protected codebook remains an explicit assumption. It contains identity symbols, not relationships or proof that a particular relation exists. [S1, §§1, 7]

<!-- PAGE_BREAK -->

## 2. Candidate set and fair controls

### Primary challengers
| Arm | Proposed mechanism | Main question |
|---|---|---|
| **A — Selective nearest-code repair** | Find the nearest active code, but accept it only when absolute distance/similarity and the margin to the next candidate meet calibration-set criteria. | Is a small inspectable rule sufficient? |
| **B — Learned selective repair** | Add a trained match/reject decision with an explicit no-match outcome. Keep the prior restorer and reader frozen in the primary comparison. | Does learning improve the useful acceptance/error tradeoff enough to earn its cost? |

For A, register the feature convention before fitting thresholds. A nearest candidate is not automatically a plausible candidate: both absolute fit and competition matter. Reject-only, distance-only, and margin-only versions are ablations, not secretly tuned extra winners.

For B, train on fresh dictionaries with familiar, noisy-familiar, unregistered, and near-neighbor examples. Use code-permutation-equivariant features, such as pairwise fit, vector norm, nearest/runner-up separation, and active reference count. No fixed row may stand for a particular entity. The no-match output must not be merely a renamed maximum closed-set softmax score.

To separate selection from rejection, include **A's gate with the old learned restorer** and **B's gate with nearest projection**. Compare them on the same saved inputs. Main training changes the declared resolver only; other weights remain pinned. Fit calibration on separate data for both arms and count those labels.

### Controls to keep
**No repair** and **normalization only** preserve the earlier failure references. They show whether the intervention helps; neither is the only baseline.

**Unconditional nearest repair** and **the existing learned dictionary repair** measure the recovery/false-association tradeoff we are trying to improve. [S1, §§3, 6]

**Exact traversal of the same candidate-written store** separates storage or binding errors from neural reading errors. A separate gold graph provides answerability and scorer checks only. Do not supply it to repair or the reader.

**Reject-all** exposes the trivial way to eliminate false acceptance. It must fail the supported-answer and new-record requirements.

### Conditional alternative: robust reader
If the primary comparison leaves errors on otherwise well-identified inputs, train a new reader revision on the same declared evidence and missing/unregistered examples, with no external query snapping. Evaluate its extra preparation cost separately. This asks whether interface preparation is preferable to a cleanup layer.

This arm requires its own development lock and training budget. It is not authorized by a failed score to change the frozen main comparison. The broader generic-Transformer competence gap remains open; this focused study cannot support a family-wide architecture ranking. [S1, §9]

<!-- PAGE_BREAK -->

## 3. Decision semantics and a writable lifecycle

### Distinguish three things
**Identity membership:** whether the input has a sufficiently supported match in the currently registered reference.

**Relation presence:** whether the relevant relationship was actually recorded. A registered identity can have no recorded location.

**Content readability:** whether a present relation's numerical key/value can be used reliably now. Unreadable does not mean never recorded.

The resolver returns either **MATCH(code, diagnostics)**, **NO_SUPPORTED_MATCH(reason)**, or **INVALID_REFERENCE(reason)**. Low support and competing matches are possible reasons for no supported match. This status does not prove that the real-world object is novel, false, or nonexistent.

### Do not overwrite uncertainty with a confident-looking symbol
Measure admission from the input before snapping or normalizing it into a canonical answer. Preserve the raw input through that decision. A canonical repaired result must not become independent evidence that the original match was correct.

A declined query stops that query's unsupported path and remains unresolved. It does not alter storage, register an identity, or clear a relation. A declined stored field keeps the relation-presence flag intact, retains its available numerical state, and is marked unreadable for use in the chain. A later qualified write or an explicitly tested recovery path may restore readability.

Do not keep an uncounted clean shadow copy. Audit logs are available to the scorer, not secretly to the model. Unreadable fields cannot keep accumulating confidence from repeated processing of unchanged evidence. Their exact reassessment policy must be frozen before main evaluation.

### Proposed registration sequence
1. Query an identity absent from the active reference: no supported match and no mutation.
2. Receive an explicit, in-scope **REGISTER** event carrying that identity's canonical representation: add it to the active reference, but add no relationship.
3. Query its location: still no established relation.
4. Receive a qualified relationship write: create the relation; the existing binder must place it without receiving a gold slot.
5. Query it cleanly and under declared noise; then correct, clear the relation, and rewrite it.
6. Reset the scope and verify that old identities, relations, caches, and unresolved flags do not leak forward.

Registration authority is supplied by the synthetic environment, not inferred from confidence. This tests state construction, not autonomous discovery or weight learning. A rejected match is not permission to register anything.

Start registration episodes below a fixed capacity, with unused rows masked and containing no future identity vectors. The resolver and final decoder see only currently registered codes. Log codebook revisions. Changing membership can invalidate cached choices or calibration assumptions; it must not silently rewrite old evidence.

Capacity-full, denied, duplicate, near-collision, and wrong-scope registrations need explicit outcomes. Registration succeeds only if the state operation is valid; a very similar new code may still remain difficult to distinguish at query time. Do not merge distinct identities just to hide that difficulty.

<!-- PAGE_BREAK -->

## 4. Stage A — Isolate the familiar/unfamiliar boundary

Use intact stores or isolated vectors first. Freeze the readers. Produce independent training, calibration, and confirmatory dictionaries, identities, and noise draws.

| Input family | What it tests | Role |
|---|---|---|
| Exact registered identities | Basic competence and unchanged clean matching. | Core |
| Registered identities with query noise 0.05 and 0.20 | Useful repair, not universal rejection. | Core |
| Independent unregistered unit vectors | Whether new inputs are forced into familiar codes. | Core |
| Registered identity with no recorded relation | Membership must not stand in for relation presence. | Core |
| Near-neighbor novel identities and two-code mixtures | Collisions and ambiguity hidden by easy random negatives. | Stress |
| Query noise 0.40, strong scale changes, erasure | Degraded observability and out-of-preparation behavior. | Stress |

The numerical noise settings inherit the Study007 test vocabulary, not a biological or hardware noise model. [S1, §§2, 6]

Generate unfamiliar vectors from the same base normalization/distribution as registered vectors. Otherwise the gate may recognize a norm or marker shortcut instead of familiarity. Never mark unfamiliar input by putting it in the UNKNOWN coordinate. The existing UNKNOWN sentinel and erased inputs are separate cases.

Near-neighbor cases must vary distance and similarity systematically. Include removed-from-reference identities, unrelated new vectors, and novel vectors deliberately near existing codes. Preserve all strata even if only the easy group meets the target. Reverse reference-row order and consistently rename identities to check for index dependence.

### An explicit information-limit control
Construct paired cases with exactly the same observable vector, codebook, scope, and record state, but different hidden origins: one is a distorted registered identity, the other an unfamiliar identity that produces that vector.

A resolver with identical inputs cannot reliably produce two different origin-dependent decisions. Report this as an ambiguity boundary, not a failed universal-memory promise. Hidden origin may be used by a labelled scorer/oracle diagnostic, never by a competitive arm. Rejecting both can avoid a false association but loses supported coverage on the familiar member; show both costs.

### Planned data scale
Target at least five paired main resolver seeds, retaining all five previously used reader/binder parents. For inexpensive membership tests, aim for at least 512 independent episodes per core class per pair. Final sample sizes, bounded development trials, and compute limits are fixed after an execution-only pilot and before confirmatory data are inspected.

These are fresh resolver fits and episode samples, not five independently rediscovered full architectures. The inherited tasks and parent models have already been studied. Do not claim an untouched task-family or depth-selection evaluation.

<!-- PAGE_BREAK -->

## 5. Stage B — Put selective repair back into state and reasoning

### Required comparisons
| Dimension | Proposed settings and purpose |
|---|---|
| Damage location | Keys only, values only, both, and query only; do not combine them initially. |
| Retention horizon | Clean, 64 noise ticks, and 1,024 noise ticks; match graphs and disturbances across arms. |
| Storage disturbance | 0.02 per tick in core comparisons; 0.08 as a separately reported stress setting. |
| Query-time depth | 1, 2, 4, and 8 rounds on matched 4- and 8-link tasks. |
| State availability | Retained-state reference plus a labelled state-removal intervention. |
| Evidence condition | Fully established chain, missing link, cleared link, unregistered starting identity, and corrupted intermediate identity. |

Keep event-time repair work fixed when query depth changes. Record decisions at every resolver invocation, including intermediate values that become the next query. A pipeline that checks only the initial query may still make an unsupported match later.

First install exact visible records to isolate repair. Then run the live-write version through the inherited learned binder. Never silently repair its initial placement with the gold graph. Score known binding errors separately from later storage damage or reader errors. [S1, §§3, 5]

Test the registration sequence from Section 3 with neighbor records already populated. Add a separate 4,096-tick empty/idle interval before a valid new registration and write if the core harness budget supports it; lock inclusion before main evaluation. Do not replace the core horizon with a shorter one after failure.

### Query-time cleanup must not bypass the resolver
All final decoding and intermediate traversal must honor active membership and no-supported-match status. A rejected vector must not slip into the old unconditional final codebook decoder and return a room anyway. Report invalid/unresolved intermediate outputs separately from unsupported room answers.

### Stage C — Cost and cadence, after a working boundary
Compare every-tick repair, one repair every 8 ticks, one every 32 ticks, and repair just before reading on the same graphs and disturbances. Query-only repair and store maintenance remain separate costs.

A periodic-versus-late test with the same total number of repair calls is an additional timing control, not a claim of equal actual runtime. Use bounded schedule choices registered before main scoring; do not search a large cadence grid and report only the best point.

This stage asks whether continuous cleanup is worth its cost once a good admission rule exists. It should not expand the first classifier pilot into an all-mechanism Cartesian search. Preserve the chosen schedule's task, error, state, and time results together.

### End-to-end failure attribution
Trace each failure through registration, initial binding, field corruption, identity admission, relation presence, neural traversal, and final decoding. Record the first wrong or unsupported transition, not just the final answer.

<!-- PAGE_BREAK -->

## 6. Measures and proposed acceptance screens

### Measure usefulness and restraint together
**Supported-answer accuracy:** correct destination divided by all answerable episodes. Abstention counts as failure here. Also report conditional accuracy among answered episodes and answer coverage.

**False identity acceptance:** unregistered inputs assigned any registered identity, even when the resulting chain happens to return UNKNOWN. Measure wrong-identity assignments on registered queries separately.

**Unsupported terminal answers:** room claims for unregistered or missing-relation queries. Distinguish these from unresolved nonterminal outputs; neither should disappear from error accounting.

**Lifecycle integrity:** successful registration, first write, correction, clear, rewrite, reset, neighbor preservation, and capacity handling. Membership, presence, and readability need separate metrics.

**Dynamics and resources:** whole-chain success, false matches per query/stream, time to first false match, repair cadence, query rounds, state bytes, peak temporary allocations, latency, and total preparation cost. Repeated steps within an episode are correlated, not independent experiments.

### Initial nominal targets — proposed, not passed
| Gate | Proposed requirement |
|---|---|
| Useful known retrieval | At least 95% correct supported answers in each parent pair at sufficient depth in each core condition. |
| Missing-relation handling | At least 95% correct unresolved answers in each pair; report unsupported terminal claims separately. |
| Unregistered-input handling | At most 1% false identity acceptance and at most 1% unsupported terminal answers per pair on the declared core independent-unregistered distribution. |
| Preserve prior benefits | No more than 1 percentage point loss versus the paired unconditional-repair reference on clean/core-known conditions, while meeting the 95% floor. |
| Writable novelty | At least 95% correct task behavior after valid registration/writes, with missing relations still unresolved before the first relation write. |
| Exact software boundaries | Zero observed unauthorized registry/record mutations, silent capacity overwrites, or invalid snapshot acceptance; all specified boundary tests pass. |

These are initial screening goals. Use a development pilot to judge feasibility and choose resource ceilings, then version and freeze the actual thresholds before confirmatory runs. A change must remain visible; no post-main lowering of standards. Near-collision and high-noise stress tests remain mandatory reports, not hidden exclusions or implied guaranteed coverage.

Report every seed, paired effects, ranges, and uncertainty intervals. Intervals use independent episode/stream units rather than all hops as independent trials. An empirical 1% limit is not proof that a deployment failure probability is below 1%; provide sample counts and an appropriate upper bound. Do not claim success by a rounded average that hides a failing pair.

A behaviorally successful learned gate is not automatically the preferred implementation. If the simple gate matches it and costs less, prefer that control for this scope. State which advantage, if any, justifies extra complexity.

<!-- PAGE_BREAK -->

## 7. What to watch for and the controls that expose it

| Failure or misleading result | Required check |
|---|---|
| Rejecting almost everything | Supported accuracy, coverage, and new-registration lifecycle measured jointly with false acceptance. |
| Snapping first and scoring afterward | Log the raw pre-repair fit and gate decision; do not let projection manufacture its own confidence. |
| Every unfamiliar input is conveniently far away | Same-generator novel vectors plus near-neighbor and observed-equivalent stress cases. |
| Hidden future identities | No future codes in inactive rows, candidate inputs, lookup caches, or final decoder before registration. |
| Registered identity is treated as a recorded relationship | Query registered entities with absent and cleared relations at several path positions. |
| Repetition becomes fake corroboration | Repeat the identical unresolved query without new evidence; no registry growth or rising evidence count. |
| Query resolution silently changes stored records | Query-time state hashes must remain unchanged; writes require separate declared events. |
| An unreadable record is silently erased | Preserve relation presence and original available data; distinguish unreadable from absent. |
| A correct write is undone by maintenance | Test first write and correction immediately and after long noisy idle periods. |
| A soft mixture lands between identities | Compare accepted learned output with nearest projection under the same gate; inspect next-hop behavior. |
| Different codebook size changes confidence | Vary active membership at constant allocated capacity; freeze or explicitly condition thresholds. |
| Larger registry changes unrelated answers | Re-query unchanged facts after every registration; inspect near-code collisions. |

### Additional fault checks
Supply a wrong or stale codebook revision, an unregistered near-duplicate, an exact value erasure, and a different but valid identity substituted into a relation. Version validation should catch declared metadata incompatibility; it does not certify the truth of an otherwise valid record.

Test original-versus-shuffled codebooks and key/value association permutations. Shared noise affecting several fields, rather than only independent noise, belongs in the declared stress set. Match corruption draws across candidates.

When repeated projection turns an earlier wrong match into a stable representation, call it wrong convergence, not successful restoration. Save enough causal history to identify the first erroneous transition. Retained canonical symbols cannot recover a relationship that was never supplied. [S1, §7; S2, p. 9]

### Biological interpretation
The ongoing motivation is compatible with studying selective stabilization rather than indiscriminate attraction to familiar patterns. This is a transfer hypothesis. No claim about a particular human or fly circuit, biological fidelity, or neural novelty follows from success here. The handoff requires mechanism-specific interventions rather than anatomical resemblance as the acceptance criterion. [S2, pp. 7–8, 21]

<!-- PAGE_BREAK -->

## 8. Preparation, resource accounting, and reproducibility

### Development and confirmation
Use a bounded development phase to choose gate features, training mixture, thresholds, and cadence. Keep training, calibration, and main episode seeds disjoint. Candidate A receives the same calibration evidence as B; labels used for calibration are part of its preparation budget. Preserve failed development variants.

Target five new resolver seeds paired to all five inherited parents. Reserve a fresh calibration stream per pair. Do not discard an inherited parent or a new seed for poor results. Register the candidate list, training steps, episode families, sample sizes, core/stress split, thresholds, memory/time ceilings, and source hashes before main evaluation. No test-result-driven refits are permitted in that registered comparison.

This v0.1 document is the planning input, not the frozen execution registration. All budgets and outstanding implementation details must be resolved before the confirmatory run; unresolved fields block that run rather than inviting silent defaults.

### Compare complete costs
Include resolver and inherited model weights; 17-coordinate records; relation-presence and readability flags; codebook and active mask; scope/version metadata; query scratch space; distances/scores; any caches; training activations, gradients and optimizer state; calibration data; checkpoints; and framework overhead.

Separate persistent state from temporary peak and exact audit storage from active inference access. A scalar threshold, a null head, and a reference lookup all have costs. No continuously growing unresolved-query backlog or uncounted exact shadow memory is allowed in the bounded-state arm.

Report controlled same-evidence comparisons first. They are not automatically matched-parameter or matched-FLOP comparisons. Record CPU/device, thread count, warmup, batch size, and measured latency distributions; measure batch-one behavior as well as throughput. Count failed/incomplete training attempts separately from completed fits. Do not extrapolate this environment's numbers to the user's hardware.

### Verification deliverables
Preserve all original inputs and input hashes. Test mask semantics, no-match propagation, update/clear ordering, query read-only behavior, registration capacity, and compatibility rejection before scoring models.

Save per-example inputs or reproducible seeds, raw match evidence, admission decisions, record state, reference revisions, first failure location, and final answers. An independent scorer uses the exact event graph and hidden origins; neither is passed back to the candidate.

Replay every main evaluation in a fresh interpreter. Reproduce at least one complete resolver training trajectory if a learned arm is fitted. Exercise state/RNG and mid-query restore after registration, correction, and unresolved status; compare against uninterrupted runs. Pin model, codebook, interface, calibration and schedule identities.

Rerun relevant unchanged foundation and prior-study tests, counting distinct tests once. Package code, protocol, parameters, calibration, per-seed results, failures, and receipts. A future package belongs beside the studies in `MegaMind_Alpha_Proto`, not merged into the foundation.

Internal replay, local Windows execution, independent external replication, and longitudinal companion testing are separate claims. This pass can establish only what it actually runs. [S1, §9]

<!-- PAGE_BREAK -->

## 9. Decisions this pass must enable

| Observed outcome | Decision |
|---|---|
| Simple gate preserves known repair and rejects most unsupported matches at lower cost | Keep the geometric mechanism for this scope; retain the learned arm as research evidence, not mandatory machinery. |
| Learned gate improves the joint accuracy/coverage/error frontier enough to justify its cost | Keep that resolver revision with its exact calibration, reference assumptions, and lifecycle tests. |
| Both fail chiefly where observable familiar/unfamiliar inputs overlap | Name the missing information or representation change needed. Do not launch an unbounded threshold search or promise perfect recognition. |
| Correct identities are recovered but chain answers still fail | Revise reader/binder preparation or interface; do not describe the residual as lost memory. |
| Registration corrupts old associations or silently merges nearby identities | Revise reference addressing, capacity, or lifecycle semantics before expanding scope. |
| Cadence reduction preserves quality while lowering measured cost | Keep the cheaper schedule, including its failure horizon and restart state. |
| No candidate reaches the useful joint criteria | Preserve the best measured tradeoff and a named failure explanation. No pass and no silent main-data retuning. |

### Recommended execution order
**First:** implement and test active-membership, unresolved-status, and registration semantics without changing the foundation.

**Second:** run a small isolated membership pilot for A and B. Confirm that known and unfamiliar inputs are not separable through accidental labels or formatting.

**Third:** lock the main protocol and run the paired fixed-reader corruption, unknown-query, and registration lifecycle comparisons.

**Fourth:** run the bounded cost/cadence comparison on behaviorally useful candidates. Invoke the robust-reader alternative only through its separately declared extension.

**Finally:** produce a mechanism decision and remaining-failure map. Do not automatically declare all of NBR-01 complete. Generic baseline competence, broader task diversity, richer identity representation, and an overall quality/resource frontier remain beyond a single successful membership pass. [S1, §10; S2, p. 20]

### What success would let us say
"Within the declared numerical identity system, the candidate repairs perturbed known inputs, declines unsupported matches, admits new identities through an explicit event, and preserves the tested relationship lifecycle at measured cost."

It would not establish general natural-language entity recognition, semantic truth, unlimited memory, self-directed learning, biological equivalence, or a deployed tri-core companion.

<!-- PAGE_BREAK -->

## Appendix — Sources and execution lock

### Source register and preparation record
**[S1]** NSS NBR-01 — RepairBinding007, v0.1: REPORT.md §§1–10; packaged spec/PROTOCOL.md; nbr007/repair.py. Reviewed for this plan, not rerun here.

**[S2]** NSS: Cognition, Architecture & Low-Bit Learning, research handoff v1.0, 20 September 2026: pp. 7–9, 13, 19–21. Preserved state/depth/learning distinction and experimental decision rules. Later user instructions keep 1–8-bit learning-state work deferred.

**[S3]** BindingDepth006 v0.1, reference/nbr006/store.py as preserved in Study007, plus the supplied report. Used for bounded store, learned binding, qualification, and compatibility context.

RepairBinding007 archive SHA-256:
`7f904c3fea2f724c980119a5c4adafc1c7a4da3ee96a4fd264d048a6e5028f80`

RepairBinding007 REPORT.md SHA-256:
`d2bd40670f84ac7505550c80a98192b1254a64a6567c120f08bc849837c8a933`

Preparation consisted of source reading and protocol drafting. No new experiments, statistical estimates, model fits, or external literature claims were produced. All MembershipRepair008 experimental stages remain **NOT_RUN**.


### Required fields in the eventual frozen registration
| Field | What must be recorded before confirmation |
|---|---|
| Component identities | Reader, binder, restorer, resolver, and interface hashes; all five retained parent pairs. |
| Data separation | Training, calibration, pilot, and main seeds; unfamiliar-input generation and core/stress definitions. |
| Candidate preparation | Complete feature set, objectives, steps, batch sizes, development-trial cap, and calibration selection rule. |
| State semantics | Active mask, UNKNOWN handling, no-match propagation, unreadable-field reassessment, registration ordering, and reset policy. |
| Evaluation contract | Sample counts, query points, horizons, depth grid, noise families, acceptance targets, and uncertainty reporting. |
| Resource boundary | Resident and temporary memory ceilings, elapsed-compute budget, thread count, and allowed cadence settings. |
| Reproduction | Event/weight/RNG snapshots, independent scorer version, training-rerun choice, and packaging checks. |

These fields become specific during implementation and development. An unresolved field does not authorize an evaluator to choose whichever value gives a favorable result. Once frozen, changes create an explicit new comparison; failed or incomplete runs remain in the record.

**Run boundary:** the user's current request is for this research plan. The document does not represent execution of MembershipRepair008, approval of a production component, or permission to substitute another NBR stage.
