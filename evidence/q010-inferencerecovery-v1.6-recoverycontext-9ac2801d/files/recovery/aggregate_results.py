"""Data-only full-matrix coverage and frozen-criteria evaluation. No producer imports."""
from pathlib import Path
from collections import defaultdict
import csv,json,hashlib,datetime,sys
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n')
def csvout(p,rows):
    with p.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    out=ROOT/'results/analysis';out.mkdir(exist_ok=False)
    criteria=read(ROOT/'protocol/RECOVERED_CRITERIA.json');protocol=read(ROOT/'protocol/ORIGINAL_FROZEN_PROTOCOL.json')
    cells=criteria['conditions'];seeds=protocol['main_seeds'];roles=criteria['coverage']['reader_roles_by_seed']
    metrics=defaultdict(lambda:[0,0,0]);totals=defaultdict(lambda:[0,0,0]);seen=set();inputs=[];all_rows=[];stages=0;failures=[]
    combined=out/'ALL_QUERY_SCORES.csv'
    with combined.open('x',newline='') as cf:
        writer=None
        for seed in seeds:
            base=ROOT/f'results/main/seed{seed}';cap=read(base/'capture/CAPTURE.json');start=read(base/'capture/START.json');ver=read(base/'score/VERIFICATION.json');rep=read(base/'EXACT_REPLAY.json')
            if start['split']!='heldout' or start['development_count'] is not None or start['selected_cells'] is not None or cap['cells']!=64:raise ValueError('not full held-out scope')
            if cap['weights_before']!=cap['weights_after']:raise ValueError('weight mutation')
            if rep['status']!='PASS_EXACT_LOCAL_FRESH_PROCESS_REPLAY' or not rep['all_metadata_exact']:raise ValueError('replay did not pass')
            p=base/'score/QUERY_SCORES.csv'
            if sha(p)!=ver['query_scores_sha256'] or sha(base/'capture/CAPTURE.json')!=ver['capture_sha256']:raise ValueError('verification binding')
            inputs.append({'seed':seed,'scores_sha256':sha(p),'capture_sha256':sha(base/'capture/CAPTURE.json'),'verification_sha256':sha(base/'score/VERIFICATION.json'),'replay_sha256':sha(base/'EXACT_REPLAY.json')})
            n=0;dep=0
            with p.open(newline='') as f:
                rd=csv.DictReader(f)
                if writer is None:writer=csv.DictWriter(cf,fieldnames=rd.fieldnames+['reader_role']);writer.writeheader()
                for r in rd:
                    if int(r['seed'])!=seed or r['condition'] not in cells or r['reader'] not in roles[str(seed)]:raise ValueError('score identity outside matrix')
                    role=roles[str(seed)][r['reader']];cls=r['evidence_class'];cp=None if r['checkpoint']=='' else int(r['checkpoint'])
                    key=(seed,r['condition'],cp,r['case_id'],role)
                    if key in seen:raise ValueError('duplicate scored query')
                    seen.add(key)
                    if r['correct'] not in ['True','False'] or r['whole_map_correct'] not in ['True','False']:raise ValueError('non-boolean score')
                    correct=int(r['correct']=='True');mapok=int(r['whole_map_correct']=='True')
                    if bool(correct)!=(r['expected']==r['predicted']):raise ValueError('score not answer equality')
                    if cls not in cells[r['condition']]['role_rules'][role]:raise ValueError('undeclared evidence class')
                    for dest,k in [(metrics,(seed,r['condition'],cp,role,cls)),(totals,(seed,r['condition'],role,cls)),(metrics,('pooled',r['condition'],cp,role,cls)),(totals,('pooled',r['condition'],role,cls))]:
                        dest[k][0]+=correct;dest[k][1]+=1;dest[k][2]+=mapok
                    r['reader_role']=role;writer.writerow(r);all_rows.append(r);n+=1;dep+=int(r['depth'])
            if n!=89928 or dep!=609096 or n!=ver['query_chains'] or dep!=ver['stage_arithmetic_audits']:raise ValueError('incomplete query/stage workload')
            stages+=dep
    # Verify every declared condition/class/reader/seed, including expected zero classes.
    coverage_checks=0;checkpoint_checks=0
    for condition,rule in cells.items():
        for seed in seeds:
            for rid,role in roles[str(seed)].items():
                expected=rule['expected_class_counts_by_seed_reader'][str(seed)][rid]
                for cls,count in expected.items():
                    if totals[(seed,condition,role,cls)][1]!=count:raise ValueError(f'class coverage mismatch {seed} {condition} {role} {cls}')
                    coverage_checks+=1
                grid=rule.get('checkpoint_grid')
                if grid:
                    for cp in grid['checkpoint_values']:
                        expected_cp=grid['expected_class_counts_by_seed_reader_checkpoint'][str(seed)][rid][str(cp)]
                        for cls,count in expected_cp.items():
                            if metrics[(seed,condition,cp,role,cls)][1]!=count:raise ValueError('checkpoint class/stream coverage mismatch')
                            checkpoint_checks+=1
    gate_rows=[]
    for seed in [*seeds,'pooled']:
        for role in ['ordinary','near','attention']:
            for condition,rule in cells.items():
                for cls,gate in rule['role_rules'][role].items():
                    if gate['disposition']!='accuracy':continue
                    if (gate['metric'],gate['operator'])!=('accuracy','>='):raise ValueError('unsupported frozen gate')
                    cps=rule['checkpoint_grid']['checkpoint_values'] if 'checkpoint_grid' in rule else [None]
                    for cp in cps:
                        correct,total,_=metrics[(seed,condition,cp,role,cls)]
                        if total==0:continue
                        rate=correct/total;passed=rate>=gate['threshold']
                        row={'seed':seed,'role':role,'condition':condition,'checkpoint':cp,'evidence_class':cls,'correct':correct,'total':total,'accuracy':rate,'threshold':gate['threshold'],'passed':passed};gate_rows.append(row)
                        if not passed:failures.append(row)
    candidates=[]
    for role in ['ordinary','near','attention']:
        pooled=[r for r in gate_rows if r['role']==role and r['seed']=='pooled'];per=[]
        for seed in seeds:
            rows=[r for r in gate_rows if r['role']==role and r['seed']==seed]
            per.append({'seed':seed,'checks':len(rows),'passed':all(r['passed'] for r in rows),'failures':[r for r in rows if not r['passed']]})
        candidates.append({'role':role,'pooled_gate_checks':len(pooled),'pooled_gate_pass':all(r['passed'] for r in pooled),'pooled_failures':[r for r in pooled if not r['passed']],'per_seed':per,'strict_all_seed_gate_pass':all(r['passed'] for r in per)})
    metric_rows=[]
    for (seed,condition,cp,role,cls),(c,n,m) in sorted(metrics.items(),key=lambda x:tuple(str(k) for k in x[0])):
        if n:metric_rows.append({'seed':seed,'condition':condition,'checkpoint':cp,'role':role,'evidence_class':cls,'correct':c,'total':n,'accuracy':c/n,'whole_map_correct':m,'whole_map_accuracy':m/n})
    csvout(out/'METRICS_ALL_SEEDS_AND_POOLED.csv',metric_rows);csvout(out/'FROZEN_GATE_CHECKS.csv',gate_rows)
    # Unique store/case observations avoid multiplying map diagnostics by six readers.
    store_rows=[r for r in all_rows if r['reader_role']=='exact_owner'];store_stats=defaultdict(lambda:[0,0])
    for r in store_rows:
        k=(r['condition'],r['checkpoint']);store_stats[k][0]+=r['whole_map_correct']=='True';store_stats[k][1]+=1
    maprows=[{'condition':k[0],'checkpoint':k[1],'whole_map_correct':v[0],'unique_store_queries':v[1],'whole_map_accuracy':v[0]/v[1]} for k,v in sorted(store_stats.items())]
    csvout(out/'WHOLE_MAP_DIAGNOSTICS.csv',maprows)
    # Publish every wrong answer, not just accepted gates or a selected seed.
    bad=[r for r in all_rows if r['correct']=='False'];csvout(out/'ALL_NEGATIVE_QUERY_RESULTS.csv',bad)
    prior=read(ROOT/'provenance/prior_reported_results/results/qualification/QUALIFICATION.json')
    old={r['seed']:r['sha256'] for r in prior['input_scores']}
    historic=[{'seed':r['seed'],'fresh_sha256':r['scores_sha256'],'historical_reported_sha256':old[r['seed']],'exact_score_file_match':r['scores_sha256']==old[r['seed']]} for r in inputs]
    write(out/'HISTORICAL_SCORE_COMPARISON.json',{'scope':'Comparison against retained historical digests only. Not a comparison to absent historical raw captures or an acceptance target.','rows':historic})
    result={'status':'COMPLETE_INFERENCE_EVALUATION_RECOVERY_WITH_DECLARED_HISTORICAL_GAPS','original_training_protocol_fully_requalified':False,'original_protocol_sha256':sha(ROOT/'protocol/ORIGINAL_FROZEN_PROTOCOL.json'),'criteria_sha256':sha(ROOT/'protocol/RECOVERED_CRITERIA.json'),'main_seeds':seeds,'conditions_per_seed':64,'condition_seed_pairs':320,'reader_condition_seed_cells':1920,'frames':645,'query_chains':len(all_rows),'logical_stage_audits':stages,'coverage_class_checks':coverage_checks,'checkpoint_class_checks':checkpoint_checks,'nonzero_metric_rows':len(metric_rows),'frozen_gate_checks':len(gate_rows),'new_optimizer_updates':0,'candidates':candidates,'all_negative_queries_retained':len(bad),'input_scores':inputs,'replay_arrays_exact':sum(read(ROOT/f'results/main/seed{s}/EXACT_REPLAY.json')['arrays_exact'] for s in seeds),'replay_elements_exact':sum(read(ROOT/f'results/main/seed{s}/EXACT_REPLAY.json')['elements_exact'] for s in seeds),'full_optimizer_rng_checkpoints_available':0,'raw_main_training_numeric_traces_available':0,'partial_rng_metadata_retained':True,'fresh_training_reproduction_performed':False,'historical_score_digests_all_match':all(r['exact_score_file_match'] for r in historic),'underflow_original_contract_passed_unchanged':False,'underflow_amendment_implementation':'v2 reconstructed from retained rationale; separately pinned before all-case verification','limits':['New v1.4 reconstruction, not the lost original Qualification010 study.','Exact local CPU replay; no Windows/GPU/third-party replication.','Raw original underflow row and original v2 implementation unavailable; fresh same-regime reproduction retained.','Three archived verifier errors preserved, not converted to passes.','No integrated NSS, online learning, language competence or low-bit claims.'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if len(all_rows)!=449640 or stages!=3045480:raise ValueError('whole study workload mismatch')
    write(out/'STUDY_RESULT.json',result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
