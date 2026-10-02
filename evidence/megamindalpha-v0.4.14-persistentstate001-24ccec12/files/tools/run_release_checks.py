#!/usr/bin/env python3
"""Retain actual local verification output OUTSIDE the repository being checked.

Not a neural benchmark, security audit or release-authority implementation.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--timeout',type=int,default=1200);args=parser.parse_args()
    if args.timeout<1:parser.error('Timeout must be positive')
    output=Path(args.output).resolve()
    if output==ROOT or output.is_relative_to(ROOT):parser.error('Evidence output must be outside the release tree')
    output.mkdir(parents=True,exist_ok=True)
    scripts=['tools/generate_experience_schemas.py','tools/generate_dataset_schemas.py','tools/generate_evaluation_schemas.py',
             'tools/generate_subsystem_logic.py',
             'tools/generate_qualification_schemas.py',
             'tools/generate_permission_schemas.py','tools/generate_generation_schemas.py','tools/generate_learner_schemas.py']
    regeneration="""from pathlib import Path
import subprocess,sys
root=Path('.')
paths=list(root.glob('schemas/*.json'))+[root/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',root/'docs/DATASET_SNAPSHOT_LOGIC.md',root/'docs/EVALUATION_RUN_LOGIC.md',root/'docs/NEURAL_PROBE_LOGIC.md',root/'docs/QUALIFICATION_EVIDENCE_LOGIC.md',root/'fixtures/qualificationevidence002/policy.json',root/'fixtures/localnexuspermissions002/policy.json',root/'docs/LOCAL_NEXUS_PERMISSIONS_LOGIC.md',root/'docs/OVERLAY_GENERATION_LOGIC.md',root/'docs/OVERLAY_CATALOG_LOGIC.md',root/'docs/CONTEXT_RETRIEVAL_LOGIC.md',root/'docs/BOUNDED_LEARNER_LOGIC.md',root/'docs/CANDIDATE_ACCEPTANCE_LOGIC.md',root/'docs/PERSISTENT_STATE_LOGIC.md',root/'fixtures/overlaygenerationmanager001/policy.json']+list(root.glob('docs/logic_flowcharts/*.dot'))
before={str(p):p.read_bytes() for p in paths}
for script in SCRIPTS:subprocess.run([sys.executable,script],check=True)
changed=[p for p,b in before.items() if Path(p).read_bytes()!=b]
print('REGEN_CHANGED',changed)
raise SystemExit(bool(changed))
""".replace('SCRIPTS',repr(scripts))
    helpers="""from nss_base.logic_atlas import load_atlas
for path,count in [('spec/dataset_snapshot_flows.json',2),('spec/evaluation_run_flows.json',3),('spec/neural_probe_flows.json',3),('spec/qualification_evidence_flows.json',3),('spec/local_nexus_permissions_flows.json',3),('spec/overlay_generation_flows.json',3),('spec/overlay_catalog_flows.json',3),('spec/context_retrieval_flows.json',3),('spec/bounded_learner_flows.json',3),('spec/candidate_acceptance_flows.json',3),('spec/persistent_state_flows.json',3)]:
 a=load_atlas(path);assert len(a['flows'])==count;print(path,':',count,'valid subordinate flows')
"""
    commands=[('unittest',[sys.executable,'-m','unittest','discover','-s','tests','-v'])]
    for module in ('experiment001a','experiment001b','stagehandoff001','experiencearchive001','datasetsnapshot001','evaluationrun001'):
        commands.append((module,[sys.executable,'-m','nss_base.'+module]))
    commands.append(('neuralprobe001',[sys.executable,'-m','nss_base.neuralprobe001','--directory',str(output/'neuralprobe-run')]))
    commands.append(('qualificationevidence002',[sys.executable,'-m','nss_base.qualificationevidence002','--directory',str(output/'qualification-run')]))
    commands.append(('localnexuspermissions002',[sys.executable,'-m','nss_base.localnexuspermissions002','--directory',str(output/'permission-run')]))
    commands.append(('overlaygenerationmanager001',[sys.executable,'-m','nss_base.overlaygenerationmanager001','--directory',str(output/'generation-run')]))
    commands.append(('overlaycatalogcontroller001',[sys.executable,'-m','nss_base.overlaycatalogcontroller001','--directory',str(output/'catalog-run')]))
    commands.append(('contextretrieval001',[sys.executable,'-m','nss_base.contextretrieval001','--directory',str(output/'context-run')]))
    commands.append(('boundedlearnercoordinator001',[sys.executable,'-m','nss_base.boundedlearnercoordinator001','--directory',str(output/'learner-run')]))
    commands.append(('connected_alpha_acceptance',[sys.executable,'tools/verify_connected_alpha.py','--summary',str(output/'learner-run/summary.json')]))
    commands.append(('candidateacceptance001',[sys.executable,'-m','nss_base.candidateacceptance001','--directory',str(output/'candidate-run')]))
    commands.append(('candidate_connected_acceptance',[sys.executable,'tools/verify_connected_alpha.py','--summary',str(output/'candidate-run/summary.json')]))
    commands.append(('persistentstate001',[sys.executable,'-m','nss_base.persistentstate001','--directory',str(output/'persistent-state-run')]))
    commands.append(('maintenance',[sys.executable,'tools/audit_maintenance.py']))
    commands.append(('fresh_exact_neural_evidence',[sys.executable,'tools/verify_fresh_neural_evidence.py','--report',str(output/'neuralprobe-run/report.json')]))
    commands.append(('historical_portability_audit',[sys.executable,'tools/audit_historical_neural_metrics.py']))
    commands.append(('reference_neural_evidence',[sys.executable,'tools/verify_neural_evidence.py']))
    commands.extend([('atlas',[sys.executable,'-m','nss_base.logic_atlas']),('helper_graphs',[sys.executable,'-c',helpers]),
        ('dependencies',[sys.executable,'tools/check_dependencies.py']),('compile',[sys.executable,'-m','compileall','-q','nss_base','tests','tools']),
        ('regeneration',[sys.executable,'-c',regeneration]),('manifest',[sys.executable,'tools/verify_manifest.py'])])
    evidence={'version':(ROOT/'VERSION').read_text().strip(),'started_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'platform':platform.platform(),'root':str(ROOT),'command_timeout_seconds':args.timeout,'gates':[]}
    for name,command in commands:
        t=time.monotonic()
        try:
            run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=args.timeout)
            text=run.stdout+run.stderr;code=run.returncode
        except subprocess.TimeoutExpired as exc:
            text='TIMEOUT\n'+str(exc);code=124
        (output/(name+'.txt')).write_text(text)
        evidence['gates'].append({'name':name,'command':command,'exit_code':code,'seconds':round(time.monotonic()-t,3),
            'log_sha256':sha256(text.encode()).hexdigest(), 'required':name!='reference_neural_evidence'})
        print(name,code,flush=True)
    evidence['passed']=all(g['exit_code']==0 for g in evidence['gates'] if g['required'])
    evidence['all_gates_passed']=all(g['exit_code']==0 for g in evidence['gates'])
    evidence['advisories']=[g['name'] for g in evidence['gates'] if not g['required'] and g['exit_code']!=0]
    evidence['advisory_policy']='Legacy schema-v1 archive remains historical and raw strict-MSE disagreement remains visible. New schema-v2 evidence binds CPU/build/backend policy and requires exact replay through the same sealed-checkpoint path. Historical diagnosis is NOT qualification or permission.'
    evidence['completed_utc']=datetime.now(timezone.utc).isoformat()
    (output/'summary.json').write_text(json.dumps(evidence,indent=2)+'\n')
    return 0 if evidence['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
