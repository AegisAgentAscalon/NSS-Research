# DatasetSnapshot001 — plan decisions and audit repairs

1. Input ZIP v0.4.3 matched its published SHA-256, manifest and 210-test baseline.
   No missing-source 0.6 code was inferred. One new bounded subsystem is integrated.
2. A necessary narrow archive extension supplies current-use batches under one
   transaction, including exact review/purpose observations. A series of separate
   single-record reads cannot by itself promise a consistent multi-record snapshot.
   Snapshot code does not use peer private SQL, inspection or history to grant use.
3. Four new modules: dataset contracts/projection, single-owner snapshot storage,
   operator CLI and synthetic demo. No scheduler, learned curator or trainer added.
4. Two fixed non-executable text projections; tokenizer identity is verified against
   actual local bytes but tokenization is not implemented. No invented instruction-
   tuning pairs or summaries that hide the original uncertainty/provenance.
5. Immutable manifests and operation receipts publish atomically in the snapshot
   database. Archive checks are separate point-in-time observations, not a distributed
   lease. A regression explicitly revokes after observation but before publication;
   subsequent consumption must reject that historical snapshot.
6. Exact-current policy deliberately rejects any changed selected head. Every read
   checks all members, including the other split; no silent filtering/rebuild.
7. Local archive location binding was selected instead of introducing an unreviewed
   authenticated portable store identity/migration system. Same-path hostile rollback
   remains outside the prototype guarantee. This limitation is explicit in the API.
8. Train/development-validation splits only. Independent release/held-out evaluation
   access and exposure tracking remain a separate boundary, not silently simulated.
9. Source/family split rules use all declared source refs (including included
   ancestors). Exact duplicate projected examples are rejected, not dropped. No
   semantic deduplication, family discovery or cross-snapshot exposure claim.
10. Self-audit found two genuine inherited revocation-index weaknesses: deleting a
    revocation-index row, or repointing it to another digest, could make a recorded
    withdrawal invisible to a selected-source lookup. New regression tests failed
    before the fix (retained output). The archive owner now verifies event/index
    correspondence and all local revocation bindings before filtering. Batch use
    checks this once per transaction. Existing single-record consumption also gains
    the repair. This knowingly trades a full local revocation-ledger scan for correct
    fail-closed behavior; future scaling work must preserve the regression cases.
11. Initial new corruption tests surfaced ResourceWarnings because SQLite context
    managers do not close connections. New test helpers now explicitly close them;
    no inherited tests were edited to lower expectations.
12. Additional tests cover transaction abort preserving an earlier dataset, copied
    result immutability, malformed CLI/API data, exact retry semantics, incomplete
    batch results and tokenizer-byte limits. Six new process-death scenarios cover
    four publication fault points and two revocation/retry cases.
13. Parent Atlas remains 25 flows; only builder and experience entries changed.
    Two subordinate JSON graphs elaborate snapshot build/read and use the existing
    graph validator. The full Builder/training policy still is not implemented.
14. Word/reference artifacts and the reviewed compression guide remain unchanged.
    Only affected Markdown/schema/spec/diagram views are regenerated. No official
    DOCX, neural, energy, production security or independent-audit claim is made.
15. A remaining ResourceWarning was present in the baseline as well as this full
    run. Tracemalloc localized it to unchanged tests/test_stagehandoff001.py:201;
    all 47 targeted tests pass. It is documented as inherited test-fixture cleanup,
    not suppressed or described as zero warnings.
