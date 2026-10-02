# NSS TS02-MW01 — maintained management workspace and learned derived progress
## Completed execution v0.2 / reviewed scientific protocol v0.1

**Disposition: execution and independent numerical checks completed; the predeclared scientific screen FAILED.** The native workspace model achieved a modest pooled improvement, but did not meet the feasibility/safety conditions or the required benefit over both recurrent-only controls. No thresholds, cases, fit counts, or checkpoints were changed in response.

**ELI5:** the learned worker uses the little instruction card, and it helps some answers. But the worker still mishandles combinations of changed instructions and sometimes says work is complete or based on the right revision when it is not. A used organizer is not yet a reliable organizer.

The 15 new main models and three cost-only probe models are separate from the historical models. All retained Q010/CM-02/TS01/architecture input archives remain byte-identical. No old model was loaded or updated.

## 1. What changed from TS01

Two tasks each have four milestone states. A completion is supported by the revision under which it was performed: milestones 0/1 depend on the left source; 2/3 on the right. A new revision can invalidate previous progress. Missing or conflicting evidence yields the declared UNKNOWN states; restoring the same supported revision can make retained work usable again. Goal order determines which unfinished milestone is next. Public authority, owner/scope checks, reference status, routing to protected task banks, and no-op filtering are supplied by deterministic code.

The learned transition must maintain and revise progress, not retrieve a stored answer. Each head independently predicts four three-way milestone categories (not done/done/unknown), a six-way next action (0–3/DONE/UNKNOWN), and two five-way revision claims (0–3/unresolved). Primary joint correctness covers the milestones and next action; revision claims are separately scored safety outputs. No head is repaired from another head or from gold.

RW maintains five categorical tokens per task: goal, left revision/status, right revision/status. Ten uint8 IDs are resident; a shared 18×4 learned embedding provides 20 float32 values to the addressed recurrent update. This is a native categorical-token input, not English text, the older byte-control string, a separate language-model prompt, or soft latent slots. Heads read recurrent state only. The maintained fields contain no milestone-completion stamps, gold next action, or hidden repair mask.

The writer copies lawful observed metadata. It does not learn to write. The workspace persists across switches/resets, is consulted at actual recurrent transitions, and is rewritten on accepted metadata events. Queries are read-only; residency is not continual processing. An explicit task RESET is learned through the transition, not implemented by clearing the carried state. Protected per-task routing and authority checking remain software assistance.

| New configuration | Recurrent input / hidden size | Trainable parameters | Float32 weight payload | Two state banks | Extra workspace payload |
|---|---|---:|---:|---:|---:|
| R: recurrent-only | 42 / 48 | 14,620 | 58,480 bytes | 384 bytes | none |
| R+: larger recurrent-only | 42 / 60 | 20,428 | 81,712 bytes | 480 bytes | none |
| RW: recurrent plus workspace | 62 / 48 | 17,572 | 70,288 bytes | 384 bytes | 10 uint8 IDs |

R+ has more ordinary capacity than RW; it is a generous control, not exact parameter/FLOP matching. All configurations receive the same public events and receipts. RW additionally receives a maintained representation of already observable metadata. Representation-specific token superiority cannot be isolated without a learned same-information structured encoding arm; S and X below are exact software controls, not that learned comparison.

## 2. Frozen training and evaluation

Fifteen main fits completed 1,000 Adam updates each, batch size 8, with five paired stream sets shared across R/R+/RW. There are 40,000 separately allocated main training streams, presented 120,000 times across configurations. The three fixed 100-update probes used 800 separate shared streams (2,400 presentations). Total training/probe event presentations: 4,425,600; total optimizer and backward updates: 15,300. Main streams had 17/33 events plus an 11-message prelude; probe streams used 33+11. Full BPTT and both heads at every public message were charged.

All initial tensors followed the pinned uniform initialization and dedicated seeds; Adam used the fixed settings. Probe state was discarded and not reused by main models. Probe cost, not accuracy, determined feasibility. Only terminal update 1000 was evaluated; all 15 terminals were hash-locked before concrete main evaluation generation. No sweep, extra fit, checkpoint selection, data culling, post-held-out repair, or optimization retry occurred.

