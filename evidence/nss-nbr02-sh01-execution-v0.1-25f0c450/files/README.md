# NSS SH01 — runnable first maintenance prototype

Read REPORT.md first. This is a typed-record research prototype, not a language model or an
installed NSS companion. Three paired comparisons completed; a fourth HSA fit is incomplete.
Both positive results and runtime disadvantages are retained.

## Demonstrate the saved reader

Python3.13.5, PyTorch2.10.0+cpu, NumPy2.3.5 were used. With compatible dependencies installed,
run from the extracted archive directory:

```bash
python source/demo.py
python source/demo.py --reader dense
python source/demo.py --reader hsa --packet examples/packet.json --output my_output.json
```

The demo reads an existing checkpoint and emits advisory JSON. It performs no training or
external action. Do not load untrusted PyTorch checkpoint files. Example output includes
source and model identities. Digests verify integrity, not authenticity or permissions.

## Components

- source/store.py: VersionedStore, Manager, explicit record proof and restart.
- source/common.py: typed features, dense/HSA reader, gather and masked references.
- source/preflight.py: lifecycle faults, math/gradient and isolation tests.
- source/run.py: original prospective training/scoring runner.
- source/complete_retained.py: one-use operational recovery of untouched8804 fits.
- source/post_retained.py: all available final comparisons, timing, independent recount/replay.
- source/demo.py: fixed JSON maintenance output interface.
- source/diagnostics.py: retained-result analysis; no new neural inference.

## Reproduction without overwriting evidence

Never run the training/audit scripts in the only copy of this evidence archive: they write
relative to their parent directory. Copy source/ and PROTOCOL.md into a NEW experiment folder,
create fixtures/,results/,checkpoints/,failures/, then use the original run.py after reviewing
its resource settings. Its output SOURCE_LOCK will be a new lock. Do not run complete_retained.py
for a fresh complete experiment; it is specific to the retained interruption and refuses existing
8804 checkpoints. No automatic tool timeout or supervised process wrapper is included; a durable
per-step journal and signal-safe interruption handling remain an identified engineering gap.

Exact same-framework bitwise reproducibility is not promised across different library/hardware
versions. The numerical envelopes in PROTOCOL.md apply to this prospective experiment only.

## Important boundaries

The policy can be solved exactly in ordinary software. HSA was given explicit dependency-based
edges; it did not discover dependencies. The manager uses fixed exact lookup, not learned RAG.
Summaries are typed metadata, not generated prose. There is no language-token budget measurement,
no DARP, and no full overnight learning/repair cycle. Logical score counts are not peak-memory
measurements. The sparse gather kernel is currently slower than dense SDPA at the tested sizes.
