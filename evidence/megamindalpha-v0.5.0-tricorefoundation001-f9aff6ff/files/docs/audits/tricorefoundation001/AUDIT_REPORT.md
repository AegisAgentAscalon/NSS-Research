# TriCoreFoundation001 — scoped implementation audit

**MegaMind Alpha v0.5.0 · 20 September 2026**  
**Result: the overlay-independent foundation is implemented and its selected checks pass. This is not a qualified four-neural-model companion or a completed NBR study.**

## 1. What was built

The new current-role path is executable through `python -m nss_base`. It has explicit component revisions, Primary generation, state/exchange/context versions and scope rather than activation profiles or fabricated empty overlays. It reuses the existing `Generations` journal and shared reviewed TaskRecord update, exact-source reader, purpose-aware experience archive and context selection logic. It does not introduce a second current-task database.

The runner performs real calls to installed deterministic test adapters: Primary before and after every bounded auxiliary step; Secondary and Tertiary share the exclusive slot, including the Secondary candidate-step phase. The Primary-only path requires no auxiliaries. Validator advice is data received by the Primary, not a permission check or output veto. Tertiary-generated messages remain hypothetical. These are software contracts tested using explicitly non-neural adapters.

Atomic complete-tick publication records component state, messages, call receipts and output together. Interrupted ticks preserve the last completed checkpoint and require explicit recovery. Live workers are protected from concurrent execution/recovery by an OS cooperative lock. Completed retries return receipts without rerunning calls or redisclosing the prior output. Candidate state remains separate from serving state. See [`../../TRICORE_FOUNDATION_001.md`](../../TRICORE_FOUNDATION_001.md) for the implementation map and exact boundaries.

## 2. Source identity and preservation

This is a cumulative branch from **v0.4.14 PersistentState001**, not v0.4.17. None of the missing intermediate changes or later standalone studies has been invented or merged.

The supplied recovery ZIP remains **28,327,938 bytes** with SHA-256:

```text
24ccec12a0513e3e60cdba49df54f25db476786b2b0770bb4a628017d9c0736a
```

Its CRC check passes, and all **903 extracted original files** still match their pre-work hashes. The new checkout retains every original relative file path; 13 existing files were deliberately changed plus the separately regenerated release manifest. Original root guidance and manifest are retained in `docs/history/`. The original ZIP is not embedded again inside the new ZIP. Extract the new checkout alongside the recovered one, not on top of it.

`ORIGINAL_PRESERVATION.json`, `INPUT_ARTIFACTS.json`, `SOURCE_CHANGES.json` and `CHANGED_EXISTING_FILES.patch` record these distinctions. The new root `MANIFEST.sha256` covers all packaged files except itself. Integrity hashes are not signatures or proof of trusted authorship.

## 3. Fresh tests against the final implementation

| Suite | Distinct tests | Final outcome |
|---|---:|---|
| New current-role contracts, context/archive, scheduling, crash/recovery and boundaries | 68 | PASS |
| Recovered persistent state and its recovery paths | 48 | PASS |
| Recovered context tests | 58 | PASS |
| Recovered experience/archive tests | 82 | PASS |
| Recovered tiny neural backend | 30 | PASS |
| Recovered runtime-contract simulator | 13 | PASS |
| **Total selected unit/regression tests** | **299** | **PASS** |

The final command set also passed dependency-DAG validation, compilation, the foundation lifecycle demonstration, NBR-01 preflight generation, the 24-case engineered harness smoke check and capability reporting: **12 commands total**. Preflight success means it accurately reports missing controls; it does not mean the study is runnable or completed.

Commands, exit codes, durations and log hashes are in `CHECK_RESULTS.json`. Source, schemas, specs, tests and tools were hashed before the final command set in `TESTED_INPUTS_SHA256.json`; `TESTED_INPUT_PRESERVATION.json` confirms those inputs were unchanged during it. Final evidence logs are `logs/final_*.txt`. Development logs are retained separately and must not be substituted for final checks or added to the test count.

The selected historical numerical tests exercise inherited numerical fixtures. This release does **not** count them as new tri-core neural training. The legacy runtime suite tests the legacy contract simulator, not the separate generic Aegis Runtime product.

**Not rerun:** the full historical 1,111-test suite, all 27 old required release gates, every historical demo, full old candidate/adoption workflows, or production qualification. Passing 299 selected tests is not a claim that every inherited overlay-era tool is compatible with the new format.

## 4. Demonstrated lifecycle

The final demo ran with site packages disabled and assertions optimized out (`python -S -O`), so acceptance checks do not depend on Python `assert` statements. It used a new isolated local evidence/store directory and five phases: Primary-only, task, test candidate step, reflection and verification.

Measured outputs:

