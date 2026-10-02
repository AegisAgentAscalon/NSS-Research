# Proposed numerical contract — PROTECT01 v0.2

**Reviewer-designed, unexecuted.** This document is the main target for the last Codex audit. It is not a report of successful QP, gradient, float32 or runtime tests. All constants below are proposed empirical engineering tolerances, not certified error bounds.

## N1. Sign, geometry and exact optimization problem

For old binary target y_i, m_i=z_y_i−z_(1−y_i); row a_i is its full exact derivative at theta0, in W,U,b,V,a order. “Exact” distinguishes chain-rule differentiation from L's deliberate approximation; recorded values still use finite precision. Inherit lowest-index argmax ties: a zero binary margin is class-correct for label0, not label1. Score all records; do not impose a positive-margin-only buffer.

Capture B1/B2 exactly as the inherited float32 raw-gradient norm, clipping factor and multiplication/subtraction. The QP target d2 is the negative captured float32 clip2 product, promoted without change to float64. Do not recalculate the norm in a different dtype for B2. eta=1 is unchanged. The solver is not a new learning-rate schedule.

    minimize 1/2 ||d − d2||², subject to A d ≥ 0.

Zero is feasible. The primal minimizer is unique; dual multipliers need not be. For the convention Lagrangian=1/2||d−d2||²−lambdaᵀA d, KKT is:

    d − d2 − Aᵀ lambda = 0
    A d ≥ 0, lambda ≥ 0, lambda_i (A d)_i = 0.

In exact arithmetic this is projection onto a closed convex cone; the projected norm cannot exceed ||d2||. The numerical certificate and cast allowance below are separate. No infeasibility fallback, ridge term, slack penalty, row removal, norm restoration, line search or post-output rollback is permitted.

## N2. Derivatives and row normalization

P and S each rebuild the eight old three-transition graphs with current, publicly released labels and the same theta0. Perform one exact reverse-mode margin derivative per record, including for L branches. Release each old graph after extracting its derivative. Save full float32 A and old logits. Independently reconstruct the old derivatives in float64 NumPy from source inputs; use the inherited `2e-6 + 2e-5*abs(reference)` elementwise check and report rowwise absolute/relative discrepancy. This does not guarantee the projected solution is insensitive to derivative error.

Promote each captured row to float64. For nonzero row i, r_i=||a_i||₂ and C_i=a_i/r_i. Exactly zero rows stay all zero and remain in checks and reports. Do not discard a small nonzero row by a magnitude threshold. Check nonfinites/overflow. Positive rescaling leaves the exact feasible set unchanged. Record A, C, r and all zero-row IDs.

The QP and its independent KKT audit use this same finite-precision input C. Also report predicted changes using the independently reconstructed mathematical reference A_ref; no stronger real-gradient guarantee is inferred from fidelity to C. Actual finite-step margins remain the scientific evidence.

## N3. Finite active-support enumeration (proposed solver)

Eight rows allow at most 2^8=256 support subsets. This is a finite audit-friendly proposal, not a measured fastest solver. Order rows by old cue coordinate0–7. Enumerate subsets by cardinality, then lexicographic row-index tuple; empty first. No early exit on a promising scientific score. Each subset is an attempt and is charged. Inspect all subsets even when an early certificate succeeds, except an exact zero d2 special case.

For a nonempty S, compute a thin float64 SVD of C_S = U diag(s) Vᵀ. Record all singular values. Define numerical rank by s_j > 1e−12 max(1,s_max). If rank < |S|, mark that support rank-deficient and skip its equality solve; **retain every row in the global constraints**. Dependent supports are skipped, not dependent constraints. A full certificate can still be represented on an independent support in the exact problem; near-dependent numerical failures are possible and must stop rather than trigger hidden regularization.

For independent S:

    t = Vᵀ d2
    d_S = d2 − V t
    lambda_S = −U (t / s), with all other lambda entries zero.

This projects onto the equality subspace for S and constructs the multipliers without solving normal equations of the Gram matrix. Then check the full eight-row KKT conditions. For S empty, d=d2 and lambda=0.

Let b=max(1,||d2||₂). Admission thresholds:

- primal: max_i max(0,−C_i d) ≤ 1e−9 b;
- dual: max_i max(0,−lambda_i) ≤ 1e−9 b;
- stationarity: ||d−d2−Cᵀlambda||_∞ ≤ 1e−9 b;
- complementarity: max_i |lambda_i C_i d| ≤ 1e−9 b²;
- norm: ||d||₂ ≤ ||d2||₂ + 1e−8 b.

Retain signed raw values as well as pass flags. Do not clamp small negative multipliers or linear residuals to zero. Among all certified candidates choose smallest objective; objective ties within 1e−12 b² use the declared subset order. Save all candidates' mask/rank/status/objective/residual maxima and the selected full certificate. If no candidate passes, stop `QP_NO_CERTIFIED_SOLUTION`. Mathematical feasibility does not authorize manufacturing a numerical solution.

The independent scorer must reconstruct C and check the certificate/objective and analytic fixtures without importing the production solver. KKT checks are certificate verification, not a claim of an independently optimized second solution. Main adaptive replay repeats the actual solver from the same input; same-host determinism must be established before fitting.

Use CPU float64 SVD from the frozen NumPy/LAPACK implementation. Pin NumPy version, BLAS/LAPACK build, thread configuration and source implementation at execution. Current package metadata is not a runtime pin or a cross-platform equality guarantee. A different algorithm, rank threshold or tolerance requires an explicit reviewed revision before main stimuli.

