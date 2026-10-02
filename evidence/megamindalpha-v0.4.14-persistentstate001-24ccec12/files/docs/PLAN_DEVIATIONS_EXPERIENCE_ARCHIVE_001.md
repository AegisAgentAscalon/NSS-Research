# ExperienceArchive001 — decisions, deviations and self-audit repairs

1. **Exact baseline preserved:** verified supplied 0.4.2 ZIP checksum and reproduced
   all 128 tests, prior demos, atlas, imports, compile and file manifest. The old
   runtime implementations/tests remain byte-identical. No absent 0.6 source was
   inferred from notes. Version continues the reviewed-baseline branch at 0.4.3.
2. **Separate domain, not duplicate active state:** a new archive.sqlite3 owns only
   experience/history/evidence. RecoveryStore remains the single active-checkpoint
   owner. Intake is explicit and read-only against its public API.
3. **Scope held:** no DatasetSnapshot builder, automatic semantic curation, trained
   evaluator, private data import, training, external data feed, real tools,
   generic Runtime changes or new generation/release authority.
4. **Record event lineage:** source evidence is content-addressed once; normalized
   event payloads store references, not repeated raw source text. Revisions are
   verified by replaying the pure reducer, not by trusting stored status fields.
5. **Human attestation only:** role metadata can reject explicitly MODEL-labelled
   approvals, but no authentication was invented. A malicious caller can lie
   about its role; a trusted host/Nexus boundary is required before production.
6. **Source revocation is deliberately conservative:** exact byte hash + purpose
   blocks all linked records. No restoration, secure deletion, export recall or
   automatic unlearning is promised. WITHDRAW is an inspection-only tombstone.
7. **Unknown authors stay unknown:** TaskRecord role labels cannot identify an
   actual speaker. Intake stores UNKNOWN attribution instead of inventing a user
   or author. Only the runtime capture operation itself gets a known SYSTEM author.
8. **API audit repair:** validate use-purpose syntax before set lookup to prevent
   malformed list/dict purposes from leaking TypeError instead of typed outcomes.
   Added malformed-input regression coverage and explicit corrupted-open failures.
9. **Provenance audit repair:** validate an imported TASK_STAGE snapshot's own task,
   stage, sealing, source list and canonical record hash before accepting its
   claimed execution context. This is structural binding, NOT authentication of
   a claimed ECID or independent verification of source truth.
10. **Duplicate source audit repair:** reject duplicate source IDs within an edit
    request even when the metadata is identical. Same ID cannot acquire new bytes.
11. **Long-ID audit repair:** represent unresolved original authors with a bounded
    digest-based label rather than prefixing a maximum-length source ID beyond
    the schema's ID budget.
12. **Bounded lookup refinement:** use indexed source/purpose revocation lookup for
    current record consumption; full archive scanning is reserved for explicit
    audit. No cross-call validation cache or unchecked authority cache added.
13. **Testing hygiene:** closed SQLite handles in new corruption tests after the
    first run surfaced Python ResourceWarnings. Existing test files were untouched.
14. **Documentation:** only affected `experience` JSON/Mermaid/DOT/PNG view is
    reconciled, preserving 25 schema-v2 flows. Old Word/reference artifacts remain
    historical, not falsely regenerated. No new DOCX/accessibility claims.
15. **Evidence limits:** tests precede primary implementation; later API/provenance
    findings received dedicated regressions. The release audit is local self-review,
    not an independent Astra audit or a neural viability/production-security proof.
