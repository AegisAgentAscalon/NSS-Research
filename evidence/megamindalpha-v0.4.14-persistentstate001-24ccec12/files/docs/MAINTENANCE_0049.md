# Maintenance report — v0.4.9

## Rule
Remove stale constraints and duplicate mechanics, not unique failure coverage. Fewer
lines and more tests are neither performance proofs nor quality scores. This pass adds
a real bounded generation catalogue, so overall code volume rises while repeated tooling
is reduced. No runtime speedup or energy saving was measured.

## Removed or consolidated
| Change | Reason / replacement | Coverage retained |
|---|---|---|
| Five `generate_*_logic_docs.py` scripts | Repeated entry/Mermaid/DOT generation consolidated in `tools/logic_views.py` and `tools/generate_subsystem_logic.py`, configured by `spec/logic_documents.json` | Deterministic regeneration gate across all current helper schemas/graphs and affected parent docs |
| `tools/update_review_doc.py` | One-off v0.4.1 Word converter addressed fixed paragraph indices and could replace a historical report with current content | Historical outputs/archives untouched; current editable JSON/Markdown/DOT/SVG/PNG remain supported |
| `test_inherited_python_code_and_tests_are_preserved_exactly` | Permanently locking every old file byte prevented legitimate repairs and shared-mechanics refactoring; not a behavior invariant | Original input manifests retained; current complete-file manifest, dependency rules, immutable *model artifact* tests, full regression suite |
| Permission SQLite mechanics | Extracted to bounded `EventJournal`; permission and generation stores retain separate file, schema, policy and reducers | Existing permission tests including process crashes run against the shared mechanics |
| SQLite fixture resource leak | Added explicit connection close in `test_stagehandoff001`; transaction context alone did not close the connection | Same corruption scenarios/assertions retained |
| Direct-file Atlas import | Root path setup now works from another current directory | Explicit external-cwd CLI test |
| Stale package description | Removed obsolete claim that this package has no neural execution | Description now says bounded neural laboratory, not production authority |

## Measured physical Python lines (includes comments; excludes generated docs/assets)
| Area | Baseline | v0.4.9 | Net |
|---|---:|---:|---:|
| `nss_base` | 7,022 | 7,919 | +897 |
| `tests` | 4,889 | 5,454 | +565 |
| `tools` | 1,011 | 912 | -99 |

The tools directory is smaller despite gaining generation-schema export and a static
retired-tool check. Tests remain a substantial portion of the repository because
state/permission/crash behavior is substantive functionality; no arbitrary test-line
quota was imposed. New mutation/crash cases share fixtures and bodies where practical.

## Deliberately retained
Legacy Recovery001A/001B tests still exercise supported recovery behavior. Historical
neural records and the original strict-MSE advisory are not obsolete merely because
a later run is correct. Existing snapshots/manifests and audit files remain byte-identical.
Generated schemas/diagrams are documentation views, not independently edited logic.

## Cleanup boundary
This was a focused audit of changed/reused paths and current tooling references, not
a repository-wide proof of dead-code absence. `tools/audit_maintenance.py` checks
specific retired commands/assertions and reports size; it is not a semantic reachability
analyzer. Future cleanup must name each retired behavior and identify its replacement
or explicitly retire the public feature. Do not create tests requiring ordinary source
files to remain forever unchanged to this release.
