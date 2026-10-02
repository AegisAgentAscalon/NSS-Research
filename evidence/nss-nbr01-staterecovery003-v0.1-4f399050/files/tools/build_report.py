from pathlib import Path
import json,statistics,collections
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'SUMMARY.json').read_text());r=json.loads((ROOT/'evidence/RESOURCE_ACCOUNTING.json').read_text())
d=json.loads((ROOT/'evidence/EMPTY_STATE_DIAGNOSTIC.json').read_text())
rows=s['summary']
names={'hold':'Hold + original readout','readout_repair':'One-step learned readout repair','recurrent':'Learned recurrent maintenance',
'fast_slow':'Learned fast/slow filter','fast_slow_equal':'Same filter, equal maintenance rates','two_copy_mean':'Two-copy mean (equal state bytes)',
'nearest_read':'Nearest supplied prototype at read','nearest_maintenance':'Nearest-prototype maintenance','recurrent_query4':'Recurrent map only at read (4 rounds)',
'exact_archive':'Protected exact-record control','recurrent_off':'Same recurrent checkpoint, maintenance off','state_off':'State removed'}
def find(group,condition,level,rounds,mode):
 return next(x for x in rows if (x['group'],x['condition'],x['level'],x['rounds'],x['mode'])==(group,condition,level,rounds,mode))
def fmt(x,key):
 v=x[key];return '—' if v['mean'] is None else f"{100*v['mean']:.2f} ± {100*v['sd']:.2f}%"
def table(group,condition,level,rounds,modes):
 out=['| Mechanism | Known-record accuracy | UNKNOWN accuracy |','|---|---:|---:|']
 for mode in modes:
  x=find(group,condition,level,rounds,mode);out.append(f'| {names.get(mode,mode)} | {fmt(x,"known")} | {fmt(x,"unknown")} |')
 return '\n'.join(out)
def screen_table():
 modes=['hold','readout_repair','recurrent','fast_slow','two_copy_mean','nearest_maintenance','state_off']
 out=['| Mechanism | Competence screen | Clean long-maintenance screen |','|---|---:|---:|']
 for m in modes:
  a=[x for x in s['screens'] if x['mode']==m]
  out.append(f'| {names.get(m,m)} | {sum(x["competence"] for x in a)}/5 | {sum(x["long_stability"] for x in a)}/5 |')
 return '\n'.join(out)
mu=lambda xs:statistics.mean(xs)
fd=[x for x in d['local_stability'] if x['epsilon']==1e-3]
unknown=[x['unknown_radius'] for x in fd];known=[x['known_max_radius'] for x in fd]
resource=[]
for m in r['modes']:
 if m['mode'] not in ['hold','readout_repair','recurrent','fast_slow','two_copy_mean','nearest_read','nearest_maintenance']:continue
 resource.append(f'| {names[m["mode"]]} | {m["raw_activation_bytes_per_stream"]} B | {m["extra_parameter_bytes"]} B | {1e6*m["median_seconds_per_maintenance_plus_read_batch"]:.1f} µs |')
