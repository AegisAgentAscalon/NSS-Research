# NBR02-EVAL01 — real-candidate evaluation and bounded review
## Completed retrospective pass: execution v0.2 / scientific contract v0.1

**Result:** the evaluator/report and fixed-budget review comparison executed on real retained neural outputs. Targeted checking substantially reduced out-of-envelope approvals in the pooled historical cohort, but deferred more genuinely acceptable candidates. Benefits were not consistent across both learners and source studies. This is a measured trade-off, not a universally better reviewer, improved learning rule, deployment acceptance, or NSS transfer result.

The pass remains **NBR-02**. It tests a possible component here for later adaptation elsewhere. No historical model was instantiated, forwarded, differentiated, trained, edited, or adopted. No micro/macro rehearsal, Tertiary, self-play or NBR-01 reopening occurred. Source learning trajectories were held fixed.

## 1. What is new relative to C00
C00 applied rules to deliberately authored behavior tables. Here measurements come from actual captured logits in REV01 v0.4 and TIMING01 v0.1. The new evaluator exposes only a declared candidate panel to an ordinary reviewer; an independent assessor subsequently checks the full finite capability panel. The reviewer is not a neural judge and the evaluator is an offline measurement-retrieval implementation, not a live model-probing service.

The two source archives were byte/hash/CRC verified. Direct manifest payloads were checked and the complete primary numerical stream in each was losslessly reconstructed in memory and matched to its original byte hash. Each raw array or alias was checked. Every source query row was compared against its raw logits, and class/loss values were recomputed. This does not repeat the source training, differentiate any model, or newly reproduce either source's adaptive replay. Some unrelated logical aliases in the original complete archives were not restored.

## 2. Cases and observation boundary
All G/L main development and exposed historical-held-out sessions at delay zero are included. The common after-receipt-2 version is the fixed parent AND stable reference. At each actual post-receipt-3–6 or post-maintenance boundary, the saved version is considered as an independent adoption offer. The parent's focal logits are evaluated against the CURRENT released correction, not its superseded label. All old targets are checked against the recorded public receipt tables.

| Source | Model/base contexts | Actual candidate occasions | Distinct candidate versions after in-context deduplication |
|---|---:|---:|---:|
| REV01 | 96 | 768 | 768 |
| TIMING01 | 96 | 1,728 | 1,440 |
| Total | 192 | 2,496 | 2,208 |

The 288 TIMING aliases genuinely share parameters and current targets; their branch/stage references remain retained. No outcome-based examples were removed. Within the historical-held-out subset there are **1,472 candidate snapshots across 128 model/base contexts**: two studies, each with eight bases, four fitted models per learning method, and two methods. Snapshots, checkpoints, methods, replay, and policy/profile repetitions are not independent new tasks. Development is tabulated separately. All material is previously exposed retrospective evidence, not fresh confirmation.

This is not a cumulative simulated learner. Rejecting an earlier update in a real system would alter later learning; we do not splice the archived branches into a fictitious trajectory. Independent rejection outcomes use the saved fixed parent. The separate offer-availability table describes when a recorded acceptable offer existed; it is not a measured live adoption latency.

## 3. Evidence allocation, with a strong ordinary reference
Every policy receives the same eight old reference records, current correction receipt, and parent/candidate version information. The parent panel is charged as nine reference records per standalone opportunity, even though it can be shared in this analysis.

* **FIXED_LOW:** one fixed old record from each scope/label group; four old checks plus the focal check.
* **TARGETED:** in each scope, select the initially less-confident record opposite the newly corrected label, and keep a fixed record of the other label. It still makes four old checks plus the focal check. Selection sees only the parent reference and lawful target, never unqueried candidate logits.
* **FIXED_HIGH:** use the other coordinate in each group, with identical cost. This exposes dependence on which fixed representative was chosen.
* **FULL_PANEL:** inspect all eight old outputs and the focal output. Its nine candidate checks are a stronger, more expensive finite-panel reference.
* **ACCEPT_ALL / NEVER_ADOPT:** descriptive boundary controls, not equally costly solutions.

TARGETED is a transparent heuristic motivated by the PREVIOUSLY OBSERVED label-group interference. It is not learned, selected on new review outcomes, or proven transferable. The fixed controls already cover both labels and scopes; they are not deliberately weak unstratified samples.

Candidate measurements are served from retained logits. Five versus nine means stored-output requests in this pass, not five versus nine newly executed neural forwards or a deployment-time speedup. All policies' full reference requirements, selector work, source extraction, memory and independent audits still cost work.

## 4. What “acceptable” means here
User direction permits manageable regression and some missed useful adaptation, rather than perfect preservation. This pass fixes three illustrative contracts before review: CAUTIOUS, **MODERATE (primary)**, PERMISSIVE. They are study-local sensitivity settings, not established operational safety standards or revisions of earlier study gates.

