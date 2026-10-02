# IdentityBinding009

NBR-01 / Distinct records and provenance-aware recovery

**Research plan v0.1 | 21 September 2026 | PROPOSED — NOT_RUN**

Decision: first prevent a newly registered identity from taking over an older identity’s record. Then test whether recovery of established internal state should differ from admission of an external observation. Add genuinely informative context only in a separately labelled comparison. Do not launch another unrestricted threshold search.

## 1. Target and why it follows Study008

Question: can NSS preserve distinct entity–relationship bindings through registration, updates, disturbance and repeated reasoning, without forcing ambiguous inputs into familiar identities or rejecting useful established information? “Identity” here means a generated entity code, not a person or the companion’s personality.

| Study008 evidence | Consequence for this plan |
| --- | --- |
| A registered near-duplicate was distinct in the registry, but the learned binder reused an existing slot in 282/320 cases and changed older content in 246/320. [S1 §7; S2] | Measure storage ownership and unaffected records, not only the new answer. |
| At 32-tick maintenance intervals, nearest repair retained 99.38% established-chain accuracy; selective A/B retained 40.00% / 10.63%. [S1 §6] | Separate recoverable internal damage from unfamiliar external observations. |
| Selective gates handled ordinary unfamiliar inputs but rejected many q20 familiar inputs and accepted all tested near-novel0.1 inputs. [S1 §§3,7] | Do not expect the same vector-only threshold to recover origin information that is absent. |

## Scope boundary

Preserve the tri-core + Validator roles, exact evidence, scope/version boundaries, existing readers and useful repair controls. This remains fixed-evaluation-weight NBR-01. Offline candidate fitting is permitted only when the study is authorized; no optimizer runs during scored evaluation. No online learning, delayed credit, 1–8-bit study, new core, language-generalization claim, or deployment is included. [S4 pp. 3–6,20–21]

This document is a proposed protocol. No new candidates have been fitted, no Study009 benchmark has run, and no source release has been modified for it. Reported numbers above are Study008 results, not new measurements.


---

# 2. A testable identity contract

Working hypothesis: similarity may nominate an identity, but once a scoped identity has been explicitly established or resolved, writing must not silently choose another owner through a second fuzzy lookup. This is a proposed separation, not a demonstrated Study009 result.

## A concrete source-level reason

In the supplied source, State.event resolves source/value codes, then RecordStore.event invokes its learned matcher again to choose the physical slot. Existing-slot writes replace the value while retaining that slot’s older key. This path is consistent with the reported aliasing failure; inspection is not a fresh execution or proof of every cause. [S3]

Proposed write path: observation → supported scoped identity decision → candidate record selection → checked commit. Retain the identity decision and record owner as explicit versioned state instead of discarding them after projection. Scope/permission checks remain separate from all neural confidence.

## Two input tracks, never silently conflated

Resolved-identity diagnostic: use an identity returned by a real registration transaction or an explicitly identity-addressed permitted event. This supplies exact identity information, not a target slot or answer. It tests allocation and ownership after the identity decision is settled. Label it as an information-rich control, not solved recognition.

End-to-end track: supply only the declared observations to the resolver. Any handle is its own decision, possibly wrong; do not replace it with the generator’s true identity. Score resolver mistakes and binder mistakes separately, and count both in end-to-end task accuracy.

## State and transitions

| Proposed field or rule | Meaning / limitation |
| --- | --- |
| Scoped entity handle + lifetime/revision | Names an established catalogue entry. It is not evidence that its properties are true. A stale handle cannot name a reused entry. |
| Record owner: entity + relation type | Separate entity identity from physical storage position. Keep the existing single location relation in the main study; do not add a new relation task silently. |
| Relation presence and readability | Absent, present-readable and present-unreadable remain distinct. Registration alone creates no relation. |
| Atomic checked write / clear | A correction targets its declared owner; a clear removes that relation, not the entity. A denied or failed write changes no unrelated record. |
| Query and recovery restrictions | Queries cannot enroll identities. Recovery cannot manufacture a missing relationship, grant authority, or silently merge owners. |

Version the changed state schema and compatibility contract. Count owner handles, revisions, indexes and protections. Do not load the old snapshot under changed semantics just because the vector shapes still match. Inject stale/missing/corrupted ownership metadata as separate faults.


---

# 3. Candidates and fair controls

## A — Identity-keyed commit: the engineering control

Use a validated candidate entity handle plus relation type to locate the corresponding record or allocate a free one. Different active owners must not alias. The registry and checked commit use exact rules; the relation contents and existing neural reasoning can remain approximate. This tests how much of the failure is avoidable bookkeeping.

A cannot repair a wrong upstream identity decision. Its stable ownership metadata is additional protected information relative to the original vector-only store. Report this openly; do not call its success a learned binding breakthrough.

