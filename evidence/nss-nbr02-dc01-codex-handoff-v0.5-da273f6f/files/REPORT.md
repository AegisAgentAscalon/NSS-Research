# NSS-NBR02-DC01 — full gated pass after storage repair
## Execution v0.5; integrated scientific protocol v0.3; 25 September 2026

**The full initial/development/held-out study and its fresh adaptive replay completed. A0 immediate competence, D1 numerical/delay fidelity, D2 adaptation/old-association retention for both learners, and D3 the small-sample local-rule noninferiority screen passed.** This is a bounded laboratory result, not superior learning in general, an overall efficiency pass, or automatic NBR-02 closeout.

The retained failures are informative: every held-out learned primary error was the first post-feedback response after an abrupt label reversal. The update was independently verified and reduced that case's loss, but did not always move the output across the correct class boundary. After the next corrective receipt, both methods answered correctly. The experiment does not uniquely identify clipping as the cause of that lag.

## 1. What was repaired

v0.4 remains STOPPED_AT_STORAGE_ADMISSION. Its 240 applications and complete stopped evidence are not erased. It had never fitted the main models or generated held-out associations.

The repaired delivery representation decodes the durable per-frame record envelopes and compresses them together with XZ. Restoration reproduces the original framed bytes and checks the original SHA-256. All arrays, aliases, metadata, gradients, failures and independent replay remain retained. Probe weights are discarded as before. The live fsynced record format, scientific computation, scoring, seeds, task and gates were not changed.

The same cost sample, application multiplier and twofold safety margin now give a delivery forecast of **62,694,619 bytes**, below 67,108,864. The cost sample's decoded envelopes occupy 1,440,157 bytes and losslessly compress to 495,256 bytes. The old per-frame forecast was 92,784,897 bytes. This is an encoding repair, not neural-memory compression or a weakened scientific criterion.

The old copied `209 MiB` boolean was removed. The replacement enumerates eleven record kinds, their complete counts and dtype/shape payloads, variable-header allowances, frozen-array aliases and nonnumeric reserves. It projected 231,282,164 bytes of encoded capture versus the 256 MiB cap. **Compression forecasts remain empirical, not formal worst-case proofs.** The reported no-alias logical-envelope upper allowance is 385,669,872 bytes; that is not the stored footprint of the losslessly encoded/aliased evidence. Actual completed record counts, header sizes and array sizes were checked independently (`audit/ACTUAL_SCHEMA_ACCOUNTING.json`). Actual runtime and delivery caps remain enforced.

No main fit, cue label, learning rate, norm-clipping rule, threshold or fit count was adjusted after seeing results. New execution limits include all prior attempts. Prior recorded active work (864.208668 seconds) plus this authorized repair turn share the two-hour active-work ceiling; the inactive inter-turn conversation gap is explicitly excluded. This is not a claim that the total calendar interval was two hours.

## 2. What was tested

The new laboratory network has 674 float32 parameters, a 16-unit dense tanh recurrent cell and a two-class readout. START, PRIME(scope), and CUE create the prediction. G retains a true reverse-mode computation graph. L retains a specified diagonal-sensitivity eligibility approximation that omits cross-neuron derivative terms. Both update all five parameter tensors with plain SGD, learning rate 1 and global gradient-norm clipping at 1.

One identified receipt is pending. Parameters and cue-time learning information remain fixed while 0, 8 or 32 detached filler events are processed. A receipt contains the target but does not resend cue features. Temporary state resets after each receipt; learned parameters persist inside its condition. Conditions restart from their respective initial-fit checkpoints. Thus post-feedback scratch queries test changed parameters, not a recent answer sitting in live recurrent state.

Eight old associations are initially learned; four different focal associations are used in development, and eight different focal associations in held-out streams. Four paired fits are retained. Each base crosses stable/reversal policy and three delays. The transaction schedule is f,p,f,f,p,f. A reversal changes f at the third receipt. Five primary queries follow the receipts at trials 2,3,4,5,6. Predictions made before each receipt are a separate raw score.

There are 48 held-out streams, 240 primary occasions across all three delays, repeated across four fits. Delay-zero summaries below contain **80 occasions × four fits = 320 readouts**; these are not 320 independent association tasks. Eight bases, not invariant delay repetitions or frozen-control duplicates, supply the principal paired breakdown. Four named families are bookkeeping pairs of bases rather than IID population samples.

No historical Q010, TS01, TS02 or TS03 model was loaded or changed. This does not test multiple pending receipts, moving cue-time parameters, ambiguous credit attribution, learned workspace writing, or integrated NSS cores.

## 3. Admission and predefined decisions

All eight initial-fit model inventories (four G/four L) answered 8/8 old cues correctly. Zero-delay development primary scores were G: 38,36,37,38/40 and L: 39,36,38,38/40, versus each fit's own frozen control at 28/40. Both arms passed A0 in **4/4 fits**, exceeding the required 3/4. All fits were then evaluated; none was selected away.

