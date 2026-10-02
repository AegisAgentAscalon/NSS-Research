# NSS NBR02 CAP02 — Larger-layout preparation and bounded closeout v0.1

**Disposition: COMPLETE_BOUNDED_PREPARATION; SEGMENTED-CONTEXT/HSA COMPONENT PARKED FOR INTEGRATION.** One fixed-budget follow-up completed. No tuning loop, extra hierarchy level, seed replacement, best-checkpoint selection, or DARP run. Mixed-size preparation substantially improved the existing HSA reader on fresh128-task layouts and retained its eight-task skill. A separate512-task stress remains imperfect. This is sufficient evidence for a bounded working component, not general NSS qualification or proof of unique custom segmentation superiority.

**Execution receipt date:** 2026-09-28T12:38:46.030357+00:00. Main optimizer applications **1152**; disposable preflight applications **3**; total **1155**. Twelve continuation branches from six exact existing parents; zero random-initialized refits. Original source parents and historical findings remain unchanged.

## 1. What was compared
The six CAP01 dense/HSA checkpoints (paired seeds8801,8802,8804) retain37 engineered input features,18,500 parameters,two attention blocks,and task/region/global topology. Each has U(untouched),S(96 extra updates on8-task worlds),and M(96 updates cycling8,32,128-task worlds). Every update supervises exactly eight selected decisions in each of four worlds:32 labels/update and3072 per continuation. Corresponding eight-task steps use identical data. All weight tensors may learn.

Fresh AdamW,lr0.0005,weight decay0.01,betas0.9/0.999,eps1e-8,clip1.0; no schedule, early stopping or endpoint selection. Optimizers reset for each branch. Checkpoints retained at0,24,48,72,96; only fixed96 endpoints evaluated. The M condition uses more source records and computation; equal update and label counts are NOT equal FLOPs, information, or runtime. No claim of training efficiency follows.

Training uses resident source graphs, not a32-record training limit. CAP01 streaming is separately checked after learning. No summaries, JSON-language models, learned segmentation, or new procedural rules were introduced.

## 2. Fresh evidence and denominators
Training has640 unique worlds; each curriculum presents384 worlds, with128 shared. New confirmation has32 independent nonfrozen worlds plus8 separate frozen controls at each of8/32/128 tasks; the independent512-task stress has8 nonfrozen worlds plus2 frozen controls. Total130 worlds, common across all models and branches. No confirmation scoring occurred until all12 continuations completed.

The primary job consists of eight randomly selected task decisions, NOT every task in the archive. Thus each primary size contributes32worlds×3models×8targets=768 paired decision observations and96 eight-answer jobs per reader/arm. The512 stress contributes192 observations and24 jobs. Shared worlds across seeds/arms are repeated comparisons, not independent random problems. Secondary all-task outputs are also saved to avoid hiding errors outside the selected targets.

World hashes excluding their ID have zero exact train/confirmation overlap and zero overlap with9952 retained SH01 fixture fingerprints. New dependencies are distributed across regions. Public prerequisite identities remain supplied metadata; the model predicts the same immediate-prerequisite/freeze/completion rule, not unfamiliar transitive reasoning.

## 3. HSA primary result (exclude easy all-DEFER controls)

| Source tasks | Untouched U | Small-only S | Mixed-size M | Whole eight-answer jobs U → M |
|---|---|---|---|---|
| 8 | 767/768 (99.870%) | 768/768 (100.000%) | 768/768 (100.000%) | 95/96 (98.958%) → 96/96 (100.000%) |
| 32 | 762/768 (99.219%) | 767/768 (99.870%) | 767/768 (99.870%) | 91/96 (94.792%) → 95/96 (98.958%) |
| 128 | 749/768 (97.526%) | 730/768 (95.052%) | 766/768 (99.740%) | 80/96 (83.333%) → 94/96 (97.917%) |
| 512 | 175/192 (91.146%) | 177/192 (92.188%) | 189/192 (98.438%) | 11/24 (45.833%) → 21/24 (87.500%) |

The512 row is separate beyond-training-size stress, not pooled primary qualification. Mixed preparation trains only through128 tasks.

At128 tasks, wrong selected answers fall19→2, and entirely correct jobs rise80/96→94/96. M meets the prospective descriptive95%decision/90%represented-class macro recall/90%whole-job working points at8,32,128. At512 it reaches98.4375% selected-answer accuracy but87.5% whole-job accuracy, below the90% job working point. That known stress limitation stays open rather than triggering further tuning.

Eight-task retention is100% for every HSA M parent: all768 selected/all-task answers and96 jobs correct. It repairs the one pre-existing miss and introduces no eight-task errors. This is retention of this narrow rule, not companion identity or broad skill retention.

### Paired128-task HSA results
| Parent | U | S | M |
|---|---|---|---|
| 8801 | 242/256 (94.531%) | 220/256 (85.938%) | 256/256 (100.000%) |
| 8802 | 252/256 (98.438%) | 254/256 (99.219%) | 255/256 (99.609%) |
| 8804 | 255/256 (99.609%) | 256/256 (100.000%) | 255/256 (99.609%) |

M improves on U in two parents and ties its accuracy in the third; it beats S in two and is one answer worse in the third. The effect is not uniformly favorable at every position or seed. S's aggregate128-task accuracy falls to95.052%, despite improving eight-task performance to100%; practice coverage matters in this recipe, not simply more updates.

## 4. Do not hide collateral errors
At128, M fixes all19 of U's originally wrong selected positions but introduces two new errors elsewhere. One is a false BLOCKED on an already-complete task (8802), the other a false COMPLETE on a blocked task (8804). Net improvement19→2 is meaningful, but not error-set-perfect recovery. At32, one pre-existing false COMPLETE from8804 remains. At512, three false READY answers remain; M repairs14 of17 U errors there without introducing new selected errors. All selected failure records retain source identity, prerequisite IDs/progress, predicted/true classes and logits in`failures/SELECTED_BEHAVIORAL_ERRORS.json.gz`.