## B — A learned binder prepared for close-but-distinct entities

Continue the existing matcher on near-duplicate registered identities, valid corrections, new-record choices and missing-record cases. Target: select the correct existing record or NEW without confusing visual/numerical similarity with identity. Train only declared binder parameters; freeze after preparation. Retain a matched extra-training control using ordinary examples so more steps alone are not credited to hard-negative teaching.

The primary learned comparison uses the same numerical evidence as the inherited binder, without a scorer-supplied identity or slot at evaluation. Compare unguarded proposals and, separately, proposals checked against explicit owner metadata in the resolved-identity track. A guard must not hide a reject-all binder: report pre-guard errors, vetoes and successful writes independently.

## C — Informative context: conditional diagnostic, not a default expansion

After binding is isolated, add a second independently observed identity cue to ambiguous external queries. Compare an inspectable matcher with a small learned matcher only if the pilot justifies that cost. This asks whether extra information, rather than a more elaborate threshold on the same vector, addresses the uncertainty.

The cue must not be a hidden known/unknown flag, the target room, a true-ID label, or a future catalogue entry. Use present, missing, conflicting, shuffled and shared-corruption conditions. Compare with an equal-sized single-view representation and an equally sized duplicate of the first cue: extra bytes and correlated copies are not independent evidence.

## Controls retained

Keep the inherited binder, geometric A and learned B membership heads from Study008, nearest and learned restorers, and both frozen structured readers. Use exact traversal on the actual candidate-written store plus a separately isolated scorer graph. Keep reject-all and no-repair ablations. No oracle repairs the candidate’s store before scoring.

Do not mix A, B and C into one architecture ranking: they address different interfaces and may receive different information. Report matched-information contrasts separately from best attainable quality at a shared total-resource ceiling. A simple rule may be the preferred implementation for a discrete lifecycle contract.


---

# 4. Stage A — Separate records before adding noise

Priority: reproduce the structural failure on fresh close-identity pairs, with no storage corruption. Keep the reader, resolver and restorer fixed unless the specific comparison changes them. Distinguish improved allocation from easier identity recognition.

## The decisive paired-object test

Establish pouch A → study. Register a distinct but numerically similar pouch B. Before writing B’s location, query A, B and unaffected neighbors. Write B → workshop. Query both again and inspect the candidate’s actual record owners. Correct B → kitchen; A must remain in the study. Clear B’s location; A remains answerable and B’s identity remains registered. Rewrite B, reset the scope, then install fresh records.

Include independent variations with near-identical source keys, near-identical destination values, and both; rooms and intermediate entities should each be tested. Randomize codebooks, handle numbering, physical slot order and which object is written first. Labels and physical addresses cannot be memorized.

## Separate registration interference from write interference

Run register-only, denied-write, valid-write and correction branches from the same pre-event snapshot. Catalogue growth can change the resolver or reader’s competition even if record contents do not change. Do not blame every changed answer on overwriting. Compare the source receipt, stored owner, stored payload, reader’s selected path and final decoded identity.

Where exact traversal of the unchanged store succeeds but a frozen neural reader fails, record a read-interface failure. Do not secretly replace that reader’s selections with exact owner lookup. A separately labelled exact reading control is useful; silent oracle assistance is not.

## Metrics that an attractive answer cannot hide

| Measure | What it catches |
| --- | --- |
| Wrong-owner commits / eligible write attempts | A new relationship stored under a different established entity. |
| Distinct-record creation and valid-write acceptance | Rejecting every difficult registration/write is not a solution. |
| Untargeted logical changes after each transaction | Damage to older facts or relation presence/readability. |
| Old/new/unaffected answer correctness jointly | Correct new answers that conceal broken older ones. |
| Register-only versus write-induced differences | Changed matching competition without a content overwrite. |
| First failure location | Registration, resolver, binder, commit, repair, read hop or decoder. |

Compare logical records for neural trials, and byte-for-byte untouched state for exact no-op/denied-write transaction tests when maintenance is disabled. A legitimate numerical restoration can change bytes without changing the stored fact. Keep those checks distinct.


---

# 5. Stage B — Recover state without inventing certainty

Begin only after Stage A provides a structurally intelligible store. Freeze its candidate selection before scored comparisons. The purpose is to test the Study008 32-tick failure, not to widen every familiarity threshold indiscriminately.

## Separate source histories, not “trusted equals true”

External observation: identity must be inferred from the supplied evidence; unfamiliar and ambiguous cases remain possible. Internal field: the system has a real prior write receipt and a declared owner, but the value may still be wrong, changed or erased. The source class comes from execution provenance, never from a hidden familiarity label. A retrieved value used as the next query carries only provenance actually available to that read.

