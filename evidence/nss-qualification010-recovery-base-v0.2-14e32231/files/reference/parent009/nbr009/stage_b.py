"""Registered history versus external admission: isolated recovery, then depth.

Exact ownership is the intelligible Stage A store control. Protected source
owners rehydrate KEYS only. Values have no saved destination ID or shadow copy.
"""
from .common import *
from .state import OwnedState,N
from .readout import neural_read,exact_owner_read
from nbr008.pipeline import make_problem


def install(p,binder):
    b=len(p['q']);active=torch.from_numpy(p['codes'][:,:N].square().sum(-1)>.5) if isinstance(p['codes'],torch.Tensor) else torch.from_numpy((p['codes'][:,:N]**2).sum(-1)>.5)
    # Canonical owner attached by the permitted source event, no destination ID kept.
    rng=np.random.default_rng(993);allocation=torch.from_numpy(np.argsort(rng.random((b,N)),axis=-1).astype(np.int64))
    s=OwnedState(torch.from_numpy(p['codes'][:,:N]),active,binder,allocation=allocation,mode='identity');r=np.arange(b)
    for j in range(N):
        src=p['slot_ids'][:,j];dst=p['parent'][r,src]
        s.event(src,torch.from_numpy(p['codes'][r,dst]),1,dst!=N)
    return s


def scenarios():
    out=[]
    def add(label,policy,horizon,fields='both',cadence=8,hops=8,fault='',sigma=.02,query_noise=0,state_on=True):
        out.append(dict(label=label,policy=policy,horizon=horizon,fields=fields,cadence=cadence,hops=hops,fault=fault,sigma=sigma,query_noise=query_noise,state_on=state_on))
    for pol in ('shared_A','internal_A','nearest','none'):
        add(f'clean_{pol}',pol,0)
        for cad in (1,8,32,1024):add(f'long_{pol}_c{cad}',pol,1024,cadence=cad)
    for pol in ('shared_A','internal_A','owner_keys','recover_values'):
        for field in ('keys','values','both'):add(f'isolate_{pol}_{field}',pol,64,field,cadence=32,hops=4)
    for pol in ('shared_B','internal_B','owner_keys','recover_values'):add(f'long_{pol}_c32',pol,1024,cadence=32)
    for pol in ('shared_A','internal_A','nearest'):
        for fault in ('erased_value','wrong_valid_value','stale_owner','wrong_scope','valid_wrong_owner'):
            add(f'fault_{pol}_{fault}',pol,0,fault=fault)
        add(f'common_{pol}',pol,1024,cadence=32,fault='common_noise')
        add(f'query20_{pol}',pol,0,query_noise=.20)
    for h in (4,8):
        for retained in (False,True):add(f'factorial_h{h}_state{int(retained)}','internal_A',1024,cadence=8,hops=h,state_on=retained)
    return out

@torch.no_grad()
def maintain(s,policy,rs):
    if policy=='none':return
    if policy=='nearest':s.maintain(rs['nearest'],'shared');return
    if policy.startswith('shared'):s.maintain(rs['A_nearest' if policy.endswith('A') else 'B_nearest'],'shared');return
    if policy.startswith('internal'):
        s.maintain(rs['A_nearest' if policy.endswith('A') else 'B_nearest'],'internal',value_restorer=rs['nearest']);return
    if policy=='owner_keys':
        s.maintain(rs['A_nearest'],'internal','keys');s.maintain(rs['A_nearest'],'shared','values');return
    if policy=='recover_values':
        s.maintain(rs['A_nearest'],'shared','keys');s.maintain(rs['A_nearest'],'internal','values',rs['nearest']);return
    raise ValueError(policy)

def query_resolver(policy,rs):
    if policy.endswith('B'):return rs['B_nearest']
    if policy in ('nearest','none'):return rs['nearest']
    return rs['A_nearest']

