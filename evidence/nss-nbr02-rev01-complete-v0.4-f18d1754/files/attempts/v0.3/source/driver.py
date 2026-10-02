"""Frozen REV01 scheduling and data generation. Worker sees only current public events."""
import json,sys,os,time,hashlib,subprocess,traceback,math,zlib,struct,lzma
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent;SOURCE=ROOT/'source';PROTOCOL=ROOT/'protocol'
SEEDS={a['label']:a['uint64'] for a in json.loads((PROTOCOL/'SEEDS.json').read_text())['allocations']}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def scope(c):return 0 if c in (0,1,2,3,8,9,12,13,14,15) else 1
# Same dtype and PRNG operation order as inherited DC01 driver.
def initialize(seed):
    g=np.random.Generator(np.random.PCG64(seed));before=g.bit_generator.state
    W=g.uniform(-math.sqrt(6/39),math.sqrt(6/39),(16,23)).astype('f4');U=(g.uniform(-.05,.05,(16,16))+np.eye(16)*.25).astype('f4');b=np.zeros(16,'f4');V=g.uniform(-.02,.02,(2,16)).astype('f4');a=np.zeros(2,'f4')
    return np.concatenate([x.ravel() for x in (W,U,b,V,a)]),{'initial':before,'final':g.bit_generator.state}
def order(seed,n):
    g=np.random.Generator(np.random.PCG64(seed));before=g.bit_generator.state;v=[]
    while len(v)<n:v.extend(map(int,g.permutation(8)))
    return v[:n],{'initial':before,'final':g.bit_generator.state}
def read_frames_raw(path,start=0):
    with open(path,'rb') as f:
        f.seek(start)
        while True:
            h=f.read(40)
            if not h:return
            if len(h)!=40:raise ValueError('TRUNCATED_RAW_HEADER')
            n=int.from_bytes(h[:8],'little');b=f.read(n)
            if len(b)!=n or hashlib.sha256(b).digest()!=h[8:]:raise ValueError('RAW_HASH')
            yield zlib.decompress(b)

