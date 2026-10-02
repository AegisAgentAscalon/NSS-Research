# R3 corrections to the R2 revision pack

These amendments take precedence within this prototype; the supplied R2 documents remain unmodified historical references.

1. **Replay and side effects (Master section 7).** Replay reconstructs computation from portable input references. Never blindly restore hidden state produced under an incompatible ECID. Preserve committed-action IDs; uncertain outcomes require reconciliation. A durable executor must eventually define intent records, idempotency keys, receipts, and crash recovery. Already presented output cannot be undone by restoring a model checkpoint.
2. **Qualified directed transitions (Master sections 6–7).** A qualified destination is insufficient. Each allowed source-to-target edge declares reuse or replay, evidence, and failure behavior. The base implementation rejects migration and reuse across changed active weights. No implicit reverse edge or arbitrary overlay subtraction.
3. **Mandatory Core-only operation (Master section 3).** Replace “if defined by the generation” with “Every released Core generation includes a qualified Core-only profile.” This promises baseline operation, not completion of every task after capability loss.
4. **Generation output validation.** Both AR and DARP outputs pass the same applicable intent/constraint validation boundary. Engine fallback does not waive constraints or change modality without policy/user allowance.
5. **Diagram authority.** Training candidates always pass independent qualification and Nexus authorization before deployment. Explicitly label compatible-state continuation. Repulsors derive from user intent or applicable policy, not invented preferences.
6. **Evidence scope.** Audit PASS means a specified issue was addressed in documents. Runtime tests, neural cooperation, identity continuity, and production qualification require separate evidence.

The main architecture stays fixed. HSA/MSA, recurrent depth, DARP, neural training, and full external action execution remain deferred.
