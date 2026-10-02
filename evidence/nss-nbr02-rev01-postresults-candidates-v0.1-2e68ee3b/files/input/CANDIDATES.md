# NSS NBR-02 — candidates after REV01
## Selective correction, matched-state attribution, and rehearsal

**Version:** v0.1 · **Date:** 25 September 2026  
**Status:** CANDIDATE_DESIGN_ONLY. Not an execution authorization or a frozen executable protocol.

**Recommendation:** prepare **PROTECT01** as the next main intervention. **PAIR01** is a smaller, separately authorized diagnostic that can inform that choice without another initial-training campaign. Keep **REHEARSE01** as the simpler competing maintenance hypothesis; do not launch all three automatically.

Read this document and CHAT_PROMPT.md first. PROTECT01_TECHNICAL.md contains the proposed equations and controls. The budget file is an explicit planning envelope, not a measured runtime or a complete call ledger.

## 1. The evidence we are trying to improve

REV01 changed only the maximum norm of the first lawful changed-label correction, from 1 to 2. Its paired branches began from identical parameters and cue calculations. Both G (exact gradient) and L (specified approximate eligibility) improved to **32/32** first-correction successes, from **17/32** and **16/32** respectively. Both branches were already correct after the next corrective receipt. The intervention accelerated correction; it did not raise the eventual focal class score in that short schedule. [S1, §§1,3]

The result was a trade-off, not a complete pass:

* G preserved every tested old class answer, but exceeded the declared old-confidence loss/margin limits.
* L immediately lost five previously correct model/base/cue answers under the larger step. The same five stayed wrong at four subsequent checkpoints: twenty repeated errors, not twenty different memories. None concerned the repeatedly reinforced protected cue; that concentration is a lead, not proof that replay would repair the problem.
* G and L arrived at different learned prestates. Comparing their native retention outcomes does not isolate the approximation as the sole cause. The independent exact-at-L-prestate gradient audit did not execute the alternative full-gradient parameter update and score its consequences. [S1, §§4–5]

Receipt matching, saved learning information, gradient-formula fidelity, clipping, and application checks passed. The main question is therefore **how to change a learned association without excessive collateral change**, not whether the experiment merely applied the wrong receipt. [S1, §5]

These are short, exactly programmable association tasks. Exact causal lookup remains a required strong control. No candidate below establishes lifelong learning, recovery of plasticity, unambiguous temporal credit assignment, or a working Tertiary.

## 2. PAIR01 — apply both correction rules to exactly the same learner

### Question
Would the exact and approximate gradients damage the same old associations when applied to the **same parameter state, public cue, and released correction**?

### Why this is useful now
It distinguishes the immediate derivative intervention from the different histories that produced the G-trained and L-trained models. No new initial fits are needed. However, this is **not zero-work or inference-only**: it calculates derivatives and applies isolated counterfactual parameter updates on copies, each of which must be counted.

### Proposed comparison
Use every retained main pre-correction snapshot: four development and eight held-out bases × four fits × two originating methods = **96 prestates**. Preserve the old split names as provenance only: all of these cases are now retrospective diagnostic material, not fresh confirmation. Do not select only the five damaging cases or only B1 misses.

At each prestate, reconstruct the same lawful cue-time calculation and branch into:

| Applied derivative | Update norm ceiling |
|---|---:|
| Exact G | 1 |
| Exact G | 2 |
| Local L | 1 |
| Local L | 2 |

All four use the same prestate and currently released outcome. Score the focal cue and eight old cues immediately afterward. No further training tail is necessary for this diagnostic. Preserve the original archives and source checksums; new arrays belong only to the new counterfactual study.

Alongside actual class/loss/margin changes, compute each old cue's pre-update logit-margin derivative and its predicted first-order change. Compare that prediction with the actual finite-step effect. A correctly predicted damaging direction points toward interference; a favorable linear prediction followed by actual damage highlights a finite-step/nonlinearity limitation. Neither uniquely identifies the whole learning-history cause.

### Interpretation
If G is safer than L on the same prestate at the same norm, that supports an immediate update-rule effect there. If both damage the same associations, approximation alone is insufficient to explain the harm. If results depend strongly on which method trained the prestate, report a state-by-update-rule interaction. Do not replace the historical native-method scores with the better counterfactual.

**Illustrative workload:** 384 snapshot applications per pass, 768 with replay; sixteen allocated fixture applications including replay gives 784 scheduled, under a proposed 1,000-application cap. Snapshot extraction, both derivative calculations, old-cue sensitivities, all readouts and independent verification are additional work. See BUDGETS_AND_FREEZE.md.

## 3. PROTECT01 — steer the correction instead of just turning it down

### Question
Can one retention-aware update preserve the useful norm-2 correction while reducing the harm to old answers?

**ELI5:** rather than “make the push weaker,” try “push in a direction that changes the new answer without moving the old answers as much.”

