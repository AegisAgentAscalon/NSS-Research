"""Command-line execution and retained failure evidence for SURFACE01."""
from common import *
import argparse, shutil, subprocess, traceback


def record_failure(code,phase,detail,context=None, disposition='STOP', cause='CAUSE_UNRESOLVED'):
    item={'time_utc':utc(),'code':code,'phase':phase,'context':context or {},'detail':detail,
          'cause_status':cause,'disposition':disposition,'source_hashes':{p.name:sha_file(p) for p in (ROOT/'source').glob('*.py')}}
    append_json(ROOT/'failures'/'ledger.jsonl',item)
    return item


def probe_resume(checkpoint,data_path,kind,output):
    m,p=load_checkpoint(checkpoint); opt=opt_for(m,frozen=kind=='F'); opt.load_state_dict(p['optimizer'])
    torch.set_rng_state(p['torch_rng']); data=np.load(data_path)
    records=[]
    for i in range(8,12):
        kwargs={'tokens':data['tokens'][i],'labels':data['labels'][i]} if kind=='parent' else {'correction':3}
        records.append(update(m,opt,**kwargs))
    save_checkpoint(output,m,opt,12,{'probe':kind,'resume':True})
    write_json(str(output)+'.json',{'records':records,'counters':COUNTERS,'peak_rss':rss()})


def tree_equal(a,b):
    if isinstance(a,torch.Tensor): return isinstance(b,torch.Tensor) and torch.equal(a,b)
    if isinstance(a,dict): return a.keys()==b.keys() and all(tree_equal(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)): return type(a)==type(b) and len(a)==len(b) and all(tree_equal(x,y) for x,y in zip(a,b))
    return a==b


