# PersistentState001 — implementation audit / v0.4.14

Status: **PASS for the scoped trusted-local symbolic-state contract**; not production,
neural-memory, model-identity, prompt-injection or performance qualification.
Completed verification: 2026-09-13T12:31:04.314266+00:00.

## Basis and scope
User-approved first integration from the fly-inspired addendum v0.2 §§6–7,18,23 and
provided PS-01…PS-12 cases. See INPUT_LOCK.json and ../../PERSISTENT_STATE_SOURCE_MAP.md.
Baseline ZIP SHA-256: `5bf65a94f85e3c70ac53757d61754f63358389c8d8629c2aede5c270815e5dcf`
Exact input bytes and all four source hashes are recorded in INPUT_LOCK.json.

Baseline archive/sidecar and all 832 manifest-covered files were checked. The unchanged
baseline passed 1,063 tests before implementation (baseline_tests.txt). Original
addendum, reconciliation, acceptance cases and baseline ZIP remain unchanged.

## Implemented boundary
- Same Generations journal and current-task owner; no extra database or pointer.
- Explicit reviewed admission from TaskRecord v1 to agent/project/session-scoped v2.
- Small allowlisted, source-backed deltas with expected revision/hash/ECID and exact
  short-lived review; protected policy/scope/receipt/source/Core fields cannot be patched.
- Initial policy requires separate declared review for ALL new state deltas, more
  conservative than the source's consequential/identity minimum.
- Goal, questions and notes remain attributed working DATA, never root instructions.
- Existing source/experience readers verify admitted exact sources, current retrieval
  rights, revision, identity challenge, expiry and byte limits.
- Current read and context reuse fail on stale or incompatible scope/configuration.
  Retry of the identical committed event returns HISTORY_ONLY, not renewed permission.
- Events, revisions and current head commit atomically; normal state recovery does not
  re-execute external effects. Existing uncertainty reconciliation remains authoritative.
- Existing v1 schemas remain unchanged. Explicit v2 exports add scoped lifecycle/state
  behavior; v1 command access cannot bypass scope after admission.

## Actual verification
1,111 unit tests passed (1,063 inherited + 48 new collected cases).
The 48 new cases include four dynamically generated BIND/UPDATE process-crash cases,
one real uncertain-external-action process exit, and an explicit versioned-export regression.
All 68 inherited Python test/helper files remain byte-identical; none was removed or weakened.

All 27 required gates passed out of 28 recorded gates. The 15 demos include
both the previous connected learning/adoption loop and the new scoped-state demo. The
25 parent + 32 subordinate graphs pass structural validation, not semantic proof.
Dependency edges, compilation, deterministic regeneration, maintenance and manifest checks pass.

| Gate | Status role | Exit | Seconds |
|---|---|---:|---:|
| unittest | required | 0 | 807.825 |
| experiment001a | required | 0 | 0.564 |
| experiment001b | required | 0 | 0.62 |
| stagehandoff001 | required | 0 | 0.88 |
| experiencearchive001 | required | 0 | 1.009 |
| datasetsnapshot001 | required | 0 | 1.467 |
| evaluationrun001 | required | 0 | 2.188 |
| neuralprobe001 | required | 0 | 23.867 |
| qualificationevidence002 | required | 0 | 9.604 |
| localnexuspermissions002 | required | 0 | 9.186 |
| overlaygenerationmanager001 | required | 0 | 13.27 |
| overlaycatalogcontroller001 | required | 0 | 12.847 |
| contextretrieval001 | required | 0 | 17.377 |
| boundedlearnercoordinator001 | required | 0 | 19.712 |
| connected_alpha_acceptance | required | 0 | 0.623 |
| candidateacceptance001 | required | 0 | 46.444 |
| candidate_connected_acceptance | required | 0 | 0.957 |
| persistentstate001 | required | 0 | 19.814 |
| maintenance | required | 0 | 0.794 |
| fresh_exact_neural_evidence | required | 0 | 2.649 |
| historical_portability_audit | required | 0 | 2.705 |
| reference_neural_evidence | historical advisory | 1 | 2.593 |
| atlas | required | 0 | 0.569 |
| helper_graphs | required | 0 | 0.66 |
| dependencies | required | 0 | 0.826 |
| compile | required | 0 | 0.676 |
| regeneration | required | 0 | 5.227 |
| manifest | required | 0 | 0.672 |

