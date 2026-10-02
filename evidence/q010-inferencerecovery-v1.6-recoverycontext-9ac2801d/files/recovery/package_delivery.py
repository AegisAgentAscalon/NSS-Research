"""Lossless package, independent extraction checks, and explicit compact context.

Run only after the study and reports have completed. Never removes raw evidence.
No trainer, optimizer, or scientific evaluator is imported by this packager.
"""
from __future__ import annotations
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent
WORK = OUT / 'q010_deliverycheck'
FULL = OUT / (ROOT.name + '_Complete.zip')
COMPACT = OUT / (ROOT.name + '_RecoveryContext.zip')
RECEIPT = OUT / (ROOT.name + '_Delivery.json')
LOCK = (ROOT / 'protocol/RECOVERY_SOURCE_LOCK.sha256').read_text().strip()
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


def sha(path: Path) -> str:
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')


def files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Symlink rejected: {p}')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
            out.append(p)
    return sorted(out, key=lambda p: p.relative_to(root).as_posix())


def info(path: Path) -> dict:
    return {'bytes': path.stat().st_size, 'sha256': sha(path)}


def make_zip(path: Path, pairs: list[tuple[Path, str]]) -> dict:
    if path.exists() or path.with_suffix('.partial').exists():
        raise FileExistsError(path)
    tmp = path.with_suffix('.partial')
    start = time.monotonic()
    with zipfile.ZipFile(tmp, 'x', allowZip64=True) as z:
        for p, name in pairs:
            # NPZ and original input ZIPs already contain compression.
            mode = zipfile.ZIP_STORED if p.suffix.lower() in {'.npz', '.zip', '.xz', '.gz'} else zipfile.ZIP_DEFLATED
            z.write(p, name, compress_type=mode, compresslevel=None if mode == zipfile.ZIP_STORED else 6)
    with zipfile.ZipFile(tmp) as z:
        bad = z.testzip()
        if bad is not None:
            raise ValueError('ZIP CRC failure: ' + bad)
        count = len(z.infolist())
    os.replace(tmp, path)
    result = {'filename': path.name, **info(path), 'zip_members': count,
              'crc_check': 'PASS', 'build_and_crc_seconds': time.monotonic()-start}
    print(json.dumps({'event': 'ZIP_BUILT', **result}), flush=True)
    return result


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            target = destination / member.filename
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError('Unsafe ZIP path')
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('ZIP symlink rejected')
        z.extractall(destination)


def command(name: str, args: list[str], cwd: Path) -> dict:
    base = WORK / 'checks' / name
    base.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t = time.monotonic()
    with (base/'stdout.log').open('w') as so, (base/'stderr.log').open('w') as se:
        run = subprocess.run([sys.executable, *args], cwd=cwd, env=ENV,
                             stdout=so, stderr=se, timeout=1800, check=False)
    rec = {'name': name, 'argv': [sys.executable, *args], 'cwd': str(cwd),
           'start_utc': started, 'wall_seconds': time.monotonic()-t,
           'exit_code': run.returncode,
           'stdout': (base/'stdout.log').read_text(),
           'stderr': (base/'stderr.log').read_text()}
    write(base/'RECEIPT.json', rec)
    print(json.dumps({'event': 'DELIVERY_CHECK', 'name': name,
                      'exit_code': run.returncode, 'wall_seconds': rec['wall_seconds']}), flush=True)
    if run.returncode:
        raise RuntimeError('Delivery check failed: '+name)
    return rec


def compact_selection(name: str, locked: set[str]) -> bool:
    if name in locked:
        return True
    if name in {'REPORT.md','STATUS.json','README.md','START_HERE_SOURCE_REPAIR.md'}:
        return True
    if name.startswith(('audit/','protocol/','recovery/','source/','tools/','tests/',
                        'failures/','logs/','results/analysis/','results/integration_fixture/')):
        return True
    if name.startswith('results/') and name.count('/') == 1:
        return True
    if name.startswith('results/main/'):
        if '/score/' in name:
            return True
        if name.endswith(('/START.json','/CAPTURE.json','/EXACT_REPLAY.json')):
            return True
        return False
    if name.startswith('provenance/'):
        return not name.startswith('provenance/input_archives/')
    if name.startswith('workspace/'):
        # Preserve source, configuration, parent exports and small legacy summaries,
        # not inherited raw demo captures or unsafe torch-pickle checkpoints.
        return Path(name).suffix.lower() in {'.py','.json','.md','.txt','.csv','.log','.yaml','.yml','.toml','.safetensors'}
    return False


