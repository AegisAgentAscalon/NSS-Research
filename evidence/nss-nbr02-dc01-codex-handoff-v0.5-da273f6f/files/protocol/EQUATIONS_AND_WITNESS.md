# Exact and approximate derivatives; proposed runtime checks

**Status:** algebraic review and fixed diagnostic specification. No model, autodiff engine or numerical fixture was executed here. Scalar parameter/budget arithmetic was checked independently of any learner.

## 1. Exact sensitivity versus retained diagonal component

Let theta be a parameter in postsynaptic row i of W, U or b. With D[t]=diag(1-h[t]^2), its exact recurrent sensitivity vector obeys

    J_theta[t] = D[t] (s_theta[t] + U J_theta[t-1]), J_theta[0]=0.

The source vector s has only component i nonzero: x[j] for W[i,j], h_prev[j] for U[i,j], and 1 for b[i]. For dense U, a perturbation introduced at neuron i can propagate into other neurons and later contribute to the readout.

L keeps only a scalar sensitivity assigned to the parameter's postsynaptic neuron and propagates that scalar through U[i,i]:

    d[i]       = 1-h[i]^2
    EW[i,j]    = d[i] (x[j]      + U[i,i] EW_prev[i,j])
    EU[i,j]    = d[i] (h_prev[j] + U[i,i] EU_prev[i,j])
    Eb[i]      = d[i] (1         + U[i,i] Eb_prev[i]).

All right-hand sides use previous traces and the pre-transition state, never partially updated rows. EW,EU,Eb begin at zero for every trial and are updated only for START/PRIME/CUE. Freeze copies at cue time. Do not update, decay or overwrite those snapshots during fillers.

At receipt, q=p_c-one_hot(y), delta=V_c^T q:

    gW[i,j]=delta[i]*EW[i,j]; gU[i,j]=delta[i]*EU[i,j]
    gb[i]=delta[i]*Eb[i]; gV=q outer h_c; ga=q.

G differentiates exactly through all three causal transitions. It includes the cross-unit contributions that L omits. Both use the same forward cell and loss; L uses the ordinary output derivative, not a random feedback matrix. The algorithm is not declared biologically local or a named RFLO/e-prop replication.

Raw gradients are concatenated W,U,b,V,a (row-major). Clip by factor min(1,1/||g||_2), with factor 1 at zero norm. Then apply theta_new=theta_old-1.0*g_clipped. All raw components and the norm use pre-update parameters. No projection, momentum or optimizer state is present. Log raw gradient, clipping factor and committed result. Independent checks reconstruct clipped values from the stored raw gradient; no missing clipped-array history is implied by that lossless representation.

## 2. Why the diagonal special case is exact—and its limit

At a fixed diagonal U, any source perturbation initially in row i remains in row i during subsequent propagation. The vector recurrence reduces to L's scalar recurrence, so the raw derivatives agree in exact arithmetic.

This statement is about the gradient at that parameter point. If the full dense U is then updated, an off-diagonal entry can become nonzero. Do not claim G/L trajectory equivalence from a diagonal initialization alone. Fixed diagnostic examples are reset before each check, not learned sequentially.

## 3. Fixed coupled witness with a closed-form reference

Use H=16,D=23, all h initially zero, and all parameters zero except

    U[0,0]=1/2; U[1,0]=1/2; U[1,1]=1/2; V[1,1]=1.

Inputs in order are START=e22, PRIME(scope0)=e20, CUE(0)=e0. Use target class0 at the receipt. All states are zero, tanh derivatives are exactly1 in real arithmetic, p=(1/2,1/2), and readout sensitivity delta=(0,1/2,0,...).

The exact backwards sensitivities at t3,t2,t1 are respectively

    (0,1/2), (1/4,1/4), (1/4,1/8)

in the first two neurons. Therefore the only nonzero exact W components are

    row0: W[0,22]=1/4, W[0,20]=1/4
    row1: W[1,22]=1/8, W[1,20]=1/4, W[1,0]=1/2.

Exact gb[0]=1/2 and gb[1]=7/8. L has the same row1 entries, but all its row0 components and gb[0] are zero. Both have gU=0 and gV=0 at this operating point; ga=(-1/2,1/2).

On the encoder gradient vector (W,U,b):

    ||g_exact||^2 = 47/32
    ||g_exact-g_local||^2 = 3/8
    relative discrepancy = sqrt(12/47) ≈ 0.5053.

Thus the proposed exact-norm floor1e-3 and discrepancy floor0.05 have an algebraic witness. The witness does NOT have a nonzero gradient of U itself. Its discrepancy is in W/b gradients because their effects pass through the existing cross-unit U[1,0]. That limitation is explicit rather than concealed by the term 'recurrent gradient'.

The diagonal-zero control deletes U[1,0] and requires equality. The two nonlinear controls additionally set W[0,22]=0.4 (one with, one without U[1,0]); all other settings are unchanged. They exercise nonzero h and U derivatives. No threshold is chosen after examining a numerical run. The nonlinear coupled case must match independent exact/local calculations, not G=L.

Each of four cases runs both G and L once per primary/replay pass, three cells and one head per case/arm, zero optimizer updates. This reserves24 cells,8 heads and4 G backward calls per pass. Future runtime verification must meet the empirical scalar tolerance and the analytic witness discrepancy. A mismatch stops before cost probes or fitting.

## 4. Natural-update diagnostics

For every actual update, independently reconstruct its permitted three-event prefix and pre-update parameter version. Audit G against a float64 exact reverse recursion. Audit L against an independently written float64 local recurrence. Both references must be separate from producer functions.

At every L point, also retain or reproducibly regenerate the exact gradient at L's own prestate, measuring absolute/relative encoder-gradient difference, clipping effects and gradient cosine when norms exceed1e-12. A zero norm has a tagged undefined angle, not a fabricated cosine. Report U off-diagonal norm throughout training; a learned near-diagonal solution is allowed and must not trigger a post-result redesign of the witness.

Differences between G and L after they have learned different weights are trajectory differences, not direct measurements of approximation at the same state. No independent exact gradient or hidden target is fed back as a corrective hint to L.

## 5. Delay invariance

Given identical parameter start, receipt order and target sequence, each method's pending cue information is a deterministic function of its three upstream events. Fillers cannot change it. After receipt, live h and eligibility are cleared. By induction over trials, per-method predictions, raw corrections and learned weights are independent of filler count. This holds even for approximate L.

This is a designed invariance, not a tested fact in this proposal. G/L equality in dense recurrence is neither expected nor required. The short, explicit-ID task does not establish broad delayed credit assignment or a need for the learned system to infer which event deserves the correction.