### Proposed intervention
Retain a costed buffer of the eight old associations from their **actual earlier public receipts**, including cue features, scope, label, source receipt, and revision. At the first observed label change, calculate how a small parameter movement would change each old answer's correct-label logit margin. Project the ordinary norm-2 proposal onto the closest direction that does not predict a decrease in any of those margins.

Apply that projected update **once**. Do not repeatedly search until a post-update answer passes; do not roll back a scientifically bad candidate and omit it; do not enlarge its norm afterward. All later receipt updates use the original norm-1 rule, independently in each branch.

This is a proposed, per-record logit-margin constraint, motivated by the gradient-constraint approach in Gradient Episodic Memory. It is not an unchanged implementation of GEM, a new non-gradient law, or a proved finite-step safety guarantee. [P1]

### Four branches are necessary

| Branch | First changed-label step | Role |
|---|---|---|
| B1 | Ordinary norm-1 step | Retention/lag reference |
| B2 | Ordinary norm-2 step | Fast-correction reference |
| P | Projected norm-2 proposal | Selective-direction candidate |
| S | B2 direction, shortened to exactly P's step norm | Tests whether P merely helps by taking a smaller step |

If P and S do equally well, we cannot attribute the improvement to directional protection. If P simply refuses to move, the zero step is mathematically feasible but should fail the focal adaptation requirement. Preserve either result.

The S branch receives P's norm as an explicitly costed statistic from the old-evidence calculation. It is not an independently optimized clipping schedule or a cheap, ordinary focal-only learner. Both branches share public observations and obtain no held-out target from the scorer.

### The protection is deliberately a hybrid
For the first screen, use **exact old-margin derivatives for both G- and L-based candidates**. L still proposes its local focal correction, but L+P now uses exact derivatives as a retention guard. Call it a hybrid; do not say it remains an entirely local learner or claim the exact work was free.

The eight protected records also exhaust the toy's old-association inventory. Success would establish preservation of **buffered, explicitly revisited records**, not generalization to all unobserved old skills. The buffer and repeated access are new study resources.

### What a useful result must preserve
G and L are judged separately. Keep raw predictions; X or a validator must not repair the learned outputs.

Proposed screen: P satisfies the original REV01 efficacy rule over B1, loses no paired first-correction class successes relative to B2, and preserves old labels and the unchanged B1-calibrated confidence limits at all four tail checkpoints. A result that protects old answers by forfeiting fast correction is a trade-off, not the intended combined pass.

Evaluate the P-versus-S contrast separately. Evidence for steering needs more than passing when S passes too. Full base/fit/cue plots, actual step norms, projected fraction, and both first-order and actual margin changes are required. Thresholds and the solver's numerical rules must be frozen before a future source/data lock; the draft decision rules are in the technical companion.

### Likely failure modes worth learning from
A finite norm-2 movement may violate old margins despite satisfying the local linear constraints. The feasible projected direction may contain little useful correction. The old buffer may not cover other associations. Exact protection derivatives may cost too much. Keeping the old records stable may conflict with legitimately changing a record that was accidentally left in the protection set. Each has a distinct required log and test.

**Proposed scope:** four paired fits, four development/eight held-out bases, unchanged f,p,f,f,p,f chronology, main delay 0 and delay fixtures only. All four branches start at the same pre-correction point. Fresh main fits and mappings are for confirmation; prior REV01 errors remain regression/development evidence. The small binary grammar will still overlap and must be described honestly.

**Illustrative envelope:** 5,704 total update applications including probes, fixed fixtures, and full adaptive replay; proposed hard ceiling 7,000. The extra old-gradient and solver computations require a separate full cell/head/backward/native-storage ledger. This envelope is not proof that the workload fits.

## 4. REHEARSE01 — correct first, then deliberately practice the old work

### Question
Can a small, fixed rehearsal operation repair the collateral harm without undoing the new correction?

This is a simple alternative to projection, and a useful precursor to maintenance research. It does not implement dreaming or demonstrate restored plasticity. Episodic replay has an established research basis, but its outcomes and costs must be measured on this NSS task. [P2]

### Proposed three branches
All start with the same norm-2 first correction. Then:

| Branch | Extra operation before the next external event |
|---|---|
| U | None |
| F | One norm-1 update on a batch of eight copies of the just-corrected focal example |
| R | One norm-1 update on a batch containing the eight previously observed old associations once each |

F and R have the same additional update count and eight example presentations. F's duplicates are deliberate cost/exposure controls, not new independent feedback. Compute and charge the examples; do not call R equally cheap because both have one optimizer application. U is the cheaper no-rehearsal control and is not resource matched.

For L, recompute its specified local derivative separately from zero temporary state for every batch example at the common pre-extra-update weights; average raw gradients, then clip once and apply once. For G use its exact derivatives with the same accumulation order. No sequential hidden extra steps, no old derivative evaluated at a different version, and no fresh feedback invented from repeated data. The extra step is a separately logged rehearsal application linked to already released evidence; it must not consume the external receipt twice or bypass the duplicate-receipt check.

