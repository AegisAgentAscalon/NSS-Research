# EvaluationRun001 — public contract and operator guide

Status: implemented **local synthetic development evidence**. Not neural evaluation,
independent qualification, a permission service, or deployment approval. The learned
evaluator in the Primary Core remains a future implementation. This piece prepares
its result boundary without pretending arithmetic Python checks are intelligence.

## Owners and dependencies
`evaluation_contracts` owns pure schemas, bounds, thresholds and integer comparison.
`evaluation_inputs` owns bounded artifact capture and installed-code fingerprinting;
any development data is consumed only through `DatasetSnapshots.read_for_use`.
`evaluation_store.EvaluationRuns` alone owns evaluation SQLite rows and receipts.
The CLI and demo orchestrate public interfaces. No evaluation module owns the live
runtime configuration, archive revisions, snapshot manifests, or release status.
There is no trainer/executor/plugin callback accepting arbitrary executable code.

## Exact identities
An `EvaluationPlan` contains: schema_version; run_id; locally HUMAN-attested actor;
UTC operator timestamp; reason; exact candidate manifest path/hash, profile and
expected ECID; exact suite path/hash; implementation SHA-256; repeat count; maximum
check budget; optional development snapshot ID/hash with `validation` split.

The suite is separately authored DEVELOPMENT_SYNTHETIC data with an explicit local
evaluation-use attestation. It contains test IDs/versions, an allowlisted checker,
exact fixture-file hashes, expected integer vectors, mandatory flags and frozen
integer pass threshold (basis points). At least one mandatory case is required.
Duplicate exact input/checker cases are rejected rather than silently reweighted.
No raw string, filename or catalogue entry is executed as Python or a tool.

The candidate uses the existing integer Core/Overlay manifest and ECID convention.
All Core and overlay artifacts are verified, including inactive artifacts covered
by that manifest. An arbitrary individually valid union cannot be synthesized.
Manifest evidence_ref values remain DECLARATIVE FIXTURES, not trusted qualification.
Tokenization, context and overlay ABI identifiers are bound manifest metadata here;
this slice does not execute those neural mechanisms or establish their validity.

Material retains bounded UTF-8 JSON artifact bytes plus digests, ordered operation
semantics and environment identity. The implementation fingerprint includes all
installed nss_base Python sources, all schemas, VERSION, Python version/implementation,
platform and machine. A process pins that manifest on import and refuses observed
changes until restarted. This is source-file checking, not trusted binary attestation
or proof against a malicious host/import race. Tests and candidates are ordinary
data; self-consistent hostile rewriting of all local hashes is outside the threat
model.

## State machine and outcomes
`ABSENT -> PREPARED -> FINALIZED` is monotonic. PREPARED stores exact plan/material
but NO trial score/verdict or completion receipt. EXECUTE may restart only the pure
bounded computation. FINALIZED publishes the report and its completion receipt in
one SQLite transaction. A finalized attempt is never edited into a better score.
A new candidate, budget, suite, threshold, fixture or requested data selection needs
a new plan/run identity. Exact retries return the historical receipt.

Operation outcomes (`status`) and evaluation outcomes (`verdict`) are different:
- SUCCESS means the requested record operation completed.
- PASS means the entire scheduled matrix ran, mandatory cases passed and the fixed
  overall threshold passed. It is NOT a qualification or deployment token.
- FAIL means a complete attempt did not meet its frozen acceptance criteria.
- INCONCLUSIVE means the check budget left planned trials unexecuted. Missing trials
  are not silently omitted from the denominator. A failure among a partial matrix
  remains visible but does not turn incompleteness into a complete result.
- A source, schema, storage or access error returns a typed non-success with no
  new finalized report. If preparation committed, PREPARED remains for inspection.
- Reproducible is null for incomplete or single-repeat runs, not a fabricated true.

The only checker is `exact_integer_sequence_v1`: apply bounded manifest affine
integer operations and compare exact vectors. It records input/expected/output
hashes and output vectors for every ordered case/repeat. Report validation recomputes
that versioned deterministic relation from retained material. This catches accidental
or inconsistent row/score edits; it is NOT an independent judge of the algorithm.

## Public API
Class creation/open raise typed ContractError on invalid initialization. Operations
return `{status, data, detail, historical, replayed, authorizes_deployment:false}`.

