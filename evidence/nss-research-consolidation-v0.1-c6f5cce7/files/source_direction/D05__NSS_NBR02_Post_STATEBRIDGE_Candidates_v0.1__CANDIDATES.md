# NBR-02 after STATEBRIDGE01: preserve the task operator, not just its state
## Candidate review v0.1 — 26 September 2026

**Status: PROPOSALS ONLY. No experiment dispatched.** This document responds to the user's request for candidate solutions. It does not load a model, compute a gradient, rescore the historical arrays, fit a model, or qualify STATEBRIDGE01. The source report, archived protocol, model/loss source, status, and return tickets were inspected as documents. This is mechanism-led NBR-02 work, not an adoption of either tri-core or shared-backbone NSS.

## Executive decision

**Recommended first learning diagnostic: test the permitted update surface and remove the deliberately shared A/B output as a controlled intervention.** Before inventing a larger repair mechanism, ask whether learning the B correction needs to modify the computation used by A at all.

If shared recurrent adaptation remains necessary or useful, the next repair candidate is **old-state-anchored continuation rehearsal**: train the changed model to continue from lawful old-version task states, rather than only rehearse from reset.

Keep **task-version pinning and qualified handoff** as a practical containment reference. Do not count its already demonstrated fixed-weight correctness as a new learning achievement, and do not let keeping every old version forever become the solution.

The numerical verification contract is a separate prerequisite for new qualifying results. Preserve the original whole-trajectory failure without retrospectively enlarging its tolerance.

## 1. Source-derived findings and limits

STATEBRIDGE01 used a new GRUCell(16,64) and Linear(64,9), with 16,329 trainable parameters. A was a four-flag checklist with a next-action readout. B comprised four scoped binary associations and deliberately used the same bit-0 output logit as A. All six parameter tensors could change. Task markers distinguished the tasks. [S1 §§1–2; S2 Task A, task B, and model; S3]

The model initially learned A and B. After eight B updates, A joint continuation with the old carried state was 4,050/5,120; after four repair batches it was 4,519/5,120. Rebuilding the same history with those updated weights scored 2,503 and 3,355, respectively. Original-version pinning remained 5,120/5,120. These are related readouts over four fits, eight B scenarios, 32 A histories and five positions—not independent tasks. [S1 §3]

Immediately reading the old state was correct in all 1,024 queries at each changed-weight stage. Problems emerged during continuation. The changed B label was correct in all 32 contexts, while the other B associations fell to 64/96 and recovered to 83/96. Thus restoring A by undoing the B correction is not a successful repair. [S1 §§4–5]

**The previous repair already rehearsed sequences, not just isolated labels.** Each of its four batches contained eight real previously observed length-17 A training episodes, supervised at their steps, plus the four current B labels. It started its A replay from reset and used ordinary SGD. A proposal to 'try sequence replay' without a more specific change would duplicate an existing mechanism. [S1 §2; S2 Learning intervention and fixed repair]

The final four commands of each scored A prefix set its four endpoint bits. Therefore the task requires earlier input than the final continuation cue, but does not establish dependence on every event in a long history. Any successor must retain this limitation or explicitly change the task. [S1 §2]

The original independent whole-prefix numerical tolerance failed on 11 array comparisons. Additional one-step checks passed, all independent scored class vectors agreed, and full adaptive replay matched. These are distinct evidence lanes; the study remains diagnostic and unqualified. No candidate here reclassifies that outcome. [S1 §§7–10]

## 2. Candidate 1 — separate readout sharing from recurrent adaptation
### CAND-NBR02-READOUT-SURFACE-001 / highest-priority numerical proposal

**Question:** How much of the observed interference depends on forcing A and B to share their final scalar readout, and how much B learning actually requires changing the recurrent operator?

This is a prospective controlled diagnostic, not a claim that the shared head is the established cause. The source deliberately introduced that coupling. Both the shared-output choice and the adaptive recurrent core deserve independent contrasts before making an architectural conclusion.

### Paired starting point

Use isolated copies of a qualified initial model. A separate scalar B head can be initialized by copying the current A bit-0 weight row and bias: 64 weights and one bias. Its initial B logits are then intended to match the old head exactly; verify that in preflight. The recurrent state dimensions and A readout remain unchanged. No extra layer, hidden state mapper, or new core is introduced.

A first screen could use all four archived terminal initial models as read-only starting evidence, explicitly labelled a retrospective intervention study. Existing task streams would then be diagnostics, not unseen confirmation. A later confirmatory run would require a separately specified new evaluation construction and, if required by that protocol, fresh initial fits. Original models are never overwritten. Loading copies and applying new updates is real new experimental work; it is not free retained-data analysis.

