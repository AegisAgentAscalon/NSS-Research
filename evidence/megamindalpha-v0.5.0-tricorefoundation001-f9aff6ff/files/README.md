# MegaMind Alpha v0.5.0 — TriCoreFoundation001

**Neural Space Systems / Tri-Core Validator NSS xTREME**  
**Current-role framework release; deterministic test adapters, not four trained models.**

This is a **complete cumulative source checkout branched directly from the recovered v0.4.14 PersistentState001**. It does not reconstruct the unavailable v0.4.15–v0.4.17 changes or merge later standalone studies. The original ZIP is the recovery reference; extract this release into a separate directory rather than overwriting it.

## Current active path

The default `python -m nss_base` path has **no neural overlays, activation profiles or dummy empty-overlay configurations**. It uses explicit Primary/Secondary/Tertiary/Validator component revisions, a Primary generation, scope, context/exchange versions and state compatibility.

The recovered legacy path remains in the cumulative tree as a historical control. Its old documentation, reports, diagrams and overlay-oriented demos do not define the new architecture. See `docs/history/v0.4.14_*` for original root documents and the original file-hash inventory.

### Run from this extracted directory

The new foundation and its tests use the Python standard library. They were also run with `python -S` (site packages disabled). The optional legacy numerical tests still require the separately listed historical neural dependencies; nothing installs them automatically.

On Windows, use **`RUN_FOUNDATION_CHECKS.cmd`**, **`RUN_FOUNDATION_DEMO.cmd`**, or **`RUN_NBR01_PREFLIGHT.cmd`**. The demo launcher creates a unique sibling `NSS_Run_Output` directory; it does not overwrite an existing run. Windows launcher execution and the Windows OS-lock branch have not been exercised on the user's machine.

Equivalent commands, from the extracted root:

```text
python -m nss_base capabilities
python -m unittest discover -s tests -p "test_foundation*.py" -v
python -m nss_base demo --output ../NSS_Run_Output/my-first-foundation-demo
python -m nss_base research --preflight
python -m nss_base research --harness-smoke
python tools/check_dependencies.py
python tools/verify_manifest.py
```

The demo output directory must be new or empty. Run-output files belong outside the release tree so its exact checksum manifest remains valid. Source execution was tested on Linux / Python 3.13.5, not on a target companion device. Other Python versions/platforms need their own checks.

## What is implemented

**One durable owner.** `Generations` remains the task/state/generation-journal owner (`generations.sqlite3`). A new explicit store format adds current-role configuration, scoped tasks, component checkpoints, candidate-job state, tick reservations and recovery. It is not a parallel current-task database. Existing reviewed TaskRecord changes, immutable source readers and context selection are reused.

**Current-role execution.** A bounded tick invokes the Primary, the phase-specific auxiliary when present, and the Primary again. Secondary inference and candidate-step work share the same exclusive worker slot as Tertiary execution. OS-level cooperative locking also prevents another live worker from recovering or stealing that slot. The Primary-only path works with every auxiliary absent. This is bounded local execution, not an always-running multi-model daemon.

**Versioned exchange and state.** Scope, exact configuration, component revision, codec, representation, event cutoff and state revision are checked. Generated output cannot claim the `observed` exchange kind. The initial Tertiary exchange remains hypothetical; Validator output is advice, not permission or release authority. Exact source references remain distinct from generated text.

**Freeze and recovery checks.** Adapters are checked against their pinned serving-parameter digest before/after execution. State and output commit atomically after the tick. A crash leaves a durable pending reservation and the last committed state; explicit recovery is required after the worker has exited. A committed retry returns a receipt without rerunning callbacks or redisclosing a cached answer. No external action is replayed.

**Actual use of existing context/evidence.** Current-role context v3 uses the existing selector, exact-source reader and purpose-aware `ExperienceArchive`. Current source permissions are rechecked after callbacks. Stale packets, wrong scope, changed sources and mandatory-context overflow are rejected. These are point-in-time local checks, not cross-store atomic permission leases or proof of neural prompt-injection immunity.

**Research entry point.** NBR-01 has a checked protocol, preflight reporting and 24 hand-engineered event/depth/reset/restore harness cases. No trained recurrent or Transformer comparison has run. The eight raw numerical bytes in the diagnostic estimator exclude its JSON metadata and are not a neural learning-memory result.

## What is not implemented or qualified

There are no competent English/Japanese neural roles, native latent recurrence, delayed-credit learner, packed low-bit eligibility arrays, trained latent bridges, DARP decoder or native HSA/MSA kernels in this new path. The test adapters are explicitly non-neural; their candidate-step counter performs **zero parameter updates**. They test integration, not cognition.

Generic Forge and independent Runtime are **NOT_CONNECTED**. Their ports return explicit unsupported results rather than inventing training, hard preemption, target-device budgets, permits or deployment authority. Long-running model/training jobs must be integrated through those systems, not smuggled into a synchronous test callback.

Whole-test-configuration switching and rollback are executable with independent local declarations and quiescence checks. Their qualification scope is **structural test attestation**, not real-model qualification. The existing historical `Qualifications`, `LearningCycles` and dataset owners remain intact, but their overlay-era orchestration has not all been migrated. No accepted production generation or real companion state is silently upgraded.

## Evidence and next step

Read **`docs/TRICORE_FOUNDATION_001.md`** for the implementation map and boundaries, and **`docs/audits/tricorefoundation001/AUDIT_REPORT.md`** for the exact fresh checks, failures corrected during development, input hashes and limitations.

The next bounded research work is an NBR-01 pilot with a competent task-matched Transformer-with-memory control, an explicit estimator and a trained recurrent candidate, holding evaluation-time learning fixed while varying state and internal depth separately. A missing product integration does not prohibit an explicitly isolated mechanism study; it does prohibit claiming that such a study already supplies a deployed companion.