report=f'''# NSS NBR-01 / StateRecovery003
## Native state maintenance: recovery, fast/slow lanes, corrections and empty-state integrity

**20 September 2026 · Standalone research package v0.1**  
**Main experiment RUN; main protocol locally registered before training/scoring. Post-hoc diagnosis separately labelled.**  
**Full NBR-01 remains OPEN. No architecture replacement, production qualification, or trained-core integration.**

## Decision brief

A learned recurrent repair mechanism recovered damaged known patterns and maintained them under repeated state noise. However, the same dynamics could turn an empty state into a known pattern. This is a joint accuracy/absence failure, not useful complete memory. A stable answer is not necessarily a supported answer.

The fast/slow candidate helped when its slower lane remained intact. With independent damage to both lanes, an equal-byte two-copy average performed better; common-mode damage removed the benefit. This candidate does not establish a general advantage for multiple neural timescales.

A simple nearest-prototype control was extremely strong in this deliberately closed, categorical representation. Do not claim neural or biological superiority by omitting it. Keep exact evidence and the tri-core framework. Carry learned restoration forward as a bounded research mechanism, but revise its empty-state stability and uncertainty handling before expansion.

## 1. What was actually built and run

We reused five competent, frozen wide-training soft-state representations from HorizonBinding002 (seeds301–305). Each supplies16-dimensional learned value codes and its original trained nine-class readout: eight known values plus UNKNOWN. Their source gates, encoders and readout weights were not changed.

For each representation, a new learning-data/initialization seed501–505 prepared three candidates: a2,128-parameter one-step repair network used only at read time; a2,128-parameter recurrent repair network; and a three-parameter fast/slow filter. That is **ten newly trained small neural repair networks and five fitted fast/slow filters**, not fifteen newly pretrained companion cores.

All15 fits completed1,800 AdamW steps at batch128: **{s['total_main_optimizer_steps']:,} optimizer steps and {s['example_presentations']:,} example presentations**. Within each paired seed, all three arms received identical noisy inputs, answer labels and target-code supervision. The paired data digests matched. Distinct input presentations are reused across arms; these are not3.456million independent examples. The repair-at-read arm uses one computational round, while recurrent/filter training samples1/2/4 rounds. Same data/steps is **not** the same compute or state capacity.

This is intentionally a **qualified-write ablation** of the prior representation, not an unchanged end-to-end rerun of the previous soft learner. Four addresses and the clean score≥0.5 qualification rule are supplied. A legitimate write installs its code; ignored events do not write; explicit reset clears the state. These choices isolate maintenance from qualification and binding. They are not discoveries of this experiment.

The protected exact-record control initializes a separate ledger from the same visible setup records and updates it only on the same qualifying events/clears. No test answer is passed into its read method. Neural-coordinate faults do not corrupt that ledger. Its extra intact information is declared, not available to the neural arms.

## 2. Mechanisms and biological scope

The project handoff identifies persistent temporal stateG03, stabilityG05 and recurrent-depth separation, and on page7 uses fly heading-circuit attractors as a mechanism reference. Our study extracts the functional question—maintenance and perturbation recovery—without simulating a fruit-fly connectome, human circuitry, physiology or subjective memory. No anatomical data or new literature claim is established by these tests.

**Hold:** preserve the current vector; use the original readout.

**Read-time repair:** train a nonlinear repair map, apply it once to the vector used for answering, and leave the stored state alone.

**Recurrent maintenance:** repeatedly apply a shared learned residual map to the stored state. In normalized coordinates, F(h)=0.5h+0.5[network(h)−network(0)]. An exact-zero guard enforces F(0)=0 at machine precision; it does not protect nonzero perturbed empty states. This is actual recurrent numerical processing, not repeated prompting.

**Fast/slow:** retain two16-dimensional lanes. Maintenance is f′=(1−b)f+b·s and s′=(1−g)s+g·f, using the previous pair simultaneously. A qualifying write puts the new code in f and blends it into s with coefficient a. The three rates are learned. Both lanes are activations; evaluation does not change a weight or a fast-association matrix.

**Controls and interventions:** disable the recurrent update; apply the same recurrence only at read; equalize fast/slow maintenance rates; use two independent copies averaged at read; decode the nearest supplied prototype; repeatedly project onto that prototype; restore from a protected exact ledger; remove all state. Nearest-prototype modes use the same finite learned code bank as the neural models. That strong supplied structure must not be confused with solving arbitrary representations.

## 3. Main protocol and qualification boundaries

Each shock condition uses256 four-address streams per paired seed. Corruptions include independent Gaussian noise, shared noise across both lanes, first-lane-only noise, coordinate erasure, directed mixing toward an incorrect prototype, erasing the first lane and erasing all neural state. Noise is measured relative to the source embedding's RMS, **not** in biological units.

Maintenance is scored at0/1/2/4/8/16/32/128 rounds. Training covered at most four rounds and Gaussian standard deviation0.5;1.0 and1.5 shocks are distribution-shift challenges. Clean state is checked through4,096 logical autonomous rounds. These are **not4,096 fresh observations or a reasoning test**. If deterministic autonomous iteration reaches a bit-identical fixed point, later identical rounds may be fast-forwarded; both logical and executed counts are recorded.

A genuine qualifying replacement at address0 follows32 maintenance rounds; acceptance of the new value and retention of the unchanged addresses are evaluated separately. Explicit reset is checked through4,096 logical rounds. In the chronic-damage condition, new independent noise enters each lane at every event, followed by one maintenance step. There are64 four-address streams per seed/noise level and up to1,024 actual noise events. No fixed-point skipping is possible across fresh noise.

The confirmatory output contains **{s['cells']:,} main metric cells and {s['total_answer_evaluations']:,} repeated answer evaluations**. Many cells share the same assignments or trajectories. Do not treat that number as independent subjects, training examples, or replicates. Tables report means and sample standard deviations across five paired, reused-representation/new-training-data seeds, with no best-seed selection.

The registered competence gate combines clean known/UNKNOWN accuracy, replacement accuracy and exact reset at≥95%. Long clean maintenance additionally requires≥95% and≤1percentage-point loss versus the short horizon. These gates do not certify noisy recovery, semantic truth, general memory, or companion readiness.

{screen_table()}

All non-state-removed modes preserved clean records and explicit reset, and accepted the tested qualified replacements. This establishes the controlled starting point; holding an explicitly qualified exact code is intentionally easy.

## 4. A real recovery effect—with a false-memory tradeoff

The following is a single Gaussian shock of standard deviation1.0, evaluated after four maintenance rounds:

{table('shock','gaussian',1.,4,['hold','readout_repair','recurrent','fast_slow','two_copy_mean','nearest_read'])}

The recurrent candidate gained **29.63percentage points** in known-value accuracy over the same checkpoint with maintenance disabled:65.01%→94.64%. The raw state reconstruction error also fell substantially. However, UNKNOWN accuracy fell from71.33% to47.43%. Answering a familiar class more successfully while converting empty records into familiar classes is not a complete improvement.

One-step learned read repair achieved89.15% known accuracy while preserving78.23% UNKNOWN accuracy. The nearest-prototype control achieved96.29% known and77.35% UNKNOWN. Consequently, recurrence has a demonstrated effect relative to its intervention control, but **does not earn a blanket acceptance over the stronger simple alternatives**.

After a single isolated shock, applying this same four-round recurrent map only at read produced exactly the same final predictions as four maintenance steps. No extra information enters between them. That equivalence prevents crediting an ongoing-state mechanism for work that could be done once at the interface.

At the milder0.5 shock the recurrent candidate reached99.98% known and86.73% UNKNOWN, while nearest-prototype decoding reached100% known and99.82% UNKNOWN. The full condition/depth curves, including all failures, are in SUMMARY.json and evidence/results.

## 5. Repeated damage makes repair timing matter

With standard deviation0.15 fresh state noise on every event, after1,024 events:

{table('chronic','independent_state_noise',.15,1024,['hold','readout_repair','recurrent_query4','recurrent','two_copy_mean','nearest_maintenance'])}

The learned recurrence retained all tested established values in all five pairs, but **none of the initially empty records remained correctly UNKNOWN**. Both numbers are essential. The exact projection mechanism preserved both in these small known-code conditions.

Doing up to1,024 applications of the same learned repair map only at the end reached **29.56±3.32% known accuracy** and **0.71±1.60% UNKNOWN**, compared with100%/0% for one update after every noise event. Thus waiting until corruption accumulates was not repaired by granting more rounds at the end. The two branches have the same *maximum logical repair budget*; fixed-point skipping and execution timing differ, so this is not a matched-wall-time benchmark.

The finding is scoped: corrective state dynamics can preserve an already encoded category under repeated disturbance. It does not establish multi-step reasoning, noise-aware interpretation of uncertain external observations, or general consolidation.

## 6. What the two-timescale result actually means

With independent1.0 shocks to both copies, fast/slow reached81.73% known accuracy, while a simple equal-byte average reached85.53%. Equalizing the maintenance rates produced the same accuracy as the mean control in that cell. With a common1.0 shock applied to both lanes, all these linear two-lane variants retained the same64.83% known accuracy as the unmaintained reference.

That is explicable from the candidate's own equations. Its autonomous consensus approaches (g·f₀+b·s₀)/(b+g). It pools information from the two lanes; it cannot remove a disturbance shared identically by both. Learned b values were approximately0.681–0.691 and g0.296–0.312, so the steady estimate weights the slower lane more heavily. Training included cases where only the first lane was damaged; equal-weight averaging is not guaranteed optimal across that mixture.

When only the first lane received a1.0 shock, the fast/slow candidate reached99.98% known accuracy versus97.56% for the equal-byte mean. When that first lane was completely erased but the second stayed intact, **both** achieved100%. Erasing both removed that advantage entirely.

**Decision:** this fitted fast/slow candidate has not demonstrated a general benefit beyond selective redundancy and pooling. Retain the question of distinct timescales; do not promote this specific filter merely because it resembles a brain-inspired diagram. It also does not rule out nonlinear multi-timescale mechanisms or their usefulness for other tasks.

## 7. Stable wrong answers and the information-loss control

Mixing the state75% toward a different valid code drove all non-archive candidates to0% accuracy in that condition, and they remained wrong through128 rounds. Stable convergence is not a truth test. Attractors can restore a neighborhood of a representation; they cannot infer that an observation has been moved into the wrong neighborhood without additional information.

After complete neural-state erasure to zero, every neural/non-archive mechanism returned UNKNOWN:0% known-record recovery and100% correct UNKNOWN. The protected exact-record control recovered100% because it retained the recorded values outside the faulted state. This demonstrates the declared information boundary, not a new information-theory theorem or a cost-free neural recovery.

All qualifying corrections at the designated address were accepted, including after the misleading-state challenge. Exact writes and clears remain supplied operations; these results do not prove a learned system knows which natural-language correction is valid.

## 8. Post-hoc diagnosis: the empty point was fixed, but not stable

After the main results, a separately recorded diagnostic inspected the learned map locally. Main scores and weights were not changed. Central finite differences at two step sizes measured the local linearized update around settled known-code points and around zero.

At step size0.001, the largest-magnitude local eigenvalue at UNKNOWN was **{min(unknown):.3f}–{max(unknown):.3f}**, greater than one in all five pairs. The largest such value across the eight settled known codes for each pair was **{min(known):.3f}–{max(known):.3f}**, below one. The0.0001 estimates gave the same qualitative distinction. This is evidence of local amplification around the empty point versus local restoration around known points; it is **not** a global convergence proof.

The exact-zero guard ensured clean reset remained exactly zero. But forcing F(0)=0 did not make a neighborhood of zero stable. Real injected nonzero perturbations could be amplified and settle into a familiar pattern. The main false-UNKNOWN result is therefore not the old, unfixed development reset bug.

A second diagnostic kept a protected record-presence flag per address, derived from visible setup WRITE observations. With the same learned weights and1,024 fresh0.15-noise events, clamping known-empty addresses back to zero after maintenance produced100% known and100% UNKNOWN in all five pairs. The unguarded arm again produced100%/0%. Deliberately inverting the metadata produced0%/0%.

**This is a post-hoc exact-metadata intervention, not a learned neural solution.** It adds four raw boolean bytes per stream (not packed bits), and the neural fault does not touch that metadata. It cannot reconstruct which value was completely erased, establish factual correctness of a present record, or justify treating uncertain observations as exact. It does identify a useful next contract and failure injection: presence/absence must not be inferred solely from a damaged semantic vector, and metadata itself needs provenance and integrity.

Files: spec/POSTHOC_EMPTY_DIAGNOSTIC.json, evidence/EMPTY_STATE_DIAGNOSTIC.json, evidence/DIAGNOSTIC_VERIFICATION.json. Ten local-stability cases and15 presence-intervention cases were replayed in a fresh interpreter with identical numerical output.

## 9. Resources and the boundaries of efficiency claims

{chr(10).join(['| Mechanism | Raw activation state per stream | Extra candidate weights | Maintenance + read, batch64 |','|---|---:|---:|---:|']+resource)}

Each stream has four addresses. All neural modes also share4,072bytes of frozen code/readout tensors; file headers, scope metadata and snapshots cost additional space. Nearest-code modes use the same supplied finite code bank, not a free uncounted catalogue. The current exact-ledger harness retains a dummy neural buffer plus a separate32-byte int64 ledger per stream; the guard diagnostic's existence flags use4bytes. These are measured tensor sizes, not complete process memory.

Times above are descriptive medians of five300-iteration CPU microbenchmarks on one representative pair, each iteration containing one maintenance call and one read across64 streams. They are not token latency, user-PC performance, biological efficiency, or fully controlled end-to-end quality/compute frontiers.

New main training loops took **{s['training_loop_seconds']:.2f}s**, and main evaluation took{s['evaluation_seconds']:.2f}s. These tiny numerical mechanisms are not language models. Reused source preparation previously took48.81s for12,000steps,576,000example presentations and18,820,224event presentations; it was not redone here and is not free. The additional development, diagnostics, validation, reporting and full training reproduction are excluded from the main-loop total.

Training RSS samples peaked at{max(t['rss_process_peak_5ms_sample_bytes'] for t in r['training_records'])/1e6:.2f}MB for the Python/framework process. Five-millisecond sampling can miss short peaks. Exact temporary operation peaks, target-device memory/latency and energy remain unmeasured. Stored states and weights are float32; no packed low-bit learning state was tested.

## 10. Reproducibility, recovery and preserved failures

**38 unit tests passed.** All15 main checkpoints passed source/initialization/changed-parameter identity checks. A fresh interpreter replayed all**11,090 main metric rows and every saved prediction array**, including failed cases. One complete1,800-step recurrent training trajectory (representation303, learning seed503) was repeated from initialization with the same input digest, final tensor identity and safetensors checksum. These checks are not additional independent seeds or an external scientific replication.

Sixty actual weight/mode configurations passed snapshot→fresh-interpreter restore→continue checks, with exact final tensor identities, pure reads, scope/revision validation and clearing. They are research-state checks, not a production database or power-loss durability qualification. The independent protected-ledger control is not presented as a neural snapshot mode.

The untouched foundation was freshly extracted; its68 foundation tests, dependency check and974-file manifest passed. The full historical1,111-test suite and Windows execution were not run. Input archive hashes are checked before and after the work.

Three600-step development fits were retained separately. Development exposed a numerical zero-offset bug caused by differing evaluation/reduction shapes at a mathematically identical zero. An exact-zero guard was added before main registration. The old implementation and its failed results are retained. No main seed was discarded, no scored threshold was retuned, and the post-hoc guard does not overwrite main results.

## 11. Engineering decision and next bounded work

**Keep:** the exact evidence substrate, explicit qualified updates/resets, whole-generation boundaries and existing tri-core + Validator framework. All these candidates are alternative mechanisms, not separate personalities or new serving cores. The source foundation remains unchanged and its adapters remain labelled test adapters; Forge/Runtime integration has not been created by this study.

**Carry forward, but revise:** learned restorative recurrence. It has a causal recovery effect and a meaningful repeated-damage retention effect, but the current objective does not make UNKNOWN a robust region. The next native-state study should explicitly train and test that region: local contraction/denoising objectives around empty state, longer variable-depth/chronic-noise preparation, and comparison with an exact, integrity-checked presence field. Preserve established-value acquisition and correction agility while doing so; suppressing every answer is not a pass.

**Do not promote:** this simple linear fast/slow filter on the present evidence. Its advantages substantially track replication and the assumed fault location. Nonlinear timescale separation remains an open candidate, not a rejected field.

**Keep the strong control:** nearest-code correction for this finite categorical task. A broader representation/binding study must include equally strong relevant controls and unseen/compositional cases, not merely remove the successful simple control. The current fixed nine-code universe is not a general memory architecture.

After joint known/UNKNOWN stability is addressed, remove the supplied-address shortcut in a separate binding comparison and test real relational recurrent depth. Delayed-credit and low-bit eligibility work remain separate NBR-02/03 stages. No part of this package proves human/fly brain fidelity, a superior Transformer replacement, lifelong learning, identity continuity, or integrated companion value.

**Bottom line:** restoration is a usable candidate mechanism, not permission to trust the restored content. The next neural target is a state space with stable known representations **and** a stable, explicit way to remain without a record.

## Evidence index

Main design and chronology: spec/protocol.json, spec/REGISTRATION.json, spec/DEVELOPMENT_FINDINGS.md.  
Exact trained weights and learning logs: evidence/main. Frozen source checkpoints: reference.  
Every metric and prediction array: evidence/results; aggregation: SUMMARY.json.  
Numerical replay: evidence/INDEPENDENT_VERIFICATION.json. Full trajectory replay: evidence/TRAINING_REPRODUCTION.json.  
State lifecycle: evidence/LIFECYCLE_VERIFICATION.json and evidence/snapshots.  
Post-hoc diagnosis: evidence/EMPTY_STATE_DIAGNOSTIC.json and its separate registration/verification.  
Resource measurements: evidence/RESOURCE_ACCOUNTING.json.  
Foundation regression: evidence/FOUNDATION_REGRESSION.json.  
Input preservation and final manifest: evidence/INPUT_PRESERVATION.json, MANIFEST.sha256.  
ZIP-level delivery verification is provided beside the package after a fresh extraction check.
'''
(ROOT/'REPORT.md').write_text(report)
print('Report words',len(report.split()))