| Predeclared decision | Result |
|---|---|
| A0: initial and immediate-feedback competence | PASS, both arms 4/4 fits |
| D1: exact/formula fidelity, update arithmetic, delay invariance and fresh adaptive replay | PASS |
| D2-G: focal loss improvement with old-association retention | PASS, 8/8 bases for each criterion |
| D2-L: focal loss improvement with old-association retention | PASS, 8/8 bases for each criterion |
| D3: L within declared accuracy/loss/retention margins of G | PASS, all 8 bases meet both per-base margins |
| Overall efficiency/superiority | NOT ESTABLISHED; not a blanket gate |

D2's focal-loss improvements over each learner's own frozen control range from 0.546 to 0.846 nats for G and 0.603 to 0.924 for L. Old-inventory classification loss is zero in all bases. D3's pooled L−G accuracy difference is −0.3125 percentage points and loss difference −0.011598 nats. These are fixed exploratory margins and observations, not statistical confidence bounds or equivalence beyond this small task.

## 4. Held-out answers after feedback

| Method | Correct at delay 0 | Accuracy | Mean loss |
|---|---:|---:|---:|
| G, exact-gradient learner | 302/320 | 94.375% | 0.107930 |
| L, approximate eligibility learner | 301/320 | 94.063% | 0.096332 |
| N_G, frozen G initial fit | 224/320 | 70.000% | 0.518088 |
| N_L, frozen L initial fit | 224/320 | 70.000% | 0.535967 |
| X, causal last-observed label table | 80/80 unique occasions | 100% | Not a neural probability model |

Across all delays, G is 906/960 and L 903/960. Those tripled denominators do not add independent performance evidence: the per-method trajectories are bit-identical across delays.

Every old-association endpoint inventory is correct: **512/512 at delay 0 for each learner**. Adding the focal association gives 576/576 complete-inventory answers per learner. Mean old-inventory probability loss nonetheless rises from approximately 0.00236 initially to 0.01618 for G and 0.03879 for L. Retained labels are not identical to unchanged confidence, and the full old inventory was sampled at condition end, not after every intervening step.

X's perfect post-feedback score follows its deliberately strong ordinary bookkeeping contract. It has just observed the relevant label and records it exactly. It does not know an unannounced reversal or a new label before the receipt.

## 5. Failure-first analysis: where the misses actually occurred

### First reversal correction, not trace loss

Stable-policy primary probes were **160/160** for each method. Under reversal, all post-feedback errors occur at trial 3:

| Reversal checkpoint, delay 0 | G | L |
|---|---:|---:|
| Before the first changed label is released | 0/32 correct | 0/32 correct |
| After its first corrective update | 14/32 correct | 13/32 correct |
| After the next receipt with that changed label (trial 4) | 32/32 correct | 32/32 correct |
| Final focal probe after trial 6 | 32/32 correct | 32/32 correct |

The first pre-feedback reversal mistakes are expected surprises under the declared information contract. The **18 G and 19 L post-feedback misses** are genuine lag in adaptation, not excused by the lack of advance warning. Across the invariant delays those produce 111 retained held-out learned-primary failures.

For every one of the 37 delay-zero post-correction failures, the audit establishes: the receipt matched; the pending record and parameter version survived the delay; the raw gradient matched the method's specified equation; norm clipping and SGD application were correct; the resulting prediction loss decreased; but the class remained wrong. Exact-G gradient checks and exact-at-L-prestate comparisons are distinct. `scores/FIRST_REVERSAL_FAILURES.csv` joins each error to its actual gradient and applied step.

All 32 first-reversal gradients per method were clipped. G raw norms were 5.20–6.99; L raw norms were 5.87–7.61; the applied step norm was capped at 1. These observations motivate testing correction dose. **They do not prove clipping caused the lag:** the initial margin, gradient direction, nonlinear state response and shared parameters can also matter. A larger step's effect on old knowledge was not tested.

### Before-feedback probability quality is worse than the primary score suggests

Across 384 delay-zero before-feedback readouts, G correctly predicts 308 (80.21%) and L 303 (78.91%), versus N_G 262 and N_L 258. Yet mean pre-feedback losses are **0.7148 for G and 0.7247 for L**, worse than **0.5682 and 0.5862** for their frozen controls. The learners confidently predict the previously taught label before an unannounced reversal: mean loss at that boundary is 5.842 and 6.014 nats.

Learning improves class accuracy and the post-feedback criterion, but high confidence makes the reversal surprises expensive under log loss. The original primary score must not be substituted for these earlier predictions. A future calibration or reversal-speed intervention must retain both surfaces.

### Approximation is substantial but not a formula failure

Across L's 384 delay-zero held-out updates, its encoder-gradient difference from the exact derivative **at L's own pre-update weights** averages 0.7668 in relative norm; mean cosine is 0.6468. This is not a 76.68% prediction-error rate. L is implementing its approximate equation correctly, and still met D3 here. Neither that gate nor small task error establishes that dropped cross-neuron terms will remain harmless on deeper causal tasks.

### Complete negatives and detector coverage