### Four informative conditions

| Condition | B readout | Recurrent cell during B learning | Interpretation |
|---|---|---|---|
| Shared/adaptive | Existing A bit-0 row | Updates permitted | Historical mechanism reference |
| Separate/adaptive | Copied independent scalar B row | Updates permitted | Removes direct A/B output-weight sharing, but not shared recurrent changes |
| Shared/frozen | Existing A bit-0 row | Frozen | Isolates effects possible through the shared output even with fixed recurrent processing |
| Separate/frozen | Independent scalar B row only | Frozen | Tests whether B can be learned within a restricted readout surface |

In the separate cases, B updates cannot write A-head parameters. In the frozen-cell cases, all input/recurrent weights and GRU biases are frozen—not just one recurrent matrix. The initial A/B fitting is common and completed before these masks are applied. There is no performance-dependent unlocking or additional fitting if a restricted branch fails.

A prospective first diagnostic should end after the identical scheduled B learning, with no new repair stage. That isolates where the initial damage enters before comparing maintenance. Original no-update/pinned references remain costed controls.

### Why the restricted arm is informative, and what it cannot prove

With the complete A path frozen and scratch states isolated, A's function is unchanged by construction. Its continued success is primarily an invariant check, not a discovery of spontaneous noninterference. **The nontrivial question is whether the restricted B head still acquires the new mapping, preserves the other B mappings, and does so within the allowed feedback/work budget.** A tiny fixed-feature problem may permit this even when harder future tasks do not.

A separate B head is extra task-specific capacity and supplied routing. Account for the 65 parameters, active/trainable parameter counts and routing. One option is to allocate the same auxiliary row in every condition, with unused rows explicitly inactive; that equalizes storage, not function or active capacity. Do not portray this as a perfectly equal-capacity architecture superiority study.

### Readouts and outcomes

Measure A immediate read, continuation positions, bit errors and next-action errors separately; A rebuilt/fresh-history performance; changed B acquisition; all other B associations; probability quality; and actual work/parameter displacement by group. Use the same saved h, histories, labels and B receipt order within each paired comparison. Forward queries do not update weights. No hidden evaluator state enters training.

- Separate/adaptive improves A at unchanged B learning: evidence that direct readout sharing contributes to this implementation's interference; not proof that all recurrent interference is solved.
- Separate/adaptive remains poor, separate/frozen preserves A and learns B adequately: a restricted update surface may suffice for this bounded task.
- Frozen-cell conditions fail B: feature/recurrent adaptation may be needed under this budget; this does not prove insufficient capacity or permanent impossibility.
- Every shared-core adaptive condition harms A: proceed to protecting or repairing the recurrent computation itself.
- A is protected only by failing to acquire B: not a working joint solution.

This four-condition screen is recommended before a larger teacher, a new recurrent topology, or a broad rehearsal sweep. It does not restore the removed neural-overlay system or decide how full NSS cores must be organized.

## 3. Candidate 2 — rehearse how to continue from old working states
### CAND-NBR02-STATE-ANCHORED-REPAIR-001 / conditional next maintenance comparison

**Question:** Does explicitly training the updated model to continue from old-version states preserve interrupted work better than repair that rebuilds state at the current version?

The old repair already contained sequential A training and current B targets. The proposed change is **the origin of the starting state for a repair suffix**, not merely adding more old examples or calling replay 'state repair.'

### Core construction

Retain a bounded training-only collection of previously observed A histories, legal cut points, continuation segments and recorded task targets. Obtain an old-state snapshot at each cut with the accepted pre-update model; bind the snapshot to that model, source history and cutoff. No states from the current held-out continuation test enter repair.

At each repair batch, compare two parameter-copy branches using the same histories, suffixes, released current B targets, A/B loss weighting, suffix length, update count and clipping:

- **Current-state suffix repair:** rebuild each source prefix using the current candidate, detach its endpoint, and train through the declared A suffix.
- **Old-state suffix repair:** initialize the same suffix from the saved accepted-version state, detached, and train through the suffix under the current candidate.

Both backpropagate only through the same suffix. There is no gradient through the old model or through the current prefix in either branch. Hold the same B correction and retention objective in both. The old-state branch is being trained on an explicitly supplied old-state distribution; disclose that assistance.

