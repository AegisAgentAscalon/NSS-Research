#!/usr/bin/env python3
"""Verify this documentation bundle; no model loading, learning or scientific replay."""
from pathlib import Path
import hashlib, json, re, sys

def main() -> int:
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text())
    failures=[]
    for row in manifest['files']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            failures.append('Unsafe path: '+str(rel));continue
        p=root/rel
        if not p.is_file():failures.append('Missing: '+str(rel));continue
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
            failures.append('Changed: '+str(rel))
    s=json.loads((root/'STATUS.json').read_text())
    requirements={
      'workspace_branch_status':'PARKED_OPEN',
      'nbr01_closeout':'PROPOSED_NOT_ADOPTED',
      'nbr02_status':'PROTOCOL_PREPARATION_RECOMMENDED_NOT_DISPATCHED',
      'nbr02_protocol_execution_ready':False,
      'nbr02_execution_authorized':False,
      'current_turn_new_fits':0,'current_turn_model_loads':0,
      'current_turn_optimizer_updates':0,'current_turn_model_forwards':0,
      'current_turn_numerical_replays':0,
      'parent_architecture_bytes_changed':False,
      'scientific_claims_changed':False,'historical_scores_changed':False
    }
    for k,v in requirements.items():
        if s.get(k)!=v:failures.append('Wrong status: '+k)
    r=json.loads((root/'REGISTERS.json').read_text())
    if r['all_revived_question_ids'] != [f'G{i:02d}' for i in range(1,23)]: failures.append('Question ID loss')
    rows=re.findall(r'^\| (G\d{2}) \|',(root/r['revived_question_source']).read_text(),re.M)
    if rows!=r['all_revived_question_ids']:failures.append('Question source rows mismatch')
    for group in ('log_records','return_tickets','phase_decisions','freeze_items'):
        for item in r[group]:
            if not (root/item['path']).is_file():failures.append('Missing register target:'+item['id'])
    # Independent integer check of the review's budget observation.
    scheduled=2*4*(100+(24+48)*6)+2*50
    spare=4900-scheduled
    condition_replay=2*4*(24+48)*6
    if (scheduled,spare,condition_replay)!=(4356,544,3456):failures.append('Arithmetic mismatch')
    out={'pass':not failures,'manifest_files':len(manifest['files']),
         'revived_questions':len(rows),'current_turn_model_forwards':0,
         'optimizer_updates':0,'scope':'Documentation integrity/status/arithmetic, not scientific verification',
         'budget_review':{'scheduled':scheduled,'remaining':spare,'full_condition_replay':condition_replay},'failures':failures}
    print(json.dumps(out,indent=2))
    return 0 if not failures else 1
if __name__=='__main__':sys.exit(main())