The full all-task secondary check also improves at128: HSA U11962/12288 (97.347%) → M12275/12288 (99.894%), versus S11675/12288. At512 U11178/12288 → M12083/12288. These full-world diagnostics are not the same denominator as selected eight-answer jobs; raw arrays retain all mistakes.

All HSA frozen-control decisions are correct in U/S/M. Dense has isolated frozen-control failures (one U8; one U/S/M512). They are recorded separately rather than blended into the nonfrozen headline.

## 5. Dense comparison: retained but not overclaimed
| Source tasks | U | S | M | M whole jobs |
|---|---|---|---|---|
| 8 | 694/768 (90.365%) | 698/768 (90.885%) | 692/768 (90.104%) | 42/96 (43.750%) |
| 32 | 655/768 (85.286%) | 654/768 (85.156%) | 654/768 (85.156%) | 29/96 (30.208%) |
| 128 | 592/768 (77.083%) | 604/768 (78.646%) | 624/768 (81.250%) | 26/96 (27.083%) |
| 512 | 111/192 (57.812%) | 101/192 (52.604%) | 136/192 (70.833%) | 1/24 (4.167%) |

Dense receives identical continuation examples and target labels. Its M128 selected accuracy improves77.083%→81.250%;512 improves57.813%→70.833%. It remains substantially weaker on this fixed recipe. The inherited dense parents were already weaker after SH01 training;96 additional updates do not establish that dense attention was optimally prepared or intrinsically cannot solve the task. This is a bounded same-recipe comparison, not a universal architecture ranking.

## 6. Cross-segment compatibility after learning
All six M endpoints were checked on the first nonfrozen32- and128-task confirmation worlds using unchanged CAP01 streaming with32 active record positions. All12 checks completed. Full first-layer/selected-second-layer outputs, stream logits and prepared resident logits were compared against the original same-weight resident source reader.

Across89,952 scalar comparisons there were **0 tolerance violations** and zero class differences. The unchanged float32 envelope is`2e-5 + 2e-5*abs(reference)`; maximum absolute discrepancy6.198883056640625e-6. Peak counted active positions remained32. These12 checks establish compatibility on their declared subset, not streamed execution of every confirmation world or32-token/total-memory training.

CAP01 previously showed ordinary multi-pass retrieval can obtain the same capacity. This training comparison does not reassign that gain to custom segmented grouping.

## 7. Verification, operational incidents and costs
Preflight passed12 named checks: four compiler-byte tests, two packed-vs-masked output/gradient tests, independent labels, deterministic optimizer resume/parent isolation, three injected faults, and paired schedule/target counts. Three disposable optimizer applications tested exact resume. Source/input lock contains18 objects and remained intact.

All12 trained branches finished96 steps. All18 U/S/M endpoints were evaluated on all130 worlds:2340 endpoint/world records,18720 selected decision observations,and213120 all-task prediction observations. Independent vector/scalar recount found zero discrepancies. All60 continuation checkpoint parameter hashes and parent links matched. A fresh process replayed every endpoint/world logit array bit-for-bit (18 files,2340 worlds,852480 score scalars); zero replay mismatches. This is internal repeatability, not third-party replication.

One pre-lock syntax error in the new evaluation record writer was caught before data preparation or model work. The two rejected parse attempts and failed source are retained; no optimizer work occurred. The closing brace was repaired before preflight/main lock. No main interruption, replacement, budget extension, post-result recipe change, numerical-gate relaxation, or extra optimizer step occurred.

Tracked main command cores summed22.073s including training precompilation, training, endpoint evaluation and the12 streaming checks. This excludes interpreter/import overhead outside the timers, source writing, fixture preparation(2.819s),preflight(0.416s),post-result audit(7.708s),packaging and analysis. It is NOT the entire research wall time. Peak recorded main-process RSS was399,749,120bytes and includes resident training/evaluation, framework and plan allocations; it is not a32-record or per-policy memory claim. No per-method speed comparison or energy measurement was conducted.

## 8. Bounded closeout
Retain segmented context + three-level HSA as an executable maintenance component with explicit information/state/cost boundaries. Preserve exact original checkpoints and this fixed mixed-preparation candidate; do not adopt a new NSS serving model from a synthetic result.

This pass gives a positive answer to the narrow outstanding preparation question: a small multi-size training phase can improve use of expanded evidence while preserving the tested small task. It is enough to stop polishing this subproblem. Keep512-layout errors, dense-baseline adequacy, total-memory/long-term lifecycle costs, and language-token interfaces as recorded limits for later integration—not automatic invitations to launch another study.

Next research work can move to the next component, with DARP's maintenance-output concept the previously discussed candidate. No DARP implementation or other follow-on execution is authorized or performed here. None of these results qualifies natural-language context,25,000-token operation,general memory/identity,autonomous night repair,or a full NSS architecture.

## Evidence map
- `PROTOCOL.md`, `SOURCE_FIXTURE_LOCK.json`: prospective scope and frozen identities.
- `source/`: standalone runner and unchanged reused HSA/streaming modules.
- `parents/`, `checkpoints/`: exact parents and all60 continuation states, optimizers and RNG/cursors.
- `fixtures/`: common raw training/confirmation worlds and target selections.
- `results/`: per-update logs, all endpoint logits, summaries, continuation/streaming receipts and audits.
- `failures/`: pre-lock parse incident and every selected behavioral error.
- `audit/`: separately labeled post-result recount/replay/publishing code.

No SH01,SH02,SC01,SC02,CAP01,or earlier NSS outcome was rewritten.
