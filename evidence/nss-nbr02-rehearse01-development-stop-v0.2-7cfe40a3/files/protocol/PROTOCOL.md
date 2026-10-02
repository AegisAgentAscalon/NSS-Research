# NSS-NBR02-REHEARSE01 — recovery after a strong correction
## Reviewed proposal v0.1 • 25 September 2026 • NOT DISPATCHED

This is a prospective specification, not an execution result, an implementation lock, or user authorization.
It adopts Codex's single REHEARSE01 candidate and explicitly labels Chat's completions in REVIEW.md.
Normative companions: BATCH_AND_AUTHORITY.md, DATA_AND_ADMISSION.md, FIXTURES.md, WORK_AND_STORAGE.md,
WORK_LEDGER.json and SEEDS.json. Historical sources are read-only references, not dispatch scripts.

## 1. Question and evidence boundary

Can one paid batch update on eight lawful old records, immediately after a stronger changed-label correction,
restore old-answer quality without losing that new answer? Distinguish:
(a) successful correction, (b) intervening damage, (c) recovery, (d) sustained retention over the remaining
receipts, and (e) the benefit of selecting old rather than focal records.

The preferred predecessor, PROTECT01, stopped under its original A0. It did not receive a held-out
qualification. Its known development data may motivate this candidate but cannot confirm it.
REV01's complete retention failures also remain failures. No historical unused budget or model weights
transfer to this new study.

This is an eight-record buffered-rehearsal test. It is not Tertiary dreaming, learned replay selection,
plasticity rejuvenation, cumulative lifelong learning, general delayed credit assignment, or protection
of unbuffered skills. Each base resets to its method/fit's newly trained initial checkpoint.

## 2. Inherited numerical learner

Float32 dense tanh recurrence H=16, input D=23, two output classes:
    h_t = tanh(W x_t + U h_(t-1) + b)
    z = V h_3 + a
    p = softmax(z)
Parameter order W[16,23], U[16,16], b[16], V[2,16], a[2]: 674 parameters, 2,696 float32 bytes.
Input prefix: START coordinate22, PRIME coordinate20+scope, CUE coordinate0–19. Begin from h=0.
All five parameter tensors are adaptive in this laboratory, not serving Primary weights.

G differentiates the three-event cue prediction exactly by reverse mode when its target is released.
L uses the pinned diagonal-sensitivity recurrence in BATCH_AND_AUTHORITY.md; omitted cross-unit terms
remain intentional approximation. Rehearsal for L uses L's same rule, not exact old-record derivatives.
No QP, projection, changed topology, additional hidden recurrence, or new optimizer is introduced.

Plain SGD, eta=1, global raw-gradient norm clipping; no momentum, weight decay, schedule or projection.
Clip=1 on ordinary real receipts. Only U/F/R's first publicly detected changed-label receipt uses clip=2.
Subsequent real receipts use clip=1 for every branch. Queries never update model or public metadata.
Class is argmax of the two logits, choosing class0 on a tie. Score raw outputs without repairs.

CPU float32, deterministic operations, one intra-op and inter-op thread; no GPU, compilation, dropout,
autocast or silently changed numerical backend. Pin actual versions and build/configuration before
execution. The current host observation is package metadata, not a runtime compatibility pass.

## 3. Four branches with a common origin

Each six-receipt context uses f,p,f,f,p,f, where p is an old cue from the other scope.
The focal label silently reverses at receipt3 in the source grammar. The learner does not see a trial-number
reversal flag: it detects the first validated label unequal to the previous released label for that cue/scope.
All branches share the first two clip1 applications and the recorded original pre-feedback prediction.
After lawful changed receipt validation, fork the pre-update parameter state, authority state and source prefix:

| Branch | First changed receipt | Immediately afterward | Remaining real receipts |
|---|---|---|---|
| B1 | Clip1 | No extra update | Clip1 |
| U | Clip2 | No extra update | Clip1 |
| F | Clip2 | One clip1 batch on eight copies of this released focal example | Clip1 |
| R | Clip2 | One clip1 batch on eight distinct current old examples | Clip1 |

