# NSS-NBR02-STATEBRIDGE01 — interrupted task state across learning and repair
## Prospective scientific protocol v0.1 / execution v0.1

User authorized the state-learning bridge and suggested per-task weight freezing. This execution completes the previously open task, model and budget choices. It is not a tri-core test, not a rerun of NBR-01, and not a new G-versus-L learning-rule contest. One EXACT reverse-mode learner is used to isolate the state/version boundary; no old checkpoints are loaded.

## Question
When shared model weights learn a changed association, and subsequently receive one fixed repair cycle, does an unfinished task state still support correct continuation? At the SAME post-change weights, compare reuse of old state to reconstruction from the same observed history and no-history reset. Keep an old immutable weight revision as a separately costed task-pinning reference. Rebuild is inference, never another application of training feedback.

## Task A, task B, and model
A is a four-bit task checklist. Public codes SET0–3=0–3, CLEAR0–3=4–7, RESET=8, NOOP=255. RESET is a learned event; NOOP has explicitly supplied identity-state routing. The model reports four independent bit logits and five next-incomplete/DONE logits. No state/answer oracle enters the transition. Current A semantics NEVER change during B learning.

B is four scoped binary associations. Public inputs are START_B=9, scope=10 or11, cue=12–15. All four associations are initially taught; the online condition reverses ONE of them while preserving the others. B uses the SAME bit-0 output logit as A (binary sigmoid), not a separate insulated head. Task markers distinguish their meanings. Using a shared output is deliberate, not a diagnosed location of previous NSS failures.

Fresh model: GRUCell(input16,hidden64) + Linear64→9, 16,329 float32 parameters (65,316 tensor bytes). Exact gradient on all six parameter tensors. Uniform initialization ±.125 from a dedicated hashed Torch seed. No historical hidden vector is transplanted. Each A instance has64float32 state entries (256 bytes); 32 active logical instances share one parameter version, not32 model copies. Physical execution is serial: this does NOT benchmark multithreading, live serving atomicity, or a concurrent training deployment.

## Initial fitting
Four NEW fits, each exactly2,000 Adam updates (lr.001, standard betas/eps, no decay, foreach/fused false). Each update has16 A episodes, alternating length17/33, supervised at each step with mean bit BCE + next-action CE; plus the mean B BCE over the four 3-event cue prefixes. Sum A+B with weight1 each. Gradient norm clipping1. Dedicated PCG64 training events, actual bytes retained; no selected checkpoint, sweep, retry, or extra fit.

A training codes are uniform0–9, with9 mapped to supplied NOOP; unused padding excluded from loss. Readout labels reconstructed from history, never supplied as input. Full Adam/model/runtime and dedicated RNG state/cursor at0,250,...,2000, actual event arrays, every loss/norm/input hash/post-weight hash retained. Initial gradients and full activation graphs are NOT all archived; full adaptive replay checks every initial update hash. Online and repair gradients/states/weights ARE completely captured.

## Evaluation histories and prior support
Development32 A prefixes: all16 end masks at lengths17/33. Test32 fresh prefixes: all16 at33/65. Earlier events randomized; final four public SET/CLEAR operations provide balanced endpoint states. This is NOT a claim of long-term dependence on every earlier event: the final four steps set the checkpoint state. The continuation suffix is8operations; at least one bit never changes, so identical suffixes require different outputs for different histories. Query positions0,1,2,4,8 after the interruption; additional states/logits retained as auxiliary evidence.

Development B scenarios are cue/order(0,0),(2,1). Main scenarios are4focal cues×2 transaction orders, NOT eight independent cue types. They repeat known elementary grammar and include development order identities; only A histories are fresh. No external generalization claim. Interpretation is a controlled interface diagnostic.

A0 before adaptation/main histories: each fit≥95% A joint on160development queries,4/4 B old associations, CARRY–RESET advantage≥40points, exact unchanged CARRY/REBUILD equality. Group requires≥3/4 fits. If admitted retain all4. Otherwise stop and preserve initial/development-gate evidence with no main generation. Admission checks base ability, not whether the proposed repair succeeds.

## Learning intervention and fixed repair
Each scenario resets PARAMETERS to that fit's initial terminal checkpoint. A is first paused with its saved state h0 and public prefix. Scratch learning has separate arrays and no pending task-A derivative. Cue-time B forward occurs before receipt target enters loss. Eight online SGD steps, lr.5, clip1; five focal corrections and three unchanged cue receipts in one of two fixed orders: f,f,p0,f,p1,f,p2,f OR p0,f,p1,f,p2,f,f,f. No score-directed schedule.

