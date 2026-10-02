# QualificationEvidence002 — bounded implementation packet

## Question / scope
Can a trusted-local reviewer qualify an EXACT already-evaluated neural profile or
directed transition, bind that decision to frozen evidence, and withdraw it without
rewriting history or granting execution/deployment permission? Initial adapter:
NeuralProbe001 only. It does not certify arbitrary LLMs, neural novelty, efficiency,
training-history authenticity, every subset, every input, or production safety.

## Ownership and boundaries
qualification_contracts: pure bounded JSON, fixed policy/claim types, certificates.
qualification_neural: evidence adapter; public ProbeRuns/ProbeData/NeuralSession
interfaces; re-executes numerical checks lazily using optional PyTorch. It does not
train, change prior reports, or access another owner's SQL/private helpers.
qualification_store: owns its event journal; independent reviewer role declarations,
prepared requests, immutable review/certificate receipts, irreversible revocation.
qualification_cli/demo: explicit local operator tooling; no implicit promotion.
No old runtime owner imports the new subsystem. No callable/code supplied via JSON.

## Preconditions and invariants
Request identifies run/plan/report, one trial, ALL checkpoint hashes, Core/package
ABI, exact profile ECIDs, fixtures, numerical conditions, policy/version/checker.
Core-only is compulsory: non-Core profile approval requires an exact accepted
Core-only claim; transition approval requires exact source/destination profiles.
The bindings of all prerequisites must match. A qualified AB does not imply A,
B, BA, A->AB, another seed, another precision, generation, or other inputs.
Producer cannot review its own request. Reviewer must have the local reviewer role.
Roles are trusted-operator attestations, NOT authentication or cryptographic trust.
Fresh issuance rechecks current source permissions before AND after checking.
Only complete PASS reports can support acceptance. FAIL -> rejected; INCONCLUSIVE
-> inconclusive. Exact terminal retries are HISTORY, never current permission.
Every consumption rechecks scope/hash, prerequisites, revocation, source bytes and
current permission. Revoking a prerequisite blocks dependent use transitively.

## Publication / failures
PREPARED -> DECIDED(QUALIFIED|REJECTED|INCONCLUSIVE). Inspection is historical.
All local mutations append one hash-chained event and head update in a single
SQLite transaction. No separate revocation index; consumption derives it from the
validated event log. Corrupt/missing events fail closed. No undeclared repair.
Contract/permission errors leave the request PREPARED, not an invented verdict.
Crash hooks after prepare, after check, before/after decision commit, before/after
revocation commit. Interrupted decisions may repeat PURE local tests; old external
effects and deployments are never executed. Data checks are point-in-time, not leases.

## Acceptance tests (stimulus -> expected)
Accept exact Core and AB/A profiles -> claim-scoped certificates, no deploy authority.
Try own review / unknown role -> denied, previous history unchanged.
Try AB certificate for A or A->AB -> scope mismatch; no inferred qualification.
Change artifact/report/code/data/fixture -> fresh issuance/use blocked.
Use a failed/incomplete run -> no certificate. Reject manually -> history retained.
Revoke Core evidence -> dependent profiles/transition blocked; old receipts intact.
Delete middle/tail event or change head/body -> RECOVERY_REQUIRED/VALIDATION_FAILED.
Crash before commit -> PREPARED/old revocation; after commit -> durable exact receipt.
Reopen source/store and consume -> same claim with fresh current-use checks.
Evaluation is not approval: merely running the existing probe creates NO claim.

## No hidden expansions
No Nexus authentication/tokens, generation deployment, broad profile selection,
protected exam, learned judge, network, PKI, Runtime integration, or new training.
Source reports are verified by the SAME checked local implementation, not an
independent scientific replication. Role separation is workflow-only here.
