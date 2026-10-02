# NSS-NBR02-REV01 — first-correction dose
## Completed execution v0.4 / reviewed scientific protocol v0.2

**Disposition: efficacy passed for both methods, but neither passed the complete correction-with-retention screen.** Permitting a norm-2 step at the first publicly identified label change made all tested first corrections class-correct. It also reduced old-answer confidence beyond the declared limits in both methods, and created wrong old answers in the approximate learner. This is a measured adaptation/retention trade-off, not an overall pass or an efficiency claim.

The Tertiary dream-linked maintenance idea is documented separately under **RET-DREAM-MAINT-001 / CAND-NSS-DREAM-MAINT-001**, with a grounded rehearsal/qualification lifecycle. No Tertiary, dream process, maintenance training, or production-core integration was implemented in this study.

## 1. What actually ran

The inherited 674-parameter float32 tanh network uses START, PRIME(scope), CUE and two output logits. G calculates exact reverse-mode gradients. L calculates the pinned diagonal-sensitivity approximation, omitting cross-neuron derivative propagation. Both methods retain the DC01 model, initialization recipe, SGD learning rate1 and numerical order; all fifteen historical Q010 models and the saved TS/DC01 models remained unloaded and unmodified.

Four new initialization seeds are paired between G and L. Each initial fit receives100 old-association updates. Four development and eight held-out focal bases use fresh, scoped mappings. Each base restarts from its method/fit's fixed initial checkpoint and processes f,p,f,f,p,f. The first focal label is replaced by a different valid receipt label at its next presentation.

The controller detects that change from a legitimate last-observed-label table; it does not receive a hidden reversal flag. Both treatments receive the same paid table. From the common cue-time state, B1 uses clip1 and B2 clip2 **for that correction only**. Every other update uses clip1. B2 reconstructs the identical causal cue calculation; its reconstructed output is not presented as another before-feedback prediction. Both gradients are compared bit-for-bit before either branch is changed. The two branch tails and all post-update inventories are then executed separately.

Main development/held-out delay is0. A separate branched fixture tests0/8/32 detached filler events. Those fixture invariance checks are not another broad delayed-credit study.

Each main base/method/fit has two shared prefix updates and two four-update tails:10 actual applications. After every application the focal cue and all eight old cues are queried from reset scratch state. N_G/N_L freeze their own initial-fit parameters and process the same public records without adapting. X records only previously released labels and has no advance knowledge of a new association or reversal.

The first-correction denominator **32 per method** is eight held-out bases repeated across four fitted models. It is not32 independent tasks, and duplicate branch prefixes, later probes and replay are not additional independent observations.

## 2. Admission and fixed confidence limits

All eight initial old-cue inventories were8/8 correct. The B1-only development gate admitted G in3/4 fits and L in4/4 fits; the required group threshold was3/4. The one G fit that missed the relative gain floor remained in all results. Its17/20 development answers exceeded the absolute16/20 floor, but its gain over its frozen control was3 rather than4. No model or condition was selected away.

Before held-out mapping generation, the B1-only calibration fixed:

| Method | Allowed additional old mean loss | Allowed mean probability-margin decrease |
|---|---:|---:|
| G | 0.0075619681 nats | 0.0147790546 |
| L | 0.0100000000 nats | 0.0200000000 |

The values follow the exact proposed midpoint-median/clamping formula on development observations. They are pragmatic exploratory guardrails, not confidence intervals or established deployment-harm thresholds. B2 performance did not set or relax them.

## 3. First-correction efficacy

| Method | B1 clip1 correct | B2 one-time clip2 correct | B1 mean focal loss | B2 mean focal loss |
|---|---:|---:|---:|---:|
| G | 17/32 (53.125%) | **32/32 (100%)** | 0.875471 | 0.037884 |
| L | 16/32 (50%) | **32/32 (100%)** | 0.809712 | 0.016806 |

