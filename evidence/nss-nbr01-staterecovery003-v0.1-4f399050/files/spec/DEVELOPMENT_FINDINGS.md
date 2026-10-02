# Development record (before main training)

Three completed600-step fits on the prior development representation141 and new
learning seed441 were retained. There was no main-seed maintenance training or
protected scoring at this point. Development fault inputs used a separate seed.

The development evaluator exposed tiny nonzero outputs at the mathematically
reserved zero: subtracting an independently evaluated one-row network baseline
from a larger-batch network output did not enforce bit-identical zero due to
floating-point reduction ordering. Repeated maintenance amplified this in the
unfixed implementation. This is an implementation/reset-contract failure, NOT
biological evidence. The initial source and all failed results are preserved.

Before main registration, add an EXACT-zero input guard to Repair.forward. This
only enforces F(0)=0. It does not suppress small nonzero inputs, repair a damaged
empty state, or label a class UNKNOWN. No norm-based cutoff is added.

The development single-shock results also justified keeping strong controls:
nearest supplied prototype decoding was substantially better than the original
readout under strong Gaussian damage, and equal-byte replica averaging competed
with the fast/slow candidate. Main training retains the planned1,800 steps, the
same data generator, same losses and same architectures; no favorable arm or
seed is selected. Main retention/recovery criteria will be written before its
training or evaluation. Development results are not counted as main evidence.
