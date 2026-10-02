"""Post-result reporting and delivery, separate from frozen scientific source."""
from pathlib import Path
import json,hashlib,zipfile,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];OUT=R.parent
S=json.loads((R/'results/SUMMARY.json').read_text());A=json.loads((R/'results/AUDIT.json').read_text())
def get(mode,arm,n,f=False):return next(x for x in S['pooled'] if x['mode']==mode and x['arm']==arm and x['n']==n and x['frozen']==f)
def pct(v):return f'{100*v:.3f}%'
def cell(x):return f"{x['correct']}/{x['total']} ({pct(x['accuracy'])})"
def whole(x):return f"{x['whole_correct']}/{x['jobs']} ({pct(x['whole_accuracy'])})"
rows=[]
for n in [8,32,128,512]:
 u,s,m=[get('hsa',arm,n)['selected'] for arm in ['U','S','M']]
 rows.append(f'| {n} | {cell(u)} | {cell(s)} | {cell(m)} | {whole(u)} → {whole(m)} |')
dense=[]
for n in [8,32,128,512]:
 u,s,m=[get('dense',arm,n)['selected'] for arm in ['U','S','M']]
 dense.append(f'| {n} | {cell(u)} | {cell(s)} | {cell(m)} | {whole(m)} |')
parent=[]
for seed in [8801,8802,8804]:
 vals=[next(x['selected'] for x in S['per_parent'] if x['seed']==seed and x['mode']=='hsa' and x['arm']==a and x['n']==128 and not x['frozen']) for a in ['U','S','M']]
 parent.append(f'| {seed} | {cell(vals[0])} | {cell(vals[1])} | {cell(vals[2])} |')
