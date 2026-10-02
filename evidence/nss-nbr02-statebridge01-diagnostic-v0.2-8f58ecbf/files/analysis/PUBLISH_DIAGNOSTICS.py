"""Independent rescoring and numerical reconstruction; no torch, producer or data imports."""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from reference import KEYS,SHAPES,from_flat,forward,gradient,oracle,sigmoid,softmax

def read(p):
    with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def jload(p):return json.loads(p.read_text())
def jwrite(p,o):p.write_text(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n')
def outcsv(p,rows):
    with open(p,'w',newline='') as f:
        if rows:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
class Check:
    def __init__(self,atol,rtol):self.n=0;self.r=0.;self.bad=[];self.atol=atol;self.rtol=rtol
    def compare(self,a,b,name):
        a=np.asarray(a,np.float64);b=np.asarray(b,np.float64)
        if a.shape!=b.shape or not np.isfinite(a).all() or not np.isfinite(b).all():raise RuntimeError('SHAPE_OR_NONFINITE '+name)
        q=np.abs(a-b)/(self.atol+self.rtol*np.abs(b));self.n+=a.size;self.r=max(self.r,float(q.max(initial=0)))
        if np.any(q>1):self.bad.append({'item':name,'ratio':float(q.max())})
    def finish(self):
        if self.bad:raise RuntimeError('INDEPENDENT_NUMERICAL_FAILURE '+str(self.bad[:8]))

def trace_check(w,events,states,logits,check,label,h=None):
    hs,lo,_=forward(w,events,h);check.compare(states,hs,label+'/h');check.compare(logits,lo,label+'/z')

def score_out(logits,truth,nxt):
    bits=logits[:4]>0;act=int(np.argmax(logits[4:]));correct=bool(np.array_equal(bits,truth.astype(bool)) and act==int(nxt))
    bz=logits[:4].astype(np.float64);z=logits[4:].astype(np.float64);mx=z.max()
    loss=float(np.mean(np.logaddexp(0,bz)-truth*bz)+mx+np.log(np.exp(z-mx).sum())-z[int(nxt)])
    return correct,float(np.mean(bits==truth)),bool(act==int(nxt)),loss

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--input',required=True);pa.add_argument('--output',required=True);pa.add_argument('--config',required=True);args=pa.parse_args()
    src=Path(args.input);out=Path(args.output);out.mkdir(parents=True,exist_ok=False);conf=jload(Path(args.config));ch=Check(conf['float_atol'],conf['float_rtol'])
    query=[];brows=[];effects=[];versions=0;updates=0;gate=[];wfiles={}
    # Reconstruct every saved exact online/repair derivative independently at its own prestate.
    for p in sorted(src.rglob('update_*.npz')):
        r=read(p);w=from_flat(r['pre']);l,g=gradient(w,r)
        ch.compare(r['gradient'],g,str(p.relative_to(src))+'/gradient');ch.compare(r['stats'][0],l,str(p)+'/loss')
        for kind in ['A','B']:
            if kind+'_events' in r:trace_check(w,r[kind+'_events'],r[kind+'_states'],r[kind+'_logits'],ch,str(p)+'/'+kind)
        # Exact byte checks use captured operands under the frozen single-example/batch arithmetic.
        grad=r['gradient'];factor=np.float32(r['stats'][2]);lr=np.float32(r['stats'][3]);product=(grad*factor)*lr
        if not np.array_equal(product,r['product']) or not np.array_equal(r['pre']-product,r['post']):raise RuntimeError('SGD_BYTES '+str(p))
        ch.compare(r['stats'][1],np.linalg.norm(g),str(p)+'/raw_norm');updates+=1
    for f in range(conf['fits']):
        path=src/f'gate/fit{f}/EVIDENCE.npz'
        if not path.exists():continue
        e=read(path);w=read(src/f'train/fit{f}/terminal.npz');ls=e['lengths'];ev=e['events'];ss=e['suffix']
        flat=np.concatenate([w[k].ravel() for k in KEYS]);wf=from_flat(flat)
        for n in sorted(set(map(int,ls))):
            ii=np.flatnonzero(ls==n);trace_check(wf,ev[ii,:n],e['prefix_states'][ii,:n],e['prefix_logits'][ii,:n],ch,'gateprefix')
        truth=[];nexts=[]
        for seq,n in zip(ev,ls):
            b,a=oracle(np.r_[seq[:n],ss]);truth.append(b[0,int(n)-1:]);nexts.append(a[0,int(n)-1:])
        truth=np.array(truth);nexts=np.array(nexts)
        if not np.array_equal(e['truth'][...,:4],truth) or not np.array_equal(e['truth'][...,4],nexts):raise RuntimeError('GATE_TARGETS')
        aok=[];zok=[]
        for i in range(len(ev)):
            for pos in conf['read_positions']:
                aok.append(score_out(e['carry'][i,pos],truth[i,pos],nexts[i,pos])[0]);zok.append(score_out(e['reset'][i,pos],truth[i,pos],nexts[i,pos])[0])
        by=read(src/f'train/fit{f}/INPUTS.npz')['b_labels'];bc=int(np.sum((e['B_logits'][:,0]>0)==by))
        passed=np.mean(aok)>=conf['a0_joint_min'] and bc==4 and np.mean(aok)-np.mean(zok)>=conf['a0_state_advantage']
        rec={'fit':f,'A_joint':float(np.mean(aok)),'RESET_joint':float(np.mean(zok)),'B_correct':bc,'pass':bool(passed)}
        orig=jload(src/f'gate/fit{f}/DECISION.json')
        if any(rec[k]!=orig[k] for k in rec):raise RuntimeError('A0_DISAGREEMENT')
        gate.append(rec)
    for ctx in sorted((src/'contexts').glob('*')) if (src/'contexts').exists() else []:
        meta=jload(ctx/'CONTEXT.json');comp=jload(ctx/'COMPLETE.json');pub=read(ctx/'PUBLIC.npz');ev=pub['events'];lengths=pub['lengths'];s=pub['suffix']
        truth=[];acts=[]
        for e,n in zip(ev,lengths):
            b,a=oracle(np.r_[e[:n],s]);truth.append(b[0,int(n)-1:]);acts.append(a[0,int(n)-1:])
        truth=np.array(truth);acts=np.array(acts);w0=read(ctx/'weights_0.npz');parent=from_flat(np.concatenate([w0[k].ravel() for k in KEYS]));h0=pub['initial_h']
        for n in sorted(set(map(int,lengths))):
            ii=np.flatnonzero(lengths==n);hh,lo,_=forward(parent,ev[ii,:n]);ch.compare(h0[ii],hh[:,-1],'h0')
            ch.compare(pub['initial_prefix_states'][ii,:n],hh,'initialprefixstate');ch.compare(pub['initial_prefix_logits'][ii,:n],lo,'initialprefixlogit')
        last=None
        for k in range(12):
            r=read(ctx/f'update_{k:02d}.npz')
            if k==0:last=np.concatenate([w0[n].ravel() for n in KEYS])
            if not np.array_equal(last,r['pre']):raise RuntimeError('UPDATE_CHAIN')
            last=r['post']
            if k in [7,11]:
                wx=read(ctx/f'weights_{1 if k==7 else 2}.npz')
                if not np.array_equal(last,np.concatenate([wx[n].ravel() for n in KEYS])):raise RuntimeError('STAGE_WEIGHTS')
        oldy=np.array(meta['old_B_labels']);newy=oldy.copy();newy[meta['focal_cue']]=1-newy[meta['focal_cue']]
        for stage in range(3):
            w=read(ctx/f'weights_{stage}.npz');wf=from_flat(np.concatenate([w[k].ravel() for k in KEYS]));a=read(ctx/f'A_stage_{stage}.npz')
            for n in sorted(set(map(int,lengths))):
                ii=np.flatnonzero(lengths==n);hs,lo,_=forward(wf,ev[ii,:n]);ch.compare(a['prefix_states'][ii,:n],hs,'rebuildprefixh');ch.compare(a['prefix_logits'][ii,:n],lo,'rebuildprefixz');ch.compare(a['rebuilt_h'][ii],hs[:,-1],'rebuilt_h')
            for mode in ['CARRY','REBUILD','RESET','PINNED']:
                h={'CARRY':h0,'REBUILD':a['rebuilt_h'],'RESET':np.zeros_like(h0),'PINNED':h0}[mode]
                mw=parent if mode=='PINNED' else wf
                hs,lo,_=forward(mw,np.tile(s,(32,1)),h);hfull=np.concatenate([h[:,None],hs],1)
                zfull=np.concatenate([(h.astype(np.float64)@mw['head.weight'].T+mw['head.bias'])[:,None],lo],1)
                ch.compare(a[mode+'_states'],hfull,'resumeh');ch.compare(a[mode+'_logits'],zfull,'resumez')
                for i in range(32):
                    for pos in conf['read_positions']:
                        ok,bitok,nextok,loss=score_out(a[mode+'_logits'][i,pos],truth[i,pos],acts[i,pos])
                        query.append({'split':meta['split'],'fit':meta['fit'],'case':meta['case'],'cue':meta['focal_cue'],'order':meta['order'],
                         'stage':stage,'mode':mode,'history':i,'prefix_length':int(lengths[i]),'suffix_position':pos,'joint_correct':int(ok),'bit_accuracy':bitok,'next_correct':int(nextok),'loss':loss})
                effects.append({'split':meta['split'],'fit':meta['fit'],'case':meta['case'],'stage':stage,'mode':mode,
                  'state_L2_from_saved':float(np.linalg.norm(h.astype(float)-h0.astype(float),axis=-1).mean()),
                  'rebuild_extra_transitions':int(lengths.sum()) if mode=='REBUILD' else 0,'active_A_state_bytes':int(h.nbytes),
                  'parameter_tensor_bytes':int(sum(np.asarray(v).size*4 for v in mw.values())),
                  'pinned_extra_parameter_bytes':65316 if mode=='PINNED' and stage>0 else 0})
            if not np.array_equal(a['PINNED_logits'],read(ctx/'A_stage_0.npz')['CARRY_logits']):raise RuntimeError('PINNED_ROUTING_CHANGED')
            for typ in ['','PINNED_']:
                b=read(ctx/f'B_{typ}stage_{stage}.npz');mw=parent if typ else wf;hs,lo,_=forward(mw,b['events'])
                ch.compare(b['states'],hs,'B_states');ch.compare(b['logits'],lo[:,-1],'B_logits')
                y=oldy if stage==0 else newy
                for c in range(4):
                    z=float(b['logits'][c,0]);loss=float(np.logaddexp(0,z)-int(y[c])*z)
                    brows.append({'split':meta['split'],'fit':meta['fit'],'case':meta['case'],'stage':stage,'weight_path':'PINNED_OLD' if typ else 'CURRENT',
                      'cue':c,'focal':int(c==meta['focal_cue']),'target':int(y[c]),'correct':int((z>0)==bool(y[c])),'loss':loss})
            versions+=1
    # Aggregate with paired histories kept explicit. No IID confidence intervals.
    aggregate=[]
    for split in ['dev','test']:
        for stage in range(3):
            for mode in ['CARRY','REBUILD','RESET','PINNED']:
                rr=[r for r in query if r['split']==split and r['stage']==stage and r['mode']==mode]
                if rr:aggregate.append({'split':split,'stage':stage,'mode':mode,'correct':sum(r['joint_correct'] for r in rr),'n':len(rr),'accuracy':sum(r['joint_correct'] for r in rr)/len(rr),'mean_loss':float(np.mean([r['loss'] for r in rr]))})
    bsum=[]
    for split in ['dev','test']:
        for stage in range(3):
            for mode in ['CURRENT','PINNED_OLD']:
                for focal in [0,1]:
                    rr=[r for r in brows if r['split']==split and r['stage']==stage and r['weight_path']==mode and r['focal']==focal]
                    if rr:bsum.append({'split':split,'stage':stage,'weights':mode,'focal':focal,'correct':sum(r['correct'] for r in rr),'n':len(rr),'mean_loss':float(np.mean([r['loss'] for r in rr]))})
    pairs=[]
    for split in ['dev','test']:
        for fit in range(4):
            for case in range(2 if split=='dev' else 8):
                for stage in range(3):
                    def select(mode):return [r for r in query if (r['split'],r['fit'],r['case'],r['stage'],r['mode'])==(split,fit,case,stage,mode)]
                    c,r,z,p=[select(m) for m in ['CARRY','REBUILD','RESET','PINNED']]
                    if not c:continue
                    pair={'split':split,'fit':fit,'case':case,'stage':stage,'n':len(c)}
                    for name,rr in [('carry',c),('rebuild',r),('reset',z),('pinned',p)]:pair[name+'_correct']=sum(x['joint_correct'] for x in rr);pair[name+'_loss']=float(np.mean([x['loss'] for x in rr]))
                    pair['rebuild_rescues']=sum(a['joint_correct']==0 and b['joint_correct']==1 for a,b in zip(c,r));pair['carry_rescues']=sum(a['joint_correct']==1 and b['joint_correct']==0 for a,b in zip(c,r))
                    pairs.append(pair)
    decisions=[]
    for mode in ['carry','rebuild']:
        ok=0;counts=[0]*4
        for row in pairs:
            if row['split']!='test' or row['stage']!=2:continue
            old=next(p for p in pairs if (p['split'],p['fit'],p['case'],p['stage'])==('test',row['fit'],row['case'],0))
            focal=next(b for b in brows if (b['split'],b['fit'],b['case'],b['stage'],b['weight_path'],b['focal'])==('test',row['fit'],row['case'],2,'CURRENT',1))
            good=(row[mode+'_correct']/row['n']>=.95 and (old['carry_correct']-row[mode+'_correct'])/row['n']<=.05 and focal['correct']==1)
            ok+=good;counts[row['fit']]+=int(good)
        if any(p['split']=='test' for p in pairs):decisions.append({'mode':mode,'cycles_pass':int(ok),'cycles_total':32,'per_fit':counts,'screen_pass':bool(ok>=29 and min(counts)>=6)})
    # Original strict checker remains failed; export diagnostic scores without altering predictions.
    outcsv(out/'A_QUERIES.csv',query);outcsv(out/'A_AGGREGATES.csv',aggregate);outcsv(out/'B_QUERIES.csv',brows);outcsv(out/'B_AGGREGATES.csv',bsum);outcsv(out/'PAIRED_CONTEXTS.csv',pairs);outcsv(out/'STATE_COSTS.csv',effects)
    outcsv(out/'A_NEGATIVES.csv',[r for r in query if not r['joint_correct']]);outcsv(out/'B_NEGATIVES.csv',[r for r in brows if not r['correct']]);outcsv(out/'A0.csv',gate)
    jwrite(out/'DECISIONS.json',decisions)
    jwrite(out/'AUDIT.json',{'strict_numerical_pass':not bool(ch.bad),'strict_numerical_failures':ch.bad,'original_strict_scorer_completed':False,'scalar_comparisons':ch.n,'max_tolerance_ratio':ch.r,'exact_sgd_updates_checked':updates,'stage_weight_sets':versions,'no_torch_import':True,'A_query_rows':len(query),'B_query_rows':len(brows),'A_negatives':sum(not r['joint_correct'] for r in query),'B_negatives':sum(not r['correct'] for r in brows),'source_status':jload(src/'STATUS.json')['status']})
    print(json.dumps({'audit':jload(out/'AUDIT.json'),'A':aggregate,'B':bsum,'decisions':decisions}),flush=True)
if __name__=='__main__':main()
