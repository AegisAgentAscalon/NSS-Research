# NSS Base Build Out — Recovery 001A/001B + Logic Atlas 001

Version **0.4.1-logicatlas001-corrected** corrects Logic Atlas 001 and several Recovery 001B resume/publication boundaries. See [review corrections](docs/REVIEW_CORRECTIONS.md). The atlas remains specification/test infrastructure; it does not implement planned neural, cognition, multimodal, training, or governance subsystems.

The purpose of this pass is anti-spaghetti implementation planning. `spec/logic_atlas.json` defines 25 build-level flows with typed boundaries, state nodes, transitions, typed failure outcomes, forbidden edges, invariants, compact pseudocode, shared primitives, and structural complexity metrics. `nss_base/logic_atlas.py` validates that specification graph before implementation code is written.

## Run

Python 3.10 or newer, from this extracted folder:

```console
python -m unittest discover -s tests -v
python -m nss_base.experiment001a
python -m nss_base.experiment001b
python -m nss_base.logic_atlas
```

The demos use temporary local SQLite stores and remove them afterward. Tests launch child processes that deliberately exit with code 73 to model action and recovery-publication crash windows. No packages, network, credentials, GPU, or model weights are needed.

001A expected result: AB computes `[-4, 14, 26, 80]`; recovered A and clean A both compute `[-11, 7, 19, 73]`; one mock effect remains committed despite restart/replay.

001B expected result: the AB checkpoint stays current through PREPARED/STAGED recovery states, the rebuilt A checkpoint is published atomically only after staging, recovered A exactly equals a clean A execution, and the task's committed mock action remains a single effect.

## Read first

- [Next instructions](NEXT_STEPS.md)
- [Implemented contracts and limitations](docs/BASE_CONTRACTS.md)
- [Progress](docs/PROGRESS.md)
- [Test audit](docs/TEST_AUDIT.md)
- [Editable recovery flowcharts](docs/FLOWCHARTS.md)
- [Pseudocode flowchart atlas](docs/PSEUDOCODE_FLOWCHART_ATLAS.md)
- [Logic compression guide](docs/LOGIC_COMPRESSION_GUIDE.md)
- [Implementation packet template](docs/IMPLEMENTATION_PACKET_TEMPLATE.md)
- [Logic atlas metrics](docs/LOGIC_ATLAS_METRICS.md)
- [Earlier corrections](docs/CORRECTIONS.md)

## Included

`schemas/` now contains ten JSON Schemas, including the 001B recovery-attempt record. `fixtures/recovery001a/` remains the deterministic hashed Core/A/B/input fixture used by both experiments. `nss_base/serialization.py` validates only the subset of JSON Schema keywords used here; it is not a general JSON Schema engine.

`artifacts.py`, `recovery.py`, and `ledger.py` implement the 001A path. `publication.py` adds the 001B durable single-runner publication store. `runtime.py` and `demo.py` retain the original in-memory v0.1 simulator for regression coverage; its order-sensitive configuration identity/reuse semantics were corrected during the 001B audit.


## Logic Atlas 001

The Logic Atlas deliberately separates **specification compression** from implementation compression. Repeated mechanics may eventually collapse into shared code, but no decision, failure state, invariant, or rollback meaning may be deleted merely to reduce line count.

The JSON atlas is validated for: unique flow/node IDs, one start node per flow, reachable nodes, valid decision exits, typed terminal outcomes, known shared primitives, known failure codes, strict malformed-input rejection, complete terminal mappings, terminal exit reachability, unambiguous edge labels, and absence of outgoing edges from terminal states. Schema v2 maps each terminal to a list of allowed outcomes and labels each flow with its implementation status. These are structural specification checks, not proof that future implementations obey the flows.

## Evidence limits

These experiments prove deterministic integer replay and tested local process-crash behavior under a single-runner mock protocol. 001B additionally proves, within this simulator, that a rebuilt checkpoint can be staged durably while the source remains current, and that target publication plus the attempt's PUBLISHED state occur in one SQLite transaction.

They do **not** prove neural compatibility, model quality, identity continuity, device loading, real Nexus authorization, multi-runner concurrency, power-loss recovery on arbitrary filesystems/hardware, hostile-input sandboxing, or exactly-once behavior for arbitrary external systems. Qualification references still name tests; they are not signed certificates.

## ZIP handoff

The versioned ZIP includes source, schemas, fixtures, tests, docs, and the original R2 reference pack. It excludes Git internals, caches, temporary databases, and generated test state. Upload it to Chat and direct the next reviewer to `NEXT_STEPS.md`, `docs/PROGRESS.md`, and `docs/TEST_AUDIT.md`.

## Regenerate review views

Run `python tools/generate_logic_docs.py` for Markdown, and `python tools/render_logic_flowcharts.py` with Graphviz `dot` on PATH for DOT/PNG. A Node fallback accepts `--node` and `--node-modules` and needs `@viz-js/viz` plus `sharp`. `python tools/update_review_doc.py` needs `python-docx` and Pillow and updates the preserved v0.1 Word template from current atlas/PNGs. These optional authoring dependencies are not required to run tests or demos. Regenerated DOCX files require visual review.
