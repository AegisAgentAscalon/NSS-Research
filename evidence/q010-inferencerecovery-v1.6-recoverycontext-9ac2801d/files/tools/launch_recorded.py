from pathlib import Path
import subprocess,sys,json,os,datetime
R=Path('/mnt/data/NSS_NBR01_Q010_InfrastructureRepair_v1.3');S=R/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0';A=S/'implementation_A';B=S/'verification_B'
name=sys.argv[1];cwd=sys.argv[2];cmd=sys.argv[3:]
env=os.environ.copy();env.update(PYTHONPATH=os.pathsep.join(map(str,(R/'source',A,B))),OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
log=R/'logs'/f'{name}_supervisor.log'
with log.open('xb') as out:
 p=subprocess.Popen([sys.executable,str(R/'tools/run_logged.py'),'--root',str(R/'logs'),'--id',name,'--seconds','1200','--rss-mib','1800','--cwd',cwd,'--',*cmd],env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
receipt={'pid':p.pid,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':cwd,'log':str(log)}
(R/'logs'/f'{name}_launch.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