Main evaluation uses 32 chronological sequences: three development and five held-out families, four templates each (H handoff/goal, E evidence revision, F conflict/withdrawal, K reset/revocation). Each has 65 events after the 11-message prelude. Query checkpoints are 0,8,16,32,48,64. There are 192 unique query occasions, 120 held out across 20 sequences. Five model fits repeat these same observations; model repetitions/checkpoints do not create independent task families. The tasks remain closely related, finite, programmed recipes.

A separate untrained three-model fixture checked 24 occasions before probes or fitting. Its poor accuracy is retained and is not an admission failure.

## 3. Primary held-out results

| Primary CARRY configuration | Correct milestone+next readouts | Accuracy |
|---|---:|---:|
| R | 507/600 | 84.50% |
| R+ | 496/600 | 82.67% |
| RW | 526/600 | 87.67% |

RW is +19/600 = **3.17 percentage points** over R and +30/600 = **5.00 points** over R+. These are descriptive pooled differences over 120 occasions × five fits, not calibrated general performance or a statistical significance claim.

### All fits, including weaker workspace fits

| Fit | R | R+ | RW |
|---|---:|---:|---:|
| 1 | 107/120 | 103/120 | 96/120 |
| 2 | 93/120 | 94/120 | 113/120 |
| 3 | 102/120 | 92/120 | 112/120 |
| 4 | 104/120 | 104/120 | 108/120 |
| 5 | 101/120 | 103/120 | 97/120 |

Only RW fits 2,3,4 reached the predeclared 108/120 (90%) floor: **3/5, not the required 4/5**. RW did not beat both controls in every paired fit. The same data pairing does not mean identical weight initialization or learning trajectories across different models. Fixed equal update budgets also do not establish equally converged models.

### All held-out family summaries

Each cell is 24 occasions × five fits = 120 readouts. Count differences below avoid floating rounding at exactly 5 points (6/120).

| Family | R | R+ | RW | RW−R | RW−R+ |
|---|---:|---:|---:|---:|---:|
| MW01EVAL-01 | 99/120 | 98/120 | 103/120 | 4/120 | 5/120 |
| MW01EVAL-02 | 99/120 | 100/120 | 106/120 | 7/120 | 6/120 |
| MW01EVAL-03 | 108/120 | 103/120 | 109/120 | 1/120 | 6/120 |
| MW01EVAL-04 | 96/120 | 93/120 | 100/120 | 4/120 | 7/120 |
| MW01EVAL-05 | 105/120 | 102/120 | 108/120 | 3/120 | 6/120 |

RW−R reaches at least five points in **1/5 families**; RW−R+ does so in **4/5**. Both comparisons must meet the rule; one does not. Both pooled directions are positive in every family, but that weaker fact does not replace the frozen requirement.

### Known-evidence repair subset

On E:16, E:32, E:48, F:48, F:64 (25 unique held-out occasions × five fits):

| Configuration | Joint repair successes |
|---|---:|
| R | 76/125 = 60.8% |
| R+ | 79/125 = 63.2% |
| RW | 79/125 = 63.2% |

RW does not improve over R+ on this central repair subset. Its milestone-only correctness on those occasions is 95/125 versus R's 100/125 and R+'s 97/125; next-action correctness is 96/125 versus 87/125 and 88/125. The aggregate joint score conceals differing errors across the independent heads.

All CARRY models correctly handled the 50 held-out readouts whose next action was genuinely UNKNOWN. The differences are not solely a gain in abstention. On known-next-answer occasions RW scored 476/550, R 457/550, R+ 446/550. R/RW had no known-next abstentions in this pool; R+ had three.

## 4. Safety failures remain raw model failures

RW made **75 stale or unsupported USE/revision claims out of 1,200 held-out group predictions**. It made **17 wrong-DONE assertions across the 100 designated assessments** (E:16/E:32/K:16/K:32). Both required zero. A wrong-DONE assertion counts either the next head saying DONE or all four predicted milestones saying DONE when gold is not complete. These are raw output diagnostics, not unauthorized operations actually executed by a deployed system.

R made 10 designated wrong-DONE assertions; R+ made 20. Thus RW's better pooled accuracy does not imply every safety metric improved over R. Across all held-out query positions, wrong-DONE totals were R=32, R+=50, RW=25. No validator repaired or suppressed these outputs.

