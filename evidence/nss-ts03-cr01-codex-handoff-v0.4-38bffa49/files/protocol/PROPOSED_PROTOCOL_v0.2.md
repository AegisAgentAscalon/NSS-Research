# NSS-TS03-CR01 — controlled composition exposure and raw-output fidelity
## Proposed scientific protocol v0.2 — review only

**Status:** a frozen proposed design, not execution authorization, an executable source lock, generated data, a new fit, or a scientific result. Codex's v0.1 candidate is the source proposal. Reviewer completions are explicitly identified below and in REVIEW.md. The historical TS02-MW01 screen remains FAILED.

## 1. Question and limits

Does teaching the lawful concurrent revision composition improve raw learned progress and revision claims, and is the response different for the maintained-workspace configuration than for recurrence alone? The primary experiment is a **2 curricula × 3 architectures** intervention. It is not a contest between categorical tokens and an equally informed learned structured encoding, and it is not a new NBR-02 delayed-learning experiment.

C0 retains ordinary both-valid (0,0) metadata and separate advances to revision 1 or 2, but excludes both-valid (1,1). C1 re-pairs the same single-source trajectories to include (1,1), with matched one-source distributions and equal training budgets. Both exclude (1,2)/(2,1) from training, probes and development. Concurrent in-distribution success and asymmetric transfer must be reported separately.

The factorial experiment can measure a coverage-policy effect and an architecture-by-coverage interaction. **It cannot uniquely identify an internal transition defect versus an output-head defect.** Raw failure tables localize observable mismatches; changing a readout, retraining a decoder, or intervening on hidden state would require a separate experiment. All predictions depend on jointly trained state and heads. No assertion that a latent state is correct follows merely from a correct action.

## 2. Fixed public task and architecture

Retain the TS02-MW01 v0.2 execution semantics bound in SOURCE_IDENTITIES.json and the 36-member historical source lock. Those files were read as text and checked by hash, not imported. MODEL_CONTRACT.json reproduces the numerical interface.

There are two registered, software-routed task banks and four milestones per task. Milestones 0/1 depend on left evidence and 2/3 on right evidence. Exact controls track the revision of each completion, or NONE. A valid current record yields DONE only when the completion stamp equals its current revision; otherwise NOT_DONE. Missing/conflicting evidence yields UNKNOWN for the affected group. The next action scans milestones in the public goal order: the first NOT_DONE gives its step, the first UNKNOWN gives UNKNOWN, and all DONE gives DONE. Each group claim is its current valid revision, or UNRESOLVED. UNKNOWN is not permission to ignore a known answer.

The public controller provides authority checking, source registration, scope, index lookups, receipts, no-op filtering and protected task-bank selection. This is supplied code, not a learned writer/router or the architectural advisory Validator. Invalid requests remain observed/journaled but do not update the neural bank. Accepted GOAL, evidence and progress events update only the addressed bank. REGISTER, ACTIVATE and DISTRACT do not invoke a recurrent update. Accepted duplicate/older publications follow the original receipt rules rather than being silently filtered differently.

The same owner may publish the next revision, including after withdrawal. A contradictory payload at the same live revision creates conflict. RESOLVE chooses an already reported payload at the current conflicted revision. WITHDRAW marks that revision unavailable. **Publishing the same withdrawn revision cannot resurrect it; a new revision is required.** The withdrawal/restore family therefore uses a higher revision. Conflict resolution at the same revision is a different case.

Episode initialization clears all banks, registration metadata and workspace. A public task RESET is a learned event: it clears exact progress stamps in S/X, but the learned CARRY transition must learn the change. It does not externally zero CARRY, erase the current evidence/goal, or wipe the management packet. Queries are read-only. These distinctions match the retained TS02 execution source; no retrospective violation is inferred from the earlier informal word 'reset'.

