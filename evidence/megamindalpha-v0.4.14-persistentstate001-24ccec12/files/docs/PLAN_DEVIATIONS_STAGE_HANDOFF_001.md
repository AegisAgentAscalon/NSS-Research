# StageHandoff001 — decisions and deviations

1. **Actual source baseline:** used the full 0.4.1 reviewed working files and
   reproduced 81 tests. The later MegaMind directory has only AGENTS/README/
   NEXT_STEPS; no attempt was made to reconstruct a reported 0.6.0 implementation
   from its claims. This is explicitly a reviewed-baseline branch.
2. **Next-slice authority:** the old source recommended qualification evidence;
   the newer lifecycle handoff and current user authorization select portable
   task state first. Qualification/Nexus are still fixtures, and the remaining
   authority gap is stated rather than filled with simulated credentials.
3. **Single storage owner:** embed TaskRecord in checkpoint v2 and exact handoff
   in attempt v2. A separate archive or parallel current pointer was rejected.
   Legacy v1 fields and default behavior remain intact and retain all tests.
4. **No neural claims:** TaskRecords are annotations for an integer simulator.
   Their meaning, correctness and receipt classes remain upstream fixture inputs.
5. **Bounded source completion:** explicit source-field JSON only. No general
   knowledge store, natural-language extraction or learned curation in this pass.
6. **Artifact scope:** historical Word files and original R2 ZIP are unchanged.
   Current API/spec updates are Markdown, schemas and the original 25-flow atlas.
7. **Review process:** implementation packet and acceptance tests preceded new
   code. The human/machine atlas reconciliation was completed before the final
   acceptance run. A blank pseudocode line was rejected by the existing validator
   during regeneration and removed; validation was not weakened.
8. **Audit repair:** historical PUBLISHED reads now recheck exact target and
   TaskRecord bindings, not merely the pointed-to checkpoint's self-hash. A
   regression injects an internally well-formed but substituted historic target.
9. **Initialization/finish:** upstream computation is represented by supplied
   results and explicit sealing. No automatic task solver or completion judge was
   introduced. Later integration must not interpret sealing as semantic success.
