# NBR-01 / Pilot001 — State, Depth and Learned Write Admission

**20 September2026 · Research packagev0.1 · PILOT + POST-PILOT DIAGNOSTICS RUN**  
**Full NBR-01 remains open. No production architecture acceptance.**

## Decision brief

Keep exact memory as a strong control and as the owner of exact facts. Retain a **soft-trained, selectively closed state-update gate** as a candidate for the next registered study. Do not promote the poorly trained hard-gate-from-scratch arm, and do not treat short-horizon training success as proof of durable memory.

The important measured result is not that recurrence is generally better or worse than attention. Several trained models solved the short recall task, yet failed at longer delays. In the simple gated candidate, the gate had already learned to distinguish WRITE from DISTRACTOR tokens, but small residual updates on distractors erased the remembered value. Closing only those low gates, with **the same learned weights**, restored recall on the diagnostic cases. Opening high gates fully without closing low gates did not.

This is useful engineering evidence for NSS, not a novelty claim about gating, a full companion capability, or evidence about any laboratory's unpublished research.

## 1. Source, authority and chronology

The reference foundation is `MegaMindAlpha_v0.5.0_TriCoreFoundation001.zip`, SHA256 `f9aff6ff4509a1d797ca378122b3bda1e97d20bd50cf136a283739c51f7504e8`. It remains unchanged. A scratch extraction passed all974 manifest-covered file hashes,68 foundation tests and the static dependency check after the study.

The study is standalone. It imports no NSS serving code, opens no NSS database, and changes no accepted generation. It implements a bounded diagnostic trainer rather than another permanent Forge engine. Generic Forge and independent Runtime are still unconnected. The working v0.5.0 adapters remain test adapters; these trained checkpoints have not been wired into the tri-core lifecycle.

The task and state/depth factors follow the cognition/low-bit handoff, especially its G02–G04 requirements and NBR-01 description on pages6 and20–21. This first pilot narrows the task to temporal competence and readout-depth stability; the broader multi-step reasoning task is still required.

Chronology matters. The initial registration is retained in `spec/protocol_registered_v1.json`. Three development fits used seed101 and300 optimizer steps each. Their source snapshots, pre-run hashes, outputs and negative results are retained. After observing long-delay failures, the amended `spec/protocol.json` added soft/hard-gating variants and an explicit-memory Transformer control **before** the five-seed main pilot. After the main pilot, separate gate diagnostics were registered and run. Those reused pilot information and are labelled post-pilot, not retroactively preregistered confirmation.

Two host-command timeouts interrupted starts of additional runs. Their partial artifacts are retained outside the completed-pilot directory and excluded from result totals. Each was retried from its original seed; **no optimizer-resume claim** is made. The package contains all20 completed main runs, not just the favorable ones.

## 2. Task and fairness

There are eight possible symbols. A WRITE event replaces the remembered symbol. DISTRACTOR events must not do so. At QUERY, return the latest written symbol or UNKNOWN when this scope contains no write. A single early cue tests retention; a second, different cue tests overwrite; no-cue episodes test false recall. No target label enters a model input.

Training draws delays uniformly from0 through16, with occasional intervening updates and explicit no-cue examples. Evaluation uses delays0/4/16/64/128, with256 generated instances per condition and training seed. In the early-cue condition, delay really is the number of distractors after that cue. In the overwrite condition, the newer cue occurs near the midpoint, so the delay variable denotes overall episode span, **not** time since the last valid write. All raw condition-specific results are preserved.

Four small neural architectures were trained from random initialization at seeds201–205: a GRU, a soft scalar-gated state, a hard-gated state using a straight-through surrogate, and a two-layer Transformer. Each completed600 AdamW steps with batch64. Within a seed, the neural arms received exactly the same batch observations, targets and selected readout depths; hashes independently confirm that match. The20 completed pilot fits comprise12,000 optimizer steps and768,000 example presentations. Development and reproduction costs are separate, not concealed inside those totals.