Historical advisory: **reference_neural_evidence**. The older schema-v1 strict numerical report is not
rewritten or made eligible; it lacks the fresh numerical contract. Fresh exact numerical
replay passed separately. A raw archived MSE discrepancy is not hidden by a tolerance change.

Raw command logs and exact command identities are in release_checks/summary.json. Their
hashes were checked before copying. This audit is assistant self-review plus independent
fresh-process/clean-extraction execution, not a separate external reviewer endorsement.

## Connected result
Reviewed goal and consequential unresolved question survive owner close/reopen exactly.
Wrong scope is rejected; source unit **m/s** is resolved from the
admitted exact source. Unreviewed deltas and mandatory byte overflow are refused.
An identity-sensitive source dispute blocks current use but preserves its prior revision;
an explicit reviewed retirement restores a usable current record.

The task then follows **AB → A → CORE**, preserving scoped
state and provenance, and closes. It records 12 task revisions.
A historical retry does not reopen it. Accepted Core/overlay artifacts, current generation,
declared instruction reference and original probe report remain unchanged. Prior committed
mock external effect count: **1**.
Final current record: 2922 canonical JSON bytes under a
65536-byte admitted cap. This is accounting, not a token/energy win.

## Audit findings and repairs
1. Initial targeted test used wall-clock review timestamps against a fixture's deliberately
   shifted clock. The review correctly failed. Fixture timestamps were aligned to its
   declared clock; review validity was not relaxed.
2. A source referenced only by a state note was validated but omitted from the context
   source list, blocking exact rehydration. A negative-first test reproduced it; the
   shared context assembler now includes such references as mandatory source pointers.
3. The initial 32-delta cap could prevent retiring a larger expired-note set: every partial
   cleanup still failed current-use checks. Reproduced with 33 notes. The event bound is
   now 256 distinct targets while record collections remain capped at 128 each and byte
   budgets remain enforced. One explicitly reviewed cleanup can cover the admitted set.
4. The first complete clean suite caught an accidental expansion of the legacy catalogue
   schema export. The inherited test was correct. Restored its original five-arm file
   byte-for-byte and added catalog_command_v2.schema.json instead; runtime dispatch and
   a new export-regression test enforce the version boundary. The intermediate 1,109-test
   run had one ERROR and was not accepted. Another incomplete clean run was stopped when
   this was diagnosed. The final 1,111-test run includes all repairs.

Negative-first and intermediate failure evidence is preserved under diagnostics/. Earlier
partial runs are not represented as successful releases. Three new Graphviz charts were
rendered and visually inspected; schema/graph sources, not image prose, are authoritative.

## Limits and unimplemented work
- Scripted proposer/reviewer; no learned summarizer, factuality/sensitivity classifier or
  self-evaluation quality claim. Local labels/scopes are not authenticated tenancy/security.
- Structural DATA labels do not prove a future LLM ignores malicious source instructions.
  The pinned instruction-policy hash is a declared reference, not a verified policy file.
- Source permission checks are point-in-time; there is no cross-store lease or recall of
  exported bytes. Scoped historical inspection preserves evidence, not training authority.
- Expiry is explicit removal after review, not secure erasure or deletion of backups/weights.
- JSON byte limits are not tokenizer limits. Mandatory state is preserved wholesale; no
  semantic compressor, automatic decomposition or end-to-end efficiency gain is claimed.
- The five new fault cases are process exits, not power-loss, disk-failure or concurrent
  multiworker qualification. Tests executed on Linux-6.18.44-x86_64-with-glibc2.41; native Windows is untested.
- No neural h/eligibility/adaptive W, new Core, live learning, model downloads, DARP/HSA,
  native low-bit execution or generic Runtime adaptation. Existing fixture setup may train
  the same tiny neural probe; state commits themselves do not train or dispatch effects.

## Release closure protocol and evidence location
The fully tested clean tree and final deliverable are compared against all 301 pinned
implementation/test/spec/schema/fixture/reference/version inputs in CLEAN_TEST_INPUTS.json.
Only audit/Markdown evidence and the release manifest are finalized after the full run.
The final clean-extracted demonstration, fresh numerical replay, integrity and structural
check results are recorded separately in
`MegaMindAlpha_PersistentState001_Release_Verification.txt` delivered alongside the archive.
That external record binds the final ZIP SHA-256; this source document does not claim
an archive can include a stable hash of itself.