| Architecture | Input / hidden per task | Parameters | Float32 weights | Two banks | Additional workspace |
|---|---:|---:|---:|---:|---:|
| R | 42 / 48 | 14,620 | 58,480 bytes | 384 bytes | None |
| R+ | 42 / 60 | 20,428 | 81,712 bytes | 480 bytes | None |
| RW | 62 / 48 | 17,572 | 70,288 bytes | 384 bytes | Ten uint8 IDs; learned 18×4 embedding |

RW has five fixed field-typed slots per task: goal, left revision/status, right revision/status. A lawful source-copying writer maintains them; it cannot store completion stamps, gold next actions, future events, repair masks or curriculum/family tags. The embedding contributes 20 float32 values to each admitted recurrent update. **Heads still read h only.** Do not add direct token-to-head access, a constrained decoder, postprocessed heads, a larger vocabulary or a learned writer in this experiment.

Use one GRUCell and one Linear(H,28), with four independent 3-category milestone blocks, a 6-category next-action block, and two 5-category binding blocks. Decode each by argmax, lowest-index tie break. Loss is the mean of milestone categorical cross-entropy, next-action cross-entropy, and binding cross-entropy, equally averaged across events, both banks and batch members. Do not repair one output from another. Inconsistencies are outcomes.

R+ is deliberately larger than RW, not an exact match for FLOPs, update dynamics or optimization difficulty. Exact S/X are programmed controls, not a learned information-matched structured workspace comparator. Any configuration-specific interaction remains narrower than categorical-token superiority.

## 3. Reviewer completion: a controlled marginal-matched curriculum

Each batch contains eight abstract episode slots. Their final target-source revision pairs before any optional conflict/withdrawal are:

| Slot | C0 | C1 |
|---:|---|---|
| 0 | (0,0) | (0,0) |
| 1 | (0,0) | (0,0) |
| 2 | (1,0) | (1,1) |
| 3 | (1,0) | (1,0) |
| 4 | (0,1) | (0,0) |
| 5 | (0,1) | (0,1) |
| 6 | (2,0) | (2,0) |
| 7 | (0,2) | (0,2) |

C1 is constructed by swapping the entire right-group component histories of slots 2 and 4, not by adding extra examples or training updates. For either source independently, revision 0 occurs in 5/8 endpoints, revision 1 in 2/8, and revision 2 in 1/8. Both curricula have ordinary jointly valid baseline. The deliberate change is their **joint correlation**: C1 adds (1,1) and compensating (0,0), while reducing the two mixed (1,0)/(0,1) cells.

This is an unavoidable part of matching marginals. The causal treatment is this balanced joint-support redistribution, not 'one isolated extra tuple with everything else unchanged'. C0 is a new controlled baseline, not a byte-for-byte rerun of old TS02.

DATA_CONTRACT.md defines the temporal block and component re-pairing. Within a batch, share the public nuisance schedule, task/goal context, payload recipe and component timing across eight slots; identities differ and are hidden from learned numerical embeddings. The right-source intervention re-pairs its whole evidence/progress trajectory. No right-source task consequence may be read from a gold table to construct a command.

Before training, independently verify equal per-side revision/status and event/receipt marginals at **every absolute public prefix**, not only the endpoint table. Report normalized component-history multisets, operation/acceptance counts, goal distributions and per-side label marginals. Joint progress/action targets may differ; that is the intended treatment. A construction failure is an engineering stop requiring a new lock/version, not permission to repair support after learning.

The valid revision supports are C0 {(0,0),(1,0),(0,1),(2,0),(0,2)} and C1 the same plus (1,1). Both exclude (1,2)/(2,1) even while a source is unavailable. The untouched task remains at (0,0) in training, with ordinary progress events; target bank orientation alternates. Status combinations from the declared conflict/withdrawal profiles do not authorize extra revision combinations.

All content/temporal templates differ from the old TS02 main E sequences. The old failure is a motivation, not a reused confirmation set. New names or IDs alone do not establish semantic novelty. Audit full-wire, normalized stream, and predeclared prefix overlaps; count and retain deliberate duplicates from block weighting.

