# NSS Research Compendium v1.0

## Purpose and reading guide

Documentation snapshot: **29 September 2026**. This compendium organizes the currently retained NSS research by the broader question each pass contributes to, then records the specific question, compared systems, methodology, results and limitations of that pass. It includes 67 indexed entries across scientific studies, reconstruction/prototype work, retrospective audits, report-only records and prospective designs. The status on each entry matters: an indexed entry is not necessarily a completed experiment.

The coverage pass inspected the directory metadata of 52 canonical ZIPs under Research and the workspace root, alongside the retained reports and source documents. The companion evidence bundle includes 77 documentary source files. This is a compilation and source review, not a rerun, independent replication, new qualification or recovery of missing evidence. Original archives and earlier handoffs remain unchanged.

**Current priority:** low-bit inference and training, as directed by the user on 29 September. Earlier architecture, memory, competence and direct-generation questions remain open and deferred. A proposal in this document does not dispatch an experiment.

**How results are presented.** Each entry retains the documented arm-level aggregate outcomes, declared gates, negative findings and unperformed stages available in the reviewed sources. Individual event records, every seed-level row in large raw logs and numerical arrays remain in their identified source archives. Unknown method fields are left unknown. The evidence bundle preserves full primary reports and their tables for inspection beyond the compiled narrative; absent reports and execution payloads are called out rather than filled in.

**Evidence labels.** A retained archive means bytes are present, not that the study was replicated. Report-only means a supplied report documents a result while its original execution bundle is unavailable here. Retrospective audit means analysis of an earlier run, not a new fit. Prototype or contract tests measure their declared fixture. Proposal-only entries have no observed result. Historical failed gates remain failed even where a later test passes or a different operating tolerance is proposed.

**Historical versus current status.** The lookup and pass conclusions record the disposition at that pass. Earlier statements that NBR-01 remained open are historical: the later bounded closeout adopted Q010 v1.6 as a reconstructed reference while leaving identified fitting and missing-source problems open. No entry below reverses that closeout. Similarly, an earlier proposal can coexist with a later reported run; their versions and evidence are kept separate.

**Units and comparisons.** A correct answer, correct event, complete trajectory, admitted parent, snapshot and completed session are different units. Repeated snapshots from a shared parent are not independent trained systems. Rates from unrelated tasks cannot be pooled into an NSS accuracy score. Numerical equivalence, behavioral correctness, contained invalid drafts and successful external effects are also distinct outcomes.

The question groups below are editorial cross-references, not retroactive claims about preregistration. Each pass preserves its original protocol/version. G01–G22 links retain the older question taxonomy.

## Contents by broader question


- [1. How should components, records, permissions and actions work together?](#question-1) — 3 entries
- [2. What information survives bounded state, interference and retrieval?](#question-2) — 7 entries
- [3. Can processing depth, binding and repair preserve relations and identity?](#question-3) — 4 entries
- [4. What was qualified, reconstructed or left unrecoverable?](#question-4) — 3 entries
- [5. Can a learned task workspace maintain progress and transfer?](#question-5) — 4 entries
- [6. Can delayed feedback teach new behavior without losing old behavior?](#question-6) — 6 entries
- [7. When do repair, replay and accumulated learning help?](#question-7) — 6 entries
- [8. Can evaluation and revision preserve decisions and continuation?](#question-8) — 5 entries
- [9. Can segmented or externally backed context support larger workloads?](#question-9) — 6 entries
- [10. Can another writer improve on autoregressive output?](#question-10) — 3 entries
- [11. Can a reader interpret evidence and benefit from retrieval or preparation?](#question-11) — 10 entries
- [12. Which research proposals and unresolved questions remain open?](#question-12) — 10 entries

- [All-pass lookup](#all-pass-lookup)
- [G01–G22 question map](#g01g22-question-map)
- [Historical candidate-review register](#historical-candidate-review-register)
- [Archive coverage and provenance](#archive-coverage-and-provenance)
- [Evidence-bundle guide](#evidence-bundle-guide)

## All-pass lookup

| Pass | Type | Recorded status | Broader question |
| --- | --- | --- | --- |
| [Q001 — State, Depth and Learned Write Admission (Pilot001)](#pass-q001) | five-seed synthetic feasibility pilot with separately registered post-pilot interventions | completed; NBR-01 remains open; no architecture accepted | 2 |
| [Q002 — Longer Horizons, Addressed Memory and Write-Admission Uncertainty (HorizonBinding002)](#pass-q002) | registered bounded numerical-memory comparison; supplementary controls and post-hoc interface diagnostic | completed; NBR-01 remains open; no architecture accepted | 2 |
| [Q003 — Native State Recovery (StateRecovery003)](#pass-q003) | registered synthetic state-maintenance study using frozen learned representations, with separately labelled post-hoc diagnosis | completed; NBR-01 remains open; no architecture accepted | 2 |
| [Q004 — Stable Absence, Writable Lifecycle and Recurrent Empty-State Protection (WritableEmpty004)](#pass-q004) | paired five-seed synthetic lifecycle study with post-hoc local-dynamics, delivery and fault diagnostics | completed; dynamic presence retained as an engineering control; revised neural maps not adopted | 2 |
| [Q005 — Learned Existence with Frozen Content (ExistenceContent005)](#pass-q005) | registered five-pair synthetic writable-lifecycle study using frozen learned value codes | completed; learned split-state candidates passed nominal criteria but showed no quality/cost advantage over fixed rules | 2 |
| [Q006 — Content-Based Binding and Useful Processing Depth (BindingDepth006)](#pass-q006) | registered five-seed fixed-weight synthetic relational retrieval study with post-main diagnostics | completed; structured readers remain research references, not qualified serving cores | 3 |
| [Q007 — Compatible Restoration, Relationship Traversal and Failure Isolation (RepairBinding007)](#pass-q007) | five-pair fixed-reader synthetic restoration study with post-main diagnostics | completed; bounded building block; no general-memory qualification | 3 |
| [Q008 — Familiarity-Aware Repair and Writable Novelty (MembershipRepair008)](#pass-q008) | registered five-pair membership and repair comparison with post-hoc near-duplicate binder diagnostic | main comparison completed; full joint target not met; NBR-01 remains open | 3 |
| [Q009 — Distinct Records and Provenance-Aware Recovery (IdentityBinding009)](#pass-q009) | completed bounded five-pair NBR-01 study with paired binder preparation and separate rule-based cue diagnostic | exact owner-keyed storage retained as engineering reference; no learned pipeline passed the full joint identity target; NBR-01 remains open | 3 |
| [Q010-HIST — Qualification010 v0.1 historical result (original study bytes missing)](#pass-q010-hist) | historical scientific report and receipt; unavailable original execution archive | historical report claims bounded nominal qualification; original implementation, checkpoints, raw outcomes and source lock missing, not independently recomputable | 4 |
| [Q010-RECOVERY-BASE-v0.2 — Partial inherited-reader recovery and smoke](#pass-q010-recovery-base-v0-2) | read-only recovery package audit with retained bounded smoke receipt | recovery base package verified; smoke is explicitly not original Q010 qualification | 4 |
| [Q010-INF-REC-v1.6 — Reconstructed fixed-weight inference recovery](#pass-q010-inf-rec-v1-6) | report-based inference re-evaluation and local exact replay; no retraining | bounded inference recovery complete; original training protocol explicitly not fully requalified | 4 |
| [CM01 — Grounded reference packet for fixed-weight retrieval](#pass-cm01) | completed bounded fixed-weight interface pilot | completed; positive high-noise reference reconstruction with no general close-identity or net-efficiency claim | 2 |
| [CM02 — Reference continuity, revisions, and freshness policy](#pass-cm02) | completed deterministic information-management study with fixed reader exports | completed; workspace ties ordinary index; pooled gain over no selection varies with query noise; exact retrieval/revision policy stronger | 2 |
| [TS01 — Learned task-progress state](#pass-ts01) | completed supervised five-fit finite-state feasibility screen | bounded screen passed; no maintained workspace, memory compression or broad competence claim | 5 |
| [TS02-MW01 — Maintained workspace plus learned derived progress](#pass-ts02-mw01) | completed 15-fit training study with recurrent-only, larger recurrent and native workspace configurations | predeclared scientific screen failed; modest pooled gain did not meet fit/family/safety criteria | 5 |
| [TS03-CR01 — Controlled revision-composition exposure](#pass-ts03-cr01) | completed v0.4 24-fit crossed-curriculum study under reviewed protocol v0.2 | D1 coverage, D2 workspace interaction, D3 reliability and final advantage all failed | 5 |
| [CKA01 — Retrospective checkpoint learning/generalization audit](#pass-cka01) | completed exploratory post-result scoring audit of retained checkpoints; no training | TS01 saturates without observed late damage on sampled panels; TS03 had no earlier competent checkpoint and failed sampled familiar material | 5 |
| [NeuralProbe001 — Fixed small-model composition and recovery confirmation](#pass-neuralprobe001) | completed six-trial empirical neural confirmation within a software implementation audit | positive prescribed linear composition/recovery smoke test; no demonstrated modular accuracy advantage or broad NSS claim | 1 |
| [FND-AUDITS — Foundation engineering validation passes](#pass-fnd-audits) | compact matrix of thirteen deduplicated trusted-local engineering audits | bounded software gates reported per source; self-audits, not independent review or production qualification | 1 |
| [E07 — DC01 v0.4 preflight: delivery-size admission stop](#pass-e07) | engineering_preflight | STOPPED_AT_STORAGE_ADMISSION; no main learning fit | 6 |
| [E08 — DC01 v0.5: identified delayed feedback and bounded adaptation](#pass-e08) | completed_synthetic_learning_study | A0/D1/D2-G/D2-L/D3 passed within task; reversal misses and resource-superiority gap remain | 6 |
| [E09 — REV01 v0.4: a one-time larger correction step](#pass-e09) | completed_heldout_intervention_with_retention_failure | first-correction efficacy passed for G and L; complete screen failed for both on old confidence, and L also lost old labels | 6 |
| [E10 — PROTECT01 v0.3: projected updates trade correction for old confidence](#pass-e10) | development_experiment_stopped_at_admission | A0 failed for G (2/4 vs 3/4 required), L passed 4/4; held-out mappings not generated | 6 |
| [E11 — REHEARSE01 v0.2: strong correction followed by rehearsal (development stop)](#pass-e11) | development_experiment_stopped_at_admission | STOPPED_AT_A0; G passed 2/4 and L 4/4; held-out labels and conditions not generated | 6 |
| [E12 — REHEARSE01 v0.1 analysis: the same rehearsal gain was temporary under continued focal updates](#pass-e12) | retrospective_retained_data_audit | completed data-only analysis; E11 A0 stop and missing held-out assessment remain | 6 |
| [E13 — TIMING01 v0.1: early versus delayed old-record rehearsal](#pass-e13) | completed_heldout_timing_study_all_arms_failed_full_trajectory_gate | baseline passed; E/LATE passed focal/old-class screens but failed confidence; all complete gates failed | 7 |
| [E14 — TIMING01 v0.1 retrospective audit: later repair improves the ending but not the peak](#pass-e14) | retrospective_retained_data_audit | completed data-only analysis; original all-boundary failure unchanged | 7 |
| [E15 — C00-CONTRACT01: a synthetic change-and-review/adoption contract](#pass-e15) | synthetic_engineering_conformance_test | completed_finite_fixture_suite; v0.1 withdrawn after schema bug; corrected v0.2 passes declared contract fixtures | 8 |
| [E16 — EVAL01 v0.2: targeted review reduces harmful approvals but defers more useful changes](#pass-e16) | retrospective_finite_panel_policy_evaluation | completed_source-data_reanalysis; no new model execution or adoption | 8 |
| [E17 — MICROMACRO01 v0.2: a bounded complete distributed repair cycle](#pass-e17) | completed_heldout_mechanism_study_and_historical_adaptive_replay | D and B4 pass primary G/L screens with L exactly at 29/32; U and F4 fail; stricter mean-recovery sensitivity fails all old-repair schedules | 7 |
| [E18 — TEACH01 v0.1: a fixed Primary surrogate teaches a Secondary surrogate](#pass-e18) | completed_bounded_teacher_student_synthetic_study_source_reported | source report and delivery receipt document completed pilot; full named execution archive missing, raw fits/replay arrays not independently re-opened | 7 |
| [E19 — STATEBRIDGE01 v0.2: retained task state under changed weights](#pass-e19) | completed_diagnostic_execution_with_historical_adaptive_replay | NOT_QUALIFIED: original whole-trajectory numerical gate failed 11 comparisons; changed-weight continuation and rebuild adequacy screens both fail after repair | 8 |
| [E20 — SURFACE01 v0.1: fixed-weight baseline failed zero false-DONE admission](#pass-e20) | completed_fixed_weight_baseline_execution_admission_stop | three of four parents pass; parent 4103 fails zero false-DONE gate with one connected six-prediction episode; correction/adaptation and confirmation histories not run | 8 |
| [SH01 — First shared typed-record / HSA maintenance reader](#pass-sh01) | completed learning and integration study | three complete paired seeds; fourth HSA fit stopped at step 200 | 9 |
| [SH02 — Clean graph, plan, and packed HSA execution](#pass-sh02) | engineering refactor and saved-model regression | completed; tolerance/class parity passed; historical bitwise replay failed and is retained; no training | 9 |
| [SC01 — Exact backward-closure segmented workspace](#pass-sc01) | completed bounded component study | all 324 main conditions complete; same-class and numerical parity; efficiency gain modest/workload dependent | 9 |
| [SC02 — Incremental publication, scheduling, and neural-cache ablation](#pass-sc02) | completed engineering and workload comparison | completed; publication/scheduling gains with workload-dependent costs; intermediate neural cache slower in all tested cells | 9 |
| [CAP01 — Exact computation across active record tiles](#pass-cap01) | completed computation and engineering study | completed; exact outputs under declared checks; tile-size/cost tradeoffs retained | 9 |
| [CAP02 — Mixed-size preparation with small-task retention](#pass-cap02) | completed preparation and retention study | completed; larger-task results and small-task retention/cost limits documented | 9 |
| [DARP01 — First token-level plan / check / edit writer](#pass-darp01) | completed bounded generation study; consolidated-report evidence | completed; substantial writer errors and no working point | 10 |
| [DARP02 — Common metadata wrapper and repair/revision preparation](#pass-darp02) | completed continuation/preparation study; consolidated-report evidence | completed; completion improved but two-of-three working point and broad typed-feedback advantage not established | 10 |
| [DARP03 — Actual writer-error rehearsal and prospective keep-or-park comparison](#pass-darp03) | completed bounded comparison; consolidated-report evidence | both prospective quality and efficiency routes failed; park current DARP implementation | 10 |
| [RECOVER01-v0.2 — Ordinary replay recovery after new association learning](#pass-recover01-v0-2) | report/plan-reported completed diagnostic | strong reported recovery; residual false-DONE and strict numerical failure; original report absent from bounded source set | 7 |
| [TRACE01 — Guided replay from observed degradation](#pass-trace01) | source-reported historical diagnostic | technical stop with partial confirmation after numerical failure/storage stop; no qualified guided-replay superiority | 8 |
| [CYCLE01-A — Two-night maintenance feasibility](#pass-cycle01-a) | completed development-feasibility study; embedded report source | balanced replay signal promising; 5/8 candidate nights accepted; all results development; reserved main not run | 7 |
| [CYCLE01 — Repeated day/night learning roadmap](#pass-cycle01) | roadmap proposal | general repeated-cycle question remains open; CYCLE01-A was only a two-night development branch; CYCLE01-B not started | 12 |
| [CYCLE01-B — Longer fresh-confirmation comparison (proposal)](#pass-cycle01-b) | next-pass proposal | protocol and reserved run not started | 12 |
| [BRIDGE01 — Dummy orchestrator bridge and simulated action journal](#pass-bridge01) | completed bounded integration prototype; report evidence | 216/216 authored sessions complete; 4,144/4,144 recurrent event matches; no language model or low-bit execution | 1 |
| [BALANCE01 — Current-evidence rehearsal crossed with update size (proposal)](#pass-balance01) | proposal only | not run; do not infer evidence from CYCLE01-A BALANCED arm | 12 |
| [DIRECT01-SPEC — Parallel structured output versus autoregressive readout (proposal)](#pass-direct01-spec) | conditional protocol proposal | documentation complete; no model/readouts/experiment selected or run | 12 |
| [LB01 — Low-bit inference weights and recurrent state (protocol proposal)](#pass-lb01) | low-bit protocol proposal | not run; first low-bit protocol preparation priority | 12 |
| [LB02 — Compressed learning-state memory (proposal)](#pass-lb02) | conditional low-bit training proposal | not run; exact method and fixture unselected | 12 |
| [LB03 — More aggressive precision and low-bit update paths (conditional proposal)](#pass-lb03) | conditional later proposal | not run; gated on informative LB01/LB02 results | 12 |
| [ADAPT01 — One computation-preserving update mechanism (conditional proposal)](#pass-adapt01) | conditional roadmap proposal | not run; on hold behind current low-bit priority | 12 |
| [BUDGET01 — Measure and reduce a demonstrated resource bottleneck (proposal)](#pass-budget01) | conditional roadmap proposal | not run; may move earlier only if measured resource constraint blocks feasibility | 12 |
| [INT01 — Integrate only components that earned a place (proposal)](#pass-int01) | conditional integration proposal | not run; broader integration on hold | 12 |
| [COMP01-A — exam and exact-field scorer engineering only](#pass-comp01-a) | engineering_only_test_preparation | COMPLETE_ENGINEERING_ONLY | 11 |
| [COMP01-B/SETUP — pinned language-reader route selected, acquisition blocked](#pass-comp01-b-setup) | engineering_setup_model_acquisition_blocked | ENGINEERING_ONLY_MODEL_ACQUISITION_BLOCKED | 11 |
| [LAB01 — first three fresh autoregressive reader fits](#pass-lab01) | completed_bounded_training_inference_diagnostic | COMPLETE_BOUNDED_DIAGNOSTIC_REFERENCE_NOT_READY | 11 |
| [LAB02-SIZE — three widths, no consistent width gain](#pass-lab02-size) | completed_bounded_size_diagnostic | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CONSISTENT_WIDTH_GAIN | 11 |
| [LAB02-BIND — mixed versus staged binding curriculum](#pass-lab02-bind) | completed_paired_curriculum_diagnostic | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CURRICULUM_GAIN | 11 |
| [LAB-READER-DECISION — park reader preparation and route to handoff diagnosis](#pass-lab-reader-decision) | documentary_route_selection | ROUTE_SELECTED_READER_PREPARATION_PARKED | 11 |
| [LAB-SEMANTIC-REVIEW — corpus review recorded, retrospective adjudication pending](#pass-lab-semantic-review) | documentary_review_and_prospective_policy | NEW_CORPUS_REVIEW_COMPLETE_RETROSPECTIVE_REVIEW_PENDING | 11 |
| [MEM01 — bounded handoff and compact-scope retrieval diagnostic](#pass-mem01) | completed_bounded_frozen_reader_handoff_diagnostic | COMPLETE_BOUNDED_HANDOFF_DIAGNOSTIC_READER_LIMITED | 11 |
| [PREP01 — query-independent source sheet versus retrieval/cache controls](#pass-prep01) | completed_bounded_frozen_reader_preparation_diagnostic | COMPLETE_BOUNDED_DIAGNOSTIC_WORKSHEET_TRADEOFF_NO_ADVANCE_GAIN | 11 |
| [READER-SUPPORT01 — answer-only versus answer-plus-source supervision](#pass-reader-support01) | completed_paired_reader_training_and_inference_diagnostic | COMPLETE_BOUNDED_DIAGNOSTIC_NO_PRIMARY_GAIN_OUTPUT_CONTRACT_LIMIT | 11 |

<a id="question-1"></a>

## 1. How should components, records, permissions and actions work together?


<a id="pass-neuralprobe001"></a>

### NeuralProbe001 — Fixed small-model composition and recovery confirmation

**Broader question category:** Can the bounded training/evaluation harness train a small frozen Core plus modular A/B overlays to solve a prescribed composition task, preserve old behavior through A2, and reconstruct a state after transition? (Weakly related to G02 baseline competence and G17 exchanged information/revision, but the experiment is chiefly an engineering neural probe; it does not answer broad NSS architecture questions.)

**Specific question:** On a token-wise synthetic linear task with atomic symbols seen during training but pairs held out, do modular A+B composition, a matched joint control and a newer A2 candidate retain exact symbol-pair correctness across two numerical modes and neural recovery?

**Type and status:** Completed six-trial neural confirmation within NeuralProbe001's software implementation audit. The protocol was fixed before these confirmation trials but was not independently preregistered or protected: developer-visible data and feasibility pilots existed. It is positive evidence for a deliberately easy prescribed linear composition/recovery setup only. This is not a broad model comparison or proof that “tri-core” neural specialists compose on realistic tasks.

**Systems and arms:** Core is a 512-parameter identity transducer, frozen before candidate training. Separate A and B adapters have 128 trainable parameters each; A+B joint candidate has 256. A2 is a new candidate version after the prior A/B path; B is reused exactly, Core remains frozen. The relevant behavioral arms are Core-only identity, modular A+B, joint control, ablations with A removed/B removed/both removed, generation-2 A2, and the retained domain. Same seeds were evaluated in `fp32` and `ternary_core_reference` (seeds 101, 211, 307 each mode). The “ternary” treatment quantizes only Core values with float32 arithmetic/master weights/overlays; it is not packed 1.58-bit execution or a BitNet implementation. Recovery invalidates stale AB activations and rebuilds A from retained state. All authority/review/deployment adapters in the encompassing audit are scripted/trusted-local.

**Method and data:** Six planned trials; CPU only and no model/data downloads. Every atomic symbol appears in training; 64 held-out test pairs and a separate 49-pair retained Gen2 domain. Core identity measures the base transducer, while A+B tests a simple composed transform. Pair accuracy counts exact correctness of both symbols, not token accuracy. Modular A and B see separate target relationships; joint model sees composed targets, so parameter counts, optimizer updates and input presentations are not exactly supervision/FLOP-matched. Total reported optimizer updates 11,940; coordinator elapsed 44.571 seconds including data gates/checks but excluding setup. No energy/performance claim. The raw protocol, plan/code/environment, checkpoints and metrics are retained adjacent to the audit report; review notes that data were not independently blinded.

**Results, every reported arm:**

| Mode | Seed | Core-only | A+B | A removed | B removed | Both removed | Joint | Gen2 | Retained domain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fp32 | 101 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| fp32 | 211 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| fp32 | 307 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 101 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 211 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 307 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |

All six Core tensors remained byte-identical after freeze; prior A/B remained exact through A2 training and B was reused. Every recovery check rejected stale AB activations, rebuilt A with 0.0 maximum absolute error against a fresh instance, returned to Core-only, rejected an unapproved reverse transition and retained exactly one mock effect. A+B and the joint control both scored 100%; thus the result does **not** demonstrate a modular accuracy advantage. A removal leaves 56.25%; B removal 57.81%; both removed 48.44%, which confirms dependence on trained components for this easy prescribed transform but does not establish general information integration.

**Limits and interpretation:** The report calls this a positive prescribed linear-composition smoke test. The task has simple linear factorization, prescribed slots/auxiliary identity targets, and no unseen atomic symbols; joint baseline also solves it perfectly. Three seeds × two modes do not constitute broad independent benchmark evidence. No language competence, trained assistant Core, learned evaluator/router, realistic cognition, modular scaling advantage, production recovery, native packed ternary inference, independent external validator or broader NSS qualification follows. Separate archive audit tests are software lifecycle checks, not scientific task examples.

**Source locators:** `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip::MegaMindAlpha_v0.5.0_TriCoreFoundation001/docs/audits/neuralprobe001/AUDIT_REPORT.md`; `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip::MegaMindAlpha_v0.5.0_TriCoreFoundation001/docs/audits/neuralprobe001/RESULTS.md`; `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip::MegaMindAlpha_v0.5.0_TriCoreFoundation001/docs/audits/neuralprobe001/` (protocol, raw plan, checkpoint tensors and results).


<a id="pass-fnd-audits"></a>

### FND-AUDITS — Foundation engineering validation passes

**Broader question category:** Do the cumulative NSS foundation components enforce bounded, inspectable task state, data rights, evaluation/claim boundaries, current-candidate transitions and local recovery behavior? This is an engineering and evidence-governance category; no single Gxx assignment is asserted. NeuralProbe001 is a separate empirical entry immediately above. Several later connected demos also use a tiny fixed linear neural candidate, which is identified explicitly rather than calling the entire foundation purely deterministic.

**Specific question:** What did each retained audit actually build and check, and what did it establish about bounded trusted-local behavior, given that local tests, authored fixtures, model training, neural qualification, production security and external authority are distinct claims?

**Type and status:** Compact documentary matrix of thirteen engineering audits, with the neural empirical pass separated as NeuralProbe001. The `AUDIT_REPORT.md` sources are self-audits of successive local ZIP releases. Their test/gate counts are each source-reported; they are not independent reviews and are not summed, because inherited test suites, fixtures, source versions, demonstrations and gate sets overlap. Same-identity PersistentState001 material appearing in multiple foundation ZIPs is counted once here. “Pass” below means the report's bounded engineering gate only.

| Audit / source identity | Engineering question and system | Documented method | Reported result and boundary |
|---|---|---|---|
| StageHandoff001 | Can portable task records share the existing deterministic recovery store and publish an exact stage/task/profile handoff atomically? | 81-test inherited baseline; new API/demo, denial/stale/schema/dependency cases; four real child exits at PREPARED, after compute, STAGED and PUBLISHED; 25-flow schema-v2 atlas. | 128 methods passed (81 inherited +47 new); Recovery001A/B and connected `core→AB→A→core` demo passed, clean-A equality and one mock effect. Trusted-local deterministic behavior only, not neural viability, true identity continuity, external exactly-once or generic Runtime. |
| ExperienceArchive001 | Can source records be captured append-only, reviewed, corrected/disputed, purpose-permitted, revoked and retrieved without training/action permission leaking? | Baseline 128 tests/25 flows; 210 final tests; 13 process-crash windows across 3 methods; source/correction/revocation, fail-closed corruption and sealed-stage intake checks. | 210 passed (128 inherited+82 new), Recovery001A/B/StageHandoff and all 25 structural atlas flows; correction history retained, retrieval separately permitted, training blocked/revocation enforced. Trusted-local authored review, not authenticated humans, neural learning, production security or arbitrary exactly-once. |
| DatasetSnapshot001 | Can immutable train/validation snapshots be built from exact reviewed revisions and blocked after correction or training-right revocation? | Baseline 210; 293 final tests (83 new), six crash scenarios, correction/rebuild/revocation connected demo, 25 parent +2 helper graphs. | Full suite 293 passed; snapshot demo showed old bytes remain unchanged but conflict blocks use, reviewed rebuild succeeds, later revocation blocks reopened use. Two manifests/two publications; mock effect remains one. Fixed-tokenizer bytes only; not learned evaluation, semantic deduplication or external permission system. |
| EvaluationRun001 | Can repeatable fixed synthetic evaluations distinguish PASS, FAIL and INCONCLUSIVE and recover transactionally without mutating task state? | 404 tests (293 inherited+111 new), eight child-process deaths across compute/commit plus revocation/plan change; six demos and 25 parent flows; public snapshot-only scorer. | Demo A PASS, AB FAIL on A-target suite, insufficient-budget run INCONCLUSIVE; exact repeat digests agree, withdrawn source blocks use and history stays unchanged. 404 passed. No neural capability or production exactly-once guarantee; acceptance authority remained unimplemented. |
| NeuralProbe001 predecessor audit, QualificationEvidence002 | Can claim-scoped certificates bind exact model/evaluation/source evidence while preserving a historical strict numerical disagreement? | Baseline 498 tests; six journal process-exit cases; current source/rights, owner separation, profiles/transitions, immutable histories, revocation and exact saved-metric replay. | 615 expected methods (498+117); runner retains 16 required gates and one explicitly advisory strict historical-reference gate. Archived six-trial accuracy/count groups match, but MSE differs (max 3.725290298e−9); strict historical gate remains failed advisory and is not tolerance-relaxed. This is a local claim-review workflow, not a production authority or new model result. |
| LocalNexusPermissions002 | Can explicit local grants constrain numerical replay/use, task authority and current state while retaining the older strict-MSE result? | Clean extracted baseline 615 tests; 730 tests after changes including 11 process crashes; nine demos; 25 parent/14 subordinate graph checks. | 730 passed, all 18 required gates; the one non-required `reference_neural_evidence` check retains old strict-MSE disagreement. Local permission lifecycle, not authentication or generic Runtime permit; not neural quality. |
| OverlayGenerationManager001 | Can an immutable released family be staged, reviewed, published, retried and rolled back by new expiring local grant with one current pointer/epoch? | Baseline 730 and final 798 tests; 20 required gates/21 raw checks; ten demos including fresh schema-v2 neural report replay; transactional failure-path checks. | 20/20 required gates and 21/21 raw checks; earlier portability issue remains documented though not reproduced. Trusted-local experimental catalogue, not production activation; returned tensor does not prove GPU residency. |
| OverlayCatalogController001 | Can exact reviewed profile descriptors drive portable task handoffs through the existing generation owner, with explicit current task and receipts? | Clean inherited 798; final 869 tests, 71 new; 19-flow additions, 11 demos, catalog/profile/task failure tests. | 869/869 tests, 21/21 required release gates, all eleven demos. Restored canonical operation after a first clean run caught an inherited Atlas failure; no numeric tolerance change. Local deterministic control only, not learned routing, native paging or production qualification. |
| ContextRetrieval001 | Can the current task's bounded exact record, requirements, selected reviewed experiences and source slices form a context packet with strict overflow and live permission recheck? | 869 baseline; 927 tests (58 new); clean-tested 247-file input map; source/revision/UTF-8 slice and rehydration checks. | 22/22 required checks, 22/23 all recorded; exact selection/budget/rehydration behavior. “Context” is bounded canonical JSON UTF-8 bytes and literal-term shortlist, not native tokens/HSA/MSA, learned retrieval, semantic understanding, training rights, authentication or neural gain. |
| BoundedLearnerCoordinator001 | Can an approved local plan link reviewed data/snapshot/numerical owners to one bounded new A2 update while core/A/B stay frozen, with a review-only proposal and current-use rechecks? | Baseline 927, 987 final tests; 350 optimizer updates on new A2; recorded numerical repeats and source-withdrawal/approval denials. | 24/24 required gates, 25 total commands, 13 demos. Updated A2/A2+B report 100% on 64 developer-visible held-out pairs; retained behavior 100% on 49 designated pairs; parent A+B on updated target 76.5625%. Despite those tiny authored synthetic results, proposal is `INSUFFICIENT_EVIDENCE` for release, `candidate_deployed=false`, `runtime_execution_permit=false`. Not a broad performance, packed ternary, energy or learned evaluator result. |
| CandidateAcceptance001 | Can the owner-backed workflow evaluate a fresh candidate against exact candidate-specific criteria, certify only scoped transitions, require whole-family grant, stage/adopt/rollback transactionally, and block current use after revocation? | One new A2 fixed-recipe candidate; core and accepted A/B frozen; 1,063 tests (76 new); 26/26 required gates, 14 demos, crash, grant, revocation, parent-current and rollback scenarios; exact six-trial replay. | Required local-demo gates pass; candidate family staged/adopted from epoch 1→2 and explicitly rolled back to parent at new epoch3; six numerical trials replay exactly. An undertrained sealed candidate was rejected. Historical strict schema-v1 MSE advisory still fails; all-gates-pass remains false. No modular/energy/memory/general-intelligence advantage, real authentication or production release. |
| PersistentState001 | Can reviewed source-backed task deltas enter a scoped v2 state with atomic revisions/events, exact-source reads, stale/revoked-use rejection and history-only retries? | Baseline 1,063 tests, 1,111 final tests; 48 new cases including four BIND/UPDATE process crashes, uncertain external-action exit, versioned-export regression; 27 required gates and 15 demos. | 1,111 passed; all 27 required of 28 gates. One non-required raw `reference_neural_evidence` MSE gate retained failure. Scoped symbolic state behavior passed; not production, model memory, model identity, injection resistance or performance. Structural graphs are not semantic proof. |
| TriCoreFoundation001 | Does the overlay-independent role path atomically schedule Primary plus mutually exclusive Secondary/Tertiary, accept advisory Validator data without veto, and preserve recoverable tick state? | Fresh selected checks total 299 tests across new contracts and recovered persistent/context/archive/neural-backend/runtime fixtures; 12 commands including 24-case engineered harness smoke, preflight and lifecycle demo. | Selected checks passed; 903 recovered originals hash-matched; 299 selected tests and 12 commands passed. Adapter calls are deterministic test adapters (plus inherited tiny numerical/backend fixtures), not four qualified neural models. ClockEstimator has zero learned parameters and is a hand-engineered harness control. Not full historical 1,111 suite, every old release gate, production qualification, completed NBR study or actual serving integration. |

**Interpretation and limits:** These audits establish an incremental trusted-local software lifecycle and data-rights scaffold, plus bounded test-harness/neural candidate probes. Most acceptance claims are authored fixtures, structural graph validation and local owner protocols; principal/operator identifiers are declared labels rather than authenticated identities. Stage/workflow tests are not production security or external exactly-once. Some connected demos genuinely train or replay small fixed linear adapters, and NeuralProbe001 is a genuine empirical small neural comparison; those results are explicitly separated from symbolic-state software audits. None qualifies the intended four-model tri-core or adopts a new production architecture. The reports preserve their initial defects/stops and strict MSE advisory rather than smoothing them into blanket success. Counts above intentionally are not cumulative independent evidence.

**Source locators:** All rows use corresponding exact `AUDIT_REPORT.md` members in `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip::MegaMindAlpha_v0.5.0_TriCoreFoundation001/docs/audits/`: `stagehandoff001/`, `experiencearchive001/`, `datasetsnapshot001/`, `evaluationrun001/`, `qualificationevidence002/`, `localnexuspermissions002/`, `overlaygenerationmanager001/`, `overlaycatalogcontroller001/`, `contextretrieval001/`, `boundedlearnercoordinator001/`, `candidateacceptance001/`, `persistentstate001/`, `tricorefoundation001/`. NeuralProbe001 source and `RESULTS.md` are linked in its distinct entry above. `Research/Foundations/MegaMindAlpha_v0.4.14_PersistentState001.zip` is the earlier foundation archive carrying overlapping persistent-state material; same audit identity is deduplicated. `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip::MegaMindAlpha_v0.5.0_TriCoreFoundation001/TRICORE_FOUNDATION_001.md` supplies the role-path boundaries.


<a id="pass-bridge01"></a>

### BRIDGE01 — Dummy orchestrator bridge and simulated action journal

**Type and status:** Completed bounded integration prototype; report says it worked on its authored engineering fixture. The BRIDGE package calls it a frozen reference before low-bit work. Not a language-model or end-product qualification. Source is the retained original prototype ZIP; the compact report was read, not executed again.

**Broad question:** Can a scripted language-shaped proposal interface, exact task records, a frozen recurrent advisor and an action checker be wired together so unfinished work survives interruption and invalid proposals cannot change the exact task state?

**Specific question:** Across authored two-task sessions, can deterministic rules, shadow recurrent suggestions and guarded recurrent suggestions preserve task scope, revisions, approval, ordered completion and idempotent simulated effects through restart and a deliberately lost reply?

**Systems and arms:**

- **Rule:** exact lowest-pending-item computation. This is the conventional software coordinator and completed all 24 episode setups.
- **Shadow:** the frozen neural model’s suggestion is recorded, while the scripted proposal adapter receives the Rule answer; it completed all 24×4 = 96 sessions.
- **Recurrent:** the same neural suggestion is supplied to the scripted adapter and checked by the same action gate, with explicit rule fallback if needed; it completed 96 sessions. No fallback was required due to a natural neural event error in this fixture.
- **Shared scripted proposal generator:** sends/receives a six-field JSON proposal through a chat-style interface; it is not a Transformer, real LLM or learned language system. The HTTP adapter was tested against a loopback server with a scripted reply generator.
- **Shared exact journal, gate and executor:** SQLite journal binds owner/task/revision, typed events, approvals and receipts; reconstructs current task state and only records simulated effects after rule checks. It is software, not a learned reviewer or real external tool executor.

The recurrent adviser is each retained 18,249-parameter `GRUCell(26,64)+Linear(64,9)` checkpoint, using six original float32 NPZ arrays totaling 72,996 raw bytes, materialized as float64 runtime arrays totaling 145,992 bytes. It keeps one 64-value recurrent vector per owner/task (512 bytes, object/cursor overhead additional); model values stay frozen. The model reads only SET/CLEAR/RESET/NOOP typed task events and proposes the lowest unfinished item. It does not parse English, create permissions, route arbitrary tasks or discover a new workflow. Rule and Recurrent use the same eight-step public ordering; source truth is stored exactly and updates immediately, separately from model weights.

**Method, data and constraints:** Twenty-four authored episode setups comprise 12 named recipes and two owner/task naming variants, with two tasks per episode. Every setup was run once under Rule and once under Shadow and Recurrent for each of four unfiltered original parents: 24 + 96 + 96 = **216 sessions**. The main cases cover clean finish/approval, snapshot restart/lost reply, revision/reopen, tool failure/malformed response, wrong owner/task and false completion, untrusted permission note, redundant events, and forty NOOPs. All source changes, faults and approvals are authored, not sampled from users. Most naming variants reuse underlying histories; repeated sessions and event traces are not independent statistical observations.

The exact contract requires eight ordered steps, each initially pending; a trusted receipt makes a step done until explicit reopen; next allowed item is the lowest pending step; publishing also requires approval bound to the current revision; DONE is legal only after all eight steps. Proposal fields cannot create approvals, receipts, task changes or source updates; extra fields are rejected. Repeated successful request IDs return the existing receipt; changed content under a reused ID is rejected. A lost response is injected after SQLite has atomically committed a simulated effect/receipt; a fresh bridge instance rebuilds state from the journal and returns the receipt. This avoids duplicate local simulated effects but is not an external distributed-transaction proof. Snapshots are checked against journal identity/cursors, and the loader replays the journal before validating the saved envelope; no efficient restart or changed-weight migration is claimed.

The package froze protocol/source/fixtures/model exports and 14 lock entries before the run and separately locked post-result audit sources. Preflight passed 41 checks. Overall resource limits were checked after the run rather than continuously enforced by an OS sandbox. No real LLM checkpoint or download, optimizer update, low-bit test, live external tool effect or arbitrary web/shell execution was involved.

**Aggregate outcomes:**

| Mode | Sessions | Correct final sessions | Recurrent event answers | Rejected proposals |
|---|---:|---:|---:|---:|
| Exact rule | 24 | 24/24 | Not applicable | 62 |
| Rule with neural shadow | 96 | 96/96 | 2,072/2,072 | 248 |
| Guarded recurrent suggestions | 96 | 96/96 | 2,072/2,072 | 248 |

| Result across modes | Observed |
|---|---:|
| Authored episode setups | 24 (12 recipes × two naming variants) |
| Completed sessions with correct final task records | 216/216 |
| Rejected invalid or failed proposals | 558 |
| Distinct simulated durable effects | 3,474 |
| Duplicate, wrong-order or unapproved effects | 0 |
| Recurrent next-event answers matching exact rule | 4,144/4,144 |
| New training / low-bit execution / real LLM inference | None |

The 558 rejections are expected containment events, not neural correct-answer successes: 432 approval-required rejections plus 126 other rejections (18 each for malformed JSON, wrong owner, wrong task, stale revision, false completion, unsupported extra proposal fields and simulated tool failure). Responses included 3,456 normal effect confirmations, 18 commits whose replies were deliberately lost and 18 replayed existing receipts, plus 432 legitimate finish responses and the 558 rejections. Hence 3,474 distinct effects are the 3,456 normal effects plus 18 committed lost-reply effects; replays did not add effects. Exact Rule completed every authored case as well, so no recurrent superiority is measured.

**Verification and costs:** An independently implemented set-based audit checked all 216 journals for order, revision, current approval, step epochs, duplicate effects and finish assertions. All 216 complete episodes were regenerated in fresh Python processes with fresh temporary journals; 4,482 proposal/interruption entries and all retained non-timing results, raw messages, numeric states and snapshots matched exactly. Across 4,144 recurrent events, independent PyTorch GRUCell/Linear results were compared with NumPy over 302,512 hidden/logit scalars: zero declared float64-envelope violations, zero class differences, max absolute difference 7.11×10⁻¹⁵. This is coverage of the retained event traces, not all possible inputs.

| Resource measure | Recorded value |
|---|---:|
| Parameters per recurrent model | 18,249 |
| Runtime weight payload | 145,992 bytes, float64 |
| Per-task recurrent state payload | 512 bytes for 64 float64 values, plus cursors/objects |
| Largest packet | 1,574 UTF-8 bytes; tokens not measured |
| Largest retained JSON snapshot | 8,872 bytes; journal/source records extra |
| Main runner core | 6.331 s for 216 sessions |
| Main-process peak RSS | 99,147,776 bytes, includes Python/NumPy/SQLite and no LLM |
| Independent audit core | 7.861 s in separate PyTorch process |

These are environment-specific implementation observations, not model-serving comparisons or total research cost. The 24 Rule cases and repeated neural traces are not independent samples; the preflight/resource check did not continuously enforce limits. Result supports the interfaces/guards on fixed authored cases, not general learned orchestration, language understanding, superiority over exact coordination, authentic permissions, arbitrary external side-effect safety or tri-core architecture.

**Lineage and limits:** The BRIDGE prototype’s four exported parents are linked to the CYCLE01-A/RECOVER01 lineage. The separate BRIDGE evidence review reports that the archive contains original PT/NPZ parent pairs and lossless NPZ exports of the CYCLE01-A source parents; its audit checked container/array metadata without deserializing and comparing weights. Therefore treat this as a reported lineage/export, not a new CYCLE fit or independently verified equality of all parent tensor values. Event inputs in BRIDGE differ from the simpler CYCLE01-A test distribution and its all-perfect advice panel does not erase prior false-DONE evidence.

**Source locators:** Prototype report `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md`, §§1–9; compact provenance report `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/REPORT.md` describes CYCLE01-A lineage, not a replacement BRIDGE report; source paths and result files named in the prototype report include `results/main/SUMMARY.json`, `results/main/cases/*/RESULT.json`, `audit/AUDIT.json`, `fixtures/EPISODES.json`, and `docs/TESTS_AND_ANSWERS.md`. The bounded intake/review is `.consolidation/20260929/bridge01/EVIDENCE_REVIEW.md` and `REPORT_TEXT.txt`. Current checklist/status source is `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` and `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json`.


<a id="question-2"></a>

## 2. What information survives bounded state, interference and retrieval?


<a id="pass-q001"></a>

### Q001 — State, Depth and Learned Write Admission (Pilot001)

**Broader question category:** Persistent temporal state and recurrent depth (G03, G04). This pilot also informs baseline competence (G02), but its strongest direct questions are whether a small learned state survives distractors and whether extra readout depth helps.

**Specific question:** Can a small persistent state retain a written symbol through distractor events, and does trained depth help? Does admission control prevent low-strength irrelevant writes from erasing a valid memory?

**Type and status:** Five-seed synthetic feasibility pilot with separately registered post-pilot interventions. Completed; NBR-01 remains open. No production architecture was accepted.

**Systems and arms:** Four small neural readers were trained from random initialization: a GRU persistent state; a soft scalar-gated state whose update blends the old state with a learned candidate value; a hard-gated state trained with a straight-through surrogate; and a two-layer Transformer that retains and reads the full bounded token tape. A second evaluation used the same Transformer weights with an exact-memory tool that kept the latest valid source token. An exact state estimator was another control. Post-pilot, the same five soft-gate checkpoints were evaluated with a hard forward-admission rule. Follow-up gate interventions either closed only low gates or opened only high gates while leaving the learned weights fixed. State-off deliberately erased prior information and was an information-removal control, not a competitive baseline.

**Method and criteria:** The task had eight possible symbols. WRITE replaced the current symbol; DISTRACTOR should leave it unchanged; QUERY returned the latest valid symbol or UNKNOWN if there had been no write. Episodes included early cues, overwrites, and no-cue trials. Training delays were sampled uniformly from 0–16; evaluation delays were 0, 4, 16, 64, and 128, with 256 generated instances per condition and training seed. Each main neural arm used seeds 201–205, 600 AdamW steps, and batch size 64. Neural arms received matched observations, targets, and selected readout depths within each seed. Three 300-step development fits preceded the amended five-seed pilot; two timed-out starts were excluded and retained as interrupted attempts, then retried from original seeds without optimizer resume. The registered competence screen required at least 95% aggregate known recall and 95% no-cue accuracy over trained depths 1, 2, and 4 at delays 0, 4, and 16. The readout MLP was applied 1, 2, 4, or 8 times; depth 8 was held out. Training data and labels were matched, but parameter counts, representation, operations, runtime and memory were not.

**Documented results:** The competence screen passed in 5/5 seeds for the GRU, soft-gated state and full-tape Transformer, but only 1/5 for the hard-gate-from-scratch learner. At depth 4, early-cue recall (mean ± sample SD over the five seeds) was:

| Arm | 16 distractors | 64 distractors | 128 distractors |
|---|---:|---:|---:|
| GRU persistent state | 100.00 ± 0.00% | 4.53 ± 10.13% | 0.39 ± 0.87% |
| Soft-gated persistent state | 100.00 ± 0.00% | 0.00 ± 0.00% | 0.00 ± 0.00% |
| Hard gate trained from scratch | 23.83 ± 42.68% | 24.30 ± 42.45% | 23.12 ± 43.07% |
| Transformer with full retained tape | 99.53 ± 0.85% | 64.22 ± 26.23% | 63.05 ± 35.13% |
| Same Transformer plus exact-memory tool | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Soft-trained weights plus hard admission (post-pilot) | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

After 128 distractors and at depth 4, no-cue accuracy was 100.00 ± 0.00% for the GRU, soft-gated learner, exact-memory-assisted Transformer, and post-pilot soft-trained/hard-admission condition; 68.05 ± 29.27% for hard-gate-from-scratch; and 76.02 ± 40.45% for the full-tape Transformer. For depth 1/2/4/8 at 128 distractors, early-cue recall was respectively 0.00/0.00/0.39/1.56% for GRU, 0/0/0/0% for the soft gate, 23.20/23.12/23.12/21.72% for the hard gate, 64.06/63.59/63.05/61.72% for Transformer, and 100% at every depth for both the exact-memory-assisted Transformer and the post-pilot intervention. More readout repetitions did not repair the soft-gate long-delay failure; depth 8 was untrained and this simple recall task does not establish a broad depth advantage or disadvantage.

The unchanged soft-gate checkpoints passed every tested state-on condition, depth and delay after applying a fixed 0.5 hard-admission rule. In the depth-4, 128-distractor gate isolation, original soft gates scored 0% known recall, closing only low gates scored 100%, and opening only high gates scored 0%. These were fixed-weight, post-pilot diagnostics, not independent training arms or confirmatory evidence. They support residual irrelevant writes as the explanation for this task's failure; they do not establish clean relevance signals in natural language or a universal hard-threshold rule.

| Arm | Parameters | Weight bytes | AdamW tensor bytes | Five-seed training-loop seconds |
|---|---:|---:|---:|---:|
| GRU | 11,497 | 45,988 | 92,036 | 12.98 |
| Soft-gated state | 6,250 | 25,000 | 50,060 | 11.63 |
| Hard gate from scratch | 6,250 | 25,000 | 50,060 | 12.28 |
| Full-tape Transformer | 22,249 | 88,996 | 178,132 | 26.65 |

The 20 completed main fits therefore account for 12,000 optimizer steps and 768,000 example presentations. The reported training times exclude development, scoring and verification, and are not target-PC benchmarks. Each recurrent stream retained 32 float32 values (128 raw bytes, excluding weights and metadata); Transformer tape bytes grew with sequence length. No low-bit state, full lifecycle cost, device energy or production memory budget was tested. All 28 new unit tests and the documented fresh package/model rechecks passed; a single 600-step GRU trajectory was rerun from initialization with matching batch hash and final parameter digest. These are study-internal verification claims, not an independent replication. The source states that the unchanged v0.5.0 foundation's 68 tests, dependency check, and 974-file manifest also passed afresh.

**Interpretation and limits:** Short-task competence coexisted with rapid long-delay forgetting in recurrent state; exact memory and the full-tape Transformer were important controls. Hard-gate-from-scratch training was unreliable in this pilot, while post-hoc admission changes rescued the soft-trained weights. The pilot does not rank architectures under equal compute, and its after-the-fact interventions must not be relabeled as preregistered confirmation. The next suggested boundary was fresh-seed comparison of soft training plus qualified admission against direct hard-gate training and longer-horizon controls, followed by a harder relational task for depth.

**Source locators:** `Research/NSS_NBR01_StateDepth_Pilot001_v0.1.zip::NSS_NBR01_StateDepth_Pilot001_v0.1/REPORT.md` §§1–9, especially result/resource tables; `Research/NSS_NBR01_StateDepth_Pilot001_v0.1.zip::NSS_NBR01_StateDepth_Pilot001_v0.1/evidence/SUMMARY.json` for the full condition/depth/seed aggregation; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q001 row. The report's source-foundation and verification locators are also cited in its §9.


<a id="pass-q002"></a>

### Q002 — Longer Horizons, Addressed Memory and Write-Admission Uncertainty (HorizonBinding002)

**Broader question category:** Persistent temporal state, evidence/uncertainty and the limits of supplied structure (G03, G06, G07; G02 for baseline competence). The study directly tests bounded retention and missing-state behavior, not arbitrary entity binding.

**Specific question:** Does addressed writable state persist through up to 4,096 distractor events, preserve missing values and uncertain writes, and compare favorably with a full-history reader? Are learned write-strength values calibrated admission probabilities?

**Type and status:** Registered bounded numerical-memory comparison with main fits, separate supplementary controls and a post-hoc interface diagnostic. Completed; no core or architecture replacement.

**Systems and arms:** Four addresses, each holding one of eight values or UNKNOWN, were supplied by the harness; score qualification and RESET were also explicit. Newly trained mechanisms were an address-separated GRU, soft-state learner, and hard-gate learner. For the soft checkpoints, fixed-weight interventions used native soft updates, a fixed 0.5 gate, low-gate suppression, or a threshold calibrated on separate labelled admission examples. A two-block full-history cross-attention reader received address masks and relative log-age bias; its same trained reader was also paired with exact selected records. A clean exact observation-policy ledger and a generator-informed belief filter were controls. A post-hoc diagnostic passed the exact reader a “qualified event view” encoding the external tool's already-known qualification separately from the raw selected record. That view changed input semantics and preserved original observations; it did not edit training weights or claim that the original confidence score had been high.

**Method and criteria:** The 40 main checkpoints crossed four mechanisms, two preparation curricula and five seeds (301–305); each completed 2,400 AdamW steps at batch size 48. Short preparation used 1–16 events; wide preparation used 1–64. All neural arms matched batches and labels within seed/curriculum, while curricula differed in event exposure and difficulty. Five soft checkpoints per curriculum received additional calibration examples (10,240 unique labelled calibration events; 20,480 presentations after reuse across curricula). Each record had a visible synthetic score; clean writes at score ≥0.5 were accepted and lower-score events were ignored. Evaluation used 0/16/64/256/1,024/4,096 additional events following an eight-event setup, with 128 streams per seed and four queries per cell. The largest complete history had 4,104 events. Conditions covered clear retention, known and missing records, replacement, other-address interference, rejected/valid near-boundary scores, reset and corrupted observations. Gaussian σ=0.10 corrupted observed scores in the noise challenge while intended labels followed the uncorrupted policy. The baseline gate required ≥95% on each specified short known and missing condition; clean long-horizon admission required ≥95% at 4,096 events and at most a one-point drop from 16; low-margin admission was a separate criterion. Main evidence comprises 3,840 model metric cells, 240 exact-control cells, and 1,966,080 repeated model answer evaluations over shared cases, not that many independent episodes.

**Documented results — seed-level gates:** Counts are out of five seeds; all registered failures remain included.

| Mechanism | Preparation | Baseline | Clean long horizon | Low-margin challenge |
|---|---|---:|---:|---:|
| Addressed GRU | short | 0/5 | 0/5 | 0/5 |
| Addressed GRU | wide | 4/5 | 0/5 | 0/5 |
| Hard gate from scratch | short | 5/5 | 5/5 | 0/5 |
| Hard gate from scratch | wide | 5/5 | 5/5 | 0/5 |
| Same soft weights, close low gates only | short | 5/5 | 5/5 | 0/5 |
| Same soft weights, calibrated hard gate | short | 5/5 | 5/5 | 5/5 |
| Same soft weights, fixed hard gate | short | 5/5 | 5/5 | 0/5 |
| Native soft state | short | 5/5 | 0/5 | 0/5 |
| Same soft weights, close low gates only | wide | 5/5 | 5/5 | 0/5 |
| Same soft weights, calibrated hard gate | wide | 5/5 | 5/5 | 5/5 |
| Same soft weights, fixed hard gate | wide | 5/5 | 5/5 | 0/5 |
| Native soft state | wide | 5/5 | 5/5 | 0/5 |
| Same reader + exact selected records | short | 5/5 | 5/5 | 0/5 |
| Full-history cross-attention reader | short | 0/5 | 0/5 | 0/5 |
| Same reader + exact selected records | wide | 5/5 | 5/5 | 0/5 |
| Full-history cross-attention reader | wide | 0/5 | 0/5 | 0/5 |

**Clear record retention by wide-prepared arm** (mean ± sample SD across five fits; event counts are after the eight-event setup):

| Mechanism | 16 | 64 | 256 | 1,024 | 4,096 |
|---|---:|---:|---:|---:|---:|
| Native soft state | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft weights, fixed hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft weights, close low gates only | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft weights, calibrated hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Hard gate from scratch | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Addressed GRU | 96.17 ± 1.58% | 61.25 ± 7.54% | 0.00 ± 0.00% | 0.00 ± 0.00% | 0.00 ± 0.00% |
| Full-history cross-attention reader | 97.85 ± 1.01% | 89.80 ± 2.12% | 63.52 ± 9.10% | 23.16 ± 5.60% | 15.70 ± 9.33% |
| Same reader + exact selected records | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

This pilot's results differed from Q001: wider-prepared native soft state retained clean records perfectly through 4,096 events and direct hard-gate training passed clean retention in all ten fits. This does not isolate curriculum from task/interface changes across studies. The short-prepared soft learner still returned a known value for empty slots at 4,096 events (100% known, 0% UNKNOWN). Wider preparation passed both. In the supplied other-address interference case, every wide-prepared gated variant and the exact-memory-assisted reader retained the protected address at 100%; address separation was built into the system.

**Low-margin qualification, noisy observation and receiver interface:**

| Mechanism | Clear retention | Ignore weak invalid writes | Accept weak valid writes |
|---|---:|---:|---:|
| Native soft state | 100.00 ± 0.00% | 0.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft weights, fixed hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same weights, close low gates only | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same soft weights, calibrated hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Hard gate from scratch | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same reader + exact selected records | 100.00 ± 0.00% | 100.00 ± 0.00% | 52.27 ± 16.72% |
| Exact observation-policy ledger | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

The fixed 0.5 threshold on a learned gate rejected all weak valid writes; the trained gates mapped input scores around 0.544–0.547, and their training left a score gap from 0.45–0.55. Separate labelled calibration passed both low-margin conditions in every seed. With corrupted observations at 4,096 events, wide-prepared accuracy was 58.55 ± 0.84% for native soft state, 60.00 ± 0.91% fixed hard gate, 48.79 ± 1.27% calibrated hard gate, 60.27 ± 1.49% hard-from-scratch, 44.77 ± 1.38% GRU, 42.54 ± 2.25% full-history attention, 45.82 ± 1.97% reader plus exact selected records, 48.83 ± 1.25% exact observation-policy ledger, and 62.73 ± 1.13% for a noise-informed belief filter. The last control used generator knowledge unavailable to learned models; it is an informed control rather than a matched-knowledge architecture win. A deliberately censored pair of incompatible hidden intentions had a 50% maximum without additional evidence by construction.

After main results, the same wide reader scored 52.27 ± 16.72% on weak true writes with raw exact-selected records and 100% with a separate qualified-event view; on corrupted observations the respective scores were 45.82 ± 1.97% and 48.83 ± 1.25%. This post-hoc view diagnoses an interface mismatch; the original source results remain unchanged. Retrieval of a record and correct interpretation by its receiver are separate stages.

**Resources and reproducibility:** Parameters / weight bytes / AdamW tensor bytes / ten-fit training-loop seconds were: addressed GRU 2,681 / 10,724 / 21,492 / 125.38; hard gate 1,050 / 4,200 / 8,444 / 80.89; soft state 1,050 / 4,200 / 8,444 / 80.91; full-history tape reader 5,771 / 23,084 / 46,316 / 156.78. The main loops totaled 443.95 CPU seconds; recurrent state was 256 raw bytes per stream and the full-tape state grew with all 4,104 events. The generated belief control held 36 float64 probabilities (288 bytes), with additional posterior work arrays. Whole-process RSS samples, full lifecycle costs, target-device costs and energy were not qualified; nothing was packed to one-bit state. All 33 new unit tests passed, all 40 checkpoints and 3,840 model cells were replay-checked internally, one complete 2,400-step soft fit was reproduced from initialization, and 70 snapshot/restore/continue configurations were checked. These repeated checks are not additional seeds or external replication. The report also says the unchanged foundation's 68-test suite and all 974 manifest entries passed afresh.

**Interpretation and limits:** Clear-state retention, admission confidence, missing-state semantics, corrupted observation uncertainty and receiver interpretation are distinct claims. Exact policy remains a stronger option where the rule is known; a hard gate is not automatically calibrated confidence. This four-address synthetic study does not establish learned arbitrary binding, language performance, system memory efficiency or an overall architecture winner. Proposed next steps are separate fields for source, qualification, belief and permission, plus independent testing of noise-aware learners and interfaces.

**Source locators:** `Research/NSS_NBR01_HorizonBinding002_v0.1.zip::NSS_NBR01_HorizonBinding002_v0.1/REPORT.md` §§1–11; `Research/NSS_NBR01_HorizonBinding002_v0.1.zip::NSS_NBR01_HorizonBinding002_v0.1/evidence/results/SUMMARY.json` for the full seed/cell tables and `evidence/results/*.eval.json` for per-case results; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q002 row.


<a id="pass-q003"></a>

### Q003 — Native State Recovery (StateRecovery003)

**Broader question category:** Persistent state under disturbance and explicit absent-state integrity (G03, G05, G07; G01 is only a literature analogy, not an empirical mapping).

**Specific question:** Can a learned maintenance map repair noise-damaged known codes while preserving UNKNOWN? Do fast/slow state lanes offer value beyond equal-byte redundancy? How do updates, repeated noise, resets and exact metadata affect the answer?

**Type and status:** Registered five-pair synthetic maintenance/repair study using frozen learned value codes from Q002. A separately labelled post-hoc diagnosis tested local stability and protected presence metadata. Completed; no new core or architecture was adopted.

**Systems and arms:** The study reused five competent frozen Q002 wide-soft representations and their nine-class readouts (eight values plus UNKNOWN); gates, encoders and readouts remained fixed. For each representation, a paired seed 501–505 fit three candidate systems: a one-step learned nonlinear read repair applied only to the read copy; a shared recurrent residual repair map that modifies stored numerical state; and a three-parameter fast/slow two-lane filter with learned rates. Controls were Hold with original readout, recurrent repair applied only at read, disabled updates, equalized fast/slow rates, a same-byte two-copy mean, nearest-supplied-prototype decoding or projection, state removal, and a protected exact ledger. Nearest prototypes used the finite learned code bank supplied by the experiment. The post-hoc diagnosis added four protected raw boolean presence bytes per stream, external to the corrupted neural state.

**Method and criteria:** The three candidates per each of five reused representations received paired noisy examples, labels and target-code supervision; all 15 fits completed 1,800 AdamW steps at batch 128 (27,000 steps; 3,456,000 repeated example presentations). The recurrent candidate used a shared residual map with an exact-zero guard; the fast/slow arm simultaneously updated two 16-dimensional activation lanes, with learned blending rates but no online weight update. Four addresses, RESET, and the clean score≥0.5 qualification rule were supplied. Conditions included independent Gaussian noise, common-mode noise, first-lane damage, erasure, directed corruption toward a wrong prototype, and chronic fresh noise. Main maintenance horizons were 0–128 rounds; training covered at most four rounds and Gaussian σ=0.5. σ=1.0/1.5 were shift challenges. Clean state/reset were also run through 4,096 logical autonomous rounds (not new observations or reasoning), and chronic-noise conditions used up to 1,024 fresh noise events. The registered gate required ≥95% known/UNKNOWN and replacement performance, exact reset, and a clean long-maintenance drop no greater than one point versus short horizon. Each shock condition contained 256 four-address streams per seed. The source notes 11,090 main metric cells and 10,626,560 repeated answer evaluations share assignments/trajectories and are not independent samples.

**Documented results — admission gates and single-shock outcomes:**

| Mechanism | Competence screen | Clean long-maintenance screen |
|---|---:|---:|
| Hold + original readout | 5/5 | 5/5 |
| One-step learned read repair | 5/5 | 5/5 |
| Learned recurrent maintenance | 5/5 | 5/5 |
| Learned fast/slow filter | 5/5 | 5/5 |
| Two-copy mean | 5/5 | 5/5 |
| Nearest-prototype maintenance | 5/5 | 5/5 |
| State removed | 0/5 | 0/5 |

At a single Gaussian σ=1.0 shock followed by four maintenance rounds, mean ± sample SD across the five pairs was:

| Mechanism | Known-record accuracy | UNKNOWN accuracy |
|---|---:|---:|
| Hold + original readout | 65.01 ± 3.05% | 71.33 ± 2.55% |
| One-step learned read repair | 89.15 ± 1.03% | 78.23 ± 5.76% |
| Learned recurrent maintenance | 94.64 ± 0.74% | 47.43 ± 6.55% |
| Learned fast/slow filter | 81.73 ± 2.36% | 72.57 ± 4.64% |
| Two-copy mean | 85.53 ± 1.73% | 70.97 ± 6.66% |
| Nearest supplied prototype at read | 96.29 ± 0.96% | 77.35 ± 4.36% |

At σ=0.5, recurrent maintenance scored 99.98% known and 86.73% UNKNOWN, versus nearest-prototype 100.00% and 99.82%. A same-map read-only four-step pass after the isolated shock gave exactly the same predictions as four maintenance steps, so this cell did not show that storing the repaired vector had a unique benefit over repairing at the interface.

With 1,024 fresh σ=0.15 noises—one noise at each event—the reported outcomes were:

| Mechanism | Known-record accuracy | UNKNOWN accuracy |
|---|---:|---:|
| Hold + original readout | 10.44 ± 1.65% | 60.71 ± 8.38% |
| One-step learned read repair | 10.09 ± 2.63% | 65.71 ± 8.22% |
| Recurrent map only at read (4 rounds) | 24.39 ± 2.94% | 30.00 ± 5.42% |
| Learned recurrent maintenance | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Two-copy mean | 14.47 ± 2.26% | 68.57 ± 10.23% |
| Nearest-prototype maintenance | 100.00 ± 0.00% | 100.00 ± 0.00% |

The same recurrent map applied up to 1,024 times only at the end reached 29.56 ± 3.32% known and 0.71 ± 1.60% UNKNOWN; per-event recurrence reached 100%/0%. This compared timing with the same maximum logical repair budget, not matched wall-time. An exact protected ledger restored 100% known after complete neural-state erasure, while all non-archive neural/control arms returned UNKNOWN (0% known; 100% UNKNOWN), reflecting its separately retained information. Directed corruption 75% toward a different valid code left non-archive arms at 0% through 128 rounds; stability did not recover the intended answer.

For the fast/slow comparison, with independent σ=1.0 damage to both lanes, the trained filter achieved 81.73% known versus 85.53% for equal-byte averaging. Equalized rates matched the mean on that cell. Under common-mode σ=1.0 damage, all linear two-lane arms matched unmaintained known accuracy at 64.83%. With first-lane-only σ=1.0 damage, fast/slow reached 99.98% versus 97.56% for the mean; if the first lane was fully erased but the second intact, both reached 100%. The learned rates were about b=0.681–0.691 and g=0.296–0.312. The benefit tracked fault location and redundancy and did not establish a general timescale advantage.

In post-hoc local analysis, at finite-difference step 0.001, the largest-magnitude local eigenvalue at the UNKNOWN point was 1.045–1.524 across the five pairs, while the largest values across settled known codes were 0.627–0.684; step 0.0001 gave the same qualitative result. This is local evidence, not a global convergence proof. A protected external presence flag with the same weights under chronic noise yielded 100% known/UNKNOWN in every pair, versus 100%/0% without it; deliberately inverted flags yielded 0%/0%. The intervention demonstrated the value of exact known/empty metadata for this task, not a learned solution. It adds four raw boolean bytes and cannot restore a value if it is erased.

**Resources and verification:** For each batch-64 stream, Hold used 256 raw activation bytes and no candidate weights (63.9 μs median maintenance+read); read repair used 256 bytes plus 8,512 weight bytes (217.1 μs); recurrent maintenance likewise 256 + 8,512 bytes (216.1 μs); fast/slow used 512 bytes plus 12 weights bytes (99.5 μs); two-copy mean 512 bytes and no extra weights (72.3 μs); nearest prototype at read 256 bytes and no extra weights (34.7 μs); nearest-prototype maintenance 256 bytes (122.2 μs). All modes also shared 4,072 bytes of frozen representation/readout tensors, and additional headers, scopes and snapshots were excluded. Main candidate training took 46.59 seconds; reused Q002 representation preparation (48.81 seconds) was not repeated and was not cost-free. These are descriptive CPU measurements, not full device/system costs. State and weights remained float32; no packed low-bit mechanism was tested.

All 38 new unit tests passed; all 15 main checkpoints and 11,090 metric rows/prediction arrays were internally replay-checked. One full 1,800-step recurrent training trajectory matched its saved identities on rerun. Sixty weight/mode snapshot-restore-continue configurations were checked. These are not new independent seeds or external replication. The report also says the untouched foundation's 68 tests, dependency check and 974-file manifest passed; the study's full historical 1,111-test suite and Windows execution were not run.

**Interpretation and limits:** Recurrent restoration recovered known patterns but destabilized the empty region and could settle on a stable wrong answer. Nearest supplied-prototype maintenance was a strong simple control. Fast/slow filtered redundant information but did not show general gain. Exact presence metadata repaired the specific known-versus-empty failure, with an explicit extra-information cost. The study isolates state maintenance under a finite known-code bank and supplied addresses; it does not test arbitrary binding, external factual correction, reasoning depth, biological fidelity, general noise handling or a production memory service.

**Source locators:** `Research/NSS_NBR01_StateRecovery003_v0.1.zip::NSS_NBR01_StateRecovery003_v0.1/REPORT.md` §§1–11; `Research/NSS_NBR01_StateRecovery003_v0.1.zip::NSS_NBR01_StateRecovery003_v0.1/SUMMARY.json` and `evidence/results/` for the full cell/prediction tables; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q003 row.


<a id="pass-q004"></a>

### Q004 — Stable Absence, Writable Lifecycle and Recurrent Empty-State Protection (WritableEmpty004)

**Broader question category:** Persistent temporal state, recurrent stability, and what must remain explicit in memory (G03, G05, G07).

**Specific question:** Can an empty record remain absent through repeated noise while still accepting a first write, correction, clear and rewrite? Does adding neural empty-region stability preserve established known values across a full writable lifecycle?

**Type and status:** Paired five-seed extension of Q003 with separately reported local-dynamics, weakened-write and stronger-fault diagnostics. Completed. Dynamic presence was retained as an engineering control; revised neural maps were not adopted.

**Systems and arms:** All arms used five frozen Q002 16-dimensional code/readout representations and five frozen Q003 2,128-parameter recurrent content-repair parents. The original recurrent content map remained unchanged for the original-recurrence arm. Three new revisions were trained: broader rehearsal of the original map, that rehearsal plus a sampled empty-contraction loss, and a one-parameter positive radius that locally attenuated the parent's output near EMPTY=0. Dynamic presence controls stored one protected Boolean byte per record and clamped empty content to zero while allowing explicit writes to set presence. Nearest-prototype maintenance projected to one of the finite supplied known/empty codes. Hold, original reader, original recurrence, protected presence, revised recurrence plus presence, and the nearest-code system were distinct controls. A post-hoc local finite-difference analysis and delivered-write attenuation stress did not alter main results.

**Method and criteria:** New learning seeds 601–605 produced 15 fits: five continuation fits, five with contraction loss and five local-gain radius fits. Each received 1,800 AdamW steps (27,000 optimizer steps; 3,456,000 sequence presentations and 21,337,344 within-sequence event presentations total); arms shared paired input/label draws but differed in parameter count, objective and computation. Four addresses, eight known codes plus EMPTY/UNKNOWN, qualification at score≥0.5, and full-code writes/clear events were provided by the harness. Each stream's focus address moved through Empty→first write→correction→clear→rewrite, with five 1,024-round phases under fresh σ=0/0.15/0.30 noise and reads every round. The extended stress began with 4,096 fresh σ=0.15 empty rounds, then a legitimate first write and 256 more rounds. A separate state-presence condition and a weakened-delivery condition isolated other mechanisms. The joint nominal pass required ≥95% known and UNKNOWN at every phase endpoint, ≥95% immediate legitimate writes, and ≥95% of streams correct at every read. Five paired seeds define replication; 6,560 rows and 1,986,560 saved answers reuse trajectories.

**Documented nominal lifecycle results** (final rewritten phase under repeated σ=0.15 noise; mean ± sample SD across five pairs):

| Mechanism | Known endpoint | UNKNOWN endpoint | Every read correct over whole stream |
|---|---:|---:|---:|
| Hold + original reader | 5.94 ± 1.20% | 68.75 ± 7.73% | 0.00 ± 0.00% |
| Original recurrent maintenance | 100.00 ± 0.00% | 0.00 ± 0.00% | 0.00 ± 0.00% |
| Broader rehearsal + code anchors | 92.29 ± 10.81% | 100.00 ± 0.00% | 71.88 ± 28.90% |
| Rehearsal + empty contraction loss | 94.17 ± 7.56% | 100.00 ± 0.00% | 79.06 ± 21.61% |
| Original recurrence + protected dynamic presence | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Revised recurrence + protected dynamic presence | 94.17 ± 7.56% | 100.00 ± 0.00% | 81.25 ± 22.88% |
| Frozen original + fitted local empty gain | 77.29 ± 9.95% | 96.25 ± 2.37% | 0.00 ± 0.00% |
| Nearest-prototype maintenance | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

The protected-presence/original-recurrence control passed every phase endpoint, but only 319/320 streams (99.6875%) had every intermediate answer correct. Its one transient error involved a populated record, not an empty record. The nearest-prototype control had every nominal trajectory correct. Seed counts for clean / joint nominal-noise / extended 4,096-round screens respectively were: hold 5/5, 0/5, 0/5; original recurrence 5/5, 0/5, 0/5; broader rehearsal 5/5, 1/5, 3/5; rehearsal+contraction 5/5, 1/5, 3/5; original recurrence+presence 5/5, 5/5, 5/5; revised recurrence+presence 5/5, 2/5, 3/5; local gain 2/5, 0/5, 0/5; nearest prototype 5/5, 5/5, 5/5.

After an extended 4,096-round empty interval followed by a first write, known endpoint / UNKNOWN endpoint / full-stream success were 6.56/70.62/0% for hold; 100/0/0% for original recurrence; 91.88/100/82.81% for broader rehearsal; 93.59/100/85.62% for rehearsal+contraction; 100/100/100% for original recurrence+protected presence; 93.59/100/88.12% for revised recurrence+presence; 76.56/98.28/0% for the local gain; and 100/100/100% for nearest prototype. Both best controls therefore preserved writable absence after the long empty period.

The empty fixed point was locally unstable in the old map: at ε=0.001, the maximum local eigenvalue magnitude was 1.045–1.524 for old maps versus 0.118–0.404 for contraction maps; rehearsal-only maps were also locally below 1, and the fitted radial gain was near-zero at the origin. This did not secure the neighboring known attractors: the radial-gain mechanism still failed the clean long-maintenance screen in 3/5 pairs. A post-hoc write-delivery test after 16 rounds found focus recall at 25%/50%/100% delivered content of 52.50/100/100% for original recurrence; 0/5/100% for broader rehearsal; 0/2.50/100% for rehearsal+contraction; 0/25/100% for local gain; 52.50/100/100% for recurrence+protected presence; and 0/100/100% for nearest prototype. The exact presence field could not reconstruct a partially delivered value.

At σ=0.30, final known/UNKNOWN scores were 65.94/100% for original recurrence+presence; 5.83/98.75% for revised recurrence+presence; and 100/100% for nearest prototype. For a single σ=1.0 shock plus four repair rounds, known/UNKNOWN values respectively were 66.43/73.30% hold; 94.57/49.34% old recurrence; 93.06/90.04% broader rehearsal; 93.11/89.75% contraction; 94.57/100% old recurrence+presence; 93.11/100% revised+presence; 93.72/71.92% local gain; 96.07/82.66% nearest prototype. Sufficiently strong shocks therefore also moved a valid code closer to another prototype; the catalogue control was not infallible.

**Resources and interpretation:** Per-stream raw state / additional serving-weight bytes / median maintenance+read time at batch 64: hold 256 B/0/97.1 μs; old recurrence 256/8,512/254.7 μs; broader rehearsal 256/8,512/256.2 μs; contraction 256/8,512/265.7 μs; old recurrence+presence 260/8,512/276.9 μs; revised+presence 260/8,512/273.9 μs; local gain 256/8,516/291.0 μs; nearest prototype 256/0/163.4 μs. Every mode also used 4,072 bytes of common representation/readout tensors; bytes exclude complete process/transient memory. The four presence values are four Boolean bytes, not packed bits. Main training loops summed 150.25 CPU seconds; sampled RSS was up to 315.60 MiB. All 44 new unit tests, 15 checkpoint identities, all 6,560 rows and prediction traces were internally replayed; one 1,800-step fit and 80 state/RNG snapshots were reproduced. The unchanged foundation's reported 68 tests and 974-file manifest passed; full historical 1,111-test qualification and Windows execution were not run.

The best native change reduced empty-state errors but damaged established retention; the small local fix destabilized other behavior. The original map with an explicit exact presence field and the simple nearest-code control were strongest. This was not learned admission or broad uncertainty, arbitrary binding, delayed credit, low-bit state or a biological simulation.

**Source locators:** `Research/NSS_NBR01_WritableEmpty004_v0.1.zip::NSS_NBR01_WritableEmpty004_v0.1/REPORT.md` §§1–11; `Research/NSS_NBR01_WritableEmpty004_v0.1.zip::NSS_NBR01_WritableEmpty004_v0.1/SUMMARY.json` for all rows and traces; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q004 row.


<a id="pass-q005"></a>

### Q005 — Learned Existence with Frozen Content (ExistenceContent005)

**Broader question category:** Persistent temporal state, writable absence, and explicit versus learned memory structure (G03, G06, G07).

**Specific question:** Can one- or four-coordinate learned existence lanes tolerate noise and preserve a writable absence state while content recurrence remains frozen? Does a jointly refit content/existence map improve the full lifecycle?

**Type and status:** Registered five-pair synthetic lifecycle study, using learned finite-code values and post-hoc diagnostic controls. Completed; one- and four-coordinate split state remain research candidates, not adopted architecture.

**Systems and arms:** All arms inherited five frozen Q002 value representations and five Q003 content-repair parents; the unsuccessful Q004 content revisions were not used. Five fits each created a 49-parameter one-coordinate existence map, a 148-parameter four-coordinate existence map, and a jointly refit 2,257-parameter 17-D content/existence map. Controls included original content recurrence without a separate existence signal, protected Boolean existence, fixed sign restoration for one float, fixed mean/sign restoration for four floats, an unmaintained existence coordinate, and nearest-prototype maintenance over the common finite code catalogue. All explicit-existence arms used a sign-derived guard that clears content when existence is decoded absent; the flag is not protected from noise in neural arms.

**Method and criteria:** New paired seeds 701–705 trained all 15 fits for 1,800 AdamW steps each (27,000 optimizer steps, 3,456,000 sequence presentations and 21,288,576 within-sequence supervised presentations). Paired arms saw identical generated episodes and labels, but their trainable sets and objectives differ. Four addresses, eight values, an absence code, explicit writes/clear, qualification at score≥0.5 and scope checks were supplied. Sixty-four streams per setting traversed empty→first write→correction→clear→rewrite with 1,024 fresh Gaussian-noise rounds per phase (σ=0, 0.15, 0.30); an extended arm used 4,096 empty rounds then a new write. Every answer and existence-status read was saved. Nominal acceptance required ≥95% known/UNKNOWN at all phase endpoints, ≥95% immediate writes and ≥95% whole streams with correct answer and status at every read. Paired seeds, not 308 million stored answer positions, define replication.

**Documented nominal results:** At the final rewritten endpoint under σ=0.15, each cell below is known / UNKNOWN / existence status / whole-stream correct:

| Mechanism | Known | UNKNOWN | Status | Whole stream |
|---|---:|---:|---:|---:|
| Original content recurrence | 99.90% | 0.00% | 75.00% | 0.00% |
| Original + protected dynamic existence | 99.90% | 100.00% | 100.00% | 99.69% |
| Frozen content + learned 1-coordinate existence | 99.90% | 100.00% | 100.00% | 99.69% |
| Frozen content + learned 4-coordinate existence | 99.90% | 100.00% | 100.00% | 99.69% |
| Jointly retrained 17-D content/existence | 100.00% | 91.88 ± 8.15% | 97.19 ± 2.25% | 0.94 ± 2.10% |
| Frozen content + fixed sign restoration | 99.90% | 100.00% | 100.00% | 99.69% |
| Frozen content + fixed four-coordinate mean/sign | 99.90% | 100.00% | 100.00% | 99.69% |
| Frozen content + unmaintained existence coordinate | 15.73 ± 1.07% | 59.38 ± 5.63% | 53.75 ± 4.87% | 0.00% |
| Nearest-prototype maintenance | 100.00% | 100.00% | 100.00% | 100.00% |

The split one- and four-coordinate learned candidates matched the protected-existence traces, including the same one failed content stream: 319/320 streams were fully correct (99.6875%); one of 960 known answers was wrong. All three passed the clean screen 5/5, but the clean/nominal/extended screen counts were 5/5/5 for original+protected existence, each learned split, each fixed restore, and nearest prototype. Original recurrence, jointly refit 17-D and unmaintained existence scored 5/5 clean but 0/5 nominal and 0/5 extended. The protected and learned split lanes thus passed the registered nominal lifecycle; no learned-quality advantage over fixed rules was demonstrated.

At stronger σ=0.30 across both content and existence, known / UNKNOWN / status / whole-stream rates were: original recurrence 66.88/0/75/0%; protected existence 66.88/100/100/8.75%; learned scalar 6.67/54.37/53.12/0%; learned four-coordinate 66.77/99.69/99.77/8.75%; coupled 17-D 65.00/25.94/71.17/0%; fixed scalar sign 24.17/51.25/56.88/0%; fixed four-coordinate mean/sign 66.88/100/100/8.75%; unmaintained scalar 9.69/52.50/53.20/0%; nearest prototype 100/100/100/99.69%. Strong noise exposed the content map's limits even when existence was reliable.

For 2,048 rounds of presence-only σ=0.30 noise, correct status / full-stream rates for independent/common-mode noise were: learned scalar 51.72/0% and 51.72/0%; learned four-coordinate 100/100% and 53.52/0%; fixed scalar 58.59/4.06% for both; fixed four-coordinate mean/sign 100/100% and 58.59/4.06%; jointly refit 17-D 65.55/0% for both; unmaintained scalar 57.19/0% for both. At σ=0.45 independent presence noise, fixed four-coordinate restoration achieved 95.9375% fully correct streams versus 4.375% for learned four-coordinate. Under 0.15 in a separate presence-only trajectory, the learned scalar had one false-presence stream even though its answer endpoints remained 100%; full-stream success was 99.6875%.

Targeted presence faults: inverting one of four coordinates was recovered by learned/fixed four-coordinate mechanisms on tested clean cases, while inverting all coordinates changed the decoded meaning and could erase content. Erasing all coordinates to zero was not an explicit clear; the coupled model recovered status in the specific case because content remained intact. Erasing a populated content vector did not recover its value from existence alone. Under half delivery of content only, both learned split candidates recovered the focus value 100%; under half delivery of the whole neural state (existence code interpolated to zero), both scored 60%, fixed sign controls 0%, and coupled17 90% in that case. Full-code writes were accepted by all arms. The report highlights that a committed write must establish both existence and content.

**Resources and interpretation:** Raw state/additional active-parameter bytes/median maintenance+read at batch64 were: original content 256/8,512/283.7 μs; original+protected 260/8,512/381.0 μs; learned scalar split 272/8,708/397.2 μs; learned four-coordinate split 320/9,104/372.5 μs; coupled17 272/9,028/316.7 μs; fixed scalar 272/8,512/331.2 μs; fixed four-coordinate 320/8,512/346.9 μs; unmaintained scalar 272/8,512/325.2 μs; nearest prototype 256/0/172.4 μs. All arms also depend on 4,072 shared representation/readout bytes; the convenience loader kept the 8,512-byte parent resident even if not used. The Boolean control is four bytes; float state is float32. Main fit loops used 108.84 summed worker CPU seconds; per-worker RSS samples reached 314.84 MiB, but concurrent peak was not measured. All 44 new unit tests passed; 45 configurations/9,210 summary rows and 308,317,440 overlapping saved answer positions were internally checked. One full split4 fit and 90 two-RNG snapshots were reproduced. The unchanged foundation's reported 68 tests and 974-file manifest passed. Full historical 1,111-test qualification, Windows, target-device budgets, energy and low-bit state were untested.

**Interpretation and limits:** Separating a learned existence lane from frozen content retained the writable lifecycle at nominal corruption, but fixed sign/mean controls matched its metrics. The jointly refit map showed a targeted benefit for status after a fault but failed the joint noisy lifecycle, and stronger noise damaged both content and status. Neither learned nor protected presence proves factual correctness or authority. The follow-up recommendation was to keep content, existence, and present-but-unreadable state distinct and qualify migrations when changing their representations.

**Source locators:** `Research/NSS_NBR01_ExistenceContent005_v0.1.zip::NSS_NBR01_ExistenceContent005_v0.1/REPORT.md` §§1–9; `Research/NSS_NBR01_ExistenceContent005_v0.1.zip::NSS_NBR01_ExistenceContent005_v0.1/SUMMARY.json` and `evidence/results/` for complete traces; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q005 row.


<a id="pass-cm01"></a>

### CM01 — Grounded reference packet for fixed-weight retrieval

**Broader question category:** Does a bounded, externally managed context/reference channel help preserve/use exact knowledge and reduce identity ambiguity without growing a transcript? (G03 state continuity; G06 record identity; G07 exact lookup versus approximate learned reading.)

**Specific question:** On a fixed, noisy record-reader task, can a small workspace constructed from observable selection/correction events replace a noisy numerical query with a canonical query and improve a frozen reader, and does structured representation differ from serializing identical fields?

**Type and status:** Completed bounded fixed-weight interface pilot. No training, no optimizer updates, and no Q010 export changes. The experiment was CM-01 in the latest `NSS_Context_Management_v0.1` protocol, not an earlier similarly numbered MicroContext draft or a separate Q010-P1 proposal.

**Systems and arms:** The base learned reader is evaluated using A, the original numerical query; B, a structured workspace; and C, exactly the same workspace fields serialized as UTF8_BYTE_V1. B/C match all 7,680 main reader/case comparisons. The workspace is a persistent 56-byte packet (26 bytes in a hypothetical packed semantic encoding) with version/scope/handle/revision/binding-event reference/operation, derived from public observable management events. It is checked/read by deterministic code, retained across events and consulted at a learned read endpoint. It is not an always-active learned token stream or a language-model prompt. The manager can return the original or previously observed canonical query, or abstain; it does not supply an expected answer. A public exact lookup control follows a valid observed reference; a privileged exact-owner control uses isolated ownership truth and is never pooled with ordinary readers.

**Method and data:** Eight new episode families, three development/five held out, eight strata and eight labeled records per stratum; five fixed model seeds 1201–1205 repeated the same inputs. The retained E01 report does not enumerate per-export parameter counts or architecture details for all 15 frozen readers. Each case has a fresh path-length-one source graph, 16 catalogue codes of dimension 17 and one learned reader stage. At most two indexed lookups occur per management request. A retained Q010 case generator supplied synthetic inputs; the independent scorer re-derived source keys/values/masks from seeds without importing producer code. Before any generated fixture/main cases, configuration and 2,284 seed allocations were frozen; seed scan covered 5,091 retained files/298,234,599 bytes. Thirteen non-neural contract test methods and a fresh-process fixture/replay passed. This is internal implementation independence and exact replay, not third-party replication. CM-02/03/05 and Q010-P1 were not launched as part of CM01.

**Arm-by-arm primary results:** Each learned-reader cell is 40 held-out records × five fixed seeds = 200 repeated reader/case assessments, not 200 independent episode families.

| Reader/arm | Ordinary known, original → workspace | Close identity, original → workspace |
|---|---:|---:|
| Near reader | 157/200 (78.5%) → 200/200 (100%) | 88/200 (44%) → 142/200 (71%) |
| Ordinary reader | 113/200 (56.5%) → 200/200 (100%) | 73/200 (36.5%) → 129/200 (64.5%) |
| Attention reader | 114/200 (57%) → 200/200 (100%) | 62/200 (31%) → 108/200 (54%) |

The predeclared primary near reader gained 27 points on close identities and 21.5 points on ordinary known records. All five held-out families met the primary close-gain/control rule; the family improvements were +22.5, +30, +45, +27.5 and +10 pp, the last exactly 4/40 on its denominator. Ordinary-arm exploratory gain failed in CMEVAL-05 (47.5%→45%, −2.5 pp). Attention met its gain/control rule in each family but its pooled close score remained lower than the near reader. B/C always tied: no benefit for serialization was demonstrated.

**Noise and negative results:** In the primary near arm, close recall barely moved at sigma .01 (71/100→70/100) but rose at sigma .2 (17/100→72/100). Ordinary bound-known recall at .01 was already 100/100 for both modes, while at .2 it rose 57/100→100/100. Unbound-known at .01 was 100/100 both and at .2 66/100 both; unbound-absent at .01 was 0/100 and at .2 34/100 both. The net gain is therefore chiefly high-noise query reconstruction, not a general solution to close identity. Public exact retrieval was 40/40 on held-out ordinary-known and 40/40 on close-identity references, outperforming the learned hybrid whenever the reference was valid.

| Primary near held-out case | Task correct | Manager abstained | Wrong reference accepted |
|---|---:|---:|---:|
| Stale revision, revision case | 0/100 | 100 | 0 |
| Stale revision, deletion | 100/100 | 100 | 0 |
| Foreign scope checkpoint | 0/200 | 200 | 0 |
| Detectably wrong reference | 0/100 | 100 | 0 |
| Wrong reference with no public cue | 33/100 | 0 | 100 |
| Correction | 100/100 | 0 | 0 |
| Unresolved correction conflict | 74/100 | 0 | 0 |

These refusals correctly block observably invalid bindings but still lose a known answer in 400/500 assessments. All 100 no-cue wrong bindings were accepted; the apparent 33/100 content successes do not validate provenance. Across 64 opposite-truth pairs, all public history/workspace/numerical inputs are byte-identical; deterministic processing cannot infer the missing origin distinction (50% balanced accuracy). The learned-interface negative table retains 10,571 incorrect main rows; 256+4 exact-control errors remain in main/fixture totals. Total reported calls including replays were 21,186/30,816 cap and optimizer updates were zero.

**Measured resources:** The 56-byte packet (26 bytes if its semantic fields were hypothetically packed) is not the full working set. Each case’s public K/V/valid arrays were 2,192 bytes, output resolver catalogue/symbol arrays another 1,232 bytes, query 68 bytes; canonical public journal JSON was 12,897–14,111 bytes and materialized directories 13,374–14,367 bytes, before the binding index. Across 512 main records the manager processed 8,832 public events and logged 448 workspace changes; B made 544 indexed lookups returning 246,683 serialized bytes. Python object/lookup counts are retained but not a complete native allocation measure. Supervised stages through main replay took 55.64 s; conservative shared clock at that point was 780.92 s, and through relocated delivery QA 1,247.85 s. Sampled process-tree RSS was 627,650,560 B (598.6 MiB), at 0.1 s sampling; the short pre-instrumentation extraction has no continuous peak claim. Total model calls including exact replays were 21,186/30,816 cap, 492 physical forward batches, and zero optimizer updates. These are study host costs, not deployed memory or latency.

**Interpretation and limits:** CM01 shows grounded external reference management can improve this fixed reader, primarily under high query noise. It does not show native learned tokens, autonomous writing, a whole-system memory saving, memory compression, recurrent-state control, long-horizon cognition, or that neural retrieval is needed when a valid exact pointer exists. The packet is tiny relative to its JSON archive/index and Python runtime costs; report explicitly declines net efficiency. It does not fill any Q010 training/raw-evidence gap.

**Source locators:** `Research/NSS_CM01_Execution_v0.2.zip::NSS_CM01_Execution_v0.2/REPORT.md`; `Research/NSS_CM01_Execution_v0.2.zip::NSS_CM01_Execution_v0.2/protocol/PROTOCOL.json`; `Research/NSS_CM01_Execution_v0.2.zip::NSS_CM01_Execution_v0.2/protocol/SEEDS.json` (model seeds 1201–1205; PCG64/digest-derived case seeds); `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E01__NSS_CM01_Execution_v0.2__REPORT.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/CM01_v0.2_20260924/`.


<a id="pass-cm02"></a>

### CM02 — Reference continuity, revisions, and freshness policy

**Broader question category:** Can a compact context reference survive events, task switches and revisions, and what trade-offs appear between a resident context, ordinary exact indexing, and no retained selection? (G03 persistent state; G07 exact versus approximate retrieval; related G06 binding.)

**Specific question:** With fixed Q010 near-reader exports, does a two-task workspace preserve current selection/history through delayed queries and changes better than a conventional dictionary/index or discarding selection history; how does pinning a selected revision compare with following a later valid revision?

**Type and status:** Completed deterministic information-management study. No training and zero optimizer updates; all 15 Q010 exports remained byte-identical. This was not a native neural-memory or learned-token experiment.

**Systems and arms:** Five frozen 818-parameter near readers (seeds 1201–1205, 3,272 weight bytes each) read the same unchanged numerical interface/catalogue decoder. W is two 56-byte ASCII UTF8_BYTE_V1 reference strings (one/task), containing the declared reference fields. I is a conventional two-entry dictionary holding the same six semantic fields as immutable tuples. O discards retained selection history and uses the original numerical query/store. W and I share revision-pinned checks: committed events update task entries; switches preserve both, corrections change the addressed entry, conflict marks it unresolved, and revisions/deletions do not silently refresh a pinned selection. Queries are read-only. Four exact non-neural controls are X_W (validated pinned workspace), X_I (validated pinned index), X_S (reconstruct the observed prefix then apply the same pinned policy), and X_latest (follow a valid observed revision chain). These controls differ in retrieval policy and are not repeated across neural seeds.

**Method and data:** 32 chronological sequences, three development and five held-out families, four sequence templates/family. Each has a fresh 16-record catalogue, two task contexts, 16 registrations plus activation, then events 0–64. Queries occur after 0,8,16,32,48,64: 192 total query occasions, 120 held out across 20 sequences/five families. The five frozen readers repeat each occasion; those repetitions are not independent episodes. A separate explicit chronology/scorer reconstructed truth, query, and binding without importing producer logic; fresh local replay matched retained arrays, outputs and metadata exactly. There were 29 frozen local source/protocol checks, 19 non-neural contract methods, and 384 changed-hidden/future envelope projections per main capture/replay; these are implementation checks rather than a formal security proof. No new recall-gain threshold was declared.

**Primary results:**

| Interface | Held-out correct readouts | Accuracy |
|---|---:|---:|
| O, no retained selection | 307/600 | 51.17% |
| W, compact workspace | 391/600 | 65.17% |
| I, ordinary maintained index | 391/600 | 65.17% |

W–O was +14 percentage points; W–I was exactly zero. W/I match on 192 routes/current-context choices and all 960 paired reader/query decisions. Family W/I vs O accuracy was CM02EVAL-01 58.33/45.83 (+12.50 pp); -02 64.17/63.33 (+0.83); -03 73.33/48.33 (+25); -04 63.33/48.33 (+15); -05 66.67/50 (+16.67). Direction was positive in each family, but the report did not turn these observations into a new statistical gate. At sigma .01, O was 222/300 (74%) and W/I 202/300 (67.33%, −6.67 pp). At sigma .2, O was 85/300 (28.33%) and W/I 189/300 (63%, +34.67 pp). These pools also vary event/policy conditions, so the noise comparison is not a clean factorial estimate. For unchanged-target delay/switch streams, W/I reached 104/150 (69.33%) versus O 78/150 (52%); at D:64 W/I retrieved only 14/25 while exact retrieval had all five unique endpoint answers.

**Exact retrieval and revision-policy outcomes:** X_W, X_I and X_S each returned 100/120 held-out correct occasions (83.33%); X_latest returned 105/120 (87.5%). These deterministic controls are once per occasion, not 600 outcomes. At F:16, a selected entity had a valid newer revision and a current answer: pinned W/I correctly treated the selected old reference as stale, so W/I had 0/25 learned outputs; X_W/I/S returned UNKNOWN on all five unique current-answer occasions. X_latest followed the observed revision chain and recovered 5/5 current answers. O happened to answer 16/25. At F:48 the record was deleted: W/I returned correct UNKNOWN 25/25, O did so only 2/25, and all exact controls returned UNKNOWN 5/5. This is a deliberate difference between “same selected revision” and “continuing entity’s current content,” not a post-result change in W/I.

**Negative cases and limits:** At unresolved conflict C:32, W/I were correct 12/25. In publicly consistent but wrong-intent N:16/N:32, W/I had correct content 10/50 and accepted the wrong intended binding for all 50 readouts; exact retrieval followed the same plausible wrong pointer and was wrong on 10/10 unique main-intent occasions. Alternate hidden-intent scoring on identical inputs gave W/I 40% balanced correctness, O 39%, exact controls 50%; no deterministic method can satisfy both hidden labels. Main negative rows were 1,165 learned plus 120 exact-control errors; fixture retained 14 and 15. The study is not a proof of faultless reference continuity: W/I intentionally trade away some current-revision recall in favor of stale-reference refusal. The string interface has 112 ASCII bytes total, but a resident Python graph, journal, record store, row index, arrays and transient parser remain. W saved only 24 bytes of peak Python object graph per held-out family versus I, while using more parsing transients, packet writes/decodes and logical returned bytes; the report rejects a meaningful total-memory/efficiency advantage. Ordinary indexing did the same selection work without byte encoding.

**Measured representation costs:**

| Seed-1201 held-out cost observation | W workspace | I ordinary index |
|---|---:|---:|
| Mean resident object graph | 117,407.72 B | 117,440.47 B |
| Maximum resident object graph | 183,508 B | 183,532 B |
| Maximum route-time transient controller graph | 169,155 B | 168,945 B |
| Semantic task fields rewritten per family | 884 B | 884 B |
| Selection-object shell bytes allocated per family | 3,298 B | 2,992 B |
| Packet encodes / decodes per family | 34 / 50 | 0 / 0 |
| Event-plus-query indexed reads per family | 560 | 560 |

W’s 24-byte lower maximum resident graph met only the narrow declared object-inventory comparison, while its route-time parsing transient was larger, it allocated 306 more selection-shell bytes, rewrote 1,904 packet bytes, decoded 50 packets, and returned 1,500 more logical bytes/family. It is therefore not meaningful total memory compression. Prefix-scan X_S visited 5,520 events across held-out queries; ordinary indexing does not inherently rescan history. A shared experimental model-input cache grew to 9,145,833 object-graph bytes and is not free deployed memory. Exact retrieval incremental costs must be added to W/I manager costs; X_S also pays reconstruction and X_latest its revision policy/index. These are object/accounting measurements, not actual hardware/network traffic or optimized deployment allocation.

**Attempt and cost history:** Versions v0.3/v0.4/v0.5/v0.6 attempted 45/1,175/1,175/3,600 model forwards respectively; only v0.6 completed the main capture/scoring/replay, while interrupted attempts remain preserved and charged. Two in-flight attempts had no acknowledged completion (5,993 acknowledged of 5,995 attempted), under the 6,000 cap. Main replay matched 14,400 arrays/187,200 numeric elements and 16 score files; carried fixture matched 360 arrays/4,680 elements. There were zero optimizer updates. The shared study clock through replay was 1,726.40 s, and through delivery QA 2,145.57 s, under two hours; sampled process-tree RSS peak 597,893,120 B, container 1,920,397,312 B. These are this CPU host's supervised samples, not deployment latency/peak guarantees; interrupted supervisors and the initial extraction did not produce continuous receipts. Complete completed-run, failure, cost, and negative evidence is retained. Historical Q010 training omissions, original verifier failures and reconstructed underflow amendment remain unchanged.

**Interpretation:** The bookmark survives this tested changing library, but an ordinary dictionary/index works exactly as well. Exact revision following is a different contract from conservative pinning. Neither interface detects a plausible but wrong intent without public disambiguating evidence. CM02 motivates a separately specified native recurrent/context study; it does not itself test one, train one, or authorize it.

**Source locators:** `Research/NSS_CM02_Execution_v0.6.zip::NSS_CM02_Execution_v0.6/REPORT.md`; `Research/NSS_CM02_Execution_v0.6.zip::NSS_CM02_Execution_v0.6/protocol/PROTOCOL_v0.6.json`; `Research/NSS_CM02_Execution_v0.6.zip::NSS_CM02_Execution_v0.6/protocol/SEEDS.json` (reader seeds 1201–1205; seed-file status is proposed allocations only); `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E02__NSS_CM02_Execution_v0.6__REPORT.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/CM02_v0.6_20260924/`.


<a id="question-3"></a>

## 3. Can processing depth, binding and repair preserve relations and identity?


<a id="pass-q006"></a>

### Q006 — Content-Based Binding and Useful Processing Depth (BindingDepth006)

**Broader question category:** Recurrent computation and whether relations can be recombined from stored records (G04, G06, G03).

**Specific question:** Can learned content matching follow multi-link relationships at controlled internal depth while preserving absence? Does iterative query processing help with an eight-link chain beyond the trained maximum, and how does a shared hop compare with untied stages, generic attention and exact traversal?

**Type and status:** Registered five-seed fixed-weight synthetic relational retrieval study, with post-main diagnostics separately labelled. Completed; structured readers are research references, not qualified serving cores.

**Systems and arms:** Each episode used 16 random 17-coordinate entity codes (16 identity coordinates plus UNKNOWN), two rooms, explicit source/value fields, Boolean relation presence, qualified full-vector writes, and room/self terminal records. The shared record-hop had 818 learned projection/threshold parameters and repeatedly attended across all live records; the gated-hop added a GRU transition (2,654 parameters). The untied-hop4 comparator used four separately learned attention stages (3,272 parameters), normally executed once; a `cycled4` intervention explicitly repeated those stages. Generic shared and four-block cross-attention controls had 10,850 and 36,482 parameters. An 818-parameter learned binder decided match/new from vectors and live keys, and exact byte-key traversal was run over the same workspace as a control. State was not maintained by the Q003 restorative model. An external decoder codebook and intermediate per-round targets were supplied; the correct next record/slot was not.

**Method and criteria:** Five paired seeds 801–805 produced 30 fitted checkpoints (25 readers and five binders), 156,000 optimizer steps, and 9,984,000 example presentations. Readers each received 6,000 steps on 64 examples; binders 1,200. Readers trained on at most four-link paths and 1/2/4 processing stages. Evaluation included up to eight links and eight query rounds; eight-round paths/depth were inspected in development, so they were not wholly untouched architecture-selection variables. Episodes included missing links, writes, corrections, clears, reset, background relations, slot order variations, and identity/query noise. Competence was ≥95% on known and missing four-link visible conditions across sufficient depth. All reader weights remained fixed during inference; extra rounds did not alter weights or event count. Replication is the five paired seeds, not 7,920 replay rows or 1,013,760 saved answer evaluations.

**Documented results — visible fact competence and eight-link depth:** At four links/four stages, means ± sample SD across five seeds were:

| Mechanism | Established chain | Required link missing |
|---|---:|---:|
| Shared record-hop | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Gated-hop | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Untied four-stage attention | 100.00 ± 0.00% | 99.38 ± 0.65% |
| Shared generic cross-attention | 90.00 ± 6.31% | 72.19 ± 5.94% |
| Fixed four-block generic cross-attention | 95.16 ± 3.47% | 79.53 ± 3.47% |
| Exact byte-key traversal | 100.00 ± 0.00% | 100.00 ± 0.00% |

Record-hop, gated-hop, untied-hop4 and exact traversal passed the joint ≥95% known/missing visible screen at h1/h2/h4 in all five seeds; both generic cross-attention candidates passed in 0/5. On eight-link visible problems at eight actual rounds, record-hop scored 100% known/100% missing, gated-hop 100%/99.84%, exact traversal 100%/100%. Shared/gated readers had 0% final-room accuracy at one, two or four rounds, then 100% at eight; their early outputs were intermediate entities, not necessarily wrong terminal judgments. Standard untied-hop4 was limited to its four learned stages under an eight-round allowance and remained 0% known; when its four stages were explicitly cycled twice, it reached 100% known and 99.06% missing. This shows that extra execution can help this trained structured procedure; it does not isolate a unique advantage from shared weights.

**Retention separate from depth:** For the shared reader after 1,024 unrelated events, known accuracy with state retained versus removed was: one-link at 1/2/4/8 rounds, 99.84/99.84/99.69/99.69% versus 0% throughout; four-link, 0/0/99.69/99.53% versus 0%; eight-link, 0/0/0.31/99.22% versus 0%. The gated and exact readers achieved 99.38% on the eight-link retained-state case; much of the small gap from 100% existed already at delay 0 due to initial binding. The store remained bounded by entities rather than event transcript length; 1,024 events mainly updated one unrelated relation.

**Lifecycle and representation diagnostics:** After 64 distractors, shared/gated/exact same-store accuracy by initial/correction/clear/rewrite/global reset/fresh scope was respectively 99.38/99.53/99.69/99.22/100/100%; 99.53/99.84/99.53/99.38/100/100%; and 99.53/99.69/99.69/99.38/100/100%. All three passed the declared ≥95% lifecycle screen in every seed, though 98.75% of sampled full stores were entirely correct in clean initial/corrected/cleared conditions and only 2.5% after noisy storage. Reversing slot order preserved answers; selected shared orthogonal recoding retained 100%. Shuffling key/value association reduced known-chain accuracy to 11.56%/11.72%; removing evidence gave 0% on known queries. With σ=0.02 noise per key/value coordinate after 64 events, both structured shared readers fell to 0% on four-link known cases at four rounds; σ=0.08 also gave 0%. Presence remained protected, so this was a combined binding/representation/readout stress.

Query-side noise showed 100% known four-link recall at perturbation 0.05, falling to 22.97%/26.56% for shared/gated readers at 0.2; exact byte lookup fell to 0% when query bytes changed. A separate exploratory 0.2-noise paired-query diagnostic with eight rounds yielded known/UNKNOWN: record-hop 22.27/100%; gated-hop 25.39/100%; shared generic attention 79.61/56.41% (41.52% unsupported room claims on missing cases); fixed generic attention 49.34/91.09%. These 200 rows were not main-gate evidence. A 32-record visible set had 100% known for both structured shared readers, with missing 99.84%/100%, still within the same synthetic code conventions.

**Resources, reproducibility and limits:** Store raw bytes were 2,192 per stream for 16 records (two 17-float fields plus one Boolean byte each); external codebook added 1,156 bytes, and query/model/attention/runtime buffers were extra. Batch128 median query time for record-hop was 0.317/0.556/1.078/2.030 ms at 1/2/4/8 rounds on one Linux CPU. Main training loops summed 654.42 s, development 170.38 s, and one full 6,000-step reproduction 19.53 s; these are not wall-time or device comparisons. All 52 new tests, 68 foundation tests and 44 unchanged Q005 tests passed (164 distinct). All 30 fits/configurations were internally regenerated, an independent Python/NumPy graph walk rescored 7,920 rows, one full reader fit was reproduced, and 20 store/RNG plus 100 query snapshots were checked. This was internal single-environment reproduction, not external replication. Full historical 1,111-test qualification, Windows, long-term use and language operation were not performed.

The study supports more computation for a trained relational procedure on this task; it does not establish general reasoning, attention/recurrent family superiority, biological fidelity, learned open-ended relationship semantics or arbitrary noisy-memory recovery. It suggested a separate robust identity/query alignment study rather than online learning or a core replacement.

**Source locators:** `Research/NSS_NBR01_BindingDepth006_v0.1.zip::NSS_NBR01_BindingDepth006_v0.1/REPORT.md` §§1–11; `Research/NSS_NBR01_BindingDepth006_v0.1.zip::NSS_NBR01_BindingDepth006_v0.1/SUMMARY.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q006 row.


<a id="pass-q007"></a>

### Q007 — Compatible Restoration, Relationship Traversal and Failure Isolation (RepairBinding007)

**Broader question category:** Representation and identity binding, memory recovery and the limits of approximate identity (G06, G07; G03 for maintenance timing).

**Specific question:** Can a learned or exact dictionary-conditioned restorer repair Q006's frozen record-hop readers without retraining them, and can either system distinguish a damaged familiar identity from a truly unregistered one?

**Type and status:** Five-pair fixed-reader synthetic restoration study with separately labelled post-main cadence/query diagnostics. Completed; compatible identity repair retained as a bounded building block, with no general-memory qualification.

**Systems and arms:** The study reused five frozen record-hop readers, five gated-hop readers and five binders from Q006, using the same 17-coordinate identity ABI. Protected relation presence, scopes, full-vector writes and exact identity codebooks were supplied. Ten new restorers were fitted in pairs: a 2,257-parameter intrinsic residual MLP without a catalogue and a 225-parameter learned dictionary-conditioned repair that received the episode's canonical symbol set. Exact nearest-code repair received the same dictionary. All three could be applied periodically or late; the original shared/gated readers remained fixed. Additional arms used repair disabled, normalization only, key-only or value-only repair, and exact same-store traversal. Missing relation and unregistered identity tests were distinct: a symbol dictionary does not contain graph edges or tell whether an edge was ever observed.

**Method and criteria:** Seeds 901–905 paired with Q006 seeds 801–805; each of ten new fits completed 1,800 AdamW steps on batches of 96 (18,000 steps; 1,728,000 sequence presentations). Training perturbations were 0/0.02/0.05/0.10/0.20, with 5% erased vectors labelled UNKNOWN. Each main scenario contained 64 episodes per pair, 32 with an established relation chain and 32 with a missing link. Evaluation included key/value corruption, query-only corruption, four/eight-link traversal, 64/1,024 event horizons and different maintenance schedules. The sources remained fixed during all inference. The primary nominal screens were ≥95% known and missing-link behavior across five pairs; the main long condition required adequate repair through the declared horizon. Post-main matched-cadence and paired-query diagnostics are not promoted to preregistered main results.

**Documented outcomes:** On primary record-hop known-destination accuracy across five pairs, the nominal corruption rows were:

| Damage and horizon | No repair | Intrinsic MLP | Learned dictionary repair | Exact nearest repair |
|---|---:|---:|---:|---:|
| Keys only, σ=.02 × 64 | 2.50% | 0.00% | 100.00% | 100.00% |
| Values only, σ=.02 × 64 | 3.12% | 0.00% | 100.00% | 100.00% |
| Keys + values, σ=.02 × 64 | 0.00% | 0.00% | 100.00% | 100.00% |
| Keys + values, σ=.02 × 1,024; eight links | 0.00% | 0.00% | 100.00% | 100.00% |

Both dictionary-assisted restorers also returned 100% correct UNKNOWN for missing relations in these rows; the gated reader independently passed the nominal screens. At stronger σ=.08 × 64, learned repair scored 99.38 ± 1.40% known and 99.38 ± 1.40% UNKNOWN, while nearest repair remained 100%/100% on these samples. Yet the noisy keys remained nearest their intended codes 99.83% of the time and values 99.96%, while four-link answer accuracy without repair was 0%; this indicates an overly strict frozen matcher can fail before all identity information is lost. Repairing keys alone yielded only 3.12 ± 3.12% known accuracy and repairing values alone 2.50 ± 2.61%; both were needed. A longer eight-link question still required eight query rounds after repair.

At 64 ticks, applying 64 repairs only at the end reached 99.38 ± 1.40% known; after 1,024 unmaintained ticks, 1,024 late repairs recovered only 0.62 ± 1.40% known with learned cleanup and 1.25 ± 2.80% with nearest cleanup. A separately labelled post-main paired four-link diagnostic compared periodic versus late repair on the same graphs/noise: both learned and nearest periodic repair recovered 100% known/UNKNOWN. This supports cadence before drift exceeds recovery, not an optimum. A separate clean 1,024-step check found dictionary maintainers stable while the intrinsic MLP drifted to 0% known.

The live learned-binder lifecycle (initial install/correction/clear/rewrite/reset/fresh install) passed the ≥95% nominal screen in all five pairs for both dictionary repair mechanisms, with 100% at the initial/correction/rewrite points, 100% UNKNOWN after clear/reset, and 99.38 ± 1.40% known after fresh installation. These are specified query checkpoints, not every intermediate read. For intact storage with σ=.2 query noise, no repair reached 26.25 ± 13.55% known/100% UNKNOWN; either dictionary repair reached 100% known but 99.38% UNKNOWN. At σ=.4, learned cleanup reached 80.62 ± 7.78% known/87.50 ± 3.83% UNKNOWN and nearest cleanup 89.38 ± 2.80%/84.38 ± 4.94%.

For identities deliberately outside the codebook:

| Query about unregistered identity | Correct UNKNOWN | Unsupported room answer |
|---|---:|---:|
| No repair | 100.00% | 0.00% |
| Learned dictionary repair | 45.94% | 47.81% |
| Nearest-code repair | 29.38% | 62.81% |

The remaining errors were unresolved nonterminal outputs. The dictionary arms assumed a matching canonical symbol exists. A wrong dictionary geometry gave 0% known accuracy; a different valid destination and full erasure likewise produced 0% correct recovery for all arms. The dictionary knows possible symbols, not lost relations.

**Resources, verification and limits:** The 16-record state used 2,192 raw bytes, plus a 1,156-byte identity dictionary and 68-byte query vector per stream; model, temporary and process allocations were extra. Per-batch64 key/value cleanup medians were 5.981 ms learned dictionary, 0.382 ms nearest projection, 0.608 ms intrinsic MLP and 0.047 ms normalization. The learned exact-reference repair was thus slower than the simple exact projection in this implementation. All 34 new, 52 Q006 and 68 foundation tests passed (154 distinct). Fresh-process checks reproduced 4,200 rows and 268,800 answers; an independent scorer replayed results; ten model fits and 25 snapshot/continuation cases were checked. These are internal one-environment checks, not external replication. Full historical 1,111-test qualification, Windows and device profiling were not performed. No biological or hardware noise model was used.

The bounded combination works under the declared conditions, but novelty rejection is a separate requirement. Tight matching can lose a perturbed familiar identity; permissive repair can turn a novel vector into an unsupported old relation. This result does not establish which future-language identity rule should be used.

**Source locators:** `Research/NSS_NBR01_RepairBinding007_v0.1.zip::NSS_NBR01_RepairBinding007_v0.1/REPORT.md` §§1–10; `Research/NSS_NBR01_RepairBinding007_v0.1.zip::NSS_NBR01_RepairBinding007_v0.1/SUMMARY.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q007 row.


<a id="pass-q008"></a>

### Q008 — Familiarity-Aware Repair and Writable Novelty (MembershipRepair008)

**Broader question category:** Representation/binding and exact-versus-approximate identity admission (G06, G07).

**Specific question:** Can geometric or learned membership gates reject unfamiliar inputs while preserving noisy known identities, recovered state, missing answers and the ability to register and write a genuinely new identity?

**Type and status:** Five-pair registered membership/repair study with a post-hoc near-duplicate binder diagnostic. Main comparison completed, full joint target not met; NBR-01 remains open.

**Systems and arms:** Five new 633-parameter learned match heads were trained over Q006 frozen readers/binders and Q007 frozen restorers. They were paired with a simple geometric gate calibrated on the same held-out evidence, each combined with nearest-code repair. Controls were unconditional nearest projection and unconditional learned repair. Stage-A ablations considered distance-only and margin-only decisions; cross combinations paired both gates with the Q007 learned dictionary restorer. No reader was retrained. Inputs included exact known, mildly altered known, heavily altered known (q20), independent unregistered, near-novel, doubled-magnitude and quarter-magnitude codes. Stage-B tested the existing association reader and whole registration/write/correction/clear lifecycle. Separate internal maintenance and external-query policies were examined under long delay.

**Method and criteria:** New seeds 1001–1005 each trained one head for 1,200 AdamW steps, batch 256 (6,000 main steps; 1,536,000 presentations). The geometric gates used 4,096 examples in each of seven classes per pair (143,360 total main calibration labels), and learned gates also consumed their counted training data. Main source/checkpoint/calibration lock preceded main episode scoring but followed disclosed pilot information. Each membership cell averaged five pairs × 1,024 episodes per stratum. Main state tests used 64 streams/pair; cadence tests extended to 1,024 σ=.02 noise events/eight-link queries. The registered joint screen required each candidate to meet the empirical 1% ordinary unregistered false-acceptance ceiling while retaining the declared ≥95% q20 supported coverage and allowed known-repair regression. It also required the state/missing/lifecycle tests. All five pairs and failed strata remain in the reported denominators.

**Membership tradeoff:**

| Mechanism | Exact known | Mild known q05 | Altered known q20 | False acceptance: independent unregistered |
|---|---:|---:|---:|---:|
| Unconditional nearest | 100.00% | 100.00% | 98.85% | 100.00% |
| Unconditional learned repair | 100.00% | 100.00% | 98.85% | 100.00% |
| A: geometric gate + nearest | 100.00% | 100.00% | 70.16% | 0.43% |
| B: learned gate + nearest | 100.00% | 100.00% | 66.93% | 0.55% |

Across 5,120 independent unregistered inputs, A accepted 22 and B accepted 28. On a second noisy-independent negative stratum, A was 0.41% and B 0.43%. The per-pair ordinary-negative gate results and Wilson intervals were: A pairs 1–5 = 5/1024 (0.21–1.14%), 5/1024 (0.21–1.14%), 5/1024 (0.21–1.14%), 2/1024 (0.05–0.71%), 5/1024 (0.21–1.14%); B = 8/1024 (0.40–1.53%), 7/1024 (0.33–1.40%), 5/1024 (0.21–1.14%), 3/1024 (0.10–0.86%), 5/1024 (0.21–1.14%). These are descriptive episode intervals, not future risk guarantees. End-to-end q20 supported destination accuracy was 75.63% for A and 71.25% for B. Neither selective option met the joint criterion in any of five pairs for any of the four gate/restorer configurations; q20 coverage failed despite good ordinary novelty rejection.

With 64 streams/pair and σ=.02 corruption to both fields, known/missing answers at 64 ticks and after 1,024 ticks/eight links were 100/100% for unconditional nearest, unconditional learned repair, A+nearest and B+nearest. Unsupported room claims for an unregistered query were 67.50%, 49.38%, 0%, and 0%, respectively (320-query subset; zero of 320 is not zero risk). The eight-phase registration lifecycle table was 100% task accuracy for both A and B at before-register, after-register, after-write, correction, clear, rewrite, reset and fresh. This is a queried checkpoint result, not an all-time guarantee; registration is explicit and the relation binder remains a separate learned operation.

**Maintenance cadence:** with the same 1,024-tick, σ=.02/eight-link family, supported/missing answers were: every-tick repair A/B 100/100/100% missing; every 8 ticks 100/100/100%; every 32 ticks 40.00/10.62/100%; and read-time-only repair 0/0/100%. Every-eight reduced sweeps from 1,024 to 128 while preserving these nominal outcomes; it does not establish an eightfold full-system speedup. Unconditional nearest scored 99.38% supported at 32 ticks. External admission gates suitable for novel queries were too conservative for recovering previously established state.

For unregistered codes near a known identity at distance 0.1, both gates accepted all 5,120 (end-to-end unsupported room answers 50% of 320 queries). On equal two-code mixtures, B false acceptance was 0.21% versus A 6.41%; B retained 100% under doubled magnitude while A rejected all; both rejected all quarter-magnitude inputs. These stress differences did not erase q20 failure. In a post-hoc near-registered-collision diagnostic, B-nearest's binder accepted all 320 new writes but used an existing slot in 282 (88.125%) and actually replaced older content in 246 (76.875%); only 38 obtained a separate slot. The reader still answered the new query correctly in all main cases, masking the structural overwrite. A stricter A path blocked most such writes, but also risked rejecting useful writes. Registration and relationship binding are separate gates.

**Resources and limits:** Batch64 per-field timing medians (10th–90th percentile) were 1.020 ms (0.999–1.168) unconditional nearest, 4.142 (3.888–5.144) unconditional learned repair, 1.025 (1.012–1.125) A+nearest and 1.261 (1.199–1.472) B+nearest. Raw active state was 3,336 bytes/stream, before query tensors, model weights, buffers and evidence. The head adds 2,532 parameter bytes; fitting tensors total 10,152 raw bytes before activations and temporaries. Main head fitting summed 21.01 s; driver evaluation 653.26 s; sampled largest evaluation RSS was 432.3 MiB, below the declared 4 GiB process ceiling. All 45 new, 34 Q007 and 68 foundation tests passed. Independent scoring rederived 1,210 membership and 14,940 state/depth rows from saved data; fresh-process array replay and one full head fit were reproduced. Full 1,111-test suite, Windows, device budgets, language and long-running use were not tested. Float32 work was not low-bit learning, and the study is not a biological or hardware-fault model.

The selective gate is a useful precision-oriented option for ordinary novel inputs, not a full solution: q20 coverage and near-duplicate binding remain poor. The same mechanism should not be treated as an internal recovery gate without a provenance-aware policy.

**Source locators:** `Research/NSS_NBR01_MembershipRepair008_v0.1.zip::NSS_NBR01_MembershipRepair008_v0.1/REPORT.md` §§1–10; `Research/NSS_NBR01_MembershipRepair008_v0.1.zip::NSS_NBR01_MembershipRepair008_v0.1/SUMMARY.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q008 row.


<a id="pass-q009"></a>

### Q009 — Distinct Records and Provenance-Aware Recovery (IdentityBinding009)

**Broader question category:** Entity identity, relationship binding and correct use of owned records (G06, G07; G03 for restored internal state).

**Specific question:** Does explicit ownership prevent near-identity overwrites? Where do frozen numerical readers still fail when storage is exact? Can internal recovery use legitimate ownership information without applying the same conservative gate to external queries?

**Type and status:** Completed bounded five-pair NBR-01 experiment. Exact owner-keyed storage is an engineering reference; no learned pipeline passed the full joint identity target; NBR-01 remains open.

**Systems and arms:** The new `nbr009-owner-state-v1` store separated identity registration, record owner, scope/epoch, revision, relation presence, key/value readability, transaction state, and numerical key/value. Exact identity-keyed writing allocated by owner metadata; numerical inherited/continued binders chose match or NEW from vector similarity; an exact ownership guard could reject conflicting proposals; exact owner traversal was a read control. Frozen readers were inherited shared/gated record-hop models. Internal recovery used explicit owner metadata to rehydrate keys and nearest-code repair for values, while external queries used geometric gate A, learned gate B or unconditional nearest. Ten 818-parameter binders were continued with ordinary or near-negative preparation. A separate, rule-based cue experiment compared one noisy identity view, a duplicated view, two independent views and a single wider random code; it was not a trained semantic encoder or a change to the 17-coordinate reader.

**Method and criteria:** Five paired inherited reader/binder pairs (801–805) formed the reference. New ordinary/near-negative continuation seeds 1101–1105 each received 1,200 AdamW steps, batch 128 (12,000 optimizer steps and 1,536,000 example presentations). The near curriculum included close distinct identities and close competing identities at .01/.03/.10 perturbation. A 130-file source/spec/checkpoint identity lock preceded main scoring but followed pilots; it was a local lock, not external preregistration. Stage A used five pairs × six identity families × eleven variants × 64 episodes with lifecycle checkpoints. Stage B comprised 61 scenarios per pair, key/value/query corruption, 64/1,024-step horizons and maintenance schedules. A conditional cue diagnostic used 12 families ×1,024 episodes/pair and four rule feature arms. Each identity used 16 numeric coordinates plus UNKNOWN; up to 16 identities/records. Protected registry/owner metadata did not contain the relation graph or destination ID; owner could recover a key but not a lost destination value.

**Whole logical-map correctness after a new relation write:**

| Writer | Ordinary identities | Similar sources (.10) | Very close sources (.01) |
|---|---:|---:|---:|
| Inherited numerical binder | 99.69 ± 0.70% | 0.00 ± 0.00% | 0.00 ± 0.00% |
| Ordinary additional preparation | 100.00 ± 0.00% | 9.06 ± 3.01% | 0.00 ± 0.00% |
| Near-negative preparation | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Near-prepared binder + ownership guard | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Exact identity-keyed writer | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

At separation .10, near-negative preparation had 320/320 correct maps versus 29/320 for ordinary preparation and 0/320 for the inherited binder. At .01, every numerical binder wrote the wrong owner in all 320 cases; the near-prepared ownership guard blocked damaging proposals but also rejected every useful new write. Exact owner-keyed storage maintained all relations across every tested family and 7,680 transaction comparisons, but that is protected bookkeeping, not learned recognition.

With the exact store, jointly correct old/new/unaffected queries were:

| Ambiguity family | Shared reader | Gated reader | Exact owner traversal |
|---|---:|---:|---:|
| Ordinary | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Very close source identities | 20.00 ± 5.68% | 20.31 ± 4.42% | 100.00 ± 0.00% |
| Similar source identities | 99.06 ± 1.40% | 99.06 ± 0.86% | 100.00 ± 0.00% |
| Very close destination identities | 21.25 ± 5.70% | 0.62 ± 0.86% | 100.00 ± 0.00% |
| Very close intermediate identities | 17.50 ± 7.19% | 21.56 ± 6.39% | 100.00 ± 0.00% |
| Very close sources and intermediates | 5.94 ± 5.34% | 0.62 ± 1.40% | 100.00 ± 0.00% |

For internal maintenance after 1,024 σ=.02 noise events, repair every 32 events, eight-link queries and eight read rounds, established-chain / missing-link results were 41.88±10.50/100% for shared geometric admission on internal+external inputs; 11.88±4.07/100% for shared learned admission; 59.38±6.25/100% for owned-key rehydration + selective values; 65.62±11.05/100% for value repair + selective keys; 100/100% for owned-key rehydration + nearest values with external A; 100/100% with external B; and 99.38±1.40/100% for unconditional nearest. For the primary reader, these corresponded to 67/160, 19/160, 160/160 for each split A/B policy, and 159/160 nearest supported answers. This is reuse of legitimate stored ownership, not inference of arbitrary erased identity. Fully erased or wrong-valid destination values were not recovered.

Retained-state four-link tasks after 1,024 events reached 100% at four/eight rounds. Eight-link supported answers remained 0% at one/two/four rounds and reached 100% at eight; removing state yielded 0% at every depth. The separate rule-cue diagnostic reported known-input accuracy / ordinary-novel rejection / close-novel rejection: one 16-D view 68.48±4.59/99.79±0.08/0%; same view duplicated to 32-D, identical; two independent 16-D views 99.90±0.07/99.96±0.09/91.05±5.20%; one random 32-D view 99.73±0.19/99.39±0.26/0%. Even the independent second view falsely accepted 8.95% of close novelty and it carried cleaner information in the designated known-noise condition. More dimensions explain part of the gain; cue diversity is not uniquely causal here.

**Resources and limits:** Owner-state was 3,864 raw bytes per stream; this excludes readers, query buffers, metadata objects, logs and process memory. Ten completed fit loops used 29.32 s; five main-process timers summed to 644.75 s with overlap. In a quiet single-process CPU test, exact/learned write medians were 0.858/1.030 ms, shared-A maintenance 3.027 ms, split internal-A 1.789 ms; shared query was 2.085 ms at one round and 11.127 ms at eight. All 45 new, 45 Q008 and 68 foundation tests passed. Five main evaluations and 20,375 arrays were replayed; an independent scorer reconstructed 68,305 metric rows, and one full binder fit/80 continuations were reproduced. These are internal evidence checks. External replication, Windows, target-device use, long-running companion, biology and language tests were not performed. Full 1,111-test release qualification was not run; no training during evaluation or low-bit state was used.

The study closes neither arbitrary identity recognition nor all of NBR-01. It demonstrates the important separation: perfect exact ownership can preserve the map while a frozen learned reader still confuses close codes; conversely, learned preparation can help at moderate similarity and fail completely at the closest condition. Internal recovery may use trusted ownership, while external admission needs separate uncertainty handling. The proposed richer-cue arm supplies additional information and is not a learned fix.

**Source locators:** `Research/NSS_NBR01_IdentityBinding009_v0.1.zip::NSS_NBR01_IdentityBinding009_v0.1/REPORT.md` §§1–9; `Research/NSS_NBR01_IdentityBinding009_v0.1.zip::NSS_NBR01_IdentityBinding009_v0.1/SUMMARY.json` and `evidence/results/`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` Q009 row.


<a id="question-4"></a>

## 4. What was qualified, reconstructed or left unrecoverable?


<a id="pass-q010-hist"></a>

### Q010-HIST — Qualification010 v0.1 historical result (original study bytes missing)

**Broader question category:** Exact owned memory, learned record reading, state maintenance, and depth on a bounded synthetic relation-following task (G03 persistent state; G04 recurrent depth; G06 binding; G07 exact versus approximate recovery; also G02 baseline competence).

**Specific question:** Under a declared 16-record task, can compact shared recurrent readers and a larger task-adapted untied attention/pointer reader preserve and follow eight-link relations after writes and maintenance, and how do ordinary versus close-identity preparation compare with inherited-reader and exact-ownership controls?

**Type and status:** Historical scientific study whose report and delivery receipt survive, but whose original archive, implementation, training outputs, raw result arrays, source lock, and full protocol bytes are missing from this workspace. The numbers below are faithfully described in the retained report and are not independently recomputable historical findings. The report claimed qualification of a bounded hybrid reference; that claim must remain historical rather than being promoted to a currently verified original qualification.

**Systems and arms:** Every learned reader receives the same public key/value/valid-record/query tensors and shares the external task wrapper. Five inherited 818-parameter RecordHop checkpoints (families 801–805; trained before Q010) form the inherited arm. A cap-only arm uses those same weights with the attention-scale cap increased from 80 to 20,000. Ordinary continuation adds 6,000-step preparation to each inherited reader. Close-identity continuation uses the same initial readers and added budget, with half of its examples containing an unrelated identity perturbed at sigma .01–.15. The attention arm is described as eight untied self-attention/residual/layer-normalization/feed-forward blocks, width 32, two heads, learned pointer/copy outputs, explicit 17-coordinate inter-stage entity state, and 94,728 parameters. It is a task-adapted pointer-bottleneck comparator, not a generic language Transformer. Exact ownership traversal is a deterministic non-neural relation algorithm. The five surviving inherited reader checkpoints are distinct from the 15 claimed new checkpoints; no surviving original evidence establishes or permits tensor-level validation of the latter.

**Method and documented recipe:** Six development fits reportedly used 27,000 steps in total. The report says the main source/recipe/threshold/job set was locally hash-locked across 140 files before main fits/scoring, but the lock itself is absent. Three trainable main recipes (ordinary, close-identity, attention) were paired over seeds 1201–1205: five fits each, 6,000 AdamW updates, batch 64, paths up to eight, eight supervised stages. Reported objective: row-selection cross-entropy plus half squared code error; teacher forcing for the first 1,000 updates and every fourth update thereafter; learning-rate endpoints .0015 and .00015; weight decay 1e-5; gradient clip 5. Reported total: 90,000 main optimizer steps, 5.76 million sequence presentations, 46.08 million stage presentations. These are report-transcribed settings, not a complete executable specification: attention layout and initialization, loss reductions, RNG draws, optimizer defaults, cadence/index conventions, complete condition matrix, and exact source/seed formulas remain undocumented or unavailable. Development is not mixed into main confirmation. The report claims one full 6,000-step ordinary-fit reproduction and 90 continuation checks, but the underlying logs are unavailable here.

**Reported results:** The nominal headline is an eight-link/eight-stage problem after 1,024 Gaussian disturbance events (sigma .02 per coordinate), maintenance every eight events, and unrelated writes every 64 events; five paired sets each contain 128 streams, ordinarily divided into 64 supported and 64 missing-link queries. Reported aggregate table:

| Reported reader | Supported | Correct missing-link response | Complete nominal screen |
|---|---:|---:|---:|
| Inherited shared reader | 100.00% (320/320) | 99.69% (319/320) | 5/5 pairs |
| Cap-only, inherited weights | Report says its reported main answers match inherited reference | Reported as the inherited reference | Reported as reference control |
| Ordinary continuation | 100.00% (320/320) | 100.00% (320/320) | 5/5 pairs |
| Close-identity continuation | 100.00% (320/320) | 96.56% (309/320) | 0/5 pairs |
| Untied attention/pointer stack | 100.00% (320/320) | 98.12% (314/320) | 5/5 pairs |
| Exact ownership traversal | 100.00% (320/320) | 100.00% (320/320) | 5/5 pairs |

The close-identity continuation is a clear arm-level negative: passing this nominal row did not save its failure on required conditions/prefixes. Direct visible-fact scoring without between-stage cleanup reportedly met the ≥95% criterion for inherited, cap-only, ordinary, and attention in all five pairs, but failed in all five close-identity pairs. All readers required eight stages for ordinary eight-link supported answers: one/two/four stages gave 0% final supported-destination accuracy. Removing relation state, or running 1,024 disturbances without maintenance, yielded 0% supported answers. These are information ablations, not resource-matched competitors.

**Other retained report results:** At cadence 32, headline answers were unchanged, but whole-map correctness was only 638/640 stores; cadence 8 was retained as the reference. The reported ordinary registration/correction/clear/reset lifecycle had 640/640 correct checkpoint queries for inherited, ordinary, exact traversal; 615/640 for close continuation; and 639/640 for attention. At close-source separation .01 with all logical stores reportedly intact, assisted supported/missing answers were: inherited 83.44%/58.75%; ordinary 83.75%/63.44%; close continuation 85.31%/55.00%; attention 85.31%/64.06%; exact traversal 100%/100%. Without between-stage cleanup, close-source supported/missing was inherited 26.88%/79.06%; ordinary 22.81%/79.69%; close continuation 71.88%/47.81%; attention 54.69%/74.38%. Thus the targeted curriculum improved a narrow supported-answer score while worsening missing-information behavior and failing the complete screen. On independent unregistered inputs each primary pipeline reportedly emitted one unsupported terminal answer in 640 (0.15625%). On deliberately near-colliding unregistered identities, unsupported room answers were 50% for inherited, ordinary, attention, and exact pipelines, and 51.56% for close continuation. Erased or wrong-but-valid values remained damaging; sigma .2 known queries were screened to 69.06% supported for inherited/ordinary/attention/exact due to the common external gate. The exact owner/traversal control was both more accurate on the nominal task and cheaper in the reported timing table: 7.36/11.15 ms for batch 1/64 versus 9.57/14.52 inherited, 9.47/18.04 ordinary, 9.44/14.81 close, and 12.91/28.06 attention. The common owned-state payload was reported as 3,864 raw bytes/stream; the attention reader has 94,728 parameters versus 818 in the shared reader. These historical cost estimates omit broader process/deployment costs and are not target-device results.

**Interpretation and limits:** The report's bounded finding was ordinary shared-reader and task-adapted attention competence under its declared support, with exact traversal as a strong baseline; the close-identity continuation did not qualify as a replacement. It does not establish broad language ability, arbitrary identity recognition, production NSS, device performance, or the general superiority of recurrence or attention. Most importantly, archive/receipt integrity cannot supply missing evidence bytes. The surviving report's original archive size (302,820,867 bytes) and SHA-256 (`0d8a0e01…f2d5fe`) are receipt claims that cannot be compared to the absent original ZIP. Original code, complete lock/protocol, 15 new models, six development artifacts, full main arrays/results, source/test fixtures, and raw training traces are not available. The report preserves 151-test, 33,605-array, 19,960-row, 2,554,880-answer, and 90-continuation claims, but the present recovery audit cannot verify their contents. Reported 94,728 attention parameters do not uniquely identify its network. The correct historical conclusion is “reported pass/negative arms; original full qualification not currently reproducible,” not reconstructed scientific execution.

**Source locators:** `Research/NSS_WorkspaceSupport_v0.1.zip::Q010_Reonstruct/REPORT.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::Q010_Reonstruct/NSS_NBR01_Qualification010_v0.1_DELIVERY_VERIFICATION.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/recovery_audit.md` (historical byte gaps and report provenance); `Research/NSS_WorkspaceSupport_v0.1.zip::Q010_Reonstruct/RECOVERY_PROGRESS.md`.


<a id="pass-q010-recovery-base-v0-2"></a>

### Q010-RECOVERY-BASE-v0.2 — Partial inherited-reader recovery and smoke

**Broader question category:** What Q010 dependencies can be recovered byte-identically from its Q009 parent, and can a small source-derived adapter be smoke-checked without claiming the absent Q010 study? (G03/G06/G07; provenance/recovery engineering, not a fresh scientific qualification.)

**Specific question:** Does the retained v0.2 package provide a valid base for later fixed-reader reconstruction, and what did its bounded smoke actually verify?

**Type and status:** Read-only recovery/audit record for a partial recovery package. The smoke had already been recorded in the archive; no code or model was run for this chapter. It is explicitly `NEW_RECOVERY_SMOKE_NOT_010_QUALIFICATION`.

**Systems and arms:** The recovery package restores 134 selected source/evidence files from IdentityBinding009, plus five inherited 818-parameter `record_hop_801`–`805` checkpoints that are byte-identical to the Q009 parent. A newly written cap-only adapter (scale cap 80 to 20,000) and smoke harness are recovery additions derived from retained report detail; they are not original Q010 code. The exact ownership traversal is a software control. The parent inventory contains 35 checkpoints, but that broader inventory supplies none of the missing 15 Q010-trained checkpoints. No model tensor was deserialized in this research pass.

**Method and documented coverage:** The retained smoke receipt reports 25 cases and 575 arrays across the inherited reader, cap-only adapter, and exact control; zero optimizer steps and zero new Q010 checkpoints. Its summary says the 20 state-on cases passed known and missing queries for three profiles at depth 8. The audit independently compares all 134 declared parent-subset files and all five inherited checkpoints against the current Q009 archive, byte for byte; the recovery package's own 167 manifest-covered members also verify, but this establishes internal package consistency only. There is no 128-stream original main evaluation, 1,024-event horizon, live unrelated-write stress matrix, full timing/resource screen, or 90 continuation runs in this smoke. We inspected its receipt rather than rerunning it.

**Result and limits:** It is a useful authentic inherited-reader baseline and provenance-checked partial recovery, but it neither reproduces the historical learned continuations nor restores their training record. The reported historical receipt digest for the absent 302,820,867-byte Q010 original archive is not validated by the current 5,627,820-byte recovery package. The recovery adapter is a new reconstruction, and the five parent weights are pre-Q010 readers. No new Q010 candidate weights exist here.

**Source locators:** `Research/NSS_WorkspaceSupport_v0.1.zip::Q010_Reonstruct/NSS_Qualification010_Recovery_Base_v0.2.zip` (members `NSS_Qualification010_Recovery_Base_v0.2/provenance/PARENT_SUBSET.json`, `NSS_Qualification010_Recovery_Base_v0.2/provenance/CHECKPOINT_INVENTORY.json`, `NSS_Qualification010_Recovery_Base_v0.2/audit/reference_smoke/SMOKE_RESULTS.json`, `NSS_Qualification010_Recovery_Base_v0.2/spec/HISTORICAL_RECIPE.json`); `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/recovery_audit.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::Q010_Reonstruct/REPORT.md`.


<a id="pass-q010-inf-rec-v1-6"></a>

### Q010-INF-REC-v1.6 — Reconstructed fixed-weight inference recovery

**Broader question category:** Can saved Q010 main exports still be bound to the recovered historical contract and have inference gates independently rescored/replayed, despite missing optimizer history and raw training records? Does close-identity handling generalize? (G03/G06/G07, and G02 competence.)

**Specific question:** Using the 15 surviving exports and the recovered thresholds, do ordinary continuation, close-identity continuation, and task-adapted attention pass the frozen reconstructed inference gates over the declared 64-condition protocol, and what failures remain under deeper horizons, state faults, maintenance ablation, and novel identities?

**Type and status:** Completed v1.6 report-based inference recovery and re-evaluation. No training reproduction: zero optimizer updates. All 15 exports were hash-, tensor-, architecture-, seed-, fit-role-, and 6,000-update-metadata-bound to `NSS_NBR01_Q010_Reconstruction_v1.4`. The machine-readable status explicitly says `original_training_protocol_fully_requalified=false`. This recovered inference ledger is not the original Qualification010 execution and is not a substitute for the v0.2 inherited-reader smoke above.

**Systems and arms:** Per seed 1201–1205, six readers were evaluated: inherited 818-param reader; cap-only 818-param control; ordinary continuation; close-identity continuation; reconstructed task-adapted attention (86,464 parameters); and privileged exact-owner control. The 86,464-parameter attention export is the surviving v1.6 reconstruction, not the historical report's absent 94,728-parameter attention model. The task uses 16 records/eight stages, supplied catalogues/owner metadata and qualified writes. Core gate thresholds remained 0.90 for applicable core classes, 0.95 for direct visible facts and 0.90 at every declared cadence-8 durability checkpoint. They were recovered from the retained criteria digest, not refit to scores.

**Method, coverage, and resource controls:** One end-to-end integration fixture covered 64 conditions, 129 frames, 2,880 query chains and 19,104 logical stages. The main ledger covered 320 condition/seed pairs, 1,920 reader/condition/seed combinations, 645 frames, 449,640 independently scored query chains and 3,045,480 audited reader stages. There were 50,835 replay arrays/419,453,820 elements compared exactly; 11,520 condition/class coverage checks; 12,600 checkpoint/class checks; 18 named loader/underflow checks; and 23 unchanged fixture regression assertions (zero failed/skipped). Every declared depth/fault/lifecycle/durability phase was kept; non-lifecycle main conditions used 128 cases, lifecycle its declared single case. Independent scorer re-derived source truth and decoded expected versus predicted values. Fresh local replay compared arrays and case/query/event metadata exactly. This is internal independent implementation plus local replay, not third-party replication.

**Gate and negative results:** Ordinary continuation, close-identity continuation and task-adapted attention each passed all pooled frozen gates and all five seed-level gates (5/5; 83 checks per seed). Those passing narrow gates coexist with important retained negatives:

| Pooled diagnostic | Ordinary continuation | Close continuation | Attention |
|---|---:|---:|---:|
| State removed: supported | 0/320 (0%) | 0/320 (0%) | 0/320 (0%) |
| Erased values: supported | 143/320 (44.69%) | 143/320 (44.69%) | 143/320 (44.69%) |
| Wrong-but-valid values: supported | 165/320 (51.56%) | 165/320 (51.56%) | 165/320 (51.56%) |
| No maintenance, event 1,024: supported | 0/320 (0%) | 0/320 (0%) | 0/320 (0%) |
| Close source: supported | 199/320 (62.19%) | 229/320 (71.56%) | 168/320 (52.50%) |
| Ordinary novel query returns UNKNOWN | 640/640 (100%) | 640/640 (100%) | 638/640 (99.69%) |
| Near-collision novel query returns UNKNOWN | 0/640 (0%) | 0/640 (0%) | 0/640 (0%) |

The inherited/cap-only controls are retained in the detailed all-seed/all-condition matrices; the table above is limited to the three new candidate arms. All 133,658 incorrect query outcomes remain in the raw negative table, including intentional state-removal and low-depth negatives, and must not be confused with only failed qualification rows. The close source metric improved in this execution relative to the historical report's close continuation pattern, but close/collision novelty remains poor. This is a separate recovered inference pass on surviving exports; it does not adjudicate the missing original arrays or establish why historical and reconstructed scores differ. The amendment to the final-probability underflow bound (`eta=2^-126`, `u=2^-24`) is transparently reconstructed from retained rationale because the original v2 implementation and historical rejected row are absent. Thresholds, relative multipliers, scoring labels, decoder and exact replay were not changed. Three historical verifier errors remain recorded (two Windows byte mismatches and one unavailable lifecycle fixture); the 23 new fixture checks are not retroactive resolution of those errors.

**Interpretation and limits:** This validates a bounded inference recovery against documented report/criteria for the surviving models. It does not recreate any of 90,000 historical optimizer steps, restore full optimizer/RNG states, recreate absent raw training arrays/traces, reproduce the full original archive or eliminate unresolved original code/verifier gaps. No full main optimizer/RNG checkpoint and no raw main numerical training traces were available; a separate uploaded Q009 ZIP appears truncated, while needed inherited checkpoints were already verified in the usable Q009 parent. No downloaded data/model or cross-device/Windows test was used. The logged host was CPU Linux/Python 3.13.5/Torch 2.10.0+cpu, NumPy 2.3.5. The report calls this inference/evaluation recovery complete but expressly declines full original training requalification.

**Source locators:** `Research/Q010_InferenceRecovery_v1.6_RecoveryContext.zip::Q010_InferenceRecovery_v1.6/REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E00__Q010_InferenceRecovery_v1.6__REPORT.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/Q010_v1.6_20260924/` (retained evidence/review); `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/recovery_audit.md`.


<a id="question-5"></a>

## 5. Can a learned task workspace maintain progress and transfer?


<a id="pass-ts01"></a>

### TS01 — Learned task-progress state

**Broader question category:** Can a small recurrent system retain task progress across a public event stream, corrections, resets and interleaved tasks, and how does carried state compare with replay and exact tracking? (G03 persistent temporal state; G04 internal processing depth; G02 narrow baseline competence; adjacent G17 interface correctness.)

**Specific question:** In a tiny synthetic checklist task, can learned GRU state update two independent four-flag task banks from public events and answer milestone/action queries at event checkpoints; do state erasure and prefix replay change performance or computation?

**Type and status:** Completed supervised five-fit finite-state feasibility screen. It passed the predeclared bounded feasibility criterion. The complete primary TS01 execution ZIP is absent from this workspace and the logged scoped discovery; the retained consolidation E03 report and archive catalog carry the headline result. The text here transcribes those reports, not a fresh reproduction. It is not a test of the maintained management-token workspace.

**Systems and arms:** The learned transition is one shared float32 GRUCell(9,64) followed by Linear(64,9), 14,985 trainable parameters/59,940 weight bytes. Its two task state banks are each 64 floats (512 bytes total). Software maps task IDs to banks, routes updates, preserves unaddressed banks, filters labeled distractors/no-ops and handles queries. The learned part updates checklist bits and next action; it does not learn the task routing or archive management. CARRY maintains learned state; ZERO_EVERY_EVENT clears both banks before every event; PREFIX_REPLAY reconstructs state from the observed prefix before each query. EXACT_STREAM is an ordinary packed progress tracker, not learned. An initialized untrained fixture checks interface/numerical plumbing and is not treated as a scientific competence result.

**Method and data:** Five separate fits each made 2,000 Adam updates, batch 16, full BPTT over 17/33-event episodes. Training total: 10,000 optimizer/backward updates, 160,000 episodes, 4,000,000 events. Both banks’ four bit logits and next-action head were supervised after each event; gold state was not fed to the transition. Only terminal step-2000 checkpoints were admitted. Hashes were fixed before main data generation; no main dev tuning, model selection, additional fit, retries or criterion changes. Main evaluation used 32 sequences (three development/five held-out families, four templates each), 65 events after registration/activation prelude, and queries after 0,8,16,32,48,64. This yields 192 occasions, 120 held out across 20 sequences. Five fits share these streams, so 600 fit/occasion outcomes are not 600 independent tasks. Training/test templates are closely related; 65 events is a bounded length generalization test, not arbitrary-horizon evidence. The E03 report says 164 direct seed allocations and regenerates derived episode seeds, but the full execution archive is absent and the exact seed roster/initialization manifest is not in the retained report.

**Training result:** All five fits changed all 14,985 parameters. Their mean first-100 vs last-100 batch losses were fit 1: 1.992898→.063673; 2: 1.966765→.064830; 3: 2.037984→.065917; 4: 2.053146→.070999; 5: 2.022202→.065960. These are different batches under the fixed recipe, descriptive only. Each fit had 45 full model/Adam/RNG/cursor checkpoints at steps 0,250,…,2000. Independent retained-data regeneration reconstructed all 160,000 training episodes and 4,000,000 prefix targets but did not repeat optimization.

**Primary outcomes:**

| Held-out arm | Correct joint checklist + next action | Accuracy |
|---|---:|---:|
| CARRY | 600/600 (120 occasions × 5 fits) | 100% |
| ZERO_EVERY_EVENT | 200/600 | 33.33% |
| PREFIX_REPLAY | 600/600 | 100% |
| EXACT_STREAM | 120/120 unique occasions | 100% |

Every one of five fits was CARRY 120/120, ZERO 40/120, PREFIX_REPLAY 120/120. The screen required ≥114/120 in at least four fits; CARRY achieved 5/5 at 120. All five held-out family CARRY-vs-ZERO differences were positive: TS01EVAL-01 120/120 vs45/120 (+62.50 pp); -02 120 vs50 (+58.33); -03 120 vs45 (+62.50); -04 120 vs30 (+75); -05 120 vs30 (+75). Each family count repeats 24 query occasions across five fits. Exact tracker was 192/192 across the entire main set, once per occasion. State-off is an information ablation, not an equal-resource competitor; its lower score supports dependence on carried information, not neural superiority over code.

**Negative and computation outcomes:** At forced revocation checkpoints V:16/V:32/V:48, CARRY made 0 wrong-DONE assertions in 75 held-out assessments. An auxiliary diagnostic inspected 13,000 bank/event observations; reported counts for missed revocation, reset carryover, inconsistent head, wrong-DONE and stale inactive output were all zero. These are strongly correlated observations, not 13,000 independent tests. All 655 incorrect main query rows remain; 400 held-out and 255 development errors are ZERO. ZERO held-out next-action accuracy alone was 60%, bit accuracy 62.92%, joint only 33.33%; partial metrics do not replace joint correctness. The fixture retains 63 incorrect interface rows. The packed tracker needs eight progress bits plus task IDs/active metadata/archive/software overhead, while learned state alone is 512 bytes plus 59,940 weight bytes. CARRY used 1,612 actual GRU transition examples per model's 32-sequence main evaluation; replay used 4,303 (about 2.67× as many transitions) and matched endpoint states/logits exactly. This is a transition-count comparison under a specified six-query schedule, not a wall-clock speedup. All archive, auxiliary readouts, trace, process and operator costs remain; no overall efficiency pass or compression result was claimed.

**Resource reservations and measured execution:** Cell-example reservations were 4,099,712 against a 4,200,000 cap (4,077,168 actually dispatched); head-vector evaluations/reservations 8,089,216 against an 8,200,000 cap; backward and optimizer attempts/completions 10,000 each against 10,000 caps. Main clock through scoring/replay/comparison was 1,083.51 s. Sampled process-tree peak was 611,901,440 B and container peak 1,453,477,888 B; 0.1 s sampling cannot guarantee detection of brief peaks, and the initial preflight was not fully instrumented. Development/preparation is included on the shared clock. No target-device or wall-time advantage is claimed.

**Interpretation and limits:** TS01 demonstrates that this tiny supervised GRU can learn a narrow two-task checklist transition and use carried state on related held-out templates. Task IDs/bank routing, event filtering, archive management, labels and exact controls were supplied. It does not demonstrate a learned organizer, native HSA/MSA, open-ended instruction following, language capability, or broad benefit from depth. PREFIX_REPLAY is equal in accuracy at extra transitions; exact packed tracking is both perfect and extremely compact. No old Q010 model was loaded or updated.

**Source locators:** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E03__NSS_TS01_Execution_v0.3__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::ARCHIVE_CATALOG.json` (full execution archive unavailable); `RESEARCH_INDEX.md` (missing archive and retained report scope); `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md` (Q-series context only).


<a id="pass-ts02-mw01"></a>

### TS02-MW01 — Maintained workspace plus learned derived progress

**Broader question category:** Does a small maintained context representation usefully condition learned recurrent task state across source revisions, conflicts, resets and chronology, beyond recurrent-only capacity controls? (G03 persistent state; G06 binding/composition; G07 explicit metadata versus derived memory; G02 competence; related G17 interface correctness.)

**Specific question:** When two task records each have four milestones supported by left/right source revisions, does a native field-typed workspace improve joint milestone-plus-next-action performance over a 48-unit recurrent-only learner and a larger 60-unit recurrent-only control, while remaining reliable on revision provenance and completion claims?

**Type and status:** Completed new five-fit-per-configuration training study with independent scoring and fresh replay; the predeclared scientific screen FAILED. Full TS02 execution ZIP is not present in the reviewed inventory; E04's report is the retained result record. No historical Q010, CM02 or TS01 model was updated or loaded.

**Systems and arms:** R is a recurrent-only float32 GRU input/hidden size 42/48, 14,620 trainable parameters, 58,480 weight bytes, two banks totaling 384 recurrent bytes. R+ is a larger recurrent-only 42/60 GRU, 20,428 parameters, 81,712 weight bytes and 480 state bytes; it is a generous capacity control, not exact FLOP/parameter matching. RW is recurrent input/hidden 62/48, 17,572 parameters, 70,288 weight bytes, 384 recurrent state bytes plus ten uint8 token IDs. Its shared 18×4 embedding contributes 20 float32 input values. Five field-typed metadata slots/task (goal, left revision/status, right revision/status) persist and enter the addressed recurrent update. A deterministic writer copies observable metadata; it does not learn to write. Milestone/action heads read h only; the workspace contains no gold completion stamps/next action. Authority checks, protected task-bank routing and no-op filtering are supplied. Public RESET is learned through the GRU. Exact structured S and packed streaming X controls solve the progress task deterministically. RW diagnostics include CARRY, SLOT_MASK_EVERY_EVENT, ZERO_EVERY_EVENT and PREFIX_REPLAY. The no-training, three-model fixture is an interface check, not evidence of learned competence.

**Method and data:** Fifteen main fits (five each R/R+/RW) used 1,000 Adam updates, batch 8, with five paired stream sets shared across architectures; only terminal checkpoints were evaluated, hash-locked before concrete main stream generation. Forty thousand main training streams were presented across configurations 120,000 times; three separate 100-update cost probes used 800 additional streams. Full BPTT and both heads at every public message were charged; total 15,300 optimizer/backward updates and 4,425,600 event presentations including probes. Main development/held-out design: 32 chronological sequences, 3 development/5 held-out families ×4 templates, 65 events after 11-message prelude, queries at 0/8/16/32/48/64: 192 occasions, 120 held out. Each family spans handoff/goal, revision, conflict/withdrawal, reset/revocation. Five fits repeat the same streams; they are not new families. The task is a finite programmed recipe, not broad independent sampling. E04 does not preserve exact seed integers, full initializer/Adam hyperparameters or full raw stream/checkpoint bytes in the retained report, and the full archive is absent. Scores were reconstructed from public history by an independent NumPy scorer, with exact fresh replay; numerical tolerance `2e-6 + 2e-5*|reference|` is empirical, not a proven error bound.

**Primary held-out aggregate and fit outcomes:**

| CARRY configuration | Joint milestone + next correct | Accuracy |
|---|---:|---:|
| R | 507/600 | 84.50% |
| R+ | 496/600 | 82.67% |
| RW | 526/600 | 87.67% |

RW improved pooled score by 19/600 (+3.17 pp) over R and 30/600 (+5 pp) over R+. Descriptive only, not significance/generalization claims. Per-fit successes, preserving the weaker workspace fits:

| Fit | R | R+ | RW |
|---|---:|---:|---:|
| 1 | 107/120 | 103/120 | 96/120 |
| 2 | 93/120 | 94/120 | 113/120 |
| 3 | 102/120 | 92/120 | 112/120 |
| 4 | 104/120 | 104/120 | 108/120 |
| 5 | 101/120 | 103/120 | 97/120 |

Only 3/5 RW fits met the frozen ≥108/120 (90%) criterion; the rule required 4/5. RW also did not beat both controls every fit.

| Held-out family | R | R+ | RW | RW−R | RW−R+ |
|---|---:|---:|---:|---:|---:|
| MW01EVAL-01 | 99/120 | 98/120 | 103/120 | +4/120 | +5/120 |
| MW01EVAL-02 | 99/120 | 100/120 | 106/120 | +7/120 | +6/120 |
| MW01EVAL-03 | 108/120 | 103/120 | 109/120 | +1/120 | +6/120 |
| MW01EVAL-04 | 96/120 | 93/120 | 100/120 | +4/120 | +7/120 |
| MW01EVAL-05 | 105/120 | 102/120 | 108/120 | +3/120 | +6/120 |

RW beat R by at least five points in 1/5 families and R+ in 4/5; both family-level rules had to pass. Known-evidence repair subset (25 unique occasions ×5 fits): R 76/125 (60.8%), R+ 79/125 (63.2%), RW 79/125 (63.2%). RW did not beat R+ on this central subset. Milestone-only successes were R100/125, R+97/125, RW95/125; action correctness 87/125, 88/125, 96/125 respectively. All models answered the 50 held-out genuinely UNKNOWN-next queries correctly; on known answers RW 476/550, R 457/550, R+446/550.

**Safety and information-ablation results:** RW produced 75 stale/unsupported USE/revision claims in 1,200 held-out group predictions, versus a zero allowance, and 17 designated wrong-DONE assertions in 100 assessments, also versus zero. R and R+ had 10 and 20 designated wrong-DONE respectively; over all query positions total wrong-DONE counts were R32/R+50/RW25. All three configurations scored 0/25 joint successes at E:32. RW made 11 designated false-DONE claims there and six more at K:16; each configuration returned 25/25 correct primary task outputs at E:48 and E:64 even while provenance claims could still be wrong. Post-result audit found no training/probe prefix had both source revisions at valid revision 1, although the held-out E scenarios did; this is a plausible coverage association, not a preregistered causal explanation. The metadata packet itself was correct in the failing examples.

| RW held-out intervention | Joint correct | Meaning/limit |
|---|---:|---|
| CARRY | 526/600 (87.67%) | State and tokens present |
| SLOT_MASK_EVERY_EVENT | 366/600 (61.00%) | Same model; embeddings zeroed; information ablation |
| ZERO_EVERY_EVENT | 38/600 (6.33%) | Banks cleared, workspace remains |
| PREFIX_REPLAY | 526/600 (87.67%) | Same model; endpoint state/logits bit-identical |

Each R and R+ scored 0/600 under state removal. Exact structured S and packed X each returned 120/120 unique held-out answers including revision claims; X carries eight 3-bit stamps (24 sufficient progress bits) plus metadata/indexing. These deterministic controls outperform learned scores on the tested task; no efficiency/compression comparison passed.

**Resource, verification and failure ledger:** Each RW pass used 330 carried CARRY transitions versus 1,525 under the specified replay schedule; this is not 4.62× wall-clock speed. The 10-byte IDs omit recurrent state/weights, index tensor, embedding output, metadata maps/journal, object/runtime/operator costs. A held-out RW writer made 170 assignments of five-byte packets (850 payload bytes assigned) including 231 actual changed uint8 fields at 146 events; 425 counted indexed lookups returned 23,038 canonical logical bytes. Across sequential held-out episodes, event archives total 291,379 bytes but were not simultaneously resident. Cost tables are component-level Python inventories, not full native allocator traces. All 15,300 optimizer/backward updates completed; 75 main full checkpoints plus six probe start/end checkpoints retained; 4,108 incorrect main joint rows, 963 invalid group claims, union-negative 4,717 across main learned/control rows; fixture retained 238 incorrect joint rows and 239 invalid group claims. Fresh replay matched 17,120 arrays/10,019,920 elements for main and 428/250,498 for fixture; all 15 score files/split matched. Main independent arithmetic audit checked 5,717,120 scalars, max tolerance ratio .170498. A shared study clock of 1,315.48 s and sampled peaks 620,367,872 B process tree /1,606,270,976 B container were below limits, but brief peaks and initial shell inspection were not covered. All results are internal checks, not external replication.

**Interpretation:** This experiment shows the native field-token channel affects computation, and it gives a modest pooled increase over two recurrent controls. It fails its reliability, safety and required relative-benefit screen. Exact structured controls solved the task. It does not prove context workspaces cannot help; it rejects this particular recipe/representation/budget/split as sufficient and reliable. The architecture ledger and frozen tri-core Primary/Secondary/Tertiary/advisory Validator roles were not changed. It is distinct from proposed post-result coverage fixes and from the later TS03 experiment.

**Source locators:** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E04__NSS_TS02_MW01_Execution_v0.2__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::ARCHIVE_CATALOG.json`; `RESEARCH_INDEX.md` (full archive absent and evidence-scope notice); `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/2026-09-22/experiment_history.md`.


<a id="pass-ts03-cr01"></a>

### TS03-CR01 — Controlled revision-composition exposure

**Broader question category:** Does a controlled change in joint source-revision coverage improve a recurrent learner's evidence binding and derived progress, and does an explicit management workspace benefit more than recurrent-only controls? (G02 baseline competence; G03 temporal state; G06 compositional binding; G07 evidence provenance; related G17 interface.)

**Specific question:** Does adding joint (1,1) source-revision support while preserving per-source marginal histories improve a native workspace model (RW) on revision repair, relative to no such pairing and matched recurrent-only R / larger R+ controls, without harming reliability on held-out chronology and asymmetric combinations?

**Type and status:** Completed v0.4 execution under reviewed protocol v0.2, new 24-fit study, not a continuation or re-score of TS02. D1 coverage-effect, D2 workspace/coverage interaction, D3 absolute reliability, and the additional final-level advantage criterion all FAILED. Numerical engineering/replay passed; scientific screen remains negative. Full execution ZIP is absent; report and compact handoff/reporting materials remain.

**Systems and arms:** R recurrent-only (42 input/48 hidden; 14,620 parameters/384 bytes state); R+ larger recurrent-only (42/60; 20,428 parameters/480 bytes); RW native maintained workspace (62/48; 17,572 parameters/384 bytes plus ten uint8 IDs and 18×4 learned embedding). Five typed metadata slots/task are embedded into recurrent input; output heads read h only. Public authority checks, metadata writer, protected task routing and no-op filtering remain supplied software. No direct metadata-to-head bypass or output repair was added. Exact structured S and packed tracker X controls are deterministic. A shadow consistency filter is reported separately, never substituted for raw learned answers. C0 omits jointly valid revision pair (1,1); C1 re-pairs whole right-source histories in an eight-slot block to add (1,1), with compensating (0,0), preserving marginal revisions/status/receipts/targets at every prefix. This is a controlled support redistribution, not only adding one tuple with all else fixed. Both curricula still omit (1,2)/(2,1) from training/probes/development/fixture; asymmetric held-out rows are reserved unseen combinations.

**Method and data:** Four paired fits per architecture/curriculum (24 main models), exactly 800 updates each; initial tensors and fresh optimizer states paired across C0/C1 within fit. Six discarded 50-update cost probes; total 19,500 optimizer updates. Only step 800 was evaluated, no checkpoint chosen by outcome. Sixteen held-out sequences across four stress categories, eight development sequences/40 occasions; 65 events after 11-message prelude; checkpoints 0,8,16,32,64. Each cell has 80 held-out occasions ×4 fits=320 readouts; primary repair subset P has three non-asymmetric families at events16,32,64: 36 unique occasions ×4=144. Event histories expose milestone progress, revisions, conflict/withdrawal/reset and next action. Joint J requires four milestone categories and next action; B requires both raw evidence-binding categories correct. The held-out semantic task is finite and related, not IID broad sampling. Independent scorer/replay checked exact retained arrays, numerical tolerance and seeded streams; no optimization replication occurred.

**Full held-out joint and binding results:**

| Architecture | C0 joint | C1 joint | C1−C0 joint | C0 both bindings | C1 both bindings |
|---|---:|---:|---:|---:|---:|
| R | 124/320 (38.75%) | 139/320 (43.44%) | +4.69 pp | 152/320 (47.50%) | 194/320 (60.62%) |
| R+ | 95/320 (29.69%) | 119/320 (37.19%) | +7.50 pp | 137/320 (42.81%) | 193/320 (60.31%) |
| RW | 144/320 (45.00%) | 139/320 (43.44%) | −1.56 pp | 236/320 (73.75%) | 224/320 (70.00%) |

These are 80 occasions ×4 fits, not 320 independent tasks. C1 helped recurrent-only controls but did not improve RW.

**Predeclared primary repair and gates:**

| Architecture | Joint P, C0 → C1 | Change | Both bindings, C0 → C1 | Change |
|---|---:|---:|---:|---:|
| R | 37/144 →49/144 | +8.33 pp | 82/144 →128/144 | +31.94 pp |
| R+ | 20/144 →35/144 | +10.42 pp | 53/144 →113/144 | +41.67 pp |
| RW | 58/144 →51/144 | −4.86 pp | 144/144 →144/144 | 0.00 pp |

D1 failed: RW lost 7 joint successes; binding was already at ceiling and did not increase. D2 failed: relative C1 response for RW vs R was −19 joint and −46 binding successes; vs R+ it was −22 and −60 on the shared denominator. D3 failed: C1-RW fits had 34/80,36/80,34/80,35/80; zero of four met ≥72/80. These C1-RW outputs contained 96 invalid raw USE-revision claims/640 group predictions, six designated wrong-DONE assertions/128 assessments, and 102 binding errors when unresolved outputs are counted. Final-level advantage also failed: C1-RW had only two more P joint successes than C1-R (51 vs49/144), below a required eight; it did outperform R+ but both controls were required; pooled C1 RW tied R at 139/320.

**Failures, controls, and whole-run negatives:** On primary P, C1-RW binding was correct 144/144, yet joint output was only 51/144; milestone correctness declined 75→67/144 and next action 91→86/144. At initial checkpoint C1-RW was 64/64, but at event64 0/64 joint despite 48/64 binding pairs correct. On reserved asymmetric repair positions it had 16/48 J, 0/48 both-bindings and 0/48 all-head success; across all asymmetric occasions 32/80 J and 19/80 B. A post-result non-neural audit found every primary repair metadata+gold state occurred somewhere in each fit's training prefixes (21–4,439 times); target-state occurrence does not prove transition/order coverage. Both exact S and X controls scored 80/80 held out and 120/120 all-main occasions, once per unique occasion. For C1-RW, CARRY and PREFIX_REPLAY were 139/320; slot mask 105/320; zero-every-event 0/320. C0-RW CARRY 144/320, slot-mask 101/320, state removal 0/320. A shadow filter accepted 179/320 C1-RW rows (121 correct joint, 58 still wrong), blocked invalid USE but let ten wrong-DONE outputs through, and rejected 16 otherwise-correct known answers. It is not a learned repair and cannot replace raw performance. The completed main set retained 7,155 wrong joint rows, 3,064 invalid USE claims and 7,543 union-negative rows across 9,600 learned-interface rows; the untrained fixture retained 200 wrong joint/all-head rows and 302 invalid USE claims.

**Training history, verification and costs:** Twenty-four main models plus six probes; 132 full model/Adam/runtime-RNG/cursor checkpoints at 0/200/400/600/800 for each main and 0/50 for each probe. All completed first schedules. v0.3 stopped after fixture/replay and before optimization because a codec tried to share lookup costs across identity-dependent histories; the failed in-memory probe batch was not captured. Its deterministic reconstruction is explicitly post-stop, not original captured evidence. v0.4 separated the lookup cost lane; no fit was retried and extra cell/head attempts were charged. Total 19,500 backward/optimizer updates. Fresh main replay matched 20,544 arrays/12,916,064 elements; fixture 428/270,046; all 18 score files/split matched. Independent NumPy score covered 7,459,584 scalars, max tolerance ratio .143784. Reserved/completed potential cell examples 6,064,000 (cap 6,500,000); actual dispatch 4,080,964; head vectors 11,708,000 (cap 12,500,000); backward/optimizer 19,500 (caps 19,500). Whole study clock 1,875.12 s, sampled process-tree RSS 620,281,856 B, container 1,723,162,624 B below declared limits; brief peaks not guaranteed. Full cost and raw paired/family/seed rows are report-linked. This is not a deployment-speed or efficiency screen.

**Interpretation:** The report rejects this coverage repair for RW under this architecture, optimizer, budget and stress set; it does not prove workspaces can never help or coverage is irrelevant. Correctly bound current metadata was not enough for correctly derived progress; learned state/head remain confounded. Exact controls solved this toy task. TS03 is a new recipe/curriculum, not evidence that TS02 weights merely decayed or that simply training longer is a fix. No architecture or global role changes were made and NBR-02 was not launched.

**Source locators:** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E05__NSS_TS03_CR01_Execution_v0.4__REPORT.md`; `Research/NSS_TS03_CR01_Codex_Handoff_v0.4.zip` (compact report/headline tables; full archive absent); `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/TS03_CR01_v0.4_20260924/`; `RESEARCH_INDEX.md` (archival coverage statement).


<a id="pass-cka01"></a>

### CKA01 — Retrospective checkpoint learning/generalization audit

**Broader question category:** Were TS01/TS03 outcomes caused chiefly by training too long, or were learners already competent on familiar examples and only failing transfer? (G02 baseline competence; G03 persistent task state; G06 compositional generalization.)

**Specific question:** How do saved TS01 and TS03 checkpoints change on identical early-training, fresh same-recipe, and original evaluation panels, and do TS03's late stress losses follow earlier high competence or persistent underfitting?

**Type and status:** Completed exploratory post-result scoring audit; 0 new fit, optimizer update or backward call. The full CKA01 archive is absent; E06 report and review analysis are retained. Historical held-out panels are now known retrospective stress tests, not new confirmatory data. Q010 and TS02 were not evaluated.

**Systems, cohort, and method:** TS01 comprises five original fits × checkpoints 0,250,…,2000 (45 snapshots); TS03 comprises C0/C1 × R/R+/RW × four fits × 0/200/400/600/800 (120 snapshots); total 165 across 29 fits. Each checkpoint evaluates the same 64 actual early-training episodes, 64 freshly seeded recipe episodes and all original main sequences. These tiny panels are not accuracy estimates over all training episodes. Model/state architecture, routing, deterministic workspace integration and public-event semantics are unchanged; only CARRY is evaluated. Original dev and held-out partitions remain separate, but held-out is retrospective. New recipe panel draws were not outcome-selected; TS03 has semantic overlaps across curricula and is not threefold evidence. Full-prefix inputs are independently scored with NumPy; saved checkpoint tensors are hash-verified data-only snapshots, no optimizer/RNG restoration.

**TS01 checkpoint outcomes:**

| Stored update | Original held-out joint | New same-recipe endpoint |
|---:|---:|---:|
| 250 | 363/600 (60.50%) | 195/320 |
| 500 | 549/600 (91.50%) | 287/320 |
| 750 | 598/600 (99.67%) | 311/320 |
| 1000 | 600/600 (100%) | 319/320 |
| 1250 | 600/600 (100%) | 320/320 |
| 1500 | 600/600 (100%) | 320/320 |
| 1750 | 600/600 (100%) | 320/320 |
| 2000 | 600/600 (100%) | 320/320 |

The 600 original denominator repeats 120 occasions over five fits; 320 new endpoints are 64 per fit. All five fits first reached original 120/120 together at step1000; new recipe endpoints uniformly correct from step1250. Fixed-recipe loss declined .138454 at step1000 to .056169 at step2000. This supports saturation of this narrow benchmark without observed late deterioration on these panels; it is not arbitrary-horizon/general competence.

**TS03 checkpoint outcomes:** C1 workspace model on original chronological stress queries rose 83/320 (25.94%) at step200 to 132/320 (41.25%) at 400, 143/320 (44.69%) at 600, then 139/320 (43.44%) at 800. The step600→800 fall is 4/320=1.25 points; two fits were unchanged, one lost one answer, one lost three. No individual TS03 fit exceeded 39/80 (48.75%) on original held-out stress at any checkpoint. Other 600→800 changes were heterogeneous: C0-R +2.19 pp, C1-R +6.88, C0-RW +0.94, C1-RW −1.25, C0-R+ −3.75, C1-R+ −1.56. This is not a broad worsening pattern nor evidence of an earlier competent model hidden in the checkpoints.

At step800 C1-RW correctly answered the final active-task query on 51/256 actual early-training episodes (19.92%) and 65/256 newly seeded same-recipe examples (25.39%). Matching all-event/both-bank diagnostics for C1-RW improved at each checkpoint:

| Update | Actual training panel joint per bank/event | Fresh recipe panel | Mean original objective, training | Mean original objective, fresh |
|---:|---:|---:|---:|---:|
| 200 | 44.15% | 43.77% | .748093 | .754839 |
| 400 | 54.54% | 55.89% | .539293 | .531800 |
| 600 | 59.89% | 61.00% | .460610 | .444445 |
| 800 | 63.86% | 67.25% | .409811 | .388344 |

These event/bank rows are correlated. Endpoint practice percentages and chronological stress percentages have different panels/horizons and are not difficulty rankings. Of 256 fresh C1 curriculum streams, 88 overlap semantically with retained training; among 168 nonoverlapping episodes C1-RW achieved 36/168=21.43% at endpoints. Nonoverlapping 44-event subset rose 3/128→28/128 from step200→800. This still does not prove broad distributional independence or identify one cause.

**Audit work, negatives, resources and interpretation:** Across both capture and exact fresh replay the audit reports 1,255,758 GRU transition attempts and 4,037,760 bank-head vectors, zero optimizer/backward calls. NumPy reconstruction checked 1,720 inputs/56,768 prefixes through independent oracles, 13,181,760 categorical output coordinates and 12,445,440 state/logit/loss scalars. Fresh replay matched 990 arrays/25,678,410 elements; archived terminal TS01/TS03 inference also reproduced bitwise on both passes. All 44,160 query rows, including 27,570 all-head-negative rows, remain. It did not retain all intermediate hidden states/all nonquery logits. Two scorer implementation/tool attempts failed (unsigned no-op slot represented as 255 instead of −1; non-scientific plotting permission/interactive-shell issues); a separate signed-conversion scorer v0.2 passed regression without changing model/inference sources or rerunning training. Retained source reports preserve those failures. Conclusion: TS01 appears saturated on its narrow benchmark, not “ruined by overtraining”; TS03 has some late stress declines but no earlier competent checkpoint and also struggles on sampled familiar material. Incomplete fit and transfer are live explanations; the audit neither proves that more updates fix TS03 nor changes historical screens. A next experiment was only proposed, not launched.

**Source locators:** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E06__NSS_Checkpoint_Generalization_Audit_v0.2__REPORT.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/CKA01_v0.2_20260924/`; `RESEARCH_INDEX.md` (full archive missing); source-linked E06 tables/analysis for individual checkpoint and overlap traces.


<a id="question-6"></a>

## 6. Can delayed feedback teach new behavior without losing old behavior?


<a id="pass-e07"></a>

### E07 — DC01 v0.4 preflight: delivery-size admission stop

**Broad question.** The inherited DC01 line concerns whether a recurrent learner can use a later, explicitly identified feedback receipt to update the cue-time prediction while retaining unrelated associations. This preflight did not test that learning question. It tested the engineering question of whether the frozen v0.3 study could produce a complete, losslessly deliverable evidence archive within its 64 MiB ZIP cap. It is relevant background to G08 (which activity gets credit) and G09 (new learning while retaining old associations), but leaves both unanswered.

**Exact question and type.** Could the declared derivative, failure-detector, integration, cost-probe and evidence-delivery prefix be completed and conservatively projected below the delivery cap before starting the eight main fits and held-out work? This is a preflight engineering/admission pass, not a learning result. Status: `STOPPED_AT_STORAGE_ADMISSION`.

**Systems and methods.** The intended comparison had G, the exact reverse-mode learner, and L, a local diagonal-sensitivity eligibility approximation that omits cross-neuron derivative terms; both use a small recurrent two-class model. In this pass, neither arm received a main scientific fit. The preflight ran frozen derivative witnesses, 12 clean fixture applications per pass (G/L × two diagnostic labels × three delays 0/8/32, with model reset), a 14-category detector catalogue, eight deliberately faulty sandbox applications per pass, and two cost-only fits of 50 updates each. The cost-probe models were discarded. A fresh process replayed the executed prefix.

The frozen delivery estimate used 8,353.36 bytes per measured cost-probe update, 4,424 forecast applications per complete pass, a twofold engineering allowance, and 18 MiB for non-update evidence and metadata. The protocol required feasible delivery before main fitting. It did not prescribe the specific twofold forecast as a scientific threshold. No main split, held-out labels, A0 competence gate, or held-out criteria were reached. The 120 updates per pass are cost/diagnostic prefix work, not A0 fits.

**Documented arm and gate results.**

| Prefix result | G (exact gradient) | L (local eligibility approximation) | Scope |
|---|---:|---:|---|
| Cost-probe raw predictions | 43/50 correct; 7 incorrect | 42/50 correct; 8 incorrect | One paired initialization and repeated old-cue teaching only; not competence/adaptation/retention evidence |
| Clean-fixture post-receipt scratch query | 12/12 correct | 12/12 correct | Small reset fixture, not held-out streams |
| Mean relative encoder-gradient difference from exact derivative at L's own prestate | — | 0.6468; maximum 0.8008 | Vector-norm difference, not prediction error |
| Injected wrong sign/double update detection | 8/8 faulty applications detected | 8/8 faulty applications detected | Faulty sandbox weights isolated; no scientific fit used them |

Both fresh executions measured 8,353.36 stored bytes per probe update and forecast **92,784,897 bytes (88.49 MiB)** against **67,108,864 bytes (64 MiB)**, exceeding the cap by 25,676,033 bytes. Without the factor of two, the projection would be 55,829,632.64 bytes (53.24 MiB), but this was not accepted as a safe bound. The actual full archive was never produced, so actual full-study size is unknown. A further review found the copied 209 MiB `fixed_full_raw_schema_bound` boolean was not an independently derived count of all serialized fields and therefore did not prove the schema bound.

The prefix did pass its bounded numerical and integration checks: 306,968 scalar comparisons per pass, maximum empirical tolerance ratio 0.04156 under `2e-6 + 2e-5*abs(reference)`; 88 arrays / 24,960 elements in the equal-delay checks; 240 update applications across original plus replay (200 cost, 24 clean fixture, 16 deliberately faulty), with 1,160 recurrent transitions, 280 head evaluations and 128 G backwards per pass. Zero of eight proposed main fit/arm combinations were trained. Eight intentionally wrong update applications per pass were detected. The report separately notes limits in live fault coverage and a deliberately undetectable authenticated wrong label.

**Negative or stopped outcome.** Both original and fresh-process prefix replay stopped at the same `STORAGE_PROJECTION_FAIL` boundary before main initialization/fitting. The stop was caused by the implementation's conservative delivery forecast, not a failed learning gate, exhausted RAM/disk, or incorrect update arithmetic. No learning conclusion follows. The source's post-stop XZ measurement reduced retained-prefix representation from 1,050,202 bytes of individually compressed frames to 542,940 bytes losslessly; this suggested an encoding repair but did not itself establish full-run fit.

**Interpretation and limits.** This pass establishes reproducible arithmetic at an engineering gate and retains useful derivatives, detector cases, probe predictions and costs. It does not establish whether delayed learning works or whether the complete study would actually exceed the cap. v0.5 later repaired delivery encoding without changing the learning design; that later success does not replace or erase this stopped record.

**Version gap.** The assigned scope also names a DC01 v0.2 record. In the inspected primary E07–E19 register, current research index, old NBR02 proposal/research-log handoff, and v0.5 compact handoff, I found no DC01 v0.2 execution report or arm-level outcome. The available dated records here are the proposal/review handoff, E07 v0.4 preflight and E08 v0.5 execution. I preserve the version distinction noted by the index but do not infer v0.2 methods or results from later runs.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E07__NSS_NBR02_DC01_Execution_v0.4__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R07__NSS_NBR02_DC01_Preflight_Stop_v0.4_Delivery.json`; `Research/NSS_Research_Log_NBR02_Handoff_v0.1.zip::NSS_Research_Log_NBR02_Handoff_v0.1/NBR02_DC01_REVIEW.md`; `Research/NSS_NBR02_DC01_Codex_Handoff_v0.5.zip::NSS_NBR02_DC01_Codex_Handoff_v0.5/RESEARCH_LOG.md`.


<a id="pass-e08"></a>

### E08 — DC01 v0.5: identified delayed feedback and bounded adaptation

**Broad questions.** G08 asks which prior activity deserves an update; DC01 deliberately restricts this to one pending receipt whose cue identity is known, so it tests retaining/applying assigned cue-time learning information rather than ambiguous multi-event credit assignment. G09 asks whether new competence can improve without destroying prior competence. The study also measures a bounded update-timing condition related to G10, but does not test serving-revision admission. Its result is a narrow synthetic learner reference, not general continual learning.

**Exact question and type.** After a cue makes a prediction, can one later, causally matched label receipt—without replaying the cue features—support adaptation after 0, 8, or 32 intervening filler events, while preserving unrelated old associations? Can the local diagonal-sensitivity rule stay within predeclared accuracy, loss and retention margins of exact reverse-mode differentiation on this task? Type: completed controlled synthetic recurrent-learning study with initial fitting, development admission, held-out streams, cost probes, detector checks and a historical adaptive replay. Status: bounded A0/D1/D2/D3 pass; first post-reversal correction misses retained; full resource superiority and generality not established.

**Systems and controls.** The new laboratory network has 674 float32 parameters: a 16-unit dense tanh recurrent cell and a two-class readout. `START`, `PRIME(scope)` and `CUE` form the prediction input. Both learning arms update all five parameter tensors with plain SGD (learning rate 1, global gradient norm cap 1).

- **G — exact-gradient learner:** retains the true reverse-mode computation graph upstream of the cue-time prediction until the matching receipt arrives.
- **L — local eligibility learner:** retains the specified diagonal-sensitivity trace and omits cross-neuron derivative terms. This is an explicit approximation, not an incorrectly implemented exact gradient.
- **N_G / N_L — frozen controls:** each arm's own initial fit, evaluated without updates.
- **X — causal last-observed-label table:** exact bookkeeping by cue/ID, with no neural probability model. It records a label once observed; it cannot predict an unannounced reversal or a new label before receipt and is not an oracle.

One identified receipt can be pending. Cue-time parameters and learning information are held fixed while 0/8/32 detached fillers are processed; the receipt contains the target but omits cue features. Temporary recurrent state resets after each receipt, while parameters persist within that condition. Every condition restarts from its own initial-fit checkpoint. Therefore post-receipt scratch queries measure parameter learning rather than a cached answer in the live recurrent state.

**Data, splits, seeds and budgets.** Eight old associations were learned initially. Four distinct focal associations supplied development; eight different focal associations supplied held-out streams. Four paired G/L fits were retained and none was selected away. The held-out design crossed each of eight bases with stable versus reversal policy and three delays (0/8/32), giving 48 streams, five primary queries after receipts at trials 2, 3, 4, 5 and 6, and 240 primary occasions across delays per fit. The transaction schedule was `f,p,f,f,p,f`; reversal changed `f` at the third receipt. A separate raw pre-receipt score was retained. The delay-zero summary is 80 occasions × four fits = 320 readouts per arm; those repeated observations are not 320 independent association tasks. Four paired fits and the eight bases are the relevant bounded replication units; the report cautions that named base families are bookkeeping pairs, not IID populations. Exact seed values are not in the report's narrative tables; the compact handoff and source report preserve four fit indices and seeded transaction recipes/draws rather than a seed-value summary table.

The full protocol allowed 9,800 update applications cumulatively, counting v0.4 work; 9,088 were committed across original prefix plus v0.5, leaving 712 unused. There were no scientific retry fits or post-result extra training. New v0.5 work used 4,424 committed applications, including cost/diagnostic/probe/sandbox work. The two-hour active-work ceiling included 864.208668 seconds of prior recorded active work, not the inactive conversation gap. Delivery admission forecast was 62,694,619 bytes under the unchanged 67,108,864-byte ZIP cap, using the repaired lossless envelope encoding; the separate encoded-capture forecast was 231,282,164 bytes under a 256 MiB cap, explicitly empirical rather than a formal worst-case proof.

**Predeclared gate outcomes.**

| Gate | Criterion in the retained protocol | Result |
|---|---|---|
| A0 initial/immediate-feedback competence | All 8 initial old cues correct and minimum 16/20 primary correct plus ≥4 over each fit's own frozen control; at least 3/4 fits per learner | PASS, G 4/4, L 4/4. G: 38,36,37,38/40 vs 28/40; L: 39,36,38,38/40 vs 28/40 |
| D1 numerical/update/delay/replay fidelity | Frozen formula/update checks, delay-invariance array audit and historical adaptive replay | PASS; 64,600 array comparisons / 11,050,368 elements for delay invariance; historical adaptive replay matched 42,402 frames, 117,866 arrays and 29,728,572 numerical elements |
| D2-G focal adaptation and old-association retention | Improvement over own frozen control and old-association accuracy under fixed per-base rules | PASS, both criteria on 8/8 bases |
| D2-L focal adaptation and old-association retention | Same criteria for L | PASS, both criteria on 8/8 bases |
| D3 local-rule noninferiority screen | L within declared per-base accuracy and loss margins of G; old accuracy retained | PASS, accuracy and loss margins on 8/8 bases; pooled L−G accuracy −0.3125 percentage points, loss −0.011598 nats, old accuracy difference 0 |
| Whole-system learning efficiency or superiority | Complete comparable native memory/time accounting and an actual named advantage | NOT ESTABLISHED; explicitly not a blanket pass |

The fixed exploratory D2 focal-loss reduction over each arm's own frozen control ranged 0.546–0.846 nats for G and 0.603–0.924 for L. Old-inventory class loss was zero across bases, but post-learning old-inventory mean probability loss increased from about 0.00236 initially to 0.01618 (G) and 0.03879 (L). Thus class-label retention does not mean unchanged confidence. The v0.5 receipt also resolves delivery ticket RET-DC01-DELIVERY-001 for this bounded workload; it does not close NBR02.

**Held-out arm-level results at delay zero.**

| Arm | Post-receipt primary answers | Accuracy | Mean loss | Raw pre-receipt answers | Raw pre-receipt mean loss | Old inventory labels | Old mean probability loss |
|---|---:|---:|---:|---:|---:|---:|---:|
| G | 302/320 | 94.375% | 0.107930 | 308/384 | 0.714776 | 512/512 | 0.016176 |
| L | 301/320 | 94.063% | 0.096332 | 303/384 | 0.724657 | 512/512 | 0.038791 |
| N_G | 224/320 | 70.000% | 0.518088 | 262/384 | 0.568195 | 512/512 | 0.002361 |
| N_L | 224/320 | 70.000% | 0.535967 | 258/384 | 0.586192 | 512/512 | 0.002365 |
| X | 80/80 unique post-feedback occasions | 100% | Not a neural probability model | Learns nothing before observing receipt | — | — | — |

Across all three delays, trajectories were bit-identical by method: G 906/960, L 903/960, N_G 672/960, N_L 672/960. The tripled denominator does not add independent evidence. Adding the focal association, learned models returned 576/576 complete-inventory answers, while the frozen controls returned 544/576.

**Failures and negative outcomes.** Stable-policy primary probes were 160/160 for each learner. Under reversal, delay-zero accuracy changed as follows:

| Reversal checkpoint | G | L |
|---|---:|---:|
| Before the new label is released | 0/32 | 0/32 |
| After first corrective update | 14/32 | 13/32 |
| After next receipt with the changed label (trial 4) | 32/32 | 32/32 |
| Final focal probe after trial 6 | 32/32 | 32/32 |

The first pre-feedback errors were expected because reversal information was unavailable. The first update still left 18/32 G and 19/32 L wrong-class; those 37 errors all had matched receipts, intact pending record/parameter version, equation-correct gradients, correct clipping and SGD, and decreased loss without crossing the class boundary. Across invariant delays these yielded 111 retained held-out learned-primary failures. All 32 first-reversal gradients per method were clipped; raw norms were 5.20–6.99 for G and 5.87–7.61 for L, applied step norm capped at 1. That motivates, but does not prove, a correction-dose/clipping cause; starting margin, gradient direction, nonlinear response and shared parameters remain live alternatives. Larger correction's old-skill cost was not tested.

Before-feedback confidence was another negative: at delay zero G/L correctly answered 308/384 and 303/384 (80.21%, 78.91%) compared with 262/384 and 258/384 frozen, yet their mean losses were worse: 0.7148 and 0.7247 versus 0.5682 and 0.5862. At the surprise boundary, mean losses were 5.842 and 6.014 nats. Across L's 384 held-out delay-zero updates, its encoder-gradient relative difference from the exact derivative at L's own pre-update weights averaged 0.7668 (mean cosine 0.6468); this is not prediction error, and L still passed the small D3 screen. The full raw capture retained 24,196 scored query rows, 3,238 incorrect rows across all phases/methods and 111 held-out learned-primary failures; phases and denominators remain separated in the failure index.

**Interpretation and limits.** The evidence supports a specific identified delayed-feedback learner and three-delay invariance only under retained cue-time parameters/trace and this small task. It does not establish ambiguous credit assignment, multiple pending receipts, traces carried across weight changes, workspace writes, serving integration, temporal memory efficiency, or that the approximation generalizes to deeper causal tasks. “Delay had no performance effect” applies to the invariant constructed conditions after excluding live filler state and timing costs; it is not a general claim that arbitrary delay is harmless. The internal replay is not third-party replication. Cost subtotals omit NumPy backing/native graph memory; OBS-DC01-COST-001 remains open, and there is no overall memory/speed win.

**Version and source boundaries.** v0.4's stopped 240-application prefix remains separate and unchanged. The v0.5 execution archive is missing from the current workspace; the result is supported by the E08 source report, delivery receipt, compact Codex handoff with aggregate score tables and retained review evidence, not by a reopened full run archive. I located no standalone DC01 v0.2 execution report/results in the inspected register or compact handoffs (see E07 version-gap note).

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E08__NSS_NBR02_DC01_Execution_v0.5__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R08__NSS_NBR02_DC01_Complete_v0.5_Delivery.json`; `Research/NSS_NBR02_DC01_Codex_Handoff_v0.5.zip::NSS_NBR02_DC01_Codex_Handoff_v0.5/REPORT.md`; `.../scores/DECISIONS_AND_SUMMARY.json`; `.../scores/PRIMARY_BY_FIT.csv`; `.../scores/FIRST_REVERSAL_FAILURES.csv`; `.../scores/FAILURE_INDEX.csv`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/NBR02_DC01_v0.5_20260925/EVIDENCE_REVIEW.md`; `Research/NSS_NBR02_DC01_Codex_Handoff_v0.5.zip::NSS_NBR02_DC01_Codex_Handoff_v0.5/RESEARCH_LOG.md`.


<a id="pass-e09"></a>

### E09 — REV01 v0.4: a one-time larger correction step

**Broad questions.** G09 asks whether an update can gain a new association without harming old behavior; this line examines that trade-off after an explicitly observed label change. It is a narrowly identified feedback event, not ambiguous G08 credit assignment. The six-receipt timing is relevant to G10 but does not test serving-revision adoption.

**Exact question and type.** Does permitting one norm-2 instead of norm-1 update at the first public, scoped receipt whose label differs from the prior label make a reversed focal answer correct sooner, and does the added dose keep old class answers and confidence within limits? Completed held-out intervention study with a retained prefix-stop attempt; efficacy passed but the complete correction-with-retention screen failed for both learning rules.

**Systems, split and controls.** The inherited system is the 674-parameter float32 dense tanh recurrent learner with START/PRIME(scope)/CUE input and two output logits. G uses exact reverse-mode gradients; L uses the specified diagonal-sensitivity approximation, omitting cross-neuron derivatives. Four paired initialization seeds were used, each with 100 updates on eight old associations. Four development and eight held-out focal bases were fresh scoped mappings. Each base restarted from its fit's initial checkpoint and used `f,p,f,f,p,f`; reversal changed the focal label at its third receipt. The controller saw a lawful last-observed-label table, not an oracle reversal flag. Four development bases and eight held-out bases were crossed with four fits, so each first-correction denominator of 32 is eight bases × four fits, not 32 independent task families.

- **B1:** norm-1 correction throughout (reference).
- **B2:** norm-2 for the first changed-label correction only, then norm-1 (candidate intervention).
- **N_G / N_L:** each initial fit held frozen while it sees the same public record sequence.
- **X:** exact causal table containing only labels already observed; no unannounced reversal knowledge.

The intervention uses the same cue-time state/prestate in the paired branches; both computed gradients were compared before either branch was updated. A separate branched 0/8/32 detached-filler fixture checked bounded delay invariance; it is not a broader delayed-credit experiment. All eight old cues were queried after each application from reset scratch state.

The B1-only development gate required 8/8 old associations, at least 16/20 development answers, and at least four correct answers above that fit's frozen control; at least three of four fits per method had to qualify. G passed 3/4 and L 4/4; the subthreshold G fit remained in all data. B1-only development calibration set additional old mean-loss/probability-margin tolerances: G 0.0075619681 nats / 0.0147790546; L 0.01 / 0.02. These are exploratory fitted guardrails, not confidence intervals or established operational limits.

**Arm-level adaptation results.**

| Method / branch | First changed-label answer correct | Mean focal loss | First-correction efficacy |
|---|---:|---:|---|
| G / B1 norm 1 | 17/32 (53.125%) | 0.875471 | Reference |
| G / B2 one-time norm 2 | 32/32 (100%) | 0.037884 | PASS |
| L / B1 norm 1 | 16/32 (50%) | 0.809712 | Reference |
| L / B2 one-time norm 2 | 32/32 (100%) | 0.016806 | PASS |

G's per-fit net B2-minus-B1 gains were 5, 3, 2, 5; all eight held-out bases improved. L's were 5, 6, 2, 3; seven of eight bases improved and one tied. Neither had a B1-correct answer become wrong under B2. All B1/B2 focal answers were 32/32 after the next same-label receipt, so B2 reduced the first-correction lag without changing final class accuracy in this short schedule. Both methods were 0/32 on the reversed label before release, as expected.

**Retention and complete-screen outcomes.**

| Method / branch | Old class answers after correction 3 | After receipt 4 | After receipt 5 | Final receipt 6 |
|---|---:|---:|---:|---:|
| G / B1 | 256/256 | 256/256 | 256/256 | 256/256 |
| G / B2 | 256/256 | 256/256 | 256/256 | 256/256 |
| L / B1 | 256/256 | 255/256 | 255/256 | 255/256 |
| L / B2 | 251/256 | 251/256 | 251/256 | 251/256 |

Each old-answer count repeats eight cues × eight bases × four fits. G retained every class, but B2's immediate old mean loss was 0.017008 versus 0.004075 under B1: increase 0.012933 above its 0.007562 limit. Its mean margin decrease was 0.025260 above 0.014779; it failed 17/32 base/checkpoint confidence checks (pooled tail confidence later recovered). L's B2 immediately introduced five wrong old-label cases across two fits/four bases/three cue identities; those five cases persisted at four tail checkpoints, producing 20 repeated observations, not 20 memories. L's old mean loss rose from 0.004481 under B1 to 0.079193 under B2 (increase 0.074712 > 0.01); margin decrease 0.126025 > 0.02 and 30/32 confidence checks failed.

| Predeclared complete decision | G | L |
|---|---|---|
| First-correction efficacy | PASS | PASS |
| Old-label preservation | PASS | FAIL |
| Old-confidence preservation | FAIL | FAIL |
| Complete correction-with-retention screen | **FAIL** | **FAIL** |

The five L/B2 old failures were fit0/base8/cue7; fit0/base10/cue7; fit2/base9/cue2; fit2/base9/cue4; fit2/base11/cue4. No affected cue was the repeatedly protected cue for its condition. The causal bookkeeping control answered all after-receipt held-out queries correctly but could not predict before the receipt. Frozen errors, development rows, fixture/cost rows and replay are separate surfaces.

**Failures, numerical checks and resource history.** All natural G/L gradients and clipped SGD applications passed their own formula checks; L was compared to the exact derivative at L's own prestate, not a different G prestate. The primary capture retained 18,170 scored query rows and 1,431 incorrect rows, including frozen/diagnostic data; `reports/FAILURE_INDEX.csv` preserves categories. Fresh adaptive replay reproduced 24,720 frames, 71,400 arrays and 11,946,576 numerical elements. Each audit reconstructed 5,770,152 scalar comparisons; maximum tolerance ratio 0.070091 under the empirical `2e-6+2e-5*abs(reference)` envelope. The v0.3 predecessor did 168 updates, then stopped at a 70,206,051-byte estimate against 67,108,864 (64 MiB), before main fits; its stop is preserved. A storage-only v0.4 encoding change lowered the forecast to 63,991,104 bytes without changing learning settings, seeds, targets, or guardrails. The completed v0.4 pass and replay used 4,024 committed updates including the 168 stopped prefix, under the unchanged 4,500 cap; 119,184 cell examples, 38,528 heads, 2,024 backwards. There were no unknown-completion learner updates or fit retries. Sampled memory and whole-process costs do not establish an overall G/L efficiency advantage; OBS-DC01-COST-001 remains open.

**Interpretation and limits.** A causal paired intervention supports faster first correction under this specific model, rule, starting state and task. It does not show norm-2 is safe under noise, identify clipping as the unique cause of prior misses, or show that the local approximation alone caused L's greater retention harm; G/L fit checkpoints differ. No architecture, rehearsal or Tertiary was implemented. Full delivery and internal replay evidence are not third-party replication.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E09__NSS_NBR02_REV01_Execution_v0.4__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R09__NSS_NBR02_REV01_Complete_v0.4_Delivery.json`; `Research/NSS_NBR02_REV01_Complete_v0.4.zip::NSS_NBR02_REV01_Execution_v0.4/REPORT.md`; `.../reports/SUMMARY.json`; `.../protocol/ENGINEERING_AMENDMENT_v0.4.md`; `.../attempts/v0.3/protocol/PROPOSED_PROTOCOL_v0.2.md`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/NBR02_REV01_v0.4_20260925/`.


<a id="pass-e10"></a>

### E10 — PROTECT01 v0.3: projected updates trade correction for old confidence

**Broad question.** G09 asks whether new learning can improve without destroying older competence. PROTECT01 tests a specific first-order safety mechanism: whether constraining an update by old-output margins can preserve old behavior while still correcting a new cue. It is development evidence only; the held-out test was not generated.

**Exact question and type.** Compared with an ordinary larger correction and a same-applied-norm unprojected step, does projecting the first correction into the locally estimated old-margin-safe region reduce old-output regression without losing too much focal correction? This is a development experiment that stopped at its preregistered A0 admission gate. The implementation and numerical checks passed, but G failed relative-gain admission in two of four fits; no held-out mapping exists.

**Systems and arms.** Eight new 674-parameter float32 dense tanh fits used the inherited task, G's exact reverse-mode and L's diagonal-sensitivity gradients, four fit seeds per method, eight old binary associations, and four development focal bases. All fits received 100 old-association updates. Four development bases × four fits = 16 paired first-correction observations per method; these are repeated model/base outcomes, not independent tasks. No historical Q010/TS/previous NBR02 model was loaded.

- **B1:** ordinary clip-1 correction.
- **B2:** ordinary clip-2 correction.
- **P:** clip-2 candidate displacement projected against the eight exact old-margin gradients using the frozen QP/support solver, then applied as the actual float32 step.
- **S:** clip-2's unprojected direction scaled to the actual applied norm of P (norm-matched control).

G P/S and L P/S are contrasted from matched parameters within each paired fit/branch. L+P is a hybrid only for the protection rows, which use exact reverse-mode old-margin derivatives; L's focal learner and ordinary branches still use the approximate local rule. The P/S comparison uses actual stored float32 displacements and independent pre-update margin-gradient recomputation.

**Admission criteria and gate.** Each fit had to answer all eight old cues correctly, reach at least 16/20 focal primary answers on B1, and gain at least four answers over its own frozen control. Each learning method needed at least three of four fits. The fixed relative-gain criterion is unattainable for G fit 1 at its realized 17/20 frozen baseline (maximum possible gain three); G fit 3 also misses by one. This is an admission-design/headroom issue in the observed fit, not permission to amend the gate or remove a fit. All eight fits passed 8/8 old initial answers and the absolute 16/20 floor.

| Method | Fit0 B1 /20 (frozen; gain) | Fit1 | Fit2 | Fit3 | A0 fits passing | Gate |
|---|---|---|---|---|---:|---|
| G | 17 (11; +6) pass | 18 (17; +1) fail | 19 (14; +5) pass | 17 (14; +3) fail | 2/4 | **FAIL** (3/4 required) |
| L | 18 (14; +4) pass | 18 (14; +4) pass | 19 (14; +5) pass | 18 (14; +4) pass | 4/4 | PASS |

Both method arms ran all development branches before the admission decision. The screen is not a held-out validation result. Development-calibrated loss/margin limits were fixed from B1; the exact values and fit data are retained in the report. Since the cohort gate failed, those limits were never tested against confirmation data.

**All development branch outcomes.**

| Method / branch | First-correction answers correct /16 | Mean focal loss | Old classes in four repeated tails |
|---|---:|---:|---:|
| G / B1 | 7/16 | not separately tabulated in the report | 512/512 |
| G / B2 | 16/16 | — | 512/512 |
| G / P | 13/16 | — | 512/512 |
| G / S | 15/16 | — | G: all old classes retained in sample |
| L / B1 | 9/16 | 0.7857 reported by comparison | 512/512 |
| L / B2 | 16/16 | — | 512/512 |
| L / P | 10/16 | 0.8540 | 512/512 |
| L / S | 16/16 | — | one old cue became wrong at trial 4 and stayed wrong through trials 5/6 |

P never regressed a B1 focal success in these development cells but lost three of B2's focal successes for G and six for L. P retained all old class labels; S retained all G labels and lost one L model/base/cue. In P's old-confidence comparison with S at their same applied norms, mean final-tail old losses were G 0.0018223 (P) vs 0.0444573 (S), and L 0.0097994 vs 0.0645918. P thus had much better old confidence but lower focal answer counts; L's mean first-correction focal loss was 0.8540 for P versus 0.7857 for B1. This is a development trade-off, not a combined win.

**First-order safety was not finite-step immunity.** All captured QP certificates and first-order constraints passed. Nevertheless, actual old logit margins declined by more than 1e-6 in 28/128 G and 59/128 L first-correction old readouts under P; none of these became an old class error. The largest falls were about 0.20540 (G) and 0.83066 (L) margin units. Captured-gradient predictions of actual P displacements had small minimum residuals (about −2.01e−7 G, −2.62e−7 L), within the declared rounding envelope; larger actual drops are retained as nonlinear finite-step effects. The held-out mapping stage and its proposed old-confidence qualification were never opened.

**Negative outcomes, work and limits.** G's 2/4 A0 is the hard stop. A historical adaptive replay reproduced the completed prefix and the source report retains all development observations; there are no held-out labels/results to report. The report records 3,400 update attempts/commits including replay, 86,472 recurrent cells, 26,584 heads, 3,260 reverse calls, 1,552 old-margin backwards, 1,708 local focal derivatives, 224 QP calls, 56,832 support candidates and 56,834 SVD calls against their caps. Primary capture retained 12,372 primary neural query rows and 1,796 incorrect rows across all marked technical/frozen/development surfaces. Every actual update has a durable commit; intentionally wrong updates were isolated and detected. The independent audit checked 4,305,048 scalar comparisons, max tolerance ratio 0.119214 under the empirical `2e-6+2e-5*abs(reference)` rule. Internal replay is not third-party replication.

**Interpretation and limits.** Projection improves old confidence relative to an equal-norm direction in this small development sample while sacrificing some focal corrections. It does not pass its own cohort gate, test held-out mappings, protect unbuffered abilities, prove finite-step monotonicity, isolate G-versus-L approximation causality, or qualify an architecture. Keep the failed A0 unchanged.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E10__NSS_NBR02_PROTECT01_Execution_v0.3__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R10__NSS_NBR02_PROTECT01_Development_Stop_v0.3_Delivery.json`; `Research/NSS_NBR02_PROTECT01_Development_Stop_v0.3.zip::NSS_NBR02_PROTECT01_Execution_v0.3/REPORT.md`; `.../protocol/PROTOCOL.md`; `.../analysis/EXPLORATORY_SUMMARY.json`; `.../raw/primary/SOLVER_FIXTURE_RESULTS.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/NBR02_PROTECT01_v0.3_20260925/`.


<a id="pass-e11"></a>

### E11 — REHEARSE01 v0.2: strong correction followed by rehearsal (development stop)

**Broad questions.** G09 asks whether new competence can improve while retaining older behavior. G14 asks whether additional replay/training work improves later performance beyond immediate data. REHEARSE01 is a bounded rehearsal comparison with a full old-record buffer; it is not an idle reflection system or learned Tertiary.

**Exact question and type.** After a lawfully observed focal-label reversal, does a strong update followed by rehearsal on the new example or on old examples improve old behavior while retaining the new answer? Type: executed development screen with a prospective A0 stop. Its exposed development branches are candidates for a later design, not held-out qualification. Status: `STOPPED_AT_A0`; no held-out label maps/conditions generated.

**Systems, data and arms.** Eight fresh 674-parameter float32 dense tanh fits used the earlier 16-unit model. G computes reverse-mode gradients; L uses the diagonal-sensitivity approximation for both new and rehearsal examples. Both use SGD learning rate 1 and normally clip norm 1; the first publicly identified changed-label correction in U/F/R clips at 2. Four fits per method each learned eight old associations with 100 updates. Four development focal bases were crossed with four fits; there are 16 repeated model/base outcomes per method, not 16 independent families. Each short context forks from its method/fit's initial checkpoint after the shared public receipt prefix; there is no lifetime aggregation, dream process, plasticity-restoration test or architecture-scale integration.

- **B1:** clip-1 changed-label update; no added batch.
- **U:** clip-2 correction; no additional batch.
- **F:** clip-2 correction, then one extra clip-1 mean-gradient batch made from eight copies of the current focal example (repetition advances work but supplies no new observation).
- **R:** clip-2 correction, then one clip-1 mean-gradient batch on the eight lawfully observed old records in the supplied complete buffer.

All later public receipts use clip 1. F/R recompute eight per-example gradients at one shared post-clip-2 prestate, serially accumulate in float64, cast once to float32, clip once and apply once. Rehearsal has its own operation ID and is not counted as eight new observations. L's rehearsal remains local-rule computation, not an exact-gradient hybrid. The buffer, scoped receipt detector, routing, state resets and label authority are ordinary harness software.

**Admission rule and outcome.** Each fit required 8/8 old associations initially, at least 16/20 B1 development primary answers, and recovery of at least half its frozen control's net errors on fixed K (12 focal post-feedback opportunities across four bases at trials 3/4/6); each method needed 3/4 qualifying fits. Development-calibrated old-confidence limits were G loss 0.0091161877 / margin 0.0177325873; L loss 0.01 / 0.02. No held-out calibration was possible.

| Method / fit | Initial old /8 | B1 overall /20 (frozen /20) | B1 K /12 | Frozen K /12 | H (frozen errors) | Net gain / H | Fit admission |
|---|---:|---:|---:|---:|---:|---:|---|
| G0 | 8 | 18 (17) | 10 | 9 | 3 | 1/3 | FAIL |
| G1 | 8 | 16 (14) | 8 | 6 | 6 | 2/6 | FAIL |
| G2 | 8 | 18 (14) | 10 | 6 | 6 | 4/6 | PASS |
| G3 | 8 | 16 (8) | 8 | 0 | 12 | 8/12 | PASS |
| L0 | 8 | 19 (17) | 11 | 9 | 3 | 2/3 | PASS |
| L1 | 8 | 17 (11) | 9 | 3 | 9 | 6/9 | PASS |
| L2 | 8 | 17 (14) | 9 | 6 | 6 | 3/6 | PASS |
| L3 | 8 | 16 (8) | 8 | 0 | 12 | 8/12 | PASS |

G passed 2/4, below 3/4; L passed 4/4. All fits met the absolute floors, but G's normalized improvement gate failed. The report says this rule was attainable in every fit and must remain fixed. Both branches/methods completed their prescribed development work before the stop; no held-out mapping was generated.

**Exposed development outcomes.**

| Method / branch | First changed-label answer correct | Focal loss after extra batch (reported) | Old classes across four recovery checkpoints |
|---|---:|---:|---:|
| G / B1 | 4/16 | — | 512/512 |
| G / U | 16/16 | 0.068150 | 509/512 |
| G / F | 16/16 | 0.008651 | 507/512 |
| G / R | 16/16 | 0.087837 | 512/512 |
| L / B1 | 5/16 | — | 512/512 |
| L / U | 16/16 | 0.037131 | 512/512 |
| L / F | 16/16 | 0.007338 | 512/512 |
| L / R | 16/16 | 0.054975 | 512/512 |

Immediately after the strong correction, all 128 old model/base/cue answers per method still had correct classes. Mean old loss before extra work was 0.022229 G / 0.049394 L; after F it rose to 0.070237 / 0.072631; after R it fell to 0.013178 / 0.016503. R preserved all old class answers in these development traces; it did not repair any already-wrong old class because there were none before R. It also did not clear every confidence limit: the report's diagnostic envelope check found R outside it in 2/16 G and 5/16 L base/checkpoint cells; U exceeded it in 11/16 G and 13/16 L; F in 12/16 G and 14/16 L. These are descriptive, development-derived counts, not an official held-out gate.

The R batches were not clipped (mean raw norms 0.09616 G / 0.22222 L; cancellation ratios 0.74074 / 0.80738). Every recorded batch reduction and applied step was independently checked; the arithmetic isn't a demonstrated bottleneck. Fresh adaptive replay matched 19,428 frames / 61,150 arrays / 14,577,108 elements. The study retained 13,220 neural query/diagnostic rows and 2,046 incorrect rows, including expected diagnostic/frozen/control outcomes. It used 3,576 update attempts/commits across capture and replay, within the 7,000 cap. The full held-out portion (2,560 capture/replay applications) was not spent. No inference here upgrades the stop to a scientific failure or success.

**Interpretation and limits.** In this exposed development sample, old-record rehearsal improved old probability quality more than repeated focal practice while keeping new class answers correct; later focal learning can still reintroduce interference. This is an exposed recovery lead, not held-out confirmation, restoration of an already lost class, complete confidence recovery, or proof of plasticity restoration. The subsequent E12 analysis reuses these same rows; its retrospective calculations are separate from this stopped execution and do not waive A0.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E11__NSS_NBR02_REHEARSE01_Execution_v0.2__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R11__NSS_NBR02_REHEARSE01_Development_Stop_v0.2_Delivery.json`; `Research/NSS_NBR02_REHEARSE01_Development_Stop_v0.2.zip::NSS_NBR02_REHEARSE01_Execution_v0.2/REPORT.md`; `.../analysis/SUMMARY.json`; `.../protocol/PROTOCOL.md`.


<a id="pass-e12"></a>

### E12 — REHEARSE01 v0.1 analysis: the same rehearsal gain was temporary under continued focal updates

**Broad questions.** G09 (old/new interference) and G14 (rehearsal/replay) remain the motivating questions. This entry is a retrospective audit of REHEARSE01 E11's development evidence, not a second experiment or a new example of learning.

**Exact question and type.** Do the retained logits, batch gradients and update vectors show whether R improved old behavior consistently, whether subsequent ordinary focal training reversed that benefit, and whether the original A0 failure meant inability to acquire/recover at all? Type: data-only post-result analysis. Status: completed analysis; source study remains `STOPPED_AT_A0`, with held-out qualification `NOT_ASSESSED`.

**Evidence and methods.** The analysis used the retained REHEARSE01 v0.2 archive only: 8,160 development query/diagnostic rows, 64 replay batches, the fixed eight-fit admission records and retained arrays. An independent reader verified 164 manifest entries, 19,428 frames, 61,150 arrays / 14,577,108 elements, and matched all 13,220 source score rows to saved logits; maximum score difference was zero. It used saved values only, no model construction/forward, no new derivatives, no optimizer, and no new random stimulus. All 271 development-negative rows remained retained. Four bases × four fits yield 16 contexts per method; repeated checkpoints/cues and internal replay are not new tasks.

**A0 decomposition, not a changed gate.** Saved-history reconstruction shows both method baselines learned and later recovered the focal association on all four bases/fits after the second changed-label receipt; the failed requirement is sensitive to first-correction speed relative to a frozen control.

| B1 focal checkpoint | G | L |
|---|---:|---:|
| After first teaching receipt | 16/16 | 16/16 |
| After protected-old receipt | 16/16 | 16/16 |
| After first changed-label receipt (trial 3) | 4/16 | 5/16 |
| After second changed-label receipt (trial 4) | 16/16 | 16/16 |
| After later protected-old receipt | 16/16 | 16/16 |
| Final focal answer | 16/16 | 16/16 |

The audit defines n as the count of four frozen-model bases already aligned with the eventual new label and k as B1's first-correction successes. For these saved trajectories only, B1_K=8+k, N_K=3n, H=12−3n; when H>0 the old rule `2(B1_K−N_K)≥H` simplifies to `k≥1.5n−2`. This illustrates that normalized gain mixes speed with frozen-label alignment; it is not proposed as a replacement. Full retained per-fit outcomes:

| Method / fit | Frozen matches n/4 | B1 first corrections k/4 | B1 K/12 | Frozen K/12 | Gain/H | Original gate |
|---|---:|---:|---:|---:|---:|---|
| G0 | 3 | 2 | 10 | 9 | 1/3 | FAIL |
| G1 | 2 | 0 | 8 | 6 | 2/6 | FAIL |
| G2 | 2 | 2 | 10 | 6 | 4/6 | PASS |
| G3 | 0 | 0 | 8 | 0 | 8/12 | PASS |
| L0 | 3 | 3 | 11 | 9 | 2/3 | PASS |
| L1 | 1 | 1 | 9 | 3 | 6/9 | PASS |
| L2 | 2 | 1 | 9 | 6 | 3/6 | PASS |
| L3 | 0 | 0 | 8 | 0 | 8/12 | PASS |

This explains a possible gate-headroom concern without changing the registered result. It does not retrospectively admit G or use the exposed bases as future confirmation.

**Old rehearsal and next-update results.** Old-record R lowered mean old loss in every one of 16 G and 16 L contexts, while preserving all 32 focal class answers:

| Method | Before R | After R | Pooled mean reduction |
|---|---:|---:|---:|
| G | 0.022229 | 0.013178 | 40.72% |
| L | 0.049394 | 0.016503 | 66.59% |

These are reductions of pooled means, not mean individual percentage gains. At the final checkpoint R remains better on old mean loss than U and F in 15/16 contexts per method, but it is not uniformly dominant on every output. Focal loss rises from 0.068150 to 0.087837 G and 0.037131 to 0.054975 L after R, though all focal classes remain correct. R maintained 512/512 repeated old-class observations per method; no pre-R class error was present to repair.

The next ordinary focal-only receipt worsened old mean loss in all 16/16 contexts per method:

| R trajectory | After strong correction | After R | After next focal update | Final after protected-old receipt |
|---|---:|---:|---:|---:|
| G old mean loss | 0.022229 | 0.013178 | 0.050170 | 0.030882 |
| L old mean loss | 0.049394 | 0.016503 | 0.040991 | 0.031669 |

The later protected-old receipt targeted one cue, not the entire buffer. R exceeded its development-calibrated confidence envelope in 2/16 G and 5/16 L context/checkpoint cells. The audit preserves the earlier excursions, including G base2 at receipt4 mean old-loss increase 0.025150 over B1 against 0.009116 allowance and L increase 0.025470 against 0.010000. All R confidence cells later fell inside the envelope at the last two checkpoints; later recovery does not erase earlier violations.

**Label and gradient interpretation.** Four of eight old records share the focal label and four oppose it. During R, opposite-label old losses improved in 64/64 observations, while same-label losses worsened in 64/64, for each learner. The next focal update reversed this pattern exactly. G old mean loss for opposite-label records shifted 0.041745→0.023138 during R, while same-label shifted 0.002712→0.003217; L shifted 0.097356→0.030960 and 0.001431→0.002046. All saved focal/old gradient dot-product cosines were negative across 32 contexts (mean −0.452806 G, −0.564193 L), consistent with competition on this toy. The audit explicitly does not locate the effect to a unit/layer or prove a general stability-plasticity law. R's raw norms were all below clip 1, so raising clip to 2 would not change those saved R steps; this is arithmetic on stored operands, not a tested intervention.

F rehearsal advances computation that U would make on the next same focal receipt: in all 32 method/fit/base contexts, F's post-extra parameters were bit-identical to U's later parameters, with matching logits. This confirms it is repeated training work, not extra environmental evidence. All batch reductions/parameter bytes were reconstructed from archived gradients; no new gradient was calculated.

**Interpretation and limits.** The most defensible result is “one old rehearsal batch helps old probability quality in these development contexts; a later focal-only update reintroduces old-loss pressure.” The audit motivates a prospective test of placement or repair-vs-next-update, but none was run. It is not evidence that increasing clipping helps, that one can repair arbitrary forgetting, that old knowledge becomes stable, or that the original A0 or future-held-out gate passed. The report's two analysis-tooling corrections are retained; all source arrays/results were rebuilt, not mutated.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E12__NSS_NBR02_REHEARSE01_Analysis_v0.1__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R12__NSS_NBR02_REHEARSE01_Analysis_v0.1_Delivery.json`; `Research/NSS_NBR02_REHEARSE01_Development_Stop_v0.2.zip::NSS_NBR02_REHEARSE01_Execution_v0.2/REPORT.md`; `.../analysis/SUMMARY.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/NBR02_REHEARSE01_v0.2_20260925/`.


<a id="question-7"></a>

## 7. When do repair, replay and accumulated learning help?


<a id="pass-e13"></a>

### E13 — TIMING01 v0.1: early versus delayed old-record rehearsal

**Broad questions.** G09 (adaptation while retaining old behavior), G10 (when corrective/maintenance changes happen), and G14 (additional rehearsal) are touched. This is a specific placement experiment, not a live serving-revision test, a dream computation or an integrated Primary/Secondary/Tertiary schedule.

**Exact question and type.** With the same eight-record replay batch and correction access, should old-record rehearsal occur immediately after the strong first correction or after one more focal update? Do either schedules satisfy a full-path protection/recovery screen, rather than only improving the ending? Type: completed prospective protocol with held-out bases, adaptive learning/replay, and a complete full-trajectory screen. Status: engineering and baseline admission passed; Early and LATE failed the full-trajectory confidence rule for both G and L.

**Systems, arms, data.** Eight new 674-parameter float32 dense tanh fits (four paired G/L initializations) received 100 old-association updates. G uses the exact three-transition derivative; L uses the pinned diagonal-local approximation even for replay. Four development and eight held-out bases use `f,p,f,f,p,f`; each base restarts from its method/fit initial checkpoint. Eight real receipts include a public focal reversal at receipt 3. Four old associations are compact hard records; all eight remain available to audit. Replay gradients are recalculated at each branch's current parameters, averaged in the pinned ordered float64 sequence, cast once to float32, clipped once and applied. The same source records at a changed prestate need not produce the same vector/norm.

- **B1:** norm-1 first changed-label correction and norm-1 later updates, no rehearsal.
- **U:** norm-2 first changed-label correction, then norm-1, no rehearsal.
- **E (Early):** U plus one norm-1 mean-gradient batch over eight old records immediately after the first correction.
- **LATE:** U plus the identical eight-record batch after the next valid same-cue/scope/same-label focal receipt.
- **X:** exact last-observed-label table for lawful labels; it does not know unannounced feedback.

E and LATE each spend one batch/eight example gradients; B1/U are cheaper. No focal-repetition control is run in this timing-only study. All branches share a six-boundary scoring grid, including aligned reuse when a branch has not yet updated. The 32-context denominator is eight held-out bases × four fits per learner, not independent task families.

**Admission and fixed thresholds.** A qualifying fit needed 8/8 initial old classes, at least 16/20 mixed B1 answers, all four focal acquisitions after first teaching, all four reversal recoveries after the second corrective receipt, and all four final focal answers; at least three of four fits per method. All G/L fits passed (G mixed 16,16,17,17; L 17,16,17,17). Relative-to-frozen K/H results were still recorded but not an admission requirement in this new protocol; this was a prospective change, not a claim that earlier gates passed. Development-only B1 calibration set G old-loss/margin allowances 0.0063722558 / 0.0123968038; L 0.01 / 0.02. New held-out mappings were generated only after admission/calibration lock.

The full-trajectory gate required first-correction efficacy over B1, no lost U-correct focal answers, every pre-fork-correct old class retained, no additional B1 old error, and every base and pooled old-confidence limit met at every aligned boundary. The boundaries were T3 pre-extra, T3 after extra, T4 pre-extra, T4 after extra, T5 post-real and T6 post-real. This is a severe all-boundary contract; it deliberately does not excuse an early violation because a later update repairs it.

**Focal and old-class results.**

| Learner | B1 first correction | U | E after early rehearsal | LATE before delayed rehearsal |
|---|---:|---:|---:|---:|
| G | 11/32 | 32/32 | 32/32 | 32/32 |
| L | 12/32 | 32/32 | 32/32 | 32/32 |

All 32 denominators repeat four fitted models over eight bases. Every old class remained correct for all four branches at all six boundaries: 256 repeated old answers × six time points (1,536 observations per branch/method). Therefore this sample shows confidence-regression failures, not old-label class forgetting or repair of a previously wrong old class. X correctly answered 48 held-out after-receipt focal and 384 old queries, while its pre-feedback score was 32/48; it is bookkeeping, not a neural achievement or oracle.

**Old-answer confidence by timing and full gate.** Lower mean old-answer loss is better:

| Learner / branch | After strong correction | After early-batch point | After next focal update, before delayed batch | After late batch | Final |
|---|---:|---:|---:|---:|---:|
| G / E | 0.013224 | 0.010385 | 0.021778 | 0.021778 | 0.020179 |
| G / LATE | 0.013224 | 0.013224 | 0.025315 | 0.013347 | 0.013545 |
| L / E | 0.050585 | 0.015746 | 0.029835 | 0.029835 | 0.024700 |
| L / LATE | 0.050585 | 0.050585 | 0.062770 | 0.015181 | 0.020211 |

Both rehearsal steps improved mean old loss in all 32 contexts per learner and preserved focal class answers. LATE had lower final old mean loss in 8/8 G bases and 7/8 L bases (G pooled late−early −0.0066335, L −0.0044888), yet it was worse during the interval before it ran. No late-only result erases those earlier trajectories.

| Learner / branch | First-correction efficacy | Old classes at all boundaries | Old confidence at all boundaries | Failed base/boundary cells /48 | Complete screen |
|---|---|---|---|---:|---|
| G / E | PASS | PASS | FAIL | 21 | FAIL |
| G / LATE | PASS | PASS | FAIL | 20 | FAIL |
| L / E | PASS | PASS | FAIL | 17 | FAIL |
| L / LATE | PASS | PASS | FAIL | 24 | FAIL |

The no-rehearsal U reference exceeded confidence limits in 30/48 G and 41/48 L base/boundary cells. For G both schedules already failed pooled confidence immediately after norm-2 correction; for L, LATE reduced final loss but increased measured boundary violations from 17 to 24. Minimum old correct-label probabilities were G .71955 (E) / .69476 (LATE) and L .55110 / .64825. Output probabilities are not calibrated safety guarantees.

**Failure evidence, work and limits.** There were 29,540 scored neural query/diagnostic rows and 2,757 incorrect rows; held-out negative rows remain classified across learned/frozen/before-feedback surfaces. All 41 held-out post-feedback learned focal misses occurred on B1's first correction. That is separate from expected pre-feedback reversal surprises and confidence-only failures. A fixed numerical audit reconstructed 9,950,920 scalar comparisons with max tolerance ratio .1112471; historical adaptive replay matched 41,508 frames / 130,206 arrays / 29,022,292 elements and score/audit files. Across capture and replay: 6,136 durable update commits, 197,112 cells, 63,464 output heads, 4,700 G backwards / L gradient examples, 3,712 replay-record fetches. No unknown-completion natural updates or fit retries. Sampled process RSS/container and time are recorded, but not deployed speed; memory backing/native-graph accounting remains incomplete. Storage projections were empirical; after sealed logs closed, three logs were losslessly compressed with hashes verified, with final pre-alias evidence 247,912,993 bytes. No evidence was truncated or discarded.

The paper *Self-Play Pretraining with Zero Data* is only a referenced external lead for future curriculum generation, not training evidence or a treatment in TIMING01. No small-plus-large combined intervention, continuation mixture, confidence cap or dream system was run.

**Interpretation and limits.** Timing changes when old confidence degrades and is restored; it does not solve all-boundary reliability here. Rehearsal usually repairs the ending, while continued focal updates push against old probability quality. Equal data/application counts do not establish equal gradient magnitude, and the study resets each context from its initial fit instead of building a lifelong history. Neither schedule is promoted as an operational policy.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E13__NSS_NBR02_TIMING01_Execution_v0.1__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R13__NSS_NBR02_TIMING01_Complete_v0.1_Delivery.json`; `Research/NSS_NBR02_TIMING01_Complete_v0.1.zip::REPORT.md`; `.../analysis/SUMMARY.json`; `.../protocol/PROTOCOL.md`.


<a id="pass-e14"></a>

### E14 — TIMING01 v0.1 retrospective audit: later repair improves the ending but not the peak

**Broad questions.** G09/G10/G14 as in E13. This is a separate retrospective analysis of saved TIMING01 evidence; it cannot qualify the original full-trajectory result or serve as new held-out confirmation.

**Exact question and type.** Across retained held-out trajectories, does late repair improve final old-answer quality while leaving higher intermediate risk; which intervening update changes old quality; and can a nominal same-batch timing comparison be interpreted as equal dose? Type: post-result, data-only descriptive audit. No new model, forward, derivative, optimizer update, or target was generated. Source study remains complete with all four Early/LATE-by-G/L failures unchanged.

**Evidence boundary.** The analysis verified the 37,195,996-byte TIMING01 v0.1 ZIP identity/CRC, restored all 168 logical manifest entries, checked 41,508 frames / 130,206 arrays / 29,022,292 elements and the retained replay hash. It independently recalculated 29,540 query classes/losses/margins from logits (max numeric discrepancy 8.88e−16), reconstructed 24,480 main targets from already released receipts, verified 384 confidence decisions and rechecked 192 batch reductions/float32 parameter subtractions. These operations used captured values only. The main held-out analysis has eight bases × four fits = 32 contexts per method; development stays separate; old cues, stages and replay are repeated measures.

**Shared pre-rehearsal confidence failure.** Every base mean for both methods already failed at the common post-norm-2 correction state before E or LATE ran:

| Method | Pooled old-loss increase over B1 | Fixed allowance |
|---|---:|---:|
| G | 0.00953234 | 0.00637226 |
| L | 0.04667736 | 0.01000000 |

No subsequent operation can retroactively satisfy the original every-boundary pass. This is a temporal observation, not a claim that a changed first correction cannot pass a future test. Any future “recovery at stage end” contract must be prospectively distinguished from strict no-early-breach, and must retain the early readouts.

**Ending, peak and trajectory-weighted result.**

| Later versus Early across paired contexts | G | L |
|---|---:|---:|
| Lower final mean old loss | 30/32 contexts; 8/8 base means | 29/32; 7/8 base means |
| Lower peak mean old loss | 7/32; 1/8 base means | 1/32; 1/8 base means |
| Higher peak mean old loss | 25/32 | 31/32 |
| Lower six-boundary equally weighted mean old loss | 18/32 | 2/32 |
| Lower final focal-answer loss | 0/32 | 3/32 |

| Mean across contexts | G Early | G Later | L Early | L Later |
|---|---:|---:|---:|---:|
| Final mean old loss | 0.020179 | 0.013545 | 0.024700 | 0.020211 |
| Context peak mean old loss | 0.023244 | 0.025315 | 0.054971 | 0.062770 |
| Six-boundary mean old loss | 0.017601 | 0.015048 | 0.028703 | 0.035487 |
| Final focal loss | 0.007374 | 0.008821 | 0.006516 | 0.007534 |

The six-boundary mean is a schedule-weighted description, not elapsed-time area; boundaries are not equally spaced. Late rehearsal is better on most final old-loss comparisons but worse on almost every peak-loss comparison. It is not a universal timing win and no confidence interval treats 32 contexts as IID.

**Update-level and label-group results.** After clip 2, the next focal-only update increased mean old loss in all 32 contexts per method, before a late batch could run. The protected-old receipt at T5 improved old loss in exactly 16/32 contexts and worsened it in 16/32 per method/placement; it targets one old cue, not the whole buffer. At a rehearsal step, all 128 opposite-label old observations improved in loss while all 128 same-label observations worsened slightly, for each method/placement; the next focal update reversed those directions. No old class became wrong on the held-out grid. Therefore the reported failure is confidence envelope, not class forgetting.

Later replay at a changed parameter state is a larger realized update in all 32 paired contexts per method. Mean raw norms were G 0.05205 early vs 0.11535 late; L 0.24736 vs 0.30628. Median later/early actual-step ratios were 1.648 G and 1.246 L; all 128 batches were below clip 1, so merely increasing that ceiling would not change them. Identical records do not isolate timing from gradient-size changes. For G, mean local predicted old-loss changes (−0.003417 early; −0.021857 late) were more favorable than actual changes (−0.002840; −0.011968); saved gradients cannot be added to infer an unexecuted small-plus-large schedule.

**Moving reference and analysis limits.** The relative guard compares each branch with B1 at the same boundary. As B1 changes, a branch can pass relative limits while its absolute old loss rises. For E, G absolute loss moves 0.010385→0.021778 while E-minus-B1 falls 0.006693→0.004614 under 0.006372 allowance; L absolute loss moves 0.015746→0.029835 while the difference moves 0.011838→−0.011153 under 0.01 allowance. This is correct application of the original rule, not a correction of the failed screen. The report asks future protocols to define both comparison surfaces rather than choose retrospectively.

The proposed small repeated maintenance plus larger later consolidation is coherent as a new controlled question, but no such branch ran. Its result cannot be inferred by combining E and LATE; an early operation changes the later gradient prestate. CANDIDATES contains proposal-only branches. The retrospective audit reported and repaired two data-filter/target-comparison tooling incidents before release, then rebuilt all tables from unchanged source data; no source scores or model outputs were changed.

**Interpretation and limits.** The audit sharpens timing's trade-off: later repair can lower final old mean loss while increasing the worst measured intermediate old loss. It does not select a schedule, undo the original complete-screen failure, establish causation at a particular parameter block, or prove safety outside this synthetic task. Fresh data-only rescoring is not retraining, model replay, or third-party replication.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E14__NSS_NBR02_TIMING01_Analysis_v0.1__REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_receipts/R14__NSS_NBR02_TIMING01_Analysis_v0.1_Delivery.json`; `Research/NSS_NBR02_TIMING01_Complete_v0.1.zip::REPORT.md`; `.../analysis/SUMMARY.json`; `Research/NSS_WorkspaceSupport_v0.1.zip::.research_review/NBR02_TIMING01_v0.1_20260926/`.


<a id="pass-e17"></a>

### E17 — MICROMACRO01 v0.2: a bounded complete distributed repair cycle

**Broad questions.** G09 asks whether new learning can preserve older associations, while G14 asks whether replay/maintenance contributes more than simply spending more focal-practice work. This is a bounded synthetic repair comparison, not a lifelong learner or production Tertiary.

**Exact question and type.** Under a prospective operational contract allowing disclosed temporary and residual probability changes, can distributed old-record repair or an equal-work late repair burst keep the new answer correct, recover old probability quality, and survive two later learning receipts? Type: completed held-out full-cycle mechanism study and genuine adaptive replay. Status: the screen passed for D and B4 in G and L (with L exactly at 29/32); U and F4 failed the primary rule. Stricter mean-recovery sensitivity failed all old-repair schedules.

**Systems, split and controls.** Eight fresh 674-parameter float32 H16/D23 dense tanh initial fits, four paired per method; G uses exact gradients, L its specified local approximation for real and rehearsal examples. All eight old toy associations are directly available in a fixed buffer. Four development and eight held-out focal bases restart from the method/fit initial checkpoint. Eight actual receipts use `f,p,f,f,p,f,p,f`; `f` reverses at its third receipt. Receipt history, not hidden trial truth, triggers the changed-label correction/maintenance slots. These are 32 held-out contexts per method (8 bases × 4 fits), not 32 independent task families.

- **B1:** norm-1 corrections; no maintenance.
- **U:** one norm-2 strong changed-label correction; later norm 1; no repair.
- **D:** U plus four distributed eight-old-record batches after T3/T4/T5/T6, coefficients 1/8, 1/8, 1/8, 5/8.
- **B4:** same four old batches/coefficient list grouped after T6.
- **F4:** same distributed schedule as D, but replay eight repeats of the most recent confirmed focal record instead of old buffer.

T7/T8 are genuine additional receipts with no maintenance; no branch stops at a flattering cleanup point. D/B4/F4 each spend four extra applications and 32 example-gradient calculations per context. Every batch is recomputed at current prestate; equal data and applications do not guarantee equal step vectors, norms, latency or interference. No exact-gradient substitute is used for L.

**Fixed laboratory feasibility contract and admission.** Common old anchor is the T2 inventory; focal is rescored under the new target. Every focal class must be correct at T3–T8. At all actual intermediate states, average old target-probability decline ≤10 percentage points, no individual decline >35 points, and at least 7/8 old classes correct. At T6-complete, T7 and T8 stricter recovery/persistence boundaries require average decline ≤3 points, individual ≤20, ≥7/8 old classes, and positive equal-weight current-target mean change across eight old + focal records. Each branch/method needs at least 29/32 cycles and ≥6/8 within every fit. These are investigator-selected lab tolerances, not operational standards. A0 separately required initial acquisition and two-receipt recovery; both G/L passed all four fits (8/8 old labels, B1 mixed ≥16/20, and all acquisition/recovery/final focal checks). Development and held-out split remained distinct; no fit was selected away.

**Primary held-out cycle result.**

| Branch | G cycles passing | L cycles passing | Primary group screen |
|---|---:|---:|---|
| B1 original | 13/32 | 14/32 | FAIL / FAIL |
| U strong correction, no repair | 25/32 | 17/32 | FAIL / FAIL |
| D distributed old repair | 32/32 | 29/32 | PASS / PASS |
| B4 late old-repair burst | 32/32 | 29/32 | PASS / PASS |
| F4 distributed focal practice | 25/32 | 16/32 | FAIL / FAIL |

D and B4 fit totals are G 8,8,8,8/8 and L 7,6,8,8/8. All strong correction branches answered focal 32/32 at every measured stage, compared with first-correction B1 14/32 G and 16/32 L. D/B4 retained all old class answers at every recorded post-update boundary (2,560 repeated observations per method/branch; 256 model/base/cue combinations at ten boundaries), but this is probability repair, not recovery of wrong classes. Only L-F4 lost one old class at the final receipt; the other 34 held-out post-feedback focal class errors belonged to slow B1 first corrections.

**Quality, placement and failure trade-offs.**

| Branch | Final mean old loss G | Final mean old loss L |
|---|---:|---:|
| B1 | 0.020090 | 0.036429 |
| U | 0.027721 | 0.053546 |
| D | 0.016355 | 0.023923 |
| B4 | 0.015913 | 0.023867 |
| F4 | 0.027105 | 0.056066 |

D had lower final old loss than U and F4 in all 32 contexts per method and better final joint probability gain in all those contexts, while spending some focal confidence. Same example/application counts for D/F4 support a role for the lawful old-record choice in this schedule, not an equal-norm directional result. B4 ended slightly better than D: lower final old loss in 32/32 G and 26/32 L contexts; pooled means differ only 0.000442 G and 0.000056 L. D had lower peak per-context old loss than B4 in 31/32 G and 32/32 L, and lower six-stage mean in every context. These are differing trajectory metrics, not a universal schedule winner.

L-D's three failed cycles remain: transient individual declines >35 points (fit0/base7 after strong correction; fit1/base10 and base11 after next focal update), even though old classes remained correct. Max D individual decline was about 40.03 points. B4 failed the same three and had maximum decline 45.70. L-D's 29/32 is exactly the group threshold. Under a stricter 1-point average-recovery limit, G U/D/B4/F4 passed 19/21/21/18 of 32 and L 13/20/20/13; none qualified. At a 5-point allowance, G U reached 29/32 (and qualifies), G D/B4 32/32, G F4 29/32; L U/D/B4/F4 were 26/29/29/24 and only D/B4 qualify. Only the mean limit changes in this sensitivity; other constraints remain fixed.

The primary capture preserved 57,428 scored rows and 4,247 incorrect rows; held-out negative rows were 557 across surfaces, of which 35 were learned post-feedback class misses (34 B1 focal, one L-F4 old). The exact-label bookkeeping control scored all 576 after-receipt held-out focal/old queries but missed 16/64 before-feedback surprises. Correct classes with confidence-envelope failures are separately recorded.

**Attempt history, cost and limits.** The archive also preserves an engineering predecessor: MICROMACRO01 v0.1 finished its prefix and stopped at a 70,048,434-byte delivery forecast over 64 MiB, before main fits/mappings; 732 applications were durably committed. v0.2 made a storage-only forecast amendment (stratified filler, exact-envelope XZ) and raised administrative delivery ceiling to 80 MiB while retaining 64 MiB as desired size; its forecast became 67,985,769 bytes. It did not change model, seed, update, behavior threshold, case count or arithmetic. Full capture/replay added 11,512 applications, for 12,244/12,500 cumulative attempts/commits. Every natural update committed. The source report records an independent audit of primary/replay numerical evidence under empirical `2e-6+2e-5*abs(reference)`, max ratio 0.044046; its adaptive replay matched 84,628 frames / 293,950 arrays / 78,258,932 elements. This is historical study evidence, not a replay executed for this compendium. Cost totals and sampled memory/time do not show overall efficiency; OBS-DC01-COST-001 remains open. The unavailable earlier micro–macro source session is explicitly `UNKNOWN`, not inferred zero work or scientific failure.

**Interpretation and limits.** D and B4 are working candidates under a new explicit recovery contract with bounded nonzero deviations, not exact restoration, optimal scheduling, a proof of unbuffered-skill retention, lifelong plasticity or Tertiary dreaming. Rehearsal is not always required: a looser five-point allowance admits cheaper G/U. Preserve all failed L cycles and stricter-sensitivity failures. No follow-up is dispatched.

**Sources.** `Research/NSS_NBR02_MICROMACRO01_Complete_v0.2.zip::NSS_NBR02_MICROMACRO01_Execution_v0.2/REPORT.md`; `...::analysis/tables/SUMMARY.json`; `...::protocol/PROTOCOL.md`; `...::attempts/v0.1/audit/HISTORICAL_SUMMARY.json`; `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E17__NSS_NBR02_MICROMACRO01_Execution_v0.2__REPORT.md`; `...::source_receipts/R17__NSS_NBR02_MICROMACRO01_Complete_v0.2_Delivery.json`.


<a id="pass-e18"></a>

### E18 — TEACH01 v0.1: a fixed Primary surrogate teaches a Secondary surrogate

**Broad questions.** G14 asks whether structured replay/idle learning work adds later value beyond recent examples. G18 asks what an always-active Primary plus alternating auxiliaries would cost; this pilot only measures a surrogate teaching protocol and does not establish production scheduling. G09 is also relevant to retaining old behavior while teaching recent experience.

**Exact question and type.** Does a frozen, correct teacher's soft behavior on old associations omitted from a compact buffer help a student retain them, when combined with current focal replay, compared with ordinary replay or recent-example practice alone? Type: completed bounded teacher/student synthetic study, source-reported from E18 and delivery receipt. The full execution archive named by R18 (79,969,138 bytes) is missing from the current workspace; I rely on the register report and receipt for outcome claims and do not claim to have re-opened raw fit/replay arrays.

**Systems, data and controls.** Four fresh 674-parameter, 16-unit dense tanh Primary surrogates each learned eight stable binary associations with 100 exact-gradient updates, answered 8/8, and were frozen. Corresponding G (exact-gradient) and L (approximate local-gradient) Secondary surrogates started from each teacher's weight copy and adapted independently. The compact student old-record buffer held four of the eight associations, one per scope/label group; four old cues remained known by descriptor but lacked direct hard-target access in compact replay. Fixed teacher distributions at temperature 1 supplied soft targets for omitted old associations. The teacher never received new focal labels. A fixed inspectable curriculum coordinator made the shortlist; there was no learned Tertiary or natural-language RAG. No data was deleted.

Four development and eight assessment focal bases were crossed with four teacher initializations and two student rules (96 total contexts; 32 per method). Each context restarted from its teacher checkpoint. Students learned an original focal label, then a lawful reversal, received the same light four-record repair, and forked from a common pre-dream state into six deep treatments. All deep treatments used eight updates of eight examples with the same half-size post-clip step; compact old examples remain in each batch and teacher/recent/focal slots vary. Two additional real receipts followed each deep phase with no further repair. G used exact gradients throughout; L used its local rule for hard and soft targets.

| Branch | Deep treatment |
|---|---|
| NONE | No deep consolidation; still receives shared prior light repair |
| REPLAY | Compact old hard targets only |
| TEACHER | Compact old plus frozen-teacher outputs on four omitted old cues |
| RECENT | Compact old plus latest lawful focal record |
| BOTH | Compact old plus teacher targets plus latest focal record |
| FULL_RECORDS | BOTH inputs, but omitted old targets supplied as expanded-buffer hard labels |

FULL_RECORDS is an information/storage upper reference, not an equal-memory competitor. Teacher snapshots/caches and distillation are not free; four missing one-bit labels are vastly smaller than a full model.

**Prospective full-cycle and incremental-teacher gates.** A screen pass required focal probability ≥0.75 and correct class; average old-probability decrease ≤0.03 from common post-receipt-2 anchor; max individual old decline ≤0.20; at least 7/8 old classes correct; and positive equal-weight nine-record current-target probability gain. These criteria applied at dream completion and after each of two later real receipts. Each branch needed ≥29/32 cycles and ≥6/8 in every fit. These allow bounded intermediate changes and evaluate recovery/persistence rather than prevention of every transient dip. A separate teacher-value discriminator compared BOTH with RECENT: lower final omitted-old mean loss in at least 6/8 base means, pooled decrease ≥0.001 nats, no more than one added focal-class error.

**Cycle results and teacher-value discriminator.**

| Branch | G qualifying cycles | L qualifying cycles | Group decision |
|---|---:|---:|---|
| NONE | 29/32 | 29/32 | PASS / PASS |
| REPLAY | 32/32 | 32/32 | PASS / PASS |
| TEACHER | 32/32 | 32/32 | PASS / PASS |
| RECENT | 32/32 | 32/32 | PASS / PASS |
| BOTH | 32/32 | 32/32 | PASS / PASS |
| FULL_RECORDS | 32/32 | 32/32 | PASS / PASS |

Because even NONE qualified at 29/32 and simpler REPLAY qualified at 32/32, all-arm pass does not mean the teacher or deep consolidation was necessary. The distinct discriminator did pass: BOTH had 8/8 favorable omitted-old base means, no added focal class errors, and pooled omitted-old loss reductions of 0.00188304 G / 0.00213751 L relative to RECENT.

Final mean loss on the four old associations omitted from the compact hard-target buffer:

| Branch | G | L |
|---|---:|---:|
| NONE | 0.02240566 | 0.02174632 |
| REPLAY | 0.01197906 | 0.01228108 |
| TEACHER | 0.01051281 | 0.01057802 |
| RECENT | 0.01365918 | 0.01400690 |
| BOTH | 0.01177614 | 0.01186940 |
| FULL_RECORDS | 0.01160528 | 0.01168791 |

BOTH lowers omitted-old loss relative to RECENT by about 13.8% G and 15.3% L. Adding recent focal evidence to TEACHER lowers final focal loss 0.00890181→0.00728793 G and 0.00891720→0.00730179 L, with a small old-loss cost; the class was correct in either case. FULL_RECORDS is slightly better than BOTH on old and focal mean losses, so hard records remain a strong reference. All actual post-update old/focal class answers were correct in the bounded pilot; measured differences concern probability quality and declared envelope.

**Failures, cost and limits.** There were 189 incorrect query rows in primary capture: 43 teacher pre-feedback, 52 development focal pre-feedback, 94 assessment focal pre-feedback. No inventory class error occurred; six NONE cycle failures concern the operating envelope, not old-class misclassification. All attempts across capture/replay: 12,528 parameter applications/commits, 68,132 example-gradient calculations, 538,956 cells, 179,652 heads, 57,600 record fetches and 6,144 teacher-cache reads. These include deliberately wrong isolated sandbox updates; no fit was retried/selected/extended. The source report records NumPy audits and internal replay passing at the stated empirical tolerances, but no overall storage-efficiency or deployed latency win is established. Teacher is a same-size synthetic Primary surrogate, never exposed to focal labels; there is no fallible/wrong-teacher treatment, long-term plasticity decline, wholly new post-dream task, live state migration, learned Tertiary selection, full core scheduler, or three-core qualification.

**Interpretation and evidence boundary.** The study supports a modest bounded result: fixed teacher outputs can complement recent evidence for omitted old associations in this small task. Ordinary replay, recent practice, and expanded accurate hard records also work, with complete hard records slightly better. It does not qualify dream computation, zero-data learning, retrieval retirement, a trained Tertiary, whole-system cost, or Primary participation scheduling. The report/receipt give valuable source-reported outcome detail, but the missing full execution ZIP means no independent raw-array rescore was done for this compendium.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E18__NSS_NBR02_TEACH01_Execution_v0.1__REPORT.md`; `...::source_receipts/R18__NSS_NBR02_TEACH01_Complete_v0.1_Delivery.json`; `Research/NSS_Research_and_Architecture_Chat_Handoff_v1.1.md` (source-absence map only).


<a id="pass-recover01-v0-2"></a>

### RECOVER01-v0.2 — Ordinary replay recovery after new association learning

**Type and status:** Completed bounded diagnostic as reported by the later planning and checklist records; not independently recounted or rerun in this review. Status in checklist v0.19: `COMPLETED_DIAGNOSTIC_STRONG_RECOVERY`. This is distinct from the earlier RECOVER01 v0.1 *proposal*, which specified a prospective four-arm experiment and is not evidence that it ran.

**Broad question:** Can ordinary rehearsal of old work repair old-task errors after learning a new association, while the corrected association remains learned? This concerns parameter-update interference and recovery, not the quality of a language reader or a complete multi-night companion.

**Specific question:** After the reported new-B learning step, does the replay path reduce the observed old-task error burden, and do corrected B class mappings remain available afterward? The newer source summary reports that the study resets each correction context to its original parent. Consequently it does not test a chain of successive accepted checkpoints or task-state continuation under changed weights.

**Systems and arms:** The documentary material consulted states the ordinary replay comparison and the retained post-learning measurements but does not reproduce a complete arm roster, branch names, or per-arm table. Checklist v0.19 gives no executable system description. Direct-plan S04 points to a separate `NSS_NBR02_RECOVER01_Report_v0.2.md`; that named report was not present in this workspace source set. I therefore do not backfill the v0.1 proposal’s U/L/R/LR arms, schedules, model specification, seeds, or task counts as though they were confirmed v0.2 details.

**Method, data and decision rules:** Exact model architecture, training steps, cohort/seed counts, input-generation split, update budget, replay quantity, numerical tolerance, old-task gate and stopping/resource rules are not recoverable from the bounded sources read for this chapter. The later plan characterizes the empirical result as ordinary replay after learning and specifically notes reset-to-original-parent contexts. It should not be upgraded to a sustained accepted-generation test, a broad no-forgetting guarantee or an equal-compute architecture comparison.

**Reported outcomes:** The later plan gives the principal aggregate: recorded post-learning errors fell from **152,606 to 1,055**, and **all 32 corrected class mappings were retained**. It also explicitly retains **false-DONE errors** and a **strict numerical-contract failure**. Denominators, identities of the counted answer locations, per-parent breakdown, arm table, and error-class table are not present in the reviewed plan/checklist excerpts, so the two error totals must remain exactly as reported rather than converted to rates or attributed to a specific arm beyond the ordinary-replay recovery claim. The class-mapping count is likewise not a whole-task, false-completion or numeric-parity result.

| Reported aggregate | Outcome | Scope limit |
|---|---:|---|
| Recorded post-learning errors, before → after recovery | 152,606 → 1,055 | Source summary does not expose denominator or per-parent distribution. |
| Corrected class mappings retained | 32/32 | Does not imply all residual old-task behavior is correct. |
| False-DONE errors | Persisted | Count, denominator and arm breakdown unavailable in the reviewed source extracts. |
| Strict numerical contract | Failed | Exact failing comparisons/tolerance are unavailable here; failure remains open. |

**Meaning and limits:** This is a large source-reported reduction in recorded errors with all 32 corrected mappings retained, alongside explicit residual false completion and strict numerical failure. That combination supports retaining ordinary replay as a strong bounded reference, not declaring the recovery mechanism qualified. The plan says reset-to-parent correction contexts prevent inference about long-run accepted-model accumulation. The report is not a fresh replication, and the lower aggregate count must not erase the false-DONE or numerical gates.

**Source locators:** Later-plan summary and boundaries: `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §§1–2 (especially source register S04, named as `NSS_NBR02_RECOVER01_Report_v0.2.md`, and the cumulative-learning discussion); `Research/NSS_DIRECT01_Chat_Handoff_v0.1.md`, “Evidence reconciliation”; BRIDGE package checklist ledger `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` and `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json`. The named RECOVER01 v0.2 report itself was not located in the bounded workspace inventory; the older `Research/NSS_NBR02_RECOVER01_Proposal_v0.1.md` is explicitly a proposal and is not the execution report.


<a id="pass-cycle01-a"></a>

### CYCLE01-A — Two-night maintenance feasibility

**Type and status:** Completed two-night development feasibility; `COMPLETE_DEVELOPMENT_FEASIBILITY / PROMISING_BALANCED_REPLAY_SIGNAL / RESERVED_MAIN_NOT_RUN`. This is the executed/report-described **CYCLE01-A** parent-history study. It must remain distinct from the general CYCLE01 roadmap and the unstarted longer CYCLE01-B confirmation proposal. The source was inspected as an embedded report in the BRIDGE01 provenance package; this chapter did not rerun the source archive or models.

**Broad question:** Can a learning system keep its serving model fixed during a simulated day, record current facts exactly, then train and gate a candidate at night so that an accepted revision carries unfinished work into the next day?

**Specific question:** Starting from four retained recurrent checklist parents, which of no update, B acquisition only, B acquisition followed by A-only replay, or B acquisition followed by balanced A replay plus current-B practice can pass the declared candidate gate over two development nights while retaining old checklist behavior and using the latest current cue mappings?

**Systems and arms:** Four source parents **4101–4104**, each `GRUCell(26,64) + Linear(64,9)` with 18,249 parameters. The float32 source arrays (72,996 bytes) were copied into float64 execution arrays (145,992 bytes); this precision conversion does not erase the separate historical float32/numerical failures. At each parent/night branch:

- **FIXED:** no parameter update, while the exact current evidence ledger remains available; measures unchanged model plus current-source retrieval.
- **LEARN:** 64 updates on current association task B only; isolates acquisition without A repair.
- **REPLAY:** 64 B updates followed by 32 old checklist A-only updates; ordinary repair omitting B from the repair objective.
- **BALANCED:** 64 B updates followed by 32 updates on A and current B; this differs from the named BALANCE01 proposal because it used a fixed update rate and did not cross the old-A/current-B factor with a gentler update-size factor.

The exact ledger was current for all policies and receives each event immediately. The neural B cue probe supplies the cue without its target label; B scoring is separate from source truth. This isolates finite association change, not new procedural learning or English-language comprehension.

**Method, data, gate and resources:** Task A is an eight-item checklist. SET completes the named item, CLEAR reopens it, RESET clears all, and NOOP changes nothing; answer is the lowest-numbered incomplete item or DONE only when all are complete. Task B begins as eight alternating binary cue assignments; night/day one changes cue 0, and day two changes cue 1 while carrying the first correction forward. For each parent, two nights run through independent policy branches. All data are development: 32 guard histories (eight per task family), eight continuing histories over two days, and 32 live events per day after prefixes of 8 or 24 events. The same histories recur across the four parents/policies; trial counts are not independent sample size. Each A replay phase reuses 64 batches per parent (2×32). All weights are eligible; a fresh Adam optimizer is used per phase, learning rate .003, gradient clip 1.0. LEARN/REPLAY/BALANCED have different total/current-B exposure, and there was no B96-only control.

Predeclared acceptance required all eight B class labels with target probability at least .80, old-task event accuracy at least 98%, complete-history accuracy at least 90%, bounded loss against original and previous-revision anchors (maximum two of 32 whole-history losses), no new false-DONE, and valid lineage/numerics. Continuation probes were informative but did not affect adoption. Gate-deferred candidates remained unserved. The work used 2,048 development optimizer applications plus seven disposable applications; no new fits. One caller interruption occurred after 15 branches and the last branch’s B64 checkpoint; locked continuation applied only the 32 missing A/B updates and repeated zero optimizer steps. Unknown discarded inference/time/RSS is explicitly not supplied. Reported known branch-core time was 9.873 s, audit 1.394 s; maximum recorded completed branch/resume RSS 335,753,216 bytes.

**Aggregate end-of-second-night outcomes:**

| Policy | Accepted revisions / 8 attempted nights | Neural current-B answers | Guard A answers | Both-day continuation answers | Entire two-day histories correct |
|---|---:|---:|---:|---:|---:|
| FIXED | No candidates proposed | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| LEARN | 0/8 | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| REPLAY | 0/8 | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| BALANCED | 5/8 | **32/32** | **4,087/4,096 (99.78%)** | **2,046/2,048 (99.90%)** | **30/32 (93.75%)** |

FIXED/LEARN/REPLAY’s perfect old-task totals largely reflect preserving the original checkpoint or source ledger, not successful acquisition plus repair: all eight changed neural B answers (two per parent) remained missing at endpoint. BALANCED acquired all four parents’ eight B classes. Its guard and live counts still include errors; it is not error free.

| Parent | BALANCED night 1 accepted | BALANCED night 2 accepted | Final guard answers | Final B classes | Both-day continuation answers |
|---|---|---|---:|---:|---:|
| 4101 | No | Yes | 1,023/1,024 | 8/8 | 511/512 |
| 4102 | No | Yes | 1,017/1,024 | 8/8 | 512/512 |
| 4103 | Yes | Yes | 1,024/1,024 | 8/8 | 511/512 |
| 4104 | No | Yes | 1,023/1,024 | 8/8 | 512/512 |

Only 4103 was accepted on both nights; 4101, 4102 and 4104 were rejected on night one and accepted on night two. Three night-one BALANCED candidates failed due to new false-DONE outputs; one also lost three whole histories. One candidate was accepted with modest non-completion errors. All four final night-two BALANCED candidates passed the unchanged gate. LEARN’s night-one candidates acquired B but severely damaged A; REPLAY candidates’ B target confidence fell below .80 despite correct labels; night-two LEARN and REPLAY still missed both changed cue classes per fixed budget.

Across accepted BALANCED endpoints, there were nine guard answer errors, 125/128 guard histories completely correct, two live errors at a repeated source occasion (parents 4101 and 4103, after SET(1) with item 0 still pending but answer item 7), and no live false-DONE. These two responses are the same source occasion, not two independent failure contexts. The two errors are wrong next-item answers, not false completion.

**Engineering verification, stops and interpretation:** All 4,608 next-event rule cases were checked, 126,976 A suffix predictions were recounted, 16 preflight groups were run, 2,048 development and seven disposable optimizer applications are accounted for, 232 retained outputs replayed bit-exactly in fresh processes, and 160 checkpoint files were hash-verified. Across 9,304,960 scalar comparisons there were zero failures of the newly declared float64 numerical envelope or class changes; that result is scoped to the new contract and does not fix older numerical failures. The 32-update continuation verified a phase-barrier resume rather than duplicating earlier updates. Some inference/time/RSS from the interrupted caller was discarded and remains unknown.

The balanced route is a promising development signal, not an adopted NSS learner or confirmed winner. All material histories and thresholds were development data; a different gate could accept different branches. B practice was not exposure-matched to the replay policies, so the gain cannot be uniquely attributed to balancing current B into A repair. The long-cycle confirmation and B96-only extra-practice control were explicitly not run; no procedure learning, deployment or HSA/DARP integration occurred.

**Source locators:** exact embedded report `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/REPORT.md`, §§1–10; delivery receipt `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/NSS_NBR02_CYCLE01A_Delivery_v0.1.json`; source-verification record `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/SOURCE_VERIFICATION.json`. The embedded report identifies original execution archive `NSS_NBR02_CYCLE01A_Feasibility_v0.1.zip` and its receipt, but the original execution ZIP itself was not present as a separate workspace file/member in this bounded review. The BRIDGE provenance says the archive’s declared 803 payload byte counts/SHA-256 values and ZIP membership/CRC had been checked before extraction; this is lineage/integrity reporting, not a rerun.


<a id="question-8"></a>

## 8. Can evaluation and revision preserve decisions and continuation?


<a id="pass-e15"></a>

### E15 — C00-CONTRACT01: a synthetic change-and-review/adoption contract

**Broad questions.** G16 asks whether a critic/evaluator can detect unsupported or harmful changes while retaining useful supported changes. This is an ordinary deterministic contract/conformance pilot for a possible reviewer; it does not test a neural critic. G10 is touched only as a simulated candidate-adoption boundary.

**Exact question and type.** Given caller-supplied old/new capability measurements and numerical tolerances, does a finite rule enforce per-record protection, valid evidence, cumulative anchors, durable review/adoption records, stale-token rejection, and conservative handling of interrupted writes? Type: synthetic engineering conformance testing. No network or model was loaded; no forward, gradient, optimizer update, or historical study reran. Fixture outcomes were deliberately authored, not sampled from a learner.

**Contract and systems.** The synthetic case has three protected old capabilities, one legitimately corrected focal target, integer-thousandth binary probability tables, a rolling parent and a stable epoch anchor. Caller-supplied example tolerances include at most 0.05 per-record loss from parent and 0.10 from epoch, with old/focal probability floors of 0.60/0.85. These are demonstration fixture numbers, not calibrated safety standards. The finite decision rule uses current public focal target (not superseded target), refuses to trade invalid authority for better accuracy, and checks each protected record rather than accepting a favorable average. A simulated store journals review/adoption intent, version, state and acknowledgment; it is not a live serving API or neural reviewer.

**Retained v0.1 attempt and v0.2 correction.** The archive preserves two source-locked iterations. v0.1's fixed-fixture pass appeared to agree on 1,484 authored cases, but a post-run adversarial schema probe passed the string `"false"` as permission; truthy coercion incorrectly made it eligible. The candidate was withdrawn. v0.2 added strict Boolean checks for permission, authority, state-compatibility and pending-trace flags plus ten adversarial cases; it reran the old cases under a new source lock. This is a real engineering defect and correction, not a neural result or operational qualification.

| Version / disposition | Cases | ADOPT_ELIGIBLE | Behavioral DEFER | Unresolved/stale DEFER | Integrity/schema REJECT |
|---|---:|---:|---:|---:|---:|
| v0.1 original fixture screen, subsequently withdrawn | 1,484 | 256 | 479 | 733 | 16 |
| v0.2 corrected Boolean/schema screen | 1,494 | 256 | 479 | 733 | 26 |

The 733 unresolved cases are not established harmful changes; 479 behavioral violations were deliberately authored. The corrected v0.2 independent evaluator matched every disposition, reason, input hash and metric. On the same fixture set, its finite-rule/accept-all/never-adopt controls behaved as follows:

| Policy | Eligible cases missed | Behavioral violations allowed | Integrity-invalid cases allowed | Unresolved cases allowed |
|---|---:|---:|---:|---:|
| Contract rule | 0 | 0 | 0 | 0 |
| Accept all | 0 | 479 | 26 | 733 |
| Never adopt | 256 | 0 | 0 | 0 |

A cumulative fixture accepted successive 0.04 reductions (0.95→0.91→0.87) from the parent but deferred the third (0.87→0.83) when total epoch decline reached 0.12 versus 0.10 allowed. After review, changed parent/epoch/target receipts made three adoption tokens stale and re-evaluation blocked them. Repeated operation IDs were rejected. Two child processes ended after durable intent and after state write, respectively; both were `UNKNOWN_COMPLETION`, and retry was blocked. In the latter, the new simulated state physically existed without acknowledgment, demonstrating that this pilot does not prove safe publication to real readers.

Six copied journal corruptions and one state-hash alteration were detected. A correctly chained prefix still passed local chain checks when external terminal identity was absent; hashes do not authenticate an arbitrary rewritten source. A hidden-capability pair had byte-identical reviewer-visible evidence and identical eligibility, while one evaluator-only description declared an unobserved capability broken. One broader-scope miss is an information limit, not a random performance estimate.

**Replay, version totals and interpretation.** The original v0.1 attempt had 1,484 cases, 3,024 ordinary rule evaluations across capture/replay, and the real schema miss was a subsequent adversarial QA finding. v0.2's total authorizations count 3,024 original rule calls +1 adverse QA call +3,044 corrected-version calls =6,069/10,000. Its primary grid has 1,494 cases. Fresh processes matched deterministic files; v0.2 replay had 46 file comparisons / 12,169,214 bytes per side. All 25 independent lifecycle assertions passed. These are software tests, not optimizer steps, held-out real tasks or broad robustness estimates. v0.1 and v0.2 both retained a deliberately authored public-panel blind spot.

**Limits and disposition.** C00 supplies a bounded ordinary engineering baseline for finite-panel decision semantics, cumulative anchors, audit journaling and simulated adoption recheck. It does not establish suitable operational tolerances, adequate coverage outside observed records, authenticated real measurements, atomic user-visible publication/recovery, a learned reviewer, triage quality, autonomous repair, or Tertiary utility. `RET-C00-POLICY-001`, `COVERAGE-001`, `PUBLISH-001`, and `AUTHORITY-001` remain open.

**Sources.** `Research/NSS_C00_Contract_Complete_v0.2.zip::REPORT.md`; `...::protocol/PROTOCOL.md`; `...::program/STEP_00_CONTRACT.md`; `...::results/primary/SUMMARY.json`; `...::attempts/v0.1/REPORT.md`; `...::attempts/v0.1/WITHDRAWAL_ADDENDUM.md`; `...::attempts/v0.1/results/primary/SUMMARY.json`; `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E15__NSS_C00_Contract_Execution_v0.2__REPORT.md`; `...::source_receipts/R15__NSS_C00_Contract_Complete_v0.2_Delivery.json`.


<a id="pass-e16"></a>

### E16 — EVAL01 v0.2: targeted review reduces harmful approvals but defers more useful changes

**Broad questions.** G16 asks about useful, fallible evaluation/review; G10 is touched by the simulated keep/defer candidate decision. This is an offline evaluator comparison on previously exposed learning outputs, not a learned critic, new model update, real adoption, or a live publication process.

**Exact question and type.** On fixed candidate snapshots from REV01 and TIMING01, how does a five-record targeted old-skill panel trade false approvals against missed acceptable changes compared with two fixed five-record panels and a nine-record full reference? Type: retrospective finite-panel policy/evaluation study. Status: completed; no historic model was instantiated, queried, trained, differentiated, edited, or adopted. Development/exposed held-out observations are historical, not fresh confirmation.

**Source data and measurement.** The two source archives' identities/CRCs and direct payloads were checked; selected raw numerical streams were losslessly reconstructed and query classes/losses recomputed from captured logits. REV01 provided 768 candidate occasions / 768 distinct versions from 96 method/fit/base contexts; TIMING01 1,728 occasions / 1,440 distinct versions from 96 contexts (288 aliases share parameters/current targets). Total 2,496 occasions / 2,208 distinct versions. The main historical-held-out comparison uses 1,472 candidate snapshots across 128 model/base contexts; the remaining development snapshots are tabulated separately. Snapshots, boundaries, replay, policies and repeated source measurements are not independent new tasks. This is not a simulated cumulative learner: rejecting an archived earlier update would change subsequent training, so paths were not spliced.

Every partial policy receives the same eight old reference records, current correction receipt, and parent/candidate version data. The parent panel is charged as nine records per standalone opportunity. `FIXED_LOW` selects one fixed old record per scope/label group plus focal; `TARGETED` selects per-scope the initially less-confident record with label opposite the correction and one fixed record of the other label; `FIXED_HIGH` uses the other fixed coordinate in each group; all three inspect four old + focal records (five candidate values). `FULL_PANEL` queries all eight old outputs + focal (nine). `ACCEPT_ALL` and `NEVER_ADOPT` are boundary controls. These are stored-output requests, not newly executed neural forwards or deployed latency. TARGETED is an ordinary fixed heuristic motivated by previously observed label-group interference; it never sees unqueried candidate outputs.

**Prospective review contract.** Three local illustrative contracts, CAUTIOUS, MODERATE (primary) and PERMISSIVE, were fixed before this audit and do not revise prior study gates. MODERATE requires focal probability ≥0.60 and gain ≥0.10 over parent under current target; average old target-probability decline ≤0.03; worst individual decline ≤0.25; old target probability ≥0.40; at most one newly wrong old class among eight; and positive equal-weight mean target-probability gain over nine capabilities. Partial rules apply rate/mean to their four inspected old records; that risk-selected subset is not an unbiased sample. Full-panel judgment is only a finite-panel reference, not a population truth oracle.

**Moderate-contract results (historical held-out cohort, n=1,472 snapshots).** Of these, 1,158 were acceptable under the full finite-panel contract. TARGETED lowered out-of-envelope approvals relative to FIXED_LOW but deferred more acceptable candidates:

| Policy | Acceptable retained /1,158 | Acceptable deferred | Outside-envelope approvals | Candidate records checked |
|---|---:|---:|---:|---:|
| FIXED_LOW | 1,112 (96.03%) | 46 | 14 | 5 |
| TARGETED | 1,074 (92.75%) | 84 | 2 | 5 |
| FIXED_HIGH | 1,123 (96.98%) | 35 | 33 | 5 |
| FULL_PANEL | 1,158 | 0 | 0 | 9 |
| ACCEPT_ALL | 1,158 | 0 | 314 | 0 |
| NEVER_ADOPT | 0 | 1,158 | 0 | 0 |

Relative to FIXED_LOW, TARGETED removed 12 approvals violating full-panel limits but deferred 38 additional acceptable offers; none of the candidates selected by the three partial panels had an old class error in the moderate cohort. Their 14/2/33 false approvals violated confidence-decline limits; ACCEPT_ALL has 23 repeated old-class error observations, not 23 independent skills. All 84 TARGETED false deferrals were triggered by OLD_MEAN_DROP; both remaining false approvals were TIMING01-L where the sampled mean understated full-panel decline.

| Source / learner | FIXED_LOW bad approvals / acceptable deferrals | TARGETED bad approvals / acceptable deferrals |
|---|---:|---:|
| REV01 / G | 7 / 3 | 0 / 9 |
| REV01 / L | 6 / 8 | 0 / 35 |
| TIMING01 / G | 0 / 12 | 0 / 11 |
| TIMING01 / L | 1 / 23 | 2 / 29 |

Thus targeted review did not win every stratum: for REV01-L it removed six bad approvals but deferred 27 additional acceptable offers versus FIXED_LOW and kept 78.71% of fixed's acceptable probability gain; for TIMING01-L it was worse on both decision counts. TARGETED's extra deferrals cannot be dismissed by its pooled improvement. FIXED_HIGH can alter apparent comparison, which is why all fixed choices remain reported.

**Sensitivity (not threshold selection).**

| Contract | Full-panel acceptable n | FIXED_LOW bad / missed | TARGETED bad / missed |
|---|---:|---:|---:|
| CAUTIOUS | 796 | 111 / 65 | 8 / 139 |
| MODERATE | 1,158 | 14 / 46 | 2 / 84 |
| PERMISSIVE | 1,279 | 12 / 31 | 1 / 56 |

The protection/opportunity trade-off persists under all three authored tolerances; none is adopted as production policy. No prior failures are reclassified. Engineering checks caught two evidence-adapter failures before candidate review (interleaved branch state identity and REV01/TIMING01 manifest schema difference) and retained the failed versions/logs. Fourteen finite engineering fixtures passed after repair; an independent provenance audit checked 25,920 candidate/parent measurements and receipt chronology. One primary pass plus fresh review replay each evaluated 39,744 policy/profile decisions. Replay recomputed decisions from stored logits; zero neural forwards, gradients or optimizer updates. Source archives remain necessary for original trajectory provenance.

**Interpretation and limits.** The strongest conclusion is that a sentinel/risk-targeted subset and a representative mean-impact estimator are distinct jobs. Risk targeting is more cautious on the pooled cohort but can over-defer acceptable offers and still miss unqueried-panel harm in a stratum. Neither a five-record heuristic nor a full finite panel is universally qualified, calibrated, or authorized to publish weights. C00's real publication, authenticated measurement and policy calibration gaps remain open.

**Sources.** `Research/NSS_NBR02_EVAL01_Complete_v0.2.zip::REPORT.md`; `...::analysis/SUMMARY.json`; `...::protocol/PROTOCOL.md`; `...::inputs/REV01/SOURCE_REPORT.md`; `...::inputs/TIMING01/SOURCE_REPORT.md`; `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E16__NSS_NBR02_EVAL01_Execution_v0.2__REPORT.md`; `...::source_receipts/R16__NSS_NBR02_EVAL01_Complete_v0.2_Delivery.json`.


<a id="pass-e19"></a>

### E19 — STATEBRIDGE01 v0.2: retained task state under changed weights

**Broad questions.** G03 asks what survives events and weight revisions; G05 asks whether recurrence/feedback produces instability; G10 concerns candidate revisions and when tasks use them. STATEBRIDGE01 tests a particular saved-state/changed-parameter interaction, not a general task scheduler or state migration system.

**Exact question and type.** When an in-progress task continues after a separate focal-association learning phase changes model parameters, is the saved recurrent state still usable? Is keeping the task on its original weights better than carrying that state into new weights or rebuilding the public prefix under the new weights? Type: complete diagnostic execution plus historical adaptive replay. Status: not qualified—the original whole-trajectory numerical gate failed 11 array comparisons, and both changed-weight continuation/rebuild adequacy screens failed after fixed repair.

**Systems, task and protocol.** New model: GRUCell(16,64)+Linear(64,9), 16,329 parameters, 65,316 float32 parameter bytes, plus 256-byte task state. Four fits received exactly 2,000 Adam updates each. Task A is an eight-flag checklist and predicts the full next-incomplete answer/DONE; task B is four scoped binary associations sharing A's bit-0 logit. The exact shared output is a study choice, not a diagnosis of prior failures. Task routing, no-op filtering, version checks and receipts are provided software. No historical weights or hidden state were loaded.

After creating 32 fresh A prefixes per fit (all 16 endpoint masks at lengths 33/65; each has an eight-event continuation leaving one flag untouched), models learned B via eight lawful online receipts (SGD lr 0.5, clip 1) then four fixed repair batches (lr 0.1, clip 1). Repair examples were eight actually observed length-17 A episodes plus all currently released B labels, not test A labels or future feedback. Eight B cue/order scenarios crossed four cues with two receipt orders. Scenarios start at the terminal initial fit; they are not a continuous life history. At original, post-learning and post-repair weights, five continuation positions (0/1/2/4/8) compared:

- **CARRY:** original saved h with current learned parameters.
- **REBUILD:** same public prefix replayed at current parameters, then same suffix.
- **RESET:** zero state without prefix, information-removal diagnostic.
- **PINNED:** original saved h with immutable original parameters.

Each main result denominator 5,120 is four fits × eight B scenarios × 32 A histories × five readouts; paired repetitions, not 5,120 independent tasks. Joint success requires both checklist-bit vector and next-action correct. A0 admitted all four fits (160/160 joint A, 4/4 B associations; zero-history reset 46/160). No correct state was given as model input; only terminal checkpoints were used. Changed-stage initial fit state reads and later transition behavior were scored by an independent task oracle.

**Main paired continuation result (diagnostic counts; no qualification).**

| Parameter stage | CARRY | REBUILD | RESET | PINNED |
|---|---:|---:|---:|---:|
| Original weights | 5,120/5,120 (100%) | 5,120/5,120 (100%) | 1,472/5,120 (28.75%) | 5,120/5,120 (100%) |
| After B learning | 4,050/5,120 (79.10%) | 2,503/5,120 (48.89%) | 1,184/5,120 (23.13%) | 5,120/5,120 (100%) |
| After fixed repair | 4,519/5,120 (88.26%) | 3,355/5,120 (65.53%) | 1,216/5,120 (23.75%) | 5,120/5,120 (100%) |

CARRY exceeded REBUILD in all 32 fit/scenario context aggregates at changed-weight stages; it still did not win every individual query. After learning, REBUILD rescued 13 CARRY errors while CARRY rescued 1,560 REBUILD errors; after repair, 19 and 1,183 respectively. PINNED preserved original A but cannot count as complete adaptation because it retains the obsolete B answer.

After-repair adequacy required A joint correctness ≥95%, loss versus original joint accuracy ≤5 percentage points, and correct changed-B answer; at least 29/32 scenarios and ≥6/8 per fit. CARRY was 9/32 (fit counts 2,3,2,2); REBUILD 1/32 (0,0,1,0). Both fail. These pilot thresholds are not universal operational tolerances.

**Immediate state readability and trajectory failures.** Changed weights read the saved state at continuation position zero in 1,024/1,024 queries after both learning and repair—there is no immediate state-unreadability finding. As the task continued under new weights, CARRY fell:

| Position | After B learning | After repair |
|---|---:|---:|
| 0 | 1,024/1,024 | 1,024/1,024 |
| 1 | 1,022/1,024 | 1,024/1,024 |
| 2 | 790/1,024 | 986/1,024 |
| 4 | 604/1,024 | 815/1,024 |
| 8 endpoint | 610/1,024 (59.57%) | 670/1,024 (65.43%) |

REBUILD was already weaker at immediate read (483/1,024 after learning, 611/1,024 after repair); rebuilding applies changed transition weights throughout the prefix. This locates a behavioral continuation problem under changed parameters but not a unique gate/layer/cause. All six tensors changed and the shared A/B output permits interference.

**B association and numerical outcomes.** Focal B class was 32/32 after both online learning and repair; the other three old B labels were 64/96 and then 83/96. PINNED retained 96/96 old B labels but gave the now-obsolete B answer in all 32 focal scenarios; Task A retention is reported separately in the continuation table with denominator 5,120. The fixed repair helped A and most old B answers while retaining new B, but was incomplete.

The original independent float64 whole-prefix scorer checked 37,178,292 scalar comparisons, 488 recorded exact SGD updates and 120 stage weight sets. All captured gradient/application checks passed, yet 11 comparisons exceeded the frozen `2e-6 + 2e-5*abs(reference)` tolerance (10 logits, one state; max ratio 12.4231); it stopped and the scientific pass is NOT_QUALIFIED. A labeled diagnostic copy preserved the same class decisions plus `strict_numerical_pass=false`. Later localization reported 21,498,624 one-step scalars with zero failures; 1,527,552 whole-prefix logit scalars with 17 tolerance exceedances (max abs 4.33727e−05); 76,800 full-chain scored A queries with no class/joint-decision disagreement (max logit delta 9.83880e−06). These supplementary views do not repair the original failed gate. Main A read success and replay equality likewise do not waive it.

The study preserves 2,240 B pre-feedback/post-update observations and 503 negatives across labelled surfaces, with surprises before feedback kept distinct. The source report records a fresh full adaptive replay matching all 1,656 files (229,901,990 bytes per side); this compendium did not execute that replay. The data ledger audit confirmed targets and intents/commits; this is internal replay, not third-party replication.

**Engineering history, costs and limits.** STATEBRIDGE v0.1 stopped at an API shape error before first tensor copy (one update attempt, one backward, three examples; no durable completion). v0.2 corrected that fixture issue under a new source lock. Total across both: 17,025 application attempts, 17,024 durable completions; 17,017 reverse-mode attempts; 7,393,659 cell examples and 7,425,147 heads against caps. The main diagnostic uses 32 logical task states referencing shared weights, not 32 full-model copies; versioning/storage costs are small tensor components, not total service costs. The complete archive and receipt independently preserve the original numerical failure and status `NOT_QUALIFIED`; a hash pass does not equal scientific qualification. No state mapper, learned token curation, neural reviewer, production scheduler, Tertiary or architecture was adopted.

**Interpretation and limits.** Preserving a saved state alone does not preserve the task computation under a new transition function. PINNED protects old progress but ignores new correction; CARRY is initially readable but degrades across the continuation; REBUILD is worse here and repair helps but does not meet the fixed adequacy rule. Keep both return tickets open: RET-STATEBRIDGE-NUMERIC-001 and RET-STATEBRIDGE-CONTINUATION-001. The task grammar, shared output and finite prefixes sharply limit generality.

**Sources.** `Research/NSS_Research_Consolidation_v0.1.zip::source_reports/E19__NSS_NBR02_STATEBRIDGE01_Execution_v0.2__REPORT.md`; `...::source_receipts/R19__NSS_NBR02_STATEBRIDGE01_Diagnostic_v0.2_Delivery.json`; `Research/NSS_NBR02_STATEBRIDGE01_Diagnostic_v0.2.zip::NSS_NBR02_STATEBRIDGE01_Execution_v0.2/REPORT.md`; `...::analysis/tables/SUMMARY.json`; `...::analysis/numerical_localization/SUMMARY.json`; `...::protocol/PROTOCOL.md`.


<a id="pass-e20"></a>

### E20 — SURFACE01 v0.1: fixed-weight baseline failed zero false-DONE admission

**Broad questions.** G02 asks whether a task failure reflects architecture, training, data or interface; G03 asks what task meaning survives an event sequence; G05 asks whether recurrent processing becomes unstable. SURFACE01 is a fixed-weight checklist semantic-stability study. Its baseline stop happened before any correction/adaptation, so it neither answers update-surface causality nor shows forgetting from a changed model.

**Exact question and type.** Before testing frozen-versus-adaptive recurrence and shared-versus-copied readout, can every fresh parent meet strict task competence and semantic-stability gates on controlled eight-flag histories that include idempotent events? Type: completed baseline execution with an all-parent admission stop. All four parent fits completed; three passed their own admission panel. Parent 4103 produced six false-DONE predictions in one connected history. Main correction/adaptation was not run and no main confirmation histories were generated.

**Model and task.** Four new `GRUCell(26,64)+Linear(64,9)` parents have 18,249 scalar parameters, initialized under seeds 4101–4104. Inputs are one-hot SET/CLEAR/RESET/NOOP and B-cue events; neither checklist mask, answer, nor valid-action list is supplied to the learner. Exact task routing, reset and no-op-aware labels are harness support, not learned abilities. Task A has eight completion flags and predicts lowest unfinished index 0–7 or DONE class 8. Task B maps eight cues to parity labels through the same nine-class head and zero state. Each parent trained for 2,000 Adam updates at lr .003 using equally weighted A/B cross entropy and global clip 1. Training streams were 32 events, batches equally covering mixed-edit, repeated/idempotent, revision and reset families. Every parent saw all 256 exact checklist masks. No no-op filtering was done.

**Protocol and gates.** Each parent received 64 admission histories per family (256 total), half interrupted after eight and half after 24 events, followed by a scored 32-event suffix. Main B correction would change one association per independent context only if all four parents passed. The fixed admission required, for every parent and every family, ≥99% event accuracy, ≥95% whole 32-event continuations, zero false DONE; plus all original B answers correct with true-class probability ≥0.80. Confirmation histories (8 per family/parent, long suffix) were gated on every parent and were never generated. A training/admission history/window-overlap check found no exact reused panel history or 32-token window; all admission generators reported zero overlap rejections. The test shares state-space semantics by design; new histories are not new state-space semantics.

| Parent seed | Correct A suffix events | Whole continuations | False-DONE events | Original B | Admission |
|---|---:|---:|---:|---|---|
| 4101 | 8,192/8,192 | 256/256 | 0 | 8/8, minimum p 0.99997211 | PASS |
| 4102 | 8,192/8,192 | 256/256 | 0 | 8/8, minimum p 0.99997494 | PASS |
| 4103 | 8,186/8,192 | 255/256 | 6 | 8/8, minimum p 0.99997555 | FAIL |
| 4104 | 8,192/8,192 | 256/256 | 0 | 8/8, minimum p 0.99997537 | PASS |

Across all four, descriptive rates were 32,762/32,768 suffix events and 1,023/1,024 whole continuations. Those large event/history denominators do not make four parent fits into thousands of replications. Parent 4103's idempotent family was 2,042/2,048 correct events and 63/64 complete histories; both accuracy thresholds passed. Its only family gate failure was the explicit zero-false-DONE rule.

**Connected failure retained.** In admission row 120, after interruption at event 8, parent 4103 first answered correctly at absolute event 16 when `SET(0)` made item 5 the next incomplete task. Then `SET(1), NOOP, NOOP, SET(3), SET(3), SET(3)` left exact mask 223 unchanged, with item 5 still pending. Predictions at events 17–22 said DONE, with assigned DONE probability rising from 47.8078% at event 17 to 99.4094% at event 22; at actual `SET(5)` event 23, DONE became correct (p=99.8736%). No parameter update occurred in this rollout. These are model softmax outputs, not calibrated real-world probabilities. The six false-DONEs are one connected failure episode, not six independent instances.

The state was not wholly absent from training: parent 4103 saw 49,823 exposures to mask 223, including 1,389 idempotent SET(1) operations with the same before/after mask. A fixed fitting diagnostic on 160 actual training streams from batches 1/500/1000/1500/2000 returned 5,115/5,120 correct events, 159/160 whole streams and zero false DONE. Neither number establishes full-corpus accuracy or a unique cause. Plausible explanations include history-dependent representation, objective/optimization or capacity; this run does not distinguish them.

**Gate consequence and unrun arms.** The protocol required all parents to pass, so 4103 stopped the cohort. No parent was removed/replaced, no fit extended, no threshold relaxed, no frozen-versus-adaptive comparison, no shared-versus-copied readout comparison and no main confirmation. The right statement is a baseline semantic-stability failure; the proposed weight-update hypotheses remain unanswered.

**Engineering and resource checks.** The independent free-running float32 GRU reference and class decisions passed numerical admission (3,588,096 coordinates, zero out-of-envelope, max absolute 9.059906e−06, max normalized ratio 0.774906 under `2e-6+2e-5*abs(reference)`). All eight injected faults and their clean controls passed; all 256 checklist masks × 18 commands were checked by the oracle. The source review reports that a fresh process replay matched all four admission panels and full hidden trajectories; this is the study's internal reproducibility evidence, not a replay run for this compendium. All 33 retained checkpoint files passed tensor-hash checks in the reported review. The work comprised 8,000 fixed parent optimizer applications, 48 engineering-probe applications (36 unique positions plus 12 repeated resume applications), and zero main B correction applications; total 8,048/10,096 authorized. The four fitted parents and 48 probes are distinct work categories. Main phase timing was 83.317850 seconds, preflight 7.738584s, replay 0.345339s; peak process RSS 367,435,776 bytes. These are scoped container observations, not energy, deployment latency, device qualification or broad efficiency evidence.

**Interpretation and limits.** A rare connected false-DONE episode is sufficient to fail an explicit strict gate; pooled accuracy cannot average it away. Because baseline admission failed, the original question of state/semantic stability under recurrent updates is not yet isolated from parent competence. The next useful question earned by this stop is what keeps an unfinished item represented correctly while other items and redundant events are processed. That exposed row is development evidence, not a future confirmation case. No architecture is selected.

**Sources.** `Research/NSS_NBR02_SURFACE01_Execution_v0.1.zip::NSS_NBR02_SURFACE01_Execution_v0.1/REPORT.md`; `...::protocol/EXECUTION_PROTOCOL.md`; `...::evidence/admission_4101_summary.json` through `admission_4104_summary.json`; `...::failures/parent_4103_idempotent_first.npz`; `Research/NSS_NBR02_SURFACE01_Reports_and_Review_v0.1.zip::REVIEW_AND_CANDIDATES.md`; `Research/NSS_Research_and_Architecture_Chat_Handoff_v1.1.md` (current status and evidence limit). The consolidation register terminates at E19; no R20 receipt is present in that archive, so none is cited.


<a id="pass-trace01"></a>

### TRACE01 — Guided replay from observed degradation

**Type and status:** Historical report-referenced result, marked `TECHNICAL_STOP_PARTIAL_CONFIRMATION` in checklist v0.19. This chapter did not rerun it. Its named original report was not present in the bounded source set.

**Broad question:** Can observed old-task degradation guide which examples or behaviors should be replayed, rather than applying a fixed replay set?

**Specific question:** Does degradation-informed selection produce a useful replay tradeoff relative to the corresponding replay reference, with numerical reliability and enough reserved confirmation to support a decision? The accessible excerpts do not provide the complete comparator list, algorithm, split, seeds or thresholds.

**Systems and arms:** The checklist and plan support the existence of a guided-replay diagnostic and mixed development tradeoffs. They do not identify every arm or supply enough method detail to reconstruct a per-arm table. No details from PROTECT01 or RECOVER01 are substituted for missing TRACE01 arm descriptions.

**Method and stopping:** The reported pass tracked degradation onset and evaluated guided replay. A **numerical failure** and a **storage stop** interrupted the planned confirmation, leaving **3/32 confirmation contexts**. Whether that count means three completed contexts, three remaining contexts, or the precise progress convention is not further specified in the compact status text; this chapter retains the stated wording and does not infer an achieved 3/32 result. Exact model/config, sampling policy, amount of replay, evaluation families, seeds, resource ceilings and stop trigger are unknown from the consulted sources.

**Reported outcome:** Development results were mixed; the numerical failure and storage stop left only the stated partial confirmation coverage. The next-action status is **no qualified guided-replay superiority**. There is no documented qualified win in the source excerpt and no basis to infer either universal failure of guided selection or its superiority over ordinary replay.

| Evidence item | Reported status |
|---|---|
| Degradation onset | Tracked |
| Guided-replay development tradeoff | Mixed |
| Numerical verification | Failure retained |
| Storage/confirmation | Stopped with only “3/32 confirmation contexts” recorded; exact progress interpretation unavailable |
| Decision | No qualified guided-replay superiority |

**Meaning and limits:** TRACE01 is a partial, technically stopped diagnostic. Its existence and status must be retained even though the original report is unavailable. Its metrics, controls, error cases and methodology remain unknown in the materials read here; the right summary is unresolved/partial evidence, not “never executed,” “failed all cases,” or “confirmed benefit.”

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §1 and source register S06 (names `NSS_NBR02_TRACE01_Report_v0.1.md`, describes guided-selection, numerical and storage/confirmation limits); checklist `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` and `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (status ledger). The named TRACE01 report was not found in the bounded workspace scan.


<a id="question-9"></a>

## 9. Can segmented or externally backed context support larger workloads?


<a id="pass-sh01"></a>

### SH01 — First shared typed-record / HSA maintenance reader

**Type and status:** Completed bounded learning and integration prototype; seven of eight scheduled fits completed. The three available paired seed comparisons were fully evaluated. Efficiency advantage was not established.

**Broad question and mapping:** Can an explicit hierarchical attention graph help a small maintenance reader learn a declared dependency rule from typed records, while an exact versioned context manager preserves provenance and supports restart? Maps to HSC-Q01–Q04 (interfaces, supplied hierarchy, cost, preservation); no direct `Gxx` mapping is stated in the source.

**Specific question:** Can a shared exact record/packet interface, dense and genuinely sparse hierarchical readers, and simple versus persistent packet management form an executable four-way comparison with auditable lifecycle and cost behavior?

**Systems and arms:**

- **Dense reader:** 18,500 trainable parameters; 37 engineered feature channels per record position; linear input projection to width 32; two residual attention/FFN blocks (two attention heads, FFN width 64), layer normalization and a four-class head. All parameters train.
- **HSA reader:** same architecture and paired initial parameters as dense, but sparse gather computes only selected graph edges. Task queries see their four local records, exact prerequisite records, own-region query anchors, all region anchors and the global anchor; regional and global metadata anchors have their own declared neighborhoods. Edges are supplied from exact dependencies, not learned retrieval or top-k routing.
- **Simple manager:** exact dependency index and eligible evidence selection; rebuilds each packet per request.
- **Persistent segmented manager:** same packet semantics and evidence selection; caches version-bound packets and invalidates on referenced-source changes.
- The integration crossed simple/persistent management with dense/HSA reading. The managers were required to emit byte-identical packet sequences, so that arm distinguishes reuse cost rather than evidence quality.

**Method, data, controls and resources:** Four paired fresh seeds 8801–8804, 600 AdamW updates per fit, same ordered 9,600 training worlds in 600 batches of 16 per fit, deterministic single-thread CPU, float32, no best-checkpoint selection. Frozen AdamW: learning rate .002, betas .9/.999, epsilon 1e-8, weight decay .01, gradient clipping 1.0, dropout zero. Train/dev/confirmation/stress generator seeds were 771001/771002/771003/771004; development used 32 worlds, then 256 fresh eight-task confirmation worlds (2,048 decisions/model) and 64 fresh sixteen-task stress worlds (1,024 decisions/model). Fingerprints were disjoint; task decisions within worlds and reuse of the same worlds across seeds are dependent. Per-fit descriptive target: at least 95% task accuracy and 90% macro recall. There was no dense retuning, refit or replacement fit after lock. Process cap: 900 seconds, 2.5 GiB RSS, 128 MiB evidence payload with 16 MiB reserve. An exact conventional rule scored as a capability control, not as a learned arm.

**Arm-by-arm results:** 8803/HSA stopped at its durable step-200 checkpoint after an external runner interruption. The interruption interval is bounded at 4,400–4,600 main optimizer applications overall, plus four disposable preflight applications; the exact first-process terminal time/RSS and the interrupted fit's unsaved suffix are unavailable. It was not relabeled complete, selected at step 200 or replaced. Complete-pair confirmation results:

| Seed | Dense correct / 2,048 | HSA correct / 2,048 |
|---|---:|---:|
| 8801 | 1,854 (90.527%) | 2,048 (100.000%) |
| 8802 | 1,842 (89.941%) | 2,038 (99.512%) |
| 8803 | 1,855 (90.576%) | unavailable; interrupted at step 200/600 |
| 8804 | 1,857 (90.674%) | 2,047 (99.951%) |

| Complete paired readers | Correct task decisions | Exact whole worlds | False COMPLETE |
|---|---:|---:|---:|
| Dense | 5,553/6,144 (90.381%) | 368/768 (47.917%) | 10 |
| HSA | 6,133/6,144 (99.821%) | 758/768 (98.698%) | 1 |

All three completed HSA fits met the per-fit target; none of the four dense fits did. Dense weakness centered on READY/BLOCKED discrimination (for example, seed 8801 classified only 52/210 READY correctly, with 158 called BLOCKED). HSA still erred: seed 8802 had eight BLOCKED→READY, one BLOCKED→COMPLETE and one READY→BLOCKED; seed 8804 had one COMPLETE→BLOCKED. On the separate sixteen-task stress panel, HSA scored 99.902%, 99.219%, and 100% for seeds 8801/8802/8804 (3,063/3,072 pooled). This is narrow length transfer, not language or new-rule generalization.

| Integration system | Correct decisions / 2,304 | Fully correct six-job outputs / 288 |
|---|---:|---:|
| Simple + dense | 2,187 | 204 |
| Persistent + dense | 2,187 | 204 |
| Simple + HSA | 2,304 | 288 |
| Persistent + HSA | 2,304 | 288 |

Both managers produced identical packet sequences and predictions. For each complete reader/seed, persistent management recorded 64 cache hits and 32 builds across 96 jobs; simple management rebuilt 96 times. These repeated jobs are not independent worlds and show no superadditive interaction between manager and reader.

| Reader latency, batch 1 CPU | Dense ms | HSA gather ms | HSA / dense | Padded score cells saved |
|---:|---:|---:|---:|---:|
| 8 tasks | 0.237 | 0.591 | 2.50× slower | 47.2% |
| 32 tasks | 0.588 | 1.371 | 2.33× slower | 81.5% |
| 128 tasks | 2.320 | 8.092 | 3.49× slower | 93.1% |

At 128 tasks, HSA still materialized 4,829,184 bytes of selected K/V payload per layer; fewer logical score cells did not yield lower latency. Total peak memory and energy were not measured as wins. In a six-job manager-only cycle, simple versus persistent medians were 1.417 vs .970 ms (8 tasks), 5.653 vs 3.677 ms (32), and 20.079 vs 14.009 ms (128), reducing source bytes decoded from 18,841→6,537, 74,979→25,253, and 300,429→100,401. The persistent manager snapshot at 128 tasks was 73,043 bytes versus 167 bytes for uncached management; both emitted 359,268 packet bytes, so reader traffic did not fall.

**Failures and evidence limits:** Initial SH01 preflight corruption contaminated fixtures because a supposed copied test object shared nested mutable objects. The failure and traceback were retained; deep-copy isolation fixed this before the source lock, and the corrected suite passed 664/664 assertions. Trained numerical checks covered a subset of confirmation worlds, not every trajectory. Independent replay matched 21 saved logit files and 21 scalar recounts; 30 checkpoint model hashes matched. The dense comparator was the installed optimized PyTorch SDPA path, not an intentionally slow dense implementation. No full archive/disk/network cost, natural language, tokenizer, 25,000-token workspace, generated summary, task-night lifecycle, changed-weight continuation, or whole-system qualification was tested.

**Meaning:** Evidence supports a useful supplied hierarchy for this fixed learned rule and a working exact record/packet contract. It does not show that the rule needs a neural model, that an optimized dense reader cannot catch up, that HSA is faster or lower total memory, or that the manager/model pair is a qualified NSS architecture.

**Source locators:** `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.md` §§3–5, 11, 14; outer consolidation report `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/sources/SH01/REPORT.md` (protocol at the corresponding `sources/SH01/PROTOCOL.md`, lock at `sources/SH01/SOURCE_LOCK.json`); original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_SH01_Execution_v0.1.zip::NSS_NBR02_SH01_Execution_v0.1/REPORT.md` (protocol and lock are in the same inner directory).


<a id="pass-sh02"></a>

### SH02 — Clean graph, plan, and packed HSA execution

**Type and status:** Completed engineering/refactor and saved-model regression; zero training, optimizer steps, new fits, or weight changes. Functional/tolerance parity passed on the declared checks; strict archival bitwise replay failed and remains recorded.

**Broad question and mapping:** Can the SH01 hierarchical reader be separated into a clear topology/compiler/backend API and execute the same learned operation with less redundant gather work? HSC-Q01, Q03 and Q04; no workspace `Gxx` mapping is stated.

**Specific question:** Can shared-neighborhood packing preserve the exact graph, joint softmax, features and outputs while improving HSA execution and retaining safe plans over restart?

**Systems and arms:** The trained 18,500-parameter SH01 HSA reader remained unchanged. **Old HSA** gathers K/V for each query row. **Packed HSA** groups the four task queries sharing one neighborhood and gathers K/V once; region/global anchors use a second bucket. **Full dense SDPA** is a measured cost comparison with a different graph, not equal-quality competitor. **Masked dense on the same graph** is the numerical reference, not a system arm. The bounded cache stores weight-independent topology plans only; it contains no learned activations or K/V state.

**Method and controls:** Preserve the SH01 37-feature inputs, dependency graph and three levels; check graph/compiler equality, plan serialization/restart, stale-plan rejection, numerical and gradient equality, and zero class changes for all retained decisions across three complete HSA finals. The old interrupted 8803/HSA fit was not completed. Timing ran one CPU thread and identical seed-8801 HSA weights/inputs, with five warmups and 31 interleaved repetitions. Shapes: 8/32/128/512 tasks, batch 1, plus batch 16 at 8/32/128. Process cap 2 GiB, evidence cap 128 MiB. These are regression and execution checks over previously exposed fixtures, not new held-out learning or confirmation data.

**Results:** The locked engineering suite passed 92/92 case checks. Across 623,800 engineering scalars and 2,918,400 saved-model/stage scalars, no declared numerical-envelope breach occurred. Every one of 9,984 retained task decisions across development/confirmation/stress for HSA seeds 8801, 8802 and 8804 stayed in the same class. The underlying reader errors persisted. Split-level recount:

| Model | Split | Correct / decisions | Whole worlds correct | False COMPLETE | Changed classes |
|---|---|---:|---:|---:|---:|
| 8801 | development | 256/256 | 32/32 | 0 | 0 |
| 8801 | confirmation | 2,048/2,048 | 256/256 | 0 | 0 |
| 8801 | stress | 1,023/1,024 | 63/64 | 1 | 0 |
| 8802 | development | 256/256 | 32/32 | 0 | 0 |
| 8802 | confirmation | 2,038/2,048 | 247/256 | 1 | 0 |
| 8802 | stress | 1,016/1,024 | 56/64 | 0 | 0 |
| 8804 | development | 256/256 | 32/32 | 0 | 0 |
| 8804 | confirmation | 2,047/2,048 | 255/256 | 0 | 0 |
| 8804 | stress | 1,024/1,024 | 64/64 | 0 | 0 |

| Tasks, batch 1 | Old HSA ms | Packed HSA ms | Full dense ms | Old / packed |
|---:|---:|---:|---:|---:|
| 8 | .6226 | .7934 | .2663 | .78× (packed slower) |
| 32 | 1.7751 | 1.2772 | .5324 | 1.39× |
| 128 | 9.5426 | 2.5691 | 1.9619 | 3.71× |
| 512 | 71.2465 | 12.6545 | 19.5640 | 5.63× |

Packed HSA improved on old HSA at 32/128/512 tasks, but lost at 8 tasks; versus full dense it won only at 512 in this measured set. The 512-task case is cost-only, not learned-competence testing. Batch-16 old/packed/full-dense timings (ms) were 8 tasks: 4.5942/2.6222/1.0156; 32: 20.4133/9.5186/4.6354; 128: 238.6076/69.5437/29.7374. Full dense stayed faster in all measured batch-16 shapes. Packed K/V payload per layer was 41,984/210,944/1,189,888/7,755,776 bytes at 8/32/128/512 tasks, down about 75% from old HSA, but this excludes total process memory, attention workspaces and other buffers.

Plan-build / feature-spec / warm-cache lookup / full cold-pipeline medians (ms) were: 8 tasks .1724/.1443/.0111/1.1789; 32 .3495/.3044/.0114/1.7587; 128 1.0362/.9391/.0154/4.5051; 512 5.5831/3.5550/.0348/20.1825.

**Failures and evidence limits:** All nine historical archive logit files differed in least-significant values even when the unchanged legacy SH01 source and weights ran in the current runtime. Maximum absolute difference was 2.38418579e-06; admitted tolerance and class checks passed. The strict bitwise driver therefore exited 1; cause remains unresolved. A post-result replay using SH01's full-batch-then-slice convention did not remove the mismatch. Two new cleaned-path processes reproduced all nine new output files bitwise. The first cost driver hit a 20-second caller timeout after six of seven conditions; a separately identified continuation completed the last condition. These are report-level diagnostics; no current rerun was made.

**Meaning:** Packing removes redundant K/V gathering and makes medium/large HSA execution substantially faster than the previous gather implementation. It did not make HSA universally faster than full dense attention and does not claim lower total memory, energy, or full-maintenance cost. The historical numerical bitwise miss is distinct from admitted numerical tolerance and unchanged classes.

**Source locators:** consolidation `.md` §§6, 11, 14; outer report `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/sources/SH02/REPORT.md` (architecture and protocol are in `sources/SH02/`); original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_SH02_Execution_v0.1.zip::NSS_NBR02_SH02_Execution_v0.1/REPORT.md` (architecture, protocol and source lock are in the same inner directory).


<a id="pass-sc01"></a>

### SC01 — Exact backward-closure segmented workspace

**Type and status:** Completed bounded component, all 324 main conditions complete; no training or new fits. Same-class and numerical-parity checks passed. The efficiency increment over strong ordinary caching was modest and workload dependent.

**Broad question and mapping:** Can typed maintenance work be split into bounded packets without dropping information needed by the unchanged two-layer model, while tracking revisions, resumable jobs and cost against a strong cache baseline? HSC-Q01, Q05–Q08; no workspace `Gxx` mapping is stated.

**Specific question:** Can a bounded active-row workspace preserve the full SH02 computation over complete backward closures, resume interrupted work, invalidate stale results, and add value beyond indexed retrieval and conventional caching?

**Systems and arms:** All three use the unchanged SH02 hierarchy/weights, 37 engineered features, exact three-level graph, common durable progress/receipt semantics and 16-entry topology-plan cache. **INDEX** performs exact retrieval in request order, greedy cap-fitting groups, without transient source or neural-result memo. **CACHE** adds bounded LRU source-row and per-task neural-result caches, recomputing full source-version dependency fingerprints on lookup. **SEGMENT** has the same capacities but invalidates from explicit revision events and orders pending tasks by overlap of required rows; after restart it revalidates fingerprints. These are competing management policies, not different learned readers.

**Method, data and criteria:** Input for each requested task is its exact two-layer backward dependency closure, retaining original row IDs and one joint softmax; oversized closure defers explicitly rather than truncating. Seeds 932101/932102, world sizes 8/32/128, six episode families (reuse, sweep, churn, revisions, resume, oversize), 36 episodes and 324 model-policy conditions across checkpoints 8801/8802/8804. Caps 40/128/384 input rows; oversize caps 16/32/128; source/result caches 32 entries. Batch-1 single-thread CPU timing used seed 932101, model 8801, one warmup and nine shuffled interleaved repetitions per method/workload over reuse/sweep/churn/resume. Active rows are not a total-memory bound or a language-token budget. Budget/restart/planner/parser/cache/reader and receipt costs were counted in the timed episode core; disk/network latency was not.

**Correctness, closure, and work outcomes:** Across 26,604 available answer observations, there were zero changed classes relative to full SH02; across 106,416 scores, zero tolerance breaches. There were 3,294 full request occasions, 54 deliberate partial requests with work preserved, 648 undersized request occasions yielding 5,184 explicit deferred attempts, no duplicate receipts, and peak active rows 36/126/383. The unchanged neural model made mistakes: 2,903/2,940 correct at 8 tasks, 2,964/2,964 at 32, and 2,955/2,964 at 128 (98.7415%, 100%, 99.6964%); zero false COMPLETE in this observed panel. CACHE and SEGMENT produced exactly the same class counts as INDEX. These observations reuse two initial layout seeds and repeated answers.

| Tasks | Full rows | One-task exact closure range | All task-query metadata needed? |
|---:|---:|---:|---|
| 8 | 36 | 24–36 | yes |
| 32 | 135 | 66–96 | yes |
| 128 | 524 | 209–254 | yes |

| Tasks | Policy | Sliced reader calls | Reader input rows | Archive rows fetched | Reused result observations |
|---:|---|---:|---:|---:|---:|
| 8 | INDEX | 372 | 13,356 | 13,356 | 0 |
| 8 | CACHE | 120 | 4,221 | 1,344 | 2,151 |
| 8 | SEGMENT | 120 | 4,221 | 1,344 | 2,151 |
| 32 | INDEX | 804 | 92,763 | 92,763 | 0 |
| 32 | CACHE | 204 | 23,220 | 6,837 | 2,139 |
| 32 | SEGMENT | 189 | 20,862 | 6,948 | 2,139 |
| 128 | INDEX | 876 | 298,896 | 298,896 | 0 |
| 128 | CACHE | 249 | 79,770 | 30,549 | 1,851 |
| 128 | SEGMENT | 243 | 76,212 | 27,564 | 1,851 |

Most work reduction came from ordinary result/source reuse. SEGMENT matched CACHE at 8 tasks; at 32 tasks it fetched slightly more archive rows despite fewer reader rows. At 128 tasks its greedy policy sometimes caused more reader calls than CACHE: 3 vs 2 in reuse, 14 vs 13 in churn, 5 vs 4 in resume.

| Tasks | Workload | INDEX ms | CACHE ms | SEGMENT ms | SEGMENT saving vs CACHE |
|---:|---|---:|---:|---:|---:|
| 8 | reuse | 19.229 | 5.103 | 4.142 | 18.83% |
| 8 | sweep | 18.447 | 5.254 | 3.928 | 25.24% |
| 8 | churn | 22.814 | 23.836 | 21.852 | 8.32% |
| 8 | resume | 25.976 | 11.225 | 9.990 | 11.00% |
| 32 | reuse | 76.237 | 11.179 | 8.914 | 20.26% |
| 32 | sweep | 29.639 | 16.228 | 15.100 | 6.95% |
| 32 | churn | 76.823 | 40.636 | 38.477 | 5.31% |
| 32 | resume | 90.515 | 22.548 | 24.195 | -7.31% |
| 128 | reuse | 126.644 | 23.312 | 20.852 | 10.55% |
| 128 | sweep | 75.015 | 72.593 | 71.985 | 0.84% |
| 128 | churn | 156.717 | 78.592 | 74.583 | 5.10% |
| 128 | resume | 184.679 | 47.335 | 44.987 | 4.96% |

**Failures and limits:** A pre-lock JSON precision-checker bug selected float64 tolerance from the container type for float32-computed scores and failed four assertions; the error/source were retained, comparator fixed before source lock using computation precision, and the suite rerun. A 20-second call interrupted the 8-task sweep timing; a 60-second call interrupted 128-task sweep timing; separately identified continuations completed only missing resume conditions, leaving some unsaved inference work unknown. Main-process RSS was 329,707,520 bytes. The full exact archive remained in RAM; no filesystem, network, semantic memory, long-term history, trained segmentation, learned record writing, changed-weight continuation or total process-memory bound was tested.

**Meaning:** Full dependency closure and explicit deferral preserved the same learned outputs over the bounded fixtures. Conventional caching supplied most savings; SEGMENT was faster than CACHE in 11/12 timed cells but lost by 7.31% on 32-task resume and had only a 0.84% measured edge in 128-task sweep. No claim of broad or robust superiority follows from this single CPU timing environment.

**Source locators:** consolidation `.md` §§7, 11, 14; original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_SC01_Execution_v0.1.zip::NSS_NBR02_SC01_Execution_v0.1/REPORT.md` (protocol, architecture, outcome and source lock are in that inner study directory).


<a id="pass-sc02"></a>

### SC02 — Incremental publication, scheduling, and neural-cache ablation

**Type and status:** Completed bounded incremental-engineering study; all 720 main conditions and 20 timing cells finished. No optimizer applications, new fits or weight changes. Numerical/class equivalence passed. The additional first-layer neural cache was slower in all timing cells.

**Broad question and mapping:** Can selective source recompilation and query planning reduce the end-to-end cost of versioned segmented maintenance, and does a neural intermediate cache repay its costs? HSC-Q05–Q07; no workspace `Gxx` mapping is stated.

**Specific question:** Which cost reductions survive a fair contemporaneous comparison among SC01's cache/scheduler and vectorized publication, graph/signature reuse, scheduling and first-layer output caching?

**Systems and arms:** Same SC02/SH02 three-level graph, 37 features, 18,500 parameters, fixed weights 8801/8802/8804 and active-row caps. **C** is unchanged SC01 conventional cache/request order. **S** is unchanged SC01 event invalidation plus greedy overlap scheduling. **F** applies exact vectorized initial/restart compilation, changed-row source updates, graph reuse and exact signatures with complete version-tuple checks, but retains conventional request order. **P** combines F with event invalidation and compares request-order and overlap packings lexicographically by group count, closure rows and first-block output rows; ties favor request order. **I** adds to P a bounded model-bound cache of exact first-layer output rows, each validated against the full neighborhood's source versions. The cache holds no second-layer results and does not migrate across changed weights. C/S/F/P/I all receive the same facts, result-cache capacity and 16-entry plan cache.

**Method, data and resources:** 48 fresh episodes: 8/32/128 tasks × seeds 942201/942202 × eight families (reuse, sweep, churn, revisions, resume, oversize, eviction, global), run under three retained checkpoints and five arms = 720 conditions. Every arm ran the same fixture events. Caps were 40/128/384 rows; cache capacity 32 except four-entry eviction stress. Correctness had 61,620 answer observations and 246,480 score-scalar comparisons. Timing used model 8801, seed 932101, one warmup and 11 interleaved repetitions per arm/workload for 12 cells; a fresh seed 942203 added eight 32/128-task cells with seven repetitions. Timed cores included archive ingestion, publication, grouping, validation, reader work, source changes, receipts and JSON checkpoint reconstruction, but excluded process/model startup, disk durability and full-reference scoring. Full archive remained RAM-resident. Main resource was 4,803 sliced reader calls and 2,160 full-reference forwards; peak RSS 333,176,832 bytes. Unknown inference work from caller-interrupted process is not added to exact totals.

**Correctness and aggregate results:** Each arm returned 12,324 answers and was correct 12,199 times (98.9857%); all arms preserved identical underlying reader mistakes, with no false COMPLETE on this panel. There were zero changed classes, zero numerical-envelope breaches, maximum absolute difference 4.053115845e-06, no duplicate receipts, max active rows 36/126/383, and 1,728 undersized-budget attempts explicitly deferred per arm. Total unresolved observations were 1,884 per arm, including intentional interrupted positions. Exact source truth/status/labels/signatures matched at 576 paired comparisons. These are repeated fixture conditions, not independent models or 61,620 independent draws.

| Tasks | Workload | C: SC01 cache | S: SC01 segmented | F: fast cache | P: planned segments | I: P + neural cache |
|---:|---|---:|---:|---:|---:|---:|
| 8 | reuse | 2.888 | 2.084 | 2.406 | 2.395 | 2.730 |
| 8 | sweep | 2.972 | 2.119 | 2.511 | 2.313 | 2.706 |
| 8 | churn | 14.897 | 13.749 | 12.081 | 13.441 | 14.041 |
| 8 | resume | 6.712 | 6.029 | 7.222 | 6.998 | 7.241 |
| 32 | reuse | 6.799 | 4.883 | 4.716 | 4.291 | 5.836 |
| 32 | sweep | 10.104 | 8.437 | 7.868 | 8.326 | 9.449 |
| 32 | churn | 23.632 | 20.939 | 16.849 | 16.367 | 18.310 |
| 32 | resume | 14.863 | 13.144 | 13.757 | 12.939 | 14.959 |
| 128 | reuse | 15.350 | 13.181 | 9.279 | 8.909 | 11.116 |
| 128 | sweep | 47.335 | 47.788 | 35.073 | 37.414 | 44.213 |
| 128 | churn | 52.360 | 49.490 | 26.532 | 28.925 | 30.791 |
| 128 | resume | 36.427 | 33.819 | 27.451 | 26.884 | 30.763 |

Medians in milliseconds; ordering is C/S/F/P/I. P beat S in 9/12 primary cells (equal-cell geometric time ratio .88585, 11.4% lower), but it was slower on three non-churn 8-task cells: reuse (2.395 vs 2.084 ms), sweep (2.313 vs 2.119 ms), and resume (6.998 vs 6.029 ms). It was faster on 8-task churn. P and F were near tied in the primary grid (geometric ratio .99581), with cell-level wins and losses.

| Tasks | Fresh workload (seed 942203) | C | S | F | P | I |
|---:|---|---:|---:|---:|---:|---:|
| 32 | sweep | 11.260 | 9.877 | 9.821 | 10.790 | 11.887 |
| 32 | churn | 35.222 | 29.176 | 26.245 | 23.300 | 26.039 |
| 32 | resume | 15.631 | 13.833 | 13.702 | 14.155 | 15.519 |
| 32 | revisions | 16.575 | 12.780 | 12.890 | 11.316 | 14.745 |
| 128 | sweep | 44.408 | 47.505 | 36.612 | 37.274 | 44.849 |
| 128 | churn | 66.675 | 55.691 | 36.791 | 32.029 | 33.906 |
| 128 | resume | 39.149 | 31.443 | 29.029 | 27.864 | 30.965 |
| 128 | revisions | 39.921 | 26.599 | 25.844 | 21.770 | 26.691 |

P beat S in six of eight fresh cells and F in five; it was 2.3% slower on fresh 32-task resume and 9.2% slower on fresh 32-task sweep. Geometric P/S time ratio was .84450 (15.6% lower), but these are small single-CPU medians, not confidence bounds or a deployment-weighted prediction. P saves 12.782→.298 ms of source-publication time on the retained 128-task churn fixture versus S; F receives the same source-update improvement. Across fresh main episodes, C/S/F/P/I issued 987/945/987/942/942 sliced-reader calls, so scheduling saved only three calls from S in aggregate (45 against request-order F).

I reused 28,800 of 61,344 first-layer demands (46.95% fewer fresh rows; encoder rows fell 174,588→113,412) but was slower than P in all 20 timing cells, about 14.7% slower on the retained grid and 15.0% on fresh. Its extra numeric cache was at most 49,152 bytes; validity JSON peaked 55,717 bytes and additional partial-plan tensors 75,036 bytes. These are separately reported payload peaks, not simultaneous RSS.

**Failures and limits:** A 90-second caller timeout interrupted one main command after 233/240 128-task conditions were durable; a separately identified driver ran only seven missing conditions without changing existing hashes. Main measurements are complete; unsaved inference work and first-process RSS/time are unknown. Engineering passed 34 checks. Independent recount matched all 720 cases; 576 semantic comparisons matched; 36 fresh-process P/I replays and 24 saved-workspace resumes reproduced traces bit-for-bit. This is internal consistency, not independent replication. The exact archive, long-lived history, native storage/device performance, energy, total maintenance-night cost and language tokens remain untested.

**Meaning:** Incremental publishing and graph/signature reuse produced useful engineering savings in selected changing-record workloads; adding the scheduler helped sometimes and lost elsewhere; the neural cache is a measured negative. The benefit is not unique to a “segmented” category because ordinary F shares the core incremental engineering gain.

**Source locators:** consolidation `.md` §8 and §§11,14; original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_SC02_Execution_v0.1.zip::NSS_NBR02_SC02_Execution_v0.1/REPORT.md` (architecture, protocol, outcome and source lock are in that inner study directory).


<a id="pass-cap01"></a>

### CAP01 — Exact computation across active record tiles

**Type and status:** Completed bounded capacity diagnostic, all 488 planned cases complete. Ordinary multi-pass retrieval and hierarchy-grouped segment execution preserve the same outputs; learned large-layout errors remain.

**Broad question and mapping:** Can one exact attention calculation finish when its input closure exceeds the simultaneously resident packet, and does custom grouping add capability over ordinary streaming? HSC-Q08–Q10; no workspace `Gxx` mapping is stated.

**Specific question:** Can the two-block HSA reader carry a single joint-softmax calculation across 32-position active tiles, retain exact dependencies, resume after interruption, and make valid predictions with the newly accessible evidence?

**Systems and arms:** Same three retained SH01 reader seeds 8801/8802/8804, both dense and HSA weights (six models total), 37 typed features, 18,500 parameters, two blocks, and original task/region/global graph. **Ordinary multi-pass retrieval** groups consecutive query rows; **hierarchy-grouped segmentation** groups queries with matching graph neighborhoods. Both use exact backward closure, identical key ordering, multi-pass arithmetic, external file-backed intermediates, and checked resume. The attention calculation preserves running global maximum, denominator, weighted-value sum: one joint softmax over the original full key set. The resident full dense/HSA source execution is the same-weight reference, outside the active cap. Exact symbolic rule execution is a ceiling/control; resident-packet closure admission is a separate control that marks oversized cases unadmitted, not a truncated baseline.

**Method, data, criteria and resources:** Primary grid: 8/32/128 tasks × two base worlds/size × three scenarios (cross-region dispersed prerequisites, global freeze override, dependency revision after interruption) × two snapshots × three model seeds × two reader types × two managers = 432 cases, active cap 32. Stress at 512 tasks used one base world, three scenarios/two snapshots, only seed 8801, two readers and two managers = 24. Tile sensitivity at 128/512 used one separate base per size, dispersed scenario/two snapshots, seed 8801, both readers/managers at caps 16/64 = 32. Total 488 cases, 3,904 task observations including repeated arms. Main descriptive working-point criteria were at least 95% decision accuracy, 90% represented-class macro recall and 90% wholly correct eight-answer jobs. Single-run cost profiles are secondary, not repeated timing evidence. Process cap 2 GiB/900 seconds, evidence guard 240 MiB within 256 MiB; no optimizer work.

**Arm-by-arm results:** The non-freeze table excludes easy all-DEFER overrides; ordinary and segmented policies had identical class results.

| Source tasks | Encoded positions | Dense correct / selected decisions | HSA correct / selected decisions | Dense exact jobs | HSA exact jobs |
|---|---:|---:|---:|---:|---:|
| 8 primary | 36 | 204/240 (85.000%) | 240/240 (100%) | 6/30 (20%) | 30/30 (100%) |
| 32 primary | 135 | 225/240 (93.750%) | 240/240 (100%) | 15/30 (50%) | 30/30 (100%) |
| 128 primary | 524 | 188/240 (78.333%) | 235/240 (97.917%) | 3/30 (10%) | 25/30 (83.333%) |
| 512 stress, one parent | 2,072 | 16/40 (40%) | 35/40 (87.500%) | 0/5 | 0/5 |

With frozen controls included, dense/HSA correct counts were 252/288 vs 288/288 (8 tasks), 273/288 vs 288/288 (32), 236/288 vs 283/288 (128), and 24/48 vs 43/48 (512). The 512 row is a distinct one-pair stress, not a three-parent primary estimate; 128 misses the whole-job target and 512 fails the working-point targets.

| Tasks | Full encoded positions | HSA single-target full-closure range | Active cap |
|---:|---:|---:|---:|
| 8 | 36 | 30–36 | 32 |
| 32 | 135 | 69–96 | 32 |
| 128 | 524 | 218–260 | 32 |
| 512 | 2,072 | 602–755 | 32 |

Thus for 32+ tasks no selected HSA target's full original closure fits the 32-row tile; both streaming policies nevertheless completed exact calculations without truncation. At 512 they processed 2,072 encoded positions through external intermediates. This does not mean the 32-position tile stores all task meaning or caps total memory.

| Tasks | Dense score cells | HSA score cells | Dense core seconds | HSA core seconds |
|---:|---:|---:|---:|---:|
| 8 | 3,168 | 1,456 | .0124 | .0215 |
| 32 | 38,610 | 4,398 | .0419 | .0253 |
| 128 | 557,536 | 12,010 | .5097 | .0821 |
| 512 | 8,619,520 | 28,316 | 6.4958 | .1558 |

These are one measured first-snapshot dispersed-job cost observations using the segmented grouping policy, not repeated performance benchmarks; readers/graphs also differ. They exclude full research preparation/audit. At cap 32, maximum counted live attention-tensor payload was 17,936 bytes but this is partial named-tensor accounting, not total working memory or peak RSS. Peak process RSS was 383,250,432 bytes. Source plus embedding and stage arrays occupied 19,664/72,332/279,280/1,102,816 bytes at 8/32/128/512 tasks.

**Failures and audits:** HSA's five non-frozen errors at 128 tasks were all parent 8802 / target 124 repeated across scenarios/snapshots (one unresolved- prerequisite false READY pattern); the 512 HSA stress error repeats target 386 for seed 8801 across five jobs. Full resident references make the same errors, so streaming did not cause them. In tile sensitivity at 128, seed 8801 gave 14/16 correct at caps 16 and 64; at 512 it gave 16/16 at each cap on a different world. Those tiny, different-layout sensitivities do not reverse the poorer primary 512 result. All 488 cases and all 3,904 class decisions matched full same-weight inference; 4,078,784 scalar comparisons had zero tolerance violations (max absolute 1.04904175e-5, max envelope ratio .190267); 244 manager pairs preserved results. There were 152 paused cases saved at seven tiles, all 76 old-source resume attempts explicitly rejected after source change, then fresh computation restarted under new binding. Engineering passed 29 cases, selected fresh-process replays covered 40 final and all 14 retained pauses; independent scorer recounts agreed. These are internal audits, not third-party replication.

**Meaning:** This demonstrates executable input reach beyond the old resident closure and exact answer preservation through ordinary or hierarchy-grouped multi-pass arithmetic. Custom grouping added no unique capability. HSA is more accurate than these retained dense checkpoints on some layouts, but that comparison inherits a weaker dense training recipe; it is not an optimized dense ceiling. Larger task count changes distractors/context, not rule depth, and does not establish natural language or transitive reasoning.

**Source locators:** consolidation `.md` §§9, 11, 14; original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_CAP01_Execution_v0.1.zip::NSS_NBR02_CAP01_Execution_v0.1/REPORT.md` (protocol, outcome and source/fixture lock are in that inner study directory).


<a id="pass-cap02"></a>

### CAP02 — Mixed-size preparation with small-task retention

**Type and status:** Completed bounded preparation study; 1,152 main optimizer applications, three disposable preflight applications, 12 continuation branches from six exact parents. Component parked for integration after one fixed follow-up; no tuning loop.

**Broad question and mapping:** Can broader training preparation improve interpretation on larger layouts without damaging the narrow small-layout task? HSC-Q10–Q11; no workspace `Gxx` mapping is stated.

**Specific question:** Does training the fixed HSA/dense reader over mixed 8/32/128-task layouts improve fresh larger-layout answers relative to unchanged parents and small-only practice, while retaining small-task performance?

**Systems and arms:** Each of six CAP01 checkpoints (dense/HSA × seeds 8801/8802/8804) had **U**, untouched; **S**, 96 additional updates on 8-task worlds only; and **M**, 96 updates cycling 8/32/128-task worlds. All are same-size continuation branches, not new random fits. Model remains 37 features, 18,500 parameters, two attention blocks and same three-level graph. Every update uses four worlds × eight selected decisions = 32 labels/update; 3,072 labels per continuation. Matching eight-task steps use identical data. Fresh AdamW per branch, learning rate .0005, weight decay .01, betas .9/.999, epsilon 1e-8, clipping 1.0, no schedule, early stop or checkpoint selection; only final step 96 evaluated. Equal steps/labels do not equalize FLOPs, evidence or runtime because M uses larger source records.

**Method and data:** Training uses 640 unique worlds; each curriculum presents 384 worlds with 128 shared. Confirmation consists of 32 fresh non-freeze worlds plus eight frozen controls at each of 8/32/128 tasks; 512-task stress uses eight non-freeze worlds and two frozen controls. The same 130 worlds are evaluated across endpoints. Primary metrics select eight targets per world, giving 768 HSA or dense decisions and 96 eight-answer jobs per size/arm; 512 gives 192 decisions/24 jobs. Shared worlds across arms/parents are paired repeated observations. Mixed preparation trains only through 128 tasks; 512 is beyond-training-size stress. All-task outputs were retained separately. After training, all six M endpoints were tested with CAP01 exact 32-position streaming on first non-freeze 32/128-task confirmation worlds; 12 compatibility checks, not all-world qualification. Main resource: 22.073 seconds in reported command cores, peak RSS 399,749,120 bytes; source/fixture prep, preflight, audit and packaging are additional.

**HSA results (non-freeze selected answers; easy all-DEFER controls excluded):**

| Tasks | U unchanged | S small-only | M mixed-size | Whole jobs U → M |
|---:|---:|---:|---:|---:|
| 8 | 767/768 (99.870%) | 768/768 (100%) | 768/768 (100%) | 95/96 → 96/96 |
| 32 | 762/768 (99.219%) | 767/768 (99.870%) | 767/768 (99.870%) | 91/96 → 95/96 |
| 128 | 749/768 (97.526%) | 730/768 (95.052%) | 766/768 (99.740%) | 80/96 → 94/96 |
| 512 stress | 175/192 (91.146%) | 177/192 (92.188%) | 189/192 (98.438%) | 11/24 → 21/24 |

| Seed parent at 128 | U | S | M |
|---|---:|---:|---:|
| 8801 | 242/256 | 220/256 | 256/256 |
| 8802 | 252/256 | 254/256 | 255/256 |
| 8804 | 255/256 | 256/256 | 255/256 |

M improved over U in two parents and tied in one; versus S it improved two and was one answer worse in one. At 128, selected errors fell 19→2 and correct whole jobs rose 80/96→94/96. M meets the descriptive 95% decision / 90% macro recall / 90% whole-job points through 128; at 512 its 87.5% whole-job result misses the criterion despite 98.438% selected accuracy. M retained the small task perfectly (768/768 decisions, all 96 jobs). Two new 128 selected errors remain: one false BLOCKED on completed work (8802), one false COMPLETE on a blocked task (8804). Three false READY outputs remain at 512. At 128, HSA full-all-task secondary checks improved U 11,962/12,288 (97.347%)→M 12,275/12,288 (99.894%); at 512, 11,178/12,288→12,083/12,288.

| Dense tasks | U | S | M | M exact jobs |
|---:|---:|---:|---:|---:|
| 8 | 694/768 (90.365%) | 698/768 (90.885%) | 692/768 (90.104%) | 42/96 |
| 32 | 655/768 (85.286%) | 654/768 (85.156%) | 654/768 (85.156%) | 29/96 |
| 128 | 592/768 (77.083%) | 604/768 (78.646%) | 624/768 (81.250%) | 26/96 |
| 512 stress | 111/192 (57.812%) | 101/192 (52.604%) | 136/192 (70.833%) | 1/24 |

Dense got the same continuation examples/labels; its accuracy improved on some sizes but remains far below HSA under this fixed recipe. The source dense parents were already weaker after SH01; this does not establish that dense attention cannot learn the task.

**Streaming compatibility, failures and gates:** All 12 post-learning CAP01 checks finished with zero class differences and zero breaches across 89,952 scalar comparisons (max absolute 6.198883056640625e-6), still at the 32-position cap. Twelve HSA continuations were evaluated over all 130 worlds; independent recount and fresh-process replay found zero discrepancies (2,340 endpoint/world records; 60 checkpoint parameter hashes/parent links matched). The only defect was a pre-lock syntax error in the evaluation record writer; two rejected parse attempts and source failure were retained; it was fixed before preflight/model activity. No main interruption, criterion/gate relaxation, replacement, extra update or post-result tuning occurred.

**Meaning:** Mixed-size preparation improved the fixed HSA rule on 128-task layouts while retaining 8-task performance, making this a positive bounded preparation result. The benefit is not uniform in every parent and still leaves 512 whole-job performance below the working point. It does not test language record preparation, new rules, general retention, identity or full NSS lifecycle. It was enough to park further polishing of this subproblem.

**Source locators:** consolidation `.md` §§10–13; original report nested at `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip::NSS_HSA_Segmented_Context_Research_Consolidation_v1.0/original_archives/NSS_NBR02_CAP02_Execution_v0.1.zip::NSS_NBR02_CAP02_Execution_v0.1/REPORT.md` (protocol, outcome and source/fixture lock are in that inner study directory).


<a id="question-10"></a>

## 10. Can another writer improve on autoregressive output?


<a id="pass-darp01"></a>

### DARP01 — First token-level plan / check / edit writer

**Type and status:** Completed bounded model experiment; nine prescribed models reached final endpoints. The token-level masked-diffusion mechanism was implemented, but the planned DARP competence working point was not met. The source used for this compendium is the consolidated DOCX report; the named execution ZIPs were not opened or independently recounted in this review.

**Broad question and mapping:** Can a segmented diffusion writer make sequentially presented, checked maintenance records, and does it help relative to an autoregressive writer under the same workflow support? The DARP consolidation uses its own editorial question map, not a workspace `Gxx` mapping.

**Specific question:** Can a trained writer construct a maintenance plan, revise it against changed evidence, and repair erroneous output blocks when supplied exact fault localization and up to two repairs?

**Systems and arms:** Common model: two-layer prefix Transformer, hidden width 48, four attention heads, 58,354 learned parameters, vocabulary 82. The closed fixture supplies a 27-token typed JSON evidence array and expects three 17-token record arrays (51 tokens total): plan, state, and continuation. **AR** generates causal next tokens, recomputing prefixes. **DARP** denoises the current block bidirectionally over four reverse steps then checks/commits sequentially. **WHOLE** (DARP01 only) denoises the whole 51-token output before document commitment. DARP training masks positions at .25/.5/.75/1 and uses cross-entropy on masked targets; reverse steps reveal masked positions with probability 1/k for k=4,3,2,1. All writers receive the same evidence, exact fault locations, task-specific checker and at most two repairs; correct fields may be hard-copied under guidance. The checker supplies no replacement values but does know the synthetic rule. Checker and copying are software assistance, not learned self-validation or learned noninterference.

**Method, data and resource limits:** Three paired seeds 11101/11102/11103, each AR/DARP/WHOLE initialized from matched tensors, nine fresh fits ×900 logical updates =8,100 logical. Training: 4,096 materialized worlds, same ordered batches of eight worlds/update, three targets/world; AdamW cosine .001→.0002, weight decay .01, clipping 1, one CPU thread, no dropout. Half of training instances contain corrupted drafts and negative localization. Static confirmation: 48 fresh worlds, disjoint complete inputs from training; injected/revision families reuse 24 of those worlds rather than adding independent cases. Working point: ≥44/48 static guided complete handoffs in at least two of three DARP seeds. Report records 1,872 episode outputs across models, policies and ablations. Exact source, rule interpreter, malformed/stale/false-complete/conflict checks, gradient/numerical/causal tests and bounded snapshot/replay tests are documented; this compendium did not rerun them.

**Results by generation arm:**

| Guided static outcome | AR | DARP | WHOLE |
|---|---:|---:|---:|
| Complete handoffs | 5/144 | 21/144 | 0/144 |
| Token accuracy | 90.97% | 87.28% | 83.05% |
| Valid JSON | 144/144 | 144/144 | 144/144 |
| Correct plans | 8/144 | 34/144 | 2/144 |
| False-completion drafts | 6 | 31 | 30 |

DARP successes by seed were 0/48, 1/48, and 20/48; none met the 44/48 working point. High punctuation-heavy token accuracy and legal JSON did not yield reliable, evidence-grounded handoffs.

| Feedback / repair outcome | AR | DARP | WHOLE |
|---|---:|---:|---:|
| Static unguided → guided complete handoffs | 5 → 5 / 144 | 21 → 21 / 144 | 0 → 0 / 144 |
| Injected unguided → guided complete handoffs | 1 → 2 / 72 | 9 → 8 / 72 | 0 → 0 / 72 |
| Initially wrong units fully repaired | 7/417 blocks | 6/346 blocks | 0/144 documents |

All writers/policies scored 0/66 on revision worlds that actually changed the action plan; DARP's two guided revision successes were unchanged-action worlds. The initial-plan training interface always provided an empty prior-plan slot while revision inference included an old plan. This coverage gap was observed but not isolated causally. AR had all substantive fields correct in 100/144 cases but all identity/revision/source fields correct in only 7/144; DARP was 46/144 and 51/144. Omitting generated plan context in the 24-world inference ablation changed DARP success 10/72→7/72 and AR 3/72→4/72, limited evidence of context dependence, not mediation.

| Guided static attempt sample | AR | DARP | WHOLE |
|---|---:|---:|---:|
| Median time | 57.386 ms | 38.797 ms | 22.040 ms |
| Median model calls | 59 | 36 | 12 |
| Median processed token positions | 5,350 | 3,528 | 2,400 |
| Complete handoffs | 5/144 | 21/144 | 0/144 |

These were noninterleaved and quality-unmatched. Faster failed output is not cheaper useful maintenance. Selected examples showed DARP repairing an unnecessary action to `finish` and unsupported source IDs; a selected AR failure remained coherent JSON but violated identity/order evidence. Those examples do not estimate average success.

**Failures and resource accounting:** A lexical syntax defect was caught pre-lock; a report-builder error occurred post-result. AR seed 11101 was interrupted after durable step 100; the exact remaining tail is unknown within a 0–100 update interval. The original competence and revision failures remain. Consolidated accounting reports 8,100 logical main updates, 8,100–8,200 actual main updates, 12 disposable preflight updates (8,112–8,212 total); 263.332 seconds training-loop time, 122.367 seconds main-evaluation time, peak RSS 356,990,976 bytes. Timing excludes development/startup/preparation/packaging; no energy or end-to-end maintenance-night cost. Sampled numerical checks and checkpoint/replay totals are in the consolidation below.

**Meaning:** Token-level editing is possible and a few explicit corrections worked; reliable handoffs, substantive replanning, broad benefit from guidance, and superiority over supported AR did not. The next change justified by the report was better task-interface preparation, which DARP02 tested.

**Source locators:** `NSS_DARP_Research_Results_Analysis_and_Decision_v1.0.docx` §§06–08; `.consolidation/20260928/darp_review/DOCUMENT_TEXT.txt` (extracted body/table text); cited but not locally inspected: `NSS_NBR02_DARP01_Execution_v0.1.zip::REPORT.md` (`D01-R`), `::protocol/PROTOCOL.md` (`D01-P`), `::ARCHITECTURE.md` (`D01-A`).


<a id="pass-darp02"></a>

### DARP02 — Common metadata wrapper and repair/revision preparation

**Type and status:** Completed continuation/preparation study; 12 continuations completed 600 steps, with original parent and control results retained. The preparation package raised complete-handoff rates, but the prospective two-of-three DARP seed working point was not met and richer typed feedback showed no broad benefit. Source tier: consolidated DOCX report only in this review.

**Broad question and mapping:** Does teaching create/edit/revise contexts and separating exact administrative metadata from learned content make plan-guided block writing more usable? DARP editorial question map; no `Gxx` mapping stated.

**Specific question:** Does a common exact record wrapper plus location-only or typed correction feedback improve DARP/AR on complete maintenance handoffs and changed-plan cases, including natural errors, without changing the model capacity?

**Systems and arms:** The six DARP01 AR/DARP endpoints are reused. **U + wrapper** evaluates each original parent under a common wrapper that supplies 13/17 tokens in each record; writer predicts four substantive fields per record (12 per handoff). **P/location** continues the writer for 600 updates with BAD/OK location-only feedback. **R/typed** continues for 600 updates with typed error codes mapped onto existing lexical tokens (no extra parameters). WHOLE is not continued. At evaluation, each prepared endpoint faces no feedback, location-only, typed, and shuffled typed-category policies; shuffled feedback retains true error locations but permutes categories with no fixed points. No-feedback also removes correct-field protection, so it is not a pure category ablation. AR and DARP share model size, wrapper, semantic targets, contexts, task families and checker; the exact wrapper is software support.

**Method, data and resource limits:** Training uses 4,096 fresh old/current pairs =8,192 unique inputs. Phases: create (updates 1–100), equal create/revise exposure (101–200), then mixed 30% creation/35% repair/35% revision (201–600). Authored drafts include coherent wrong-order, old-evidence, premature-finish and known/hold errors plus 20% clean. Confirmation: 48 static worlds, 24 revision pairs, 24 injected cases reusing static inputs; 18 revision pairs change the action sequence and six do not. Evaluation: 5,184 main episodes (12 prepared endpoints × four feedback policies ×96 plus six U endpoints × location ×96), plus 384 development records. Static working point remains ≥44/48 in at least two of three DARP seeds; changed-revision threshold ≥17/18 reported separately. New logical updates 12×600=7,200, with three caller interruptions; actual main applications reported 7,200–7,350, plus 12 disposable applications. Exact timing/RSS: training loop 212.331 seconds, evaluation 88.312 seconds, separate development 6.948 seconds; peak RSS 358,191,104 bytes. These are not total task-cost or energy measures.

**Complete-handoff results:**

| Writer / preparation | Static | Changed plan | Injected |
|---|---:|---:|---:|
| AR U + wrapper | 95/144 | 21/54 | 43/72 |
| AR P / location | 129/144 | 46/54 | 68/72 |
| AR R / typed | 129/144 | 46/54 | 68/72 |
| DARP U + wrapper | 51/144 | 8/54 | 22/72 |
| DARP P / location | 116/144 | 48/54 | 60/72 |
| DARP R / typed | 116/144 | 48/54 | 60/72 |

Each static denominator is 48 worlds × three parents; changed is 18 pairs × three; injected is 24 worlds × three. DARP prepared pooled static was 80.56%, changed 88.89%; AR 89.58% and 85.19%. Per-parent prepared static results: AR 41/48, 43/48, 45/48; DARP 40/48, 32/48, 44/48. Only one seed per writer reaches the 44/48 bar, so neither clears the two-of-three criterion. DARP's 48/54 changed-plan successes are restricted to seven hold, seven known/unknown and four done-bit changes; no sampled order or required-bit change changed the action sequence.

| Prepared DARP feedback policy (P or R) | Static | All revisions | Changed | Injected |
|---|---:|---:|---:|---:|
| none | 113/144 | 65/72 | 48/54 | 58/72 |
| location | 116/144 | 64/72 | 48/54 | 60/72 |
| typed | 116/144 | 65/72 | 48/54 | 60/72 |
| shuffled | 116/144 | 64/72 | 48/54 | 60/72 |

P and R share complete-handoff counts. Correct category information adds one all-revision success over location/shuffled, only in an unchanged-action case; P obtains it without typed-feedback training. Prepared AR completion is unchanged across feedback policies. The data do not support mandatory typed categories; token-level differences also do not show that all feedback is ignored.

| Repair situation | Prepared AR | Prepared DARP |
|---|---:|---:|
| Naturally wrong static blocks fully repaired | 0/20 | 4/66 |
| Deliberately damaged blocks fully repaired | 210/216 | 187/216 |
| Final static false-COMPLETE handoffs | 0 | 7 |

For typed DARP, natural wrong fields fell 126→118, but 62/66 initially wrong blocks remained incorrect. Synthetic damage repair is not the same as correcting a writer's naturally persistent interpretation. Exact checker categories and correct-field copy protection remain part of the system.

**Failures and interpretation:** Three training caller interruptions at durable updates 350/500/450 were resumed by exact cursor; up to 50 repeated unsaved updates each remain included in upper-bound accounting. An audit corruption injector sometimes replaced a token already marked MASK (no-op); this retained defect was isolated, separately corrected-injector checks passed, and main study code stayed unchanged. Natural procedural errors remain visible. The substantial gain is a preparation/workflow result with extra training and broader exposure; its individual causal ingredients are not isolated. It did not establish DARP as better than AR or qualify semantic autonomy.

**Source locators:** consolidated DOCX §§09–11; `.consolidation/20260928/darp_review/DOCUMENT_TEXT.txt`; cited but not locally inspected: `NSS_NBR02_DARP02_Execution_v0.1.zip::REPORT.md`, `::protocol/PROTOCOL.md`, `::ARCHITECTURE.md` (`D02-R/P/A`).


<a id="pass-darp03"></a>

### DARP03 — Actual writer-error rehearsal and prospective keep-or-park comparison

**Type and status:** Completed, prospectively adjudicated, bounded comparison. Its two quality and efficiency routes both failed; park this DARP implementation while retaining workflow/evidence. This compendium used the consolidated DOCX report; original DARP archives, raw outcomes and checkpoints were not reopened in this review.

**Broad question and mapping:** Does learning from actual erroneous writer drafts help repair, and does the resulting supported diffusion writer yield a practical quality/cost advantage over equivalently supported AR? DARP editorial question map; no `Gxx` mapping stated.

**Specific question:** On the same fresh static, changed-plan and common-error panels, does actual-error replay (**N**) outperform matched authored-error rehearsal (**C**) and unchanged prepared parents (**U**), and does N-DARP beat N-AR under a preregistered quality or efficiency rule?

**Systems and arms:** Six DARP02 location-prepared P endpoints seed 12 branches. **U** is untouched; **C** gets artificial wrong tokens inserted at observed wrong positions, excluding the correct and original wrong token; **N** trains from frozen actual first-attempt errors pooled within each seed across AR+DARP. C and N share cases, generated plan contexts, schedules, masks and targets. DARP remains four-step, same wrapper, location-only checker, at most two repairs; AR gets the same information and opportunity. Each C/N branch receives 400 additional updates with fresh AdamW, cosine .001→.0002, weight decay .01, clipping 1.0. Three seed pairs; all 12 final endpoints complete. Additional gradient-bearing positions are matched across AR/DARP/C/N (19,271/19,734/17,725 per seed); historical training, FLOPs and all-location information were not equalized.

**Method, data and resource limits:** Collection: 256 fresh static worlds plus 96 revision pairs; 16 pairs each of done/required/order/hold/known/no-op changes. It yields 6,336 current-block records; 757 are wrong (264/363/130 by paired seed), from frozen U writers—not an on-policy continuing curriculum. Fresh evaluation: 128 static worlds plus 60 revision pairs, 3,384 handoff trials across 18 endpoints. Ten pairs per type create 50 changed-action cases plus ten binding-only revisions; a fixed common erroneous-draft probe uses every wrong U first attempt pooled within seeds. Inputs exclude 12,464 prior study hashes; primitive rules remain reused. Total logical main updates: 4,800; actual 4,800, plus six disposable checks. Training loop 148.783 seconds, main evaluation 46.287 seconds, collection 22.810 seconds, common probes 10.518 seconds, peak RSS 358,907,904 bytes. Timing excludes coding/startup/packaging; no energy or isolated model-memory measure.

**Primary complete-handoff outcomes:**

| Writer / preparation | Static | Changed plan | Equal-family macro |
|---|---:|---:|---:|
| AR U | 348/384 (90.62%) | 108/150 (72.00%) | 81.31% |
| AR C | 366/384 (95.31%) | 130/150 (86.67%) | 90.99% |
| AR N | 361/384 (94.01%) | 128/150 (85.33%) | 89.67% |
| DARP U | 314/384 (81.77%) | 82/150 (54.67%) | 68.22% |
| DARP C | 348/384 (90.62%) | 115/150 (76.67%) | 83.65% |
| DARP N | 359/384 (93.49%) | 128/150 (85.33%) | 89.41% |

DARP N improves its own U by 21.19 macro points and matched C by 5.77 points, so real erroneous content helped this DARP preparation on this task. Its macro is .260 points below AR N; changed-plan counts tie, AR has two more static successes. AR N is slightly below AR C, showing the actual-error recipe did not benefit both writers uniformly.

| Parent | AR static | DARP static | AR changed | DARP changed | DARP − AR macro |
|---|---:|---:|---:|---:|---:|
| 11101 | 123/128 | 122/128 | 48/50 | 41/50 | −7.39 pp |
| 11102 | 118/128 | 116/128 | 35/50 | 45/50 | +9.22 pp |
| 11103 | 120/128 | 121/128 | 45/50 | 42/50 | −2.61 pp |

| Revision type | AR N | DARP N | Action changes? |
|---|---:|---:|---|
| done | 24/30 | 25/30 | yes |
| required | 27/30 | 28/30 | yes |
| order | 25/30 | 20/30 | yes |
| hold | 23/30 | 27/30 | yes |
| known | 29/30 | 28/30 | yes |
| no-op / binding only | 29/30 | 29/30 | no |

DARP’s better hold results coexist with poorer order-change results. The data do not isolate why, or prove arbitrary replanning. Source revisions keep the learned writer fixed; they are not changed-weight task-state migration.

| Common fixed wrong-block probe | Common wrong blocks fully repaired | Wrong fields before → after |
|---|---:|---:|
| AR U | 216/431 (50.12%) | 786 → 386 |
| AR C | 398/431 (92.34%) | 786 → 55 |
| AR N | 386/431 (89.56%) | 786 → 79 |
| DARP U | 45/431 (10.44%) | 786 → 653 |
| DARP C | 273/431 (63.34%) | 786 → 262 |
| DARP N | 391/431 (90.72%) | 786 → 55 |

| Newly generated wrong blocks, N branches | AR | DARP |
|---|---:|---:|
| Static wrong blocks repaired | 6/33 | 35/70 |
| Changed-revision wrong blocks repaired | 3/39 | 39/78 |
| False-COMPLETE handoffs, static / changed | 0 / 1 | 6 / 0 |

The common probe's same-draft denominator tests older frozen errors, while new-error denominators differ by writer and difficulty. DARP N's five-block lead over AR N is not decisive: AR C repairs seven more common blocks; full handoff remains primary.

| Prospective practical-win criterion | Quality route | N-DARP result | Efficiency route | N-DARP result |
|---|---|---|---|---|
| Macro difference / runtime | ≥+5 pp vs AR / ≤1.25× AR | −0.260 pp / 1.066× | ≥20% faster with ≤1 pp loss pooled and per parent | DARP was slower; losses exceeded 1 pp in two parents |
| Parent consistency | no negative seed difference | two negative | same 90% macro working point required | only one parent reached 90% |
| Working point | ≥90% macro in ≥2/3 | one parent | ≥90% macro in ≥2/3 | one parent |
| False-COMPLETE | no higher than AR | 6 vs 1 | no higher than AR | 6 vs 1 |
| Route result | all conditions | **fail** | all conditions | **fail** |

The timing subset was 72 warmups and 216 interleaved episodes, first eight static and four revision cases per three seed pairs (revision subset is done-bit changes). Median AR 9.418 ms, DARP 10.041 ms, ratio 1.0661, about 6.61% slower. No GPU/optimized decoder, energy, or large-block speed claim follows.

**Failures, validation and limits:** No main numerical stop or interruption; the no-advantage result is interpretable. In the underlying studies, reports say sampled tolerance/argmax failures were zero; consolidation lists 25,092 sampled scalar comparisons, 36 selected full replays, 18 partial-sweep resumes, 54 invalid snapshots rejected, 10 preflight groups and 42 checkpoint files including six imported parents. The DARP01/02 incidents and update-count intervals remain separate; the combined logical main total is 20,100 updates (actual 20,100–20,350), plus 30 disposable checks across all three studies. Reports' model archives were integrity-checked by the consolidation author; our current pass did not rerun those checks. The task has closed schema, perfect rule-aware checker, four learned content fields/block and no HSA integration, language model, open semantic evaluation, 25k-token budget or day/night lifecycle. Neither equivalence nor impossibility of diffusion is established.

**Meaning:** Keep the exact workflow ideas—source binding, plan/edit/revision fields, checks, block commit/supersession and report of false-completion outputs. Retain AR as current reference. Park this particular DARP implementation because it demonstrated no practical advantage under its frozen decision rules.

**Source locators:** consolidated DOCX §§12–24 and extracted text; cited but not locally inspected execution sources: `NSS_NBR02_DARP03_Execution_v0.1.zip::REPORT.md`, `::protocol/PROTOCOL.md`, `::ARCHITECTURE.md`, `::results/DECISION.json` (`D03-R/P/A/D`). The source register also names matching DARP01 and DARP02 archive members above.


<a id="question-11"></a>

## 11. Can a reader interpret evidence and benefit from retrieval or preparation?


<a id="pass-comp01-a"></a>

### COMP01-A — exam and exact-field scorer engineering only

**Broad question.** Reader-path measurement and task-contract preparation; G02 (whether a failure belongs to architecture, training, data, or interface) is context only. COMP01-A is not a model comparison and does not resolve any G question.

**Exact question.** The ledger does not preserve a formal numbered hypothesis. Its recorded task is: can the exam and marking be built and checked before testing a companion? The plain-language entry says “Build the exam and check that its marking works before testing the companion.”

**Type and status.** Engineering-only test preparation, `COMPLETE_ENGINEERING_ONLY`. No model was run.

**Systems, method, and controls.** The package is reported to contain a protocol, fictional histories, an exact-field scorer, and fault checks. These are test-construction artifacts and software checks; there is no learned reader, pretrained model, trained control, or inference arm. The source catalog keys are `PLAN`, `CODEX`, and `CURRENT` (`results/PREFLIGHT.json`, scoped in the ledger as new COMP01-A engineering receipts).

**Documented result.** Checklist v0.19 reports completion of the protocol, fictional histories, exact-field scorer, and fault checks, and explicitly says there was no model run. It gives no numerical scorer accuracy, number or type of injected faults, pass counts, seeds, resource measurements, or predeclared acceptance threshold. I therefore record no numeric success rate.

**Interpretation and limits.** This establishes only that an exam/scorer engineering task was recorded as completed. The detailed preflight receipt and its exact checks are not reproduced in the checklist, so no stronger scorer-reliability claim can be made here. It is not COMP01 language evidence, not a result from a reader, and not qualification of the exam's semantic fairness.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue row `COMP01-A`; source-catalog key `CURRENT`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (priority queue); `RESEARCH_INDEX.md` (G02 wording only).


<a id="pass-comp01-b-setup"></a>

### COMP01-B/SETUP — pinned language-reader route selected, acquisition blocked

**Broad question.** Whether a small actual language model can serve as a research reader is a reader-competence/evaluation question. G02 is only a causal-diagnosis context; this setup work did not test competence and provides no direct G-question answer.

**Exact question.** The recorded COMP01-B task asks whether an actual language model can answer with the right page in front of it and then find that page in a notebook. The narrower completed setup task was to choose a small test reader and wire it to the exam.

**Type and status.** Engineering/setup only, `ENGINEERING_ONLY_MODEL_ACQUISITION_BLOCKED`; the language-reference evaluation remains deferred and unrun. Do not combine this setup record with LAB01–READER-SUPPORT01 as though they were COMP01-B language-model results.

**Selected system and fallback rule.** The ledger selects `HuggingFaceTB/SmolLM2-135M-Instruct`, pinned at revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`. `HuggingFaceTB/SmolLM2-360M-Instruct` is the sole conditional fallback, allowed only after a complete 135M development screen yields fewer than two provisionally usable families. The fallback is not authorized merely because download or runtime setup fails. The model's declared scope is a research reference, not production NSS; the ledger records that it is not to be trained. `weight_bytes_acquired` is 0.

**Method and documented results.** Acquisition failed before inference. The adapter/runner engineering record reports 18 offline runner-contract tests passed. No model load, inference, training, confirmation evaluation, or cloud fallback occurred. The source catalog names `NSS_COMP01B_Small_Reader_Setup_Report_v0.1.md`; the ledger identifies it as a current-host engineering/setup record, not a model result. Its full details are not restated in this ledger.

**Missing fields and interpretation.** There is no test corpus, data split, seed, accuracy, model output, runtime, or resource result because the selected model was never acquired and queried. The exact acquisition error, attempted byte count, and test-by-test contract results are absent from the v0.19 checklist. Selection and an 18-test adapter pass are not language-reader competence. The checklist also preserves the distinction from earlier planning: COMP01-B remains deferred, while an internal reader route could proceed without relabeling its results as COMP01-B.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue row `COMP01-B`, prior-task row `COMP01-B-SETUP`, source-catalog key `COMP01B_SETUP`, selected test reader); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (deferred route and 18-test setup outcome); `RESEARCH_INDEX.md` (G02 wording only).


<a id="pass-lab01"></a>

### LAB01 — first three fresh autoregressive reader fits

**Broad questions.** G02 asks whether reader failures arise from architecture, insufficient training, poor data, or weak interfaces. LAB01 supplies a small bounded-reader diagnostic but does not isolate those causes. Its reader-evidence question is local to simple English records, not broad NSS or COMP01 language competence.

**Exact question.** Can an internally trained small reader answer from simple English evidence without a pretrained download?

**Type and status.** Completed bounded training/inference diagnostic; `COMPLETE_BOUNDED_DIAGNOSTIC_REFERENCE_NOT_READY`. The ledger describes three fresh autoregressive (AR) readers and says no evaluation family met the working point.

**Systems, data, and method reported.** The only system description retained is three new AR fits with 92,837 parameters each. The checklist reports 5,400 main plus 6 preflight optimizer updates. It separates familiar-supported, withheld, and paraphrase answer families. It does not preserve architecture beyond “AR,” prompt or record construction, exact training/evaluation split procedure, per-fit seed, family working-point thresholds, or a named non-neural/reference arm. Do not infer them.

**Documented arm/family results.**

| Evaluation family | Ledger result | Gate statement retained |
|---|---:|---|
| Familiar supported answers | 833/1,536 | Part of the bounded diagnostic; no family met the working point overall |
| Withheld answers | 768/768 | Perfect aggregate count as reported; does not establish performance on other families |
| Paraphrase answers | 251/768 | Lower wording-sensitive result; no family met the working point overall |

The checklist's wording is “no family passes.” It does not say that the 768/768 withheld line alone qualified an entire model or family gate. The fit-level rows and any joint criterion are missing.

**Validation and costs.** The ledger reports 21 preflight groups, 5,376 recounts, 384 fresh replays, 24 checkpoint hashes, and 48,480 sampled precision values, all passing their listed checks. These are source-reported engineering/reproducibility/numerical checks, not fresh checks by this compendium. Training-update counts are above; wall time, peak memory, inference latency, energy, and storage totals are not reported here.

**Interpretation and limits.** The local reader was executed and did not reach its declared working point. The counts show a marked paraphrase deficit beside the reported withheld aggregate, but the ledger lacks the item-level data, fit variation, split protocol, and criterion needed to determine whether the cause is wording, binding, model capacity, training, or interface. Keep its model/corpus/checkpoints as diagnostic evidence; do not call it a memory-system verdict or COMP01-B qualification.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (previous-task row `LAB01`; queue row `LAB01`; source-catalog key `LAB01`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (previous research and queue).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-lab02-size"></a>

### LAB02-SIZE — three widths, no consistent width gain

**Broad question.** G02 is the relevant diagnostic context: does additional model capacity explain the reader's failures? This bounded width comparison does not demonstrate that 92,837 parameters were a resource ceiling or isolate capacity from seed effects.

**Exact question.** Does giving the same small reader more width improve project/date record answers enough to justify added parameters and training work?

**Type and status.** Completed bounded size diagnostic, `COMPLETE_BOUNDED_DIAGNOSTIC_NO_CONSISTENT_WIDTH_GAIN`. It is an executed comparison, not a proposal for another width sweep.

**Systems and method reported.** The historical planning note specifies widths 64, 72, and 80, ordinary preparation, and three fresh fits at each width; the v0.19 execution summary reports nine fresh fits total. Corresponding parameter counts are 92,837, 113,645, and 136,501. The summary reports whole supported-answer counts over 1,536 per width and a separate wording measure. It does not retain the architecture specification, item allocation, exact fit pairing/seeds, full data split, or declared qualification threshold. The ledger notes “mixed seed changes,” so do not treat the small aggregate difference as a clean causal width estimate.

**Documented arms and outcomes.**

| Width | Parameters | Supported whole answers | Other reported result |
|---:|---:|---:|---|
| 64 | 92,837 | 833/1,536 | Retained as the economical diagnostic control |
| 72 | 113,645 | 825/1,536 | No consistent improvement reported |
| 80 | 136,501 | 844/1,536 | Largest result is +0.72 percentage points relative to width 64, with mixed seed changes |

The ledger also records the wording metric changing from 31.12% to 35.81% under mixed seed changes. It does not identify the precise wording metric construction in the checklist. No family reached its working point.

**Resource and failure record.** Nine fresh fits completed with 16,218 total optimizer applications, 40 engineering groups, and no main-run interruption. Exact wall-time, activation-memory, peak RSS, energy, and storage values are not present. The earlier planning record explicitly says 92,837 parameters were a tested size, not a proven resource ceiling or cause of failure. Retain width 64 as the economical diagnostic control; no automatic fourth size or additional training was authorized.

**Interpretation and limits.** The largest width is only 11/1,536 answers above width 64 (reported as +0.72 pp), while width 72 is below it, and seed changes confound the wording comparison. This does not support a general scaling claim, a causal parameter-count effect, or an inference that width is the reader's limiting factor.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (previous-task row `LAB02-SIZE`; queue row `LAB02-SIZE`; source-catalog keys `LAB02_SIZE_PLAN`, `LAB02_SIZE_REPORT`, `LAB02_SIZE_EXECUTION`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (summary and proposal boundary).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-lab02-bind"></a>

### LAB02-BIND — mixed versus staged binding curriculum

**Broad questions.** G06 asks whether entities and relations can be recombined without confusion; project/date record binding is adjacent evidence, not a broad compositional-competence test. G02 is also context because schedule, data, interface, and reader limitations were not separately isolated.

**Exact question.** If two readers get the same kind of exercises in different orders, does a staged project/time-binding curriculum help them use evidence better than mixed practice?

**Type and status.** Completed six-reader paired bounded diagnostic, `COMPLETE_BOUNDED_DIAGNOSTIC_NO_CURRICULUM_GAIN`. The source ledger explicitly calls it an actual current execution with same-author review and internal reproduction, not an external replication.

**Systems and method reported.** The compared routes are a mixed curriculum and a staged curriculum; the ledger says six fresh paired readers (three pairs) and reports “staged lower in all 3 pairs.” It records explicit new rules and full raw test/answer traces. Exact learner architecture, parameter count, pair seeds, item/split allocation, schedule contents, update budget, resource use, and numerical working-point criteria are not stated in v0.19. The source-catalog keys are `LAB02_BIND`, `TEMPORAL_REVIEW`, and `DUAL_REVIEW`.

**Documented arm results.**

| Arm | Supported answers | Rate reported | Pairwise direction | Gate/result |
|---|---:|---:|---|---|
| Mixed | 757/1,536 | 49.28% | Higher than staged in each of the three reported pairs | No family reached working point |
| Staged | 734/1,536 | 47.79% | Lower in all three reported pairs | No curriculum gain |

The ledger reports a total of 9,984 outputs subjected to finite-grammar review and a manual review of 64 items/384 responses. No old scores were changed. The exact qualification threshold, definition of “supported answer,” and review sampling procedure are not included in the v0.19 record.

**Interpretation and limits.** The staged order did not improve this reader comparison; all three reported pairs went the other way, but no pair-level table or uncertainty estimate is retained. This is not evidence that all curricula fail or that binding is solved. The ledger's next decision parks the staged schedule and preserves all models, corrected fixtures, reviews, and raw traces.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (previous-task and queue rows `LAB02-BIND`; source-catalog keys `LAB02_BIND`, `TEMPORAL_REVIEW`, `DUAL_REVIEW`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (summary and review counts).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-lab-reader-decision"></a>

### LAB-READER-DECISION — park reader preparation and route to handoff diagnosis

**Broad question.** This is a planning/triage decision after the LAB reader family failed its working point, not a new broad research-question result. It keeps G02 (diagnose reader limitations) in view but adds no Gxx evidence.

**Exact decision question.** How should the next useful research reader be obtained without repeatedly training the same weak reader?

**Type and status.** Documentary route-selection decision, `ROUTE_SELECTED_READER_PREPARATION_PARKED`. It is not a model run, reviewer study, or independent audit.

**Decision and compared routes.** The decision records LAB02-BIND completion with no reader family at its working point, preserves all LAB reader failures, and routes next to the bounded MEM01 mechanism comparison. Further size increases and curriculum campaigns are parked by default. The route is intended to distinguish reader answer errors from additional-information/handoff losses; it explicitly forbids claiming COMP01-B competence. No numeric result or new execution is reported for this decision.

**Interpretation and limits.** The route change is a response to the diagnostic record, not evidence that handoff is the only cause of bad answers or that compact memory is better. The separate selected pretrained COMP01-B route remains deferred/acquisition-blocked. No exact formal decision threshold, alternatives table, or measured cost comparison is preserved in the checklist.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue row `LAB-READER-DECISION`; source-catalog keys `LAB02_BIND`, `CODEX`, `MEM01_ROUTE_DECISION`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (reader route decision).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-lab-semantic-review"></a>

### LAB-SEMANTIC-REVIEW — corpus review recorded, retrospective adjudication pending

**Broad questions.** This is review-method and test-validity evidence adjacent to G16 (whether unsupported claims can be caught while retaining useful supported answers). It was not a neural critic evaluation and does not establish all-panel semantic quality.

**Exact question.** Is the test fair as well as whether each response follows from what the test itself says?

**Type and status.** Documentary review/prospective policy, `NEW_CORPUS_REVIEW_COMPLETE_RETROSPECTIVE_REVIEW_PENDING`. The standard requires retaining each actual public test and raw answer and checking test validity and response appropriateness beside the original key. The policy is documented but `NOT_YET_INTEGRATED_IN_EXECUTABLE_SCORER`; the JSON says `semantic_review_completed_this_update: false` and `historical_regrading: false`.

**Method and reviewed coverage.** The checklist points to a targeted temporal wording review and a dual test-and-response review standard. For the latest recorded application, LAB02-BIND, it lists 4,768 item checks and 9,984 response checks. A manual sample covered 64/1,024 confirmation items and 384/6,144 outputs; it was same-author, not independent. The checklist says the initial targeted temporal review is not a full audit and requires exact retained prompts, raw responses, and original grading references for the broader retrospective review.

**Documented result and scope defect.** The later READER-SUPPORT01 note records a gap in the public `status` ancillary-field scope. It says to preserve raw scores, preregistered aliases, and retrospective narrow-fact interpretations separately, and expressly rejects an all-panel semantic-quality claim. No automatic historical regrading or new training was authorized. The original results remain unchanged.

**Interpretation and limits.** Some test/response review and policy documentation exist, but the retrospective audit remains pending and was not independently conducted. The listed sample denominators make the limited manual coverage explicit; do not describe this as a full test-validity audit or as a measured neural critic. The status-field issue is an output-contract/measurement limitation that must remain attached to READER-SUPPORT01's numeric scores.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (`queue` row `LAB-SEMANTIC-REVIEW`; `current_evaluation_policy`, `latest_application`, and `support01_note`; source-catalog keys `TEMPORAL_REVIEW`, `DUAL_REVIEW`, `DUAL_REVIEW_RECORD`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (standing evaluation rule and semantic review status); `RESEARCH_INDEX.md` (G16 wording only).


<a id="pass-mem01"></a>

### MEM01 — bounded handoff and compact-scope retrieval diagnostic

**Broad questions.** G03 asks what survives events, interruption, and restart without transcript growth. G07 asks what can be retained losslessly, what is approximate, and what must be rehydrated. MEM01 gives a narrow frozen-reader handoff/retrieval result, not broad memory or changed-weight state qualification.

**Exact question.** Can the work be saved and reopened with current records so that the right unfinished tasks and current facts survive, and can a compact handoff distinguish missing memory from a reader misunderstanding correct notes?

**Type and status.** Completed bounded handoff diagnostic, `COMPLETE_BOUNDED_HANDOFF_DIAGNOSTIC_READER_LIMITED`. The ledger identifies it as frozen-model inference and software lifecycle tests, same-author semantic sample and internal replay, not external replication.

**Systems and method reported.** Three frozen LAB02-BIND mixed-curriculum readers were reused; the run reports zero updates. The comparison labels are `DIRECT/FULL` and `COMPACT`. The ledger does not provide operational definitions of those labels beyond the compact-scope/packet and direct/full names, so this entry does not invent a specific serialization or lookup design. There were 3,888 response observations. The source-catalog keys are `MEM01_REPORT`, `MEM01_EXECUTION`, and `DUAL_REVIEW`; their underlying report and raw execution archive are not reproduced in v0.19.

**Documented policy outcomes.**

| Measure | DIRECT/FULL | COMPACT | Ledger interpretation |
|---|---:|---:|---|
| Post-break complete answers | 413/864 | 504/864 | COMPACT is +10.53 percentage points; 150 gains and 59 losses; all three parents gain |
| Whole four-answer resume | 8/216 | 8/216 | Ledger says 8/216 “all policies”; no per-policy split is provided |
| Record-integrity checks | — | — | Aggregate: 1,944 checks, 0 losses |
| Packet replays / snapshot restores | — | — | Aggregate: 2,592 packet replays and 432 exact snapshot restores |

The table's em dash means that the checklist supplied an aggregate or all-policy result rather than distinct arm values. It is not a zero.

**Validation, failures, and limits.** The ledger reports 23 preflight groups, 3,888 recounts/full replays, and 41,580 sampled precision values passing. One audit call timed out; the main run is marked complete, while partial audit work is explicitly “unknown.” Current-status errors remain. The reported benefit is ordinary scoped lookup, not new reader learning. Exact prompt/task split, parent seeds, interruption timing, policy contract, success thresholds, per-parent effects, and resource/timing values are absent from the checklist. No broad companion competence, retraining benefit, changed-weight continuation, or external replication is established.

**Interpretation.** This is a bounded result for frozen readers with additional handoff/retrieval conditions: the compact-labeled condition has more complete post-break answers in the reported aggregate, while whole four-answer resume remains rare at 8/216 under all policies. Record preservation/replay checks are positive software evidence, distinct from answer competence. Preserve the audit timeout and unknown partial-audit scope.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue and previous-task rows `MEM01`; source-catalog keys `MEM01_REPORT`, `MEM01_EXECUTION`, `DUAL_REVIEW`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (summary result and route/status).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-prep01"></a>

### PREP01 — query-independent source sheet versus retrieval/cache controls

**Broad questions.** G14 is adjacent: whether extra preparation helps later work beyond extra data or ordinary search. PREP01 tests fixed-reader source-sheet preparation and retrieval/caching policies; it does not test neural idle computation, rehearsal, or a learned Tertiary. G07 is also contextual because source selection, caching, and retrieval are compared, but no complete memory-cost proof is reported.

**Exact question.** Does preparing a source-linked task sheet before the question arrives help more than ordinary retrieval, or making/caching the same sheet when asked?

**Type and status.** Completed bounded frozen-reader diagnostic, `COMPLETE_BOUNDED_DIAGNOSTIC_WORKSHEET_TRADEOFF_NO_ADVANCE_GAIN`. The ledger calls it actual fixed-reader inference plus exact finite-grammar preparation and CPU timing; a privileged exposed-support diagnostic is separate. There were zero model updates.

**Systems and method reported.** Three unchanged readers of 99,674 parameters each answered 5,472 main responses. The raw condition is `RAW`; the ledger compares it with three sheet policies. It explicitly names `ADVANCE` and `CACHE`, but does not name the third policy in the result string. The sheet quality is reported identical before and after the query. It also describes an exposed gold-support diagnostic as not deployable. The exact policy-to-source construction, task split, reader seeds, per-policy counts, and criteria are not retained in the checklist.

**Documented results.**

| Policy/measure | Ledger result | Qualification/limit |
|---|---:|---|
| RAW | 818/1,368 (59.80%) | Outscored the pooled three-sheet result |
| Three sheet policies, pooled | 790/1,368 (57.75%) | All three readers decline versus RAW; 163 gains and 191 losses |
| False completion | 54 → 14 | Metric name preserved; policy-wise table absent |
| “Done-work suggestions” | 330 → 384 | Ledger's exact label; direction/meaning not further defined |
| ADVANCE versus CACHE timing | ADVANCE slower in all 9 timing medians | Exact times and third policy's timing are absent; high-reuse ratio 1.043 |
| Exposed gold-support diagnostic | 41/72 → 58/72 | Mainly status 22/36 → 36/36; work 19/36 → 22/36; explicitly not deployable |

Identical sheet quality before/after the query is reported; it does not mean identical answer quality. The named “gold-support” condition is privileged and is not an eligible deployed policy.

**Validation and engineering history.** The ledger reports 5,472 main plus 288 diagnostic recounts, 5,472 fresh replays, 576 restores, and 73,920 sampled precision values passing. There were 21 preflight groups after a preserved copy bug. A post-result audit type mismatch was corrected separately. These are historical validation notes, not checks rerun for this compendium. The ledger gives no wall-clock values, only the ordering of nine timing medians; other resource totals are absent.

**Interpretation and limits.** The query-independent sheet approaches show a quality/cost tradeoff, not an advance-preparation win: RAW scored higher in the reported aggregate, and ADVANCE was slower than CACHE in every listed median. The exposed gold-support diagnostic improved, but is not deployable and cannot rescue the main result. The three sheet policies are not all named, so do not present an invented complete arm list or claim a universal retrieval advantage.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue and previous-task rows `PREP01`; source-catalog keys `PREP01_REPORT`, `PREP01_EXECUTION`, `DUAL_REVIEW`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (summary and parked next-action).; `RESEARCH_INDEX.md` (broad G-question wording only)


<a id="pass-reader-support01"></a>

### READER-SUPPORT01 — answer-only versus answer-plus-source supervision

**Broad questions.** Reader evidence-use and answer support are the primary category. G16 is adjacent only: the study adds source supervision to a small reader but does not test a separate critic catching unsupported claims, nor does the ledger claim all-panel semantic quality. G02 remains a causal-diagnosis context because an output-contract gap limits interpretation.

**Exact question.** Can a small reader be taught which notes support its answer, and does that help compared with answer-only practice or an ordinary question-aware index?

**Type and status.** Completed fresh paired training/inference diagnostic, `COMPLETE_BOUNDED_DIAGNOSTIC_NO_PRIMARY_GAIN_OUTPUT_CONTRACT_LIMIT`. The evidence type in the ledger is finite-contract scoring plus 144 same-author reviews and sampled numerical checks; no follow-up fitting was conducted.

**Systems and method reported.** Six fresh 106,615-parameter readers are compared: `A` uses answer-only loss; `S` uses answer-plus-source loss. A public question-aware `LOOKUP` arm is also reported. The text implies paired/parent comparisons (three parent deltas) but does not supply the fit/seed table, architecture details, exact training/evaluation split, supervision examples, lookup implementation, or predeclared pass threshold. There are 1,536 supported five-field answer opportunities in the primary aggregate.

**Documented arms and outcome categories.**

| Arm / outcome | Ledger result | Meaning retained from checklist |
|---|---:|---|
| A: answer-only, supported five-field answers | 586/1,536 (38.15%) | Higher primary aggregate than S |
| S: answer-plus-source, supported five-field answers | 521/1,536 (33.92%) | No primary supervision gain |
| Parent differences, S relative to A | −11.91, −3.91, +3.13 percentage points | Mixed only in the third reported parent; exact pair table unavailable |
| “A keeps all” | “all” (no denominator supplied) | Compressed ledger wording; exact field/behavior meant by “keeps” is not defined |
| S exact support | 808/1,536 | Of those, 287/808 answers are correct |
| Public LOOKUP | A 769/1,536; S 692/1,536 | Comparison reported by arm; not the same as complete handoff |
| Retrospective named-status fact | A lookup 768/768 | Does not establish complete handoff |
| Positive completion | 136 → 89 | Raw metric label and aggregate retained |
| “Done-work suggestions” | 235 → 341 | Raw metric label retained; no interpretation beyond ledger wording |
| Whole four-answer outcome | 0 → 9/384 | Complete four-answer outputs remain uncommon |

The public `status` ancillary-field scope was underspecified. Raw-key scores, synonym handling, and the retrospective review were kept separate; the numeric outcome was not replaced by a post hoc narrow-fact interpretation.

**Validation, costs, and failure record.** The ledger reports 29,952 recounts, 576 fresh replays, 42,912 sampled precision values passing, and 30 main checkpoints verified. It distinguishes 9,600 logical main optimizer applications from a compressed execution note of 9,808–9,809 actual main plus 12 preflight after a recorded 208-step tail replay. The checklist does not make the 9,808/9,809 difference or inclusion arithmetic unambiguous; preserve the range rather than normalizing it away. No follow-up fitting occurred. Runtime, latency, energy, and memory values are not supplied.

**Interpretation and limits.** The answer-plus-source arm had fewer supported five-field answers than answer-only in the pooled result, while producing many exact-support records that were often paired with incorrect answers. A's reported public lookup is higher, but the ledger separately warns that a named-status fact lookup is not a complete handoff. The underspecified public status field and raw-key/synonym distinction materially constrain scoring. The result does not show that source supervision generally harms readers, that all supported claims were reviewed, or that the separate critic function is solved.

**Sources.** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.json` (queue and previous-task rows `READER-SUPPORT01`; `current_evaluation_policy.support01_note`; source-catalog keys `READER_SUPPORT01_REPORT`, `READER_SUPPORT01_EXECUTION`, `DUAL_REVIEW`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (summary and output-contract limit); `RESEARCH_INDEX.md` (G16 wording only).


<a id="question-12"></a>

## 12. Which research proposals and unresolved questions remain open?


<a id="pass-cycle01"></a>

### CYCLE01 — Repeated day/night learning roadmap

**Type and status:** General future-study proposal in the evidence-led plan; not itself an executed experiment or dispatch. Later CYCLE01-A is a completed two-night development feasibility branch, while CYCLE01-B is the named longer reserved comparison not started.

**Broad question:** Can useful learned changes accumulate over consecutive accepted maintenance revisions without unacceptable collateral loss, declining ability to learn, or an unbounded backlog?

**Specific question:** Does a multi-night sequence of accepted model generations preserve valid older capability, incorporate superseding facts and reusable procedures, and remain capable of learning a late new task? The important distinction from RECOVER01 is that every cycle starts from the branch’s current accepted checkpoint rather than resetting each correction to the original parent. MICROMACRO01 supplies only a narrow cycle precedent and does not settle a sustained accepted-history question.

**Proposed systems and arms:** The plan calls for a non-learning current-evidence reference, acquisition without repair, ordinary replay, and a current-evidence-balanced repair candidate. The serving model stays unchanged during the day; each night trains a candidate from the current accepted checkpoint. Rejected candidates do not silently advance serving history; the candidate’s missed learning and queue/backlog are still counted. A no-worthwhile-learning night may retain the existing weights. An extra still-valid-output preservation/distillation arm is a possible later single-factor comparator only if residual loss warrants it, not an unannounced extra treatment. CYCLE01-A’s `BALANCED` arm is not treated as a completed test of all BALANCE01 dose factors.

**Proposed method and decision criteria:** Freeze multiple simulated cycles and resource budgets after development feasibility and before reserved confirmation. Include current factual corrections, genuinely reusable procedure learning on new instances, unchanged older skills, rare important behavior, interruptions and a late task for residual learnability. Do not provide stored final answers when claiming procedural transfer. Compare each accepted endpoint against original valid-ability anchors and its prior accepted revision, updating expected answers when evidence legitimately supersedes them. Report candidate transient training harm separately from behavior of the accepted serving model, plus old-version task residency/migration, reconstruction, rejected useful changes and unresolved work backlog. If reusing the older GRU path, first diagnose exposed numerical cases and freeze a justified verifier prospectively; otherwise validate the new implementation independently. Exact models, family sizes, seeds, cycle counts, thresholds, data recipe and budgets remain to be preregistered.

**Arms/results:** No general repeated-cycle run is documented. CYCLE01-A is described separately above; it completed two development nights and does not satisfy the multi-cycle reserved confirmation question. Its unequal extra-B exposure, finite correction task and all-development histories leave the general CYCLE01 question open.

**Meaning and limits:** CYCLE01 is a roadmap study family that adds accepted-history depth and continued learnability beyond correction branches that reset to parent weights. It does not assume BALANCE01 is already successful, require a perfect reader, or authorize repeating HSA/DARP/reader sweeps. The plan identifies preparation/repair references and stop gates, not an executable protocol.

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §§6–7 (plan’s step 4); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md` (`CYCLE01-A`, `CYCLE01-B`); general report/protocol not present because this is roadmap-level planning.


<a id="pass-cycle01-b"></a>

### CYCLE01-B — Longer fresh-confirmation comparison (proposal)

**Type and status:** Next longer CYCLE01 proposal; `NEXT_LONGER_PROTOCOL_AND_RESERVED_RUN_NOT_STARTED`. No confirmation run occurred.

**Broad and specific question:** Does learning keep accumulating over several nights, rather than merely producing one successful accepted update? More specifically, can accepted history survive a longer sequence that includes a no-update night and a late new correction, while a control separates balanced replay from the benefit of simply receiving more B practice?

**Proposed systems and arms:** Start from all four original parents and retain each branch’s own accepted history. Include at least fixed/current-evidence, acquisition-only diagnostic, ordinary A replay, and balanced A/current-B repair. Add the straightforward equal-extra-B-exposure (B96-only) control before attributing benefit to joint replay. The exact procedure-learning arm and number of nights are not locked in the consulted status record. CYCLE01-B is not a completed subpass of CYCLE01-A.

**Method, split and decision criteria:** The embedded CYCLE01-A report explicitly calls for “one longer, fresh-confirmation” comparison and says to bind equal B exposure and separate screening from reserved evaluation before running. The checklist calls for several nights, a no-update night and a late correction. The larger plan prescribes accepted-branch histories, protected prior model during each simulated day, and reporting per-event plus whole-task old-skill retention. No cycle count, evaluation-family counts, thresholds, seeds, budgets, resource limits or exact split have been fixed in the material consulted. Those unknowns must remain open rather than be supplied by inference.

**Results and limits:** Not started. The CYCLE01-A signal is development-only and cannot be re-used as fresh confirmation. No adoption decision, superiority, cumulative learning or qualification follows from the proposal.

**Source locators:** `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/REPORT.md`, §§6–10; `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md`, CYCLE01-B row; `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §6. The exact protocol and reserved evaluation have not been created in the cited source set.


<a id="pass-balance01"></a>

### BALANCE01 — Current-evidence rehearsal crossed with update size (proposal)

**Type and status:** Named planning proposal only, `PROPOSAL_ONLY_NOT_RUN`. No BALANCE01 experimental arm or result is established.

**Broad question:** Can replay protect old behavior while still giving the learner enough exposure to current facts, and does a gentler update reduce the tradeoff?

**Specific question:** Relative to ordinary old-task A replay, does including the current B evidence during repair improve new-cue retention, and does crossing that replay condition with a smaller/gentler update step improve old-task behavior without simply suppressing learning?

**Proposed systems and arms:** The evidence plan describes **current-B plus A replay** crossed with a **gentler update rate** as factors. Exact factor levels, arm labels, paired seeds, architecture, optimizer schedule and endpoint count are not exposed in the plan/checklist excerpt and remain unspecified here. Ordinary A-only replay and a no-update/frozen reference are implied as comparisons in the larger CYCLE roadmap, but are not silently assigned as finalized BALANCE01 arms.

**Method and criteria:** Proposal source says to use the original bounded comparison or explicitly adapt those factors into CYCLE01; do not execute both merely to duplicate evidence. It conditions reuse of the older numerical path on prospective diagnosis of exposed numerical cases and a frozen verifier; that diagnosis is not a BALANCE01 result. The detailed protocol, train/dev/confirmation split, seeds, exact update dose, data, resource cap and decision bands were not found among the reviewed source texts.

**Results and distinction from CYCLE01-A:** Not run as BALANCE01. CYCLE01-A had an arm named BALANCED that paired A replay with current B at fixed learning rate and had unequal B exposure relative to alternatives; it did not cross update rate and did not include a B96-only equal-exposure control. The later CYCLE report explicitly states the extra-B exposure confound. Its 5/8 accepted candidate nights, 32/32 current cues and retention outcomes belong only to CYCLE01-A and are not BALANCE01 evidence.

**Meaning and limits:** BALANCE01 is an untested factorized proposal with no effect estimate. It should not be called successful from a similarly named CYCLE01-A arm.

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §§1–2 and source register S05 (named `NSS_NBR02_BALANCE01_Proposal_v0.1.md`); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md`, BALANCE01 row and optional branch table. The named BALANCE01 proposal source was not present in the bounded workspace scan.


<a id="pass-direct01-spec"></a>

### DIRECT01-SPEC — Parallel structured output versus autoregressive readout (proposal)

**Type and status:** Documentation complete, experiment not run (`DOCUMENTATION_COMPLETE_EXPERIMENT_NOT_RUN`; checklist short label `SPEC_READY_CONDITIONAL_NOT_RUN`). No model, hardware, tokenizer, source revision, threshold, data split or execution budget has been selected. This is a separate optional readout-interface hypothesis, not a DARP continuation or replacement architecture.

**Broad question:** Can a shared, competent representation support a useful direct parallel structured-output interface, and when is it a better quality/cost choice than a conventional autoregressive output path?

**Specific question:** On a fixed trunk, shared evidence, task and field inventory, can a newly trained parallel readout predict a whole structured block jointly and meet the quality of a newly trained AR readout at lower declared cost, or improve quality at acceptable added cost?

**Proposed systems and controls:**

- **AR readout:** newly trained conventional autoregressive output interface, conditioning on the common representation and its own earlier generated fields, `p(y_j | h, y_<j)`. Normal incremental KV caching is allowed; a naive full-prefix implementation must not handicap it.
- **Direct parallel readout:** newly trained one-pass readout predicts all structured fields jointly from shared representation `h`, nominally `p(y_j | h)`. A factorized field head does not express every joint dependency; any shared slot processor/coordinator must be stated and included in cost.
- **Shared trunk and evidence representation:** frozen for the primary test; both new readouts see the same eligible examples, targets and task-state fields. Existing AR weights are not assumed plug-compatible with a new parallel head.
- **Exact-rule ceiling/reference:** used only where the target rule is genuinely known, to separate task/evidence limitations from the readout. It is a reference, not an equivalent trainable arm.
- **Optional single bounded repair:** allowed only as a separately labeled secondary test on fixed drafts with checking, training and inference costs charged. Primary arms receive no checker feedback or repair; the checker only scores/rejects the initial output.

Both primary arms emit the same ordered field/value inventory using the same exact serializer and outer wrapper; wrapper fields must not leak target values. If fields are atomic labels, AR is described as a semantic-field decoder rather than unrestricted native next-token generation. If they are text spans, tokenizer, boundaries and parsing must be frozen. Multi-block handoffs feed each arm its own prior output under one predeclared continuation/rejection rule—no substitution of gold context after a failure. Cache invalidation must follow source, model, task state, prefix and tokenizer changes.

**Proposed data/method and measurements:** Use deterministic structured families requiring field coordination: independent fields, order/action changes, a field that changes completion status, and dependent continuation across blocks. Split development and untouched confirmation by histories/task families, not random output tokens. Pair AR and parallel on identical histories; treat histories as task units, inherited trunks as clusters and readout seeds as nested repeats. A shared backbone is not multiple independent pretrained models. Standard teacher forcing is allowed but generated-prefix mismatch must be recorded. Source extract does not select family sizes, seeds, optimizer, model identity, hardware or numerical acceptance bands; establish feasibility during bounded development and freeze any bands before reserved confirmation.

Score raw candidates, field correctness, whole-record/handoff validity, cross-field/order consistency, false completion and exact-checker acceptance separately. Preserve invalid candidate outputs even when blocked. An exact structural checker is not a semantic oracle for language; where needed use source-grounded independent rubric and adjudicated sample or call the family unresolved. Predeclare `ΔQ = Q_parallel − Q_AR`, one primary measured cost quantity `C`, and `R_C = C_parallel/C_AR`; show each seed/parent and critical-error category rather than hiding regressions in pooled averages. If training/preparation is amortized, specify serving horizon `n` and show `T_prep + T_train + n*T_serve` alongside unamortized cost. Measure parameter/checkpoint bytes, training targets/tokens/compute, per-phase time, cold/warm inference, actual input/output tokens, peak/retained RAM/VRAM, cache lifetime, checker/repair and full task latency; keep heterogeneous resource units separate.

**Result/status:** No DIRECT01 model, readout, fit, scoring or runtime result exists. The documented design allows “quality win,” “cost win within quality/critical-error bounds,” “tradeoff,” “no useful difference,” “mechanism failure,” or “technical stop,” but numerical gates must be declared after bounded feasibility rather than borrowed from DARP03. It remains conditional after a competent COMP01 task or a live output bottleneck; a retained four-field task is mechanism-only and cannot establish companion language competence.

**Meaning and limits:** This proposal makes the vague phrase “direct generation from weights” testable as a trained output interface while preserving the conditioning difference. It does not suggest weights are prompt-addressable finished answers, assume parallel outputs are free or jointly coherent, restore multi-core architecture, or establish superiority.

**Source locators:** `Research/NSS_DIRECT01_Chat_Handoff_v0.1.md` §§1–7; original source plan is named and copied with extracted text in `Research/NSS_DIRECT01_Chat_Handoff_v0.1.zip::NSS_DIRECT01_Chat_Handoff_v0.1/sources/NSS_Evidence_Led_Research_Plan_v0.1.docx` and `Research/NSS_DIRECT01_Chat_Handoff_v0.1.zip::NSS_DIRECT01_Chat_Handoff_v0.1/sources/PLAN_TEXT.txt`; checklist `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/provenance/CHECKLIST_v0.19.md`, DIRECT01-SPEC row. DARP motivating results are reported in `NSS_DARP_Research_Results_Analysis_and_Decision_v1.0.docx` §§13–18, summarized in this compendium’s DARP03 entry.


<a id="pass-lb01"></a>

### LB01 — Low-bit inference weights and recurrent state (protocol proposal)

**Type and status:** First low-bit research lane identified by BRIDGE01; proposal/protocol preparation only. No quantization, low-bit kernel, inference comparison or run is documented.

**Broad question:** Can the same retained learned behavior run with lower-precision weights or recurrent state without losing required decisions, numerical behavior or state continuity, and does the change reduce the measured cost that matters?

**Specific question:** Against a declared float32 working reference, what sensitivity and resource changes follow from testing lower-bit weight storage/precision (candidate 8-bit and 4-bit) and recurrent-state precision separately on fixed event traces?

**Proposed systems and controls:** The four frozen BRIDGE recurrent parents 4101–4104 provide a small controlled fixture; preserve one float32 working reference. Test weight precision while holding recurrent-state precision fixed, then state precision while holding weights fixed. The BRIDGE review says no automatic full precision cross-product. Exact record IDs, source events, action receipts and task semantics remain lossless/exact. Dequantize-then-float is a numerical sensitivity instrument, not a native low-bit execution arm; native packed/kernels must be labeled separately. Separate quantization granularity, scales, packed checkpoint bytes, working tensor memory and process overhead.

**Method and criteria:** Pin the four checkpoint identities and fixed event fixtures; specify precision map, quantizer and scales, calibration/development/confirmation split, seeds, acceptable advisory errors, critical failure rules, target hardware/runtime and resource caps before a future run. Report exact traces and source/class outcomes, state continuity after restart, storage bytes, peak memory and timing separately. No exact seed/split sizes or quantitative quality/resource gates are present in the review; those remain to be fixed in an authorized protocol.

**Arms/results:** Only proposed. There is no float32 baseline newly run for LB01 and no 8-/4-bit outcome. BRIDGE01’s existing runtime uses float64 arrays and makes no low-bit measurements; existing parent files are float32 source arrays. The proposed float32 control should therefore be a prospectively declared baseline, not confused with the BRIDGE execution representation.

**Meaning and limits:** This is a precision-sensitivity and resource-accounting study, not an already demonstrated storage or speed gain. Small recurrent fixtures can reveal numerical sensitivity but cannot establish quantized language-model behavior or system affordability. Weight quantization alone does not establish lower state or training-memory cost.

**Source locators:** `Research/NSS_NBR02_BRIDGE01_Low_Bit_Review_v0.1.md` §§1–4; `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §§8–9 (LB01 table/priority); retained model and fixture identities are described at `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §§2–6 and §9. The low-bit protocol itself was not present.


<a id="pass-lb02"></a>

### LB02 — Compressed learning-state memory (proposal)

**Type and status:** Proposed low-bit training-memory lane; not run.

**Broad question:** Can the system perform useful full-parameter adaptation and recovery while using less training-state memory, without hiding a large uncounted high-precision learner underneath?

**Specific question:** Under a real old/new-task learning objective, how does an ordinary full-precision optimizer-state reference compare with one compressed-state method on learning the new behavior, preserving old behavior, interruption/resume and measured total cost?

**Proposed systems and accounting:** Compare standard full-precision optimizer state against one declared compressed optimizer-state method. Keep full-parameter adaptation as the actual objective; a frozen quantized base with trainable adapters would answer a different, adapter-specific question. Report weights, persistent trainable parameters, gradients, optimizer moments/state, activations, recurrent state, accumulators/master copies, residuals/scales and restart snapshots separately. Four-bit moment compression reduces optimizer-state width only; it does not mean four-bit weights or learning directly in low-bit persistent parameters.

**Method and criteria:** Retain current- and old-task checks plus exact update/resume behavior; count preparation and training work, memory peak/storage and numerical/behavioral outcome. Select one compressed-state method based on the measured target bottleneck and define fairness, seeds, data split, caps and stop rules in a future versioned protocol. No optimizer, state format, quantizer, model, fixture, seed, split, threshold or run budget is yet selected.

**Results and limits:** No LB02 training or compressed optimizer-state result is documented. This proposal does not qualify QLoRA, four-bit moments, quantization-aware training or native low-bit parameter learning. A broad claim that all learning memory has been compressed would require counting every auxiliary high-precision state.

**Source locators:** `Research/NSS_NBR02_BRIDGE01_Low_Bit_Review_v0.1.md` §§2–4; `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §8 (LB02 lane and distinctions among inference/storage/training); the cited papers are literature motivation, not NSS results.


<a id="pass-lb03"></a>

### LB03 — More aggressive precision and low-bit update paths (conditional proposal)

**Type and status:** Conditional future proposal; explicitly gated on informative simpler low-bit outcomes; not run.

**Broad question:** Can more aggressive precision retain useful inference or learning behavior without concealing a full-precision parameter/trace representation that dominates memory?

**Specific question:** Only if LB01/LB02 establish an informative use case, do 4-bit, ternary or 2-bit weights/updates, accumulation and rounding choices, and trace-specific hypotheses produce a useful measured path?

**Proposed systems and controls:** Potential precision points are named but no exact arm or quantization method is selected. Compare against declared higher-precision references; distinguish packed parameter storage from working arithmetic, simulated/dequantized execution from native kernels, and low-bit forward values from higher-precision gradients/master accumulators. If those hidden higher-precision arrays are used, count them. Trace-specific ideas include eligibility traces/updates, but are not the same as quantized inference weights or optimizer moments.

**Method/status:** Conditional only. Precision maps, specific methods, dataset, splits, seeds, hardware, limits and decision bands are unselected; there is no experiment or result.

**Meaning and limits:** Ternary/2-bit language about a model representation must not be mistaken for an entirely ternary training system. This lane is a later hypothesis, not evidence of low-bit NSS performance or proof that such compression is needed.

**Source locators:** `Research/NSS_NBR02_BRIDGE01_Low_Bit_Review_v0.1.md` §§2–4; `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §8 (LB03 conditional lane, held behind low-bit inference/training protocol and results).


<a id="pass-adapt01"></a>

### ADAPT01 — One computation-preserving update mechanism (conditional proposal)

**Type and status:** Conditional roadmap proposal, not executed. The 2026-09-29 BRIDGE report places ADAPT01 and malleable-representation work on hold while low-bit inference/training has current priority.

**Broad question:** Can a distinct update or representation mechanism reduce interference observed across accepted learning cycles while still acquiring genuinely new procedures?

**Specific question:** On an adequate recurrent task/reference, can an activity-defined subspace or other computation-preserving update protect old dynamics while allocating capacity for new computations, beyond ordinary replay and a matched step-size/applied-norm control?

**Proposed systems and controls:** The evidence-led plan names activity-defined recurrent subspaces, motivated by Duncker et al., as the first mechanism to investigate. It distinguishes this from PROTECT01’s first-order old-output-margin projection, which is a different intervention and stopped at development admission. The proposed comparison is the selected replay reference, the same learner with the new protection/update method, and a step-size/applied-norm control. No concurrent mechanism bundle or tri-core reintroduction is implied.

**Method and criteria:** First derive and document equations/assumptions on a named recurrent model, including which source-method assumptions transfer. If COMP01 uses a nonrecurrent trunk, use a separately identified recurrent prototype or a supported alternative. Match authorized experience and evaluation obligations; count subspaces, stored trajectories, projection work and preparation. Require new-task acquisition, continued old-task performance beyond initial answer, rare-behavior retention and measured repair burden. Freezing/copying weights is containment, not evidence of learned compatibility. A valid exit is a useful gain at measured cost or a documented tradeoff/failure and park decision; failure of one bounded preparation does not disprove every mechanism.

**Results and limits:** No ADAPT01 method, model, arm, equation, fit, evaluation or resource result is documented. PROTECT01 evidence is not an ADAPT01 implementation; the proposal is conditional on an informative CYCLE01 mechanism failure or justified scoped question.

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §§8 and 10–11, particularly step 5 and source P04; `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §8 (ADAPT01 explicitly on hold); checklist v0.19 conditional/research-status table.


<a id="pass-budget01"></a>

### BUDGET01 — Measure and reduce a demonstrated resource bottleneck (proposal)

**Type and status:** Conditional roadmap proposal; no BUDGET01 experiment is documented. The active BRIDGE-era priority is low-bit inference/training; general resource optimization remains a later or blocker-triggered lane.

**Broad question:** Which measured resource bottleneck prevents an otherwise useful NSS mechanism from being locally affordable, and can that specific cost be reduced without unacceptable capability loss?

**Specific question:** After measuring actual serving, preparation and maintenance costs on a declared device, does one targeted change in the dominant component improve affordability while meeting predeclared capability and failure requirements?

**Proposed systems and method:** First establish a named, feasible reference. Measure daytime serving, setup/preparation and maintenance learning separately; collect peak/retained RAM/VRAM, optimizer state, activations, caches, archive/storage traffic, cumulative tokens, wall time and energy where actually measurable. Select the intervention from measured bottleneck: e.g. if optimizer state dominates, compare the qualified standard optimizer against one factored/compressed-state method; if serving state dominates, compare an appropriate recurrent/local-attention or other efficient language baseline. G12 trace precision requires a real trace/update comparison with decay, accumulation, sign reversal, delayed feedback, stochastic-rounding state and resumed updates; compressed file bytes alone are not enough. Count residuals, scales, indices, decoding buffers and recomputation.

**Arms/results:** None selected, executed or measured. Griffin, Adafactor and low-bit optimizer references in the plan are literature controls or candidate methods, not completed NSS implementations. The lane can move earlier only when a measured hardware constraint blocks COMP01 or useful candidate learning; it is not authorization to change precision, backbone and learning objective simultaneously.

**Meaning and limits:** Past studies report per-component costs and caps, but they do not establish an NSS-wide budget winner or a universal future hardware limit. This proposal requires a specific bottleneck and a single interpretable change; no resource savings are yet demonstrated.

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §9 (step 6), §§11–12; `Research/NSS_NBR02_BRIDGE01_Low_Bit_Review_v0.1.md` §§1–4 (resource and precision distinctions); BRIDGE report `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §§6,8–9.


<a id="pass-int01"></a>

### INT01 — Integrate only components that earned a place (proposal)

**Type and status:** Conditional integration proposal; no INT01 study or integrated companion is documented. Current BRIDGE decision freezes broader integration while low-bit work has priority.

**Broad question:** Does a selected set of evidence, memory, preparation, learning and output components make a local companion more useful across repeated interaction than the simplest competent reference?

**Specific question:** Once a competent COMP/MEM reference exists and individual mechanisms show value, does adding each selected component in a controlled sequence improve end-to-end behavior over the base, including interactions and lifecycle costs?

**Proposed systems and method:** Begin with working COMP/MEM reference. Add only one supported component at a time: useful information preparation, selected nightly update policy, and any justified native attention/state component. Compare the combined version and remove components to isolate contributions and interactions. AR output and exact task checks can remain; DARP, multiple learned cores, or an old architecture do not enter by default. Measure against the simplest capable base over repeated interaction, not just module microbenchmarks.

**Results and limits:** Not begun. There is no qualified set of components, integration result, companion-level language outcome, full resource figure or deployment evidence. A successful isolated component or BRIDGE’s scripted bridge does not imply an INT01 benefit; an interaction must be measured. Foundation return FCR-0103-001 remains a roadmap checkpoint after NBR-03 and before NBR-04, not an executed integration experiment.

**Meaning:** INT01 is a decision-driven integration proposal, not a culmination already established by the separate HSA, DARP, reader or BRIDGE pass reports.

**Source locators:** `.consolidation/20260928/direct_generation/PLAN_TEXT.txt` §10 (step 7); `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip::NSS_NBR02_BRIDGE01_Prototype_v0.1/docs/ARCHITECTURE_AND_REPORT.md` §§8–9 (broader integration on hold); `RESEARCH_PLAN.md` §94 onward (current compendium task and scope boundary).


<a id="g01g22-question-map"></a>

## G01–G22 question map

The original question wording is preserved below. Links use the explicit broad-question associations in each entry index; an incidental mention of a question in a limitation does not count. These editorial associations do not imply original preregistration or declare a broad problem solved. The HSA branch also has its own HSC-Q taxonomy, retained in its entries.

| Original question | Compendium cross-references |
| --- | --- |
| **G01 · A** — Which mechanisms are supported in humans, other mammals or flies, and which are only analogies? | No specific pass linked in this snapshot; see the open research register. |
| **G02 · A** — Is a failure caused by architecture, insufficient training, poor data or weak interfaces? | [Q001](#pass-q001), [Q002](#pass-q002), [Q010-HIST](#pass-q010-hist), [Q010-INF-REC-v1.6](#pass-q010-inf-rec-v1-6), [TS01](#pass-ts01), [TS02-MW01](#pass-ts02-mw01), [TS03-CR01](#pass-ts03-cr01), [CKA01](#pass-cka01), [NeuralProbe001](#pass-neuralprobe001), [E20](#pass-e20), [COMP01-A](#pass-comp01-a), [COMP01-B/SETUP](#pass-comp01-b-setup), [LAB01](#pass-lab01), [LAB02-SIZE](#pass-lab02-size), [LAB02-BIND](#pass-lab02-bind), [LAB-READER-DECISION](#pass-lab-reader-decision), [READER-SUPPORT01](#pass-reader-support01) |
| **G03 · A** — What survives events, interruptions and restarts without transcript growth? | [Q001](#pass-q001), [Q002](#pass-q002), [Q003](#pass-q003), [Q004](#pass-q004), [Q005](#pass-q005), [Q006](#pass-q006), [Q007](#pass-q007), [Q009](#pass-q009), [Q010-HIST](#pass-q010-hist), [Q010-RECOVERY-BASE-v0.2](#pass-q010-recovery-base-v0-2), [Q010-INF-REC-v1.6](#pass-q010-inf-rec-v1-6), [CM01](#pass-cm01), [CM02](#pass-cm02), [TS01](#pass-ts01), [TS02-MW01](#pass-ts02-mw01), [TS03-CR01](#pass-ts03-cr01), [CKA01](#pass-cka01), [E19](#pass-e19), [E20](#pass-e20), [MEM01](#pass-mem01) |
| **G04 · A** — Does extra internal processing improve unfamiliar problems? | [Q001](#pass-q001), [Q006](#pass-q006), [Q010-HIST](#pass-q010-hist), [TS01](#pass-ts01) |
| **G05 · A** — Do feedback, quantization or stale state amplify errors or cause loops? | [Q003](#pass-q003), [Q004](#pass-q004), [E19](#pass-e19), [E20](#pass-e20) |
| **G06 · B** — Can entities, relations, quantities and actions be recombined without confusion? | [Q002](#pass-q002), [Q005](#pass-q005), [Q006](#pass-q006), [Q007](#pass-q007), [Q008](#pass-q008), [Q009](#pass-q009), [Q010-HIST](#pass-q010-hist), [Q010-RECOVERY-BASE-v0.2](#pass-q010-recovery-base-v0-2), [Q010-INF-REC-v1.6](#pass-q010-inf-rec-v1-6), [CM01](#pass-cm01), [CM02](#pass-cm02), [TS02-MW01](#pass-ts02-mw01), [TS03-CR01](#pass-ts03-cr01), [CKA01](#pass-cka01), [LAB02-BIND](#pass-lab02-bind) |
| **G07 · A** — What is lossless, what is approximate, and what must be rehydrated? | [Q002](#pass-q002), [Q003](#pass-q003), [Q004](#pass-q004), [Q005](#pass-q005), [Q007](#pass-q007), [Q008](#pass-q008), [Q009](#pass-q009), [Q010-HIST](#pass-q010-hist), [Q010-RECOVERY-BASE-v0.2](#pass-q010-recovery-base-v0-2), [Q010-INF-REC-v1.6](#pass-q010-inf-rec-v1-6), [CM01](#pass-cm01), [CM02](#pass-cm02), [TS02-MW01](#pass-ts02-mw01), [TS03-CR01](#pass-ts03-cr01), [MEM01](#pass-mem01), [PREP01](#pass-prep01) |
| **G08 · A** — Which past activity deserves which update? | [E07](#pass-e07), [E08](#pass-e08), [E09](#pass-e09) |
| **G09 · A** — Can new competence improve without destroying old competence? | [E07](#pass-e07), [E08](#pass-e08), [E09](#pass-e09), [E10](#pass-e10), [E11](#pass-e11), [E12](#pass-e12), [E13](#pass-e13), [E14](#pass-e14), [E17](#pass-e17), [E18](#pass-e18) |
| **G10 · A** — When does a candidate update become the serving revision? | [E08](#pass-e08), [E09](#pass-e09), [E13](#pass-e13), [E14](#pass-e14), [E15](#pass-e15), [E16](#pass-e16), [E19](#pass-e19) |
| **G11 · B** — Does sparsity reduce actual work and memory, not just nonzero counts? | No specific pass linked in this snapshot; see the open research register. |
| **G12 · A** — Can traces and updates retain useful information at 1–2 bits? | No specific pass linked in this snapshot; see the open research register. |
| **G13 · A** — Do predictions remain useful under new states, actions and longer horizons? | No specific pass linked in this snapshot; see the open research register. |
| **G14 · B** — Does idle computation improve later work beyond extra data or ordinary search? | [E11](#pass-e11), [E12](#pass-e12), [E13](#pass-e13), [E14](#pass-e14), [E17](#pass-e17), [E18](#pass-e18), [PREP01](#pass-prep01) |
| **G15 · B** — Does affect improve priorities without becoming fact, permission or pressure on the user? | No specific pass linked in this snapshot; see the open research register. |
| **G16 · A** — Can the critic catch unsupported claims while preserving useful supported answers? | [E15](#pass-e15), [E16](#pass-e16), [LAB-SEMANTIC-REVIEW](#pass-lab-semantic-review), [READER-SUPPORT01](#pass-reader-support01) |
| **G17 · A** — Do cores actually use exchanged information, and does it survive revision changes? | [TS01](#pass-ts01), [TS02-MW01](#pass-ts02-mw01), [TS03-CR01](#pass-ts03-cr01), [NeuralProbe001](#pass-neuralprobe001) |
| **G18 · A** — What does always-active Primary participation cost with alternating auxiliaries? | [E18](#pass-e18) |
| **G19 · B** — Can competence, memory use and agreed defining behavior survive replacement? | No specific pass linked in this snapshot; see the open research register. |
| **G20 · A** — Can generated material leak into facts, permissions or unauthorized learning? | No specific pass linked in this snapshot; see the open research register. |
| **G21 · A** — Can NSS manage approved jobs through the same engine as ordinary LLM training? | No specific pass linked in this snapshot; see the open research register. |
| **G22 · C** — Does the combination earn its complexity and scale? | No specific pass linked in this snapshot; see the open research register. |

## Historical candidate-review register

These retained analytical passes proposed successors or alternatives. They did not themselves execute the proposed systems; their empirical outcomes belong to the separately indexed studies above. The headings below preserve each review's candidate scope, including conditional and deferred alternatives. Exact full candidate documents, including their proposed methods and controls, are included in the evidence bundle. Later execution can differ from these earlier proposals, so use the executed study's protocol for interpreting its results.

| Review source | Candidate questions / directions recorded in that review | Outcome of this document |
| --- | --- | --- |
| `Research/NSS_CM02_PostResults_Candidates_v0.1.zip::NSS_CM02_PostResults_Candidates_v0.1/CANDIDATES.md` | Priority: learned task-progress state; Conditional: explicit retrieval-time intent; Conditional: public evidence of intent | Analysis/specification; no execution result in this review |
| `Research/NSS_CM_Theoretical_Candidates_v0.1.zip::NSS_CM_Theoretical_Candidates_v0.1/CANDIDATE_REVIEW.md` | Recommended: public-reference continuity and freshness; Conditional: residency, consultation and refresh economics; Deferred: extra task/recurrent state and learned native memory | Analysis/specification; no execution result in this review |
| `Research/NSS_NBR02_DC01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | Proposed REV01 protocol for review, NOT_RUN | Analysis/specification; no execution result in this review |
| `Research/NSS_NBR02_PROTECT01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | Prospective admission repair, not a retroactive pass; REHEARSE01 comparison | Analysis/specification; no execution result in this review |
| `Research/NSS_NBR02_REV01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | PROTECT01 — directional protection at the first lawful correction (preferred); PAIR01 — same-prestate attribution diagnostic (optional); REHEARSE01 — equal-extra-work old replay (alternative) | Analysis/specification; no execution result in this review |
| `Research/NSS_NBR02_Theoretical_Candidates_v0.1.zip::CANDIDATES.md` | Proposed DC01 v0.2 contract for Chat to freeze | Analysis/specification; no execution result in this review |
| `Research/NSS_TS01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | Priority: NSS-TS02-MW01, bounded maintained workspace alongside learned state; Conditional: workspace consultation and rewrite policy; Conditional: representation and repair | Analysis/specification; no execution result in this review |
| `Research/NSS_TS01_PostResults_Candidates_v0.2.zip::CANDIDATES.md` | Priority: NSS-TS02-MW01, bounded maintained workspace alongside learned state; Conditional: workspace consultation and rewrite policy; Conditional: representation and repair | Analysis/specification; no execution result in this review |
| `Research/NSS_TS02_MW01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | Priority: NSS-TS03-CR01, compositional repair and raw-binding fidelity; Conditional: constrained head consistency; Conditional: representation and write policy | Analysis/specification; no execution result in this review |
| `Research/NSS_TS03_CR01_PostResults_Candidates_v0.1.zip::CANDIDATES.md` | Ranked directions; Proposed economical next specification: NSS-NBR02-DC01, review only | Analysis/specification; no execution result in this review |
| `Research/Q010_PostRecovery_Candidates_v1.0.zip::CANDIDATES_v1.0.md` | Priority: public evidence, identity admission and abstention; Conditional: test shared-store maintenance cost; Conditional: hard-negative training only if candidate 1 finds separable cues | Analysis/specification; no execution result in this review |
| `Research/NSS_NBR02_REHEARSE01_ProtocolReview_v0.1.zip::NSS_NBR02_REHEARSE01_ProtocolReview_v0.1/REVIEW.md` | Recommendation: specify one REHEARSE01 recovery experiment, then seek user execution authorization; What the source actually recommends; Reviewer completions, not claims already proved by Codex; What deserves caution; Evidence review performed here; Codex continuity | Analysis/specification; no execution result in this review |

## Archive coverage and provenance

This directory-level coverage list accounts for all canonical ZIPs considered. Execution bundles, post-result proposals, handoffs, copies and storage-preservation archives are not counted as separate scientific experiments merely because they have different filenames. Nested HSA original archives and Q010 recovery evidence are located in their pass entries. Paths are relative to the NSS workspace.

| Canonical archive | Bytes | Role in the compilation |
| --- | ---: | --- |
| `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip` | 51,690,328 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/Foundations/MegaMindAlpha_v0.4.14_PersistentState001.zip` | 28,327,938 | Engineering foundation and archived validation records |
| `Research/Foundations/MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip` | 28,558,869 | Engineering foundation and archived validation records |
| `Research/NSS_C00_Contract_Complete_v0.2.zip` | 7,447,771 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_CM01_Execution_v0.2.zip` | 15,265,242 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_CM02_Execution_v0.6.zip` | 13,701,695 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_CM02_PostResults_Candidates_v0.1.zip` | 28,040 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_CM_Theoretical_Candidates_v0.1.zip` | 21,396 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_DIRECT01_Chat_Handoff_v0.1.zip` | 173,526 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_LogicAtlas_HistoricalSource_v0.1.zip` | 38,101,127 | Historical source / preservation container; linked records, not an extra scientific run |
| `Research/NSS_NBR01_BindingDepth006_v0.1.zip` | 15,610,434 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_ExistenceContent005_v0.1.zip` | 6,869,840 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_HorizonBinding002_v0.1.zip` | 1,253,062 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_IdentityBinding009_v0.1.zip` | 242,997,220 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_MembershipRepair008_v0.1.zip` | 67,089,372 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_Q010_Chat_Handoff_v1.0.zip` | 28,207,060 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR01_RepairBinding007_v0.1.zip` | 3,821,479 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_StateDepth_Pilot001_v0.1.zip` | 1,334,154 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_StateRecovery003_v0.1.zip` | 1,527,576 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR01_WritableEmpty004_v0.1.zip` | 1,797,875 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_BRIDGE01_Codex_Review_v0.1.zip` | 150,152 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_BRIDGE01_Prototype_v0.1.zip` | 7,732,985 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_DC01_Codex_Handoff_v0.5.zip` | 52,630 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_DC01_PostResults_Candidates_v0.1.zip` | 65,341 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_NBR02_EVAL01_Complete_v0.2.zip` | 46,726,962 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_MICROMACRO01_Complete_v0.2.zip` | 70,437,319 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_PROTECT01_Codex_Handoff_v0.3.zip` | 196,510 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_PROTECT01_Development_Stop_v0.3.zip` | 25,494,039 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_PROTECT01_PostResults_Candidates_v0.1.zip` | 204,554 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_NBR02_RECOVER01_Proposal_v0.1.zip` | 12,680 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_NBR02_REHEARSE01_Development_Stop_v0.2.zip` | 25,131,512 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_REHEARSE01_ProtocolReview_v0.1.zip` | 92,746 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_REV01_Codex_Handoff_v0.4.zip` | 177,099 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_REV01_Complete_v0.4.zip` | 20,961,112 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_REV01_PostResults_Candidates_v0.1.zip` | 205,148 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_NBR02_STATEBRIDGE01_Diagnostic_v0.2.zip` | 121,534,068 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_SURFACE01_Execution_v0.1.zip` | 32,141,227 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_NBR02_SURFACE01_Reports_and_Review_v0.1.zip` | 27,000 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_NBR02_Theoretical_Candidates_v0.1.zip` | 65,414 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_NBR02_TIMING01_Complete_v0.1.zip` | 37,195,996 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/NSS_RecycleRecovery_v0.1.zip` | 29,795,262 | Historical source / preservation container; linked records, not an extra scientific run |
| `Research/NSS_Research_and_Architecture_Chat_Handoff_v1.0.zip` | 42,458 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_Research_Consolidation_v0.1.zip` | 502,007 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_Research_Log_NBR02_Handoff_v0.1.zip` | 48,987 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_TS01_PostResults_Candidates_v0.1.zip` | 22,475 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_TS01_PostResults_Candidates_v0.2.zip` | 22,690 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_TS02_MW01_PostResults_Candidates_v0.1.zip` | 28,219 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_TS03_CR01_Codex_Handoff_v0.4.zip` | 47,114 | Report, review, handoff or consolidation; preserves evidence and/or proposals |
| `Research/NSS_TS03_CR01_PostResults_Candidates_v0.1.zip` | 60,785 | Prospective or post-result direction; separate from observed outcomes |
| `Research/NSS_WorkspaceSupport_v0.1.zip` | 208,360,227 | Historical source / preservation container; linked records, not an extra scientific run |
| `Research/Q010_InferenceRecovery_v1.6_RecoveryContext.zip` | 48,654,694 | Retained study/prototype result bundle; see individual evidence boundary |
| `Research/Q010_PostRecovery_Candidates_v1.0.zip` | 21,657 | Prospective or post-result direction; separate from observed outcomes |

## Evidence-bundle guide

The [companion ZIP](NSS_Research_Compendium_v1.0.zip) contains this Markdown, a standalone printable HTML edition, a machine-readable pass index, the archive coverage inventory, the source-report index and 77 preserved documentary sources. It deliberately does not duplicate all model checkpoints and large raw execution logs; their original archive/member locations are provided throughout.

After extracting the ZIP, open `SOURCE_REPORTS_INDEX.md` for links to the original report copies, including the Q001–Q009 reports, E00–E19 reports, SURFACE01, foundation audit reports, the six HSA studies, DARP consolidation, BRIDGE01 and its provenance report. Source copies retain their original contents; internal links in those original reports may refer to files in their full execution archives rather than this documentary bundle. `SOURCE_REPORTS.json` records exact source locators, byte counts and hashes.

The pass index and this narrative are complementary: the narrative explains systems, methods and meaning; the inventory makes omission/status checking possible. A source reference is not evidence that missing original execution bytes have been recovered. Current low-bit priority does not erase historical failures or turn unexecuted candidates into results.