Compare the original shared membership/repair policy with a distinct internal-recovery policy. The latter may use declared redundancy, age since maintenance, owner consistency or a fixed set of alternative decoding candidates. Choose and freeze one small policy after pilot work. Preserve the original raw field for diagnosis; do not accumulate fictitious corroboration by rechecking the same data.

## What exact ownership can and cannot restore

A protected owner handle plus its catalogue representation can reconstruct that record’s source key. This is exact key rehydration from retained information, not neural rediscovery. It says nothing about the missing destination value. The main arm must not attach an undamaged destination handle or old graph as a hidden correct-answer copy.

If an exact destination reference/archive is used, isolate it as a separately costed redundancy control. An erased value is not recoverable merely because the source owner is known. A confidently wrong but valid destination code must be scored as wrong, not repaired by the ground-truth evaluator.

## Conditions and interventions

Test key-only, value-only, external-query-only and combined perturbations. Retain clean, 64- and 1,024-event horizons and maintenance cadence 1/8/32/read-time. Use paired disturbances and count actual work. Test directed movement toward a wrong valid identity, full value erasure, stale owners, wrong scope and common-mode corruption of added redundancy.

Permit reversible internal unreadability only under an explicit rule: further computation may recover available information, but repetition alone is not new evidence. If recovery remains ambiguous, expose unresolved status instead of selecting a confident answer. Evaluate rescue coverage and incorrect reinstatement jointly.

## Context diagnostic for the unresolved external cases

Retain Study008’s single-vector conditions and thresholds as reported references. Do not relabel q20 or near-collision failures as successes after adding a second cue. In the richer-input arm, test whether that cue specifically improves known-versus-novel separation; shuffle it to verify that the mechanism uses it. Identical-observable cases remain declared information-limit controls, not claims that all real identity recognition is impossible.


---

# 6. Stage C — Recheck the NBR-01 combination

Only the candidates with understood stage-A/B behavior proceed to the bounded combined comparison. Do not exhaustively cross every setting, model and stressor. Keep a fixed primary matrix and labelled secondary diagnostics.

| Axis | Proposed main comparison |
| --- | --- |
| Temporal retention | Retained state on/off. State-off removes information deliberately; retain same-evidence controls for architectural comparisons. |
| Internal computation | Query depths 1/2/4/8 with frozen learned parameters. Maintenance work does not increase with query depth. |
| Reasoning demand | Four- and eight-link chains, complete and missing; new generated structures and codebooks. |
| Time and disturbance | Clean and nominal 64/1,024-event conditions; extended/correlated stress is separately reported. |
| Updates | Register, write, correct, clear, rewrite, reset; near-duplicate objects and unaffected neighbors. |
| Continuation | Interrupt registration/commit/recovery and mid-query processing; resume identical supported state or fail compatibility explicitly. |

## What must not leak

No target row, correct next edge, true novel/known origin, future identity code, clean shadow payload, final room or unused scorer graph may enter the neural decision. A supplied exact handle appears only in its named information-rich track. Registration does not prove a relation, and model confidence never grants write permission.

Keep source/codec, owner, generation, relation revision and lifetime checks executable. Do not conflate record clear with catalogue deletion. Test stale handles after full scope reset/reuse. A result from an older snapshot must not overwrite a later correction when interrupted work resumes.

## Resource and evidence accounting

Report total active state, query workspace, owner indexes, codebooks, auxiliary cues, protected references, temporary peak and checkpoint storage. Count candidate fitting, calibration, replay and any input preparation. Report batch-one and batch timings on the actual host; no implied speedup on the user’s device.

Show quality against measured total query-plus-maintenance cost, not only number of sweeps. Separate matched-data, matched-compute and matched-state-budget claims; no single comparison can be assumed to match all three. Protect the existing exact controls and frozen reader checkpoints.

## Reproducibility

Use five paired inherited parent configurations with fresh data and candidate seeds where affordable. Pilot, fit, calibrate and main episodes must be disjoint. Lock source, candidates, thresholds, budgets and scenario counts before main scoring. Retain failed fits and every main seed. Recompute graph answers in an independent scorer; replay outputs and at least one training trajectory in fresh interpreters. Test state/RNG continuation. These are internal checks, not external replication or deployment qualification. [S4 p.21]


---

# 7. Decision criteria and stopping rules

The following are proposed mechanism-screening criteria. The pilot must fix sample counts, confidence reporting and resource ceilings before confirmatory evaluation. A requirement cannot be weakened after main failure and still be reported as passed. Report each pair and condition, not only pooled means.

