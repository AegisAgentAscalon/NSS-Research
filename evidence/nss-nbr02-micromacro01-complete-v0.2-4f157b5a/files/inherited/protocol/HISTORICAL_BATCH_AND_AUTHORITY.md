# REHEARSE01 v0.1 — derivative, batch and evidence contract
Status: proposed numerical/authority specification; no new implementation or numerical check executed.

## 1. Pinned single-example arithmetic
The historical definitions are readable in sources/PROTECT01/source/base_runtime.py and rev_runtime.py.
Do not import their experiment runners or reuse old update ceilings. Their hashes are in SOURCE_IDENTITIES.json.

G differentiates cross-entropy of the final cue logits through all three transitions from zero h.
For L, reset EW[16,23], EU[16,16], Eb[16] to zero at every new example. With h_old before the transition,
d=1-h_new**2 and u=diag(U):
    EW_new[i,j] = d[i] * (x[j] + u[i]*EW_old[i,j])
    EU_new[i,j] = d[i] * (h_old[j] + u[i]*EU_old[i,j])
    Eb_new[i]   = d[i] * (1 + u[i]*Eb_old[i])
At the cue output q=p-onehot(y), v=V.T@q:
    gW = v[:,None]*EW; gU = v[:,None]*EU; gb=v*Eb
    gV = outer(q,h_cue); ga=q.
Omitted off-diagonal sensitivity propagation is intentional. Each F/R example uses its own reset traces.
L never calls exact differentiation to choose or apply its old-replay update. Independent exact-at-L-prestate
audit gradients may be stored as diagnostics only; they must not reach the learner.

Parameter/vector order is W,U,b,V,a, row-major, totaling674 scalars. Live h and numerical trace payloads
have separate lifetimes from model weights and observation records.

## 2. Batch meaning: eight gradients at one parameter version, one application
At batch start freeze theta_plus, the post-clip2 model. No hidden answer, stored gold progress, current score
or evaluator branch is available to the learner. Set:
    F records = [newest lawful focal receipt]*8
    R records = [current valid old receipt at cue0,...,cue7].
Each entry includes the scoped START/PRIME/CUE recipe, observed outcome, source receipt ID, current
revision/validity and feature identity. F repetition is intentional; R requires eight distinct old keys.

For i=0..7:
1. Validate the record against the public journal and the fixed selected list.
2. Assert parameter bytes are theta_plus, initialize temporary state, perform three forwards.
3. Compute the method's raw float32 per-example gradient g_i at theta_plus.
4. Record source identity, inputs, forward tensors, g_i and cleared temporary state.
Release each G graph after its derivative. Do not retain eight graphs solely to produce the average.

Use a float64 zero accumulator. For i=0..7 in order, add float64(g_i); divide by exact8; cast once to float32.
That ordered result is g_bar. Record the eight gradients, accumulator, mean and cast result.
    n = float32_vector_norm(g_bar)
    c = 1 if n==0 else min(float32(1), float32(1)/n)
    step = float32(g_bar*c)
    theta_after = float32(theta_plus-step)
Apply simultaneously to the five tensors from that common prestate. No per-example clipping, serial SGD,
per-layer clipping, sum-without-division, weighting by current error, or parameter reset is permitted.
Ordinary online clipping keeps the inherited float32 path; this float64 reduction applies only to the new batch.
Nonfinite values stop before committing. A zero mean still has one attempted/committed application.

Eight repeated F gradients are numerically identical under the fixed deterministic shape. A float64 sum of
eight identical finite float32 components can represent their sum exactly, and dividing by8/casting recovers
the component. Thus the reducer must return that same raw float32 vector. This is an algebraic/reduction
identity to check in execution, not permission to omit seven recorded gradient examples.

## 3. A receipt is consumed once; its evidence may be replayed
A branch validates and consumes environmental receipt3 once. It writes a durable online UPDATE_COMMIT.
The F/R follow-up is REHEARSAL_INTENT -> validated replay records -> REHEARSAL_COMMIT. It does not call
FEEDBACK_RELEASED again, increment the trial cursor, accept the same receipt a second time, or mutate the
last-observed target. A new parameter version and application ID do result.

The authoritative focal label is the latest publicly released correction; the prior focal label is stale.
R's old keys exclude f. The old records are stable in main streams except their repeated confirmations;
the parser must still distinguish a live, overwritten, revoked, conflicted or foreign-scope source in fixtures.
Do not derive record handles from labels. Repeated source IDs are lawful in F only when the declared batch
list deliberately references the same already-consumed receipt. Duplicate UPDATE_COMMIT IDs are not lawful.

A missing/invalid R record stops BUFFER_INVALID rather than producing a seven-item batch or fetching gold.
Authenticated wrong feedback with no public inconsistency remains unidentifiable; the scorer cannot
be used as an authority oracle. Current validity does not prove that a real-world label is true.

## 4. Indispensable batch/fork checks
* Every example's parameter hash equals batch_entry_hash; state/eligibility begins zero each time.
* Record list/order exactly equals the declared F or R list; sources have been released before batch start.
* U/F/R online post-clip2 weights and scores match before either extra step.
* All B1/U/F/R pre-correction parameters and raw focal gradients match before their clip differences.
* Exact reconstructed cue values match the original; reconstruction is not labelled pre-feedback prediction.
* Frozen N never changes parameters. Queries never change state, archive, label table or update counters.
* F's captured gradients repeat exactly; R's full eight gradients are retained even if equal or zero.
* Independent reduction from captured raw32 arrays matches accumulator/mean/cast exactly.
* Independent NumPy derivatives use the same prestate and legal three-event prefix.
* Actual float32 SGD output is independently byte-checked from captured raw gradient/norm factor/product.
* Numerical tolerances for mathematical reference are abs(diff)<=2e-6+2e-5*abs(reference).
  This is an empirical elementwise check, not a proof of a true-gradient error bound.
* Fresh adaptive replay repeats each same-method gradient and application, including initial fits and probes.
* Q010's historical +2^-126 softmax verifier amendment is unrelated and is not repurposed.

## 5. Failure localization
Keep raw observation, first observable mismatch, proposed explanation, tested mechanism and evidence gaps
separate. Examples:
- Mean differs from independent reduction: batch arithmetic/implementation fault.
- Correct mean and step, old quality improves but focal flips wrong: genuine recovery–adaptation trade-off.
- R/F both improve similarly: generic extra learning is not evidence for selecting old records.
- Wrong old label sourced from the scorer rather than public history: invalid experiment, not learning failure.
- Logger commit absent: unknown completion, not zero-cost restart.
- High-probability old answers yield a small batch mean: candidate dose/signal issue to analyze, not a reason
  to silently enlarge the update. Its cause must be tested separately.