G's net gains across the four fits were5,3,2,5; every one of its eight bases improved. L's gains were5,6,2,3; seven of eight bases improved and one tied. Neither method had a class reversion from correct B1 to incorrect B2. Both meet the predeclared efficacy criterion. All first-change raw-gradient norms exceeded2, so this realized sample actually tested a doubled permitted step, rather than an unclipped no-op intervention.

Before the changed outcome was released, both adaptive methods were0/32 on the changed label. Those are unannounced surprises, distinct from the post-feedback misses. The common original prediction is scored once, not once per fork reconstruction.

After the next same-label receipt, **both B1 and B2 were32/32** in both methods. All later focal probes stayed correct. Thus B2 reduced first-correction latency on these instances, not final attainable class accuracy over this six-receipt schedule.

The causal paired intervention supports the effect of correction size under this particular rule, starting state and task. It does not establish that clipping was the unique reason for every historical DC01 miss, nor that norm2 is generally safe under noisy feedback.

## 4. Retention: the reason both overall screens failed

| Method/branch | Old class answers after correction3 | After receipt4 | After receipt5 | Final receipt6 |
|---|---:|---:|---:|---:|
| G, B1 |256/256|256/256|256/256|256/256|
| G, B2 |256/256|256/256|256/256|256/256|
| L, B1 |256/256|255/256|255/256|255/256|
| L, B2 |251/256|251/256|251/256|251/256|

Each cell is eight old cues × eight base instances × four fitted models. These are repeated probes of a small set of associations, not256 independent facts. All old labels were correct at the common pre-fork checkpoint.

**G retained every old class answer**, but old-answer confidence worsened more than permitted. Immediately after the first correction, mean old loss was0.004075 under B1 versus0.017008 under B2: a0.012933 increase, above G's0.007562 limit. The probability-margin decrease was0.025260, above0.014779. G fails17 of32 base/checkpoint confidence checks; pooled confidence passes at the last two checkpoints but not the first two. Correct classes are not proof of unchanged confidence, and this confidence deterioration is not evidence that a future class failure is inevitable.

**L incurred five old-association errors immediately after the larger correction**, and the same five model/base/cue cases stayed wrong at all four tail checkpoints. They account for20 repeated old-error observations, not20 different memories. B1 has three later wrong observations from one of those cases; B2 therefore has17 additional wrong observations relative to B1, plus20 losses relative to the correct common pre-fork labels.

The five B2 error cases are retained in `reports/OLD_ERROR_CASES.csv`: fit0/base8/cue7, fit0/base10/cue7, fit2/base9/cue2, fit2/base9/cue4, and fit2/base11/cue4. Two fitted models and four bases are involved; the errors concern three old cue identities. No affected old cue is the condition's repeatedly reinforced protected cue. This is a descriptive concentration, not proof of the missing protection mechanism.

L's old mean loss immediately after the change rose from0.004481 under B1 to0.079193 under B2; the0.074712 increase exceeds its0.01 allowance. Its mean margin decreased0.126025, above0.02. It fails30 of32 base/checkpoint confidence checks and every pooled tail confidence check.

| Predeclared decision | G | L |
|---|---|---|
| First-correction efficacy | PASS | PASS |
| Old-label preservation | PASS | FAIL |
| Old-confidence preservation | FAIL | FAIL |
| Complete dose-with-retention claim | **FAIL** | **FAIL** |

The exact causal control answers all held-out after-receipt probes correctly, including old associations. It still cannot predict an unreleased new association or an unannounced reversal. Frozen controls and their earlier errors remain separately scored.

## 5. Failure-first diagnosis and limits

Every natural gradient was checked against its own formula and every committed update against the prescribed clipped SGD application. L's raw gradient was also compared with the full exact gradient at **L's own pre-update weights**, not a different G model's weights. Branch reconstruction, parameter separation, label-table changes and every old/protected query were independently audited.

This lets us distinguish two observations:

