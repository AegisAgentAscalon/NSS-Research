# Test and implementation catalog

This catalog points to the actual retained test scripts, protocols and results. It is an editorial index built by reading source text/AST only, not by running any test or importing a model. Original study roots appear inside their unchanged ZIPs under `original_archives/`. Use a working copy for any separately authorized reproduction.

## SH01

664 reported assertions; seeded lifecycle, 11 deliberate fault checks, native/reference arithmetic, gradient and sparse-shape checks. Training cohort remains seven finals out of eight planned.

Prospective protocol: `sources/SH01/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/SH01/README.md`.

### `source/preflight.py`

Original member: `NSS_NBR02_SH01_Execution_v0.1/source/preflight.py`. SHA-256: `18d9ba341b18af426f846490254bc65fd50163f5971c57a74b377b6ebb544d79`.

Source-defined function locations: `main` (L11), `check` (L13), `throws` (L16), `__init__` (L88), `__torch_dispatch__` (L89), `walk` (L91).

The original member inventory (`indexes/SH01_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

## SH02

92 reported cases; graph/feature parity, output/gradient parity, cache/plan mutation and faults. The strict historical bitwise regression still returns failure in the recorded run despite admitted tolerance/class parity.

Prospective protocol: `sources/SH02/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/SH02/README.md`.

### `scripts/post_audit.py`

Original member: `NSS_NBR02_SH02_Execution_v0.1/scripts/post_audit.py`. SHA-256: `76e0e5cb4f3605fcc9927596d7b8e0008028ac6ef7dc1dd4a9df743a60006522`.

Source-defined function locations: `main` (L8).

### `scripts/regression.py`

Original member: `NSS_NBR02_SH02_Execution_v0.1/scripts/regression.py`. SHA-256: `e7d43eb07a4e37a48b8d6138d6a5b5c41b26367226d4b5252629799bfd5b5c74`.

Source-defined function locations: `main` (L8), `record` (L22).

### `tests/validate.py`

Original member: `NSS_NBR02_SH02_Execution_v0.1/tests/validate.py`. SHA-256: `e114459d3797db8e1ccd4eba2fb4fbb3b692614d6e7275c5e2a2b82651695fcd`.

Source-defined function locations: `check` (L13), `cmp` (L21), `expected` (L25), `graph_features` (L31), `numerical` (L46), `full_gradient` (L66), `cache_test` (L79), `degenerate_graph` (L86), `noninterference` (L93), `shape_trace` (L100), `__torch_dispatch__` (L104), `visit` (L106), `faults` (L118), `mut` (L135).

The original member inventory (`indexes/SH02_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

## SC01

34 checks plus 12 pipeline preflights; exact closure, scope/revision/receipt lifecycle, restart and budget deferral. Main: 324 conditions.

Prospective protocol: `sources/SC01/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/SC01/README.md`.

### `scripts/audit.py`

Original member: `NSS_NBR02_SC01_Execution_v0.1/scripts/audit.py`. SHA-256: `2728c6cdcf6a3d0372379b3fd92796baa15c48080fbf4ecec15ea1090a411227`.

Source-defined function locations: `main` (L8).

### `tests/pipeline_preflight.py`

Original member: `NSS_NBR02_SC01_Execution_v0.1/tests/pipeline_preflight.py`. SHA-256: `4ed736d9ede966109c4d687021631ed8cf36f00572e07390e63d06543818d906`.

Source-defined function locations: `main` (L8).

### `tests/preflight.py`

Original member: `NSS_NBR02_SC01_Execution_v0.1/tests/preflight.py`. SHA-256: `21ae46dd35d6f4459072db7a2a2cc2730e50b51f8d52007cc7d28eb6fbec2052`.

Source-defined function locations: `main` (L10), `check` (L12), `requires_fault` (L17), `fn` (L25), `fn` (L39), `lifecycle` (L45), `pressure` (L58), `corrupt` (L64), `event_gap` (L74), `missing_edge` (L78), `nonfinite` (L81), `isolation` (L85), `deps_revision` (L91).

The original member inventory (`indexes/SC01_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

## SC02

34 checks; incremental publisher identity, invalidation/eviction, changed parameters, snapshots and insufficient budgets. Main: 720 conditions.

Prospective protocol: `sources/SC02/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/SC02/README.md`.

### `postrun/audit.py`

Original member: `NSS_NBR02_SC02_Execution_v0.1/postrun/audit.py`. SHA-256: `523b2d97c10a2068758bcecc733ae6805cae2a33de6701478d0b436f5883ab0a`.

Source-defined function locations: `recount` (L8), `replay` (L52), `snapshots` (L67).

### `tests/preflight.py`

Original member: `NSS_NBR02_SC02_Execution_v0.1/tests/preflight.py`. SHA-256: `d84655b8f271756ea97251ca3168bc10059d72b057f766207587af522ba9aef0`.

Source-defined function locations: `check` (L13), `fault` (L17), `equal_store` (L22), `publisher` (L28), `live` (L41), `baddep` (L67), `corrupt` (L78), `eventgap` (L85), `modelmutation` (L90), `replacement` (L95), `stale_intermediate` (L100), `stale_signature` (L110), `sizecontrol` (L116), `isolated` (L122), `nan` (L128).

### `tests/smoke.py`

Original member: `NSS_NBR02_SC02_Execution_v0.1/tests/smoke.py`. SHA-256: `4636702ecff400c0b1a83e012f39da194af4fe05096c19d0cd49852f708230b6`.

Source-defined function locations: none; module-level script.

The original member inventory (`indexes/SC02_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

## CAP01

29 preflight cases; complete versus streamed outputs, partial-attention resume and invalid-input/fault controls. Main: 488 cases.

Prospective protocol: `sources/CAP01/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/CAP01/README.md`.

### `scripts/audit.py`

Original member: `NSS_NBR02_CAP01_Execution_v0.1/scripts/audit.py`. SHA-256: `23af02ec5bb969cd58c3684056e36eeb6af536c73d29e56393197eb927369e9d`.

Source-defined function locations: `model` (L9), `recount` (L12), `replay` (L54), `resume` (L67).

### `tests/preflight.py`

Original member: `NSS_NBR02_CAP01_Execution_v0.1/tests/preflight.py`. SHA-256: `e2bdc86504d3bd9e9331f0aa3d14560163dfa8f16d03d95d116a1041429dadc3`.

Source-defined function locations: `run` (L10), `fails` (L40).

The original member inventory (`indexes/CAP01_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

## CAP02

12 checks; compiler identity, packed/reference gradients, independent targets, optimizer resume/isolation, faults and schedule counts. Main: 12 continuations, 18 endpoints; 12 selected stream checks.

Prospective protocol: `sources/CAP02/PROTOCOL.md`. Original runtime/reproduction instructions: `sources/CAP02/README.md`.

### `audit/recount_and_replay.py`

Original member: `NSS_NBR02_CAP02_Execution_v0.1/audit/recount_and_replay.py`. SHA-256: `e3e4224aef92b9d88f968cd35a54ca43582eddfb728b58782dbe76c19812c53d`.

Source-defined function locations: `label` (L12), `metrics` (L16).

The original member inventory (`indexes/CAP02_members.json`) also covers all runner, fixture, source, result, checkpoint, and failure files. Historical operational completion drivers are not general alternate protocols.