- `EvaluationRuns.create(directory)` explicitly initializes an empty/new store.
- `EvaluationRuns(directory)` opens an existing valid store, never auto-repairs it.
- `prepare(plan, root=..., snapshots=None, archive=None, tokenizer_path=None)` captures
  exact valid inputs, or returns an exact historical retry. Does not run checks.
- `execute(plan, root=..., ...)` prepares/resumes, gates current inputs before each
  repeat and finalization, runs pure checks, and publishes one report+receipt.
- `inspect(run_id)` is ADMINISTRATIVE HISTORY, containing retained synthetic material.
  It neither consumes newly permitted dataset text nor certifies current eligibility.
- `verify_current(run_id, expected_report_sha256=..., root=..., ...)` checks exact
  finalized evidence and current dependencies. Never silently follows a new report.
- `compare(left_id,right_id)` compares historical complete/incomplete evidence only
  when exact suite, fixtures, repeats, budgets and implementation identities agree.
  It reports counts and verdicts, does NOT choose/deploy a model. Candidate profiles
  may differ. Development training-lineage snapshots may differ and remain explicitly
  bound; they are not scored test inputs. No resource-efficiency inference follows.
- `list_runs(limit=100,after=None)` paginates validated historical receipts.
- `audit()` validates stored identities, trial matrices and receipt relationships.
  Static audit does not regrant current source permission.

## Development snapshot integration
A selected DatasetSnapshot is an optional development training-lineage prerequisite,
NOT a hidden benchmark. Its text is NOT fed to the arithmetic checker. The public
training-purpose validation-split read is rechecked at prepare, each repeat and the
final gate. Only the snapshot identity, example digest and count are retained.
No permission is obtained by administrative snapshot/archive inspection. A stale
record, revoked source, changed tokenizer or substituted archive blocks new use.
Historical reports stay intact after revocation, and exact finalized retries remain
history. This code cannot recall exported bytes, cancel external training, erase
backups, or unlearn weights. There is no cross-store atomic permission lease: a
permission may change immediately after the last observation.

## CLI (repository root, Python 3.10+, standard library)
```console
python -m nss_base.evaluation_cli identity
python -m nss_base.evaluation_cli --store ./eval init
python -m nss_base.evaluation_cli --root fixtures/evaluationrun001 prepare-plan --run-id example-A --candidate candidate/manifest.json --suite suite.json --profile A --operator local-operator --reason "Explicit synthetic development check" > plan.json
python -m nss_base.evaluation_cli --store ./eval --root fixtures/evaluationrun001 prepare plan.json
python -m nss_base.evaluation_cli --store ./eval --root fixtures/evaluationrun001 execute plan.json
python -m nss_base.evaluation_cli --store ./eval inspect example-A
python -m nss_base.evaluation_cli --store ./eval --root fixtures/evaluationrun001 verify-current example-A --expected-report-sha256 <hash-returned-by-execute>
python -m nss_base.evaluation_cli --store ./eval list
python -m nss_base.evaluation_cli --store ./eval audit
python -m nss_base.evaluationrun001
```
`prepare-plan` does not create a store, verify a claimed human's authority, or run
checks. `execute` returns exit code 2 for non-PASS verdicts as well as operational
failure; inspect/audit may succeed for historical failed evaluations. For a linked
snapshot supply global `--snapshots`, `--archive`, `--tokenizer` together, and pin
its ID/hash in prepare-plan with `--development-snapshot` / `--snapshot-sha256`.
No deployment, network, training or dynamic plug-in command exists.

## Limits and guarantees deliberately NOT made
32 test cases, 5 repeats, 160 checks, 64 integers/case, 16 affine operations,
64 profiles, 128 declared transitions, 1 MiB/file, 2 MiB captured artifact bytes,
4 MiB stored record. The budget counts checks, not joules/latency or wall-clock time.
Local trusted operator, single-worker intended use. SQLite atomicity/crash tests
are not a concurrency, hostile-disk, distributed exactly-once or production claim.
No protected holdout access, global exposure ledger, authenticated identities,
Nexus release permits, neural evaluator, actual learning, throughput claim, or
proof that someone did not train on these development cases.

## Relationship to research
This completes result/evidence plumbing, not internal-evaluator competence (LT-08),
independent qualification, identity continuity or the NSS neural hypothesis. A next
neural checker will need an explicit numerical/tolerance, seed, device, termination,
weights-preservation and held-out-test contract. Never reuse this integer scope to
label learned model output as already qualified.
