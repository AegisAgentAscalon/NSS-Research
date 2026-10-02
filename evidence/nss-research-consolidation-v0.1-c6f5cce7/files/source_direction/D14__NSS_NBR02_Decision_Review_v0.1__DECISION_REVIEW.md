# NSS research decision review: what are we protecting, and when?
## DEC-NBR02-SCOPE-001 · v0.1 · 25 September 2026

**Disposition: EXPERIMENTAL DISPATCH PAUSED by the user's instruction.** This is a source-based decision review, not an experiment, another retained-array analysis, or a new architecture qualification. No model was loaded, numerical prediction or derivative calculated, optimizer applied, experiment fixture run, or stimulus generated. The outcome below is a recommendation and a decision checklist, not a claim that the recommended mechanism works.

> User: “I also wonder if we could make a maintenance system filter out disruptions from weight changes. Honestly, a lot of this looks like we're treading over similar ground to NBR-01. This is going to seem strange, run a decision making pass. Let's not run any tests until we know for certain what we're testing.”

**Recommendation:** do not dispatch MICRO–MACRO or another maintenance sweep. First separate the learned-update question from the accepted-serving-revision question. Specify what may change privately, which behavior must remain usable, what counts as unacceptable loss, and how quickly a valid correction must become usable. Then select one mechanism and a comparison that can distinguish it from stronger controls. The uncertainty that must be removed before execution is uncertainty about the question and interpretation—not uncertainty about the eventual answer.

## 1. The central diagnosis of the research process

The recent experiments were not duplicates. They changed update strength, direction, replay content, and replay placement, and revealed distinct trade-offs. But the sequence has narrowed from the NBR-02 learning/retention remit toward optimizing one tiny model's confidence trajectory under a short, repeated binary-association grammar. The intended architectural promise has not stayed equally explicit.

We have been moving between at least four claims:

1. The raw learner's old answers never deteriorate at any intermediate parameter update.
2. A bounded learning-and-repair cycle returns it to acceptable behavior.
3. The serving system never exposes a degraded candidate revision.
4. A continually adapting learner retains its capacity to acquire later skills.

These are not interchangeable. A schedule can improve claim 2 without satisfying claim 1. A release gate can help claim 3 without making the learner satisfy claim 1 or 4. A frozen system can look excellent on old tasks under claim 3 while never learning a correction at all.

The analysis found that the initial shared clip-2 state already exceeded every held-out base's confidence envelope before either rehearsal schedule acted. A later operation cannot erase that recorded interval on those same states. Choosing a larger or more elaborate after-the-fact schedule does not address an all-intermediate-state prevention requirement. [S01 §§2,7; S02 §§1,4]

**Review judgment:** the next priority is to resolve this mismatch of target and intervention before spending another fitting budget. This does not invalidate the preceding measurements or excuse any failed screen.

## 2. Are we repeating NBR-01?

There is a shared engineering concern—preserve the right information while something changes—but different variables are changing.

| Track | Changed quantity | Typical failure | What is held fixed or supplied |
|---|---|---|---|
| NBR-01 bounded state/depth work | Stored/temporal state and internal processing; extension studies also changed observable evidence/workspace metadata | Wrong retrieval, stale task progress, missed composition | Learned weights frozen during scientific evaluation; some routing/validation supplied |
| Current NBR-02 short adaptation work | Learned parameters after lawful feedback or rehearsal | Old outputs or confidence change after a parameter update | Three-event cue construction; scratch state reset; known receipt correspondence; complete old toy buffer |
| State–weight compatibility bridge | A learned parameter revision while unfinished recurrent state is retained | Old state may not have the intended meaning under the new weights | No established migration operator; not exercised by these scratch-reset studies |
| Cumulative plasticity | Ability to learn across a continuing sequence of tasks | Future tasks become harder to acquire, even when recent answers remain good | Requires a longitudinal task-learning comparison; not measured by the six-receipt reset-per-base task |

