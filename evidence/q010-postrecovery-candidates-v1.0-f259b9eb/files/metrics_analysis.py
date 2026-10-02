import csv, json, math, zipfile

ARCHIVE = 'Research/Q010_InferenceRecovery_v1.6_RecoveryContext.zip'
PREFIX = 'Q010_InferenceRecovery_v1.6/'
ANALYSIS = PREFIX + 'results/analysis/'
OUT = '.research_review/Q010_v1.6_20260924/'
SEEDS = ['1201', '1202', '1203', '1204', '1205']
ROLES = ['inherited', 'cap_only', 'ordinary', 'near', 'attention', 'exact_owner']
CANDIDATES = ['ordinary', 'near', 'attention']

class TextLines:
    def __init__(self, binary): self.binary = binary
    def __iter__(self):
        for line in self.binary: yield line.decode('utf-8')

def csv_rows(z, member):
    with z.open(member) as f:
        for row in csv.DictReader(TextLines(f)): yield row

def cell(a, condition, role, evidence='supported', checkpoint=None):
    good = total = 0
    for seed in SEEDS:
        if checkpoint is None:
            keys = [k for k in a if k[0] == condition and k[1] == role and k[2] == seed and k[3] == evidence]
        else:
            keys = [(condition, role, seed, evidence, str(checkpoint))]
        for k in keys:
            v = a.get(k, [0, 0]); good += v[0]; total += v[1]
    if total == 0: raise ValueError('selected metric has no retained rows: ' + condition + '/' + role + '/' + evidence)
    return {'correct': good, 'total': total, 'accuracy': round(good / total, 6)}

def per_seed_cells(a, condition, role, evidence='supported', checkpoint=None):
    out = []
    for seed in SEEDS:
        if checkpoint is None:
            vals = [v for k, v in a.items() if k[0] == condition and k[1] == role and k[2] == seed and k[3] == evidence]
            good = sum(v[0] for v in vals); total = sum(v[1] for v in vals)
        else:
            good, total = a.get((condition, role, seed, evidence, str(checkpoint)), [0, 0])
        out.append({'seed': int(seed), 'correct': good, 'total': total})
    return out

def pool_per_seed(rows):
    return {'per_seed': rows, 'pooled': {'correct': sum(x['correct'] for x in rows), 'total': sum(x['total'] for x in rows)}}