Retain the original reset-sequence repair as a historical or freshly repeated reference, but do not claim its direct comparison isolates only anchoring: it has a different replay starting-state and prefix/backpropagation contract. The matched suffix pair supplies the main discriminator.

### Cost and information controls

Old-state production, checkpoint residency, state-cache bytes, public history, prefix processing and replay all count. To match per-batch state-construction work for the causal comparison, both arms can execute the same old/current construction operations and discard the unused start; alternatively report the difference and constrain total permitted work explicitly. The protocol must pick one before execution. Do not charge a stored-state read as an entire prefix recomputation or present old-state construction as free.

Train to preserve semantic continuation, not exact hidden-vector equality. On independently specified cases, measure old-state carry AND current-weight rebuilt/fresh histories. A candidate that handles the rehearsed old states but cannot process new A histories is only an interface-specific repair, not recovered general task competence.

The real question is joint: correct A continuation, current B correction preserved, other B competence retained, and no growing reconstruction/repair requirement. Evaluation must continue beyond the exact suffix examples used for repair. The task oracle is a scorer or declared training-target source for already permitted training histories, not a provider of hidden evaluation state.

### Outcome interpretation

- Old-state repair improves carry without losing fresh A competence or B learning: supports explicit transition compatibility training within its coverage.
- Both repair forms work equally: keep the cheaper/easier representation; do not give anchoring special credit.
- Only carry improves, while rebuild/fresh A remains poor: useful restricted continuation evidence, not full competence repair.
- Both remain poor: target broader competence/update interference, not a state mapper alone.
- A improves by forgetting B: the trade-off remains unsolved.

A teacher from the frozen parent could later supply transition-behavior constraints, but adding teacher losses here would be another intervention and is deferred.

## 4. Candidate 3 — bounded task pinning and qualified handoff
### CAND-STATEBRIDGE-PINNED-TASK-001 / existing control expanded only by separate authorization

**Role:** keep a live task on a stable pair of model revision and recurrent state while preparing a usable successor. This is containment and scheduling, not parameter repair.

STATEBRIDGE01 already showed 32 logical task states sharing one immutable model revision, with correct pinned continuation. It also showed that the old revision cannot answer the new B correction. Repeating that basic numerical control alone is not a new discovery.

The untested contribution would be a small version manager with a fixed version-residency budget, explicit adoption checks and measured correction availability. An illustrative first system contract could allow one accepted serving version plus one candidate. Tasks share immutable weights but own their task states and evidence cutoffs. Proposed commit points must resolve pending learning receipts/traces and define what happens to unfinished tasks.

A new candidate must first demonstrate required A processing and B acquisition. A task boundary does not by itself make an inadequate candidate competent. Do not force a bad version onto a task merely to reclaim the old version's storage.

With a two-version bound, long tasks may delay retirement of an old version and therefore delay a subsequent training/adoption cycle. Record that delay and any version-pressure stop. Extra staging copies, journals, publication records, rollback space and concurrency are not free. Never discard a needed old version silently or promise unlimited updates without additional resources.

A meaningful test must require B's valid correction to become usable within a declared deadline and the new qualified version eventually to assume the required tasks. Keeping A correct on the old version forever while never adopting useful learning cannot pass. Exact retrieval can make new facts available separately, but it must not masquerade as neural adaptation.

Task/version/prefix/receipt references may eventually be represented in the maintained token workspace. Start with ordinary typed metadata as the strong control. Neither completed tasks nor confident answers automatically produce clean labels. Authentic feedback, observed events, failed attempts, deduplication and target revisions remain necessary. Tokens coordinate them; they do not certify them.

## 5. Numerical qualification: one open issue, not a reason to invent a cause

Before the next learning screen, address RET-STATEBRIDGE-NUMERIC-001 through a separately frozen prospective validation contract. This preparation is required whether a candidate looks promising or not.

Preserve the original 11 whole-prefix failures and the original strict scorer. Do not enlarge its tolerance until the old data pass and call that independent validation.

The new contract must distinguish: source/input/target correctness; independently reconstructed gradients and applied parameter bytes; one-step state/readout arithmetic from the captured predecessor; accumulation across an entire recurrent trajectory; semantic margins/decisions; and same-runtime exact adaptive replay. None automatically substitutes for another.

Choose and justify a future trajectory-level numerical comparison before its main run. Fixed development/analytic stress inputs or independent same-precision arithmetic can inform that contract; any adopted error allowances need a declared scope and basis. No particular replacement tolerance or proof is supplied by these notes. Shared correct classes do not settle continuous numerical fidelity, and continuous differences do not automatically explain a large semantic failure.