G/L branches are separate experiments. Four paired initializations are used for both learning methods.
Verify bit-identical parameters and raw cue gradients before the branch-specific clip. Reconstruct cue graphs
for copies using the same prestate and prefix; charge all three reconstruction exposures. Do not label
those recomputations as predictions made before feedback.

U/F/R post-clip2 parameters, raw logits and authority state must match before any extra update.
F and R each recompute eight gradients at their identical post-clip2 weights, independently, in fixed order.
Neither branch may inspect a score to decide whether to rehearse. Exactly one extra batch is applied,
even if its mean gradient is zero, the focal answer was already correct, or the batch causes harm.
No branch gets a retry, line search, gradient blend, extra rehearsal epoch, rollback or exact output repair.

F/R match eight derivative examples and one extra application; they are not resource-equal to B1/U.
F contains repetition, not eight independent observations. Source/data access differs intentionally:
F uses the focal record; R revisits old records. All record storage, retrieval and validation is charged.
An F/R tie does not establish a benefit from old-record selection.

## 4. Rehearsal arithmetic and lawful record reuse

All eight examples start from h=0, with no pending feedback. Every gradient is calculated at the same
batch-entry weights. Collect eight float32 raw 674-vectors; do not clip individual vectors or mutate weights.
Promote them to float64, sum serially in declared order, divide by8, and cast the mean once to float32.
This reviewer-specified reduction is a new batch convention, not a change to historical single-example steps.
Clip that mean once at1 using the pinned float32 norm and apply one inherited float32 SGD subtraction.

F's eight identical deterministic gradients mathematically average to one focal gradient; the specified
float64 reducer must reproduce the same float32 vector. Eight presentations do not multiply the effective
learning rate. Recompute and charge all eight in this control; no memoized gradient saving.
R's eight differing gradients may cancel or be small. A weak extra update is a scientific observation,
not permission to enlarge, rebalance, resample, or repeat it.

A batch references earlier validated source receipts and creates a REHEARSAL operation, not new feedback.
Its application ID and counter are distinct from the consumed-feedback cursor. Receipt3 is consumed once
per branch; the F/R extra update advances the parameter version, not the environmental trial number.
The live h/pending/eligibility state is empty after both operations. Read-only probes use scratch state.

The complete eight-old-record buffer is fixed; choose coordinates0..7, not the worst-scoring records.
Only current valid public labels are eligible. A missing, invalidated or conflicting expected old record
is an engineering stop under this fixed-eight task, never an excuse to skip or replace it with gold truth.
The focal cue is not in the old buffer; its obsolete pre-reversal label is never rehearsed as current truth.
Details, local equations, reduction fixtures and independent checks are in BATCH_AND_AUTHORITY.md.

## 5. Data, training, chronology and controls

Eight fresh initial fits: G/L × four paired seeds, exactly100 clip1 old-receipt updates per fit.
Initialization, ordered full-cycle old sampling, label-map stages, exact scope/cue allocation and IDs are
specified in DATA_AND_ADMISSION.md. Preserve checkpoints0,25,50,75,100, full parameter/RNG/cursor/public
buffer history, and every attempted/committed update. No performance-based checkpoint or fit selection.

Four fresh development bases and eight fresh held-out bases; one focal cue per base. Each main base starts
from the same initial-fit weights for a given method/fit. Old scope/cue grammar and simple binary pattern
overlap are deliberate limitations. Do not call a seed/ID change an unseen task; report actual overlap.

All main delays are0. The fixture separately crosses delays0,8,32. Waiting is detached from the cue-time
gradient; no main extra delay arm is added. Six receipts per context, with a read-only focal-plus-eight-old
inventory after every real application and after each F/R extra application.

Own frozen N_G/N_L receive the same public transactions from their corresponding initial-fit weights but
perform no online or rehearsal update. One N trajectory per method/fit/base, not four artificial copies.
Causal X is an ordinary last-released-label table with no privileged future labels. Its old records must trace
to public initial receipts (or declared synthetic fixture imports). X does not know a focal label or surprise
reversal before release. Run X once per base stream, not once per trained seed.

## 6. Readout timing and primary endpoints

Preserve every raw pre-feedback focal prediction. Those are not interchangeable with post-feedback results.
The intervention sequence at trial3 is:
    recorded original prediction -> valid changed receipt -> clip2 -> PRE_EXTRA inventory
    -> one F/R rehearsal application -> POST_EXTRA inventory.
