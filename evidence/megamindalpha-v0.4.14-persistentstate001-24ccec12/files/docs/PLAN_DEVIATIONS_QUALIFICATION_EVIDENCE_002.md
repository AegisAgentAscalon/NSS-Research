# Deliberate scope and audit decisions

1. NEXT_STEPS proposed QualificationEvidence002; implemented only the NeuralProbe001
   evidence adapter. No arbitrary statistical/neural/domain qualification backend.
2. Kept source public APIs and all inherited neural training/evaluation code intact.
   Existing integer authorization flags remain simulations; they do not consume
   certificates until a separately scoped permission/runtime integration pass.
3. Event sourcing replaces the need for separate mutable revocation/status indexes.
   Journal size is intentionally bounded, and fail-closed capacity errors explicit.
4. Roles are local operator attestations. Scripted demonstrations do not masquerade
   as independent human approval or a learned Core evaluator.
5. Inherited historical reference verifier FAILED baseline on tiny MSE differences.
   Original checkpoint/report/checker preserved. Added a separately named POST-HOC
   portability diagnostic; accuracy/count equality remains exact. Strict reference
   gate stays in logs as a non-blocking HISTORICAL advisory, never hidden as PASS.
   Fresh same-environment exact evidence drives new claims. Underlying cause unproven.
6. Initial new tests copied a snapshot fixture to a different absolute path. The
   inherited archive-binding guard correctly rejected it. Fixed test setup to restore
   at the original bound path; did not weaken production archive identity validation.
7. New local schema/JSON corruption paths hardened before release. Manual reject and
   inconclusive decisions remain history even without live source access; acceptance
   requires live checks. Numeric/code/data changes never silently renew approval.