If a genuine formula/application bug is found, repair it under a versioned source lock before interpreting a new scientific result. If divergence reflects the chosen arithmetic representations, report it under the future contract without changing the old disposition. This is not a request to rerun all historical training.

## 6. What to defer

**Learned state mapping:** defer until the updated model handles fresh/rebuilt A histories adequately while old-state carry remains distinctly worse. The current opposite pattern gives no basis for making a state mapper the first solution. A mapper might find a special compensating state, but that possibility does not repair the general processing problem or justify its cost now.

**More unrestricted repair by default:** the fixed repair was only one schedule, so larger or better repair may help, but no evidence establishes that more updates alone are the cheapest answer.

**Bigger core, new optimizer, native token writer, teacher/Tertiary, micro–macro scheduling changes:** none is bundled into the first surface test. The user explicitly asked for mechanism-led NBR-02 rather than validating idealized NSS roles.

## 7. Prospective success, data and resource decisions

Preserve the user's objective: manageable temporary losses, affordable repair, and useful improvement that remains after more work. Do not silently adopt exact probability preservation as the requirement. Operational floors and tolerances for the NEW task must be declared in its protocol, not selected after seeing the result. Report stricter and looser prespecified sensitivities without choosing the favorable one as the only answer.

Common measurements: immediate state read; per-position A continuation; endpoint A success; rebuilt/fresh-history competence; changed-B learning; every old-B outcome; class and probability loss; number/value of accepted changes; latency when tested; actual forward/backward/update/record-access counts; model/state/candidate/history residency; and numerical failure records. Repeated readouts are not independent tasks. Fresh sequence IDs alone do not create unseen task grammar.

There are no final fit counts, limits, seeds, derivative budgets, time or evidence ceilings in these candidate notes. The four archived fits can support a smaller retrospective surface diagnostic, but their old attempt budget is closed. Any new counterfactual gradient/application requires a new ledger. A fresh qualified study requires its own source/data lock, untouched confirmation where appropriate, adequate task admission, independent scorer, all-attempt accounting, full adaptive replay, and relocated evidence checks. No hidden retries, post-result unfreezing, output repair or loss of negative cases is allowed.

## 8. Recommended decision path

1. Finalize the new numerical verification contract and the four-condition readout/surface diagnostic.
2. If a restricted surface learns B adequately while A is unchanged, adopt that as a bounded experimental baseline and test transfer to a B task that genuinely needs richer processing before making a broader architecture claim.
3. If shared recurrent change is required and damages A, specify the matched old-state/current-state suffix-repair test.
4. Use pinning as a containment reference. Implement a bounded scheduler only when correction availability, version lifetime or adoption behavior is the next real question—not to avoid fixing the learner.
5. Reconsider mapping only if improved current-weight task competence reveals a residual old-state compatibility problem.

No automatic progression or campaign is authorized. A simpler control succeeding is a useful outcome; a correctly executed negative is preserved.

## 9. Program status and source boundary

NBR-01 stays CLOSED_BOUNDED_RECOVERED_EVIDENCE. NBR-02 remains active and mechanism-led. STATEBRIDGE01 remains diagnostic/unqualified with its numerical and continuation tickets open. No choice here adopts tri-core or the clean-slate shared-backbone challenger.

Keep RET-MW01-FIT-001 parked, the original Q010 identity question separate, dream/self-play/generational growth deferred, OBS-DC01-COST-001 open, and FCR-0103-001 (foundation consolidation after NBR-03 and before NBR-04) intact. The user's conditional earlier NBR-01 return is not reassigned to an unnamed ticket. No historical model is rewritten, no source memory retired, and no broader stage advanced.

**S1** — STATEBRIDGE01 Execution v0.2 REPORT.md (standalone bytes matched its compact handoff member).
**S2** — the compact handoff's protocol/PROTOCOL.md and protocol/CONFIG.json (archived original protocol, not a fresh execution).
**S3** — the compact handoff's source/model.py (read as text; not imported).
**S4** — the compact handoff's STATUS.json and RETURN_TICKETS.md.
**S5** — NBR02_State_Learning_Bridge_v0.1/DIRECTION_AND_CANDIDATE.md, prior mechanism-led question and constraints.

Source hashes and checked scopes are in SOURCE_IDENTITIES.json. The compact package's CRC and directly stored source-manifest hashes were checked as bytes. The complete 121.5 MB evidence archive was not restored or independently numerically rescored in this proposal pass. Candidate effects are hypotheses, not observations.