The Transformer retains the whole bounded observation tape; no relevant events are truncated in the main comparison. A second evaluation of the **same Transformer weights** uses a hand-engineered exact-memory tool that retains the latest valid source token. That tool reads observations, not labels, and is explicitly a strong engineered control—not a learned neural achievement. The same memory service could be made available to other candidates. An independently implemented exact state estimator also matches the environment on all19,200 generated evaluation instances.

Data and teaching counts are matched. Parameter count, representation, encoder operations, runtime and memory are **not** matched. There is no best-tuned-per-resource search or quality–energy frontier here. These results do not support an equal-compute architecture ranking.

State-off erases the earlier tape or hidden state before query. It deliberately removes the information needed for recall and is not used as a competitive Transformer baseline. A model may respond UNKNOWN rather than guess; near-zero known-cue accuracy is therefore not equivalent to worse-than-random guessing. Detailed UNKNOWN counts are in the raw metrics.

## 3. Competence screen and long-horizon results

The predeclared pilot screen requires at least95% aggregate known recall and95% no-cue accuracy across trained depths1/2/4 and delays0/4/16. It is a task-competence screen, not production qualification.

| Trained arm |Seeds meeting the short-task screen |
|---|---:|
|GRU persistent state|5/5|
|Soft-gated persistent state|5/5|
|Hard gate trained from scratch|1/5|
|Transformer + full retained tape|5/5|


The hard-gate-from-scratch failures are important. Four seeds never became competent even on the short task, so their long-delay failure cannot diagnose the architecture's ultimate capacity. Seed203 did learn the correct gate and retained the cue, but selecting that seed alone would conceal the training failure rate.

The table below uses **early-cue recall at depth4**, the highest trained readout depth. Each entry is the mean and sample standard deviation across all five training seeds, with256 generated instances per seed. These are variability measures, not confidence intervals. Every other depth and condition remains in `evidence/SUMMARY.json`.

| Arm |16 distractors |64 distractors |128 distractors |
|---|---:|---:|---:|
|GRU persistent state|100.00 ± 0.00%|4.53 ± 10.13%|0.39 ± 0.87%|
|Soft-gated persistent state|100.00 ± 0.00%|0.00 ± 0.00%|0.00 ± 0.00%|
|Hard gate trained from scratch|23.83 ± 42.68%|24.30 ± 42.45%|23.12 ± 43.07%|
|Transformer + full retained tape|99.53 ± 0.85%|64.22 ± 26.23%|63.05 ± 35.13%|
|Same Transformer + exact-memory tool|100.00 ± 0.00%|100.00 ± 0.00%|100.00 ± 0.00%|
|Soft-trained weights + hard admission (post-pilot)|100.00 ± 0.00%|100.00 ± 0.00%|100.00 ± 0.00%|


The final row is a **post-pilot intervention**, not another independently trained or confirmatory arm. Its source weights are the five soft-gated checkpoints. The exact-memory tool and exact estimator both remain strong controls, so the result is not a win over all simpler memory solutions.

No-cue behavior is independently relevant: absence of an observed write must not become an invented remembered symbol.

| Arm |No-cue accuracy after128 distractors,depth4 |
|---|---:|
|GRU persistent state|100.00 ± 0.00%|
|Soft-gated persistent state|100.00 ± 0.00%|
|Hard gate trained from scratch|68.05 ± 29.27%|
|Transformer + full retained tape|76.02 ± 40.45%|
|Same Transformer + exact-memory tool|100.00 ± 0.00%|
|Soft-trained weights + hard admission (post-pilot)|100.00 ± 0.00%|


The current full-tape Transformer also has long-horizon missing-memory errors. Better position/training curricula or an exact memory interface may remedy them. They are findings about this particular trained control, not a universal Transformer limitation.

## 4. What the gate diagnostics establish

The soft candidate updates `h_next = (1-g)*h + g*v`, with both gateg and proposed valuev learned from the current event. Every soft-gated main run put all eight WRITE tokens above0.5 and all eight DISTRACTOR tokens below0.5. Nevertheless, a small positive gate still admits an update. Over many unrelated events, the original contribution is repeatedly attenuated and replaced.