## 4. Training, pairing and probes

Four paired fit seeds × six cells (C0/C1 × R/R+/RW) give **24 new main models**. Each receives 800 Adam updates, batch size 8. Alternate 17/33 stream events by zero-based update parity, plus the same 11-message public prelude. This is 19,200 main updates and 153,600 episode presentations, using 51,200 allocated C0/C1 streams shared across the three architectures. A paired batch has an underlying common recipe; the C0/C1 joint assignment differs.

Within each architecture/fit pair, C0 and C1 have **identical initial model bytes**, not merely the same stream seed. Adam is freshly initialized in both. Across different architectures do not claim weight equality. No model is continued from a probe, the old TS02 fits or TS01. A valid comparison uses both new curricula and all three architectures, not a newly trained RW against historical R/R+.

Retain the original uniform [-.125,.125] tensor initialization order and dedicated Torch initialization generator. Adam uses lr .001, betas (.9,.999), eps 1e-8, zero weight decay, no AMSGrad, foreach=False, fused=False; clip global gradient norm to 1.0. CPU float32, deterministic operations, single intra/inter-op thread, no compilation, dropout, mixed precision or GPU. Full BPTT within an episode; no carry or graph across batch episodes. Both banks are supervised after every public message, including prelude/no-ops. Gold appears only in loss/scoring.

Save full model/Adam/runtime-RNG/dedicated-generator/cursor checkpoints at 0,200,400,600,800: 120 main checkpoints. Six cost probes, one per cell, receive exactly 50 updates with 33+11 messages and discarded weights: 300 updates, 800 distinct C0/C1 streams, 2,400 presentations, 12 start/end checkpoints. C0/C1 probes within an architecture share initialization. Probe streams use their assigned curriculum support; neither sees asymmetric (1,2)/(2,1). Probes are a separate development-only cost set, not the scored 40-occasion development split.

No probe accuracy may choose the architecture, threshold, training recipe or number of updates. All 24 terminal main hashes must be locked before concrete scored development/held-out streams are generated. Development is diagnostic-only in this version. **Unlike the source's allowance for setting margins from development, all margins below are proposed now, before any new data.** No best-checkpoint, seed or family selection.

## 5. Evaluation and disclosure of generalization scope

Use two development families and four held-out stress families, four 65-event sequences per family after 11 prelude messages. Query after events 0,8,16,32,64. That is 24 main sequences/120 occasions: 40 development, **80 held out across 16 sequences**. Every six-cell/four-fit comparison uses the same main public streams.

The four held-out families are concurrent (1,1) after handoff, asymmetric (1,2)/(2,1), switch plus correction/RESET, and withdrawal followed by lawful higher-revision restoration. EVENT_TEMPLATES.json fixes all symbolic event positions. Variant rules swap target bank, initial goals and evidence-order orientation without changing the model interface. Each family is a **stress category with four sequences**, not an exchangeable random sample of four broad task populations. Report all sequence/fit/checkpoint results; no IID intervals over repeated fits/checkpoints and no invented population-level significance.

Every sequence has one unresolved checkpoint (event 8), four known-answer checkpoints, and the same five read times. This fixes a 4:1 known/UNKNOWN mix within each family (16:4 occasions). It is a disclosed balanced mix across families, not a claim of 50:50 class balance. Derive action UNKNOWN from the exact ordering rule, not a family tag. A failed class-allocation audit stops rather than resampling a difficult sequence. Global initial completion before the unresolved event ensures it is the first non-DONE requirement regardless of goal order.

C1-trained (1,1) success is coverage within that joint support, with new chronology. C0 did not train on it. Asymmetric (1,2)/(2,1) is reserved for held-out composition only: absent from training, cost probes, development and untrained fixture inputs. In the asymmetric template, take one source from 0→1→2 before the other reaches 1, so this family need not first pass through (1,1). Report both orientations. Revision 2 on either side individually is trained. A violation of the declared reserved support stops before main evaluation; do not silently relabel a contaminated confirmatory stratum. A separately approved redesign may call it covered, but is not this protocol.

