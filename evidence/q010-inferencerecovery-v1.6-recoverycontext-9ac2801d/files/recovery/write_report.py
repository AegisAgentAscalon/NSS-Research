from pathlib import Path
import json,csv,hashlib,datetime
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    a=read(R/'results/analysis/STUDY_RESULT.json');e=read(R/'results/EXECUTION_COMPLETE.json');tests=read(R/'audit/RECOVERY_TESTS.json');env=read(R/'audit/ENVIRONMENT.json');meta=list(csv.DictReader((R/'results/analysis/METRICS_ALL_SEEDS_AND_POOLED.csv').open()))
    roles=['ordinary','near','attention'];names={'ordinary':'Ordinary continuation','near':'Close-identity continuation','attention':'Task-adapted attention'}
    def rate(role,condition,cls,cp=''):
        rows=[r for r in meta if r['seed']=='pooled' and r['role']==role and r['condition']==condition and r['evidence_class']==cls and r['checkpoint']==cp]
        assert len(rows)==1,(role,condition,cls,cp,len(rows));x=rows[0];return f"{100*float(x['accuracy']):.2f}% ({x['correct']}/{x['total']})"
    table='| Candidate | Pooled frozen gates | Every seed passes | Checks per seed |\n|---|---:|---:|---:|\n'
    for c in a['candidates']:table+=f"| {names[c['role']]} | {'PASS' if c['pooled_gate_pass'] else 'FAIL'} | {sum(x['passed'] for x in c['per_seed'])}/5 | {c['per_seed'][0]['checks']} |\n"
    specs=[('State removed: supported','ablation_state_off','supported',''),('Erased values: supported','corruption_erased_values','supported',''),('Wrong-but-valid values: supported','corruption_wrong_but_valid','supported',''),('No maintenance, event 1,024: supported','durability_sigma02_no_maintenance_livewrite64','supported','1024'),('Close source: supported','stress_close_source_sigma001','supported',''),('Ordinary novel query: UNKNOWN','stress_ordinary_novel','preexisting_unknown',''),('Near-collision novel query: UNKNOWN','stress_near_collision_novel_sigma001','preexisting_unknown','')]
    negative='| Diagnostic (pooled five seeds) | Ordinary | Close-identity | Attention |\n|---|---:|---:|---:|\n'
    for title,cond,cls,cp in specs:negative+='| '+title+' | '+' | '.join(rate(role,cond,cls,cp) for role in roles)+' |\n'
    peak=max(x['sampled_peak_process_tree_rss_bytes'] for x in e['worker_receipts']);times={p:read(R/f'results/PHASE_{p.upper()}.json')['wall_seconds'] for p in ['capture','score','replay','compare']}
    report=f'''# Q010 Inference Recovery v1.6

**24 September 2026 — completed inference evaluation recovery, with explicit historical training-evidence gaps.**

## Decision

The requested recovery sequence completed: shell/Python execution, original-protocol binding of all fifteen saved main exports, one end-to-end integration fixture, all 64 conditions across all five seed pairs, independent source/ledger/arithmetic/decoder scoring, and a fresh full model/state replay with exact array and metadata comparison. **No main model was retrained. No optimizer update was executed.**

This closes the inference/evaluation recovery work. It does **not** retrospectively satisfy the missing training-checkpoint, raw-training-trace, or training-reproduction obligations of the original full protocol. The machine-readable result deliberately sets `original_training_protocol_fully_requalified=false`.

## 1. Identity and unchanged contract

The binding is to `NSS_NBR01_Q010_Reconstruction_v1.4`, not to the later execution-validation fixture protocol. The original frozen protocol SHA256 is `{a['original_protocol_sha256']}`. All 15 exports match their raw-file hashes, dtype-inclusive tensor digests, public parameter fingerprints, declared architectures, paired seeds, recorded main-fit roles, and recorded 6,000-update completion metadata. All original model/data/training-source hashes in their fit manifests match the supplied implementation. The loader checks the originally declared training seed domains but never derives new training seeds or starts a trainer.

Main seeds are 1201–1205, paired with inherited checkpoints 801–805. Each seed has six readers: inherited, cap-only, ordinary continuation, close-identity continuation, task-adapted attention, and the privileged exact-owner control. The compact learned reader has 818 parameters; the reconstructed attention reader has 86,464 parameters. These are the surviving reconstructed models, not the lost earlier Qualification010 attention checkpoint.

The recovered criteria file is byte-identical to its retained historical digest, `{a['criteria_sha256']}`. The rules remain 0.90 for applicable core classes, 0.95 for direct visible-fact classes, and 0.90 at every declared cadence-8 durability checkpoint. No threshold was fitted to regenerated outcomes.

Evidence: `audit/SAVED15_CURRENT.json`, `protocol/ORIGINAL_FROZEN_PROTOCOL.json`, `protocol/ORIGINAL_CHECKPOINT_ROSTER_LOCK.json`, `audit/CRITERIA_RECOVERY.json`, and `protocol/RECOVERY_SOURCE_LOCK.json`.

## 2. Measured execution and verification

| Check | Result |
|---|---:|
| Main exports bound and loaded |15/15|
| New optimizer updates |0|
| Integration fixture |64 conditions; 129 frames; 2,880 query chains; 19,104 logical stages|
| Main condition–seed pairs |320|
| Main reader–condition–seed combinations |1,920|
| Main captured frames |645|
| Main query chains independently scored |{a['query_chains']:,}|
| Logical reader stages independently audited |{a['logical_stage_audits']:,}|
| Fresh-replay arrays compared exactly |{a['replay_arrays_exact']:,}|
| Fresh-replay array elements compared exactly |{a['replay_elements_exact']:,}|
| Declared condition/class coverage checks |{a['coverage_class_checks']:,}|
| Declared checkpoint/class coverage checks |{a['checkpoint_class_checks']:,}|
| New named loader/underflow checks |{tests['checks']} passed|
| Unchanged regression assertions on the fresh fixture |23 passed; 0 failed; 0 skipped|

The integration fixture used saved main seed 1201 readers on an explicitly marked development split, four cases per ordinary condition, and the complete declared lifecycle and 1,024-event horizons. It was independently scored and replayed before the main phase. Its queries are not counted as main observations.

Main captures preserve every allowed depth, fault, lifecycle phase, and durability prefix. Main evaluation used 128 cases per non-lifecycle condition, including both declared support strata; lifecycle phases use their declared single case. Durability checkpoints remain 0 through 1,024 in 64-event increments where declared, and the separate no-maintenance ablation retains its declared 0/1,024 grid.

The independent scorer imports no producer, model, or training implementation. It regenerates source catalogues and initial queries, reconstructs committed lifecycle facts, checks pointer arithmetic and decoding, and derives correctness from expected versus predicted answers rather than producer success flags. The separate replay reruns the full producer/model/state evolution in fresh processes and compares every saved array and every case/query/event metadata object. This is internal independent implementation plus exact local replay, **not third-party replication**.

All five newly generated score files {'match' if a['historical_score_digests_all_match'] else 'do not all match'} their retained historical score digests. This is an additional consistency comparison, not a substitute for raw evidence and not an acceptance target. See `results/analysis/HISTORICAL_SCORE_COMPARISON.json`.

## 3. Scientific gate outcomes

{table}

Both pooled outcomes and the stricter all-five-seed outcomes are published. Passing these narrow gates does not mean passing every diagnostic condition, demonstrating general intelligence, or qualifying an integrated NSS product.

### Negative and stress results are retained

{negative}

Every condition, reader, seed, checkpoint and evidence class is retained in `METRICS_ALL_SEEDS_AND_POOLED.csv`. The complete per-query dataset is in `ALL_QUERY_SCORES.csv`. **All {a['all_negative_queries_retained']:,} incorrect query outcomes** are also collected in `ALL_NEGATIVE_QUERY_RESULTS.csv`; this includes intentional insufficient-depth and state-removal negatives, not merely failed candidate gates.

Whole-map correctness is reported separately in `WHOLE_MAP_DIAGNOSTICS.csv`, with unique store/case observations rather than multiplying each store by the six readers. A correct answer must not be read as proof that the entire stored map is intact. Conditions with wrong-but-valid values, erased/shuffled values, novel identities, damaged state, and omitted maintenance are diagnostics, not removed outliers.

## 4. Underflow amendment, preserved rather than silently normalized away

The original local Float32/Float64 verifier does not pass unchanged. Its final probability error model lacks an absolute allowance at underflow. The retained amendment specifies adding `eta=2^-126` to the existing final softmax probability bound, with `u=2^-24`; the relative multipliers, scoring labels, task thresholds, exact CPU replay, decoder, and 1e-3 non-informative-normalization rejection remain unchanged.

The uploaded v1.5 package contains the amendment's rationale, but **not the historical rejected raw row or original v2 implementation**. This recovery therefore preserves the frozen verifier as `pointer_math_frozen.py` and reconstructs a separately hashed amended implementation directly from that rationale. It does not claim recovery of the absent original source or row.

Before integration/main rescoring, tests reproduced the frozen rejection on a newly constructed same-regime input, accepted that exact arithmetic under the documented bound, covered four batch layouts and four value scales plus 129 near-underflow logits, and rejected corrupted weights, weighted values and normalized outputs. A newly regenerated actual main 128-case batch also reproduces a frozen-verifier rejection at seed 1201, no-maintenance durability checkpoint 64, ordinary reader stage 0; the amended verifier accepts those unchanged bytes. Both the raw batch and rejection receipt are retained.

Evidence: `protocol/UNDERFLOW_AMENDMENT_ORIGINAL.md`, `audit/UNDERFLOW_RECONSTRUCTION.diff`, `audit/RECOVERY_TESTS.json`, and `audit/FRESH_MAIN_UNDERFLOW_REJECTION.*`. All main cases were scored with the amendment already pinned; none were excluded.

## 5. Historical gaps and failures that remain

**Full main optimizer/RNG checkpoints: 0 available.** Some stream RNG metadata and historical hashes remain in fit manifests, but they are not full joint checkpoints. These exports do not support exact training continuation. No optimizer state or missing RNG history was manufactured.

**Raw main numerical training traces: 0 available in the uploaded v1.5 delivery.** The retained v1.5 audit reports having checked 15 contiguous 6,000-row traces. The current delivery contains that audit and the fit manifests, but omits the raw `numeric_trace.npz` files. This pass therefore verifies the recorded completion metadata, not those absent trace arrays. The prior statement `full_checkpoint_retained=true` inside the historical export manifest refers to its original working study; it is not evidence that this upload contains those payloads.

**Fresh full training reproduction: not performed.** Prior training-reproduction and qualification JSONs remain labelled historical reports. This recovery must not be presented as proving every historical optimizer operation or restoring the entire original study's training audit trail.

**Three historical verifier errors remain preserved:** two byte-equality mismatches against old Windows-generated fixtures and one unavailable historical lifecycle fixture. Their original logs remain under `provenance/historical_verifier/` and in the unchanged v1.5 input ZIP. They were not skipped into passes or assigned looser tolerances. The 23 fresh regression tests are a separate, explicitly documented fixture run.

The standalone uploaded Q009 ZIP lacks a usable central directory and appears truncated. It is retained byte-for-byte, not silently repaired or used as a trusted complete archive. Required inherited checkpoints were already present and hash-verified in the valid v1.3 archive. Both usable input archives passed ZIP CRC and every manifest-covered hash: 10,525 members for v1.3 and 2,185 for v1.5.

Two new preflight driver issues are retained in `failures/`: the initial mistaken expectation that raw traces were present, and a test-harness exception-class mismatch between the frozen and amended verifier modules. Neither was a failed learned-model result. The fixes changed neither neural arithmetic nor scientific thresholds. A later ad hoc lock-inspection helper assumed the wrong JSON schema; its error is also logged, and the corrected inspection confirmed both numerical and analysis source locks unchanged.

## 6. Resource and scope limits

The observed environment is Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, CPU-only Linux, four CPUs of cgroup quota, and a 4 GiB cgroup memory limit. Workers used one Torch/inter-op/BLAS thread and at most two concurrent study workers. No packages, models, data or remote services were downloaded or installed.

Measured phase elapsed walls: capture {times['capture']:.2f} s; independent scoring {times['score']:.2f} s; replay {times['replay']:.2f} s; exact comparison {times['compare']:.2f} s. The largest supervised sampled worker process-tree RSS was {peak/1024**2:.2f} MiB. These are this host's measurements; sampled RSS is not an OS-exact peak, concurrent worker times are not additive elapsed wall, and no Windows/GPU timing claim is made. Raw starts, ends, exit codes and worker resource receipts remain in `logs/`.

This is a fixed-parameter, 16-record/eight-stage synthetic mechanism study with supplied identity catalogues, owner metadata for the privileged control, and qualified writes. It is not a language companion, integrated tri-core NSS, online learner, low-bit training experiment, unlimited-memory demonstration, or arbitrary crash/power-loss recovery certification.

## 7. Package and reproduction

The complete ZIP retains the original uploaded archives, executable inference/scoring sources, original protocol and criteria, all 15 exports, available historical records, fresh main captures, fresh replay evidence, all scores, negative outcomes, audit receipts and failure logs. Exact duplicate files may be stored once with a lossless alias index; this is byte deduplication, not quantization, omitted cases, or discarded replay evidence.

After extracting the complete ZIP, run `python RESTORE_IDENTICAL_FILES.py` and `python VERIFY_PACKAGE.py`. These standard-library tools restore and verify every logical member, including exact duplicate replay files. The separate delivery receipt records a fresh extraction, restore and verification of the distributed archive.

Numerical regeneration requires the recorded installed dependencies. See `README.md` for inference-only commands with a new output directory and the pinned recovery-source hash. Do not route these exports through the old fit-resume loader.

The compact recovery-context ZIP is for convenient review and later continuation. It is explicitly **not** the complete raw-evidence archive; its scope manifest names the omitted bulk trees.
'''
    (R/'REPORT.md').write_text(report)
    status=dict(a,execution_complete_receipt='results/EXECUTION_COMPLETE.json',report='REPORT.md',main_fits_retrained=0,training_evidence_restored=False,scientific_gates_are_not_whole_product_qualification=True)
    (R/'STATUS.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
    lock=(R/'protocol/RECOVERY_SOURCE_LOCK.sha256').read_text().strip()
    (R/'README.md').write_text(f'''# Q010 Inference Recovery v1.6 — start here

Read `REPORT.md`, then `STATUS.json`. Inference evaluation recovery is complete; missing historical optimizer/RNG checkpoints and raw main training traces remain missing. No main fit was retrained.

## Complete ZIP: restore exact duplicate files and check integrity

From the extracted package directory:

```text
python RESTORE_IDENTICAL_FILES.py
python VERIFY_PACKAGE.py
```

The ZIP stores byte-identical files once. `PACKAGING/IDENTICAL_FILES.json` binds every alias to canonical bytes and SHA256. Restoration makes all original capture/replay paths physically present. Existing different files are never overwritten. This is lossless packaging, not neural quantization or evidence exclusion.

## Inference-only commands

The measured numerical environment uses Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, and safetensors. No automatic installation occurs. Use a new output path for each command. Set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` to 1 in the launch environment. The worker also fixes Torch/inter-op threads and disables training.

```text
python recovery/worker.py audit --output new_export_audit.json --source-lock {lock}
python recovery/worker.py capture --seed 1201 --output new_capture_1201 --source-lock {lock}
python recovery/worker.py score --input new_capture_1201 --output new_score_1201 --source-lock {lock}
python recovery/worker.py capture --seed 1201 --output new_replay_1201 --source-lock {lock}
python recovery/worker.py compare --input new_capture_1201 --right new_replay_1201 --output new_replay_check_1201.json --source-lock {lock}
```

Repeat with seeds 1202–1205 to regenerate the other four paired evaluations. Add `--fixture` to a capture command for the explicitly smaller integration-development selection; never count it as full main evidence. The current result directories are immutable evidence, so do not run the supervisor over them in place.

## Important files

`results/analysis/STUDY_RESULT.json` contains complete coverage, candidate gates and historical gaps. `ALL_QUERY_SCORES.csv`, `ALL_NEGATIVE_QUERY_RESULTS.csv`, `METRICS_ALL_SEEDS_AND_POOLED.csv` and `WHOLE_MAP_DIAGNOSTICS.csv` preserve all results. Per-seed raw captures/replays and independent verification receipts live under `results/main/`. `audit/RECOVERY_TESTS.json` and `FRESH_MAIN_UNDERFLOW_REJECTION.*` document the numerical amendment. Original input archives are retained under `provenance/input_archives/`, including the unusable standalone Q009 ZIP as received.

The compact recovery-context archive contains review/continuation material but omits bulk raw main capture/replay trees and original ZIP inputs. It has its own explicit scope and file manifest. Use the complete archive for full raw-evidence inspection.
''')
    print('REPORT AND STATUS WRITTEN')
if __name__=='__main__':main()