The first diagnostic loaded the same weights into the already implemented hard forward-admission rule: use1 when the learned gate is at least0.5 and0 otherwise. No parameter changed, no threshold was fitted, and observations were replayed from empty state. All five checkpoints reached100% on every tested state-on condition/depth/delay cell, including overwrite and UNKNOWN handling. This changes the transition algorithm, even though numerical weights are identical; it is not a silently compatible serving update.

To separate closing irrelevant writes from strengthening relevant writes, `gate_isolation.py` ran fresh generated instances at delay128 and depth4. All weights stayed fixed; the threshold remained0.5:

| Isolation intervention |Known recall across five seeds |Meaning |
|---|---:|---|
|Original soft gates |0.00% |Reproduces the long-delay failure. |
|Close low gates only; retain original high gate values |100.00% |Suppressing irrelevant writes removes the failure on this task. |
|Open high gates fully; retain original low gate values |0.00% |A stronger original write alone does not remove the failure. |

These interventions support a residual-write explanation **for this discrete task and learner**. They do not establish that real language supplies such clean relevance signals, that hard thresholds are universally appropriate, or that this is an accepted new NSS core. Direct hard-gate training remained unreliable; learning softly and then changing admission is a candidate procedure requiring a fresh registered comparison.

## 5. Depth is separate—and still needs a harder task

Event encoding and readout refinement use separate clocks. The same learned residual MLP readout is applied1/2/4/8 times after encoding. Training used1/2/4;8 was held out. Readout does not advance event count or mutate the retained state. All evaluation parameters remain fixed.

| Arm |Depth1 |Depth2 |Depth4 |Depth8 (untrained) |
|---|---:|---:|---:|---:|
|GRU persistent state|0.00%|0.00%|0.39%|1.56%|
|Soft-gated persistent state|0.00%|0.00%|0.00%|0.00%|
|Hard gate trained from scratch|23.20%|23.12%|23.12%|21.72%|
|Transformer + full retained tape|64.06%|63.59%|63.05%|61.72%|
|Same Transformer + exact-memory tool|100.00%|100.00%|100.00%|100.00%|
|Soft-trained weights + hard admission (post-pilot)|100.00%|100.00%|100.00%|100.00%|


This table is early-cue recall after128 distractors. More readout rounds did not repair the soft-gated memory failure. The task is simple recall, however, not a challenging relational or planning problem. A saturated curve does **not** establish that recurrent reasoning is useless. Nor is this repeated MLP a full recurrent Transformer block. Broad G04 conclusions and a hard depth-generalization task remain open.

## 6. Resources and what the small numbers exclude

| Arm |Parameters |Weights,bytes |Optimizer tensors,bytes |Five-seed training loop seconds |
|---|---:|---:|---:|---:|
|GRU persistent state|11,497|45,988|92,036|12.98|
|Soft-gated persistent state|6,250|25,000|50,060|11.63|
|Hard gate trained from scratch|6,250|25,000|50,060|12.28|
|Transformer + full retained tape|22,249|88,996|178,132|26.65|


Times cover the20 completed training loops in this CPU environment; they exclude interpreter startup, development, metric evaluation, verification, reporting and one extra full training reproduction. They are not target-PC speed measurements. Gradients occupy another weight-sized tensor allocation when present; activation and temporary allocator peaks were not measured exactly.

Each recurrent candidate retains32 float32 values:128 raw bytes per stream. That excludes model weights, counters, metadata, validation work and temporary activations. Measured serialized32-event snapshots occupy roughly602–609 bytes. The Transformer tape uses actual int64 token storage:256 raw bytes at32 events and520 at65; a129-event tape would occupy1,032 raw bytes by the same measured format. Its32-event serialized snapshot is733 bytes. The engineered exact-memory control retains a single source token plus its bookkeeping and does not require a32-float representation.