* The31 held-out B1 first-correction misses (15G/16L) become correct under the paired larger update.
* The larger L update can turn a previously correct old answer into a wrong answer, even though the receipt, local rule, clip and application all meet their numerical contracts.

That is not a buffer-overwrite or wrong-receipt explanation. It is harmful interference in the tested learned mapping under the intervention. The records do not uniquely identify which hidden unit, parameter block, objective or omitted derivative contribution is responsible. G/L begin a base from their respective differently learned checkpoints, so their retention difference does not by itself isolate approximation error as the sole cause.

The primary capture includes18,170 scored neural query rows and **1,431 incorrect rows**, including cost/fixture data and frozen controls. `reports/FAILURE_INDEX.csv` labels these rather than pooling them into a single main failure rate. The first-correction category includes development as well as held-out observations. Exact-control diagnostics have separate rows. Fresh replay is not an additional scientific sample.

Thirteen non-neural contract tests and the fourteen-category failure catalogue passed. Coverage includes earlier/later first observed change, first-seen/no-change/second-change behavior, wrong scope/version/consumed IDs, branch isolation, independent gradient/application checks, missing evidence, quota/truncated-commit fixtures, and the explicit limit of authenticated false feedback without a public cue. Some fault checks are synthetic/copied-record tests; there is no claim of exhaustive live fault injection or formal information-flow security. The known NumPy alias fixture checks a7680-byte backing buffer without double-counting; it does not repair native graph accounting generally.

## 6. Execution history and storage repair

v0.3 completed the derivative/branched/fault fixture and the fixed cost probes, then stopped before any main initial fit. Its delivery projection was70,206,051bytes, just over67,108,864 (64MiB). It did not exhaust disk, memory or wall time. The168 attempted updates all had durable commits. The original source, records, stop and post-stop compression diagnostic remain in `attempts/v0.3`.

The storage-only correction separates exact JSON headers from their numeric payload and losslessly transposes four-byte lanes before whole-envelope XZ. On the already captured sample it reduced747,188bytes to666,600bytes without changing any decoded envelope. With the SAME2× margin and12MiB allowance, the revised forecast is63,991,104bytes. No learning setting, seed, target, scoring rule or guardrail changed. Encoding choice used stored data only, not extra model calls.

v0.4 initializes the fixture, discarded probes and all main fits freshly. Its first2,932,609 recorded bytes are identical to the entire old numeric prefix. It does not resume the discarded probe weights. The complete v0.4 capture and fresh adaptive replay each performed1928 applications. Adding the old168 gives:

| All attempts | Actual | Unchanged global cap |
|---|---:|---:|
| Update attempts / durable commits | **4024 / 4024** |4500|
| Cell examples |119184|180000|
| Head evaluations |38528|60000|
| Reverse-mode backward calls |2024|2500|

There were no unknown-completion learner updates, scientific fit retries, best-checkpoint choices, or outcome-dependent example removal. Deliberately wrong sandbox applications remain isolated and counted. Pending G graphs are not claimed as portable serialized graphs: source inputs, weights, forward states and derivative evidence permit reconstruction, while compressed delivery restores actual captured bytes without model execution.

## 7. Reproduction, counts and costs

Fresh adaptive replay reproduced **24,720 frames,71,400 arrays and11,946,576 numerical elements**, plus public requests/responses, event chains, plans, table/cursor states, the admission/calibration lock, exact controls and all11 final scientific files. Independent per-pass scalar audit checked5,770,152 values; maximum tolerance ratio was0.070091 under the unchanged empirical tolerance2e-6+2e-5|reference|. This is an empirical numerical tolerance, not a proved rounding bound. Q010's unrelated underflow amendment was not used.

Each pass contains102 verified forks,562 explicit checkpoint records,1928 update records and15,724 actual scratch queries. The earlier proposal's scratch-count label included frozen cue-time predictions; the complete head/cell totals were unchanged and are met exactly. Every planned record-kind count and maximum numeric shape was independently checked against the concrete schema. Actual maximum header size is12,314bytes; maximum decoded frame15,930bytes. Decoded-envelope size, encoded stored bytes and final archive size are distinct measures.

