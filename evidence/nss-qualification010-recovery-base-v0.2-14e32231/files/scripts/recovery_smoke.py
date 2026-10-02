"""New limited inherited-reference smoke check; NOT a Qualification010 replay.

Uses actual 009 checkpoint bytes and source. No optimizer or parameter update.
Cases deliberately use new seeds, 16 streams, 0/64 injected-noise events, no
unrelated live writes. These are NOT the original 010 128-stream main cases.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'reference/parent009'))
import numpy as np
import torch
from nbr009.common import setup, load_pair, make_resolver, model_hashes, weights_hash
from nbr009.stage_b import install, maintain
from nbr009.readout import neural_read, exact_owner_read, logical_graph_arrays
from nbr008.pipeline import make_problem
from recovery.cap_variant import CapOnlyRecordHop

def independently_expected(graph, query, rounds):
    """Scorer-only traversal of source graphs; never passed to numerical readers."""
    rows = []
    unknown = graph.shape[1] - 1
    for i, start in enumerate(query):
        cur, steps = int(start), []
        for _ in range(rounds):
            cur = int(graph[i, cur]) if 0 <= cur <= unknown else unknown
            steps.append(cur)
        rows.append(steps)
    return np.asarray(rows, dtype=np.int64)

@torch.no_grad()
def run(out: Path):
    out = out.resolve()
    forbidden = (ROOT / 'reference').resolve()
    if out == forbidden or forbidden in out.parents:
        raise ValueError('Cannot write results under immutable references')
    out.mkdir(parents=True, exist_ok=False)
    setup()
    arrays, cases, pairs = {}, [], []
    t0 = time.perf_counter()
    for pair in range(1, 6):
        ms, head, cfg = load_pair(pair)
        frozen_before = model_hashes(ms)
        head_before = weights_hash(head)
        cap = CapOnlyRecordHop(ms['record_hop'])
        assert weights_hash(cap) == weights_hash(ms['record_hop'])
        cap_before = weights_hash(cap)
        rs = {name:make_resolver(name, ms, head, cfg) for name in ('A_nearest','B_nearest','nearest')}
        for hops, horizon, state_on in [(4,0,True),(4,64,True),(8,0,True),(8,64,True),(8,64,False)]:
            seed = 93100000 + pair * 1000 + hops
            p = make_problem(seed, hops, 16)
            s = install(p, ms['binder'])
            rng = np.random.default_rng(seed + 2000000)
            for _ in range(horizon):
                s.add_noise(rng, .02, 'both')
                if s.tick % 8 == 0:
                    maintain(s, 'internal_A', rs)
            if not state_on:
                s.present.zero_(); s.kr.zero_(); s.vr.zero_(); s.owner.fill_(-1)
                s.keys.zero_(); s.vals.zero_(); s.owner_epoch.zero_()
            s.validate()
            before = s.signature()
            q = torch.from_numpy(p['q'])
            pred = {
                'inherited':neural_read(s, ms['record_hop'], rs['A_nearest'], q, 8)['pred'].numpy(),
                'cap_only':neural_read(s, cap, rs['A_nearest'], q, 8)['pred'].numpy(),
                'exact':exact_owner_read(s, q, rs['A_nearest'], 8).numpy()
            }
            assert before == s.signature(), 'Reading changed the store'
            expect = independently_expected(p['parent'], p['query'], 8)
            whole, counts = logical_graph_arrays(s.owner.numpy(), s.vals.numpy(), s.present.numpy(),
                s.kr.numpy(), s.vr.numpy(), s.book.numpy(), s.active.numpy(), s.owner_epoch.numpy(), s.epoch.numpy())
            label = f'p{pair}_h{hops}_t{horizon}_state{int(state_on)}'
            for k, a in pred.items(): arrays[label+'__pred_'+k] = a.copy()
            for k in ['parent','query','codes','absent']: arrays[label+'__source_'+k] = p[k].copy()
            arrays[label+'__expected_stages'] = expect
            arrays[label+'__actual_graph'] = whole
            for k,a in s.arrays().items(): arrays[label+'__state_'+k] = a.copy()
            metrics = {}
            for name, pr in pred.items():
                metrics[name] = {}
                for depth in (1,2,4,8):
                    known = ~p['absent']; missing = p['absent']
                    metrics[name][str(depth)] = {
                        'known_correct':int((pr[known,depth-1] == expect[known,-1]).sum()),
                        'known_total':int(known.sum()),
                        'missing_correct':int((pr[missing,depth-1] == 16).sum()),
                        'missing_total':int(missing.sum())
                    }
            cases.append({'label':label,'pair':pair,'seed':seed,'hops':hops,'horizon':horizon,
                'state_on':state_on,'batch':16,'noise_sigma':.02,'cadence':8,'live_unrelated_writes':False,
                'raw_state_bytes_per_stream':s.bytes()//16,
                'whole_maps_matching_source':int((whole == p['parent']).all(-1).sum()),
                'query_read_only':True,'metrics':metrics})
        assert frozen_before == model_hashes(ms), 'Inherited weights changed'
        assert head_before == weights_hash(head), 'Gate weights changed'
        assert cap_before == weights_hash(cap), 'Cap-only weights changed'
        pairs.append({'pair':pair,'inherited_models':frozen_before,'match_head_hash':head_before,
            'cap_only_hash':cap_before,'inherited_reader_hash':weights_hash(ms['record_hop']),
            'parameters':sum(w.numel() for w in ms['record_hop'].parameters()),
            'all_evaluation_weights_unchanged':True})
    np.savez_compressed(out/'SMOKE_ARRAYS.npz', **arrays)
    result={'status':'EXECUTION_AND_INTEGRITY_CHECKS_PASS','scope':'NEW_RECOVERY_SMOKE_NOT_010_QUALIFICATION',
        'qualification010_reconstructed':False,'training_optimizer_steps':0,'new_010_checkpoints':0,
        'profiles_checked':['recovered inherited reader','new report-derived cap-only adapter','recovered exact control'],
        'cases':cases,'pairs':pairs,'array_count':len(arrays),'elapsed_seconds':time.perf_counter()-t0,
        'limitations':['Small new-seed cases, not historical scoring','No live unrelated writes or full lifecycle suite here',
            'No 010 new trained models, main replay, timing qualification, external replication or Windows run']}
    (out/'SMOKE_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status':result['status'],'cases':len(cases),'arrays':len(arrays),
        'training_optimizer_steps':0,'scope':result['scope']},indent=2))
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    try:run(args.out)
    except (ValueError,OSError,RuntimeError,AssertionError) as exc:
        print('Recovery smoke failed: '+str(exc),file=sys.stderr);raise SystemExit(1)
