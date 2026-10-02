# Post-capture verification amendment — final Float32 underflow

**Not a training, data, decoder, score-label or scientific-threshold change.** The original locked verifier and its rejection remain untouched. This is a newly identified post-main audit correction, so the original numerical contract did not pass unchanged. All candidates and all captured cases will be rechecked under the amended verifier; none are dropped.

## Observed failure
The original verifier passed exact CPU-Torch replay, then rejected an independent Float64-bound comparison in a no-maintenance durability case. The ideal probability was approximately4.3673753e-46; the saved probability was one least-positive Float32 subnormal,1.4012985e-45. Its ideal numerator was8.2264172e-46. Rounding the exponential and the later multiplication/division separately can produce a different least-subnormal result from a single final rounding of the exact real softmax. The original bound permitted subnormal exponent errors but modelled the final probability operation only with a relative error. That model is inadequate at underflow.

## Derived correction
For the declared local Float32 arithmetic, use the mixed bound |fl(x)-x| <= u|x| + eta, with u=2^-24 and eta=2^-126. This eta covers both round-to-nearest gradual underflow and full flush-to-zero of a subnormal magnitude; it is deliberately conservative and chosen from the format's smallest normal, not fitted to an observed maximum residual. It is the same kind of absolute underflow allowance already used for the weighted reduction in the frozen checker. For positive normal outputs its absolute term is negligible compared with the existing relative/reduction terms.

Let B be the existing propagated softmax probability bound (input subtraction, exponential, denominator summation, normal rounding). The amended final probability bound is B+eta. No relative multiplier or task threshold is enlarged. Subsequent error propagation uses that extra term. Exact serialized inputs, exact Torch weights/pre-normalization/read-code replay, source/case truth, class counts, exact decoders, checkpoint identities, 1e-3 non-informative-normalization rejection and every other test are unchanged.

This is a local CPU numerical-audit contract, not a portable proof of all Torch/libm implementations. The exponent's retained2u normal-output assumption remains a declared backend assumption. The raw rejected row, prior failure trace, and two source diffs accompany this amendment.

## Required checks before reuse
Reproduce the old rejection and exact captured arithmetic; pass the same unchanged row under the derived bound; test synthetic near-underflow logits across scalar/batched layouts and diverse scales; deliberately corrupt captured weights, weighted values, and normalized outputs and require rejection. Retain original failures and pin the amendment's source separately before executing complete rescoring.