The moderate contract requires focal probability at least .60 and a gain of at least .10 over the parent under the current target. It permits a mean old target-probability decline of .03, a worst individual decline of .25, old target probability down to .40, and at most one newly wrong old class out of eight. It also requires positive equal-weight nine-capability mean target-probability gain. That last quantity is a declared toy statistic, NOT calibrated practical value, general competence, or a sum of different units. Class counts and log loss remain separate.

The partial rule applies the same rate/mean requirements to its four checked old records. Its sampled class-rate discretization can be more conservative than the full eight-record limit. More importantly, a risk-targeted sample is not an unbiased estimate of the entire old panel. That distinction is central to the observed false deferrals.

Full-panel acceptability is the reference for this comparison. It includes the four unqueried old outputs, but is neither an independently drawn capability population nor a test of unbuffered skills. FULL_PANEL matches it by construction; its zero decision errors do not demonstrate an omniscient evaluator.

## 5. Main results under the moderate contract
The following pooling is descriptive only; it mixes two different candidate-generation studies and differently sized snapshot trajectories. Per-source/method and per-base tables are mandatory companions.

Of the 1,472 exposed historical-held-out candidates, **1,158 satisfy the complete finite-panel contract**.

| Review policy | Acceptable candidates retained /1,158 | Acceptable candidates deferred | Out-of-envelope candidates approved | Candidate records checked |
|---|---:|---:|---:|---:|
| FIXED_LOW | 1,112 (96.03%) | 46 | 14 | 5 |
| TARGETED | 1,074 (92.75%) | 84 | 2 | 5 |
| FIXED_HIGH | 1,123 (96.98%) | 35 | 33 | 5 |
| FULL_PANEL | 1,158 | 0 | 0 | 9 |
| ACCEPT_ALL | 1,158 | 0 | 314 | 0 |
| NEVER_ADOPT | 0 | 1,158 | 0 | 0 |

Against FIXED_LOW, TARGETED removes 12 out-of-envelope approvals but misses 38 additional acceptable offers: a 0.815 percentage-point reduction in problematic approvals and a 2.582-point increase in acceptable deferrals among all proposals. It retains 96.96% of FIXED_LOW's captured acceptable equal-weight probability gain, or 93.71% of all available acceptable gain under this chosen statistic. These are not guarantees of long-run utility.

**None of the candidates chosen by any of the three partial policies has an old class error in this moderate cohort.** Their remaining out-of-envelope approvals violate the confidence-degradation limits, not demonstrated old-class forgetting. ACCEPT_ALL exposes 23 repeated old-class error observations; those are not 23 independent lost skills.

These figures are compatible with accepting imperfect review as useful infrastructure. They do not establish that TARGETED's additional missed learning is worth its protection in every context.

## 6. The pooled trade-off hides important heterogeneity

| Source / method | FIXED_LOW: outside-envelope approvals / acceptable deferrals | TARGETED: outside-envelope approvals / acceptable deferrals |
|---|---:|---:|
| REV01 / G | 7 / 3 | 0 / 9 |
| REV01 / L | 6 / 8 | 0 / 35 |
| TIMING01 / G | 0 / 12 | 0 / 11 |
| TIMING01 / L | 1 / 23 | 2 / 29 |

For REV01-L, targeted review removes six problematic approvals but defers 27 additional acceptable offers and retains only 78.71% of the primary fixed rule's acceptable probability gain. For TIMING01-L, it is worse on BOTH decision counts. For REV01-G the predeclared exploratory usefulness discriminator is met. For the other three primary source/method contrasts it is not. No method or source was switched after results.

The offset fixed policy changes the reference result substantially. TARGETED compares favorably against FIXED_HIGH in some cohorts where it does not improve on FIXED_LOW. Therefore a fortunate choice of panel representative can masquerade as an algorithmic advantage. All three policies remain in the record; we do not select the easier comparator.

## 7. Where the decisions go wrong
Under the moderate contract, **all 84 TARGETED false deferrals are triggered by OLD_MEAN_DROP**. The full old panel remains within the agreed limits, but the deliberately vulnerable subset looks worse. The same reason accounts for all 46 FIXED_LOW false deferrals.

Both remaining TARGETED false approvals occur in TIMING01-L and arise when the limited-panel mean understates the full-panel decline. The current heuristic is therefore conservative on many candidates, yet still not an exhaustive detector.

The key implementation lesson is not “never target vulnerable records.” It is: **a risk-sentinel panel and a representative estimate of average impact are different measurement jobs.** Applying a population-average limit directly to a severity-selected subset can unnecessarily block useful adaptations. An eventual evaluator may need representative coverage, risk-specific reporting, or a bounded additional check for ambiguous cases. None of those additional policies was run here.

## 8. Sensitivity, not threshold selection

| Contract | Complete-panel acceptable candidates | FIXED_LOW bad approvals / missed acceptable | TARGETED bad approvals / missed acceptable |
|---|---:|---:|---:|
| CAUTIOUS | 796 | 111 / 65 | 8 / 139 |
| MODERATE | 1,158 | 14 / 46 | 2 / 84 |
| PERMISSIVE | 1,279 | 12 / 31 | 1 / 56 |

