# DatasetSnapshot001 — fixed membership, live permission checks

**MegaMind Alpha 0.4.4 · reviewed-baseline branch · local schema v1**

A snapshot is an immutable selection of exact reviewed record revisions. It is
not an instruction to train, a lasting rights grant, a dataset truth certificate,
or a promise that its validation examples constitute an independent release test.

## Ownership and connection
`dataset_contracts.py` validates and projects. `dataset_store.py` alone owns
`snapshots.sqlite3`. `dataset_cli.py` is explicit operator I/O. The synthetic
`datasetsnapshot001` demo connects the prior stage/runtime/archive pipeline.

Archive history/evidence/revocations remain owned by ExperienceArchive. Active
runtime checkpoints and effects remain owned by RecoveryStore and Ledger. The new
subsystem never writes those databases and never reads another owner's private SQL.
One public archive extension supplies atomic exact-revision batches; a second
supplies a local location/format binding. Source permission integrity was hardened
in the archive owner, not bypassed by snapshot code.

## Public API (standard library only)
All store operations return `status`, `data`, `detail`, `replayed`, `historical`.
Non-success has null data; no partial dataset is returned. Constructors raise
ContractError on explicit creation/open failures. CLI non-success exits 2.

| API | Behavior |
|---|---|
| `DatasetSnapshots.create(directory, archive=...)` | Explicit new local store; binds it to the archive location/format. Requires empty/new directory. |
| `DatasetSnapshots(directory)` | Opens existing compatible storage. Never recreates/repairs missing or corrupt files. |
| `build(request, archive=..., tokenizer_path=...)` | Validate exact membership, check all current permissions, project and atomically store manifest + operation receipt. Returns only the immutable reference. |
| `inspect(snapshot_id)` | Administrative retained manifest, explicitly `use_authorized=false`. Not training access. |
| `operation_receipt(operation_id)` | Historical publication reference or null. Does not grant permission or rerun selection. |
| `list_snapshots(limit=100, after=None)` | Bounded, ID-ordered administrative references. |
| `read_for_use(snapshot_id, expected_manifest_hash=..., purpose='training', split=..., archive=..., tokenizer_path=...)` | Recheck the entire snapshot against current exact archive views, then return that split's examples. |
| `audit()` | Stored manifest/receipt/schema/hash/SQLite consistency. Not current eligibility or truth. |

Archive additions:
- `binding()` returns the verified local descriptor/hash, including canonical path.
- `read_batch_for_use(references, purpose=...)` validates up to 32 exact refs and
  checks all heads, review, purpose and revocations under **one archive transaction**.
  Its output contains the current statement, source metadata, origin observation,
  review, purpose decision, family, sensitivity, and revocation-check observation.

The API uses dictionaries with strict shipped JSON Schemas and semantic validators.
Unknown fields, bool-as-int revisions, invalid hashes/timestamps, duplicate members,
empty training selection, unsupported transforms and non-training uses fail closed.

## Build request and manifest
`DatasetBuildRequest v1` includes:
- Snapshot ID and unique operation ID; attributed HUMAN selector, UTC time, reason.
- Purpose exactly `training`; selected transform; tokenizer ID/version/SHA-256.
- Explicit members: experience ID, integer revision, exact revision SHA-256, split.

Members are sorted by experience ID for canonical operation identity. Selection
is explicit: the builder never auto-follows a newer archive head or skips a blocked
member. At least one `train` member is required. Only `train` and `validation` are
supported. Validation here is development data available to this operator, NOT a
protected evaluation holdout. The future qualification-access boundary is separate.

The manifest binds the entire normalized request, local archive binding, exact
permission-checked views, projection version, and each resulting UTF-8 example/hash.
Original uncertainty, authorship/source classes and source references remain present.
Outputs are generic curated-text examples, not fabricated prompt/answer pairs.
An approved interpretation remains an interpretation, not automatically a proven fact.

### Transforms
- `curated_text_v1`: exactly preserve the approved statement text.
- `normalize_newlines_v1`: replace CRLF/CR with LF, preserving all other characters.

No learned distillation, summarization, custom executable transform, tokenizer
execution, data download, file-code execution or optimization is performed. The
actual tokenizer identity file is hashed at build and every read (32 MiB local
limit); checking its bytes does not prove that it is a functioning trained tokenizer.

### Split and duplicate policy
All records with the same declared family must stay in one split. Any shared exact
source byte hash, including included ancestors, must also stay in one split. Exact
duplicate projected examples are rejected even within a split. There is no silent
weighting or deduplication. The operator must change the explicit selection.
These checks are per snapshot, not a global evaluation-exposure ledger. Falsely
labelled families, hidden ancestry and semantic/near duplicates are not detected.

## Preconditions, postconditions and invariants
**Build pre:** valid bounded request; compatible local stores; exact approved
current revisions; separate training permission for every member/source; pinned
available tokenizer bytes; valid projections and split assignment.

**Build success:** immutable manifest and matching operation receipt publish in one
snapshot-store transaction. A receipt states what was selected, not continuing use
eligibility. **Build failure:** no partial snapshot or receipt; prior data intact.