A5ms RSS sampler recorded whole-process training peaks around328–335MB. Those include the interpreter/framework and can miss sub-5ms peaks. They must not be presented as an exact allocator peak or as attributable only to one model. The package records weights, gradients, optimizer tensors, process samples and query timings, but **full lifecycle memory, energy and the user's device budget remain open**. No one/two-bit eligibility storage or native packed execution was attempted. A hard gate decision is not an all-one-bit learning system.

## 7. Verification and limitations

All28 new unit tests passed. They cover actual finite-gradient parameter updates, deterministic data, exact controls, state-off, event budgets, unmutated query state, scope reset, data-only checkpoint restore, and rejection of mismatched scope/weights/policy or corrupt artifacts. All20 trained checkpoint files were reloaded in a fresh interpreter; their initial seeded identities, changed-element counts and final weights were independently checked. Their3000 main metric cells and interventions were re-evaluated with matching counts and dataset hashes. Lifecycle continuation and query predictions matched exactly under roundtrip restore.

One entire600-step GRU training trajectory was rerun in a separate interpreter. Its batch hash, final parameter digest, changed-element count and safetensors checksum matched exactly. That is one full optimization reproduction, not a claim to have retrained all20 models twice. Gate diagnostic receipts are distinct from main-pilot verification. A fresh-package verification receipt accompanies the delivered ZIP.

The foundation's68 tests, dependency check and974-file manifest passed afresh without modifying the foundation. The full historical release suite, Windows launchers, generic Forge/Runtime integration, real-language models and production qualification were **not** tested by this study. The hard budget here is a configured small experiment, not an adversarial resource sandbox. State integrity is not proof of semantic correctness.

## 8. Next bounded work order

**Carry forward learned write admission as a candidate, not a conclusion that tri-core cognition is complete.** The next registered study should compare soft training followed by fixed/qualified admission with direct hard-gate training and stronger long-horizon training controls. It needs fresh seeds and episodes, multiple independently addressed facts, genuine updates versus distractors, ambiguous/noisy write signals, and longer delays. Retain the exact-memory and full-history Transformer controls, count preparation costs, and freeze criteria before confirmatory scoring.

After robust event retention is established, use a harder multi-step relational task to assess internal depth. Delayed-credit learning and trace precision follow as NBR-02/03; they should not be mixed into this inference-state result. No production core replacement is recommended on this evidence.

## 9. Evidence map and research attribution

Project basis: `NSS_Cognition_Architecture_and_Low_Bit_Learning_Handoff_v1.0`, especially pages3–6,8–14 and19–23; source foundationREADME and TriCoreFoundation001 audit. Those documents motivate the questions but do not establish these new results. Measurements in this report come from this package's executable files and receipts.

Raw results: `evidence/pilot/*_seed*.json`; original and amended protocols: `spec/`; all-seed aggregation: `evidence/SUMMARY.json`; post-pilot evidence: `GATE_DIAGNOSTIC.json`, `GATE_ISOLATION.json`; reproducibility: `INDEPENDENT_VERIFICATION.json`, `TRAINING_REPRODUCTION.json`; source preservation: `PILOT_INPUT_PRESERVATION.json`. Per-seed logs, failures and source snapshots are retained rather than substituted with a best-run summary.

Established mechanism references—not reproductions claimed by this study: Cho etal.(2014), *Learning Phrase Representations using RNN Encoder-Decoder*, arXiv1406.1078; Bengio, Léonard and Courville(2013), *Estimating or Propagating Gradients Through Stochastic Neurons for Conditional Computation*, arXiv1308.3432; Dehghani etal., *Universal Transformers*, arXiv1807.03819; Dai etal., *Transformer-XL*, arXiv1901.02860. The implemented GRU and Transformer layer API were checked against official PyTorch2.10 documentation. This pilot's particular tasks, variants and diagnostics are project engineering work; no claim is made that gated persistence or straight-through estimators are new inventions.

**Bottom line: the first useful improvement was controlling when state is allowed to change—not adding another core or compressing an already-unreliable memory.**
