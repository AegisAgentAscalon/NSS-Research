# Reconciliation and substantive review

## Evidence tiers

[S1] Codex `NSS_NBR02_Theoretical_Candidates_v0.1.zip` contains a DC01 v0.2 candidate and review sheet, not results. Its nine manifest members and ZIP CRC were checked here. Its source receipt names the accepted NBR-01 decision and earlier research-log package, not Chat's subsequently written DC01 exact-diagonal proposal or failure-first addendum. Consequently this review reconciles independently developed plans; it is not evidence that Codex rejected those later documents.

[S2] Chat `NSS_NBR02_DC01_Proposal_v0.1.zip` proposes an 8-unit diagonal recurrent cell and an exact local derivative formula. Its design choices, hyperparameters and budget were not numerically validated. [S3] Failure-first instrumentation adds a proposed observability contract. [S4] The adopted NBR-01 closeout, prior research log and question register establish program status and return-ticket context. Source identities are retained; their old numerical results were not independently rerun here.

## Reconciliation decisions

| Topic | Codex source | Earlier Chat source | Proposed v0.3 disposition |
|---|---|---|---|
| Scientific comparison | Dense 16-unit recurrence; local trace drops cross-unit derivative paths | Diagonal 8-unit recurrence; exact local derivative in real arithmetic | Use Codex's main comparison; retain diagonal exactness only as a check. These are different experiments. |
| Gradient verification | Exact diagonal check and nonzero cross-path witness | Exact G/L equivalence throughout | Compare G with exact math; compare L with its own approximate math; quantify intentional dense disagreement separately. |
| Immediate competence | Both G and L, at least 3/4 fits | G, all four fits | Use both-arm group admission, preserve all four fits after a pass. Add explicit initial-old-association competence. |
| Mapping split | Initial/development must not teach held-out mappings | All eight associations initially familiar | Separate eight initial cues, four development cues and eight held-out focal cues; old/protected cues intentionally recur. |
| Primary observation | Five post-receipt/reset, pre-next-update read-only probes | Five pre-receipt predictions | Freeze post-receipt probes as primary; preserve every before-feedback prediction as a separate raw diagnostic. |
| Receipt shuffle | A six-update valid future-free permutation; underspecified with one pending receipt | Reject wrong/consumed receipts | Reorder complete transactions and inject mismatched receipt IDs for rejection. Never pretend multiple simultaneous valid receipts exist. |
| Replay budget | 8,808 scheduled / 9,800 ceiling | 8,636 / 9,000 | Use 9,800 ceiling; add 24 clean-fixture and 16 sandbox fault updates: 8,848 planned. |
| Failure evidence | Full accounting and stop rules | Explicit flight recorder and fault catalogue | Integrate intent/commit, same-prestate references, independent audit, detector tests, and gaps/unknown causes. |
| Roadmap | NBR-02 preparation; workspace parked | Same | Add user-requested return to 01–03 after NBR-03, before NBR-04. |

## Mathematical disposition

The proposed L recurrence is a coherent diagonal-Jacobian sensitivity approximation for the stated dense tanh cell. Its output layer uses the usual exact error derivative. It drops propagated cross-neuron sensitivities, not all recurrence or all gradients. It is not exact BPTT for dense U, and no RFLO/e-prop implementation or biological locality is established.

At a diagonal U, the one-step raw-gradient comparison is exact in real arithmetic even when the full matrix is represented: parameter perturbations initially affect one postsynaptic neuron and only its self-recurrence carries that derivative onward. This does NOT imply that subsequent unconstrained SGD steps preserve diagonality. Reset the fixed diagonal case for each numerical check rather than claiming trajectory equality after off-diagonal parameters are updated.

The fixed zero-activation analytic witness in `EQUATIONS_AND_WITNESS.md` has nonzero cross-path derivatives and an encoder-gradient discrepancy sqrt(12/47), about 0.505. Zero activations do not mean zero weight derivatives. The witness's U-gradient itself is zero; it tests omitted cross-unit propagation into W and b. A separate nonzero-activation derivative fixture and same-state per-update auditing cover U. Do not relabel the witness as a nonzero U-gradient test.

## What is not settled by the design

Three upstream transitions are deliberately short. L's 640-float derivative trace may be larger than G's saved upstream activations. A smaller trace than a hypothetical full forward Jacobian is not evidence of lower total cost than the actual three-step reverse-mode baseline.

Delay invariance is expected within each method: filler state is detached; frozen pending information determines the update; the next transaction starts from zero live state. It is a retention check, not an inherent accuracy advantage for eligibility traces. G/L can diverge legitimately because L is approximate; each must nevertheless be invariant to its own delay variants.

New labels are disjoint by cue identity and receipt history; this does not establish broad out-of-distribution cognition. All cue coordinates are supplied public identities. Six online updates give a deliberately small adaptation screen, not a thorough optimizer comparison.

A competent approximate arm can differ numerically from G. Conversely a precisely implemented approximate rule can fail to learn. The former is not automatically a bug; the latter cannot be described as a delay failure when it already fails at delay zero.

## Remaining gates

Concrete code, all source hashes, independent implementation, executable byte bound, global seed/input audit, derivative fixtures, cost probes and runtime competence have not been produced. The proposed task/hyperparameters/margins require acceptance with a later execution request. That request can authorize implementation and the staged checks under this version; a semantic change discovered during implementation requires a new version before fitting. A failed cost or competence check does not authorize silent extra training.