The architecture already separates event-state changes, internal refinement, and parameter learning. TS01 trained a transition and then evaluated it at fixed weights. DC01/TIMING01 deliberately changed weights during the condition but reset temporary state for queries and restarted every base from an initial-fit checkpoint. Thus the recent effects cannot simply be called the old NBR-01 state-drift problem. [S03 §§8,14; S04 §2; S02 §1]

The parked `RET-MW01-FIT-001` asks whether learned task progress can be fitted/maintained when evidence changes. A new weight-acceptance mechanism would not answer that task-state question. A genuinely carried state surviving a model update is a third, integration-level question; it must not be invoked as the explanation for failures measured after a clean scratch reset. [S08; S03 §15]

**Decision recommendation:** preserve these as separate rows in the research map. Do not require NBR-01 to reopen because NBR-02 has interference. Do not claim NBR-02 resolves NBR-01 because a maintenance batch improves eight labels.

## 3. What the existing evidence supports

This table summarizes the supplied reports and analysis. This decision pass did not repeat their numerical checks.

| Evidence | Supported finding | Unanswered question |
|---|---|---|
| DC01 v0.5 | Exact G and the specified approximate L passed bounded competence, update/trace fidelity, adaptation/retention, and noninferiority screens. Delay 0/8/32 was invariant under a frozen cue-time record. | General temporal attribution, persistent learning across all conditions, practical trace-cost advantage, loss of plasticity |
| REV01 v0.4 | A one-time larger corrective step fixed every sampled first reversal; G violated confidence bounds and L also lost some old class answers. | A selective correction that is both fast and reliably preserves the relevant old behavior |
| PROTECT01 v0.3 | Development projection improved old confidence relative to a realized-norm control, but lost some strong-correction focal successes; valid local constraints allowed real finite-step margin decreases. Held-out not admitted. | General finite-step protection, held-out qualification, protection of unbuffered skills |
| REHEARSE01 v0.2 and its analysis | Old replay gave useful development confidence recovery without undoing focal corrections; subsequent focal updates reintroduced interference. Held-out not admitted. | Confirmed general recovery, sustained protection, rejuvenated plasticity |
| TIMING01 v0.1 and ANA-NBR02-TIMING01-001 | Both placements acted usefully on old mean loss; later placement usually improved the ending but worsened the worst intermediate mean loss. All old classes remained correct in the held-out grid. | A universal best schedule, restoration of lost classes in this sample, sustainable lifelong plasticity |

Sources: S01, S02, S04–S07. Repeated fits, cues, checkpoints, and replay are not additional independent task families. Internal independent scoring/replay is not third-party replication.

Two interpretations need particular restraint:

- **Confidence change is not automatically catastrophic forgetting.** Earlier REV01 did contain old class reversals; TIMING01's held-out grid did not. We should retain both probability quality and class correctness without substituting one for the other. [S01 §1; S02 §§2–4; S06]
- **The recurring label-group pattern is not a layer diagnosis.** Shared parameters are consistent with the observations, but the reports do not establish which layer, approximation, or representation causes all of it. G and L also arrive at different prestates. [S01 §5]

## 4. What a “maintenance filter” could mean

### A. Filter or constrain the proposed update

A rule transforms a raw displacement before it is applied, using legitimate retained evidence. PROTECT01 already tested one version: a local old-margin constrained projection. Its results show a retention–efficacy trade-off and the limit of a first-order constraint at a finite step. Calling a new mechanism “a disruption filter” is not enough to distinguish it from that tested mechanism. [S05 §§2–4]

A genuinely new candidate would have to specify what changes: the mathematical objective, the allowed support set, the finite-step criterion, the computation budget, or the learned state topology. None is selected here. There is no generic index of parameter coordinates that the current evidence identifies as “bad changes” and can safely remove without affecting the desired learning.

### B. Filter candidate adoption, not every internal update

