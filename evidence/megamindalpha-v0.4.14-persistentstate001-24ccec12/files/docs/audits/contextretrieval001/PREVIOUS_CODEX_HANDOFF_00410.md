# MegaMind Alpha v0.4.10 — current implementation handoff

Continue the working repository, not a rewrite from graphics. Current build is
OverlayCatalogController001; the next bounded subsystem is ContextRetrieval001.
Read README/NEXT_STEPS and the current audit/implementation packet first.

The older stack remains supported: deterministic recovery, StageHandoff001,
ExperienceArchive001, DatasetSnapshot001, EvaluationRun001, NeuralProbe001,
QualificationEvidence002, LocalNexusPermissions002 and OverlayGenerationManager001.
The new controller selects exact reviewed fixture profiles and persists task heads
in the existing generation owner. No duplicated current-state database was added.

Reuse public controller and TaskRecord helpers. New QAP selection is not release or
execution authorization. Costs are declarations; serialized document size is not
VRAM. Real Core/A/B tensors exist, but they are a 512-parameter linear probe plus
128-parameter overlays, not a competent general model. Native ternary kernels,
learned routing/evaluation, context architecture, production identity/security,
Aegis Runtime integration and optional research tracks remain separate work.

Before changing anything, reproduce the release checks. New implementation must
preserve failure reasons, exact source/epoch identity, finished-stage boundaries,
side-effect receipts and qualified transitions. Close/reopen must not bypass an edge.
Changes to authority or evidence semantics require explicit review; no numeric
relaxation to conceal legacy reproducibility issues. Archive-history inspection is
not a fresh permission to use data or run computation.

Refactor shared mechanics and remove proven dead paths; keep distinct regressions.
Deliver exact code/tests, actual verification logs, limitations, a versioned archive,
checksum and fresh-extraction verification. Do not ship caches, live databases,
private conversations, secrets, downloaded corpora or unreviewed model artifacts.
Historical handoff text is retained in the current audit directory as history only,
not a pile of competing "current checkpoint" instructions.
