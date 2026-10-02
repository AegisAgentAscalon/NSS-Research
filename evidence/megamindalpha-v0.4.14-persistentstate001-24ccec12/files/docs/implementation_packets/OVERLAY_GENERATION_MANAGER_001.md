# Implementation packet — OverlayGenerationManager001

## Boundary
Owner: local generation catalogue. The shared journal is mechanism only, not another
policy/authority domain. No private access to qualification, archive, dataset or task
checkpoint storage. Existing replay grants and numerical checkers keep their scope.

## Preconditions
- Exact Core/ABI/precision and immutable overlay hashes agree with current source.
- Every declared profile and directed transition has matching accepted child evidence.
- CORE is present and every selected profile has a qualified directed return to it.
- Family review is by a distinct declared reviewer; issuer differs from executor.
- Release source epoch/hash matches; target same-Core; operation scope and TTL valid.
- All work is registered; no open managed stage at each release mutation.

## Postconditions
- Success: exact staged family/current epoch, predecessor archive and completion
  receipt are committed together; prior bytes remain inspectable.
- History: exact old receipt is returned without republishing or renewing permission.
- Non-success: typed error; source pointer unchanged; partial candidate work remains
  inspectable/abandonable, never a half-current generation.
- Stage access: only a valid open exact ticket can obtain current profile artifacts.

## Invariants
No Core or overlay mutation; no inferred subset/reverse edge; no generation mixing;
no partial release; no stale-epoch cache use; no reused abandoned grant; no repeated
external effect; no automatic release authority from evaluation or qualification.

## API
`Generations.create/inspect/inspect_generation/inspect_release/inspect_stage`
`propose -> qualify -> make_request -> issue -> prepare -> stage -> publish`
`revoke(RELEASE|QUALIFICATION)`, `abandon`
`pin_stage -> read_stage -> close_stage`

Use field schemas in schemas/generation_*.schema.json. Runtime validators additionally
check semantics, time, evidence, dependency closure, exact artifacts and current state.
`from_evidence` assembles but does not qualify a candidate manifest. It accepts only
existing exact accepted certificates from the built-in qualification owner.

## State and failure table
| Stimulus | Expected outcome |
|---|---|
| Missing CORE, evidence, dependency or return | Reject manifest/review, no release |
| Wrong code/environment/artifact/source permission | Reject current use with original failure |
| Wrong actor, replay grant, expiry, withdrawal | No admission / no publication |
| Source advances then returns to same hash | Old epoch still rejected (ABA prevention) |
| Open managed work | Publication blocked until explicit finish/recovery/close |
| Crash before durable phase commit | Previous phase/epoch remains |
| Crash after phase commit | Committed phase recoverable; receipt history unchanged |
| Retry already-published operation | No second publication, even after later releases |
| Rollback request | New approval and current checks, exact archived target only |
| Current evidence revoked | New reads/pins blocked; no invented automatic fallback |
| Staged bytes corrupt | Fail closed before pointer change |
| Closed/cross-epoch ticket | Reject; portable-input rebuild required |

## Tests and optimization
Tests are split by contract, lifecycle, process-crash, integrity/CLI and tooling.
Mutation and crash tables retain explicit case labels and expected results without
one copied test body per case. The inherited behavioral suite remains, except its
obsolete blanket byte-freeze assertion. No tests are removed to obtain a green result.

Do not optimize away current-use checks or append-only history. No unmeasured speed
claims. Large model/storage throughput, authenticated authority and concurrent serving
are deliberately deferred, not represented by a generic mocked PASS.
