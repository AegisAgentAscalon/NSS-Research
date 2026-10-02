# Candidate rationale and selection — fixed before main results

This new study addresses the untested gap in pass 58: retaining an almost-perfect model is not evidence that small master values can accumulate useful updates. It is not another repeat of the same near-saturated continuation. Source claims are attributed in the reconciliation report. No paper's performance is inherited.

| Candidate | Proposed benefit | Likely failure | Selected? |
|---|---|---|---|
| C1: Q2 forward / FP16 matrix masters, nearest-even writes / M8 optimizer | Remove half the matrix-master bytes while training through the same Q2 forward rule. No extra residual array. | Small updates vanish; apparent stability can conceal failure to acquire corrected associations. | Yes; matched FP32-master/M8 control. |
| C2: Same, adjacent-value stochastic writes | Permit sub-FP16-step adjustments to contribute statistically without a stored FP32 residual. | Added rounding variance, unstable recurrence, slower writes; unbiased scalar rounding does not imply unbiased nonlinear learning. | Yes; same starting cast, data and loss as C1; explicit RNG state. |
| C3: Compress saved activations for backward, first conservatively to 8 bits | Address the larger activation storage observed in pass 58. Forward values could stay FP32; stored backward inputs compressed. | Approximate gradients, retained originals defeating savings, recurrent error amplification, decode overhead. | Deferred. Distinct mechanism; do not confound the present master-learning question. |

## Exact precision map for selected modes

| Quantity | M32 reference | C1 M16_NEAREST | C2 M16_STOCHASTIC |
|---|---|---|---|
| Matrix forward values | Four-value Q2 affine quantizer | Same | Same |
| Training representation of forward values | Transient FP32 dense effective matrices | Same | Same |
| Persistent trainable matrix masters | FP32 | FP16, initial nearest cast | FP16, identical initial nearest cast |
| Trainable biases | FP32 | FP32 | FP32 |
| Activations / recurrent state during training | FP32 | FP32 | FP32 |
| Leaf gradients | FP32 | FP32 | FP32 |
| Persistent optimizer first moment | signed 8-bit linear codes + FP32 block scale | Same | Same |
| Persistent optimizer second moment | unsigned 8-bit square-root codes + FP32 block scale | Same | Same |
| Update arithmetic | FP64 local arithmetic, FP32 proposed value | Same, then nearest-even FP16 | Same, then stochastic FP16 |
| Numerical reference evaluation | FP64 | FP64 | FP64 |
| Inference export | 2-bit packed matrix codes; FP32 scales/biases, uint8 zero points | Same | Same |

There is no persistent full FP32 master shadow or residual in C1/C2. There ARE transient full FP32 effective tensors and gradients. This is mixed-precision quantization-aware learning, not native two-bit forward/backward arithmetic. The identity straight-through gradient is an approximation to training the discrete forward rule. Master casts do not change the parameter count.

## Selection rules

Select C1 and C2 because they reuse an implemented, auditable numerical kernel and test the explicit open learnability question. Do not select models, modes, rates or endpoints from main performance. All four retained parent identities participate. C3, ternary retraining and lossless codec acceleration stay outside this pass. The full-precision optimizer and ternary-versus-Q2 comparisons already have their own evidence; repeating them would not isolate the present question.

## External primary context (abstract-level review only)

Gupta et al., *Deep Learning with Limited Numerical Precision*, ICML 2015, https://proceedings.mlr.press/v37/gupta15.html. Demonstrates the relevance of stochastic rounding in 16-bit fixed-point training. Our FP16-master/Q2-GRU candidate is not their reproduction.

Dettmers et al., *8-bit Optimizers via Block-wise Quantization*, ICLR 2022, https://arxiv.org/abs/2110.02861v2. Optimizer compression precedent. Our inherited signed-linear/square-root code is custom, not bitsandbytes' nonlinear quantizer.

Chen et al., *ActNN: Reducing Training Memory Footprint via 2-Bit Activation Compressed Training*, ICML 2021, https://proceedings.mlr.press/v139/chen21z.html. Saved-activation compression precedent on vision workloads; relevant to deferred C3, not a result about NSS recurrent learning.