Two development families test separately advanced sources (1,0)/(0,1) and (2,0)/(0,2), not the reserved asymmetric pair. The four-sequence untrained fixture exercises the control paths with fresh identities; its asymmetric-labelled slot substitutes a separate-advance recipe. All source rules are tested without teaching the reserved combination through a probe.

## 6. Controls and independent scoring

CARRY is the primary arm of all six learned cells. ZERO_EVERY_EVENT clears both learned banks before every public message but retains public metadata/workspace. PREFIX_REPLAY reconstructs the causal prefix from empty state with the same terminal model, no cached hidden state or future suffix. RW additionally has SLOT_MASK_EVERY_EVENT (embedding replaced by zero). Each intervention is a same-checkpoint information-removal or recomputation diagnostic, not a separately trained equal-cost competitor. Query heads remain read-only. Identical same-runtime carried/prefix states and logits are required.

Exact structured S and packed streaming X receive the same events. Check them with a separately implemented history oracle on every generated prefix, including all training data. S/X run once per unique occasion, not four duplicate times. Count their stamp storage, public directory, authority work, archive and lookup traffic. Perfect S/X can coexist with a failed neural study; no oracle is made artificially inefficient.

For every raw neural row retain milestone accuracy, whole-milestone correctness, next-action accuracy, primary joint correctness J, both-binding correctness B, group error counts, all-head correctness, wrong-DONE, missed valid progress, known-next abstention and true UNKNOWN behavior. Use descriptive UNKNOWN discrimination/coverage, not the word 'calibration' without a specified probability metric. Store full logits but no extra calibrated gate is fitted.

Wrong-DONE means raw next=DONE OR all four predicted milestones=DONE when true progress is not all DONE. Designated evaluations are known-evidence repair query positions 16 and 32; all other positions are reported too. Pure unsupported revision output errors are not described as executed unauthorized actions.

Cross-tabulate true milestone correctness × action correctness × binding correctness, and independently compute whether the raw action follows the raw milestone categories under the public goal. Also count raw DONE milestones whose group binding disagrees with current visible revision/status. These are observable consistency diagnostics; do not say that the hidden state itself is correct just because one head is.

**Shadow filter:** without hidden progress or oracle labels, reject a raw output if a binding claim disagrees with public current revision/status, or if raw action contradicts raw predicted milestone categories under public goal. It emits a separate MANAGEMENT_ABSTENTION; it never rewrites logits, copies a correct answer, or masks the raw score. Then the isolated scorer counts prevented wrong claims, residual errors and lost known recall. A wrong DONE consistent with wrong milestones and correct current bindings can pass this filter. Current metadata is not proof that derived work is correct. No shadow decision conditions future state or training.

No hidden-intent counterfactual forwards or additional targets are needed. The source-proposed information-limit question remains report-only; none of those labels trains a model, changes a filter or triggers an acceptance gate.

## 7. Separate decision labels (reviewer-proposed exploratory margins)

No omnibus pass may merge an explanatory result with a reliability qualification. Margins are frozen now and evaluated with integer counts; all zero requirements refer only to these finite observed tests.

**D1: coverage effect within RW.** Primary repair set P consists of events 16,32,64 in the three non-asymmetric held-out families: 36 unique occasions, each repeated over four fits. Require pooled C1−C0 gains of at least 5 percentage points in J and B (at least 8 additional successes out of 144 in each); J and B both improve strictly in at least three of four paired fits; their directions are both positive in at least two of the three contributing stress families; and designated wrong-DONE count does not rise. This supports the effect of the balanced curriculum intervention under this optimizer/budget. Compute the same contrasts for R/R+ rather than attributing a generic coverage gain uniquely to RW.