At E:32, after the second evidence group advances, **all three configurations score 0/25 joint successes**. RW makes 11 of its designated wrong-DONE assertions there; another six occur at K:16. At E:48 and E:64, every configuration recovers correct primary task output (25/25 each), yet the revision-claim failure persists. Correct visible progress therefore does not certify correct provenance.

## 5. Post-result diagnosis: unseen composition, not missing public evidence

A separately labelled audit of retained training/evaluation arrays found a concrete pattern. Training includes the left source advancing to revision 1 and the right source advancing to revision 1 in different templates. **No main-training or probe prefix has both source revisions equal to 1 and valid together.** The held-out E sequences do reach that composition.

All 75 RW invalid revision claims occur at the 15 unique held-out E:32/E:48/E:64 occasions, repeated across five fits. The recorded maintained packets correctly say both records are at revision 1. The model nevertheless claims left=1, right=0. Its native token inputs contain the correct public metadata; this is not a no-cue identity problem or a stale software packet.

This is a **post-result association and training-coverage limitation**, not a controlled causal demonstration of the failure's cause. The fixed test legitimately asked for that composition; it remains failed. The same deficiency affects the recurrent-only controls. We did not add the combination to training, adjust criteria, remove its rows, or continue fitting. A future data-coverage intervention would require a new protocol and fresh held-out evaluation.

The evidence is in `post_analysis/DESCRIPTIVE_ANALYSIS.json` and the reproducible no-model script `post_analysis/analyze_retained.py`. Those supplements are not part of the pre-generation scientific source lock, and are not presented as preregistered discoveries.

## 6. Did the model use the workspace and state?

| RW held-out arm | Joint correct | Interpretation |
|---|---:|---|
| CARRY | 526/600 (87.67%) | Both working state and maintained slots available |
| SLOT_MASK_EVERY_EVENT | 366/600 (61.00%) | Same checkpoint, embeddings replaced by zero at every update |
| ZERO_EVERY_EVENT | 38/600 (6.33%) | Both learned banks cleared before each public event; workspace remains |
| PREFIX_REPLAY | 526/600 (87.67%) | Same model reconstructs from each public prefix |

The 26.67-point slot-mask drop supports dependence on this channel. It is an out-of-training-distribution information ablation, not proof of superiority over an equally resourced model. The state-removal result shows the metadata is not a complete answer store. R and R+ each scored 0/600 under this stronger state-removal task. Carried and prefix-reconstructed state/logits are bit-identical.

Exact structured S and packed streaming X each scored **120/120 unique held-out occasions**, including revision claims. Their progress stamps are exactly programmable. X uses eight three-bit stamp fields (24 sufficient progress bits) plus public metadata and indexing; this is not a three-byte whole system. Exact software remains the stronger task solver.

Scorer-only alternate-intent labels on E:16 reuse identical public inputs and outputs, with no extra forwards. For the five held-out unique occasions the two intended answer labels differ. CARRY primary/alternate counts are R 15/25 and 0/25; R+ 15/25 and 0/25; RW 17/25 and 0/25. This is report-only nonidentifiability, not a detectable safety gate. Repeated fits do not create new counterfactual observations.

## 7. Work and memory: no efficiency PASS

RW's 10-byte token ID payload does not include its recurrent state, weights, int64 execution-index tensor, 80-byte embedding output, owner/scope mappings, authority/version/conflict indexes, journal, or operator buffers. R+ has more state and weights; RW needs extra embedding work and a deterministic metadata writer. This does not produce a blanket total-memory or speed conclusion.

For the 20 held-out sequences, the RW control writer made 170 whole-five-byte assignment requests (850 payload bytes assigned), containing 231 actual uint8 value changes at 146 events. Counting only changed fields would undercount assignment requests. This is source-level logical accounting, not measured hardware memory-bus traffic. It performed 425 counted indexed lookups returning 23,038 canonical logical bytes. The canonical event archives occupy 291,379 bytes across those sequential episodes, not simultaneously resident memory.

Each primary held-out RW model pass performs 330 actual CARRY transitions versus 1,525 under the specified PREFIX_REPLAY schedule. This is a retained-state/recomputation comparison; replay also scans prefixes. It is not a 4.62× wall-clock speedup or an advantage over S/X. All-event auxiliary heads, exact-control construction, source verification, and trace I/O are also charged.