For B1/U, the same trial3 post-real inventory supplies their unchanged value at POST_EXTRA.
Record that as a time-aligned reuse, not another inference or time-travel observation.

The recovery-primary endpoints are trial3 POST_EXTRA and the inventories after real receipts4,5,6.
At every endpoint score the current focal answer and each old class, stable log loss, correct-vs-other
logit margin and probability margin. Record paired broken->repaired and correct->broken transitions.
The trial2 shared post-receipt inventory is the pre-fork reference.

PRE_EXTRA harm is a mandatory raw result. A model may pass the recovery screen after transient harm, but
cannot be said to have prevented harm. A separate strict-no-transient-harm outcome includes PRE_EXTRA
as well as all later endpoints; it uses the same old-label/confidence requirements.

The first corrected answer is available only after the extra step. R is one-receipt learning with extra
computation, not a same-work or same-latency replacement for U. No uncontrolled latency benefit is claimed.

## 7. Prospective admission, separate from the archived failed gate

Only B1 and its own N supply development admission and confidence calibration.
Per fit: initial inventory must be8/8 and the 20 development primary B1 answers must have at least16 correct.
Define K BEFORE drawing development: the focal post-real-receipt answers at trials3,4,6 for each of the
four development bases, so |K|=12. It is not a list selected from N's errors or B1's failures.
Let H=12-N_correct(K). If H>0, require:
    2 * (B1_correct(K)-N_correct(K)) >= H.
This is the Codex-proposed >=0.5 net recovery of available frozen errors, not an accuracy confidence bound.
New mistakes on previously N-correct K occasions subtract from the numerator.

H=0 is PLASTICITY_UNIDENTIFIABLE. It is neither a fit pass nor a learner failure.
For EACH of G/L require at least3/4 fits jointly meeting absolute, informative and normalized-gain criteria.
If fewer than3 meet absolute floors, report ABSOLUTE_COMPETENCE_DEFICIT for that method.
If absolute capacity is sufficient but fewer than3 such fits have H>0, report CONTROL_SATURATION.
Otherwise a failed normalized-gain requirement is LEARNING_GAIN_SHORTFALL. Report every component for both arms.
If either group fails, finish the authorized development accounting/replay and stop before held-out generation.
If both pass, keep all four fits per arm, including any individual failure/uninformative fit.

F/R/U outcomes cannot calibrate admission. The0.5 requirement is a proposed pragmatic threshold inherited
from Codex's review, justified as demanding a material fraction of available focal learning opportunities
without demanding an impossible fixed count. It is not a discovered optimal threshold. Small H remains
unstable; publish K/H/net-gain counts, denominator sizes and class/loss results. Do not select seeds for H.

For each method, retain the prior FORMULA, not favorable old realized limits:
over all4 development bases ×4 fits × B1 trials3/4, compute each case's absolute change from trial2 in
mean-old loss and probability margin (mean across8 old cues). Let the medians be q_loss/q_margin.
    tau_loss   = min(.01, max(.002, q_loss))
    tau_margin = min(.02, max(.005, q_margin)).
Freeze those numbers, A0, source, initial-fit identities and scorer before drawing held-out maps.
Do not apply the new A0 retroactively to known PROTECT01 rows or revise that run's status.

## 8. Held-out scientific screens

Each method has32 first-correction observations:8 bases ×4 fits. They are not32 independent tasks.
Queries, old-cue lists and replay are repeated measurements. Publish all base/fit/branch/checkpoint rows.

E0: implementation fidelity, public authority and no future/gold access, atomic batch prestate,
single-clip mean arithmetic, fork equality, source/counters, no unknown completion, and exact fresh adaptive
replay. A failure invalidates/stops; it is not a scientific rejection of the rehearsal hypothesis.

D1 efficacy, R at trial3 POST_EXTRA:
* At least one net extra focal class success over B1 in at least3/4 fits.
* Positive base-average class gain in at least6/8 bases.
* Pooled focal loss no worse than B1.
* No paired loss of a focal class success U already had at its first-correction post-real endpoint.
Baseline-correct cases remain; a ceiling can make the gain gate unattainable and must be reported.

