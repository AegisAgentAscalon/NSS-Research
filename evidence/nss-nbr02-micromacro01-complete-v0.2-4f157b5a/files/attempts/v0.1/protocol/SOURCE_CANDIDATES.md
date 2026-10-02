# NBR-02 — candidates for a useful learning-and-repair cycle
## Proposal v0.1 · 25 September 2026 · NOT DISPATCHED

**Decision basis:** DEC-NSS-PROGRESS-002. First establish which bounded learning/repair mechanisms work; then compare how much degradation they cause, how much repair they need, and how much useful improvement survives. These are reviewer proposals, not additional results or a frozen execution protocol. No model, gradient, rehearsal, candidate evaluation or task generation was performed in preparing this document.

## 1. Evidence and the change in objective

The user explicitly seeks “small, manageable degradation offset entirely by repair and overall improvement,” not perfect intermediate predictions or acceptance of every useful proposal. A repaired capability has returned to its declared acceptable range. A residual deficit outweighed by another gain is a disclosed trade-off, not proof that the original capability was repaired. Exact restoration of weights or probabilities is not required. Numerical allowances, recovery deadlines, priorities and total work limits remain to be specified. [S1]

The retained TIMING01 analysis motivates, but does not execute, small repairs plus later consolidation: both replay placements helped old-answer quality when they acted, whereas later focal updates reintroduced interference; later replay improved the final result in most contexts but generally worsened the peak intermediate loss. The old-class answers in that held-out sample remained correct. A new schedule cannot be predicted by adding the benefits of the old schedules. [S2]

EVAL01 measured review decisions over recorded independent candidate offers; it did not repair or deploy a learner. Its particular targeted policy sometimes overestimated average damage by treating a vulnerability-selected subset as a representative sample. The next learning comparison should use a fixed measurement/review policy with distinct overall-impact and individual-risk outputs, not run another reviewer optimization campaign. [S4]

Historical PROTECT01, REHEARSE01 and TIMING01 verdicts remain unchanged. The present proposals change the prospective objective, not the old scores. The original micro/macro and mixed-continuation concepts remain identifiable; the design changes here are stated explicitly. [S1–S4]

## 2. Ranked candidates

| Priority | Identifier | Contribution | Main comparison |
|---|---|---|---|
| 1 | CAND-NBR02-MICRO-MACRO-001, full-cycle refinement | Small scheduled repairs plus a larger scheduled consolidation | Distributed old-record repair vs the same work postponed, and vs equal-work focal practice |
| 2 | CAND-NBR02-CONTINUATION-MIX-001, full-cycle refinement | Reduce disruption in the continued learning updates themselves | One blended current/old update vs cost-accounted alternating updates |
| 3 | CAND-NBR02-BUDGETED-REPAIR-001, new conditional candidate | Allocate repair work using evaluator evidence and a hard cycle budget | Evidence-triggered allocation vs fixed allocation under the same maximum work allowance |

These are alternatives and conditional successors, not an automatically authorized three-study campaign. Candidate 1 is the recommended next specification. Candidate 2 becomes especially useful if repair repeatedly works and is then undone. Candidate 3 is an efficiency question after a workable repair mechanism exists. Failure can motivate a new scoped design or an open dependency; it does not authorize repeated fitting until a pass.

## 3. Shared frame: keep evaluation fixed and test the learner

### 3.1 Protected and acquired behavior

Use the current NBR-02 association learner as a bounded mechanism test, not a prototype of every NSS core. Preserve the exact-G versus approximate-L distinction and keep every replay example in L under its own approximate rule. A use of exact old derivatives would need a different hybrid label.

Define the initial old-capability set, the current focal correction, which targets were legitimately revised, and the maintained source receipts. Never rehearse a superseded focal label as current truth. Do not permit evaluator-only labels, future events or unknown facts into learning, review or repair selection.

Initially retain a small complete old buffer for an auditable proof of mechanism. Its coverage must be disclosed: no claim about unbuffered skills follows. The same evaluator can inspect all eight old records plus the focal record for every branch in this toy. Cost those reads. This deliberately avoids conflating a new partial-panel rule with a new maintenance mechanism. The complete toy panel is not an independently sampled population of skills.

### 3.2 Measurement and review