The primary capture retains 24,196 scored query rows and **3,238 incorrect rows** across all phases/methods, including frozen controls and explicitly marked fixture/cost diagnostics. `scores/FAILURE_INDEX.csv` retains every negative and its phase rather than pooling all denominators. Replay is not a second scientific sample.

The 14-category fault suite and clean/tolerated controls passed in each execution, including eight charged intentionally wrong SGD applications per pass. The later live diagnostic also rejected 96 wrong-scope/consumed-or-unknown receipt envelopes per pass without changing pending state. Some fault checks are synthetic or copied-record tests, not comprehensive live injections. Authenticated incorrect outcomes without a public cue remain unidentifiable. No natural learner update has unknown completion.

## 6. Costs and a newly documented measurement limit

The retained local numerical payload is 2,760 bytes, including 2,560 bytes of eligibility. G's saved-tensor inventory for the three-transition graph is 1,692 unique storage bytes, of which 1,152 are shared parameter buffers and 540 are nonparameter tensor storage. Those counts exclude native graph-node overhead and are **components, not comparable whole-process costs**.

The inherited Python object walker does not follow NumPy `ndarray.base` or native autograd graphs. In particular, L's reshaped diagnostic trace-history array has a 7,680-byte backing buffer that can be absent from that object-inventory subtotal. This source-inspected limitation is recorded as **OBS-DC01-COST-001**; it is not a proposed cause of prediction errors. The stored full trace arrays and sampled process-memory limits remain available, but the reported Python subtotals must not be used to declare an overall memory win.

No overall resource advantage for L is established. The experiment's scientific approximation question passed its bounded performance screen; an efficient-learning claim still needs credible complete cost measurements and an actual named improvement. Output compression is unrelated to neural trace compression.

## 7. Reproduction, limits and all attempts

Fresh-process replay reinitialized and repeated the entire executed learning schedule, including initial fits, development/held-out conditions, cost probes, receipt diagnostics and isolated update faults. It matched **42,402 frames, 117,866 arrays and 29,728,572 numerical elements**, plus exact messages, instantiated plans, event hash chains, gate decisions and all **27 stage-level CSV tables**. This is internal independently scored adaptive replay, not third-party replication or cross-device equality.

Each final audit independently reconstructed 13,489,880 scalar comparisons; maximum tolerance ratio was 0.059794 under the unchanged empirical `2e-6 + 2e-5*abs(reference)` tolerance. No near-equality was excused by applying Q010's unrelated underflow amendment. Delay invariance separately checked 64,600 array comparisons / 11,050,368 elements per pass, excluding live filler state and timings.

The new capture's initial 1,050,202 framed-record bytes also reproduce the old completed v0.4 prefix exactly. The original stopped archive remains separate historical evidence, not silently replaced by a successful status.

| Quantity, all attempts including v0.4 | Actual | Original ceiling |
|---|---:|---:|
| Update attempts / durable commits | 9,088 / 9,088 | 9,800 |
| Recurrent cell evaluations | 331,744 | 400,000 |
| Head evaluations | 48,672 | 60,000 |
| Reverse-mode backward calls | 4,560 | 5,000 |

No scientific fit retry or post-result extra training occurred. Each new pass has 4,424 committed applications, including diagnostic/probe/sandbox work. Checkpoints, every pre/post parameter version, gradients, RNG records, cursors, public events and negative outputs are retained. Stateless SGD has no momentum slots. Cue-time graphs are not claimed portable serialized Python graphs: their reconstruction inputs and forward tensors are retained. Filler generators are independent, seeded transactions; their recipes and actual draws are retained, not falsely described as separate persisted final generator snapshots.

Sampled peaks were 1,152,192,512 bytes for a supervised process tree and 2,397,687,808 bytes for the container. Sampling was every0.1seconds; short peaks and the initial setup interval are not claimed fully covered. The two new supervised executions took about78.1 and79.6seconds including their internal audits. These are not deployment-speed comparisons between G and L. Delivery QA and the aggregate active clock are receipted separately.

## 8. Disposition and next candidates

`RET-DC01-DELIVERY-001` is resolved for this delivered bounded workload, with the forecast assumptions explicitly preserved. DC01 completes a bounded adaptation/retention reference, not general temporal-credit attribution. NBR-02 remains active; no automatic NBR-03 or NBR-04 dispatch or phase-closeout decision occurred.

Recommended next proposal: isolate the first-reversal correction-dose question at unchanged task/model/feedback access and fixed old-knowledge checks. Separately propose a genuinely longer causal-dependency test, and only then consider more elaborate eligibility approximations. Detailed candidates are in `CANDIDATES.md`; none was executed.

The maintained management-token concept and `RET-MW01-FIT-001` remain parked/open. NBR-01's bounded closure stays adopted. `FCR-0103-001` requires returning to the unresolved01–03 foundations after03 and before04. The parent Architecture Ledger and all historical Q010 evidence gaps remain unchanged. All G01–G22 questions travel in `protocol/PROGRAM_CONTEXT.md`.