D2 old-label recovery/retention at POST_EXTRA and trials4/5/6:
every old class correct at the shared trial2 reference must be correct, with no additional old error
relative to B1 at the aligned endpoint. Preserve all baseline-wrong records in scoring and the buffer.
No recovered later answer erases an earlier failed recovery-primary endpoint.

D3 old-confidence recovery/retention:
for every base/checkpoint, averaging all4 fits ×8 old cues, and every pooled checkpoint,
R minus B1 mean old loss <= tau_loss; B1 minus R mean old probability margin <= tau_margin.
Report individual extrema and raw class flips even when a mean passes.

Combined recovery screen requires E0/A0, D1, D2 and D3. Run all admitted held-out cases despite valid
scientific negatives. Strict no-transient-harm additionally applies old checks at PRE_EXTRA and is a
separate outcome, never a rewritten definition of recovery.

R−F selection attribution is a predeclared exploratory paired contrast on focal and old quality, not an
invented post-hoc significance gate. A shared F/R benefit supports generic extra training; an R advantage
may support these retained examples under this budget, not arbitrary buffer selection or new neuroscience.
No overall memory, latency, plasticity-restoration or architecture superiority screen exists here.

## 9. Work, preflight and stop policy

WORK_LEDGER.json derives6,136 scheduled parameter applications including complete adaptive replay:
3,068 per pass. This replaces the incompatible earlier three-branch5,272 schedule.
Scheduled full-pair work is197,112 cell examples,63,464 heads,4,700 reverse-mode calls,4,700 local gradient
examples and3,712 replay-example retrievals. No QP or margin-gradient protection is computed.

Proposed hard caps:7,000 applications,260,000 cells,80,000 heads,6,000 G backwards,6,000 local
gradient examples. Count attempts before dispatch and all failed/technical work; spare capacity
is not permission to search, extend a fit or bypass a stop. A new repeated fit needs a new authorized study.

Two-hour shared active-work ceiling from post-authorization implementation through delivery QA;
3GiB process tree/3.5GiB container current;256MiB retained evidence and64MiB single delivery ZIP.
These are admission limits, not forecasts. Pin an explicit schema and actual-host cost projection before main fitting.
The current review host metadata indicates four CPU equivalents and a4GiB container, but no numerical benchmark.
Native/array-backing memory accounting remains open under OBS-DC01-COST-001.

Execution order after separate user authorization:
source/environment/seed lock -> non-neural and derivative/reduction/fault/clean fixtures -> costly rehearsal
probes -> record-kind/time/memory admission -> initial fits -> all development -> A0/calibration lock ->
held-out generation only if admitted -> independent full scoring -> fresh process repeats every executed
initial/probe/online/rehearsal/fixture application -> exact replay comparison -> relocated evidence rescoring.
An early stop is replayed only through its completed causal prefix; held-out work is never manufactured.

Unknown completion is a stop with last durable state, never a free automatic restart. Never weaken a detector
or remove negatives to fit a cap. Before an extra batch application, retain its intent, every example gradient,
the mean/clip, source-receipt provenance and prestate; commit only after required poststate evidence is durable.

## 10. Program, source and review continuity

Chat can prepare and execute user-authorized experiments without a further Codex turn. This document
does not authorize execution. A future Codex return receives the exact archive and evidence tiers,
not a claim of independent review during its absence.

NBR01 remains CLOSED_BOUNDED_RECOVERED_EVIDENCE; NBR02 active. RET-PROTECT01-A0-001 and
RET-REV01-RETENTION-001 remain unresolved historical tickets. RET-MW01-FIT-001 stays PARKED_OPEN;
RET-DREAM-MAINT-001 stays DEFERRED_DESIGN; FCR-0103-001 requires the foundation return after03 before04.
No NBR03/04 dispatch, role replacement, dream training, workspace reopening or historical requalification.
See PROGRAM_AND_ARCHITECTURE.md and the verbatim G01–G22 register.

The parent ledger, old archives and old gates are unchanged. No new model, event, label map, derivative,
numeric fixture or adaptive replay was generated by this documentation review. SEEDS.json contains only
hash-derived identifiers; historical seed scan, actual input novelty, implementation source hash,
record-schema size proof and numerical compatibility are pending execution admission, not claimed passes.
