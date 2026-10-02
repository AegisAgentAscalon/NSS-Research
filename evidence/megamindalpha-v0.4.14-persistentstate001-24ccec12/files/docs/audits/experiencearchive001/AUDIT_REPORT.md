# ExperienceArchive001 — implementation self-audit

**Checkpoint:** 0.4.3-megamind-alpha-experiencearchive001 (reviewed-baseline branch)
**Verdict:** PASS for the specific local software checks listed below. No claim of
neural learning, semantic correctness, authenticated human review, production
security, arbitrary external exactly-once, or completion of every NSS subsystem.

## Baseline and scope
Input: MegaMindAlpha_v0.4.2_StageHandoff001.zip
SHA-256: ddbf7cf98d4826846852a12d0b266128de47fcbcd41909b59b463c1cf4a1b995

Reproduced the 128-test baseline, 001A/001B/StageHandoff demonstrations, 25-flow
atlas, static dependency checks, compilation and 164-file release manifest before
editing. All **23 inherited Python source/test files** remain byte-identical to
that archive. Historical Word/reference files and unrelated diagrams also remain
unchanged. Only the `experience` entry changed in the 25-flow schema-v2 atlas.

The implementation packet and first 48 acceptance methods were written before
new runtime behavior. The initial expected missing-module test failure is retained.
Integration/crash tests preceded their new integration implementation; subsequent
self-audit findings received additional targeted regressions.

## Implemented boundary
Five new modules: pure archive contracts/reducer; one SQLite archive owner;
read-only stage-intake adapter; local review CLI; synthetic integrated demo.
Thirteen reproducibly generated JSON Schemas describe requests and revision data.
No active-runtime state owner was duplicated or modified. Archive failure does
not change the current checkpoint or execute/redeliver an external effect.

## Retained validation results
| Check | Result |
|---|---|
| Full unit suite | **210 passed**: 128 inherited + 82 new methods |
| Archive process-crash scenarios | **13 windows**, grouped in 3 test methods |
| Recovery 001A | PASS |
| Recovery 001B | PASS |
| StageHandoff001 | PASS; core -> AB -> A -> core; clean-A equality; effect count 1 |
| ExperienceArchive001 | PASS; correction retained, retrieval separately allowed, training blocked, revocation enforced |
| Logic Atlas | All **25** structurally valid; experience reconciled |
| Static imports | PASS; no unreviewed imports or dependency cycles |
| Compilation | PASS |
| Schema regeneration | Byte-identical for all 13 new schemas |
| Unaffected source/reference comparison | PASS |
| New experience graph | Generated from reviewed JSON/DOT; visually inspected |

Full command output is retained, not replaced by a pass count. `verification.json`
records interpreter/platform/SQLite and exact source identity. The fixture-based
suite ran on Python 3.13.5 / SQLite 3.46.1 in this environment. Python 3.10+ remains
the intended API floor, not a claim of a tested multi-platform interpreter matrix.

The final release ZIP is separately extracted and rechecked; that byte-specific
result is delivered alongside the ZIP to avoid a self-referential manifest.

## What the new tests establish
- Captures begin pending, with UNKNOWN separate purpose decisions.
- Original source bytes and original interpretations survive later corrections.
- New evidence can be appended without rewriting prior capture records.
- Human-labelled review is required for consequential edits; model-labelled
  confidence cannot directly approve/grant/resolve/correct/withdraw/revoke.
- Disputes quarantine a record; resolution does not silently approve it.
- Review, retrieval permission, training permission and redistribution differ.
- Changed statements invalidate earlier ALLOWED decisions; revocation remains.
- Source-purpose revocation blocks all linked records and historic grants.
- Exact operation retries cannot duplicate capture/review or reapply an old grant.
- Stale reviewers, wrong record hashes, duplicate origins and substituted source
  IDs/bytes are rejected before publication.
- Stored states are validated against their event-derived reducer results, not
  merely self-consistent hashes or an APPROVED label.
- Missing/corrupted stores, evidence, events, pointers and revocations fail closed.
- Capture/review/revocation process crashes leave old or complete new durable state.
- Stage intake binds exact sealed task/checkpoint/Core/profile/ECID/source/receipt
  metadata, stores no cache/draft, and leaves runtime state/action count unchanged.
- Local CLI preparation does not mutate; malformed requests return typed errors.
- New module import edges and no-direct-SQL/no-runtime-mutation intake rules are tested.

## Repairs made during this pass
Input-purpose type validation before revocation lookup; exact task snapshot
binding; bounded labels for unknown original authors; duplicate submitted source
ID rejection; explicit corrupt-store open failure; closure of new fault-test SQL
handles; indexed purpose checks rather than a whole-archive scan on every use.
See PLAN_DEVIATIONS_EXPERIENCE_ARCHIVE_001.md for the rationale and limits.

## Honest limits / next gates
1. HUMAN and permission_ref are local attestations, not authenticated identity or
   verified legal rights. No adversarial caller isolation or production Nexus.
2. Source hashes bind bytes, not truth/ownership. A DB owner can rewrite a complete
   history; local integrity checks are not cryptographic nonrepudiation.
3. No semantic conflict detector, learned evaluator, autonomous curation or actual
   human-review quality benchmark. Scripted HUMAN fixtures are labelled as such.
4. No DatasetSnapshot implementation or downstream trainer. LT-04's snapshot
   isolation/consumption portions remain OPEN; LT-05's storage/review checks pass.
5. Withdrawal is logical, not secure deletion. No restore from revocation in v1;
   no retroactive export recall, backup erasure or model unlearning.
6. No cross-database outbox: intake is explicit and caller-retried. No automatic
   capture guarantee if the process stops before submitting experience.
7. Single trusted operator/runner; no power-loss/filesystem/multi-host guarantee.
8. Histories and requests are bounded. Full audit is an explicit maintenance scan.
9. The separate qualification/Nexus implementation gap remains open. No fixture
   status or archive review authorizes real model release.

**Next bounded recommendation:** DatasetSnapshot001 through the public exact-
revision/purpose interface, using synthetic records and revocation rechecks.
No neural training or generic Aegis Runtime changes are required for that slice.
