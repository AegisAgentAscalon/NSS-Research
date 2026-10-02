"""Post-execution descriptive reporting only; no model calls, tuning or source edits."""
from pathlib import Path
import csv,json,statistics,time
R=Path(__file__).resolve().parents[1]
def j(p):return json.loads((R/p).read_text())
def rows(p):
 with (R/p).open() as f:return list(csv.DictReader(f))
def write(p,x): (R/p).write_text(x)
d=rows('results/main/DECISIONS.csv');ct=rows('results/main/CONTROLS.csv');paired=rows('results/main/HELDOUT_PAIRED.csv')
comp=j('audit/COMPLETENESS.json');score=j('results/main/SCORE_RECEIPT.json')
measured=[]
for p in (R/'audit').glob('*.json'):
 a=json.loads(p.read_text())
 if 'stage_seconds' in a:measured.append(a)
cost=[json.loads(x) for x in (R/'raw/main/capture_run/capture/costs.jsonl').read_text().splitlines()]
def count(role,arm,stratum,subtype=None,sigma=None):
 x=[x for x in d if x['split']=='heldout' and x['role']==role and x['arm']==arm and x['stratum']==stratum and (subtype is None or x['subtype']==subtype) and (sigma is None or x['sigma']==sigma)]
 return sum(int(a['correct']) for a in x),len(x)
def frac(x):return f'{x[0]}/{x[1]} ({100*x[0]/x[1]:.1f}%)'
main_table=[]
for role in ('near','ordinary','attention'):
 for st,title in [('bound_known','Ordinary known'),('bound_close','Close identity')]:
  a,b=count(role,'A',st),count(role,'B',st)
  main_table.append(f'| {role} | {title} | {frac(a)} | {frac(b)} | {100*(b[0]/b[1]-a[0]/a[1]):+.1f} pp |')
family_table=[]
for x in paired:
 if x['role']=='near':family_table.append(f"| {x['family']} | {float(x['bound_close_A'])*100:.1f}% | {float(x['bound_close_B'])*100:.1f}% | {float(x['gain_pp']):+.1f} pp | {float(x['bound_known_B'])*100:.1f}% |")
noise_table=[]
for st in ('bound_known','bound_close','unbound_known','unbound_absent'):
 for sg in ('0.01','0.2'):
  noise_table.append(f"| {st} | {sg} | {frac(count('near','A',st,sigma=sg))} | {frac(count('near','B',st,sigma=sg))} |")
negative_table=[]
for st,sub in [('stale_revision','revision'),('stale_revision','deletion'),('cross_scope','foreign_scope_checkpoint'),('wrong_reference','detectable'),('wrong_reference','no_cue'),('correction_conflict','correction'),('correction_conflict','unresolved_conflict')]:
 q=[x for x in d if x['split']=='heldout' and x['role']=='near' and x['arm']=='B' and x['stratum']==st and x['subtype']==sub]
 negative_table.append(f"| {st}: {sub} | {sum(int(x['correct']) for x in q)}/{len(q)} | {sum(int(x['management_abstention']) for x in q)} | {sum(int(x['false_binding']) for x in q)} |")