The general protection-versus-opportunity trade-off appears at all three selected settings. All settings are reported, and none is selected as a production standard. Moderate and permissive results cannot retroactively reclassify TIMING01, REV01 or any earlier failed screen.

## 9. Engineering evidence and failures
The scientific policy, tolerances, source cohorts and comparison choices were fixed before producing the new review outcomes. The underlying archives and prior analyses were already exposed, so this is not prospective confirmation.

Fourteen finite engineering fixtures cover strict Boolean flags, version/receipt checks, missing/nonfinite evidence, panel coverage, duplicate/out-of-budget lookups, a corrected-label target, no-learning behavior and a hidden unqueried-value alteration. The latter produces identical operational evidence/decisions when an unrequested capability changes: an intentional coverage limit, not proof that hidden harm can be detected.

Two extractor issues were caught before ANY real candidate review:
1. A single global state slot was wrongly used across interleaved B1/B2 archived branches. The identity assertion stopped it. The corrected extractor tracks session/branch-specific versions and receipt tables.
2. REV01 and TIMING01 use different manifest structures. An adapter expecting a list failed on TIMING01's dictionary schema; normalization was made explicit.

The earlier inspection-only delivery-map mismatch is also recorded. Stopped code, source locks and error logs are preserved. No source model, raw output, current target, threshold, candidate-selection rule or old experiment was changed. These were evidence-adapter failures, not learning failures.

A supplemental independently written provenance audit checked all 25,920 selected measurements against captured raw-logit hashes, verified that referenced label releases preceded their queries, and checked every candidate/parent field and alias. This checks stored evidence relative to the source hashes; it is not live credential authentication.

The source records contain 47,710 scored queries; all were compared with the raw recorded logits. All their negative rows remain in the archived source tables in this package. Whole prior optimizer trajectories/graphs are not duplicated; the original learning archives remain their provenance.

## 10. Review replay, independent adjudication and work
One primary run and one fresh-process review replay each evaluated 39,744 policy/profile decisions and made 52,992 retained candidate-measurement requests. Empty per-decision caches and journals were rebuilt; the six policies share only the declared prior evidence and input pool. Three contract profiles reuse the same observed panel, not extra model predictions.

The independent scorer imports no production policy, runner or extractor. It rebuilds selection, full-panel judgments, probability/loss metrics, decisions and source-evidence links. Maximum numeric discrepancy was 2.220446049250313e-16. Review intent/completion pairs and hash-chain terminal identities match. All 7,837 error/missed-opportunity rows across profiles, policies, phases and extreme controls remain retained; this is not the error rate of TARGETED alone.

Primary versus fresh review replay matches **12 deterministic files, 31,437,498 bytes per side**: three compressed journals/evidence/decisions, counts, seven scored tables and the independent audit. Runtime/RSS are excluded from byte equality. Replay here means repeating evaluation/review of stored measurements; it is NOT another model forward pass, training run, or adaptive replay.

Core review evaluations total 79,488; the three finite-fixture executions add 18 review calls (plus 27 panel-selector calls). Actual neural calls, gradients and optimizer updates are zero. Measured lookup counts are stored-output access, not deployed neural costs. The full old-parent reference costs nine records per standalone decision and is reported separately; a partial candidate panel is not the entire evaluation budget.

The runtime-monitor helper was added after the core policy source lock; its identity and this timing are disclosed in LOCK_RECHECK.json. It did not change numerical policy. Supplemental input auditing and descriptive aggregation are explicitly post-result audits. The frozen eight source/protocol entries were rechecked unchanged after execution. Source decoding and the earliest setup interval were not continuously resource-sampled; supervised review/scoring stages have 0.2s samples. No unrestricted native-memory superiority claim is made.

Final archive extraction, manifest verification and relocated rescoring are documented in the external delivery receipt, not assumed by this report.

## 11. Architecture interpretation and next boundary
NBR-02 now has an evaluator/report interface consuming actual learned behavior and a measured, limited-evidence decision comparison. That is a component result. It does not fix the raw learner, restore plasticity, prove continual improvement, or qualify transfer to the NBR-01 state layer or an integrated core.

Retain ordinary evaluation/review as a small baseline. TARGETED is not promoted to a universal default: its extra deferrals and one dominated cohort need attention. The next design choice should distinguish representative average-impact measurements from risk probes, or explicitly price uncertain deferral/additional review, before adding neural review complexity. An eventual maintenance study should hold the chosen evaluator/review policy fixed so that better decisions and better learning are not conflated.

Do not equate “candidate passed a finite panel” with permission to publish its weights. C00's real serving publication, authenticated measurement acquisition and operational-tolerance tickets remain open. No candidate was actually adopted here. No long-lived recurrent state was migrated across weights.

NBR-01 remains bounded-closed; NBR-02 remains active. The parked workspace problem, deferred dream/self-play, known native-memory accounting gap, all G01–G22 questions, and the post-NBR03/pre-NBR04 foundation return remain. Other experimental candidates are not automatically dispatched by completion of this pass.
