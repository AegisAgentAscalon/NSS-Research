# NeuralProbe001 — scope decisions and audit corrections

1. Chose a deliberately small two-layer LINEAR symbol transducer, not a Transformer.
   This isolates actual frozen-weight/adapter/gradient/state mechanics within CPU
   limits. It has a favorable prescribed factorization; success is not language,
   nonlinear reasoning, independently discovered topology, or scalable NSS proof.
2. Ternary target retained as a numerical clamp/round Core reference plus fp32
   diagnostic control. FP32 overlays and master storage are explicit. No native
   BitNet, packed kernels or energy/memory efficiency claim. All-ternary overlays
   and real backend performance are separate remaining experiments.
3. Numerical evidence gets its own versioned small journal/checker. The existing
   pure integer EvaluationRun001 cannot be reinterpreted to evaluate neural outputs.
   No inheritance/runtime/test assertions were weakened or redefined.
4. The archive/snapshot data are actual consumed symbol-pair training input, not
   decorative lineage. REVIEW/HUMAN is a scripted local development attestation,
   not a trusted reviewer. Test pairs are separate, self-authored and developer-visible.
5. Existing Catalog and Ledger are reused. Neural activation recovery is ephemeral
   because the current durable RecoveryStore schema describes the earlier backend.
   Do not claim native neural publication or an Aegis Runtime backend was added.
6. Single joint-adapter baseline matches trainable parameter count, summed updates
   and training input-token presentations, but receives composed labels directly.
   No claim of identical supervision/FLOPs or modular superiority is made.
7. Restart after interruption repeats pure training from seed. No optimizer-state
   resumption or mid-step migration. Committed mock action is replay-safe, not twice.
8. Current documentation counts six proposed remaining Alpha software AREAS plus
   final integration; not six remaining research problems or six promised releases.

Audit corrections during implementation:
- Fixed mock ActionRequest payload to the existing typed object contract (initial
  integration incorrectly supplied text). No action schema was changed.
- Added independent task-input binding so substituting inputs AND recomputing their
  digest/cache cannot make them a valid continuation of the original task.
- Reject checkpoint role/dtype/shape substitution and non-roundtrippable fp32 JSON.
- Strengthened nested result, budget and environment validation; report checks do
  not treat structural success as an independent scientific judgment.
- Explicitly closed SQLite connections in new corruption tests.
- An intermediate test run correctly failed when implementation files were edited
  during its pinned run. Source was then frozen and the entire498-test suite rerun
  successfully. That interrupted/intermediate run is not release evidence.

Preserved source ancestor:
MegaMindAlpha_v0.4.5_EvaluationRun001.zip
SHA256 be2778e6daf79d166df82ca10b847460d25cfbdddc5b083fc6ffd58b91441b6e