## N4. Actual parameter displacement, not intended vector alone

Define RN32(x) as the pinned one-step conversion from the calculated float64 sum to float32. B1/B2 remain the inherited float32 update path, independently checked against their own arithmetic. Record Delta1/Delta2 = float64(theta'_32)−float64(theta0_32).

For P:

    thetaP32 = RN32(float64(theta0_32) + dP64)
    DeltaP = float64(thetaP32) − float64(theta0_32).

Do not cast dP to float32 before adding; that would introduce another rounding step. The independent checker verifies the exact resulting bytes for this defined operation before checking rows or scores. Signed-zero details must be pinned in the implementation. A wrong update must fail even if it happens to satisfy old-margin inequalities.

Calculate eP=DeltaP−dP from the verified arithmetic and report its norm. Proposed cast bound:

    ||eP||₂ ≤ 2e−6 max(1,||theta0||₂,||dP||₂).

The applied normalized row check is:

    C_i DeltaP ≥ −1e−9 max(1,||d2||₂) − sum_j |C_ij| |eP_j|.

This is an explicit allowance for independently verified rounding, not permission to excuse an arbitrary application error by inflating a tolerance from it. Log every negative actual residual even if within the envelope; do not state literal nondecrease. Also check the equivalent unnormalized row residual with its scale and actual/reference gradient predictions.

Finite-step behavior is measured separately:

    actual_old_margin_change − a_i·DeltaP.

A large or negative nonlinear residual is not an automatic solver defect. No nonlinear check feeds back into the applied P step.

## N5. S uses actual norm and actual B2 direction

Let nP=||DeltaP||₂ and n2=||Delta2||₂. Independently verify the B2 counterfactual arithmetic without reading its scores. If either is exactly zero, the proposed s64=0; retain zero cases. Otherwise:

    s64 = Delta2 * (nP/n2)
    thetaS32 = RN32(float64(theta0_32) + s64)
    DeltaS = float64(thetaS32) − float64(theta0_32).

No search for a better scale after rounding or after scoring. Record actual norms, signed mismatch, projection distance, DeltaP/Delta2 and DeltaS/Delta2 cosines when defined, and eS=DeltaS−s64. Verify the same cast bound as P. Norm mismatch must obey

    | ||DeltaS||₂ − nP | ≤ ||eS||₂ + 1e−10 max(1,nP).

Additionally, for a direction-identifiable nonzero P, require relative actual-norm mismatch ≤1e−4. This second limit is a proposed scientific-comparability tolerance, not a mathematical theorem. If it cannot be met, stop the main run as a comparison-admission failure; do not rerun S at a different scale or drop the case. If P=0 and S=0, record the non-identifiable direction and keep the case as a zero-step result. If B2=0 but a nonzero P emerges beyond numerical tolerances, stop; the theoretical target is zero.

Tiny nonzero directions may expose this limit. That is a question for the final numerical review and later fixture, not grounds to relax it using held-out outcomes. Even under the limit, the report must call the comparison numerically norm-matched, not exactly equal in real arithmetic. P–S isolates direction conditional on this projection-derived size and supplied information; it is not a contest between two independently selected step-size policies.

## N6. Fixed preflight solver/cast fixtures

Reserve16 algebraic solver cases per pass, embedded in 674 dimensions with at most8 rows. Pin their complete rational inputs and analytic answers before any fixture draw: empty/zero constraints; already feasible target; one violated halfspace; two-axis orthant; opposing normals; duplicate row; positive rescaling; mixed zero/nonzero rows; redundant dependent rows; zero projection; zero target; mildly near-parallel rows; below-rank-threshold parallel perturbation; narrow opposed cone; rotated low-dimensional orthant; row-order permutation of an earlier case. All16 sparse rational input/analytic-output tables are now specified in SOLVER_FIXTURE_LITERALS.json as mathematical proposals. Bind their byte hash and conversion implementation in the execution source lock. No random task geometry or model score may choose them.

These are solver fixtures, not task episodes. Analytic exactness is checked to the declared tolerance; representation invariance is not promised bitwise under arbitrary row permutation. Malformed/wrong-sign/KKT/renormalized/mismatched-norm copied certificates must be rejected. A correct zero projection must not be rejected as a missing solution.

Test float32 application on fixed normal/subnormal/small-step/opposite-sign inputs and exact-zero directions, with no model forwards. The mathematical example m(theta)=−theta² at theta=0 demonstrates that a zero first-order row can coexist with finite-step harm; it is an analytic classification fixture, not a demonstrated neural failure.

Eight margin-derivative checks (four fixed network geometries × both labels) are included in the neural ledger. Eight focal-gradient diagnostics (four geometries ×G/L) retain the inherited exact-versus-approximate distinction. The numerical old-gradient, solver and cast tolerances must not be conflated. Q010's historical softmax-underflow amendment is unrelated.

## N7. Last-review decisions

Codex should specifically assess the proposed SVD support/rank policy, tolerances, rounding envelope and norm-comparability stop. If a defect is found, return one deterministic replacement contract or one specific blocker, not a menu. No “solver converged” statement may substitute for full-row KKT and applied-byte verification. Do not insert output-driven backtracking or extra gradient searches as an undocumented implementation repair.