class Study:
    def __init__(self,name):
        self.path=ROOT/'raw'/name;self.path.mkdir(parents=True);(self.path/'private').mkdir()
        self.plan={'heldout_generated':False,'generated_groups':[],'targets':{},'sessions':{},'rng':{},'protocol':'reviewed v0.2 / execution v0.3'}
        self.targets={};self.weights={};self.tables={};self.xrows=[];self.wire_seen={};self.calls=0
        self.labels('old');self.save()
        self.err=open(self.path/'worker.stderr','w');env={**os.environ,'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
        self.worker=subprocess.Popen([sys.executable,str(SOURCE/'worker.py'),str(self.path/'worker')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1,env=env)
        ready=json.loads(self.worker.stdout.readline());assert ready['ready'];(self.path/'RUNTIME.json').write_text(json.dumps(ready,indent=2))
        self.requests=open(self.path/'public_messages.jsonl','w');self.responses=open(self.path/'public_responses.jsonl','w');self.send({'op':'ISOLATION_CHECK'})
    def save(self):
        p=self.path/'private/PLAN.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(self.plan,sort_keys=True,indent=2));tmp.replace(p)
    def labels(self,group):
        ranges={'old':[(0,1,2,3),(4,5,6,7)],'development':[(8,9),(10,11)],'heldout':[(12,13,14,15),(16,17,18,19)]}
        for sc,ids in enumerate(ranges[group]):
            key=f'labels/{group}/scope{sc}';g=np.random.Generator(np.random.PCG64(SEEDS[key]));before=g.bit_generator.state;vv=g.permutation(ids)
            self.targets.update({int(c):int(i<len(ids)//2) for i,c in enumerate(vv)});self.plan['rng'][key]={'initial':before,'final':g.bit_generator.state}
        self.plan['generated_groups'].append(group);self.plan['targets']=self.targets.copy()
    def send(self,msg):
        self.calls+=1;self.requests.write(json.dumps({'sequence':self.calls,'message':msg},separators=(',',':'))+'\n');self.requests.flush()
        self.worker.stdin.write(json.dumps(msg,allow_nan=False)+'\n');self.worker.stdin.flush();line=self.worker.stdout.readline()
        if not line:raise RuntimeError('WORKER_LOST:'+str(self.worker.poll()))
        ans=json.loads(line);self.responses.write(json.dumps({'sequence':self.calls,'response':ans},separators=(',',':'))+'\n');self.responses.flush()
        if 'fatal' in ans:raise RuntimeError(json.dumps(ans))
        return ans
    def txs(self,phase,base,cues,targets,delay=0):
        wk='wire/probe' if phase=='probe' else ('wire/fixture' if phase in ('fixture','derivative') else ('wire/faults' if phase=='sandbox' else 'wire/main'))
        wp='fixture' if phase in ('sandbox','derivative') else phase
        out=[]
        for i,(c,y) in enumerate(zip(cues,targets),1):
            s=f'REV01-v0.2|{SEEDS[wk]:016x}|{wp}|{base}|{i}|receipt';rid=hashlib.sha256(s.encode('ascii')).digest()[:8].hex()
            if rid=='0000000000000000':raise RuntimeError('ZERO_RECEIPT')
            identity=(wp,base,i)
            if rid in self.wire_seen and self.wire_seen[rid]!=identity:raise RuntimeError('WIRE_COLLISION')
            self.wire_seen[rid]=identity
            fillers=[]
            if phase=='fixture':
                key=f'fixture/filler/trial{i}';g=np.random.Generator(np.random.PCG64(SEEDS[key]));before=g.bit_generator.state
                v=[int(g.integers(0,4))+4*((1-scope(c)) if j%2==0 else scope(c)) for j in range(32)];fillers=v[:delay]
                self.plan['rng'][key+f'/cue{c}']={'initial':before,'final':g.bit_generator.state}
            out.append({'cue':c,'scope':scope(c),'target':y,'fillers':fillers,'receipt':rid,'wire_key':wk,'wire_phase':wp,'wire_base':base})
        return out
    def session(self,phase,arm,fit,txs,weights,table=None,candidate=False,**kw):
        spec={'phase':phase,'arm':arm,'method':arm[-1] if arm.startswith('N_') else arm,'fit':fit,'transactions':txs,**kw}
        sid=sha(canon({k:v for k,v in spec.items() if k!='transactions'}))[:24]
        if sid in self.plan['sessions']:raise RuntimeError('SESSION_COLLISION')
        self.plan['sessions'][sid]=spec;self.save()
        self.send({'op':'LOAD','weights':weights.tolist(),'arm':arm,'context':{'session':sid,'trial':0},'table':table or {},'candidate':candidate})
        return sid
    def query(self,c,kind):return self.send({'op':'QUERY','cue':c,'scope':scope(c),'meta':{'kind':kind}})
    def inventory(self,f):
        out=[self.query(f,'focal')]
        for c in range(8):out.append(self.query(c,'old'))
        return out
    def checkpoint(self,n,extra=None):return self.send({'op':'CHECKPOINT','meta':{'completed':n,**(extra or {})}})
    def transaction(self,sid,i,t,defect=None,reject=False):
        ans=self.send({'op':'CUE','cue':t['cue'],'scope':t['scope'],'receipt':t['receipt'],'context':{'session':sid,'trial':i}})
        self.send({'op':'FILLERS','codes':t['fillers']})
        receipt={'op':'RECEIPT','scope':t['scope'],'receipt':t['receipt'],'version':ans['version'],'target':t['target'],'defect':defect}
        if reject:
            checks=[{**receipt,'scope':1-t['scope']},{**receipt,'version':'0'*64}]
            if i>1:checks.append({**receipt,'receipt':self.plan['sessions'][sid]['transactions'][i-2]['receipt']})
            for bad in checks:
                r=self.send(bad);assert r.get('rejected') and r['pending_unchanged']
        return self.send(receipt)
    def branched(self,phase,base,arm,fit,txs,ww,table,delay=0):
        f,p=txs[0]['cue'],txs[1]['cue'];sid=self.session(phase,arm,fit,txs,ww,table,candidate=True,base=base,delay=delay,focal=f,protected=p)
        for i in (1,2):
            ans=self.transaction(sid,i,txs[i-1],reject=phase=='fixture');assert not ans['forked'];self.inventory(f)
        ans=self.transaction(sid,3,txs[2],reject=phase=='fixture');assert ans['forked']
        for branch in ('B1','B2'):
            self.send({'op':'SELECT','branch':branch});self.checkpoint(3);self.inventory(f)
            for i in (4,5,6):
                ans=self.transaction(sid,i,txs[i-1]);assert not ans['forked'];self.inventory(f)
            self.checkpoint(6)
    def frozen(self,phase,base,method,fit,txs,ww,table,delay=0):
        f,p=txs[0]['cue'],txs[1]['cue'];sid=self.session(phase,'N_'+method,fit,txs,ww,table,base=base,delay=delay,focal=f,protected=p)
        for i,t in enumerate(txs,1):self.transaction(sid,i,t);self.inventory(f)
        self.checkpoint(6)
    def exact(self,phase,base,txs):
        # Old table is populated by actually observed initial-fit receipts, not hidden focal labels.
        table={}
        if phase!='fixture':
            seq,_=order(SEEDS['order/main/0'],100)
            for c in seq:table[c]=self.targets[c]
        fix={0:0,1:1,2:0,3:1,4:1,5:0,6:1,7:0};f=txs[0]['cue']
        for i,t in enumerate(txs,1):
            c=t['cue'];y=t['target'];self.xrows.append({'phase':phase,'base':base,'trial':i,'kind':'raw_pre','cue':c,'target':y,'predicted':table.get(c),'correct':int(table.get(c)==y),'indexed_reads':1,'indexed_writes':1})
            table[c]=y
            for q in [f,*range(8)]:
                y=(fix[q] if phase=='fixture' else self.targets[q]) ^ int(q==f and i>=3)
                self.xrows.append({'phase':phase,'base':base,'trial':i,'kind':'focal' if q==f else 'old','cue':q,'target':y,'predicted':table.get(q),'correct':int(table.get(q)==y),'indexed_reads':1,'indexed_writes':0})
        (self.path/'EXACT.json').write_text(json.dumps(self.xrows,indent=2))
    def audit(self,stage,full=False):
        out=self.path/(stage+'_audit');cmd=[sys.executable,str(SOURCE/'scorer.py'),str(self.path),str(out)]+(['--full'] if full else [])
        with open(self.path/(stage+'_audit.stdout'),'w') as a,open(self.path/(stage+'_audit.stderr'),'w') as b:r=subprocess.run(cmd,stdout=a,stderr=b)
        if r.returncode:raise RuntimeError('INDEPENDENT_AUDIT_FAILED:'+stage)
        return json.loads((out/'AUDIT.json').read_text())
    def fixture(self):
        for coupled in (False,True):
            for nonlinear in (False,True):
                W=np.zeros((16,23),'f4');U=np.zeros((16,16),'f4');b=np.zeros(16,'f4');V=np.zeros((2,16),'f4');a=np.zeros(2,'f4');U[0,0]=U[1,1]=.5;V[1,1]=1
                if coupled:U[1,0]=.5
                if nonlinear:W[0,22]=.4
                ww=np.concatenate([p.ravel() for p in (W,U,b,V,a)])
                for arm in ('G','L'):
                    txs=self.txs('derivative',f'derivative-{arm}-{int(coupled)}{int(nonlinear)}',[0],[0]);sid=self.session('derivative',arm,-1,txs,ww,case=f'{int(coupled)}{int(nonlinear)}',coupled=coupled,nonlinear=nonlinear)
                    t=txs[0];self.send({'op':'CUE','cue':0,'scope':0,'receipt':t['receipt'],'context':{'session':sid,'trial':1}});self.send({'op':'DERIVATIVE','target':0})
        ww,rng=initialize(SEEDS['init/fixture']);self.plan['rng']['init/fixture']=rng
        for d in (0,8,32):
            ts=self.txs('fixture','clean',[0,4,0,0,4,0],[0,1,1,1,1,1],d)
            if d==0:self.exact('fixture',-1,ts)
            for arm in ('G','L'):
                self.branched('fixture',-1,arm,-1,ts,ww,{},d);self.frozen('fixture',-1,arm,-1,ts,ww,{},d)
        for arm in ('G','L'):
            for y in (0,1):
                for defect in ('sign','double'):
                    c=0 if y==0 else 4;tx=self.txs('sandbox',f'bad-{arm}-{y}-{defect}',[c],[y]);sid=self.session('sandbox',arm,-1,tx,ww,case=str(y)+defect)
                    self.transaction(sid,1,tx[0],defect=defect);self.query(c,'sandbox');self.checkpoint(1)
        self.save();self.audit('fixture')
        r=subprocess.run([sys.executable,str(SOURCE/'faults.py'),str(self.path),str(self.path/'faults')],capture_output=True,text=True)
        (self.path/'faults.stdout').write_text(r.stdout);(self.path/'faults.stderr').write_text(r.stderr)
        if r.returncode:raise RuntimeError('FAULT_SUITE_FAILED')
    def cost(self):
        ww,rr=initialize(SEEDS['init/probe']);seq,oo=order(SEEDS['order/probe'],50);self.plan['rng']['init/probe']=rr;self.plan['rng']['order/probe']=oo;ts=self.txs('probe','probe',seq,[self.targets[c] for c in seq])
        before=(self.path/'worker/records.bin').stat().st_size;t0=time.time()
        for arm in ('G','L'):
            sid=self.session('probe',arm,-1,ts,ww);self.checkpoint(0)
            for i,t in enumerate(ts,1):self.transaction(sid,i,t);self.inventory(t['cue'])
            self.checkpoint(50)
        self.save();self.audit('cost');elapsed=time.time()-t0
        # A closed sample of complete emitted envelopes, not an extrapolation of tensor bytes alone.
        raw=b''.join(struct.pack('<Q',len(x))+x for x in read_frames_raw(self.path/'worker/records.bin',before))
        comp=lzma.compress(raw,preset=6);planbytes=len(comp)*(3856/100)*2+12*1024**2
        live=sum(p.stat().st_size for p in self.path.rglob('*') if p.is_file());rawforecast=live*(3856/(100+68))/1.0+16*1024**2
        receipt={'sample_updates':100,'sample_uncompressed_envelopes':len(raw),'sample_whole_xz':len(comp),'zip_projection_bytes':planbytes,'zip_limit':64*1024**2,'whole_sample_factor':3856/100,'safety_factor':2,'additional_zip_allowance':12*1024**2,'observed_all_prefix_bytes':live,'empirical_raw_projection':rawforecast,'raw_limit':256*1024**2,'probe_wall_seconds_including_audit':elapsed,'time_projection_seconds':elapsed*(3856/100)+time.time()-json.loads((ROOT/'audit/START.json').read_text())['epoch'],'forecasts_not_formal_proofs':True}
        receipt['passed']=planbytes<=64*1024**2 and rawforecast<=256*1024**2 and receipt['time_projection_seconds']<=7200
        (self.path/'COST_ADMISSION.json').write_text(json.dumps(receipt,indent=2))
        if not receipt['passed']:raise RuntimeError('COST_ADMISSION_STOP')
    def initial(self):
        for fit in range(4):
            ww,rr=initialize(SEEDS[f'init/main/{fit}']);seq,oo=order(SEEDS[f'order/main/{fit}'],100);self.plan['rng'][f'init/main/{fit}']=rr;self.plan['rng'][f'order/main/{fit}']=oo
            ts=self.txs('initial',f'fit{fit}',seq,[self.targets[c] for c in seq])
            for arm in ('G','L'):
                sid=self.session('initial',arm,fit,ts,ww);self.checkpoint(0,{'rng':rr,'order_rng':oo})
                for i,t in enumerate(ts,1):
                    self.transaction(sid,i,t)
                    if i%25==0:cp=self.checkpoint(i,{'rng':rr,'order_rng':oo})
                self.weights[(fit,arm)]=np.array(cp['weights'],dtype='f4');self.tables[(fit,arm)]=cp['table']
            for arm in ('G','L','N_G','N_L'):
                method=arm[-1] if arm.startswith('N_') else arm;sid=self.session('warm',arm,fit,[],self.weights[(fit,method)],self.tables[(fit,method)])
                for c in range(8):self.query(c,'initial_inventory')
        self.save();self.audit('initial')
    def conditions(self,phase):
        self.labels(phase)
        if phase=='heldout':
            assert (self.path/'A0_AND_GUARDS_LOCK.json').exists();self.plan['heldout_generated']=True
        self.save()
        for base in (range(4) if phase=='development' else range(4,12)):
            f=base+8;p=[4,5,0,1,4,5,6,7,0,1,2,3][base];cues=[f,p,f,f,p,f];ys=[self.targets[c] ^ int(c==f and i>=3) for i,c in enumerate(cues,1)];ts=self.txs(phase,f'base{base:02}',cues,ys)
            self.exact(phase,base,ts)
            for fit in range(4):
                for arm in ('G','L'):
                    ww=self.weights[(fit,arm)];table=self.tables[(fit,arm)]
                    self.branched(phase,base,arm,fit,ts,ww,table);self.frozen(phase,base,arm,fit,ts,ww,table)
        self.save()
    def novelty(self):
        historical=json.loads((ROOT/'audit/HISTORICAL_SUMMARY.json').read_text());new={str(c):v for c,v in self.targets.items()};mapping={}
        for group,ids in [('old',range(8)),('development',range(8,12)),('heldout',range(12,20))]:
            if group not in self.plan['generated_groups']:continue
            current=[new[str(c)] for c in ids];old=[historical['targets'][str(c)] for c in ids]
            mapping[group]={'same_complete_label_assignment_as_DC01':current==old,'new_assignment':current,'historical_assignment':old,'coordinates_intentionally_reused':True}
        oldpatterns=set(tuple(t['target'] for t in s['transactions']) for s in historical['conditions'])
        patterns=[]
        for s in self.plan['sessions'].values():
            if s['phase'] in ('development','heldout') and s['arm']=='G' and s['fit']==0:
                pattern=tuple(t['target'] for t in s['transactions']);patterns.append({'phase':s['phase'],'base':s['base'],'labels':pattern,'abstract_label_sequence_overlap_DC01':pattern in oldpatterns})
        report={'mapping_comparisons':mapping,'patterns':patterns,'warning':'Fresh random seeds do not imply new abstract binary grammar. Maps may repeat by chance; no resampling or selective removal. Historical overlap audit is limited to retained public maps and normalized transaction-label sequences, not all latent or PRNG histories.'}
        (self.path/'NOVELTY.json').write_text(json.dumps(report,indent=2))
    def execute(self):
        self.fixture();self.cost();self.initial();self.conditions('development');dev=self.audit('development')
        gates=dev['gate'];assert len(gates)==8 and len(dev['calibration'])==2
        counts={a:sum(g['pass'] for g in gates if g['arm']==a) for a in ('G','L')};status='BASELINE_INCOMPETENT' if counts['G']<3 else ('LOCAL_RULE_COMPETENCE_DEFICIT' if counts['L']<3 else 'ADMITTED')
        lock={'status':status,'passing_fits':counts,'fits':gates,'calibration':dev['calibration'],'initial_checkpoint_digests':{f'{f}/{a}':sha(w.tobytes()) for (f,a),w in self.weights.items()},'source_lock':sha((ROOT/'audit/SOURCE_LOCK.json').read_bytes()),'heldout_not_generated':True}
        (self.path/'A0_AND_GUARDS_LOCK.json').write_text(json.dumps(lock,sort_keys=True,indent=2))
        if status=='ADMITTED':self.conditions('heldout')
        self.novelty();final=self.audit('final',full=True)
        end=self.send({'op':'CLOSE'});self.worker.wait(timeout=10);self.requests.close();self.responses.close();self.err.close();(self.path/'COUNTERS.json').write_text(json.dumps(end,indent=2));return {'admission':lock,'decisions':final.get('decisions',{})}

def main():
    s=Study(sys.argv[1])
    try:print(json.dumps(s.execute(),indent=2),flush=True)
    except BaseException:
        (s.path/'FAILED.json').write_text(json.dumps({'traceback':traceback.format_exc(),'epoch':time.time(),'rule':'preserve all attempts; no automated replay of unknown completion'},indent=2))
        try:s.worker.terminate();s.worker.wait(timeout=5)
        except Exception:pass
        raise
if __name__=='__main__':main()
