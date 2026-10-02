from pathlib import Path
import json,statistics
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'SUMMARY.json').read_text());resources=json.loads((ROOT/'evidence/RESOURCES.json').read_text())
def mr(f,m,metric='correct_identity'):
 return next(x for x in s['membership'] if x['family']==f and x['method']==m and x['count']==16)[metric]
def sr(case,m,metric='known_accuracy',reader='record_hop',depth=8):
 return next(x for x in s['state'] if x['case']==case and x['method']==m and x['reader']==reader and x['depth']==depth)[metric]
def pct(x):return '—' if x is None else f'{x*100:.2f}%'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
methods=['nearest','learned','A_nearest','B_nearest'];names={'nearest':'Unconditional nearest','learned':'Unconditional learned repair','A_nearest':'A: geometric gate + nearest','B_nearest':'B: learned gate + nearest'}
mtable=table(['Mechanism','Exact known','Mild known q05','Altered known q20','False acceptance: independent unregistered'],[[names[m],pct(mr('known_exact',m)['mean']),pct(mr('known_q05',m)['mean']),pct(mr('known_q20',m)['mean']),pct(mr('novel',m,'false_accept')['mean'])] for m in methods])
stable=table(['Mechanism','64 ticks, known/missing','1,024 ticks + eight links, known/missing','Room claims for unregistered query'],[[names[m],pct(sr('storage/both02_t64',m)['mean'])+' / '+pct(sr('storage/both02_t64',m,'unknown_accuracy')['mean']),pct(sr('storage/both02_t1024_h8',m)['mean'])+' / '+pct(sr('storage/both02_t1024_h8',m,'unknown_accuracy')['mean']),pct(sr('query/novel',m,'unsupported_room_rate')['mean'])] for m in methods])
cadence=table(['Schedule','A supported answers','B supported answers','A/B missing answers'],[[label,pct(sr(case,'A_nearest')['mean']),pct(sr(case,'B_nearest')['mean']),pct(sr(case,'A_nearest','unknown_accuracy')['mean'])+' / '+pct(sr(case,'B_nearest','unknown_accuracy')['mean'])] for label,case in [('Every tick','storage/both02_t1024_h8'),('Every 8 ticks','cadence/8'),('Every 32 ticks','cadence/32'),('Read time only','cadence/0')]])
life=table(['Phase','A task accuracy','B task accuracy'],[[phase,pct(sr('registration/'+phase,'A_nearest','accuracy')['mean']),pct(sr('registration/'+phase,'B_nearest','accuracy')['mean'])] for phase in ['before_register','after_register','after_write','correction','clear','rewrite','reset','fresh']])
prep=json.loads((ROOT/'evidence/PREPARATION_SUMMARY.json').read_text());fitseconds=sum(x['fit']['seconds'] for x in prep['runs']);peak=max(x['max_rss_kib'] for x in s['configurations'])
timing=table(['Batch64, one 16-record field','Median ms','10th–90th percentile ms'],[[names[m],f"{next(x for x in resources['rows'] if x['batch']==64 and x['method']==m and x['operation']=='one_field_16_records')['median_ms']:.3f}",f"{next(x for x in resources['rows'] if x['batch']==64 and x['method']==m and x['operation']=='one_field_16_records')['p10_ms']:.3f}–{next(x for x in resources['rows'] if x['batch']==64 and x['method']==m and x['operation']=='one_field_16_records')['p90_ms']:.3f}"] for m in methods])
intervals=[]
for m in ['A_nearest','B_nearest']:
 r=next(x for x in s['membership'] if x['family']=='novel' and x['method']==m and x['count']==16)
 for a in r['false_accept_intervals']:intervals.append([m,a['pair'],f"{a['k']}/{a['n']}",pct(a['wilson95'][0])+'–'+pct(a['wilson95'][1])])