Inventory focal and old answers **immediately after the initial correction and again after the extra update**, then after every later receipt. Any interim old harm remains visible. If R repairs an old answer after initially breaking it, call that recovery, not prevention. Check whether the replay undoes the focal reversal.

The same lawful old buffer used in PROTECT01 is a training input here; access is not a privileged exact answer from an unreleased label map. Never replay the focal cue's obsolete label as an invariant to protect. Selection is uniform/fixed, not based on which held-out cases look worst.

A useful candidate would outperform F on old-label/loss/margin preservation while retaining U's focal correction. If F and R improve equally, additional learning effort rather than the old-data choice remains a viable explanation. If old answers recover but the new answer reverts, the conflict has moved rather than been solved.

**Illustrative fresh-study schedule:** same four fits and twelve bases; per base two shared updates plus tails of 4,5,5 applications. Including probes, specified fixture allowance and replay gives 5,272 applications; proposed hard ceiling 6,500. This is a separate alternative, not an add-on silently appended to PROTECT01.

## 5. Why not just change the head or freeze most weights now?

Changing the adaptive surface may be useful later, but it is easy to manufacture a near-exact lookup solution here. Each cue has a unique input coordinate. Training only its private input-weight column while freezing shared weights could avoid old-cue interference largely by construction. Such an arm is a task-specific parameter-isolation control, not evidence of a generally transferable learning rule.

Similarly, copying an old model as a teacher and adding a same-point distillation penalty is not automatically a protective **single** step. At an exact teacher match, that penalty's first derivative is zero. To have an effect requires a changed operation—multiple steps, a look-ahead penalty, or a constraint—and its cost must be counted. We therefore propose the explicitly defined projection or actual post-update rehearsal rather than an unspecified “retention regularizer.” This observation is a mathematical design check, not a new measured model result.

## 6. Common non-negotiable boundaries

Each candidate is separately proposed. No extra fits, models, inference, derivative calculations, synthetic episodes, or injected faults were run while writing this packet.

* The exact/approximate equations and their distinction remain explicit. All needed exact work in a hybrid is counted.
* Retain the public scoped-label-change trigger; do not use hidden reversal flags or the known position of trial 3.
* New training/protection records arise only from already released public evidence. A revision or contradiction invalidates old protection targets; an unresolved conflict cannot be repaired by consulting the scorer.
* Retain the original receipt, prestate, raw correction, actual update, probes and causal evidence chain. Class, probability loss and margins are distinct. Report mean and worst-case old changes; do not hide individual lost answers behind pooled means.
* Whole-study fits, reconstruction, fault fixtures and complete adaptive replay are charged in a new ledger. The closed REV01 ledger remains 4,024 applications; its 476 unused slots are not a successor's free budget.
* Use fixed B1-only competence and confidence calibration for a fresh main study, retain all four fits after group admission, and freeze thresholds before held-out generation. Never choose the algorithm, buffer members, solver relaxation or dose using known test errors.
* Preserve exact causal bookkeeping, frozen learned controls, data-overlap disclosures, source/seed identity, durable intent/commit/unknown-completion records, independent scoring, numerical checks, and a relocated archive re-score.
* OBS-DC01-COST-001 remains open. A new tensor table or alias fixture is not complete native memory accounting. No efficiency claim without the required measurement repair.

## 7. Practical choice for the remaining Codex reviews

Ask Codex to critique **one preferred PROTECT01 protocol**, using PAIR01 as an optional diagnostic and REHEARSE01 as the simpler alternative. Do not ask it to execute or implement three studies from this note.

The review should decide whether a same-prestate attribution test is worth doing first, identify the projection solver/numerical contract, check whether the strong norm-matched control makes the result interpretable, and supply a complete measured execution/storage budget before authorization.

A useful null result is possible: directional constraints may not leave enough room to correct quickly, or rehearsal may simply move the error back to the new answer. Those outcomes should create precise return records, not encourage unbounded searches for a favorable clipping constant.

**Central question:** can the learner change the association that should change while sparing the associations that should not?

## Sources and status

[S1] REV01 execution v0.4 REPORT.md, §§1–5 and8; archived source identities are in SOURCE_IDENTITIES.json. The latest result remains overall FAIL for G and L.

[S2] Reviewed REV01 scientific protocol v0.2, §§2–6; retained through its compact handoff. Its text describes its earlier proposal status; current execution disposition comes from S1.

[S3] REV01 DREAM_MAINTENANCE.md and current program register; deferred Tertiary concept and foundation-return boundaries retained.

[P1] Lopez-Paz & Ranzato, *Gradient Episodic Memory for Continual Learning*, https://arxiv.org/abs/1706.08840 . Constraint/projection precedent, not evidence for this exact logit-margin design.

[P2] Chaudhry et al., *On Tiny Episodic Memories in Continual Learning*, https://arxiv.org/abs/1902.10486 . Replay precedent, not a forecast of NSS results.

No original architecture, prior decision, parameter file or closed experiment record was modified.