code='''# NSS CM-01 execution v0.2 — results

**Status: completed bounded, fixed-weight interface pilot.** No training, no optimizer updates, no changes to the fifteen Q010 main exports. This is the execution of **CM-01 from NSS_Context_Management_v0.1**, not the older differently numbered MicroContext draft and not the separate Q010-P1 768-case proposal.

## Executive finding

A grounded 56-byte reference workspace improved the primary near reader's held-out close-identity recall from **88/200 (44.0%) to 142/200 (71.0%)**, a **27.0 percentage-point** increase. Ordinary-known recall improved from **157/200 (78.5%) to 200/200 (100%)**. All five held-out families met the predeclared near-arm gain/control rule, versus the required four. The lowest family gain is exactly 4/40 = 10 percentage points, not a rounded sub-threshold result.

The main qualification is important: the improvement is concentrated in higher-noise queries. At sigma .01, near-arm close recall was 71/100 without the workspace and 70/100 with it. At sigma .2 it rose from 17/100 to 72/100. This supports **reference-assisted query reconstruction/denoising in this wrapper**, not a general solution to close-identity confusion.

The public exact-retrieval control returned the correct payload on **40/40 ordinary-known and 40/40 close-identity held-out records**. It outperformed the learned hybrid on close identities. Therefore the experiment does not establish that neural reading is necessary for exact stored-payload recall once a valid reference is available. Nor does it establish any advantage of token serialization: the structured and serialized interfaces agreed on all **7,680 main reader/case comparisons**.

## What “always resident” means here

The proposed architecture can maintain a fixed-size workspace available whenever a core performs a relevant operation. The controller reads and updates those symbols; the symbols are not autonomous processes. Residency, how frequently the model consults the workspace, and how frequently it rewrites it are separate choices. A resident workspace need not grow with history or be regenerated every recurrent step.

This pilot implements a limited version: a persistent reference packet populated from observable selection/correction events, retained across other events, and consulted at one learned read endpoint. A non-neural unit test confirms persistence through 32 unrelated registration events without rewriting the selected packet. **That is a software invariant, not a CM-02 continuity experiment or a learned recurrent-memory result.** No always-on learned internal token lane, model-managed storage writing, recurrent-state compression, long-horizon cognition, or 8/32/64 native-token budget was tested.

## Locked experiment and added information

The latest 512-record plan was used. The older planning handoff prohibited execution at the time it was written; the current user's explicit execution request authorizes this first bounded pilot. Conditional CM-02 through CM-05 and Q010-P1 were not automatically launched.

Eight fresh episode families were frozen: three development, five held out, with eight strata and eight labeled records per stratum. Each case uses a new path-length-one source graph with sixteen 17-dimensional catalogue codes and one learned reader stage. These families group disjoint episode/catalogue recipes; this is not one continuously evolving catalogue over 64 events. The five fixed model seeds are repeated evaluations, not independent new data families.

The source generator is the retained Q010 make_case implementation. The execution contract separately fixes public event semantics, revisions/deletions, corrections/conflicts, noise balancing, scope handling, and fault injection. Exact source reconstruction in the scorer reproduces keys, values, masks, catalogue, query and the source truth from saved seeds, without importing producer code. These execution completions are declared in protocol/PROTOCOL.json; they are not retroactive changes to Q010's 64-condition evaluation.

A streaming deterministic manager sees an observable registration/selection journal, current scope/task and retained workspace. Handles are allocated from a separate random stream, not derived from answer IDs. Its query output is only an original query, a canonical query previously observed in that journal, or explicit management abstention. It cannot open the protected truth ledger. The original learned rule, K/V/valid arrays and original catalogue-assisted output resolver remain unchanged.

The three interfaces are A: original numerical query; B: structured workspace; C: exactly the same fields serialized as UTF8_BYTE_V1. The string is **56 ASCII bytes/control symbols**, not 56 language-model tokens. Its fields are version, scope, handle, revision, binding-event reference and operation. At most two indexed lookups are made per management request. Missing/unresolved references fall back to the original query; observably invalid references cause management abstention; valid references can substitute a canonical query. The manager never substitutes an expected answer into the learned read.

A separate public exact-lookup control reads the observed payload under the same valid binding and otherwise returns UNKNOWN. It has no fuzzy fallback. A privileged exact-owner control uses the isolated source/ownership ledger to select the actual readable row; it is never pooled with nonprivileged outcomes.

## Held-out task results

Each learned-reader cell below contains **40 held-out episode records × five fixed model seeds = 200 reader/case evaluations**. B and C are identical. Percentages are exploratory descriptive outcomes, not calibrated probabilities or general NSS qualification.

| Role | Task stratum | A: original query | B/C: reference workspace | Change |
| --- | --- | ---: | ---: | ---: |
'''+ '\n'.join(main_table)+'''

### Primary near arm: every held-out family

Each close-identity percentage is over eight records evaluated with five fixed seeds, not forty independent episodes.

| Family | Original close recall | Workspace close recall | Change | Workspace ordinary-known recall |
| --- | ---: | ---: | ---: | ---: |
'''+ '\n'.join(family_table)+'''

The ordinary arm failed its exploratory gain rule in one family (CMEVAL-05: 47.5% to 45.0%, -2.5 points). The attention comparison met the gain/control rule in all five families but had lower pooled close recall. The primary arm was not switched after results. No gate, threshold, decoder or held-out selection was fitted.

### Noise-matched breakdown for the primary near arm

| Stratum | Query sigma | A | B/C |
| --- | ---: | ---: | ---: |
'''+ '\n'.join(noise_table)+'''

These strata contain different randomly drawn episodes at each noise scale, as frozen before execution. The within-case A/B comparison is paired. The pronounced high-noise gain is consistent with canonical-query reconstruction; the low-noise close-identity result does not support a blanket improvement.

## Negative cases and information limits

All negative outcomes remain in the evidence package. The table separates content correctness from management action. A safe refusal on a known record is still a recall failure.

| Primary near arm, held out | Task correct | Management abstentions | Accepted wrong bindings |
| --- | ---: | ---: | ---: |
'''+ '\n'.join(negative_table)+'''

On observably invalid bindings, B/C abstained in all **500 held-out primary reader/case evaluations** (100 unique records × five seeds). Four hundred of those evaluations still required a known answer and therefore remain task-recall losses. The remaining one hundred correspond to deleted records and correctly returned UNKNOWN. The false-reference-acceptance rule passes without pretending that these refusals constitute successful recall.

The no-cue stratum contains a public binding consistent with the journal but inconsistent with the hidden intended identity. All **100 held-out primary evaluations** accepted that wrong binding. The learned reader nevertheless returned the expected content in 33/100; these incidental content successes do not validate the binding. The public exact lookup faithfully followed the wrong reference and was wrong on all 20 unique held-out no-cue records.

There are **64 main opposite-truth pairs** whose complete public history, workspace and numerical input are byte-identical. At sigma .01, the near reader answered all known cases correctly and classified none of their matched absent counterparts UNKNOWN. At sigma .2 it achieved 66/100 known correctness and 34/100 absent correctness. Pairing yields 50% balanced accuracy in both noise strata: deterministic processing cannot recover an origin distinction absent from the supplied information. No gate was optimized for these pairs. Thirty-two additional no-cue counterfactual descriptions reuse existing evidence and invoke no models.

The public exact control's 100% absent accuracy on unbound cases comes from returning UNKNOWN whenever it lacks a usable reference; its known accuracy on the same unbound interface is 0%. This is not identity recognition.

## Verification and measured work

The original planning archive passed its ten-file integrity check; the recovery context passed verification of 5,449 manifest-listed files. Its archive SHA-256 remains `9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e`.

Before any generated fixture or main cases, the execution source/configuration and **2,284 seed allocations** were frozen. The collision audit scanned 5,091 retained source/record files (298,234,599 bytes), including reserved proposals. No collisions were found. This audit cannot inspect missing historical RNG histories or all unmaterialized historical random draws; it does not claim to do so.

Thirteen non-neural contract test methods passed, including malformed/reserved encodings, exact serialization, query provenance, scope, stale/deleted records, conflicts, and persistence without rewrite. The eight-case numerical fixture passed independent scoring and fresh-process replay before main generation.

| Work item | Actual |
| --- | ---: |
| Main labeled records | 512 |
| Main distinct public inputs | 448 (64 deliberate opposite-label duplicates) |
| Main model exports evaluated | 15 |
| Main learned interface decision rows | 23,040 |
| Main non-neural control rows | 1,024 |
| Main producer model calls | 10,560 |
| Fixture producer model calls | 33 |
| Total model calls, including both exact replays | 21,186 / 30,816 cap |
| Physical model-forward batches, including replay | 492 |
| Exact replay array comparisons | 2,228 |
| Exact replay numeric elements | 1,570,385 |
| Incorrect main learned-interface rows retained | 10,571 |
| Incorrect fixture learned-interface rows retained | 33 |
| Incorrect non-neural control rows retained, main + fixture | 256 + 4 |
| New optimizer updates | 0 |

The separate scorer imports no producer/model/generator/manager modules. It reconstructs source inputs and live truth, independently replays management actions, checks the original pointer arithmetic with the pinned verifier, and decodes outputs independently. Fresh-process replay regenerates sources and model outputs; arrays, events, routing and metadata match exactly. Timing and Python allocator-dependent object-size observations are excluded from byte-equality requirements and explicitly retained as separate measurements. Replay is not new scientific sample size. This is internal implementation independence, not third-party replication or cross-device validation.

Producer processes have a guard against opening the protected truth ledger. Public-only envelope checks with changed hidden labels were performed on all 512 main and eight fixture records in both producer/replay executions. These are concrete isolation checks, not a formal information-flow proof.

The underflow amendment was not modified. The retained v1.6 fresh-main underflow fixture still fails the frozen verifier and passes the preserved amended verifier, whose final-probability bound adds 2^-126. The lost original v2 source and historical rejected raw row are still missing and are not claimed recovered.

### Resource accounting

'''+f'''Supervised stages through main replay/comparison took **{sum(x['stage_seconds'] for x in measured):.2f} seconds of measured stage wall time**, including seed scanning/imports. The conservative shared clock at that endpoint was **{max(x['shared_elapsed_seconds'] for x in measured):.2f} seconds**, including preparation between commands. The clock begins 150 seconds before the first recorded preflight receipt to account for the initial inspection. Both figures are below the two-hour study cap; they are not deployment-latency benchmarks.

Peak sampled supervisor-plus-worker process-tree RSS during these instrumented stages was **{max(x['peak_sampled_process_tree_rss_bytes'] for x in measured):,} bytes** ({max(x['peak_sampled_process_tree_rss_bytes'] for x in measured)/2**20:.1f} MiB), below 4 GiB. Sampling was every 0.1 seconds; very brief peaks can be missed. The initial extraction/integrity commands preceded this instrumentation, so no continuously measured peak for that short prelude is claimed.

Each packet is 56 encoded bytes (26 bytes for a hypothetical packed representation of its semantic fields). Each case's public K/V/valid arrays occupy 2,192 bytes; the output resolver's catalogue/symbol arrays occupy another 1,232 bytes; each query is 68 bytes. The public journal's canonical JSON is {min(x['journal_canonical_bytes'] for x in cost):,}–{max(x['journal_canonical_bytes'] for x in cost):,} bytes per case, while the materialized directory is {min(x['directory_canonical_bytes'] for x in cost):,}–{max(x['directory_canonical_bytes'] for x in cost):,} bytes. The binding index is additional. Python object inventories, lookup bytes, event counts and rewrite counts are retained in `raw/main/capture_run/capture/costs.jsonl`; summing separate Python object inventories can double-count shared immutable objects and is not an exact allocation measurement.

Across the 512 main records, the controller processed {sum(x['journal_events_processed'] for x in cost):,} public events and logged {sum(x['workspace_changes'] for x in cost):,} selection/correction/conflict workspace changes. The B interface used {sum(x['lookup_count_per_interface'] for x in cost):,} total indexed lookups (0–2 per record), returning {sum(x['lookup_returned_bytes_per_interface'] for x in cost):,} serialized bytes. C uses the same retained information and is an encoding control. Archive/index construction, public control lookup and verification also cost work. A tiny control string is **not** the whole system memory budget, and no net memory-saving claim is made.

'''+'''## Interpretation and next boundary

The adopted role change is compatible with this result: a compact context channel can preserve information needed to select a reliable recall operation. The clearest measured contribution here is grounded reference management and reconstruction of a less noisy query. When a valid exact reference already exists, the public archive control provides a stronger payload-recall route than these small learned readers. A future system could reserve learned processing for reference acquisition, ambiguous selection, integration and task-state evolution, while using exact lookup for exact references. That is an engineering interpretation, not a newly tested integrated architecture.

The right next conditional experiment is CM-02: compare continuity after delays, switches and corrections, including a workspace-plus-archive arm with task/recurrent state disabled. This would distinguish useful workspace/archive continuity from a necessary recurrent contribution. CM-03 can then compare residency/read frequency against refresh frequency. CM-05 remains the native learned-token/recurrent experiment and needs its own small-model training specification. None was run here; the fifteen saved Q010 exports remain frozen.

## Evidence and historical limitations

The package includes the complete new bounded study's public inputs, isolated truth ledger, model-output arrays, workspace transitions, lookup receipts, public controls, negative decisions, source and locks, fixture/main replay outputs, numeric verifier provenance and audit receipts. It does not duplicate the old model archive. The separately retained 48.7 MB recovery context remains the model/source dependency.

Historical Q010 limitations remain: full main optimizer/RNG checkpoints and raw main numeric training traces are absent; the compact recovery omits the bulk original main capture/replay; three old verifier errors remain historical failures; original training qualification is false. This study does not fill those gaps and does not change old Q010 thresholds or results.

**Bottom line:** CM-01 produced a positive, noise-dependent reference-management result with reproducible limits. It did not demonstrate autonomous always-on tokens, native recurrent-state control, learned workspace generation, or state compression.
'''
write('REPORT.md',code)
write('ALWAYS_RESIDENT_ADDENDUM.md','''# Always-resident management context — proposed semantics

Status: architectural interpretation and follow-up specification notes, not a new executed candidate.

A small workspace may remain resident and be made available at each active recurrent step. Reuse fixed slots rather than append historical tokens. Distinguish (1) residency, (2) consultation frequency, and (3) rewrite frequency. Event-triggered rewriting can coexist with consultation at every step. An idle core need not execute merely to retain its workspace.

A controller interprets the tokens and updates the recurrent state or requests memory operations. Tokens themselves are not autonomous managers. Important references and write requests require provenance and revision checks. Retrieved evidence can temporarily exceed the persistent workspace budget; count that traffic separately.

A future native step could be specified as h_next = F(h, input, workspace, retrieved_evidence), with workspace_next = G(observable_events, h_next, workspace) only at declared update boundaries. This is a candidate interface, not a claim that the frozen Q010 models implement F/G in this form.

CM-01 tested a deterministic 56-byte reference manager and one-stage numerical reads. It did not test continual access inside a learned recurrence or learned storage writing. The software retention unit test is not a substitute for CM-02/03 continuity/cadence studies or CM-05 native training.

Required future comparisons: same resident buffer read each step versus event-only reads; fixed versus event-triggered/periodic rewriting; no workspace; identical structured fields; workspace plus archive with recurrent state disabled; total-memory/compute matched models. Keep constraints and hypotheses separate from demonstrated results. Do not train or edit the original 15 Q010 exports.
''')
status={'id':'NSS_CM01_Execution_v0.2','status':'COMPLETED_FIXED_WEIGHT_INTERFACE_PILOT','training_updates':0,'main_exports_changed':0,'primary_useful_reference_signal':True,
 'primary_near_close_heldout':{'A_correct':88,'B_C_correct':142,'n_reader_cases':200,'unique_episodes':40,'gain_pp':27,'families_meeting_rule':5,'total_heldout_families':5},
 'low_noise_close_gain_pp':-1,'high_noise_close_gain_pp':55,'public_exact_bound_close':{'correct':40,'unique_episodes':40},
 'structured_serialized_comparisons_equal':7680,'native_recurrent_tokens_tested':False,'memory_compression_proven':False,'all_new_negative_evidence_retained':True,
 'candidate_status':{'CM-01':'completed','Q010-P1':'not_run_separate_contract','CM-02':'not_run','CM-03':'not_run','CM-04':'not_run','CM-05':'not_run_requires_new_training_protocol'},
 'original_training_protocol_fully_requalified':False,'baseline_dependency_included':False,'complete_new_CM01_raw_evidence_included':True}
