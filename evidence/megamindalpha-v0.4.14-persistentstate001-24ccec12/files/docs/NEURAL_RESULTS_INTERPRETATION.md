# What the first neural result actually demonstrates

Checked directly in nss_base/neural_backend.py, train_trial / train_overlay.

1. Core w1,w2 (16x16 each,512 values) learns identity, including intermediate
   identity losses, before it is frozen.
2. A is initialized as a zero-output rank4 overlay. The optimizer sees only A.
   Training evaluates core(x,a=A), with no B. Target swaps0/1 and2/3.
3. A is frozen and serialized. B is initialized separately. Its optimizer sees only
   B. Training evaluates core(x,b=B), with no A. Target swaps1/2 and3/4.
4. Frozen A and B are activated together at prescribed successive slots. There is
   NO AB joint fine-tuning. For input0, A sends0->1 and B sends1->2; AB target is2.
5. B encounters A's output at combined inference, but its task and input symbols
   were already known during training. Shared near-identity interfaces make this
   deliberately favorable; it does not prove random modules will align themselves.
6. A2 is trained separately against Core-only as a fresh candidate, NOT trained with
   B present. It adds swap5/6, then reuses unchanged B. This is a limited retention test.

Training split contains128 pairs; validation64; test64. All16 individual symbols
appear in training. This is pair recombination, not unseen tokens/skills or language.
The predictions are token-wise; pair score requires BOTH tokens correct.

The48.44% Core-only number is against the COMBINED transformation, not the Core's
own identity task. Core-only scores100% on its intended baseline. A/B ablations
reduce combined score to57.81%/56.25%, while AB and joint control both score100%.
The joint control matches256 trainable parameters and total updates/input tokens,
but receives composed targets directly. Neither a performance/energy advantage nor
general independently trainable overlay compatibility is established.

Meaningful positive evidence: actual gradients learned modular transformations;
old weights stayed fixed; contributions composed in the intended order on held-out
pairs; cache invalidation/rebuild behaved as specified for the small neural state.

Important audit update (this pass): all archived accuracy/count groups reproduce
exactly, but strict MSE reproduction has tiny discrepancies (observed max~3.73e-9).
The exact source of lower-level numerical drift is not established. Archived scores
and strict checker are retained unchanged. A separate post-hoc tolerance diagnostic
is labeled historical-only and is not eligibility evidence. Fresh bound experiments
are used for this pass's live qualification checks.
