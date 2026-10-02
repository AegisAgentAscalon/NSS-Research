"""Frozen experiment scheduler. Private labels never enter worker before receipt release."""
import json,sys,os,time,hashlib,subprocess,traceback,math,zlib,struct
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'source';PROTOCOL=ROOT/'protocol'
SEEDS=json.loads((PROTOCOL/'SEED_RECIPE.json').read_text())['seeds']

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def scope(c):return 0 if c in (0,1,2,3,8,9,12,13,14,15) else 1

def init(seed):
    g=np.random.Generator(np.random.PCG64(seed));before=g.bit_generator.state
    W=g.uniform(-math.sqrt(6/39),math.sqrt(6/39),(16,23)).astype('f4');U=(g.uniform(-.05,.05,(16,16))+np.eye(16)*.25).astype('f4');b=np.zeros(16,'f4');V=g.uniform(-.02,.02,(2,16)).astype('f4');a=np.zeros(2,'f4')
    return np.concatenate([x.ravel() for x in (W,U,b,V,a)]),{'initial':before,'final':g.bit_generator.state}
def order(seed,n):
    g=np.random.Generator(np.random.PCG64(seed));before=g.bit_generator.state;v=[]
    while len(v)<n:v.extend(map(int,g.permutation(8)))
    return v[:n],{'initial':before,'final':g.bit_generator.state}