The measured execution environment is CPU-only Python3.13.5, NumPy2.3.5 and PyTorch2.10.0+cpu, one intra/inter-op thread. Main capture and replay were supervised separately. The higher successful-stage sampled process-tree peak was820,715,520bytes, and container peak2,034,774,016bytes.0.1-second sampling can miss brief peaks. Initial extraction and all unsupervised document/codec steps are included in the shared time clock but do not have continuous process-memory measurements. The clock was not reset after v0.3.

No overall memory or speed advantage is established. The inherited Python counter still omits some NumPy backing and native graph allocations. The public label tables, branch copies, reconstructed cue, query inventories, exact bookkeeping and instrumented audit cache are real costs. Canonical table bytes, recorded tensor components, call totals and sampled process memory are retained; complete per-operation deployment latency/native allocation measurements are not claimed. OBS-DC01-COST-001 remains open.

Fresh complete old/development/held-out label maps all differ from DC01's. However, every six-label condition pattern occurs in DC01's small binary grammar. New seeds/IDs do not make a new abstract task. The mappings, wire instances and initialized models are fresh under the specified recipe; no unseen-grammar or broad generalization claim follows. The novelty audit explicitly retains these overlaps.

## 8. Architectural disposition and next review

AER-NBR02-REV01-001 records an effective first-correction intervention with failed retention qualification. RET-REV01-RETENTION-001 asks how to improve adaptation selectively rather than merely increase the global dose. Any proposed old-skill rehearsal, constrained gradient, changed parameter surface or alternate dose requires a separately frozen comparison and an honest data/update/compute budget. A future exact-gradient counterfactual at L's same prestate could distinguish starting-state effects from gradient approximation, but was not run here.

RET-DREAM-MAINT-001 preserves the separate Tertiary-maintenance concept: source-grounded reflection and rehearsal planning, independently qualified synthetic targets, distinct candidate training and acceptance, old/current skill and new-task-learning tests, explicit state/trace migration, and rollback. Primary remains frozen and participating; Secondary/Tertiary mutual exclusion is not silently relaxed. Unverified imagined outcomes remain hypotheses. No dream selection or maintenance efficacy is inferred from REV01.

NBR-01 remains closed at accepted bounded recovered-evidence scope. NBR-02 remains active, with no automatic NBR-03/04 dispatch. RET-MW01-FIT-001 stays parked. FCR-0103-001 preserves the requested return to unresolved01–03 foundations after03 and before04. The parent Architecture Ledger and all original model archives are unchanged. Full G01–G22 wording is included in the handoff.

## Delivery

The full package preserves all new evidence and the stopped attempt. Lossless restoration recreates byte-identified records and exact duplicate files; it does not manufacture missing observations. Run `RESTORE_EVIDENCE.py` followed by `VERIFY_STUDY.py` after extraction. `RESCORE.py` operates on recorded arrays without training; adaptive reproduction is a separate authorized run and must never reset this study's closed attempt ledger. The external delivery receipt records final archive identity and relocated re-scoring.


### Delivery-only audit-footer correction

The first candidate archive restored and passed all272 listed-byte checks. Its independent numerical re-score reproduced all ten score/decision files, but the delivery wrapper rejected AUDIT.json: the original scorer had run immediately before CLOSE, and CLOSE then appended one WORKER_FINISH event. A later re-score correctly included that extra event and its terminal chain hash. No numerical fields differed.

The wrapper was corrected to require exact score/decision bytes and explicitly verify this single terminal append: type, predecessor hash, final hash, event-count increment and final work counters. All other audit fields must remain identical. It does not ignore arbitrary log differences or change the locked scorer. The failed wrapper/log/difference receipt are retained under audit/delivery_first_candidate. No new model call, gradient, update or score change occurred. The external final delivery receipt records the fresh extraction/restoration/re-score after this correction.