def main() -> None:
    if not (ROOT/'results/EXECUTION_COMPLETE.json').is_file() or not (ROOT/'REPORT.md').is_file():
        raise ValueError('Study and report must be completed before packaging')
    status = json.loads((ROOT/'STATUS.json').read_text())
    if status['query_chains'] != 449640 or status['new_optimizer_updates'] != 0:
        raise ValueError('Unexpected study scope')
    WORK.mkdir(exist_ok=False)
    pkg = ROOT/'PACKAGING'
    pkg.mkdir(exist_ok=False)
    scope = {
        'format':'lossless-sha256-byte-dedup-v1',
        'purpose':'Complete newly recovered inference study, not restored historical training evidence.',
        'included':'All working evidence, source, saved exports, fresh capture/replay data, audit/failure logs, original inputs.',
        'excluded_generated_only':['__pycache__ directories','*.pyc interpreter bytecode'],
        'aliases':'Exact identical bytes are stored once; run RESTORE_IDENTICAL_FILES.py before numerical use.',
        'manifest_self_exclusion':'MANIFEST.json is excluded from its own hash map; the external delivery receipt hashes the full ZIP.',
        'missing_historical_evidence':['Full main optimizer/RNG joint checkpoint payloads remain absent.','Raw main numeric_trace.npz files remain absent; earlier v1.5 verification survives only as a retained audit report.','Fresh main training reproduction was not performed.', *status['limits']],
        'scientific_transformations':[],
    }
    write(pkg/'SCOPE.json',scope)
    records = {}
    canonical = {}
    aliases = {}
    for p in files(ROOT):
        name = p.relative_to(ROOT).as_posix()
        if name in {'MANIFEST.json','PACKAGING/IDENTICAL_FILES.json'}:
            raise ValueError('Pre-existing packaging control file')
        rec = info(p)
        records[name] = rec
        key = (rec['bytes'],rec['sha256'])
        if key in canonical:
            aliases[name] = {'canonical':canonical[key], **rec}
        else:
            canonical[key] = name
    # Neither this index nor the enclosing manifest is recursively deduplicated.
    alias_doc = {'format':'lossless-sha256-byte-dedup-v1','aliases':aliases,
                 'alias_count':len(aliases),'logical_duplicate_bytes':sum(v['bytes'] for v in aliases.values()),
                 'no_lossy_transform':True}
    write(pkg/'IDENTICAL_FILES.json',alias_doc)
    records['PACKAGING/IDENTICAL_FILES.json'] = info(pkg/'IDENTICAL_FILES.json')
    write(ROOT/'MANIFEST.json',{'format':'sha256-logical-files-v1','files':records})
    pairs=[(ROOT/name, ROOT.name+'/'+name) for name in sorted(records) if name not in aliases]
    pairs.append((ROOT/'MANIFEST.json',ROOT.name+'/MANIFEST.json'))
    full = make_zip(FULL,pairs)
    full.update({'logical_files_excluding_manifest_self':len(records),
                 'logical_bytes_excluding_manifest_self':sum(r['bytes'] for r in records.values()),
                 'identical_aliases':len(aliases),'identical_bytes_stored_once':alias_doc['logical_duplicate_bytes']})
    full_dir = WORK/'complete'
    safe_extract(FULL,full_dir)
    extracted = full_dir/ROOT.name
    checks=[]
    checks.append(command('full_logical_integrity_before_restore',['VERIFY_PACKAGE.py'],extracted))
    checks.append(command('full_restore',['RESTORE_IDENTICAL_FILES.py'],extracted))
    checks.append(command('full_physical_integrity_after_restore',['VERIFY_PACKAGE.py'],extracted))
    checks.append(command('full_relocated_saved15_audit',[
        'recovery/worker.py','audit','--output',str(WORK/'full_saved15_audit.json'),'--source-lock',LOCK],extracted))
    newcap=WORK/'full_fixture_capture'
    newscore=WORK/'full_fixture_score'
    checks.append(command('full_relocated_fixture_capture',[
        'recovery/worker.py','capture','--seed','1201','--fixture','--output',str(newcap),'--source-lock',LOCK],extracted))
    checks.append(command('full_relocated_fixture_score',[
        'recovery/worker.py','score','--input',str(newcap),'--output',str(newscore),'--source-lock',LOCK],extracted))
    checks.append(command('full_relocated_fixture_exact_compare',[
        'recovery/worker.py','compare','--input',str(extracted/'results/integration_fixture/capture'),
        '--right',str(newcap),'--output',str(WORK/'full_fixture_exact_compare.json'),'--source-lock',LOCK],extracted))
    newscore_sha=sha(newscore/'QUERY_SCORES.csv')
    expected_sha=sha(extracted/'results/integration_fixture/score/QUERY_SCORES.csv')
    if newscore_sha!=expected_sha:
        raise ValueError('Relocated fixture scoring changed')
    # Compact context has no alias dependencies or claims of complete raw evidence.
    compactroot=WORK/'context_staging'/ROOT.name
    compactroot.mkdir(parents=True,exist_ok=False)
    locked=set(json.loads((ROOT/'protocol/RECOVERY_SOURCE_LOCK.json').read_text())['files'])
    selection=[n for n in records if compact_selection(n,locked)]
    for name in selection:
        dst=compactroot/name
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,dst)
    context_scope={
        'status':'REVIEW_AND_REGENERATION_CONTEXT_NOT_FULL_RAW_EVIDENCE',
        'complete_archive':FULL.name,'complete_archive_sha256':full['sha256'],
        'includes':['all 15 saved main exports and available fit records','all locked numerical source and protocol/criteria',
                    'required inherited parent weights','all fresh per-query scores, aggregate metrics, negatives and verification receipts',
                    'complete integration fixture evidence','original failures and current audit/report material'],
        'omits':['bulk raw main capture and replay array/metadata frames','original uploaded ZIP archives',
                 'most inherited legacy raw fixture arrays and torch-pickle checkpoints','full archive dedup index and manifest'],
        'omitted_logical_files_from_complete':sorted(set(records)-set(selection)),
        'no_training_evidence_recreated':True,
        'use':'Read CONTEXT_START_HERE.md; numerical inference-only regeneration is supported, but absent raw main captures cannot be inspected here.'}
    write(compactroot/'CONTEXT_SCOPE.json',context_scope)
    (compactroot/'CONTEXT_START_HERE.md').write_text('''# Compact Q010 recovery context\n\nThis is a review and inference-regeneration bundle, **not the full raw-evidence archive**.\nRead REPORT.md and CONTEXT_SCOPE.json. The original README describes both delivery variants; its restore/dedup commands apply only to the complete ZIP.\n\nRun `python VERIFY_CONTEXT.py` to verify this context bundle. All selected files are physically present; no alias restoration is needed. The `recovery/worker.py` inference-only commands in README work with new output paths and the recorded numerical dependencies. The complete ZIP named in CONTEXT_SCOPE.json contains the raw main captures/replays and original uploads.\n\nDo not run old training drivers. All fifteen main models remain fixed, and absent raw training traces and full optimizer/RNG checkpoints remain absent.\n''')
    verifier='''from pathlib import Path\nimport hashlib,json\nR=Path(__file__).resolve().parent\nm=json.loads((R/'CONTEXT_MANIFEST.json').read_text())\nfor n,r in m['files'].items():\n p=R/n\n if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(R):raise ValueError('Unsafe/missing member: '+n)\n with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()\n if p.stat().st_size!=r['bytes'] or h!=r['sha256']:raise ValueError('Hash mismatch: '+n)\nprint(json.dumps({'status':'PASS_CONTEXT_FILES','files':len(m['files']),'full_raw_evidence_archive':False}))\n'''
    (compactroot/'VERIFY_CONTEXT.py').write_text(verifier)
    cm={p.relative_to(compactroot).as_posix():info(p) for p in files(compactroot)}
    write(compactroot/'CONTEXT_MANIFEST.json',{'format':'sha256-files-v1','files':cm,'self_excluded':True})
    compact=make_zip(COMPACT,[(p,ROOT.name+'/'+p.relative_to(compactroot).as_posix()) for p in files(compactroot)])
    contextdir=WORK/'context_extracted'
    safe_extract(COMPACT,contextdir)
    context=contextdir/ROOT.name
    checks.append(command('compact_integrity',['VERIFY_CONTEXT.py'],context))
    checks.append(command('compact_relocated_saved15_audit',[
        'recovery/worker.py','audit','--output',str(WORK/'compact_saved15_audit.json'),'--source-lock',LOCK],context))
    checks.append(command('compact_relocated_fixture_capture',[
        'recovery/worker.py','capture','--seed','1201','--fixture','--output',str(WORK/'compact_fixture_capture'),'--source-lock',LOCK],context))
    checks.append(command('compact_relocated_fixture_exact_compare',[
        'recovery/worker.py','compare','--input',str(context/'results/integration_fixture/capture'),
        '--right',str(WORK/'compact_fixture_capture'),'--output',str(WORK/'compact_fixture_exact_compare.json'),'--source-lock',LOCK],context))
    # The original evidence root stays unchanged throughout delivery validation.
    changed=[n for n,r in records.items() if info(ROOT/n)!=r]
    if changed:
        raise ValueError('Working evidence changed after sealing: '+str(changed[:10]))
    receipt={'status':'PASS_COMPLETE_AND_CONTEXT_DELIVERY',
             'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'full':full,'context':compact,'checks':checks,
             'relocated_fixture_score_sha256':newscore_sha,
             'relocated_fixture_scores_match_packaged_fixture':True,
             'working_evidence_unchanged_after_sealing':True,
             'main_models_retrained':0,'new_optimizer_updates':0,
             'historical_training_gaps_restored':False,
             'all_raw_main_cases_and_replays_logically_retained_in_full_zip':True,
             'independence_scope':'Fresh directory/package relocation and data-only verification, not third-party replication.'}
    write(RECEIPT,receipt)
    print(json.dumps({'event':'DELIVERY_COMPLETE','receipt':str(RECEIPT),'full':full,'context':compact}),flush=True)


if __name__=='__main__':
    try:
        main()
    except BaseException as exc:
        import traceback
        p=OUT/(ROOT.name+'_DeliveryFailure_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')+'.json')
        write(p,{'status':'FAIL_DELIVERY','type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc()})
        raise
