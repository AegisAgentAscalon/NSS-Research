# ExperienceArchive001 — approved-scope implementation packet

## Scope and baseline
User requested the next system in the shared NSS architecture. Follow 0.4.2
NEXT_STEPS: persistent experience storage + human review only. Baseline archive
SHA-256 ddbf7cf98d4826846852a12d0b266128de47fcbcd41909b59b463c1cf4a1b995.
Reproduced 128 tests, 001A/001B/StageHandoff, 25 atlas flows, import/compile/manifest.
Target 0.4.3, reviewed-baseline branch. No missing-source 0.6 implementation implied.

## Owners / public boundary
* experience_contracts: bounded JSON validation, immutable revision reducer,
  provenance and purpose-use decisions. Pure; no SQL/runtime/neural operations.
* experience_store: ONLY owner of archive.sqlite3, captured evidence BLOBs,
  capture records, append-only revision/event histories, current archive revision,
  source-purpose revocations. No active execution pointer or checkpoint mutation.
* experience_intake: explicit one-way submission from a SEALED, exact published
  checkpoint through public runtime APIs. No changes to recovery/action stores.
* experience_cli: local operator commands; human role is attested metadata, NOT
  authenticated identity. No network server, scheduler, auto-review, or auto-training.
* experiencearchive001: synthetic demonstration of connected usage and reopening.

## Types and APIs (schema v1)
Actor(id, kind HUMAN|MODEL|SYSTEM, version); source metadata(id, kind, author,
recorded_at, media_type, sha256, content, generator?, parent_source_ids,
rights_note). SYNTHETIC requires named/versioned generator and parents.
CaptureRequest(operation_id, experience_id, actor, at, observation, family_id,
sensitivity, evidence[], statement). Submission always starts PENDING_REVIEW
and every downstream purpose UNKNOWN. Confidence never approves a record.
MutationRequest(operation_id, experience_id, expected_revision_hash, actor, at,
reason, action, payload). Actions: ANNOTATE, CORRECT, REVIEW, DISPUTE, RESOLVE,
PERMISSION, WITHDRAW. Human metadata required for consequential actions.
SourceRevocation(operation_id, actor, at, reason, permission_ref, sha256, purpose).
Revision: capture_hash, revision, parent_hash, source metadata, statement,
review, conflicts, per-purpose decisions, immutable derivation from exact command.
Purposes: memory, retrieval, training, redistribution; all distinct.

ExperienceArchive.create/open; capture; change; revoke_source; inspect; history;
list_records (bounded); inspect_source; read_for_use(expected exact head); audit.
Public methods return typed status/data/detail/replayed/historical; errors never
turn a denied capture/review into a usable record. Constructors fail explicitly.
Only operators inspect full raw/history. read_for_use always consults CURRENT
review and source revocations. Historical reads never re-grant a revoked purpose.

## State machine / logic
CAPTURE: validate bounded exact schema -> normalize/copy evidence and verify hashes
-> PENDING revision, UNKNOWN purposes -> atomic evidence+capture+event+head commit.
MUTATE: validate exact request -> retry ID lookup (historical result only) ->
verify full existing lineage -> compare expected head -> check human role/action
and timestamp -> reduce new revision -> atomic event+revision+head commit.
CORRECT/ANNOTATE: retain raw; new statement supersedes previous statement hash;
review resets to PENDING (QUARANTINED with open conflict); reset prior ALLOWED
purpose decisions to UNKNOWN. Never implicitly resolve a conflict.
DISPUTE: append identified conflict -> QUARANTINED. RESOLVE: human records evidence
and reasoning -> PENDING when no open conflicts. Separate REVIEW required.
REVIEW: human APPROVED/REJECTED only; cannot approve open conflicts or withdrawn.
PERMISSION: separate purpose decision plus permission reference; APPROVED alone
never permits retrieval/training. Declared permission is not a legal verification.
WITHDRAW: terminal archive state blocks downstream use, retains inspectable history;
not physical erasure. No purge/secure deletion guarantee in this slice.
REVOKE_SOURCE: append immutable purpose revocation -> blocks every record using
those exact bytes, including copies and older revisions. No restore in schema v1.
USE: verify lineage, exact head, current approved review, scoped ALLOWED permission,
no open conflicts/withdrawal/source revocation -> return source-linked curated view.

## Integration / failure semantics
Read exact sealed checkpoint and validate artifact/ECID/receipt metadata. Capture
its portable TaskRecord and local hashed source evidence; no cache/draft retained.
Archive commit is separate from runtime publication: failure leaves runtime alone;
explicit caller retries with the same ID. No exactly-once cross-database claim or
automatic delivery/outbox. Archive proves byte/lineage consistency, not semantic
truth or real-world authorship. One operator/runner is the supported deployment.

## Tests defined before implementation
1 strict schemas: unknown fields, bool revisions, deep/oversized/invalid UTF-8 JSON,
  invalid hashes/timestamps, duplicate IDs, dangling refs, synthetic provenance.
2 submission pending + all permissions UNKNOWN; original evidence stays exact.
3 human correction appends, does not rewrite; stale review/CAS rejected.
4 model confidence/role cannot approve/grant/resolve/withdraw/revoke.
5 approved retrieval != training; changed statement invalidates past grants.
6 disputes quarantine; explicit resolution then review needed; reject/withdraw.
7 source revocation survives reopen, blocks all linked records and historic grants.
8 operation ID exact replay vs substituted command; past result never reactivates.
9 process death before/after commit for capture, review and source revocation;
  no partial evidence/event/head; exact retries do not duplicate writes.
10 corrupt blob/revision/event/head/metadata fails closed; missing DB not recreated.
11 connect sealed StageHandoff checkpoint; preserve task/source/ECID/receipt;
   stale/unsealed/changed evidence rejected, runtime unchanged, mock effects once.
12 CLI init/submit/review/list/show/use/audit; imports bounded; full inherited suite.

## Definition of done / non-goals
Typed APIs + strict JSON schemas, docs/pseudocode/atlas experience reconciliation,
synthetic fixtures and executable demo, preserved old tests, new branch/fault tests,
full retained logs, manifest, fresh-extracted release. LT-05 storage/review portion;
LT-04 revision/revocation prerequisites only, NOT DatasetSnapshot or trainer proof.
No semantic conflict detector, RAG service, auto knowledge import, learned evaluator,
permissions authentication, training, downloads, real effects, generic Runtime,
DARP/HSA/MSA/recurrence, benchmarks or private Yumi/user records.