**D2: RW-specific coverage response.** Let d_a = score(C1,a) − score(C0,a) on P. In addition to D1, require d_RW−d_R and d_RW−d_R+ ≥5 points for both J and B, with a positive interaction for both scores in at least three paired fits and two contributing families. This is a configuration-by-curriculum interaction, not proof that categorical syntax is intrinsically superior. Report final C1 levels separately: a larger change can start from a worse baseline and still finish worse.

**D3: absolute bounded reliability.** For C1-RW, require at least 90% J (72/80) in at least three of four fits, **zero invalid raw group claims over all 640 held-out group predictions**, and zero designated wrong-DONE across every fit. Separate all-head reliability from J. No filter can turn D3 into a pass. Exact S/X must already pass engineering admission. Do not require that D1/D2 pass just to finish evaluating a D3 failure.

**Additional level comparison.** Report C1-RW minus both C1 recurrent controls on P and all held-out occasions. Claim the proposed advantage in final learned task level only if both J and B gain at least 5 points over each comparator on P without increased designated wrong-DONE. A D2 interaction alone is insufficient. This remains a bounded descriptive screen, not an efficiency or token-representation qualification.

**Asymmetric transfer:** report the 12 repair occasions and all 20 occasions in its one held-out family separately, all four fit pairs and both orientations. It is a narrow reserved-composition stress test, not enough independent families for a broad generalization claim. It is not substituted into P after inspecting results. Both curricula doing poorly here while C1 improves on (1,1) supports covered-composition learning without the desired transfer.

Engineering stops include malformed input, semantic mismatch, forbidden support leakage, unequal required marginals, S/X/oracle disagreement, hidden/future access, source mismatch, nonfinite values, or carry/replay failure. Poor accuracy, stale raw claims and inconsistent heads are scientific negatives: finish the authorized finite screen unless an engineering/resource stop occurs. Do not fix and continue on held-out data under the same lock.

## 8. Count ledger and host feasibility

CALL_AND_RESOURCE_LEDGER.json gives conservative potential cell/head counts, including skipped/no-op messages. Main CARRY/ZERO read both heads after every event; replay reads both only at endpoints. The common prefix length sum is (1+9+17+33+65)+5×11 =180. No extra query head is charged when CARRY's already recorded post-event head is reused.

| Item | Reservation |
|---|---:|
| Training/probe public event presentations and potential cells | 5,635,200 |
| Training/probe two-bank head vectors | 11,270,400 |
| Main capture + one fresh evaluation replay cells | 411,648 |
| Fixture capture + one fresh replay cells | 8,576 |
| All cell examples | **6,055,424 / 6,500,000 cap** |
| All head vectors | **11,699,248 / 12,500,000 cap** |
| Optimizer/backward attempts | **19,500 each / 19,500 cap** |
| Main learned query rows across arms | 9,600 |
| Main exact-control query rows | 240 |

The spare neural-call capacity is not permission for extra diagnostics or fitting. Charge before dispatch, including failed and unacknowledged attempts. A failed optimizer attempt consumes its slot. No restart may reset history; an incomplete 24-fit study cannot qualify as complete.

The inspected host has Python 3.13.5, NumPy 2.3.5, CPU-only Torch package 2.10.0+cpu, five visible/affinity CPUs but four CPU-equivalents of quota, and a 4 GiB container cap. These are package/OS observations only; no Torch import, model load or compatibility benchmark was performed. Current memory is a snapshot, not a peak or forecast.

Retain a shared two-hour wall ceiling from future authorization/preflight through numerical completion and delivery QA; 3 GiB process-tree RSS and 3.5 GiB container abort; 256 MiB new retained evidence and 64 MiB per delivery ZIP. Sample resources at least every .1 second; record gaps. Because 24 fits and 132 checkpoints exceed the old study's counts, **storage feasibility is not inherited from the 59.2 MB old ZIP**. The cap is tight and no compression ratio is promised.