`COSTS.csv` records component Python inventories and declared payloads. These are **not a complete per-arm native allocator trace** or an optimized end-to-end deployment benchmark. Separate component observations must not be summed blindly when they share objects. Overall execution RSS includes runtime/interpreter/training/auditing. `post_analysis/WRITER_COST_SUPPLEMENT.json` clarifies actual packet assignment versus semantic field changes without performing new inference.

## 8. Complete training/evaluation evidence and verification

The independent evaluator reconstructs public authority, status, goals, progress, and routing from current/past events using different code and representations. It imports no producer, controller, generator, or model implementation. Saved GRU/head calculations are reconstructed in NumPy float64 against the frozen empirical tolerance `2e-6 + 2e-5*abs(reference)`. This is an engineering tolerance, not a proven bound and not the historical Q010 underflow allowance.

Main arithmetic audit: **5,717,120 scalar comparisons**, maximum tolerance ratio **0.1704980291**. Fixture: **142,928**, maximum ratio **0.0147816753**. No query winner ties within the declared 1e-5 check were found. Engineering admission passed; poor learned scores are scientific negatives, not reasons to censor evaluation.

Fresh-process main replay recomputed and exactly matched **17,120 arrays / 10,019,920 elements**. Fixture replay matched **428 / 250,498**. All 15 score files for each split regenerated byte-identically. These are internal implementation checks and same-runtime reproduction, not third-party or cross-device validation. Replay is not new independent sample size and is not another training reproduction.

The evidence layout retains full public episodes, isolated labels, every distinct addressed-bank transition, all declared heads/endpoints, routing/writer records, controls, negatives, and traces. Prefix transitions were genuinely recomputed and then checked against carried arrays; hash receipts reference those equal bytes only afterward. Fresh replay similarly stores hash-verified aliases after recomputing outputs. Aliasing is lossless delivery sharing, not an inference cache or scientific memory compression. Independent scorer resolves and checks aliases.

There are **4,108 incorrect main joint rows**, and 963 invalid group claims across all 9,600 main learned rows, including controls. Their union comprises **4,717 negative rows**. Fixture has 238 incorrect joint rows, 239 invalid group claims, and 238 union-negative rows out of 240. All correct and incorrect query rows and full per-event auxiliary scores are retained. Repeated arms/fits/replay are not independent tasks. S/X have no task errors.

The new training history includes **75 full main model/Adam/RNG/cursor checkpoints** and six full probe start/end checkpoints, plus the three untrained fixture initializations. All 15,300 batch loss/finite-gradient/input/parameter-hash records and all 40,800 allocated public streams are retained. The independent audit reconstructs their 1,475,200 unique public prefixes and supervised targets, metadata, routes, and all consumed input/checkpoint identities. It **does not repeat optimization or the stochastic generator's draws**; it audits the retained public inputs against their frozen semantics.

All 40,800 wire episodes are unique. Ignoring identifiers and unused distractor payloads leaves 40,798 normalized episodes: two excess duplicates retained. All 36 fixture/main evaluation streams are distinct and do not equal complete retained training episodes. Length differences make that exact complete-stream comparison limited; this is not proof of broad distribution independence.

## 9. Frozen limits and actual execution

| Work category | Reserved/completed | Hard cap |
|---|---:|---:|
| Cell-example reservations | 4,836,256 | 4,850,000 |
| Head-vector reservations | 9,212,000 | 9,250,000 |
| Backward attempts | 15,300 | 15,300 |
| Optimizer attempts | 15,300 | 15,300 |

Actual dispatched cell examples are 3,681,666: 3,568,752 in training/probes plus 112,914 across fixture/main capture and fresh replays. Reservations conservatively cover skipped/masked work. A completed reservation means the stage finished, not that every reserved no-op cell executed. Training has 2,948,109 admitted event examples, distinct from all batched cell examples. Head-vector reservations equal 9,212,000. No extra fit, hidden neural diagnostic, reset ledger, failed numerical attempt, or unacknowledged in-flight work occurred.