Record the common pre-correction anchor, rolling parent, raw pre-feedback prediction, every learning and repair operation, completed-cycle state and subsequent ordinary work. Report old classes, target probability/log loss, affected individual records, focal/new competence, duration of any recorded breach, residual loss, and all costs. A mean over discrete checkpoints is not wall-clock exposure; event, operation and time measures must remain distinct.

Use the same task-level evaluator and review/adoption rule across the learner branches. Keep representative overall-impact summaries separate from worst-record/risk warnings. The first comparison can be offline candidate-learning assessment; it must not imply a live serving publication system. Do not substitute a retained parent or exact lookup for the raw candidate's answer and call that neural repair.

Behavioral limits may permit bounded transient loss and a defined amount of residual compromise or missed useful adaptation. Hard integrity, legal target versioning, unknown completion and evidence retention do not become tolerable accuracy trade-offs. A candidate is not disqualified merely because an intermediate probability moved; it is not qualified merely because the final average rose.

### 3.3 Feasibility before optimization

First require a finite cycle to acquire the correction, keep damage within its prospective extent/duration allowance, recover to the chosen operating range, retain the gain after ordinary learning resumes, and fit its work budget. Compare feasible alternatives on degradation, repair work and retained gain without choosing an arbitrary composite of incompatible units. Candidate superiority is a later claim, not a prerequisite for basic usefulness.

Baseline admission should establish acquisition and recovery over a declared number of valid receipts, separately from the first-correction speed an intervention is meant to improve. Keep frozen and strong exact controls. Do not require the baseline already to solve the intervention's target, impose impossible improvement headroom, select favorable seeds, or retroactively reclassify earlier stops.

A complete protocol must choose absolute competence floors, disruption/recovery bounds, repair deadline, hierarchy of metrics, replicate structure and total resource limits prospectively. These candidate notes do not invent them from already observed favorable cases.

## 4. Priority 1 — scheduled micro/macro repair

### Question

Can a finite schedule of small old-record repairs and later consolidation preserve the corrected answer and a manageable old-capability trajectory through further learning, at an affordable total cost?

### Concrete draft mechanism

Retain the ordinary first-correction comparison: a clip-1 baseline B1 and a clip-2 first-correction reference U, with later real receipts clip-1. For the candidate, after each of four declared stages, compute one batch of eight lawful old-example gradients at the current candidate weights; reduce, clip and scale with a prospectively pinned numerical convention.

A starting allocation is **1/8, 1/8, 1/8, 5/8** after the first changed-label update and the following three stages. These are illustrative post-clip multipliers, not selected optima. A larger multiplier need not give a larger realized step after earlier repairs have changed the weights. The coefficient sum of one does not make four batches computationally equivalent to one.

### Proposed first-study branches

| Branch | Behavior | Role |
|---|---|---|
| B1 | Ordinary clip-1 learning, no rehearsal | Slower-correction/retention reference |
| U | Clip-2 first changed-label correction, then ordinary learning; no rehearsal | Fast-correction, cheaper no-repair reference |
| D | Four old-record batches spread across the four stages, coefficients 1/8,1/8,1/8,5/8 | User's small-plus-large repair candidate |
| B4 | The same four old-record batches and coefficients, executed sequentially at consolidation | Same data, applications and example count; different placement |
| F4 | D's four scheduled batches and coefficients, each using eight copies of the most recently receipt-confirmed focal example | Equal-extra-effort control for what is practiced |

The F4 record is lawful historical training reuse, including when the latest real receipt addressed an old cue. It is not an invented new receipt. All eight per-example calculations occur at that batch's common entry weights; all batches recompute at their own current weights. No cached gradient gets reused at an incompatible parameter revision.

**Explicit change from S3:** its earlier five-branch draft included a uniformly distributed old-record arm instead of F4. This feasibility-first recommendation places the equal-effort focal-data control first, because the immediate question is whether useful repair is more than extra practice. The uniform-quarter comparison remains a later allocation-efficiency question; it is not an undeclared sixth arm. [S3]

D/B4/F4 each pay for four maintenance applications and 32 replay-example gradients. Their actual gradient norms, intermediate weights, retrieval details and latency can differ; equal example/update counts are not exact FLOP or norm equality. B1/U are intentionally cheaper controls. A D-versus-B4 contrast tests timing, not intrinsic superiority of old-data rehearsal over every alternative.

### Continue after the cleanup