**Read pre:** exact stored manifest identity; matching archive binding/tokenizer;
every selected revision is still current, reviewed and permitted for training.
**Read success:** one bounded split returned with lineage and point-in-time scope.
**Read failure:** typed non-success with no examples; stored manifest unchanged.

**Invariants:**
1. Published membership/text never changes in response to live archive edits.
2. Every read rechecks all selected current revisions and all current source-purpose
   revocations. Previous success or static audit is not cached authority.
3. A blocked validation member blocks a request for the train split too. No partial
   success or silent dataset shrinkage.
4. Corrections, annotation, review or even an unrelated purpose decision create a
   newer record head. This conservative version requires explicit snapshot rebuild.
   Unrelated records elsewhere in the archive do not affect membership/eligibility.
5. Permission revocation may block consumption without changing the record hash.
   The current revocation gate therefore cannot be replaced by a revision-hash check.
6. Exact operation retries return the original history/reference only; they neither
   rebuild with changed inputs nor restore a revoked grant.
7. Snapshot storage never promotes training, changes active runtime state or executes
   an external action. Human role strings are local attestations, not authentication.

## Time-of-check and crash semantics
The archive's batch transaction is a coherent point-in-time eligibility observation.
The snapshot-store publication is a separate transaction. **There is no atomic
cross-database approval lease.** If permissions change after observation, a snapshot
may legitimately persist the historical selection while being unusable at the next
read. This race is explicitly tested; build success does not promise future use.

Each read rechecks the whole snapshot under a fresh archive transaction. Downstream
batch/epoch consumers must use this gate again, not retain it as indefinite approval.
This slice has no running trainer to interrupt, no export recall and no unlearning.
Bytes already returned to a caller cannot be removed from that caller's memory.

Crash hooks are test-only Python keywords, never fields accepted in input JSON.
Child-process death is tested after manifest insert, after operation insert, before
commit and after commit. Pre-commit deaths leave neither row; post-commit death
leaves both. Reopening and replaying the exact command returns one publication.
A revocation before a new retry publication blocks it. An already committed retry
may return its historical receipt but cannot regain read permission.

## Identity, scaling and trust limits
Snapshot storage binds to a canonical local archive location. Silent relocation or
substitution is rejected. A future explicit portable identity/migration protocol is
not implemented. A malicious operator who replaces an entire store at the same path
or forges a consistent disk history is outside this local trust model. Hashes are
integrity bindings, not signatures, truth, ownership verification or anti-rollback.

Budgets: at most 32 selected members; a 4 MiB materialized manifest; the archive's
existing per-record/source/revision limits. No streaming or batching-scale performance
claim. The local revocation ledger is fully checked once per batch to detect a lost
or repointed revocation index. This conservative cost is deliberate; optimizing it
requires equivalent integrity checks, not stale cached permissions.

Logical withdrawal/revocation does not securely erase snapshots, exported copies,
backups or previously trained weights. Administrative inspection remains possible.
No private user/conversation/companion data is ingested by tests or demos.

## Local CLI
Run the connected demonstration (temporary data by default):

```console
python -m nss_base.datasetsnapshot001
```

To preserve its synthetic files for inspection:

```console
python -m nss_base.datasetsnapshot001 --directory ./snapshot-demo
python -m nss_base.dataset_cli --store ./snapshot-demo/snapshots inspect dataset-v1
python -m nss_base.dataset_cli --store ./snapshot-demo/snapshots audit
```

For operator-selected records in an existing archive:

```console
python -m nss_base.dataset_cli --store ./datasets --archive ./experience init
python -m nss_base.dataset_cli --store ./datasets --archive ./experience prepare-build --snapshot-id draft1 --operation-id build:draft1 --reviewer operator --reason "Reviewed selection" --tokenizer ./tokenizer.json --tokenizer-id core-tokenizer --tokenizer-version 1 --train exp1 --validation exp2 > request.json
python -m nss_base.dataset_cli --store ./datasets --archive ./experience build request.json --tokenizer ./tokenizer.json
```

Preparation only writes a request. Check it before applying; it neither approves
records nor grants training permission. To read, use the exact SHA-256 returned by
`build` as `--expected`:

```console
python -m nss_base.dataset_cli --store ./datasets --archive ./experience read draft1 --expected <manifest-sha256> --tokenizer ./tokenizer.json --split train
```

The CLI returns JSON; redirecting a read exports data and cannot imply recall.

## Acceptance mapping
LT-04: fixed membership, exact revision and purpose rechecks, revocation blocking,
reopen/crash behavior, explicit rebuild and no silent mutation: local software tests.
LT-05: explicit human-attested selection, no approval-by-confidence, split controls:
local software tests. LT-06 authenticated operator authority remains OPEN. No neural
learner/evaluator, release security, training, general Runtime or HSA/MSA/DARP claim.

See [logic/pseudocode](DATASET_SNAPSHOT_LOGIC.md), [implementation packet](implementation_packets/DATASET_SNAPSHOT_001.md),
[deviations and audit repairs](PLAN_DEVIATIONS_DATASET_SNAPSHOT_001.md), and
[release self-audit](audits/datasetsnapshot001/AUDIT_REPORT.md).