Execution through the final independent training audit completed at **1,315.48 seconds** on the shared clock. Peak sampled process-tree RSS was **620,367,872 bytes**, peak container memory **1,606,270,976 bytes**, below the respective 3 GiB/3.5 GiB limits. Sampling was every 0.1 seconds; brief peaks and the initial uninstrumented shell inspection are not claimed covered. Host: CPU-only Python 3.13.5, NumPy 2.3.5, Torch 2.10.0+cpu, four CPU-equivalents of quota, 4 GiB container. Host execution clock began at 2026-09-25 00:34:20 UTC; the supplied proposal is the preceding September 24 research record. Times are not deployment forecasts.

At numerical completion the retained logical evidence layout occupied **240,837,678 bytes**, below 256 MiB. Final documentation/manifest/QA sizes and ZIP identity are in the external delivery receipt. The complete delivery must remain below 64 MiB compressed. No original model/study archive is duplicated. An initial per-file DEFLATE ZIP exceeded the 64 MiB delivery cap and was rejected. Its receipt is preserved; the final delivery uses a lossless whole-payload compression container and a verified restoration helper, without changing or removing scientific evidence. Packaging/rescoring is separately counted on the same authorization clock and uses no neural calls.

### Seed-audit metadata limitation

All 216 direct numeric seeds and all 40,800 episode seeds were reproduced from the proposal's explicit label/digest rule and checked for uniqueness. The parent also carries an aggregate `derived_sorted_value_digest` without specifying its serialization. That opaque aggregate was not matched and is **not claimed verified**. No seed was changed. The executed list and its explicitly specified sorted-uint64-big-endian digest are retained in `audit/SEED_EXPANSION.json`; `audit/SEED_DIGEST_ENCODING_NOTE.md` states the boundary. This is distinct from the verified explicit seed derivations and from missing historical RNG draws.

## 10. Architecture disposition and Codex handoff

This study supplies a bounded **ST-04 → IF-02 → ST-02** realization: maintained explicit metadata is embedded and conditions the native recurrent update, and a same-checkpoint mask demonstrates channel dependence. It does not qualify the chosen realization as sufficiently accurate/safe or show the required benefit over larger recurrent capacity. The parent Architecture Ledger v0.1 is unchanged; the accompanying evidence update records this distinction rather than promoting experimental dimensions into global canon.

Maintain the user's architectural intent: a resident organizer supports richer ongoing state and exact evidence; residency, reading, and rewriting remain separate. Do not replace this with a token-free objective or treat source-copying fields as autonomous learned writing.

A useful next proposal would isolate **compositional evidence repair** and distinguish exact source metadata from learned consequences. The newly identified dual-revision gap suggests a bounded coverage/control question, not permission to add more updates until these known test cases pass. Any new training needs its own source/split/seed/budget and genuinely fresh held-out assessment. A future exact binding readout could be legitimate engineering, but would not retrospectively repair these raw model claims or demonstrate learned revision fidelity. Keep exact streaming, greater-capacity recurrence, and native state/slot ablations strong.

No learned writer, shared-state routing, consultation-cadence, precision, soft-slot, provisional-work, architecture scale-up, core replacement, or Forge/Runtime integration was launched. Frozen Primary, alternating Secondary/Tertiary, advisory fallible Validator, overlay removal, Segmented Context/HSA/MSA, DARP, learning and generation policy remain architectural context, not tested participants.

## 11. Historical limits and package use

Old Q010 optimizer/RNG/raw training gaps, compact-archive omissions, historical verifier failures and the reconstructed underflow amendment remain unchanged. The +2^-126 historical final-softmax amendment was neither modified nor applied to this GRU test. CM-02's 5,995-attempt and TS01's training ledgers remain closed.

After extracting this complete package, run `python RESTORE_EVIDENCE.py` and then `python VERIFY_STUDY.py`. Restoration extracts the lossless delivery container and verifies every retained file. The scientific replay aliases are then understood directly by the scorer. `python RESCORE.py --output /new/external/path` independently re-scores retained fixture/main evidence without training or neural forwards. `REPLAY_EVALUATION.py` offers a separate future fresh reproduction in a new directory, never overwriting this ledger; only its CLI/syntax was checked during delivery, not an unreported third replay. The old archives are historical provenance, not numerical dependencies for rescoring this study.

**Bottom line:** native maintained metadata affects learned recurrent processing and produces a modest pooled gain, but the declared repair/safety/advantage screen fails. The record is useful evidence for the architecture—not permission to claim the organizer is already reliable.
