"""Allocate and freeze execution details before generating any numerical cases."""
from __future__ import annotations
import hashlib,json,re,shutil,time,platform,sys,os
from pathlib import Path
from common import ROOT,base,sha,canonical,dump,load
r=base();plan=Path('/mnt/data/cm01_work/plan/NSS_Context_Management_v0.1')
if (ROOT/'protocol/SOURCE_LOCK.json').exists():raise FileExistsError('Protocol already frozen')
namespace='NSS-CM01-EXEC-v0.2'
scanned=[];reserved=set(range(6000,9001));total=0
inputs=[p for p in r.rglob('*') if p.is_file() and p.suffix.lower() in {'.py','.json','.md','.txt','.jsonl','.csv'}]
inputs+=list(plan.glob('*.md'))+list(plan.glob('*.json'))+[Path('/mnt/data')/x for x in ('CANDIDATES_v1.0.md','ANALYSIS.md','CHAT_PROMPT.md')]
for p in inputs:
    raw=p.read_bytes();text=raw.decode('utf-8',errors='replace')
    if namespace in text:raise ValueError('Seed namespace previously present')
    reserved.update(int(x) for x in re.findall(r'(?<![0-9])[0-9]{1,20}(?![0-9])',text))
    scanned.append({'path':str(p.relative_to(r)) if p.is_relative_to(r) else str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()});total+=len(raw)
families=['CMFIX-00','CMDEV-01','CMDEV-02','CMDEV-03']+[f'CMEVAL-{i:02d}' for i in range(1,6)]
seeds={};used=set()
def assign(label):
    b=f'{namespace}/{label}'.encode();x=int.from_bytes(hashlib.sha256(b).digest()[:8],'big')
    if x==0 or x in reserved or x in used:raise ValueError('Seed collision: '+label)
    used.add(x);seeds[label]=x
for f in families:
    assign(f+'/root')
    for unit in (1,2,3,5,6,7,8):
        for j in ([0] if f=='CMFIX-00' else range(8)):
            for c in ('graph','treatment','close','query','identifiers'):assign(f'{f}/s{unit}/j{j}/{c}')
dump(ROOT/'protocol/SEEDS.json',{'namespace':namespace,'derivation':'first 8 bytes of SHA256(UTF8(namespace + / + label)), unsigned big-endian','seeds':seeds,'pcg':'numpy.random.PCG64','unbound_pair_reuse':'strata 3 and 4 intentionally use the same s3 seeds and public state','model_seeds_reused':list(range(1201,1206))})
dump(ROOT/'protocol/SEED_ALLOCATION_AUDIT.json',{'status':'PASS_AGAINST_RETAINED_INPUTS_AND_DECLARED_RESERVED_NUMBERS','allocated_seeds':len(seeds),'distinct_allocated_seeds':len(used),'input_files_scanned':len(scanned),'bytes_scanned':total,'reserved_numeric_values':len(reserved),'collision_count':0,'scope':'All retained text/JSON/Python/CSV records in compact baseline and latest plan plus original Codex handoff. Cannot audit missing historical RNG histories or unmaterialized past random draws. Reuse of five fixed model seeds intentional.','scan_files':scanned})
protocol={
 'id':'NSS_CM01_Execution_v0.2','parent_plan':'NSS_Context_Management_v0.1 / CM-01 (512 records), not the earlier MC draft',
 'authorization':'Current user request: Let us run our tests. Numerical execution of first bounded pilot; no authorization inferred for training or auto-launch of CM02-CM05.',
 'frozen_epoch':time.time(),'training':False,'main_exports_frozen':15,'primary_role':'near','roles':['ordinary','near','attention'],'model_seeds':list(range(1201,1206)),
 'codec':{'name':'UTF8_BYTE_V1','serialized_bytes':56,'cap_symbols':64,'meaning':'one ASCII byte is one experimental control symbol, not a language-model token',
          'packed_semantic_fields_bytes':26,'grammar':'01|8hex_scope|16hex_handle|8hex_revision|16hex_binding_event|R/U/H',
          'R':'all numeric fields positive','U':'all numeric fields zero','H':'all zero or complete untrusted positive proposal; always fall back'},
 'main':{'families':families[1:],'development':3,'heldout':5,'strata':8,'records_per_stratum':8,'records':512,'forward_variants_per_case_max':2,'forwards_cap':15360,'interface_rows':23040,'nonneural_control_rows':1024},
 'fixture':{'family':'CMFIX-00','records':8,'one_per_stratum_with_j0':True,'model_seed':1201,'roles':3,'forwards_cap':48,'interface_rows':72,'nonneural_control_rows':16},
 'total_capture_replay_forward_cap':30816,'max_seconds_from_preflight':7200,'max_process_tree_rss_bytes':4294967296,'seed_file_sha256':sha(ROOT/'protocol/SEEDS.json'),
 'family_recipe':{'source_generator':'Q010 make_case, path length 1, depth 1, initially 16 valid records, all active catalogue codes','graph_and_id_seeds_separate':True,
                 'query':'normalize known anchor first16 + PCG64 Gaussian, then append 0; sigma .01 for j%4<2 else .2',
                 'close':'reserved unrelated decoy moved to normalized source+.01 Gaussian; change book/keys/values consistently, not graph truth',
                 'row_order':'original independently shuffled physical rows',
                 'known_absent':'s3/s4 same history,K,V,valid,Q,catalogue,scope,workspace; opposite protected origin labels'},
 'completion_of_open_design_details':{
  'stale_revision':'j0-3 revision payload update; j4-7 delete source record; each subgroup sigma-balanced 2+2. Workspace stays at earlier revision. Revision has known new-content truth; deletion expects UNKNOWN.',
  'cross_scope':'restore a workspace from a genuinely observed foreign-task/namespace selection; current numerical query remains for known current-store source',
  'wrong_reference':'j0-3 handle replacement preserving true selection-event ID (detectable); j4-7 consistent public selection of near decoy but hidden intent remains original source (no-cue). No-cue alternate label diagnostic reuses evidence and creates no extra forwards.',
  'correction_conflict':'j0-3 explicit binding correction; j4-7 unresolved competing bindings. Two per sigma in each subgroup; correction rewrites workspace; conflict emits H then original-Q fallback.',
  'controller':'fixed streaming event manager creates workspace from observed selection/correction, retains across ordinary events; injected faulty checkpoints explicitly labelled. Separate retained indexes are counted.',
  'public_api':'current scope/task, observed journal and retained workspace only; producer cannot open protected ledger; model receives original sanitized K/V/valid and either original or canonical Q',
  'route':'R validates scope; indexed binding lookup then indexed current record lookup (max2). Missing or conflict => original; observable mismatch/revision/delete => management abstention; valid => canonical journal query code',
  'controls':'public exact lookup reads observed payload when same binding validates; otherwise UNKNOWN with no fuzzy fallback. Privileged exact-owner reads actual source row using isolated ownership/source ledger and original independent decoder.',
  'resolver':'original Q010 catalogue-assisted resolve_code unchanged; not a pure raw-vector answer decoder',
  'always_on_interpretation':'bounded resident workspace, available at each relevant operation and rewritten on selected events; this pilot has one learned read per case, not native recurrent token-state coupling'
 },
 'decision_rules':{'bound_close_gain_pp':10,'near_families_required':4,'heldout_families':5,'bound_known_loss_pp_max':1,'observable_invalid_false_acceptance_max':.05,'no_tuning':True,'B_C_exact_required':True,'protected_input_leakage':0,'no_cue_and_matched_pairs':'report-only information limits; no fitted gate'},
 'accounting':'All attempted logical forwards and physical batches, producer/replay separately, independent arithmetic replays not model forwards; every error and negative retained. Explicit byte/traffic costs, journal and reference index overhead counted.',
 'baseline_limits':['no full main optimizer/RNG checkpoints','raw main numeric training traces absent','compact baseline excludes bulk original capture/replay','underflow v2 is retained reconstruction, not lost original source/row','historical verifier errors remain','no global NSS or native recurrence qualification'],
 'dependencies':{'baseline_zip':'Q010_InferenceRecovery_v1.6_RecoveryContext.zip','baseline_zip_sha256':'9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e','planning_zip_sha256':sha('/mnt/data/NSS_Context_Management_v0.1.zip')},
}
dump(ROOT/'protocol/PROTOCOL.json',protocol)
for name in ['CANDIDATES_v0.1.md','HANDOFF.md','WORKSPACE_CONTRACT_PROPOSAL.json','RESEARCH_ADDENDUM.md']:
 shutil.copy2(plan/name,ROOT/'provenance'/name)