stre=[v for p in (R/'results').glob('STREAM_*.json') for v in json.loads(p.read_text())['cases']]
scalars=sum(c['scalars'] for r in stre for c in r['checks'].values());violations=sum(c['violations'] for r in stre for c in r['checks'].values())
train=[json.loads(p.read_text()) for p in (R/'results').glob('TRAIN_*_?_*.json')] # actual counts collected below explicitly
train=[json.loads((R/f'results/TRAIN_{seed}_{mode}_{arm}.json').read_text()) for seed in [8801,8802,8804] for mode in ['dense','hsa'] for arm in ['S','M']]
processes=[json.loads(p.read_text()) for pat in ['TRAIN_PROCESS_*.json','EVAL_PROCESS_*.json','STREAM_*.json'] for p in (R/'results').glob(pat)]
main_s=sum(p['seconds'] for p in processes);rss=max(p.get('peak_rss_bytes',0) for p in processes)
prep=json.loads((R/'results/PREPARATION.json').read_text());preflight=json.loads((R/'results/PREFLIGHT.json').read_text())
report=f'''# NSS NBR02 CAP02 — Larger-layout preparation and bounded closeout v0.1

**Disposition: COMPLETE_BOUNDED_PREPARATION; SEGMENTED-CONTEXT/HSA COMPONENT PARKED FOR INTEGRATION.** One fixed-budget follow-up completed. No tuning loop, extra hierarchy level, seed replacement, best-checkpoint selection, or DARP run. Mixed-size preparation substantially improved the existing HSA reader on fresh128-task layouts and retained its eight-task skill. A separate512-task stress remains imperfect. This is sufficient evidence for a bounded working component, not general NSS qualification or proof of unique custom segmentation superiority.

**Execution receipt date:** {datetime.now(timezone.utc).isoformat()}. Main optimizer applications **{sum(x['updates'] for x in train)}**; disposable preflight applications **{preflight['optimizer_applications']}**; total **1155**. Twelve continuation branches from six exact existing parents; zero random-initialized refits. Original source parents and historical findings remain unchanged.

## 1. What was compared
The six CAP01 dense/HSA checkpoints (paired seeds8801,8802,8804) retain37 engineered input features,18,500 parameters,two attention blocks,and task/region/global topology. Each has U(untouched),S(96 extra updates on8-task worlds),and M(96 updates cycling8,32,128-task worlds). Every update supervises exactly eight selected decisions in each of four worlds:32 labels/update and3072 per continuation. Corresponding eight-task steps use identical data. All weight tensors may learn.

Fresh AdamW,lr0.0005,weight decay0.01,betas0.9/0.999,eps1e-8,clip1.0; no schedule, early stopping or endpoint selection. Optimizers reset for each branch. Checkpoints retained at0,24,48,72,96; only fixed96 endpoints evaluated. The M condition uses more source records and computation; equal update and label counts are NOT equal FLOPs, information, or runtime. No claim of training efficiency follows.

Training uses resident source graphs, not a32-record training limit. CAP01 streaming is separately checked after learning. No summaries, JSON-language models, learned segmentation, or new procedural rules were introduced.

## 2. Fresh evidence and denominators
Training has{prep['train_unique_worlds']} unique worlds; each curriculum presents384 worlds, with128 shared. New confirmation has32 independent nonfrozen worlds plus8 separate frozen controls at each of8/32/128 tasks; the independent512-task stress has8 nonfrozen worlds plus2 frozen controls. Total130 worlds, common across all models and branches. No confirmation scoring occurred until all12 continuations completed.

The primary job consists of eight randomly selected task decisions, NOT every task in the archive. Thus each primary size contributes32worlds×3models×8targets=768 paired decision observations and96 eight-answer jobs per reader/arm. The512 stress contributes192 observations and24 jobs. Shared worlds across seeds/arms are repeated comparisons, not independent random problems. Secondary all-task outputs are also saved to avoid hiding errors outside the selected targets.

World hashes excluding their ID have zero exact train/confirmation overlap and zero overlap with{prep['historical_fingerprints_checked']} retained SH01 fixture fingerprints. New dependencies are distributed across regions. Public prerequisite identities remain supplied metadata; the model predicts the same immediate-prerequisite/freeze/completion rule, not unfamiliar transitive reasoning.

## 3. HSA primary result (exclude easy all-DEFER controls)

| Source tasks | Untouched U | Small-only S | Mixed-size M | Whole eight-answer jobs U → M |
|---|---|---|---|---|
{chr(10).join(rows)}

The512 row is separate beyond-training-size stress, not pooled primary qualification. Mixed preparation trains only through128 tasks.

At128 tasks, wrong selected answers fall19→2, and entirely correct jobs rise80/96→94/96. M meets the prospective descriptive95%decision/90%represented-class macro recall/90%whole-job working points at8,32,128. At512 it reaches98.4375% selected-answer accuracy but87.5% whole-job accuracy, below the90% job working point. That known stress limitation stays open rather than triggering further tuning.

Eight-task retention is100% for every HSA M parent: all768 selected/all-task answers and96 jobs correct. It repairs the one pre-existing miss and introduces no eight-task errors. This is retention of this narrow rule, not companion identity or broad skill retention.

### Paired128-task HSA results
| Parent | U | S | M |
|---|---|---|---|
{chr(10).join(parent)}

M improves on U in two parents and ties its accuracy in the third; it beats S in two and is one answer worse in the third. The effect is not uniformly favorable at every position or seed. S's aggregate128-task accuracy falls to95.052%, despite improving eight-task performance to100%; practice coverage matters in this recipe, not simply more updates.

## 4. Do not hide collateral errors
At128, M fixes all19 of U's originally wrong selected positions but introduces two new errors elsewhere. One is a false BLOCKED on an already-complete task (8802), the other a false COMPLETE on a blocked task (8804). Net improvement19→2 is meaningful, but not error-set-perfect recovery. At32, one pre-existing false COMPLETE from8804 remains. At512, three false READY answers remain; M repairs14 of17 U errors there without introducing new selected errors. All selected failure records retain source identity, prerequisite IDs/progress, predicted/true classes and logits in`failures/SELECTED_BEHAVIORAL_ERRORS.json.gz`.

The full all-task secondary check also improves at128: HSA U11962/12288 (97.347%) → M12275/12288 (99.894%), versus S11675/12288. At512 U11178/12288 → M12083/12288. These full-world diagnostics are not the same denominator as selected eight-answer jobs; raw arrays retain all mistakes.

All HSA frozen-control decisions are correct in U/S/M. Dense has isolated frozen-control failures (one U8; one U/S/M512). They are recorded separately rather than blended into the nonfrozen headline.

## 5. Dense comparison: retained but not overclaimed
| Source tasks | U | S | M | M whole jobs |
|---|---|---|---|---|
{chr(10).join(dense)}

Dense receives identical continuation examples and target labels. Its M128 selected accuracy improves77.083%→81.250%;512 improves57.813%→70.833%. It remains substantially weaker on this fixed recipe. The inherited dense parents were already weaker after SH01 training;96 additional updates do not establish that dense attention was optimally prepared or intrinsically cannot solve the task. This is a bounded same-recipe comparison, not a universal architecture ranking.

## 6. Cross-segment compatibility after learning
All six M endpoints were checked on the first nonfrozen32- and128-task confirmation worlds using unchanged CAP01 streaming with32 active record positions. All12 checks completed. Full first-layer/selected-second-layer outputs, stream logits and prepared resident logits were compared against the original same-weight resident source reader.

Across{scalars:,} scalar comparisons there were **{violations} tolerance violations** and zero class differences. The unchanged float32 envelope is`2e-5 + 2e-5*abs(reference)`; maximum absolute discrepancy6.198883056640625e-6. Peak counted active positions remained32. These12 checks establish compatibility on their declared subset, not streamed execution of every confirmation world or32-token/total-memory training.

CAP01 previously showed ordinary multi-pass retrieval can obtain the same capacity. This training comparison does not reassign that gain to custom segmented grouping.

## 7. Verification, operational incidents and costs
Preflight passed12 named checks: four compiler-byte tests, two packed-vs-masked output/gradient tests, independent labels, deterministic optimizer resume/parent isolation, three injected faults, and paired schedule/target counts. Three disposable optimizer applications tested exact resume. Source/input lock contains18 objects and remained intact.

All12 trained branches finished96 steps. All18 U/S/M endpoints were evaluated on all130 worlds:2340 endpoint/world records,18720 selected decision observations,and213120 all-task prediction observations. Independent vector/scalar recount found zero discrepancies. All60 continuation checkpoint parameter hashes and parent links matched. A fresh process replayed every endpoint/world logit array bit-for-bit (18 files,2340 worlds,852480 score scalars); zero replay mismatches. This is internal repeatability, not third-party replication.

One pre-lock syntax error in the new evaluation record writer was caught before data preparation or model work. The two rejected parse attempts and failed source are retained; no optimizer work occurred. The closing brace was repaired before preflight/main lock. No main interruption, replacement, budget extension, post-result recipe change, numerical-gate relaxation, or extra optimizer step occurred.

Tracked main command cores summed{main_s:.3f}s including training precompilation, training, endpoint evaluation and the12 streaming checks. This excludes interpreter/import overhead outside the timers, source writing, fixture preparation({prep['seconds']:.3f}s),preflight({preflight['seconds']:.3f}s),post-result audit({A['seconds']:.3f}s),packaging and analysis. It is NOT the entire research wall time. Peak recorded main-process RSS was{rss:,}bytes and includes resident training/evaluation, framework and plan allocations; it is not a32-record or per-policy memory claim. No per-method speed comparison or energy measurement was conducted.

## 8. Bounded closeout
Retain segmented context + three-level HSA as an executable maintenance component with explicit information/state/cost boundaries. Preserve exact original checkpoints and this fixed mixed-preparation candidate; do not adopt a new NSS serving model from a synthetic result.

This pass gives a positive answer to the narrow outstanding preparation question: a small multi-size training phase can improve use of expanded evidence while preserving the tested small task. It is enough to stop polishing this subproblem. Keep512-layout errors, dense-baseline adequacy, total-memory/long-term lifecycle costs, and language-token interfaces as recorded limits for later integration—not automatic invitations to launch another study.

Next research work can move to the next component, with DARP's maintenance-output concept the previously discussed candidate. No DARP implementation or other follow-on execution is authorized or performed here. None of these results qualifies natural-language context,25,000-token operation,general memory/identity,autonomous night repair,or a full NSS architecture.

## Evidence map
- `PROTOCOL.md`, `SOURCE_FIXTURE_LOCK.json`: prospective scope and frozen identities.
- `source/`: standalone runner and unchanged reused HSA/streaming modules.
- `parents/`, `checkpoints/`: exact parents and all60 continuation states, optimizers and RNG/cursors.
- `fixtures/`: common raw training/confirmation worlds and target selections.
- `results/`: per-update logs, all endpoint logits, summaries, continuation/streaming receipts and audits.
- `failures/`: pre-lock parse incident and every selected behavioral error.
- `audit/`: separately labeled post-result recount/replay/publishing code.

No SH01,SH02,SC01,SC02,CAP01,or earlier NSS outcome was rewritten.
'''
(R/'REPORT.md').write_text(report)
review='''# CAP02 Codex review handoff v0.1

User explicitly wanted ONE final preparation/retention check, then no prolonged segmented-context/HSA polishing. This is completed; preserve that pacing. Do not turn the remaining512-task stress into an automatic new campaign.

Read REPORT.md, PROTOCOL.md and results/SUMMARY.json. U/S/M are untouched/small-only/mixed8-32-128. Six exact parents,12 continuations,96 steps each;1152 main+3 disposable applications. HSA128 improves749/768→766/768;whole80/96→94/96;small8 becomes768/768. Equal-update small-only128 is730/768. All three HSA M parents retain eight-task competence, but M vs S is not uniformly superior for every seed. Full all-task outputs also retained.

Important negative: HSA M128 repairs19 U errors but introduces2 new errors (one false COMPLETE). HSA512 stress189/192 with21/24 whole jobs misses90%whole-job criterion. No more training followed. Dense parents were already weaker; do not claim best-prepared baseline superiority. Fixed supervised-label budget does not imply equal total source information/compute.

All12 updated mixed endpoints' cross-segment checks matched source numeric envelope;89952 compared scalars,0 breaches,0 class disagreements. All2340 evaluated world records independently recounted; all18 complete output files exact fresh-process replay;60 checkpoint hash matches. Original18 lock entries unchanged. Source parse error before any prep/model work retained;no main interruption.

Recommended research disposition: bounded working component PARKED FOR INTEGRATION. Preserve original and mixed HSA checkpoints as reference/candidate, not serving-model adoption. Any later revisit should be tied to an actual downstream requirement, not a quest for perfection. DARP remains output architecture applied to maintenance outputs; not executed in this pass.

Review raw evidence and note any material correctness errors, but do not infer full NSS,language tokens,autonomous repair,identity retention,or unique custom segmented-grouping advantage from this study.
'''
(R/'CODEX_REVIEW.md').write_text(review)
(R/'README.md').write_text('''# CAP02 execution bundle

Fixed-budget preparation diagnostic for the existing typed NSS maintenance reader. See REPORT.md for results and limitations; PROTOCOL.md defines prospective decisions. Runnable on the recorded Python/PyTorch/NumPy CPU environment in SOURCE_FIXTURE_LOCK.json; no remote model required.

All scientific work is already complete. Do not rerun training into this directory. To independently reproduce, copy the bundle to a new output directory, retain parents/source/fixtures/protocol and remove generated checkpoints/results/audit outputs as appropriate; new run IDs and receipts must be used. `python source/cap02.py train --seed 8801` performs four96-step continuations; repeat only as a separately authorized replication, not repair of historical outcomes. The source preparation function's historical overlap check expects the supplied SH01 archive; serialized source fixtures make it unnecessary for replay.

For inference/count auditing of retained outputs: `python audit/recount_and_replay.py`. This writes audit/summary files, not training checkpoints. Use a copy to preserve delivered bytes. `source/cap02.py stream --seed ...` repeats the declared selected mixed-endpoint32-position checks, not new training.

Archive includes parent states, all60 original continuation checkpoints, raw fixtures, every endpoint output and the complete training journals. Zip hashes and the manifest detect accidental corruption; they are not authenticated adversarial storage.
''')
outcome={'status':'COMPLETE_BOUNDED_PREPARATION','component_disposition':'PARKED_FOR_INTEGRATION','utc':datetime.now(timezone.utc).isoformat(),
 'main_updates':1152,'preflight_updates':3,'total_updates':1155,'continuation_branches':12,'parent_models':6,'new_random_fits':0,
 'endpoint_files':18,'world_rows':2340,'stream_checks':12,'numerical_violations':violations,'main_core_seconds':main_s,
 'main_peak_rss_bytes':rss,'no_follow_on_run':True}