def preflight():
    started=time.perf_counter()
    env={'time_utc':utc(),'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'numpy':np.__version__,
         'device':'cpu','dtype':'float32','threads':torch.get_num_threads(),'interop_threads':torch.get_num_interop_threads(),
         'deterministic_algorithms':torch.are_deterministic_algorithms_enabled(),'mkldnn':torch.backends.mkldnn.enabled,
         'torch_config':torch.__config__.show(),'thread_environment':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS')},
         'cpu':open('/proc/cpuinfo').read().split('model name')[1].split('\n')[0] if Path('/proc/cpuinfo').exists() else platform.processor()}
    write_json(ROOT/'protocol'/'environment.json',env)
    # All 256 masks x 18 possible event commands, independently labelled.
    rows=[]
    for mask in range(256):
        prefix=[i for i in range(8) if mask & (1<<i)]
        for event in range(18): rows.append(prefix+[17]*(8-len(prefix))+[event])
    rows=np.array(rows,dtype=np.uint8); a,_=oracle(rows); b=independent_oracle(rows)
    assert_ok(np.array_equal(a,b),'ORACLE_DISAGREEMENT')
    np.savez_compressed(ROOT/'fixtures'/'exhaustive_oracle.npz',tokens=rows,targets=a)
    # Task history is necessary even if the final observed event is identical.
    history=np.array([[0,17],[17,17]],dtype=np.uint8)
    yy,_=oracle(history); assert_ok(yy[0,-1]!=yy[1,-1],'STATE_ABLATION_FIXTURE_INVALID')
    np.savez_compressed(ROOT/'fixtures'/'history_necessity.npz',tokens=history,targets=yy)
    gen_start=time.perf_counter(); toks,labels,masks,families,rngrec=training_data(4199,12)
    gen_time=time.perf_counter()-gen_start
    data_path=ROOT/'fixtures'/'probe_training.npz'
    np.savez_compressed(data_path,tokens=toks,labels=labels,masks=masks,families=families)
    write_json(ROOT/'fixtures'/'probe_rng.json',rngrec)
    probes=[]
    for kind in ('parent','F','U'):
        m=Learner(4199); opt=opt_for(m,frozen=kind=='F'); records=[]; original=copy.deepcopy(m.cell.state_dict())
        t0=time.perf_counter()
        for i in range(12):
            kw={'tokens':toks[i],'labels':labels[i]} if kind=='parent' else {'correction':3}
            records.append(update(m,opt,**kw))
            if i==7: save_checkpoint(ROOT/'checkpoints'/f'probe_{kind}_8.pt',m,opt,8)
        elapsed=time.perf_counter()-t0
        final=ROOT/'checkpoints'/f'probe_{kind}_12.pt'; save_checkpoint(final,m,opt,12)
        resumed=ROOT/'checkpoints'/f'probe_{kind}_resumed_12.pt'
        cmd=[sys.executable,str(Path(__file__).resolve()),'probe_resume','--checkpoint',str(ROOT/'checkpoints'/f'probe_{kind}_8.pt'),
             '--data',str(data_path),'--kind',kind,'--output',str(resumed)]
        sub=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        (ROOT/'logs'/f'probe_{kind}_resume.txt').write_text(sub.stdout+sub.stderr)
        assert_ok(sub.returncode==0,'RESUME_PROCESS_FAILED',sub.stderr)
        rm,rp=load_checkpoint(resumed); _,fp=load_checkpoint(final)
        exact=tree_equal(fp['model'],rp['model']) and tree_equal(fp['optimizer'],rp['optimizer']) and torch.equal(fp['torch_rng'],rp['torch_rng'])
        assert_ok(exact,'RESUME_NOT_EXACT',kind)
        if kind=='F': assert_ok(tree_equal(original,m.cell.state_dict()),'FROZEN_TRANSITION_CHANGED')
        # Full 152-event independent-equation check, not just a first-state check.
        rng=np.random.default_rng(904199); q=np.stack([stream(rng,152,f) for f in range(4)])
        with torch.no_grad(): hh,ll=m.rollout(q)
        ck=check_trajectory(m,q,hh.numpy(),ll.numpy(),tag='preflight_'+kind)
        np.savez_compressed(ROOT/'fixtures'/f'probe_{kind}_trajectory.npz',tokens=q,hidden=hh.numpy(),logits=ll.numpy())
        assert_ok(ck['pass'],'NUMERICAL_PREFLIGHT',ck)
        probes.append({'kind':kind,'optimizer_applications':16,'unique_update_depth':12,'fresh_process_replay_applications':4,
                       'uninterrupted_12_seconds':elapsed,'exact_resume':exact,'numerical':ck,'records':records,
                       'child':json.loads(Path(str(resumed)+'.json').read_text()),'final_checkpoint_bytes':final.stat().st_size})
        print('PROBE',kind,'16 total applications, exact resume and numerical checks PASS',flush=True)
    # Shared-versus-copied equivalence: two B graphs at identical weights, no extra optimizer applications.
    m,p=load_checkpoint(ROOT/'checkpoints'/'probe_U_12.pt'); explicit=copy.deepcopy(m); frozen_A_head=copy.deepcopy(m.head)
    for p in frozen_A_head.parameters(): p.requires_grad_(False)
    m.zero_grad(); explicit.zero_grad(); target=torch.arange(8)%2; target[3]=1-target[3]
    loss1=TF.cross_entropy(m.b_logits(),target); loss2=TF.cross_entropy(explicit.b_logits(),target)
    loss1.backward(); loss2.backward(); COUNTERS['backward_calls']+=2
    equivalent=all(torch.equal(x.grad,y.grad) for x,y in zip(m.parameters(),explicit.parameters()))
    assert_ok(equivalent,'SHARED_COPY_B_GRAPH_MISMATCH')
    faults=[]
    def exercise(name,clean,bad,evidence):
        clean_pass=False; caught=False
        try: clean(); clean_pass=True
        except Exception as exc: raise RuntimeError('CLEAN_CONTROL_FAILED '+name) from exc
        try: bad()
        except RuntimeError as exc: caught=True; detail=str(exc)
        else: detail='NOT_DETECTED'
        entry={'name':name,'clean_pass':clean_pass,'injected_detected':caught,'detector_message':detail,'evidence':evidence}
        faults.append(entry); assert_ok(caught,'FAULT_NOT_DETECTED',name)
    original_hash=hash_sd(m.cell.state_dict()); corrupt=copy.deepcopy(m)
    with torch.no_grad(): corrupt.cell.weight_hh[0,0]+=0.01
    exercise('frozen_parameter_mutation',lambda:assert_ok(hash_sd(m.cell.state_dict())==original_hash,'FROZEN_HASH'),
             lambda:assert_ok(hash_sd(corrupt.cell.state_dict())==original_hash,'FROZEN_HASH'),{'expected':original_hash,'mutated':hash_sd(corrupt.cell.state_dict()),'tensor':'weight_hh','index':[0,0],'delta':.01})
    exercise('copied_readout_alias',lambda:assert_ok(m.head.weight.data_ptr()!=frozen_A_head.weight.data_ptr(),'READOUT_ALIAS'),
             lambda:assert_ok(m.head.weight.data_ptr()!=m.head.weight.data_ptr(),'READOUT_ALIAS'),{'clean':'deepcopy','injected':'same module reference'})
    state=np.zeros((1,64),np.float32); receipt={'task':'A','state_hash':sha_arr(state),'prefix_hash':sha_arr(history[0]),'model_hash':hash_sd(m.state_dict())}
    def check_receipt(r): assert_ok(r==receipt,'STATE_BINDING')
    exercise('wrong_task_state',lambda:check_receipt(receipt.copy()),lambda:check_receipt(dict(receipt,task='B')),receipt)
    exercise('truncated_history',lambda:assert_ok(sha_arr(history[0])==receipt['prefix_hash'],'HISTORY_HASH'),
             lambda:assert_ok(sha_arr(history[0,:1])==receipt['prefix_hash'],'HISTORY_HASH'),{'full':history[0].tolist(),'truncated':history[0,:1].tolist()})
    desired=np.arange(8)%2; desired[3]=1-desired[3]; stale=np.arange(8)%2
    exercise('stale_B_target',lambda:assert_ok(np.array_equal(desired,desired.copy()),'B_REVISION'),
             lambda:assert_ok(np.array_equal(desired,stale),'B_REVISION'),{'current':desired.tolist(),'stale':stale.tolist()})
    ckpt=ROOT/'checkpoints'/'probe_U_12.pt'; digest=sha_file(ckpt); damaged=ROOT/'fixtures'/'deliberately_corrupted_checkpoint.bin'
    content=bytearray(ckpt.read_bytes()); content[len(content)//2]^=1; damaged.write_bytes(content)
    exercise('corrupt_checkpoint',lambda:assert_ok(sha_file(ckpt)==digest,'CHECKPOINT_BYTES'),lambda:assert_ok(sha_file(damaged)==digest,'CHECKPOINT_BYTES'),{'original_sha256':digest,'bad_sha256':sha_file(damaged),'flipped_byte':len(content)//2})
    exercise('nonfinite_tensor',lambda:assert_ok(np.isfinite(state).all(),'NONFINITE'),
             lambda:assert_ok(np.isfinite(np.array([np.nan])).all(),'NONFINITE'),{'injected':'NaN'})
    wrong=a.copy(); wrong[0,-1]=(wrong[0,-1]+1)%9
    exercise('wrong_scorer_target',lambda:assert_ok(np.array_equal(a,b),'SCORER_TARGET'),
             lambda:assert_ok(np.array_equal(wrong,b),'SCORER_TARGET'),{'index':[0,8],'correct':int(b[0,-1]),'wrong':int(wrong[0,-1])})
    write_json(ROOT/'evidence'/'fault_injection_receipts.json',faults)
    # An intentionally explicit, uncompressed forecast; never count fake duplicated arrays as evidence.
    layout={'training_tokens_labels_masks_and_families':4*(2000*32*32*3+2000*32),
            'parent_checkpoints':4*6*max(p['final_checkpoint_bytes'] for p in probes),
            'adaptation_checkpoints':16*8*(probes[1]['final_checkpoint_bytes']+probes[2]['final_checkpoint_bytes']),
            'A_main_logits':16*2*8*2*2*32*129*9*4,
            'parent_admission_and_failure_diagnostics':48*1024**2,
            'logs_and_protocol_and_B':16*1024**2,
            'failure_reserve':32*1024**2}
    forecast=sum(layout.values())
    parent_rate=probes[0]['uninterrupted_12_seconds']/12
    adapt_rate=max(p['uninterrupted_12_seconds']/12 for p in probes[1:])
    estimate_fit=8000*parent_rate+2048*adapt_rate+gen_time*(8000/12)
    # Full A evaluation and NumPy checker allowance from 152-step probes.
    model,_=load_checkpoint(ROOT/'checkpoints'/'probe_U_12.pt'); q=np.stack([stream(np.random.default_rng(998+i),152,i%4) for i in range(16)])
    t=time.perf_counter()
    with torch.no_grad(): hs,ll=model.rollout(q)
    ck=check_trajectory(model,q,hs.numpy(),ll.numpy(),tag='cost_check')
    inference_seconds=time.perf_counter()-t
    inference_forecast=inference_seconds*16*2*8*2*2*2
    forecast_wall=estimate_fit+inference_forecast+120
    assert_ok(forecast<CAP_BYTES,'EVIDENCE_FORECAST_CAP',forecast)
    assert_ok(forecast_wall<1800,'RUNTIME_FORECAST_CAP',forecast_wall)
    receipt={'status':'PASS','time_utc':utc(),'probes':probes,'optimizer_applications_total':48,'additional_graph_equivalence_backward_calls':2,
             'shared_copy_graph_equivalence':equivalent,'oracle_cases':256*18,'oracle_scored_events':int(a.size),
             'history_necessity':True,'cost_probe_numerical':ck,'fault_controls':faults,'uncompressed_forecast_by_component':layout,
             'uncompressed_forecast_bytes':forecast,'parent_update_seconds_estimate':parent_rate,'adaptation_update_seconds_estimate':adapt_rate,
             'generation_probe_seconds':gen_time,'main_workload_forecast_seconds':forecast_wall,'runtime_cap_seconds':1800,
             'runtime_stop_reserve_seconds':120,'peak_process_rss_bytes':rss(),'preflight_elapsed_seconds':time.perf_counter()-started,'counters_parent_process':COUNTERS}
    write_json(ROOT/'evidence'/'preflight.json',receipt)
    print('PREFLIGHT PASS',forecast,'forecast bytes;',forecast_wall,'internal budget estimate seconds',flush=True)


def freeze():
    pre=json.loads((ROOT/'evidence'/'preflight.json').read_text()); assert_ok(pre['status']=='PASS','PREFLIGHT_NOT_ADMITTED')
    assert_ok(not (ROOT/'protocol'/'EXECUTION_LOCK.json').exists(),'LOCK_ALREADY_EXISTS')
    lock={'study':'NSS NBR02 SURFACE01','version':'Execution v0.1','dispatch':'User: Oh yeah, always try to make it so the failures are as informative as possible. Run it.',
          'frozen_at_utc':utc(),'prior_optimizer_applications':48,'main_optimizer_applications_at_freeze':0,
          'sources':{p.name:sha_file(p) for p in (ROOT/'source').glob('*.py')},
          'proposal_sha256':sha_file(ROOT/'protocol'/'NSS_NBR02_SURFACE01_Proposal_v0.1.md'),
          'implementation_protocol_sha256':sha_file(ROOT/'protocol'/'EXECUTION_PROTOCOL.md'),
          'preflight_sha256':sha_file(ROOT/'evidence'/'preflight.json'),'environment_sha256':sha_file(ROOT/'protocol'/'environment.json')}
    write_json(ROOT/'protocol'/'EXECUTION_LOCK.json',lock); print('EXECUTION FROZEN',lock['frozen_at_utc'],flush=True)


def check_lock():
    lock=json.loads((ROOT/'protocol'/'EXECUTION_LOCK.json').read_text())
    for name,digest in lock['sources'].items(): assert_ok(sha_file(ROOT/'source'/name)==digest,'SOURCE_LOCK_MISMATCH',name)
    assert_ok(sha_file(ROOT/'protocol'/'EXECUTION_PROTOCOL.md')==lock['implementation_protocol_sha256'],'PROTOCOL_LOCK_MISMATCH')
    return lock


def train():
    check_lock(); started=time.perf_counter(); cohorts=[]
    assert_ok(not (ROOT/'evidence'/'main_started.json').exists(),'MAIN_ALREADY_STARTED')
    write_json(ROOT/'evidence'/'main_started.json',{'time_utc':utc(),'monotonic':started})
    for seed in SEEDS:
        print('PARENT',seed,'generating fixed training corpus',flush=True); genstart=time.perf_counter()
        tokens,labels,masks,families,rngrec=training_data(seed)
        np.savez_compressed(ROOT/'fixtures'/f'training_{seed}.npz',tokens=tokens,labels=labels,masks=masks,families=families)
        write_json(ROOT/'fixtures'/f'training_{seed}_rng.json',rngrec)
        classcounts=np.bincount(labels.ravel(),minlength=9)
        write_json(ROOT/'fixtures'/f'training_{seed}_coverage.json',{'classes':classcounts,'tokens':np.bincount(tokens.ravel(),minlength=26),
                   'distinct_masks':len(np.unique(masks)),'generation_seconds':time.perf_counter()-genstart})
        m=Learner(seed); opt=opt_for(m)
        save_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_0000.pt',m,opt,0,{'training_seed':100000+seed})
        log=ROOT/'logs'/f'parent_{seed}_updates.jsonl'; fitstart=time.perf_counter()
        for i in range(2000):
            rec=update(m,opt,tokens=tokens[i],labels=labels[i]); rec.update(seed=seed,step=i+1,elapsed_seconds=time.perf_counter()-fitstart)
            append_json(log,rec)
            if (i+1) in PARENT_STAGES:
                save_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_{i+1:04d}.pt',m,opt,i+1,{'training_seed':100000+seed,'next_batch':i+1})
                print('PARENT',seed,'update',i+1,'loss',round(rec['loss'],6),flush=True)
            if time.perf_counter()-started>1680:
                record_failure('STOP_RUNTIME','parent_fit',{'elapsed_seconds':time.perf_counter()-started}, {'seed':seed,'step':i+1})
                write_json(ROOT/'evidence'/'outcome.json',{'status':'STOP_RUNTIME','counters':COUNTERS,'peak_rss':rss()}); return
        cohorts.append({'seed':seed,'fit_seconds':time.perf_counter()-fitstart})
        del tokens,labels,masks,families,opt,m
    # All four final parents are retained and then screened; no seed is dropped or replaced.
    admissions=[]; numerical_pass=True
    for seed in SEEDS:
        print('ADMISSION',seed,flush=True)
        data=np.load(ROOT/'fixtures'/f'training_{seed}.npz'); tokens=data['tokens']
        panel=make_panel(seed,'admission',tokens); np.savez_compressed(ROOT/'fixtures'/f'admission_{seed}.npz',**panel)
        m,_=load_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_2000.pt')
        scored=score_panel(m,panel,f'admission_{seed}'); b=b_score(m)
        num=all(c['pass'] for c in scored['checks']) and b['numerical']['pass']; numerical_pass &= num
        passed=competence(scored['metrics'],b)
        item={'seed':seed,'competence_pass':passed,'numerical_pass':num,'metrics':scored['metrics'],'B':b}
        admissions.append(item); write_json(ROOT/'evidence'/f'admission_{seed}_summary.json',item)
        if not passed:
            record_failure('PARENT_COMPETENCE_FAIL','admission',item,{'seed':seed},'RETAIN_FIXED_COHORT_NO_ADAPTATION','OBSERVED_BASELINE_ERROR_CAUSE_UNRESOLVED')
        if not num:
            record_failure('NUMERICAL_GATE_FAIL','admission',{'checks':scored['checks'],'B':b['numerical']},{'seed':seed},'NO_QUALIFICATION')
        print('ADMISSION',seed,'competence',passed,'numerical',num,'family whole',[(k,v['whole_correct'],v['histories']) for k,v in scored['metrics']['32'].items()],flush=True)
        # Predeclared failure diagnosis: final model on five existing training batches, no new fit/data.
        if not passed or not num:
            sample=tokens[[0,499,999,1499,1999]].reshape(160,32)
            yy,mm=oracle(sample)
            with torch.no_grad(): hs,ll=m.rollout(sample)
            logits=ll.numpy(); pred=logits.argmax(-1); ck=check_trajectory(m,sample,hs.numpy(),logits,tag=f'training_diagnosis_{seed}')
            np.savez_compressed(ROOT/'evidence'/f'training_diagnosis_{seed}.npz',tokens=sample,targets=yy,hidden=hs.numpy(),logits=logits)
            write_json(ROOT/'evidence'/f'training_diagnosis_{seed}.json',{'seed':seed,'source_updates':[1,500,1000,1500,2000],
                       'event_correct':int((pred==yy).sum()),'events':int(yy.size),'whole_correct':int((pred==yy).all(1).sum()),'histories':160,
                       'false_done':int(((pred==8)&(yy!=8)).sum()),'numerical':ck,'no_training_updates':True})
            # Non-isolated prefixes: keep the first failing original full history per family, not a changed reproducer.
            for f in range(4):
                candidates=np.where(panel['families']==f)[0]
                for row in candidates:
                    pp=scored['logits'][row,1:33].argmax(-1); y=scored['targets'][row,1:33]
                    if (pp!=y).any():
                        p=int(panel['prefixes'][row]); first=int(np.flatnonzero(pp!=y)[0])+1
                        np.savez_compressed(ROOT/'failures'/f'parent_{seed}_{FAMILIES[f]}_first.npz',
                            tokens=panel['tokens'][row,:p+32],targets=panel['labels'][row,:p+32],
                            hidden=scored['full_hidden'][row,:p+32],logits=scored['full_logits'][row,:p+32])
                        write_json(ROOT/'failures'/f'parent_{seed}_{FAMILIES[f]}_first.json',{'seed':seed,'family':FAMILIES[f],'row':int(row),
                            'prefix_length':p,'first_error_suffix_position':first,'checkpoint':f'parent_{seed}_2000.pt',
                            'checkpoint_sha256':sha_file(ROOT/'checkpoints'/f'parent_{seed}_2000.pt'),
                            'fixture_sha256':sha_file(ROOT/'fixtures'/f'admission_{seed}.npz'),
                            'canonical_batch_note':'Original group batch, use source panel and checkpoint for byte-exact replay; single-row replay may differ numerically.'})
                        break
    allpass=all(a['competence_pass'] for a in admissions)
    status='PARENTS_ADMITTED' if allpass and numerical_pass else ('STOP_NUMERICAL' if not numerical_pass else 'STOP_BASELINE_COMPETENCE')
    outcome={'study':'SURFACE01','execution_version':'v0.1','status':status,'parents':admissions,'cohorts':cohorts,
             'optimizer_applications_main':COUNTERS['optimizer_applications'],'optimizer_applications_preflight':48,
             'optimizer_applications_total':COUNTERS['optimizer_applications']+48,'B_main_adaptation_updates':0,
             'confirmation_generated':False,'counters':COUNTERS,'elapsed_main_seconds':time.perf_counter()-started,'peak_process_rss_bytes':rss(),
             'numerical_admission_all':numerical_pass,'baseline_admission_all':allpass}
    write_json(ROOT/'evidence'/'outcome.json',outcome)
    print('OUTCOME',status,'applications',outcome['optimizer_applications_total'],flush=True)


def verify():
    check_lock(); t=time.perf_counter(); results=[]
    outcome=json.loads((ROOT/'evidence'/'outcome.json').read_text())
    for seed in SEEDS:
        panel=dict(np.load(ROOT/'fixtures'/f'admission_{seed}.npz'))
        expected=np.load(ROOT/'evidence'/f'admission_{seed}.npz')
        m,_=load_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_2000.pt')
        scored=score_panel(m,panel,'fresh_process_'+str(seed),save=False)
        logits_exact=np.array_equal(scored['logits'],expected['logits'])
        hidden_exact=np.array_equal(scored['full_hidden'],expected['full_hidden'])
        target_exact=np.array_equal(scored['targets'],expected['targets'])
        oracle_exact=True
        for p in (8,24):
            rows=np.where(panel['prefixes']==p)[0]; toks=panel['tokens'][rows,:p+32]
            oracle_exact &= np.array_equal(independent_oracle(toks),panel['labels'][rows,:p+32])
        entry={'seed':seed,'logits_bit_exact':logits_exact,'hidden_bit_exact':hidden_exact,'targets_bit_exact':target_exact,'independent_oracle_exact':bool(oracle_exact)}
        results.append(entry)
        assert_ok(all(entry[k] for k in entry if k!='seed'),'FRESH_PROCESS_REPLAY_FAILED',entry)
        print('FRESH REPLAY',seed,'PASS',flush=True)
    write_json(ROOT/'evidence'/'fresh_process_replay.json',{'status':'PASS','parents':results,'new_optimizer_applications':0,
               'elapsed_seconds':time.perf_counter()-t,'peak_process_rss_bytes':rss(),'counters':COUNTERS,
               'scope':'Same implementation, fresh process, retained final-parent admission trajectories. Internal reproducibility, not third-party replication.'})


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command'); parser.add_argument('--checkpoint'); parser.add_argument('--data'); parser.add_argument('--kind'); parser.add_argument('--output'); args=parser.parse_args()
    try:
        if args.command=='probe_resume': probe_resume(args.checkpoint,args.data,args.kind,Path(args.output))
        elif args.command=='preflight': preflight()
        elif args.command=='freeze': freeze()
        elif args.command=='train': train()
        elif args.command=='verify': verify()
        else: raise ValueError(args.command)
    except Exception as exc:
        trace=traceback.format_exc(); print(trace,flush=True)
        record_failure('EXECUTION_EXCEPTION',args.command,{'error':str(exc),'traceback':trace,'counters':COUNTERS},disposition='STOP_NO_RETRY')
        raise