Keep two additional ordinary feedback receipts after consolidation, one protected-old and one focal, with no further maintenance in that cycle. This proposed eight-receipt schedule is not the old six-receipt confirmation set. Inspect after both: the endpoint of the test must not coincide with the candidate's best-looking cleanup instant.

The initial feasibility study is still a short cycle. It cannot establish cumulative plasticity. A later continuing-history comparison must carry each branch's weights across cycles, include newly acquired capabilities in assessment, and follow its actual accepted/deferred history. That longitudinal extension requires its own specified task and budget, not retrospective stitching of independent forks.

### What would change our decision?

- D meets the joint recovery/usefulness budget: retain it as a workable mechanism even if not optimal.
- D outperforms B4 on the declared disruption/recovery measure: evidence for distributing the same repair work.
- D improves old retention over F4 without losing the current correction: evidence for practicing old information rather than only allocating more training effort.
- D and B4 tie: prefer the simpler/lower-overhead implementation unless another declared property differs.
- D/F4 tie: old-record selection is not established as the contributor.
- Old quality improves while the new correction is undone, or benefit disappears after the two following receipts: the full-cycle claim fails.
- All branches stay within the limits with U cheapest: no need for this repair overhead at that task difficulty; do not force a maintenance win.

No old confidence screen is silently repurposed. Strict raw prevention is supplementary; it is not the same primary claim as bounded recovery. Previous initial confidence dips remain recorded, and a prospective maximum permitted transient loss still applies.

### Cost status

At the **illustrative prior scale** of eight 100-update initial fits and 96 method/fit/base contexts, sharing the first two applications of an eight-receipt stream across the five branches gives:

- Per context: 2 shared applications + 5 branches × 6 remaining real applications + 3 maintenance branches × 4 batches = 44 applications.
- Scientific capture plus full adaptive replay: 2 × (800 + 96 × 44) = **10,048 applications**.
- Maintenance example-gradient calculations within that core: 2 × 96 × 3 × 4 × 8 = **18,432**.

This arithmetic is planning, not a selected study scale or complete dispatch cap. It excludes fixtures, cost probes, all ordinary gradients/forwards, measurement, logger tests, interrupted attempts and storage forecasts. The closed 7,000-application ledger cannot be reused. A new complete cost/host contract must precede authorization. A smaller study must be redesigned prospectively, not obtained by deleting difficult cases.

## 5. Priority 2 — mix retention into continuation, then consolidate

### Question

Can continued updates cause less damage in the first place, reducing the amount of later repair needed while preserving useful adaptation?

### Concrete draft mechanism

Keep the same strong first correction, initial repair if specified, final consolidation opportunity, evidence and evaluator across compared branches. At later valid focal receipts, form a fixed combination of the new-example derivative and the mean old-example derivative at **one common parameter state**, then clip and apply once:

    g_mix = alpha * g_current + (1-alpha) * mean(g_old_1, ..., g_old_8)

An alpha of 1/2 is an illustration, not a selected value. Exact G and approximate L compute their respective own-rule components; L is not converted into an exact-gradient hybrid.

Compare with ordinary focal updates followed by separately applied old-record updates using the same permitted examples, weights on the objectives and final consolidation budget. The sequential old derivatives are necessarily evaluated after the focal update, whereas the blended derivatives use the shared prestate: that is the intended change. Example exposure can match while optimizer applications and runtime differ; record both. Include an ordinary focal-only reference. A costly equal-example focal-repetition or actual-norm control belongs in the full protocol if required by its claim.

### Why it is distinct

Candidate 1 changes when sequential repairs happen. Candidate 2 changes the continued update objective. Testing both changes at once would obscure attribution. As scoped to continuation, candidate 2 cannot alter the already completed first correction or promise to prevent its initial dip.

### What would change our decision?

Retain it if it reaches the same declared old/new operating level with less degradation or less required consolidation work. Do not credit simple stalling: a mixture that preserves old answers by failing to acquire further corrections fails new-learning requirements. A lower average loss cannot erase individual-capability failures. If the step is smaller and no actual-norm control is run, report a joint-objective intervention result, not a uniquely directional benefit.

A follow-up fixed repair-quota comparison can measure how much cleanup it needs; it must not increase the allowed repair until each branch passes. Confidence-cap is a separately deferred alternative, not secretly included in this mixture.