(R/'OUTCOME.json').write_text(json.dumps(outcome,indent=2))
# Build manifests excluding themselves and runtime caches.
for p in list(R.rglob('__pycache__')):shutil.rmtree(p)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):
 files={str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
 (root/'MANIFEST.json').write_text(json.dumps({'schema':'nss.package.manifest.v1','files':files},sort_keys=True,indent=2));return len(files)
def archive(root,name):
 count=manifest(root);p=OUT/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for x in sorted(root.rglob('*')):
   if x.is_file():z.write(x,root.name+'/'+str(x.relative_to(root)))
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  man=json.loads(z.read(root.name+'/MANIFEST.json'))
  for rel,d in man['files'].items():
   b=z.read(root.name+'/'+rel);assert len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256']
 return {'file':p.name,'bytes':p.stat().st_size,'sha256':digest(p),'manifest_payloads':count,'crc':'PASS','all_payload_hashes':'PASS'}
full=archive(R,'NSS_NBR02_CAP02_Execution_v0.1.zip')
reviewroot=OUT/'NSS_NBR02_CAP02_Codex_Review_v0.1';reviewroot.mkdir(exist_ok=False)
for rel in ['REPORT.md','CODEX_REVIEW.md','PROTOCOL.md','README.md','OUTCOME.json','SOURCE_FIXTURE_LOCK.json','provenance/INPUT_AUDIT.json','results/SUMMARY.json','results/AUDIT.json','results/PREFLIGHT.json','results/PREPARATION.json']:
 d=reviewroot/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/rel,d)
for p in (R/'source').rglob('*.py'):
 d=reviewroot/'source'/p.relative_to(R/'source');d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,d)
for p in (R/'results').glob('STREAM_*.json'):shutil.copyfile(p,reviewroot/'results'/p.name)
small=archive(reviewroot,'NSS_NBR02_CAP02_Codex_Review_v0.1.zip')
for src,dest in [('REPORT.md','NSS_NBR02_CAP02_Report_v0.1.md'),('CODEX_REVIEW.md','NSS_NBR02_CAP02_Codex_Review_v0.1.md')]:shutil.copyfile(R/src,OUT/dest)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'archives':[full,small],
 'standalone_report':{'file':'NSS_NBR02_CAP02_Report_v0.1.md','sha256':digest(OUT/'NSS_NBR02_CAP02_Report_v0.1.md')},'report_matches_package':True}
(OUT/'NSS_NBR02_CAP02_Delivery_v0.1.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