Maintain an accepted serving revision and apply updates/rehearsal in an isolated candidate. Assess the candidate using legal observed records and declared current/old capability checks. Adopt it only through a controlled boundary. The accepted revision need not expose every candidate optimizer state.

This is the most promising **system interpretation to specify first**, because it matches the ledger's existing separation of candidate learning and serving adoption. It is not a new fifth core, overlay system, or retroactively validated runtime implementation. [S03 §§3,12,14–15; S10]

The candidate may privately deteriorate and recover. Its raw intermediate behavior remains scientific evidence. A served output protected by withholding adoption is a system-level result, not proof of an intrinsically noninterfering learner.

This design can also fail by never accepting anything. Keeping yesterday's model can preserve old answers while serving a now-obsolete focal answer. Therefore a useful adoption filter must be judged on **old competence AND bounded activation of lawful new learning**, with stale-answer time, abstention, coverage, rejected-candidate work, and memory counted. “Never commits” is a no-learning control, not success.

Finite regression checks protect only their declared coverage. If the toy guard checks every old record, its guarantee is restricted to that finite buffer and state contract. Repeated guard checks become part of the method's information and compute access; those records cannot simultaneously be called an untouched independent confirmation set. Hidden evaluator labels or future tasks must not enter the guard.

### C. Repair the candidate after an update

Ordinary replay, mixed updates, and the proposed MICRO–MACRO schedule address training/repair. They may help create an acceptable candidate. They do not themselves define when a candidate becomes served, and a late repair cannot retrospectively prevent an earlier raw failure. Their extra work and remaining failures remain visible. [S01 §§2,8; S09]

### D. Filter outputs, route to exact memory, or fall back

A downstream check may abstain or use an explicitly permitted exact record. That can be useful system behavior, especially for newly corrected facts. It does not repair the raw model's learned state. Any comparison must report the raw model, the served system, coverage, latency, and source attribution separately. A fallback that replaces every failed model answer is not evidence of improved neural memory. [S03 §§5,12,14; S08]

**Recommendation:** make candidate adoption the architectural containment boundary; keep update quality and repair as distinct learning questions. Do not rename the existing gradient projection or output checker as a new maintenance breakthrough.

## 5. A proposed lifecycle to clarify, not implement

Illustrative states, with no new implementation:

`accepted version → isolated candidate update → bounded maintenance → candidate checks → adopt or retain/defer`

The public receipt is recorded in the exact evidence system even when a neural update is deferred. Lawful current facts need not wait to become weights. Retrieving such a correction must be labelled as retrieval; it must not be counted as the raw learner adopting it. [S03 §§5,14]

A completed candidate transaction would bind at least:

- The accepted parent model and state/schema identifiers; permitted adaptive surface and scope.
- The observed event/receipt cutoff and current source revisions.
- Any pending eligibility/graph state, drained or cancelled/reconstructed under a specified lawful policy.
- The fixed learning and repair work budget; no post-score unlimited repair loop.
- The public guard data and separate untouched evaluation data.
- The accept/defer/reject reason, new/corrected capability, preserved capability, and acquisition latency.
- The exact package adopted and compatible live-state handling, with retained rollback.

No aggregate parameter hash is a substitute for reconstructible evidence. No small parameter norm proves preserved behavior. No confidence scalar is permission to release. The neural Validator remains a fallible adviser; authorized deterministic runtime/qualification policy owns adoption. [S03 §§4,10,12,15]

Primary remains frozen within its accepted generation. Its replacement remains a qualified generation change. A lab-level adaptive Secondary-like surface is not the deployed Secondary, and its parameters are not permission to mutate Primary. Tertiary can prepare grounded maintenance hypotheses/data in the deferred dream concept; it neither grants itself training authority nor becomes an acceptance oracle. Secondary/Tertiary mutual exclusion remains. A copied candidate is costed job state, not an additional continuously active personality. [S03 §§2–3,15; S10]

State migration is an explicit blocker when unfinished h is carried. Same shape does not establish semantic compatibility with new weights. Initial studies that continue using scratch resets would have to retain that limitation rather than claim online task continuity. [S03 §15]

