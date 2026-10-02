# C00-CONTRACT01: ordinary review/ledger foundation

Start with REPORT.md. Everything is synthetic engineering evidence, clearly separated
from learned-model research. No restoration or large historical model archive is needed.

Verify exact delivered bytes:

    python VERIFY_STUDY.py

Recompute the independent scalar/boolean scores from saved public inputs and raw outputs:

    python RESCORE.py --out /path/to/new_score_directory

Run a separately requested reproduction of the deterministic contract harness:

    python source/REPRODUCE.py --out /path/to/new_run_directory

The latter actually executes fault-injection subprocesses which deliberately terminate
with recorded codes73/74 and writes only under the supplied new run directory. It does
not train/load models or call the network. Do not point it at an existing evidence directory.
All Python is standard-library only. Original verification used Python3.13.5/Linux.
Timing and RSS are not expected to be byte-identical across runs or platforms.

Folders:
- protocol/: frozen specification, scope and source lock.
- source/: rule, synthetic builder, append log, independent evaluator and drivers.
- inputs/: full synthetic primary/replay cases, including evaluator-only scope probe.
- raw/: primary/replay rule outputs, journals, deliberate corrupt copies and lifecycle states.
- results/: every expected/actual decision, reasons, non-adopted cases, control counts.
- audit/: environment, actual stage receipts and deterministic comparison hashes.
- program/: original roadmap/contract and unchanged research questions, plus current addendum.

Full study data is provided without lossless aliases or hidden dependencies.