@torch.no_grad()
def run(pair,path,b=64,development=False,configs=None):
    setup();ms,head,cfg=load_pair(pair);before=model_hashes(ms);arrays={};records=[];times=[]
    rs={k:make_resolver(k,ms,head,cfg) for k in ('A_nearest','B_nearest','nearest')}
    for c in (configs or scenarios()):
        h=c['hops'];seed=(71920000 if development else 72920000)+pair*1000+h
        p=make_problem(seed,h,b);s=install(p,ms['binder']);initial=s.arrays()
        noise_seed=seed+2000000;rng=np.random.default_rng(noise_seed);t=time.perf_counter();sweeps=0
        for _ in range(c['horizon']):
            s.add_noise(rng,c['sigma'],c['fields'],c['fault']=='common_noise')
            if s.tick%c['cadence']==0:
                maintain(s,c['policy'],rs);sweeps+=int(c['policy']!='none')
        if c['horizon'] and s.tick%c['cadence']:
            maintain(s,c['policy'],rs);sweeps+=int(c['policy']!='none')
        maintenance_seconds=time.perf_counter()-t
        # Faults affect only the candidate arrays after a real source write.
        if c['fault']=='erased_value':s.vals.zero_();maintain(s,c['policy'],rs)
        if c['fault'] in ('wrong_valid_value','stale_owner','valid_wrong_owner'):
            for i in range(b):
                slots=torch.where((s.owner[i]==int(p['query'][i]))&s.present[i])[0]
                if len(slots):
                    j=int(slots[0])
                    if c['fault']=='wrong_valid_value':
                        # Known wrong room as perturbation, not a legitimate correction.
                        wrong=int(p['rooms'][i,1]);s.vals[i,j]=s.book[i,wrong]
                    elif c['fault']=='stale_owner':s.owner_epoch[i,j]+=1
                    else:
                        used=set(s.owner[i,s.present[i]].tolist());unused=[z for z in range(N) if z not in used]
                        if unused:s.owner[i,j]=unused[0]
        if not c['state_on']:
            s.present.zero_();s.kr.zero_();s.vr.zero_();s.owner.fill_(-1);s.keys.zero_();s.vals.zero_();s.owner_epoch.zero_()
        invalid=False
        try:
            if c['fault'] in ('wrong_valid_value','stale_owner','valid_wrong_owner'):maintain(s,c['policy'],rs)
            s.validate(scope='other' if c['fault']=='wrong_scope' else 'study')
        except ValueError:invalid=True
        q=p['q'].copy()
        if c['query_noise']:
            qr=np.random.default_rng(seed+3000000);q[:,:16]+=qr.normal(0,c['query_noise'],q[:,:16].shape).astype(np.float32);q=data.normalize(q).astype(np.float32)
        qr=query_resolver(c['policy'],rs);pre=c['label'];q=torch.from_numpy(q);t=time.perf_counter()
        for rd in ('record_hop','gated_hop'):
            if invalid:
                arrays[pre+'__pred_'+rd]=np.full((b,8),N,np.int64);arrays[pre+'__matched_'+rd]=np.full((b,8),-1,np.int64)
            else:
                result=neural_read(s,ms[rd],qr,q,8)
                arrays[pre+'__pred_'+rd]=result['pred'].numpy();arrays[pre+'__matched_'+rd]=result['matched'].numpy()
        arrays[pre+'__pred_exact_owner']=np.full((b,8),N,np.int64) if invalid else exact_owner_read(s,q,qr,8).numpy()
        query_seconds=time.perf_counter()-t
        for k,v in s.arrays().items():arrays[pre+'__state_'+k]=v
        arrays[pre+'__initial_vals']=initial['vals'];arrays[pre+'__parent']=p['parent'];arrays[pre+'__query']=p['query'];arrays[pre+'__rooms']=p['rooms'];arrays[pre+'__q']=q.numpy();arrays[pre+'__absent']=p['absent']
        records.append(c|{'seed':seed,'noise_seed':noise_seed,'batch':b,'invalid_detected':invalid,'raw_state_bytes_per_stream':s.bytes()//b})
        times.append({'label':pre,'maintenance_seconds':maintenance_seconds,'query_seconds_both_readers_and_control':query_seconds,'sweeps':sweeps})
    if before!=model_hashes(ms):raise RuntimeError('Evaluation weights changed')
    save_arrays(path,arrays,{'stage':'B','pair':pair,'development':development,'configs':records,'fixed_weights':before,'timing':times,'timestamp':utc()});return arrays,records