## 6. The next research question should be joint, not a blanket “no disruption” score

**Recommended question for owner review:**

> Under a fixed legitimate-feedback and compute budget, can a candidate learning-and-maintenance cycle produce an adoptable revision that acquires the required correction while retaining declared old competence, and make that correction available within a specified delay—without hiding candidate failures, refusing all learning, or outsourcing the scored learning result to exact lookup?

This contains two result lanes, not one diluted pass:

1. **Learner lane (G09):** acquisition, old competence, raw intermediate interference, post-maintenance repair, and continued learning after repair.
2. **Adoption lane (G10):** accepted-revision quality, update-to-adoption latency, incomplete or refused learning, cost, and state compatibility.

Loss of plasticity needs another explicitly longitudinal endpoint: whether acquisition on later genuinely new tasks degrades after a continuing history of parameter changes. Resetting every base to the same initial fit cannot establish that. We should not describe either a safe release gate or a good eight-record refresher as rejuvenation. [S02 §1; S04 §2; S10]

**These are recommendations for a contract, not permission to run both research lanes at once.** Before any experiment, choose which lane is the primary causal comparison. The gate/serving policy may be held identical across learner arms, or the exact candidate training trajectory may be held identical across serving-policy arms. Changing both prevents clean attribution.

## 7. Measurement decisions that cannot be left implicit

### What is protected?

Protected targets must be current, legitimate, and scoped. Do not protect a revoked focal label as old knowledge. Distinguish factual exact records, reusable skills, derived progress, raw probabilities, and live recurrent state. Each requires a different check.

### Where is the system observed?

Preserve raw before-feedback predictions, all candidate intermediates, stage-completion candidates, and actual served outputs as separately labelled lanes. Candidate isolation is an explicit costed mechanism, not just a later scoring start. Neither moving scoring windows nor dropping early measurements is permitted.

### What loss is acceptable?

The historical confidence thresholds remain historical. TIMING01's analysis establishes that they are relative to moving B1, and that a relative PASS can accompany an increase in absolute old loss. It does not calibrate those thresholds to downstream harm, future forgetting, or real-world risk. [S01 §7]

For a new design, define the role of class error, log loss, margin, fixed-parent regression, moving-comparator differences, worst records, and adaptation delay. Report both mean and worst-case behavior within the declared sample. Do not require every parameter or probability to be identical; that is a different mathematical requirement from preserving useful competence. Conversely, do not dismiss confidence failures because classes happened to remain right.

No numerical tolerance is selected in this decision pass. The choice must follow the intended application/claim and be frozen independently of the next confirmation outcomes. Dropping an old guard merely because it prevented a pass is not justified.

### What does successful learning require?

A learner must acquire current targets and remain able to change again. A no-update or reject-everything control is required for interpreting an adoption mechanism. The checkpoint that remains safe forever while never learning cannot qualify. Training speed, number of real feedback receipts, repeated examples, and when a correction becomes usable must be distinct costs.

### What is the relevant comparison?

For a maintenance rule, use equal permitted evidence and account for extra replay/gradient work. For an adoption rule, compare identical candidate work with and without the proposed adoption boundary; never treat an exact gate's mechanical rejection of bad guarded candidates as proof of wider learned generalization. Include no-learning/stable revision and strong exact-task controls when applicable. A served-answer improvement alone cannot establish a learning-rule improvement.

## 8. Decisions and candidate dispositions