Then exactly4 SGD repair applications, lr.1, clip1. Each uses8 previously observed A training episodes (length17) plus all4 B associations at their now-current released labels. The32 A examples are the first two length17 training batches, divided into four fixed groups. Same lossA+B as initialization. This is fixed balanced rehearsal, not optimized maintenance, a dream, or clean-data curation. It cannot receive current test-A labels. Clip uses concatenated float32 norm, factor=min(1,1/(norm+1e-6)), float32 gradient×factor×lr, then float32 parameter subtraction.

## The state × parameter comparison
At theta0, theta1(after8online), theta2(after4repair):
- CARRY: saved h0, current theta.
- REBUILD: recompute full allowed prefix at current theta, then same suffix. No training replay.
- RESET: zero state, same suffix; deliberate information removal.
- PINNED: use h0 AND immutable theta0 via explicit version route; same task evidence/suffix. This has old-state compatibility by construction and cannot absorb the newly reversed B association at that revision.

All modes read the SAME independent A oracle. Head/state difference is not semantic failure by itself. All B cues are queried at every stage and after every online/repair update. Separate old-weight B results expose learning staleness. Store prefixes, state-producing version, consuming version, candidate hashes, saved-state hashes, and all evaluated states/logits. h0 and theta0 byte integrity checked after every learning stage.

Per-task pinning here is one numerical control with32 logically separate states sharing theta0, plus an updated candidate. It is NOT a trained token interface or model-per-task service. Compact task/version/evidence metadata and deferred record curation are documented proposals, not numerical treatment arms.

## Decision and measurements
Primary scientific output: paired carry versus rebuilt continuation at identical theta; report cases where each rescues the other, change from theta0, bit and next-action accuracy, loss, B acquisition/retention, actual reconstruction transitions and stored-state/parameter bytes. No hypothesis is forced to win.

Prospective bounded adequacy diagnostic after repair: for each scenario, A joint≥95%, decline versus same-case theta0 carry≤5points, and the changed B focal class correct. Group requires29/32 scenarios AND≥6/8 in each fit. This is a small pilot rule, not operational safety or a statistical equivalence claim. Record individual old-B and A errors even on a passing scenario. PINNED is not eligible for a joint new-learning pass simply because A is perfect. No zero-internal-drift requirement. Both modes poor may mean lost competence; rebuild better means a state-interface effect, not a uniquely localized mechanism. If carry suffices, do not invent a migration requirement.

## Integrity, evidence, and budget
Four initial fits +8development contexts +32main contexts. Each context12updates. Untrained fixture4online+4repair applications;4deliberately bad small-array applications isolated from model weights;20initial cost-probe updates discarded. Per pass 8,512 applications, of which8,508 have actual neural backward calls. Capture+genuine adaptive replay17,024 applications,17,016 backwards. Frozen caps18,000apps/18,032backwards/12Mcell examples/12Mheads. Source-level planned cells per pass3,696,828; heads3,712,572. Independent NumPy reconstructions are separately recorded non-Torch audit work, not extra training.

CPU deterministic float32 Torch2.10.0+cpu, NumPy2.3.5; one intra/inter-op numerical thread. Independent NumPy float64 GRU/backward/Boolean oracle uses empirical2e-6+2e-5abs(reference), not a proven roundoff bound. Wrong update bytes stop even if predictions look good. Fixture derivative/adoption checks precede main fitting. Foreign versions, lost state, missing completion, source modifications, nonfinites, or numerical inconsistency are engineering failures. Scientifically poor results finish within budget; do not tune.

Two-hour wall limit starts at initial execution preparation receipt03:16:45UTC on26Sep2026, not reset at source export. ProcessRSS3GiB/container3.5GiB. Retained encoded study≤512MiB; final full delivery≤128MiB, compact review separate. A conservative schema bound is documented before main fitting; monitor actual size. Full source package exported before numerical work. Interrupted intents remain unknown until supported by durable evidence; no automatic fit retry. Historical unrecorded attempts from other studies are NOT charged as zero to this new study, and no old budget transfers.

Full adaptive replay starts fresh models, optimizers, RNGs and counters and recomputes the complete executed prefix. Independent scorer checks every recorded online/repair exact gradient, SGD application, resumed trace and semantic label; initial fitting is reproduced, not independently optimized by a second framework. Relocated rescoring does no model calls. Lossless packaging or aliases only after actual equality checks; omissions and reconstruction assumptions explicit.

## Scope
NBR01 bounded closure unchanged; NBR02 mechanism-led. No tri-core/shared-backbone adoption, learned context curation, teacher, synthetic self-play, approximation comparison, source retirement, old-state migration model, or new phase dispatched. Existing parked/deferred tickets and FCR0103 preserved. A later per-task version scheduler/clean-record pipeline requires its own control, capacity and freshness contract.