Before main training, construct a complete static evidence-layout upper bound from fixed shapes/dtypes/checkpoint counts, including raw events, targets, consumed inputs, every trace, indexes, RNG, logs, manifests and partial-failure reserve. No selected negative may be omitted. Count canonical shared streams once and model-specific outputs separately. Lossless trace aliases may be used only after genuinely recomputing and verifying equality. A restored package must reproduce retained bytes, not regenerate new unrecorded scientific evidence.

After six fixed probes, admission requires: no cap already breached; static uncompressed bound ≤256 MiB; a conservative execution plan using twice the slowest applicable measured per-update probe cost, an additional 600 seconds for evaluation/audits and 900 seconds for packaging, plus already elapsed time ≤7200 seconds; and no measured resource overflow. These allowances are proposed admission rules, not proof the later work fits. If the admission check fails, retain all probe/fixture evidence, stop and request a new version. Do not reduce seeds/updates, loosen thresholds, truncate evidence or enlarge caps automatically. Monitor actual time/memory/bytes throughout.

## 9. Verification, evidence and remaining executable gates

SEEDS.json fixes digest byte syntax and allocation labels, with an explicitly serialized sorted-uint64-big-endian audit digest. No opaque unspecified aggregate is treated as verified. Direct/batch/wire integers were allocated without stochastic draws; component-seed expansion and actual input novelty remain required pre-generation audits. Both historical nonreproducible training and the old unspecified aggregate remain historical limits, not magically repaired by this new rule.

Before fixture or data generation, obtain separate user authorization, implement generator/controller/model/scorer, check every semantic choice against these documents, and lock all source bytes. Unit tests must cover every public event, revision jump/old/duplicate publication, same-revision conflict, withdrawal/no resurrection, reset distinction, both task scopes, malformed IDs, unauthorized requests, no-op routing, observed-prefix isolation, and corpus support/marginal construction. No such experiment implementation or tests were run in this review.

Then run an untrained three-architecture, four-sequence fixture and fresh process replay. Its accuracy is not an admission gate. Run probes only after fixture arithmetic/semantics pass. Lock all terminal hashes before main development/held-out instantiation. Fresh replay must start empty and genuinely recompute; it is not a second training replication.

Independent scoring may not import producer/generator/controller/model logic. Reconstruct all public semantics and labels separately, audit every consumed training event/target, and reconstruct saved float32 GRU/head operations in NumPy float64 using the unchanged empirical tolerance 2e-6 + 2e-5*abs(reference). This is not a proved error bound, and Q010's +2^-126 softmax amendment does not apply. Same-runtime bitwise replay is separate. Retain all failures and near-boundary readouts.

Required delivery includes all new event streams and per-prefix targets/inputs, source/split/seed locks, full model/optimizer/RNG/cursor checkpoints, all attempted/completed update curves, raw heads/states, controller/writer/authority observations, exact controls, shadow results, complete negative union, sequence/fit/family/metric interactions, replay receipts and restored relocation re-score. Do not duplicate or modify old study archives. No current result can be emitted because no new model or episode exists yet.

## 10. Architecture and phase disposition

ACP-TS03-CR01-001 retains the study-local ST-04 → IF-02 → ST-02 interface. The user's maintained organizer remains a bounded support for richer state and exact evidence, not an expanding transcript or token-elimination project. Residency, consultation and rewrite are distinct. Five fields, GRU dimensions, exact writer and protected routing remain experimental choices, not global NSS defaults.

Readout-access changes, constrained heads, factorized state, learned writing/routing, precision, cadence and larger architectures are explicitly deferred. Raw-head dissociation would motivate those tests; it does not authorize them mid-study.

The NBR-01 bounded-closeout proposal is still separate and unadopted. TS03 is a management-workspace extension, not NBR-02 delayed credit/retention and not a new mandatory gate retroactively added to NBR-01. No phase transition or Primary/Secondary/Tertiary/Validator role change occurs here.