report=f'''# NBR-01 — MembershipRepair008
## Familiarity-aware repair and writable novelty · v0.1
**Executed 21 September 2026 · Main comparison RUN · Full joint target NOT MET · NBR-01 remains OPEN**

## 1. Decision brief
Selective repair worked for ordinary independent unregistered inputs while preserving nominal storage recovery, useful eight-round relationship traversal, and the ordinary registration/write/clear lifecycle. But it rejected too many familiar queries at the declared q20 disturbance. No primary or crossed candidate passed the complete joint criteria in any of its five paired runs.

A second boundary is important: a near-duplicate identity can be properly registered yet a fuzzy learned binder can still write its relationship into an older record. A plausible correct final answer can hide that structural error. The post-hoc diagnostic in §7 isolates it without modifying the main scores.

**Keep:** selective admission as a bounded precision-oriented option, explicit active-reference/absence/readability semantics, the compatible repair/readers, and the strong nearest-code control. **Revise:** heavy-query handling and near-identity binding. Do not promote either head as a general solution to familiarity, and do not declare NBR-01 complete.

This study is entirely numerical. “Identity” means a generated code in this experiment, not a person's identity. “Unknown” means no supported record/match under the declared inputs, not proof that something does not exist or is false. Numerical noise is a synthetic stress condition, not a biological or hardware fault-rate model.

## 2. What actually ran
Five new 633-parameter match heads, seeds1001–1005, were each fitted for 1,200 AdamW steps (batch256): **6,000 main optimizer steps and 1,536,000 training presentations**. Five simple geometric gates were independently calibrated on the same held-out calibration evidence used by their corresponding learned gates. Each calibration had4,096 examples in each of seven classes: **143,360 main calibration labels in total**. Learned gates additionally consumed their counted training data; this is not an equal-teaching-cost contest.

The original Study006 readers and binders801–805 and Study007 learned restorers901–905 stayed frozen. Every learned parameter stayed fixed during scored evaluation. Candidate heads use nearest distance, competing-match separation, cosine features, norm, the existing UNKNOWN coordinate and active-reference count; no true origin, noise setting, original clean vector, target slot, hidden graph or correct answer enters the resolver.

The primary comparison changes admission, not the neural reader. To isolate admission, headline tables pair each gate with nearest-code projection. Gate/restorer cross combinations were also run with the old learned dictionary restorer; none changed the joint decision. Stage A retains distance-only and margin-only ablations without new tuning. No robust-reader retraining was performed.

The original research plan is `spec/RESEARCH_PLAN_v0.1.md`; the resolved protocol is `spec/EXECUTION_PROTOCOL.md`. The local `EXECUTION_LOCK.json` records source/checkpoint/calibration hashes and was created before the main episodes were scored. This was not an external preregistration. All main seeds were retained. The pilot exposed the q20 tradeoff; the95% core requirement was deliberately retained, not reduced after seeing failure.

One completed development fit (1,200 steps) and a later exact training reproduction (another1,200) are separate from the main fit count. The first development pipeline found an implementation error in the UNKNOWN competitor; the pre-main fix restored the inherited sentinel semantics. Failed pilot logs remain in the evidence folder. One foundation-suite invocation was interrupted by the tool command timeout and was rerun completely; no main model fit was excluded or replaced.

## 3. Membership results: restraint has a cost
Each entry below is the mean across five pairs, each using1,024 fresh independent episodes for that stratum. Exact known, mildly altered known, and independent unregistered vectors share the same underlying unit-vector code convention. Factual graph relationships are not supplied to the resolver.

{mtable}

The geometric gate accepted **22/5,120** independent unregistered inputs; the learned gate accepted **28/5,120**. The same-base noisy-independent negative stratum gave A0.41% and B0.43%. All five pairs met the *empirical*1% identity false-acceptance ceiling on both ordinary negative strata. Those observations do not prove a deployment error probability below1%.

The q20 supported identity losses are decisive: A70.16% and B66.93%, versus98.85% for unconditional projection. Abstention counts as failure on a supported identity. B did not earn a nominal advantage over A in this preparation. These are bounded implementations, not proof that a better learner or richer input cannot improve the tradeoff.

The larger Stage A membership sample and smaller end-to-end query sample are different cohorts. On the end-to-end q20 case, record_hop's supported destination accuracy was A75.63% and B71.25%. No condition was relabelled stress after these failures.

Raw pre-projection scores, accepted identities and final selected codes are saved. A canonical repaired vector is not used as independent evidence that the original input was familiar. Unconditional controls naturally propose a known symbol for every independent unit-vector input; that is different from a final reader making a room claim.

### Per-pair ordinary-unregistered intervals
Descriptive95% Wilson intervals below use episodes, not recurrent hops. Different pairs have different calibration thresholds. They are not formal guarantees about future deployment.

{table(['Gate','Pair','False accepts / episodes','Wilson95% interval'],intervals)}

## 4. The useful memory/reading result was preserved
These headline state conditions use64 streams/pair (32 complete and32 missing) and the inherited record_hop reader at sufficient depth. Parent and gate weights are fixed. Both fields receive sigma0.02 disturbance per tick in the nominal storage rows.

{stable}

Both gates preserved100% tested known and missing-chain outcomes through1,024 nominal noise ticks and eight-link reasoning. The unregistered-query row contains320 queries in total: zero unsupported room outputs were observed with either selective gate, compared with67.50% for unconditional nearest and49.38% for unconditional learned repair. Zero/320 is not zero risk; the descriptive95% Wilson upper endpoint is about1.19%.

The gated_hop reader and exact traversal of the **same actual store** were also evaluated. Exact traversal received no gold rewrite of the stored associations. The two neural readers still need sufficient query depth: repairing symbols does not itself traverse the graph. All1/2/4/8 outputs remain available in SUMMARY.json and per-pair results.

The registered whole-joint screens remain **0/5 for each of the four selective gate/restorer configurations**. They pass ordinary missing-information and registration requirements, but fail q20 supported coverage and the allowed known-repair regression. This is a partial mechanism success, not a passed overall experiment.

## 5. Writable novelty and evidence status
The active reference initially contains12 identities and four zero, masked rows. The new code is unavailable to the candidate until a distinct permitted REGISTER event; querying it cannot register it. Registration changes scoped working state, not model weights. REGISTER creates no location fact. Qualified relationship writes use the inherited learned binder, without a target slot supplied by the scorer.

{life}

These ordinary registration scores are100% in every pair for A-nearest and B-nearest. Neighbour-record checks and the crossed repair arms also meet their registered95% floor. The lifecycle includes64 background/noise ticks per phase, denied and wrong-scope writes, corrections, clear/rewrite, full scope reset and fresh setup. Checks occur at declared query points; this is not an all-time guarantee.

Identity membership, relationship presence and readability remain distinct. A rejected stored field retains its presence and available raw vector but becomes sticky-unreadable until a qualified write/clear. Repeated projection of the same rejected state cannot manufacture additional evidence. This conservative policy contributes to the cadence failure below; it is a declared policy, not the only plausible one.

Protected Boolean relation-presence is still an explicit control. The learned existence maps from Study005 were not silently transplanted. The codebook remains a protected reference of symbols, not a protected graph or truth oracle. Old masks/status snapshots are rejected under the new ABI rather than assumed compatible.

## 6. Maintenance can be less frequent—but not arbitrarily delayed
The following uses the same1,024-tick/eight-link graph family and sigma0.02 schedule. It is a predeclared schedule comparison, not a search for a best result after failure.

{cadence}

Every-eight-tick repair made128 maintenance sweeps instead of1,024 and preserved all tested nominal chain outcomes. That is **eightfold fewer sweeps**, not a measured eightfold whole-system speedup. Evidence processing, queries, matching, allocation and bookkeeping still cost time.

At32 ticks, accumulated distortion made the selective policies reject fields and quarantine them. Unconditional nearest still achieved99.38% supported-chain accuracy in that condition, whereas A fell to40.00% and B to10.63%. Their good UNKNOWN rates do not offset losing established facts. A familiarity gate suitable for a fresh external query is not automatically a suitable recovery rule for previously established internal state after a longer unobserved interval.

Read-time-only repair after the full delay recovered3.75% with unconditional nearest and0% with either gate. The32-tick contrast is especially diagnostic because much of the state remained recoverable under the unselective control. No post-main cadence or threshold refit replaced these results.

## 7. Two distinct near-identity failures
### Unregistered inputs resembling a known code
At the near-novel0.1 setting, both gates accepted all5,120 such unfamiliar inputs as registered symbols. End-to-end, both produced unsupported room answers in50% of the320 near-novel queries. Half of the base graph queries deliberately lacked an answer, which explains why not every false identity match became a room claim.

The gates work well when the input is far from the registered set; they do not know its historical origin merely because it is close. The identical-observable pairing is a deliberately constructed information-limit illustration. Its50% binary-origin ceiling is an analytical consequence of opposite labels for identical observations, not an empirically discovered global bound on recognition.

B did improve particular stress tradeoffs: for equal two-code mixtures, its false acceptance was0.21%, versus6.41% for A. It preserved100% identity recognition under doubled vector magnitude, where A rejected all. Both rejected all quarter-magnitude inputs. These useful differences do not rescue B's failure on the core q20 criterion.

### Registered near-duplicates: a correct answer can conceal an overwritten record
Both the unconditional and B-nearest neural readers answered the new near-registered query correctly in100% of main cases. Yet exact traversal of the same stored records answered only11.875%. The mismatch triggered a labelled **post-hoc failure-isolation diagnostic**, with no training or changes to the main scores.

In320 replayed near-registration cases, B-nearest's binder accepted all new writes but used an existing physical record slot in **282 cases (88.125%)**. Only38 had a separate new record. It actually changed an older record's content in **246 cases (76.875%)**. The fuzzy reader could retrieve the newly written room through that older near-identical key, so the answer looked right despite the incorrect binding.

This is a binder/interface failure, not a restoration win and not evidence that registration is generally solved for near-duplicates. A's stricter margin rejected most such writes; one calibration pair without a margin admitted them and showed the same aliasing risk. The registry itself allocated distinct identity rows correctly; the subsequent relationship binder conflated them. See `evidence/NEAR_COLLISION_DIAGNOSTIC.json` and its independently rerun diagnostic arrays.

## 8. Costs and fairness
{timing}

These are local implementation measurements on Linux CPU with one Torch compute thread. Timings include validation/Python overhead; other reproduction work was running on the same host. Batch-one and complete-query measurements, percentile ranges and operator allocation profiles are in `evidence/RESOURCES.json`. Do not extrapolate to the user's device or treat these as optimized kernels.

A was lighter than B for a field sweep in this measurement, and the inherited learned projection was considerably more expensive than nearest projection. Query-time differences were smaller/noisier. Candidate complexity must be justified by the quality/error tradeoff, not a neural label.

Raw active state is **3,336 bytes per stream**:2,176 bytes for16 keys/values,48 for presence/readability flags,1,088 for registered-code capacity,16 for active masks and8 for the reference revision. Query state, scores/features, projections, model weights, framework and audit storage are additional. The head contributes2,532 parameter bytes. Float32 head parameters + gradients + two AdamW moments + six scalar steps total10,152 raw bytes during fitting, excluding inputs/activations/temporaries.

The completed main head fitting loops took **{fitseconds:.2f} seconds** in aggregate; calibration and development/reproduction work are additional. The main driver (all membership/state evaluations) took653.26 seconds. The largest reported main evaluation process peak was **{peak/1024:.1f} MiB RSS**, below the registered4GiB process ceiling. Driver and concurrently running verification processes are additional; peak RSS is not just neural-state memory. No low-bit learning or packed execution claim follows from these numbers.

## 9. Verification and delivered evidence
All **45 new tests**, **34 unchanged RepairBinding007 tests**, and **68 unchanged foundation tests** passed: **147 distinct tests**, counting reruns once. All five heads and both parent readers are included with their source identities. Main evaluation hashed every learned component before/after and found no weight change.

The independent scorer rederived graph answers without importing the candidate or evaluator metrics and checked **1,210 membership rows and14,940 state/depth rows**. These represent1,239,040 resolver decisions and956,160 scored state answers across reused paired inputs—not that many independent experiments. All raw features/decisions, state snapshots and intermediate/final outputs are retained or losslessly transported; seeds regenerate the full inputs.

Every main membership and state evaluation was replayed in fresh interpreters and all saved arrays compared exactly. One complete1,200-step head fit, its losses, selected data fingerprints, final checkpoint bytes and calibration reproduced exactly. **80 state/RNG and partial-query continuation cases** were replayed in a separate process for the tested record_hop path. This is internal reproducibility, not external replication.

Large result files are transported as lossless `.npz.xz` where present. The supplied scorer/replay tools decompress them in memory and check the original NPZ digest. This is evidence-file compression, not compressed neural learning state, and does not change a prediction. The original numeric precision is retained.

Original input archives, the research-plan files, and manifest-covered foundation/parent source files were checked unchanged. Full historical1,111-test qualification, Windows execution, language capability, generic-Transformer competence rebuilding, integrated companion operation, and third-party/longitudinal validation were NOT_RUN. The current timing metadata uses the Linux `resource` module; full experiment replay has not been ported/tested on Windows. The check/rescore entry points require no model download or automatic dependency installation.

## 10. Interpretation and next decision
The proposed gate prevented most ordinary unsupported matches without dismantling the successful clean repair/read/write lifecycle. The hard cases show why it is not a universal solution:

* A damaged known query and a genuinely new near-query can overlap in the available representation. Tightening one scalar cannot create missing origin information.
* Recovery of a previously established internal field and admission of an external query have different histories. A single stationary gate plus permanent quarantine can throw away state that a less restrictive decoder could recover.
* Membership registration and record binding are separate. A correct registry row does not guarantee that a fuzzy binder allocates a distinct relationship record.

**Next candidate direction, not yet executed:** distinguish trusted internal-state recovery from external identity admission under explicit provenance; add independently informative context or redundant identity evidence for ambiguous inputs; and test identity-preserving allocation/selection against a learned binder trained on near-duplicate negatives. Exact identity-aware bookkeeping should remain a labelled control, not be smuggled in as learned reasoning. Evaluate affected old records, not just the new query's answer.

Do not launch an unlimited threshold search, secretly retrain the frozen readers, or replace the tri-core roles. Retain A as a useful low-cost scoped reference and B's limited stress advantages. The full NBR-01 study remains open for robust representation/binding, stronger generic controls, broader tasks and a complete quality/resource comparison. Delayed credit and1–8-bit learning-state experiments remain deferred.

## Sources and provenance
The requested basis was `NSS_NBR01_MembershipRepair008_Research_Plan_v0.1.md` plus the supplied RepairBinding007 package. Parent source and checkpoint hashes are in `evidence/REFERENCE_HASHES.json` and `spec/EXECUTION_LOCK.json`. The original RepairBinding007 report is included under `reference/`. The broader cognition handoff defines NBR-01 as state/depth with learning fixed; it is not evidence that this new pass had previously run. No new outside literature, human/fly simulation, network service or external dataset was used in this execution.

The artifact is a standalone research package, not a cumulative NSS source release. Keep it beside the preceding studies in `MegaMind_Alpha_Proto`; do not merge it into the foundation.
'''
(ROOT/'REPORT.md').write_text(report)
print('wrote report',len(report.split()),'words')
