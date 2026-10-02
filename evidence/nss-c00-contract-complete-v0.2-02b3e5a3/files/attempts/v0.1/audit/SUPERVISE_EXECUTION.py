from pathlib import Path
import subprocess,sys,os,time,json,datetime,signal
import psutil
root=Path('/mnt/data/NSS_C00_Contract_Execution_v0.1')
stages=[('build_primary',['source/build_cases.py','inputs/primary']),('primary',['source/run.py','inputs/primary','raw/primary']),('score_primary',['source/check.py','inputs/primary','raw/primary','results/primary']),('build_replay',['source/build_cases.py','inputs/replay']),('replay',['source/run.py','inputs/replay','raw/replay']),('score_replay',['source/check.py','inputs/replay','raw/replay','results/replay'])]
receipts=[]; start=time.monotonic();env=os.environ.copy();env['PYTHONHASHSEED']='0';env['PYTHONDONTWRITEBYTECODE']='1'
for name,args in stages:
    t=time.monotonic();log=root/'audit'/f'{name}.log'; peak=0;status='COMPLETED'
    with log.open('wb') as f:
        p=subprocess.Popen([sys.executable]+args,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
        while p.poll() is None:
            try:
                pro=psutil.Process(p.pid);rss=sum(x.memory_info().rss for x in [pro]+pro.children(recursive=True) if x.is_running());peak=max(peak,rss)
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            if peak>1073741824 or time.monotonic()-start>1800:
                status='CAP_STOP';p.terminate();p.wait();break
            time.sleep(.025)
        ret=p.returncode
    receipts.append({'stage':name,'command':[sys.executable]+args,'returncode':ret,'status':status if ret==0 else 'FAILED','wall_seconds':time.monotonic()-t,'sampled_tree_peak_bytes':peak,'sample_interval_seconds':.025,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    (root/'audit/EXECUTION.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print(name,'return',ret,'time',receipts[-1]['wall_seconds'],'rss',peak,flush=True)
    if ret!=0:
        print(log.read_text(),flush=True);sys.exit(ret)
print('all requested stages completed')