for name in ['protocol/UNDERFLOW_AMENDMENT_ORIGINAL.md','audit/UNDERFLOW_RECONSTRUCTION.diff','audit/FRESH_MAIN_UNDERFLOW_REJECTION.json','audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz']:
 dst=ROOT/'provenance/underflow'/Path(name).name;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(r/name,dst)
for name in ['pointer_math.py','pointer_math_frozen.py']:
 shutil.copy2(r/'source/q010v'/name,ROOT/'provenance/underflow'/name)
# Record every executable baseline source and all 15 exports, not historical bulk arrays.
bfiles={str(p.relative_to(r)):sha(p) for p in r.rglob('*.py') if '__pycache__' not in p.parts}
for folder in ['protocol','provenance/saved_main_exports']:
 for p in (r/folder).glob('*'):
  if p.is_file():bfiles[str(p.relative_to(r))]=sha(p)
lock={'protocol_sha256':sha(ROOT/'protocol/PROTOCOL.json'),'study_files':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'source').glob('*.py')},'baseline_files':bfiles,'seed_file_sha256':sha(ROOT/'protocol/SEEDS.json'),'frozen_before_any_fixture_or_main_generation':True,'frozen_epoch':time.time()}
# The seed file is also checked in the study-file map.
lock['study_files']['protocol/SEEDS.json']=sha(ROOT/'protocol/SEEDS.json')
dump(ROOT/'protocol/SOURCE_LOCK.json',lock)
dump(ROOT/'audit/HOST.json',{'platform':platform.platform(),'python':sys.version,'cpu':platform.processor(),'cpu_count':os.cpu_count(),'libraries':{x:__import__(x).__version__ for x in ('numpy','torch','safetensors','psutil')},'device':'CPU','torch_threads':1,'deterministic_algorithms':True})
print(json.dumps({'status':'FROZEN_BEFORE_NUMERICAL_EXECUTION','new_numeric_seeds':len(seeds),'files_scanned':len(scanned),'bytes_scanned':total,'locked_study_sources':len(lock['study_files']),'locked_baseline_files':len(bfiles),'source_lock_sha256':sha(ROOT/'protocol/SOURCE_LOCK.json')},indent=2))