| Requirement | Proposed decision rule |
| --- | --- |
| Ownership / transaction integrity | Zero observed cross-owner commits in the exact contract track; zero unrelated logical changes caused by a denied/incorrect commit. Any violation blocks engineering adoption. |
| Useful learned binding | At least 95% correct valid first writes/corrections/clears per pair; at most 1% empirical wrong-owner proposals/commits, reported separately before/after a guard. Guarded rejection is not a correct write. |
| Joint task behavior | At least 95% supported and missing-relation accuracy at sufficient depth in each declared core condition. Near-duplicate old/new/unaffected checks are core for this pass. |
| Prior capabilities | At most 1 percentage-point regression on paired clean and nominal recovery references, while meeting the declared useful accuracy floor. |
| Admission and richer evidence | Retain the prior ordinary-novel false-acceptance ceiling of 1% empirically; declare separate criteria for the richer-input arm. Single-vector failures remain visible. |
| Cost and uncertainty | Fit within the locked resource ceiling and report the quality/cost tradeoff. Zero sampled failures is not a proven zero-risk rate. |

## A useful pass may identify a boundary rather than a winner

If A prevents overwriting but the neural reader still confuses close identities, keep the storage correction and name the unresolved reader interface. If B improves by hard-negative teaching over equal extra rehearsal, retain that scoped evidence. If informative context helps only when genuinely independent, count that information benefit separately from architecture. If provenance-aware recovery revives wrong values, reject that policy.

## Do not make NBR-01 an endless identity-recognition project

After this pass, produce a consolidated state/depth status review: demonstrated task scope, required information/protections, unsupported conditions and remaining controls. Carry forward a bounded valid mechanism rather than requiring perfect recognition from intrinsically indistinguishable inputs.

Study009 alone does not close NBR-01. The original ladder still requires a competent conventional Transformer/explicit-state comparison and task/depth/horizon/resource evidence. Study008 explicitly leaves stronger generic controls and broader tasks open. Name the smallest remaining qualification measurement; do not silently begin learning or quantization. [S1 §10; S4 pp.20–21]


---

# 8. Deliverables, sources and plan status

## Planned study deliverable

A standalone research package beside the existing studies in MegaMind_Alpha_Proto, not a merged foundation release. Include the resolved protocol, hashes, source, fitted candidates, raw decisions and logical state changes, independent scoring, full results/failures, resource records and resume checks. Report KEEP / REVISE / REJECT / NAMED MISSING MEASUREMENT for each interface, not a single celebratory score.

## Basis read for this plan

[S1] NSS_NBR01_MembershipRepair008_v0.1/REPORT.md, executed 21 September 2026. Sections 3–7 establish the membership tradeoff, preserved nominal lifecycle, cadence failure and near-duplicate binder diagnostic; section 10 identifies the next candidate direction. These are the report’s results, not newly rerun measurements.

[S2] NSS_NBR01_MembershipRepair008_v0.1/evidence/NEAR_COLLISION_DIAGNOSTIC.json. Post-hoc, no-training diagnostic of the neural/exact discrepancy. Its status remains post-hoc; this plan proposes a new confirmatory test of that failure family.

[S3] Supplied NSS_NBR01_MembershipRepair008_v0.1.zip: nbr008/state.py, nbr008/pipeline.py and reference/nbr006/store.py were read directly from the archive. No source was edited. The nested resolver/matcher path motivated the identity-preserving commit hypothesis.

[S4] NSS_Cognition_Architecture_and_Low_Bit_Learning_Handoff_v1.0, 20 September 2026. Problem register G03–G07, interface rules, NBR-01 experiment ladder and confirmatory criteria (pp.5–9,13,20–21). The original document’s NOT_RUN labels describe its proposal date; later study reports establish their own execution status. The user’s later direction keeps 1–8-bit learning-state research deferred.

## Source identity checks

NSS_NBR01_MembershipRepair008_v0.1.zip
SHA256 680ed855b084f356f5de4d059fbc29323d5fa1b56e511b20956a91e25de8bae3

NSS_NBR01_MembershipRepair008_v0.1/REPORT.md
SHA256 2a20f2d1537b2828958dcdcf6f12de7db2fb49f4d58144581974a87cc484cc81

NSS_NBR01_MembershipRepair008_v0.1/evidence/NEAR_COLLISION_DIAGNOSTIC.json
SHA256 f8e182af550e695fd25f0fb86f8ac4b460da33c22a06d79f80eacb2f3f8265fa

Source hashes identify the inputs used for planning; they are not a new release qualification. No outside literature, connector write, model download, training job, benchmark or biological simulation was performed to prepare this document. All Study009 actions remain proposed and NOT_RUN.

## Recommended order

Start with identity-preserving allocation versus the better-prepared learned binder, without noise. Next isolate internal recovery from external admission. Only then add the small extra-evidence diagnostic where the observations are genuinely ambiguous. Finish with the bounded state/depth regression and a consolidated NBR-01 decision review.