def labels(group):
    ranges={'old':[(0,1,2,3),(4,5,6,7)],'dev':[(8,9),(10,11)],'heldout':[(12,13,14,15),(16,17,18,19)]};out={};states={}
    for sc,cues in enumerate(ranges[group]):
        g=np.random.Generator(np.random.PCG64(SEEDS[f'environment/{group}/scope{sc}']));before=g.bit_generator.state;v=g.permutation(cues);out.update({int(c):int(i<len(cues)//2) for i,c in enumerate(v)});states[str(sc)]={'initial':before,'final':g.bit_generator.state}
    return out,states

def fillers(cue,key,d):
    g=np.random.Generator(np.random.PCG64(SEEDS[key]));v=[]
    for i in range(32):v.append(int(g.integers(0,4))+4*((1-scope(cue)) if i%2==0 else scope(cue)))
    return v[:d]
def ident(phase,base,d,r,trial,kind):
    s=f"DC01-v0.3|{SEEDS['public_ids']:016x}|{phase}|{base}|{d}|{r}|{trial}|{kind}";v=hashlib.sha256(s.encode()).digest()[:8]
    if int.from_bytes(v,'big')==0:raise ValueError('ZERO_ID')
    return v.hex()

class Study:
    def __init__(self,name):
        self.path=ROOT/'raw'/name;self.path.mkdir();(self.path/'private').mkdir();self.plan={'heldout_generated':False,'targets':{},'sessions':{},'rng':{},'enumerations':'see EXECUTION_COMPLETIONS.md'}
        self.targets={};self.sessions={};self.weights={};self.rawids=set();self.xrows=[]
        for group in ('old','dev'):
            y,rng=labels(group);self.targets.update(y);self.plan['rng']['labels/'+group]=rng
        self.plan['targets']=self.targets
        self.save()
        env={**os.environ,'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
        self.err=open(self.path/'worker.stderr','w');self.worker=subprocess.Popen([sys.executable,str(SOURCE/'worker.py'),str(self.path/'worker')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1,env=env)
        ready=self.worker.stdout.readline();assert json.loads(ready)['ready'];self.calls=0
        self.requests=open(self.path/'public_messages.jsonl','w')
        self.send({'op':'ISOLATION_CHECK'})
    def save(self):
        p=self.path/'private/PLAN.json';p.write_text(json.dumps(self.plan,sort_keys=True,indent=2));
    def send(self,msg):
        self.calls+=1;self.requests.write(json.dumps({'sequence':self.calls,'message':msg},separators=(',',':'))+'\n');self.requests.flush()
        self.worker.stdin.write(json.dumps(msg,allow_nan=False)+'\n');self.worker.stdin.flush();line=self.worker.stdout.readline()
        if not line:raise RuntimeError('WORKER_LOST:'+str(self.worker.poll()))
        ans=json.loads(line)
        if 'fatal' in ans:raise RuntimeError(json.dumps(ans))
        return ans
    def session(self,phase,arm,fit,transactions,weights,**kw):
        key=f'{phase}/{arm}/{fit}/{kw.get("base",-1)}/{kw.get("delay",0)}/{kw.get("reversal",0)}/{kw.get("case","")}'
        sid=hashbytes(key.encode())[:24]
        if sid in self.plan['sessions']:raise ValueError('SESSION_COLLISION')
        meta={'phase':phase,'arm':arm,'fit':fit,'transactions':transactions,**kw};self.plan['sessions'][sid]=meta;self.save()
        self.send({'op':'LOAD','weights':np.asarray(weights,dtype='f4').tolist(),'arm':arm,'context':{'session':sid,'trial':0}});return sid
    def transaction(self,sid,i,tx,defect=None,reject=False):
        sm=self.plan['sessions'][sid];cue=tx['cue'];ctx={'session':sid,'trial':i}
        receipt=ident(sm['phase'],sid,sm.get('delay',0),sm.get('reversal',0),i,'receipt')
        assert receipt not in self.rawids;self.rawids.add(receipt)
        res=self.send({'op':'CUE','cue':cue,'scope':scope(cue),'receipt':receipt,'context':ctx})
        self.send({'op':'FILLERS','codes':tx['fillers']})
        legal={'op':'RECEIPT','scope':scope(cue),'receipt':receipt,'version':res['version'],'target':tx['target'],'defect':defect}
        if reject:
            a=self.send({**legal,'scope':1-scope(cue)});assert a['rejected']=='WRONG_SCOPE' and a['pending_unchanged']
            old=ident(sm['phase'],sid,sm.get('delay',0),sm.get('reversal',0),i-1,'receipt') if i>1 else '0000000000000000'
            a=self.send({**legal,'receipt':old});assert a['rejected'] in ('UNKNOWN_ID','CONSUMED_ID') and a['pending_unchanged']
        result=self.send(legal)
        return result
    def probe(self,cue,kind):return self.send({'op':'QUERY','cue':cue,'scope':scope(cue),'meta':{'kind':kind}})
    def checkpoint(self,completed,extra=None):return self.send({'op':'CHECKPOINT','meta':{'completed':completed,**(extra or {})}})
    def diagnostics_fixture(self):
        for coupled in (False,True):
            for nonlinear in (False,True):
                W=np.zeros((16,23),'f4');U=np.zeros((16,16),'f4');b=np.zeros(16,'f4');V=np.zeros((2,16),'f4');a=np.zeros(2,'f4');U[0,0]=U[1,1]=.5;V[1,1]=1
                if coupled:U[1,0]=.5
                if nonlinear:W[0,22]=.4
                ww=np.concatenate([p.ravel() for p in (W,U,b,V,a)])
                for arm in ('G','L'):
                    tx={'cue':0,'target':0,'fillers':[]};sid=self.session('derivative',arm,-1,[tx],ww,case=f'{int(coupled)}{int(nonlinear)}',coupled=coupled,nonlinear=nonlinear)
                    rid=ident('derivative',sid,0,0,1,'receipt');self.send({'op':'CUE','cue':0,'scope':0,'receipt':rid,'context':{'session':sid,'trial':1}});self.send({'op':'DERIVATIVE','target':0})
        weights,rng=init(SEEDS['initialization/fixture']);self.plan['rng']['initialization/fixture']=rng
        for case,(y,d) in enumerate(( (y,d) for y in (0,1) for d in (0,8,32))):
            cue=0 if y==0 else 4;tx={'cue':cue,'target':y,'fillers':fillers(cue,f'filler/fixture/{case}',d)}
            for arm in ('G','L'):
                sid=self.session('fixture',arm,-1,[tx],weights,case=case,delay=d);self.transaction(sid,1,tx);self.probe(cue,'fixture_probe');self.checkpoint(1)
        for arm in ('G','L'):
            for y in (0,1):
                for defect in ('sign','double'):
                    cue=0 if y==0 else 4;tx={'cue':cue,'target':y,'fillers':[]};sid=self.session('sandbox',arm,-1,[tx],weights,case=str(y)+defect);self.transaction(sid,1,tx,defect=defect);self.checkpoint(1)
        self.save()
        self.audit('fixture_audit')
        subprocess.run([sys.executable,'-c','from faults import exercise;import sys;exercise(sys.argv[1],sys.argv[2])',str(self.path),str(self.path/'faults')],cwd=SOURCE,check=True,stdout=open(self.path/'faults.stdout','w'),stderr=open(self.path/'faults.stderr','w'))
        self.delay_check()
    def audit(self,name):
        out=self.path/name
        with open(self.path/(name+'.stdout'),'w') as stdout,open(self.path/(name+'.stderr'),'w') as stderr:
            result=subprocess.run([sys.executable,str(SOURCE/'auditor.py'),str(self.path),str(out)],stdout=stdout,stderr=stderr)
        if result.returncode:raise RuntimeError('INDEPENDENT_AUDIT_FAILED:'+name)
        return json.loads((out/'AUDIT.json').read_text())
    def cost(self):
        ww,rng=init(SEEDS['initialization/cost']);seq,rr=order(SEEDS['order/cost'],50);self.plan['rng']['initialization/cost']=rng;self.plan['rng']['order/cost']=rr
        txs=[{'cue':c,'target':self.targets[c],'fillers':[]} for c in seq];start=time.time();before=(self.path/'worker/records.bin').stat().st_size
        for arm in ('G','L'):
            sid=self.session('cost',arm,-1,txs,ww);self.checkpoint(0)
            for i,tx in enumerate(txs,1):self.transaction(sid,i,tx)
            self.checkpoint(50)
        self.save();self.audit('cost_audit');elapsed=time.time()-start;growth=(self.path/'worker/records.bin').stat().st_size-before
        from storage_admission import admit
        receipt=admit(self.path, growth, elapsed, before)
        (self.path/'COST_ADMISSION.json').write_text(json.dumps(receipt,indent=2))
        if not receipt['passed']:raise RuntimeError('REVISED_COST_ADMISSION_FAIL')
    def initial(self):
        for fit in range(4):
            ww,rng=init(SEEDS[f'initialization/main/{fit}']);seq,rr=order(SEEDS[f'order/main/{fit}'],100);self.plan['rng'][f'initialization/main/{fit}']=rng;self.plan['rng'][f'order/main/{fit}']=rr;txs=[{'cue':c,'target':self.targets[c],'fillers':[]} for c in seq]
            for arm in ('G','L'):
                sid=self.session('initial',arm,fit,txs,ww);self.checkpoint(0)
                for i,tx in enumerate(txs,1):
                    self.transaction(sid,i,tx)
                    if i%25==0:ans=self.checkpoint(i)
                self.weights[(fit,arm)]=np.array(ans['weights'],dtype='f4')
            for arm in ('G','L','N_G','N_L'):
                base=arm[-1] if arm.startswith('N_') else arm;sid=self.session('warm',arm,fit,[],self.weights[(fit,base)])
                for c in range(8):self.probe(c,'warm_inventory')
        self.save();self.audit('initial_audit')
    def conditions(self,phase):
        if phase=='heldout':
            y,rng=labels('heldout');self.targets.update(y);self.plan['targets']=self.targets;self.plan['rng']['labels/heldout']=rng;self.plan['heldout_generated']=True;self.save()
        bases=[(8,4),(9,5),(10,0),(11,1),(12,4),(13,5),(14,6),(15,7),(16,0),(17,1),(18,2),(19,3)]
        indices=range(4) if phase=='development' else range(4,12)
        for base in indices:
            f,p=bases[base]
            for d in (0,8,32):
                for rev in (0,1):
                    txs=[]
                    for i,c in enumerate((f,p,f,f,p,f),1):txs.append({'cue':c,'target':self.targets[c]^(int(rev and i>=3 and c==f)),'fillers':fillers(c,f'filler/base/{base:02}/trial/{i}',d)})
                    self.exact(phase,base,d,rev,f,txs)
                    for fit in range(4):
                        for arm in ('G','L','N_G','N_L'):
                            parent=arm[-1] if arm.startswith('N') else arm;sid=self.session(phase,arm,fit,txs,self.weights[(fit,parent)],base=base,delay=d,reversal=rev,focal=f,protected=p)
                            for i,tx in enumerate(txs,1):
                                self.transaction(sid,i,tx)
                                if i>=2:self.probe(tx['cue'],'primary')
                            for c in [*range(8),f]:self.probe(c,'inventory')
                            self.checkpoint(6)
        self.save();self.delay_check()
    def exact(self,phase,base,d,rev,f,txs):
        # Only labels actually observed by each initial-fit history enter the causal table.
        table={}
        for c in order(SEEDS['order/main/0'],100)[0]:table[c]=self.targets[c]
        for i,tx in enumerate(txs,1):
            c=tx['cue'];before=table.get(c)
            self.xrows.append({'phase':phase,'base':base,'delay':d,'reversal':rev,'trial':i,'kind':'raw_pre','cue':c,'target':tx['target'],'predicted':before,'correct':int(before==tx['target'])})
            table[c]=tx['target']
            if i>=2:self.xrows.append({'phase':phase,'base':base,'delay':d,'reversal':rev,'trial':i,'kind':'primary','cue':c,'target':tx['target'],'predicted':table[c],'correct':int(table[c]==tx['target'])})
        for c in [*range(8),f]:
            y=self.targets[c]^int(rev and c==f);self.xrows.append({'phase':phase,'base':base,'delay':d,'reversal':rev,'trial':6,'kind':'inventory','cue':c,'target':y,'predicted':table[c],'correct':int(table[c]==y)})
        (self.path/'EXACT_CONTROL.json').write_text(json.dumps(self.xrows,indent=2))
    def diagnostic(self):
        for fit in range(4):
            txs=[{'cue':c,'target':self.targets[c],'fillers':fillers(c,f'filler/receipt_diagnostic/fit/{fit}/trial/{i}',8)} for i,c in enumerate((4,0,5,1,6,2),1)]
            for arm in ('G','L'):
                sid=self.session('receipt_diagnostic',arm,fit,txs,self.weights[(fit,arm)],delay=8)
                for i,tx in enumerate(txs,1):
                    self.transaction(sid,i,tx,reject=True)
                    if i>=2:self.probe(tx['cue'],'diagnostic_probe')
                self.checkpoint(6)
        self.save()
    def delay_check(self):
        from auditor import records
        groups={};comparisons=0;elements=0
        for k,m,a in records(self.path/'worker/records.bin'):
            sm=self.plan['sessions'][m['context']['session']]
            if sm['phase'] not in ('fixture','development','heldout') or m['kind'] not in ('cue','update','frozen_receipt','query'):continue
            if sm['phase']=='fixture':key=(sm['phase'],m['arm'],sm['transactions'][0]['target'],m['kind'])
            else:key=(sm['phase'],m['arm'],sm['fit'],sm['base'],sm['reversal'],m['context']['trial'],m['kind'],m.get('query',{}).get('kind'),m.get('cue',-1))
            vals={k:a[k] for k in a}
            if key not in groups:groups[key]=(sm.get('delay',0),vals)
            else:
                d0,old=groups[key]
                if d0==sm.get('delay',0):raise ValueError('DUPLICATE_DELAY_KEY')
                assert old.keys()==vals.keys()
                for name,v in vals.items():assert np.array_equal(v,old[name]),'DELAY_DIFFERENCE:'+str(key)+name;comparisons+=1;elements+=v.size
        (self.path/'DELAY_INVARIANCE.json').write_text(json.dumps({'status':'PASS','array_comparisons':comparisons,'elements':elements,'live_fillers_timing_costs_excluded':True},indent=2))
    def execute(self):
        self.diagnostics_fixture();self.cost();self.initial();self.conditions('development');self.diagnostic();self.save();dev=self.audit('development_audit')
        gates=dev['gate'];passed={a:sum(r['pass'] for r in gates if r['arm']==a) for a in ('G','L')}
        if len(gates)!=8:raise ValueError('GATE_DENOMINATOR')
        status='BASELINE_INCOMPETENT' if passed['G']<3 else ('LOCAL_RULE_COMPETENCE_DEFICIT' if passed['L']<3 else 'ADMITTED')
        decision={'status':status,'passing_fits':passed,'individual':gates,'heldout_generation_permitted':status=='ADMITTED'}
        (self.path/'A0_DECISION.json').write_text(json.dumps(decision,indent=2))
        if status=='ADMITTED':self.conditions('heldout')
        self.save();final=self.audit('final_audit');end=self.send({'op':'CLOSE'});self.worker.wait(timeout=10);self.requests.close();self.err.close();(self.path/'COUNTERS.json').write_text(json.dumps(end,indent=2));return decision

def main():
    which=sys.argv[1];s=Study(which)
    try:
        result=s.execute();print(json.dumps(result),flush=True)
    except BaseException:
        (s.path/'FAILED.json').write_text(json.dumps({'traceback':traceback.format_exc(),'time':time.time(),'completion':'consult durable intents/commits; no automatic reapply'},indent=2))
        try:s.worker.terminate();s.worker.wait(timeout=5)
        except Exception:pass
        raise
if __name__=='__main__':main()
