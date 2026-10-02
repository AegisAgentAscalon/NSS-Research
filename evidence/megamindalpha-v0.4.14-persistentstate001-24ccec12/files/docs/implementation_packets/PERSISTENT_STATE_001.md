# PersistentState001 — compact implementation packet

Source: fly-inspired addendum v0.2 §§6–7,14,18,23; existing v0.4.13 source owners.
Owner: Generations. Entry: CatalogController.apply/read/state_history. Pure contracts:
state_contracts/state_updates. Source guard: state_sources through EvidenceReader and
ExperienceArchive. Context remains read-only. No new store.

Preconditions: current running unsealed ticket; explicit scope; expected record revision,
hash and ECID; reviewed command with distinct declared local reviewer; exact current
permitted sources; finite bounded fields; coherent action receipts.
Postconditions: exact receipt + next revision + current head atomically, or prior state
unchanged and typed failure. Duplicate exact event returns history only.
Invariants: scope/policy/weights/permissions/receipts protected; no external replay;
source attribution and review history retained; data never becomes root instructions;
mandatory overflow and source uncertainty cannot silently disappear.

Schema/API: see ../PERSISTENT_STATE_001.md and generated schemas. Public inputs distinguish
BIND_STATE, UPDATE_STATE and scoped existing lifecycle commands. Version1 inputs remain
legacy; they must not act as an unscoped bypass onto admitted version2 state.

Dependencies: static allowlist in spec/python_dependencies.json. No private SQL outside
Generations; no direct source permission mutation or training/qualification/publication.
Failure recovery: reread/re-propose on revision conflict; fresh review for changed requests;
explicit retirement/expiry for blocked state; history-only for completed tasks.

Tests: tests/test_persistent_state.py and tests/test_persistent_state_crashes.py, plus
all inherited owner/recovery/source/candidate tests. Map exact PS cases in the source map.
Run tools/run_release_checks.py from a clean extracted checkpoint before handoff.
Optimization rule: reuse validation/storage/read primitives, not duplicate state owners;
retain distinct negative/crash branches. Generated logic comes from the existing tools.
