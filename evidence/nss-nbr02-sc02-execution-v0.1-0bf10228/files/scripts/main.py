from support import *
from runner import execute,POLICIES
import argparse,traceback,gc

def main():
 a=argparse.ArgumentParser();a.add_argument('--n',type=int,required=True);args=a.parse_args()
 setup();start=time.perf_counter();done=[]
 for seed in [942201,942202]:
  for ms in [8801,8802,8804]:
   model,mid=load(ms)
   for p in sorted((ROOT/'fixtures').glob(f'n{args.n}_s{seed}_*.json')):
    ep=json.loads(p.read_text())
    for variant in POLICIES:
     dest=ROOT/'results'/'episodes'/f'{ep["id"]}_m{ms}_{variant}.json'
     if dest.exists():raise RuntimeError('Refusing to overwrite main output')
     try:
      out=execute(ep,model,mid,variant,audit=True,snap_dir=(ROOT/'results'/'snapshots')if ms==8801 and ep['family']=='resume'and variant in ('P','I')else None)
      out['model_seed']=ms;out['runtime']=runtime();save(dest,out)
      done.append({'file':dest.name,'numeric_violations':out['numeric_violations'],'changed_classes':out['changed_classes'],'answers':out['answers'],'core_seconds':out['core_seconds']})
     except Exception:
      save(ROOT/'failures'/f'main_{dest.stem}.json',{'traceback':traceback.format_exc(),'runtime':runtime(),'completed':done})
      raise
     if runtime()['peak_rss_bytes']>2*1024**3 or time.perf_counter()-start>180:raise RuntimeError('PROCESS_RESOURCE_GUARD')
   save(ROOT/'results'/f'main_progress_n{args.n}.json',{'completed':done,'runtime':runtime(),'elapsed_seconds':time.perf_counter()-start})
   print('main',args.n,seed,ms,'conditions',len(done),flush=True)
 save(ROOT/'results'/f'main_n{args.n}.json',{'status':'COMPLETE','conditions':done,'elapsed_seconds':time.perf_counter()-start,'runtime':runtime(),'optimizer_applications':0})
 print('COMPLETE',args.n,len(done),round(time.perf_counter()-start,2),flush=True)
if __name__=='__main__':main()
