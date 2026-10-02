import sys,subprocess,concurrent.futures,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def worker(path,out):
    receipt=out/'receipts'/path.name;log=out/'logs'/path.with_suffix('.log').name
    receipt.parent.mkdir(parents=True,exist_ok=True);log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('w') as f:
        r=subprocess.run([sys.executable,str(ROOT/'tools/verify_results.py'),'--file',path.name,'--replay','--out',str(out/'results'),'--receipt',str(receipt)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError(f'{path.name}: inspect {log}')
    return json.loads(receipt.read_text())
if __name__=='__main__':
    out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=False)
    paths=sorted((ROOT/'evidence/results').glob('*.json'))
    if len(paths)!=45:raise RuntimeError('Expected complete 45 configurations')
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(lambda path:worker(path,out),paths):records.append(result);print('PASS',len(records),flush=True)
    checks=[x for r in records for x in r['checks']]
    result=dict(status='PASS',fresh_interpreter_per_configuration=True,configurations=len(records),metric_rows=sum(c['rows'] for c in checks),
        answer_evaluations=sum(c['snapshot_answers']+c['trace_answers'] for c in checks),checks=checks,all_complete_prediction_and_existence_arrays_replayed=True,
        ground_truth_reconstructed_from_source_events=True,scope='Internal reproduction, not external independent replication')
    (ROOT/'evidence/INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