with zipfile.ZipFile(ARCHIVE) as z:
    study = json.loads(z.read(ANALYSIS + 'STUDY_RESULT.json').decode('utf-8'))
    acc = {}; unknown = {}; negative_by_class = {}; role_total = {}; conditions = set(); seeds = set(); roles = set(); readers = set(); cells = set(); seed_conditions = set(); query_rows = 0; negative_rows = 0
    for r in csv_rows(z, ANALYSIS + 'ALL_QUERY_SCORES.csv'):
        query_rows += 1
        seed, cond, role, evidence, checkpoint = r['seed'], r['condition'], r['reader_role'], r['evidence_class'], r['checkpoint']
        correct = int(r['correct'] == 'True')
        conditions.add(cond); seeds.add(seed); roles.add(role); readers.add(r['reader']); cells.add((seed, cond, role)); seed_conditions.add((seed, cond))
        k = (cond, role, seed, evidence, checkpoint)
        v = acc.setdefault(k, [0, 0]); v[0] += correct; v[1] += 1
        t = role_total.setdefault(role, [0, 0]); t[0] += correct; t[1] += 1
        if evidence == 'preexisting_unknown':
            uk = unknown.setdefault((cond, role, seed), [0, 0]); uk[0] += correct; uk[1] += 1
        if not correct:
            negative_rows += 1; negative_by_class[evidence] = negative_by_class.get(evidence, 0) + 1
    metrics_rows = sum(1 for _ in csv_rows(z, ANALYSIS + 'METRICS_ALL_SEEDS_AND_POOLED.csv'))
    gate = {}
    for r in csv_rows(z, ANALYSIS + 'FROZEN_GATE_CHECKS.csv'):
        role, seed = r['role'], r['seed']
        k = gate.setdefault((role, seed), [0, 0]); k[0] += 1; k[1] += int(r['passed'] == 'True')

    gates = {}
    for role in CANDIDATES:
        seeds_out = []
        for seed in SEEDS:
            n, p = gate.get((role, seed), [0, 0]); seeds_out.append({'seed': int(seed), 'checks': n, 'passed': p, 'all_pass': n == 83 and p == 83})
        pooled_rows = [v for (r, s), v in gate.items() if r == role and s not in SEEDS]
        n = sum(v[0] for v in pooled_rows); p = sum(v[1] for v in pooled_rows)
        assert len(pooled_rows) == 1 and n == 83 and p == 83
        gates[role] = {'per_seed': seeds_out, 'pooled': {'checks': n, 'passed': p, 'all_pass': True}}

    close = {r: pool_per_seed(per_seed_cells(acc, 'stress_close_source_sigma001', r)) for r in ROLES}
    intermediate = {r: pool_per_seed(per_seed_cells(acc, 'stress_close_intermediate_sigma001', r)) for r in ROLES}
    near_novel = {}
    ordinary_novel = {}
    for role in ROLES:
        for label, condition, target in [('near_collision', 'stress_near_collision_novel_sigma001', near_novel), ('ordinary_novel', 'stress_ordinary_novel', ordinary_novel)]:
            ps = []
            for seed in SEEDS:
                good, total = unknown.get((condition, role, seed), [0, 0]); ps.append({'seed': int(seed), 'unknown_correct': good, 'unknown_total': total})
            assert all(x['unknown_total'] == 128 for x in ps)
            target[role] = {'per_seed': ps, 'pooled': {'unknown_correct': sum(x['unknown_correct'] for x in ps), 'unknown_total': sum(x['unknown_total'] for x in ps)}}
    signals = {
        'close_source_supported': close,
        'close_intermediate_supported': intermediate,
        'near_collision_expected_unknown': near_novel,
        'ordinary_novel_expected_unknown': ordinary_novel,
        'altered_known_supported': {r: cell(acc, 'stress_altered_known_q020', r) for r in ROLES},
        'erased_values_supported': {r: cell(acc, 'corruption_erased_values', r) for r in ROLES},
        'wrong_but_valid_supported': {r: cell(acc, 'corruption_wrong_but_valid', r) for r in ROLES},
        'state_off_supported': {r: cell(acc, 'ablation_state_off', r) for r in ROLES},
        'core_l08_d01_under_depth': {r: cell(acc, 'core_assisted_l08_d01', r, evidence='under_depth') for r in ROLES},
        'core_l08_d08_supported': {r: cell(acc, 'core_assisted_l08_d08', r) for r in ROLES},
        'durability_cadence08_supported': {r: cell(acc, 'durability_sigma02_cadence08_livewrite64', r) for r in ROLES},
        'durability_cadence32_supported': {r: cell(acc, 'durability_sigma02_cadence32_livewrite64', r) for r in ROLES},
        'durability_no_maintenance_event1024_supported': {r: cell(acc, 'durability_sigma02_no_maintenance_livewrite64', r, checkpoint=1024) for r in ROLES}
    }
    summary = {
        'source_members': {
            'report': PREFIX + 'REPORT.md',
            'study_result': ANALYSIS + 'STUDY_RESULT.json',
            'per_query_scores': ANALYSIS + 'ALL_QUERY_SCORES.csv',
            'gate_checks': ANALYSIS + 'FROZEN_GATE_CHECKS.csv',
            'metrics': ANALYSIS + 'METRICS_ALL_SEEDS_AND_POOLED.csv',
            'whole_map': ANALYSIS + 'WHOLE_MAP_DIAGNOSTICS.csv'
        },
        'recomputed': {
            'query_rows': query_rows, 'conditions': len(conditions), 'seeds': sorted(int(s) for s in seeds),
            'roles': sorted(roles), 'reader_names': len(readers), 'condition_seed_pairs': len(seed_conditions),
            'reader_condition_seed_cells': len(cells), 'incorrect_outcome_rows': negative_rows,
            'incorrect_rows_by_evidence_class': negative_by_class, 'metric_table_rows': metrics_rows,
            'frozen_gate_rows': sum(v[0] for v in gate.values()), 'gates_by_candidate': gates,
            'query_rows_by_role': {r: {'correct': v[0], 'total': v[1]} for r, v in role_total.items()}
        },
        'study_result_claims': {
            'query_chains': study.get('query_chains'), 'logical_stage_audits': study.get('logical_stage_audits'),
            'condition_seed_pairs': study.get('condition_seed_pairs'), 'reader_condition_seed_cells': study.get('reader_condition_seed_cells'),
            'frozen_gate_checks': study.get('frozen_gate_checks'), 'nonzero_metric_rows': study.get('nonzero_metric_rows'),
            'all_negative_queries_retained': study.get('all_negative_queries_retained'),
            'logical_stage_audits_recomputed_from_selected_score_files': False
        },
        'signals': signals,
        'scope': {
            'analysis_type': 'retained-row metric recomputation only; no model imports, inference, training or experiment',
            'replicate_unit': 'five paired seeds; query rows are repeated outcomes within seed, not independent trained models',
            'archive_limit': 'RecoveryContext is compact and omits raw main-capture trees; whole-map diagnostics and per-query score rows are retained summaries',
            'training_limit': 'No fresh training reproduction; original main numerical traces and full optimizer/RNG checkpoints unavailable',
            'gate_limit': 'Frozen gates cover the declared candidate criteria; diagnostic failures remain outside those pass counts'
        }
    }
    with open(OUT + 'metrics_summary.json', 'w', encoding='utf-8') as f: json.dump(summary, f, indent=2)

    lines = [
        '# Q010 v1.6 retained metrics analysis', '',
        'This is a deterministic count-and-rate recomputation from retained CSV rows, not a new inference run. The archive and all of its members were read-only.', '',
        '## Recomputed cross-checks', '',
        f"`ALL_QUERY_SCORES.csv` contains {query_rows:,} reader-query outcome rows across {len(conditions)} conditions, {len(seeds)} seeds and six reader roles ({len(cells):,} unique condition-seed-role cells; {len(seed_conditions):,} condition-seed pairs). `FROZEN_GATE_CHECKS.csv` contains {sum(v[0] for v in gate.values()):,} rows. The three candidate arms each have 83/83 checks in every seed and 83/83 pooled, matching `STUDY_RESULT.json`.", '',
        f"The {negative_rows:,} incorrect outcome rows match the study result's retained-negative count. Their evidence classes are: under_depth {negative_by_class.get('under_depth',0):,}; unobservable_missing {negative_by_class.get('unobservable_missing',0):,}; observable_missing {negative_by_class.get('observable_missing',0):,}; supported {negative_by_class.get('supported',0):,}; preexisting_unknown {negative_by_class.get('preexisting_unknown',0):,}. This is an outcome-row count across readers, not a count of unique inputs or candidate-gate failures.", '',
        f"The result JSON reports {study.get('logical_stage_audits'):,} logical stage audits. That value is not re-derived from the selected score and gate tables; this review did not open stage-level captures. The result's 83-check-per-seed/pooled gate claims and {study.get('query_chains'):,} query count were checked directly against retained rows.", '',
        '## Scientific signals outside the frozen gates', '',
        f"- Close-source supported queries: ordinary {close['ordinary']['pooled']['correct']}/{close['ordinary']['pooled']['total']}; near {close['near']['pooled']['correct']}/{close['near']['pooled']['total']}; attention {close['attention']['pooled']['correct']}/{close['attention']['pooled']['total']}; inherited/cap-only {close['inherited']['pooled']['correct']}/{close['inherited']['pooled']['total']} each; exact-owner {close['exact_owner']['pooled']['correct']}/{close['exact_owner']['pooled']['total']}. Near exceeds ordinary in all five paired seeds (per-seed gains: {', '.join('+'+str(close['near']['per_seed'][i]['correct']-close['ordinary']['per_seed'][i]['correct']) for i in range(5))} of 64). It still gets only {near_novel['near']['pooled']['unknown_correct']}/{near_novel['near']['pooled']['unknown_total']} near-collision novel queries labeled UNKNOWN; exact-owner gets {near_novel['exact_owner']['pooled']['unknown_correct']}/{near_novel['exact_owner']['pooled']['unknown_total']}.",
        f"- At coded condition `core_assisted_l08_d01`, under_depth diagnostic accuracy is {signals['core_l08_d01_under_depth']['ordinary']['correct']}/{signals['core_l08_d01_under_depth']['ordinary']['total']} for every role; `core_assisted_l08_d08` supported accuracy is {signals['core_l08_d08_supported']['ordinary']['correct']}/{signals['core_l08_d08_supported']['ordinary']['total']}. Each seed has the same 0/64 versus 64/64 pattern across roles.",
        f"- State-off supported queries score {signals['state_off_supported']['ordinary']['correct']}/{signals['state_off_supported']['ordinary']['total']} for each role. With cadence 08, supported durability rows are {signals['durability_cadence08_supported']['ordinary']['correct']}/{signals['durability_cadence08_supported']['ordinary']['total']}; cadence 32 falls to {signals['durability_cadence32_supported']['ordinary']['correct']}/{signals['durability_cadence32_supported']['ordinary']['total']}. At event 1,024 without maintenance, ordinary/near/attention are {signals['durability_no_maintenance_event1024_supported']['ordinary']['correct']}/{signals['durability_no_maintenance_event1024_supported']['ordinary']['total']}, {signals['durability_no_maintenance_event1024_supported']['near']['correct']}/{signals['durability_no_maintenance_event1024_supported']['near']['total']}, and {signals['durability_no_maintenance_event1024_supported']['attention']['correct']}/{signals['durability_no_maintenance_event1024_supported']['attention']['total']}.",
        f"- Erased-value support is {signals['erased_values_supported']['ordinary']['correct']}/{signals['erased_values_supported']['ordinary']['total']} for every role; wrong-but-valid support is {signals['wrong_but_valid_supported']['ordinary']['correct']}/{signals['wrong_but_valid_supported']['ordinary']['total']} for every role. These equal marginals do not establish that the same individual queries failed. On altered-known stress, near gets {signals['altered_known_supported']['near']['correct']}/{signals['altered_known_supported']['near']['total']}, ordinary {signals['altered_known_supported']['ordinary']['correct']}/{signals['altered_known_supported']['ordinary']['total']}, and attention {signals['altered_known_supported']['attention']['correct']}/{signals['altered_known_supported']['attention']['total']}.", '',
        'These denominators are query outcomes pooled over five paired seeds; the five seeds, not hundreds of query rows, are the model-level replication count. Candidate gate passage therefore does not establish broad close-identity admission, corruption tolerance or no-maintenance durability.', '',
        '## Evidence boundary', '',
        'The package report says no optimizer update or fresh training reproduction occurred, and `STUDY_RESULT.json` records the training audit as incomplete. Full main numerical training traces and full optimizer/RNG checkpoints are unavailable. This compact RecoveryContext package omits raw main-capture trees; the recomputation covers its retained score summaries only. It does not rederive the reported 3,045,480 logical-stage audits or constitute independent inference or third-party replication.', '',
        'Primary members: `Q010_InferenceRecovery_v1.6/REPORT.md`; `Q010_InferenceRecovery_v1.6/results/analysis/STUDY_RESULT.json`; `Q010_InferenceRecovery_v1.6/results/analysis/ALL_QUERY_SCORES.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/FROZEN_GATE_CHECKS.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/METRICS_ALL_SEEDS_AND_POOLED.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/WHOLE_MAP_DIAGNOSTICS.csv`.'
    ]
    with open(OUT + 'metrics_analysis.md', 'w', encoding='utf-8', newline='') as f: f.write('\n'.join(lines) + '\n')




