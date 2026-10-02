"""Data-only, scope/model/semantics-bound state + TWO RNG snapshots.
A research API, not production transactional storage or a Runtime integration.
"""
import json,os,shutil,tempfile
from pathlib import Path
import torch
from safetensors.torch import save_file,load_file
from .util import write_json,sha

def save(m,gc,gp,path):
    path=Path(path)
    if path.exists():raise FileExistsError('Immutable snapshot')
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=Path(tempfile.mkdtemp(prefix='.snapshot-',dir=path.parent))
    try:
        data={'z':m.z.detach().contiguous(),'rng_c':gc.get_state(),'rng_p':gp.get_state()}
        if m.p is not None:data['p']=m.p.detach().contiguous()
        if m.flag is not None:data['flag']=m.flag.contiguous()
        save_file(data,str(temp/'state.safetensors'))
        write_json(temp/'metadata.json',dict(identity=m.identity(),events=m.events,rounds=m.rounds,sha256=sha(temp/'state.safetensors')))
        os.replace(temp,path)
    finally:
        if temp.exists():shutil.rmtree(temp)

def restore(m,gc,gp,path):
    path=Path(path);meta=json.loads((path/'metadata.json').read_text());f=path/'state.safetensors'
    if meta.get('identity')!=m.identity():raise ValueError('Scope/mode/schema/weights/shape mismatch')
    if f.stat().st_size>16*1024*1024 or sha(f)!=meta.get('sha256'):raise ValueError('State integrity')
    data=load_file(str(f));expected={'z','rng_c','rng_p'}|({'p'} if m.p is not None else set())|({'flag'} if m.flag is not None else set())
    if set(data)!=expected:raise ValueError('Unexpected fields')
    for name,ref in (('z',m.z),('p',m.p),('flag',m.flag)):
        if ref is None:continue
        x=data[name]
        if x.shape!=ref.shape or x.dtype!=ref.dtype or not torch.isfinite(x).all():raise ValueError('State type/shape/value')
    for name,ref in (('rng_c',gc),('rng_p',gp)):
        x=data[name]
        if x.dtype!=torch.uint8 or x.shape!=ref.get_state().shape:raise ValueError('RNG state')
        torch.Generator().set_state(x)
    for name in ('events','rounds'):
        if type(meta.get(name))!=int or meta[name]<0:raise ValueError('Invalid clock')
    m.z=data['z'].clone()
    if m.p is not None:m.p=data['p'].clone()
    if m.flag is not None:m.flag=data['flag'].clone()
    gc.set_state(data['rng_c']);gp.set_state(data['rng_p']);m.events=meta['events'];m.rounds=meta['rounds']