| Item | Disposition in this review | Reason |
|---|---|---|
| New experimental execution | USER_DIRECTED_HOLD | Latest user explicitly requests no tests until the question is clear. |
| MICRO–MACRO | HOLD_PENDING_OBJECTIVE | Useful schedule hypothesis, but after-the-fact repair cannot answer strict earlier raw prevention; higher work not yet a chosen need. |
| CONTINUATION-MIX | HOLD_PENDING_OBJECTIVE | Changes the update objective; should not be combined with schedule and acceptance changes. |
| CONFIDENCE-CAP | HOLD_PENDING_OBJECTIVE | Needs a current-target confidence standard and continued-correction test; not a guaranteed learning improvement. |
| A new gradient “filter” | NOT_SELECTED | Existing projection already covers one such idea; a new mechanism must differ precisely. |
| Candidate/adoption isolation | RECOMMENDED_DESIGN_SPECIFICATION | Consistent with retained lifecycle; not implemented or qualified here. |
| Longitudinal plasticity study | OPEN_REQUIRED_FOR_PLASTICITY_CLAIM | Current reset-per-base design cannot establish cumulative learner aging/recovery. Not dispatched. |
| NBR-01 return | PARKED / EXACT_TICKET_TO_CONFIRM | The workspace-fit ticket and original Q010 identity candidate remain different questions. |
| NBR-02 | ACTIVE_RESEARCH / DISPATCH_PAUSED | No stage closure or advancement follows from this decision review. |

Do not make a “pass something before we can return” loop an implicit research objective. Reopening an earlier question should follow its own named hypothesis and owner decision, not favorable random seeds or a conveniently loosened guard. The user's existing conditional return plan is preserved; this review does not silently cancel it or choose the skipped ticket.

FCR-0103-001 remains the broader return/consolidation checkpoint after NBR-03 and before NBR-04. No NBR-03/04 permission is created. NBR-01 stays closed at its accepted bounded recovered-evidence scope. Historical original training/RNG/verifier gaps remain gaps. [S08; S11]

## 9. Documentation drift found during this review

The latest analysis ZIP contains an intentionally inherited `program/INHERITED_PROGRAM_STATUS.md` still describing REHEARSE01 as a proposed next experiment. Its `program/USER_RETURN_PLAN.md` also retains earlier REHEARSE-specific wording. These are historical snapshots copied for context, not up-to-date dispatch authority. Likewise Architecture Ledger v0.1 predates the native workspace and NBR-02 executions: its older “untested” labels must not override later scoped results.

This review does not rewrite those source bytes. `CURRENT_STATUS.md` and `DECISIONS.json` provide an explicitly dated addendum. Use latest explicit user instruction for authorization, latest dated result for what actually ran, and the ledger for retained architectural boundaries. A document saying “can run after authorization” is not authorization during this hold.

The G01–G22 table is preserved verbatim with its original priority note. G09 (new competence without destroying old competence), G10 (when a candidate becomes served), G17 (interfaces across revisions), and G19 (continuity across replacement) are especially relevant. G14 dreaming/replay and G12 trace precision remain distinct questions—not automatic mechanisms or phases to launch.

## 10. Exit from the decision pause

The next preparation deliverable should be a one-page, owner-reviewed question contract, not a larger candidate catalogue. It must identify:

1. The protected capability and its current-evidence authority.
2. Whether the primary result concerns raw learning, repair at a stage boundary, serving containment, or long-term plasticity.
3. The permitted private-update/serving topology, adaptive surface, and state/receipt boundary.
4. Required new learning and maximum acceptable delay/abstention; a nonlearning baseline cannot win by freezing.
5. Primary metric, baseline, operationally justified tolerance, and mandatory adverse measurements.
6. One intervention and an equally informed, fully costed comparator that distinguishes its cause.
7. Data roles, cumulative/reset contract, fresh confirmation and unseen-skill limits.
8. Result-to-next-decision mapping, complete work/evidence budget and a later explicit execution instruction.

`NEXT_QUESTION_CONTRACT.md` gives that structure with unresolved fields left unresolved. There is no new batch count, learner fit schedule, threshold, model choice, or automatic resume in this package.

**Bottom line:** the meaningful goal is not “find a setting that never fails this confidence screen.” It is to learn how a system can accumulate useful changes while preserving the competence and service guarantees we actually require. We now pause to choose those guarantees and the mechanism being judged.
