# NeuralProbe001 — measured confirmation results

Six planned trials: seeds101,211,307 × fp32/ternary_core_reference. CPU, no downloads.
Protocol fixed before these trials; developer-visible data and feasibility pilots
mean this is not an independently preregistered or protected benchmark.

| Mode | Seed | Core-only baseline | A+B combined task | A removed | B removed | Both removed | Joint control | Gen2 | Retained domain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fp32 | 101 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| fp32 | 211 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| fp32 | 307 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 101 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 211 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |
| ternary_core_reference | 307 | 100% | 100% | 56.25% | 57.81% | 48.44% | 100% | 100% | 100% |

Each accuracy is exact BOTH-SYMBOL correctness, not token accuracy. Test64pairs;
retained Gen2 domain49pairs. Every individual symbol is seen in training. Core-only
baseline measures identity, while all three ablations target the combined transform.

Core512 parameters; A128 and B128; joint256. Joint sees composed targets; modular
A/B see separate targets. Equal trainable parameters, summed optimizer updates and
input-token presentations are NOT identical supervision/FLOPs. Joint100% means
there is **no demonstrated modular accuracy advantage**. This simple prescribed
linear factorization only validates basic training/composition/recovery wiring.

All six accepted Core tensors remained unchanged after freeze. Previous A/B remained
exact through A2 training; B was reused. All six recovery checks rejected stale AB
activations, rebuilt A with0.0 max absolute error against a fresh instance, returned
to Core-only, rejected the unapproved reverse transition, and retained one mock effect.

Recorded optimizer updates: 11940; elapsed coordinator
time in this local confirmation: 44.571s (includes data gates and checks;
not a speed benchmark, excludes setup and no energy measurement).

Ternary mode is a fixed-scale simulated ternary CORE with fp32 overlays/master
weights/arithmetic, NOT packed native1.58bit inference or a BitNet replication.
The Core is an identity transducer, not a trained assistant or evaluator.

Raw exact protocol, plan/code/environment, checkpoint tensors, reports and summaries
are next to this file. The final archive is re-tested separately from a fresh
extraction; those logs are external to avoid a self-referential package hash.