- Five committed ticks; ten Primary calls, two Secondary calls, one Tertiary call and one Validator call.
- Three symbolic-state revisions including initial admission; exact reconstruction after reopening the store.
- Unreviewed state update refused; stale context refused; candidate and serving checkpoints distinct.
- A deliberately wrong Validator message did not override the exact supported result; Tertiary output remained hypothetical.
- Serving test-parameter dictionaries unchanged; **zero new parameter updates**, zero external actions, Forge and Runtime unconnected.

`DEMO_RESULT.json` includes the call receipts and corresponding input/output/parameter hashes. The English/Japanese exact fixture is a byte-preservation example, not English/Japanese language competence.

Real process-exit tests cover reservation, Primary completion, Secondary candidate-step completion, precommit and postcommit boundaries. Separate processes/threads tested live lock contention and recovery refusal while a worker holds the slot. Neither this test adapter nor its candidate-step counter is a learned recurrent component or a real optimizer checkpoint.

## 5. NBR-01 status

`spec/nbr01_protocol.json` and `python -m nss_base research --preflight` expose the proposed state-off/on × internal-depth 1/2/4/8 experiment and required controls. `NBR01_PREFLIGHT.json` reports **BLOCKED_FOR_FULL_NBR01**: a competent task-matched Transformer control, trained recurrent candidate, measured target-device budget and pilot-selected confirmatory criteria are missing.

The supplied `ClockEstimator` is a **hand-engineered control for testing the harness**, with zero learned parameters. Its 24 cases check event/depth separation, three delays, reset and restart. Eight raw numerical bytes exclude serialized metadata, runtime objects and temporary computation. `NBR01_HARNESS_SMOKE.json` explicitly marks the study **NOT_RUN**. This is not a memory-efficiency benchmark, low-bit trace study, learned-refinement result or model comparison.

The next real study should establish competent task-matched controls, then vary temporal state and internal depth with evaluation-time learning fixed. Missing full-product Forge/Runtime integration does not by itself prohibit a separately labelled isolated study. It does prohibit describing that study as integrated companion learning.

## 6. Corrections made during development

An early integrated demo fixture used an invalid legacy stage enumeration (`analysis`); it was corrected to the schema-supported `WORK`. More importantly, the first 82-test legacy experience run caught a real circular import introduced by the new mixin plus imports absent from the strict dependency inventory. The creation dispatcher was moved into its owning generation module, the cycle was removed, and the explicit dependency allowlist was reviewed and updated. The dependency checker and its cycle rules were **not weakened**. The corrected 82-test suite and then the entire final selected check set passed. The initial failure and corrected logs remain in this package.

## 7. Remaining boundaries and risks

This is trusted local, cooperative execution. The lock is not an adversarial sandbox; callbacks are not forcibly interrupted. Overlong work is rejected after return, so hard time/memory preemption, loading/residency accounting and continuous Primary cadence need actual backend and independent Runtime integration. No claim is made that computation continues while paused or powered off.

All active adapters in this release are admitted as `TEST_ADAPTERS_ONLY`. Their pinned parameter dictionaries demonstrate the freeze checks, not a practical freeze proof for large neural weights. Token exchange requires a matching ABI; native latent alignment and internal refinement are explicitly unsupported rather than silently emulated. There is no real language Primary, broad adaptive Secondary, trained world-model Tertiary or competent language Validator in the new path.

Configuration switching/rollback is executable only with a **structural test attestation**, independent local declarations and no open work. It is not a replacement for independent neural qualification. Live legacy-store migration, actual generation succession, companion-contributed continuity criteria, catch-up windows and backend-qualified hidden-state migration remain required product work.

Evidence permissions are checked at admission/use and again after callbacks. These are point-in-time checks across separate owners, not atomic cross-store authorization leases or proof of neural prompt-injection immunity. Generated content has no authority to grant permissions or become observed memory through the exchange API. Direct hostile file/database modification is outside the cooperative contract.

Generic Forge and independent Runtime ports return **NOT_CONNECTED**. No model download, cloud training, repository merge, remote write or deployment occurred. Delayed-credit algorithms, native packed low-bit traces, DARP and native HSA/MSA remain research work. NBR-00 remains partial overall, the product language/memory G02 baseline remains unestablished, and full NBR-01–07 studies remain NOT_RUN.

Execution environment: Linux x86_64 / Python 3.13.5 in this workspace, **not the user's device**. Windows convenience launchers and the Windows lock branch are provided but were not executed here. A fresh extracted-package check is recorded in the adjacent delivery-verification JSON, outside the checksum-closed ZIP.

## 8. Decision

**Keep this foundation as the current implementation branch and proceed to the first actual NBR-01 pilot.** Its purpose is to let replaceable neural candidates use explicit state/context/lifecycle contracts without depending on overlays. This release settles neither the neural backbone nor the learning rule, and it does not convert test-adapter names into claims of cognition.
