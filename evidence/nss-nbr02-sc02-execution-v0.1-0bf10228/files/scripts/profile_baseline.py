from support import *
from legacy_run import execute
import cProfile,pstats,io
from fixture_factory import episode
setup();m,mid=load(8801)
rows=[]
for n,family in [(32,'resume'),(128,'churn')]:
 for policy in ['cache','segment']:
  ep=episode(n,932101,family)
  execute(ep,m,mid,policy,audit=False)
  prof=cProfile.Profile();prof.enable()
  out=execute(ep,m,mid,policy,audit=False)
  prof.disable()
  s=io.StringIO();pstats.Stats(prof,stream=s).sort_stats('cumulative').print_stats(45)
  (ROOT/'development'/f'profile_n{n}_{family}_{policy}.txt').write_text(s.getvalue())
  rows.append({'n':n,'family':family,'policy':policy,'out':out})
  print(n,family,policy,round(out['core_seconds']*1000,3));print(s.getvalue()[:7000],flush=True)
save(ROOT/'development'/'baseline_profiles.json',{'rows':rows,'runtime':runtime(),'note':'cProfile overhead included; diagnostic only'})
