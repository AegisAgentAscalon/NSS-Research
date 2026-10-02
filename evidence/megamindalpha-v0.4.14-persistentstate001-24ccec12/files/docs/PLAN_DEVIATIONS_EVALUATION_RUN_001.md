# EvaluationRun001 — deliberate limits and audit decisions

1. Followed NEXT_STEPS on the complete reviewed-baseline 0.4.4 source, not the
   incomplete 0.6 notes. Implemented one bounded owner, not qualification authority.
2. Concrete integer checking reuses the candidate fixture schema and existing
   Catalog invariants. It binds a selected profile/ECID but does not run external
   actions, transition a live worker or certify fixture qualification references.
3. Added pure catalog validation mirroring the public Bundle ordering/transition
   constraints; inherited artifacts.py remains unchanged. Tests cover ECID agreement,
   ordered dependency failures, and invalid candidate catalogs. Consolidation of
   this helper into the existing owner requires a separately tested refactor.
4. The development snapshot is consumed only for exact currently permitted lineage
   observation; arithmetic tests use a separate self-authored fixture suite. No
   repurposing training material as protected release tests. No snapshot text copy
   is embedded into the result store.
5. An interrupted run retains PREPARED rather than intermediate mutable scores.
   Replaying bounded pure arithmetic is simpler and safer here than inventing
   partial-result migration. No side effect executor exists in this boundary.
6. Any completed report says authority NONE. Threshold failure/budget exhaustion
   is data in a finalized report, not permission to deploy or alter policy.
7. Returning historical receipts does not require current data permission and does
   not grant it; verify_current requires an exact expected report digest and gates
   all current input dependencies separately.
8. Installed source identity is pinned per process and per plan; restart is required
   after code/environment changes. This is not executable binary attestation.
9. Prototype reports retain raw SYNTHETIC fixture material for audit/recomputation.
   They are not a privacy-preserving storage service for private real benchmarks.
10. Initial new tamper tests used SQLite context managers without explicit connection
    closure. ResourceWarning diagnostics caught this; new fixture connections now
    close explicitly. The inherited StageHandoff test warning remains unchanged and
    disclosed. No production connection leak was inferred.
11. Official DOCX/reference files remain historical and unchanged. Only the affected
    parent qualification note, three helper graphs, Markdown, schemas and code were
    updated. Graph generation is programmatic; no semantic guarantees are inferred
    from diagram reachability or test count.