write('STATUS.json',json.dumps(status,indent=2)+'\n')
write('READ_ME_FIRST.md','''# NSS CM-01 execution v0.2

Read REPORT.md for results and limitations, and ALWAYS_RESIDENT_ADDENDUM.md for the proposed architectural interpretation. STATUS.json separates completed work from unrun candidates.

This is the complete evidence package for the **new bounded CM-01 study**, not a complete Q010 archival replacement. No old model/archive ZIP is duplicated.

## Integrity

Run `python VERIFY_STUDY.py` after extraction. It checks all manifest-listed files without loading models or running experiments.

## Tables

- results/main/HELDOUT_PAIRED.csv: all five held-out families and all three roles.
- results/main/FULL_GRID.csv: every split/family/model seed/role/arm/stratum/subtype/noise cell.
- results/main/DECISIONS.csv: all 23,040 main interface decisions.
- results/main/CONTROLS.csv: all 1,024 main non-neural control decisions.
- results/main/NEGATIVE_OUTCOMES.csv: all 10,571 incorrect main learned-interface decisions. Incorrect controls remain in CONTROLS.csv.
- results/fixture/: corresponding eight-case integration-fixture evidence and outcomes.

B/C are encoding controls, not independent learned models. Count unique episodes and model repetitions separately.

## Complete new raw evidence

raw/fixture and raw/main each contain capture_run and replay_run. Inputs contain public numeric arrays, observable journal, and a separate protected.jsonl truth ledger. The inference producer is blocked from opening that ledger. Capture folders retain numerical outputs, transition traces, routing, controls, model identities, costs and attempt counts. Replay is a deterministic fresh-process rerun, not extra scientific sample size.

## Dependency and reproduction

The existing Q010_InferenceRecovery_v1.6_RecoveryContext.zip is required for model inference. Expected SHA-256: `9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e`.

Extract it, verify it with its VERIFY_CONTEXT.py, and use REPLAY_STUDY.py for a separately logged future local reproduction. Consult `python REPLAY_STUDY.py --help`. The historical source/run_stage.py intentionally refers to the original study clock; it is retained as execution evidence, not the future-run driver. Do not rerun source/prepare.py or change the locked protocol.

The current package already contains exact local CPU replay results. A future backend/version/host may differ; do not alter numerical tolerances to force a pass. requirements_snapshot.json records the actual library versions; it is a version record, not an instruction to replace your environment.

Historical missing training evidence and old verifier errors remain. See REPORT.md and provenance/. CM-02–05 were not automatically executed.
''')
write('requirements_snapshot.json',json.dumps(j('audit/HOST.json'),indent=2)+'\n')
print('REPORT_WRITTEN',len(code),'characters')