## 6. Priority 3 — evaluator-triggered repair within a fixed budget

### Question

Once a repair operation is shown to work, can the same evaluator/reviewer allocate it only when useful, reducing average repair cost without allowing material deficits to accumulate?

### Concrete draft mechanism

Freeze the chosen repair operation, task, reviewer, data authority, adoption policy and overall disruption/recovery limits. Change only when finite repair slots are spent.

A proposed policy could use one fixed micro-repair at a scheduled check when the permitted evaluator reports that a defined repair band has been crossed. A final consolidation deadline caps how long it can defer a deficit. The number of slots, checks and repairs is finite; on budget exhaustion the result is an unresolved/failed cycle, not an unlimited repair-until-pass loop.

Compare with the same maximum repair resources allocated on a fixed schedule. A second predeclared fixed lower-work schedule may be useful to assess whether dynamic allocation beats simply doing less work everywhere; it must be costed before execution, not selected to match whichever result looks good afterward.

Representative mean-impact reporting and individual-risk warnings remain separate, following EVAL01. The trigger sees lawful operational evidence, not hidden research assessment scores. Repeatedly checking buffer records is part of the algorithm and cost, not untouched evaluation. A broader independent assessment set is needed for claims beyond the monitored buffer.

### What would change our decision?

An equal or acceptable performance/retention level at lower total repair-plus-evaluation cost supports usefulness. Lower repair cost that is offset by much more probing, excessive missed corrections, larger duration/extent of deficits or later catch-up work does not. Reject-all, HOLD-everything or indefinite deferral cannot qualify. The maximum quota matches between policies, but actual work is deliberately allowed to differ and must be reported, not claimed equal.

This is an allocation-efficiency candidate, not a replacement for establishing the repair mechanism first. No learned reviewer or Tertiary is required for the first version.

## 7. Decision sequence and limits

1. Prepare one complete protocol for Candidate 1 using the owner's full-cycle objective. Keep the evaluator simple and fixed. Do not launch another filter-only campaign.
2. If workable, compare degradation, recovery cost and surviving gain. If ongoing updates are the dominant reason it fails, consider Candidate 2 instead of only adding more maintenance.
3. Once an effective fixed policy exists, Candidate 3 can ask whether its work can be allocated more cheaply. It is not a prerequisite to a first usable cycle.
4. A real cumulative test follows a qualified/accepted bounded mechanism: persistent parameters, recorded lawful target revisions, new-task acquisition and repair debt across cycles. It remains essential for plasticity claims; the short proof of mechanism is not equivalent.

Before any run: one chosen contrast; selected task-level transient/residual limits and recovery deadlines; absolute acquisition/retention prerequisites; fixed development/confirmation roles; source/seed/scorer locks; full current and replay workload; actual storage/runtime feasibility; all negative and uncertain-completion evidence; and explicit run authorization. No new experiment was authorized by asking to see these candidates.

NBR-02 remains active. NBR-01's bounded closeout and every failed/stopped study remain intact. RET-MW01-FIT-001 is parked; Tertiary maintenance and self-play are deferred. The native-memory accounting issue remains open. FCR-0103-001 (foundation return after NBR-03, before NBR-04) is preserved. No frozen Primary change, Secondary/Tertiary concurrency, Validator authority change, neural overlay or additional core is adopted. The parent Architecture Ledger is not overwritten.

## Sources and verification boundary

- **S1:** NSS_NBR02_Learning_Repair_Objective_v0.1/OBJECTIVE.md — latest user objective and complete-cycle assessment.
- **S2:** NSS_NBR02_TIMING01_Analysis_v0.1/REPORT.md — reported trajectory, label-group and clipping observations; not independently rescored in this turn.
- **S3:** NSS_NBR02_TIMING01_Analysis_v0.1/CANDIDATES.md — prior proposed micro/macro, uniform/burst controls and continuation-mix concepts; no claim they ran.
- **S4:** NSS_NBR02_EVAL01_Execution_v0.2/REPORT.md — retrospective evidence-allocation comparison and report-semantics limitation; no new numerical reproduction here.

Exact file identities and byte sizes are in SOURCE_IDENTITIES.json. The source documents were read; only document writing, source-byte hashing and proposal-package integrity checks were performed. No source model, training script, data generator or numerical scientific evaluator was imported or executed.
