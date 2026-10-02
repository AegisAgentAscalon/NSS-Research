# Acceptance matrix — ContextRetrieval001

| Stimulus | Required observation |
|---|---|
| Mandatory goal/constraints/clarifications and receipt-bearing record | Exact spine retained, no owner mutation |
| Optional irrelevant source not selected | Not read; omission retains only its identifier/reason |
| Missing speed unit with a pinned source providing m/s | Packet includes exact m/s plus hydration provenance; record stays unchanged |
| Known value disagrees with exact source | CONSTRAINT_CONFLICT; no partial packet |
| Required fact absent or source unit unknown | NEEDS_CLARIFICATION; no fabricated answer |
| Missing file/field, changed hash, invalid UTF-8/duplicate JSON field | Typed failure, not plausible replacement |
| Mandatory payload exceeds limit or limit is one byte too small | BUDGET_EXHAUSTED with explicit recovery; state unchanged |
| Optional item exceeds payload limit | Omitted, not mandatory-field truncation |
| Non-ASCII content | Count actual canonical serialized bytes, not characters/tokens |
| Training allowed but retrieval unknown/denied | Retrieval blocked |
| Approved experience with open dispute/new revision/source withdrawal | Exact current check blocks stale use |
| Optional candidate is inaccessible or has no query term | Explicit omission; no text leakage |
| Rehydrate source through a permitted record | Exact bytes; administrative inspection methods never called |
| UTF-8-splitting/out-of-range/wrong-hash evidence slice | Explicit typed rejection |
| Old packet used after finish/move/cancel/generation withdrawal | Rejected by existing task/qualification owner |
| Goal/payload/omissions tampered and outer digest recomputed | Rebuild-and-compare rejects it |
| State/permission changes during assembly | Recheck rejects before payload return |
| Process exits during task or archive read | No task/archive/pointer/action mutation; normal read can resume |
| Restart consumer process and use persisted packet | Fresh checks, no in-memory permission dependency |
| Import or open CLI help | No implicit training/network/actions |
| Full synthetic integration | AB -> A -> CORE, exact evidence, explicit overflow, revocation/stale rejection, effect count 1 |

Tests use small synthetic fixtures and scripted local review. They do not certify
semantic selection quality, native context efficiency, adversarial storage, power
loss, concurrency, learned evaluation, production security or general neural skills.
