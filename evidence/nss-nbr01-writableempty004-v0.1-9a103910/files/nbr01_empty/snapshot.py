"""Scoped data-only checkpoints for the research state and RNG.
This is not the production foundation's state owner or generic Runtime.
"""
import json,os,shutil,tempfile
from pathlib import Path
import torch
from safetensors.torch import save_file,load_file
from .util import write_json,sha

def save(memory,generator,path):
    path=Path(path)
    if path.exists():raise FileExistsError('Snapshot is immutable')
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=Path(tempfile.mkdtemp(prefix='.snapshot-',dir=path.parent))
    try:
        tensors={'z':memory.z.detach().contiguous(),'rng':generator.get_state()}
        if memory.presence is not None:tensors['presence']=memory.presence.contiguous()
        save_file(tensors,str(temp/'state.safetensors'))
        write_json(temp/'metadata.json',{'identity':memory.identity(),'events':memory.events,'rounds':memory.rounds,
            'sha256':sha(temp/'state.safetensors')})
        os.replace(temp,path)
    finally:
        if temp.exists():shutil.rmtree(temp)

def restore(memory,generator,path):
    path=Path(path);meta=json.loads((path/'metadata.json').read_text())
    if meta.get('identity')!=memory.identity():raise ValueError('Scope, mode, schema or weights mismatch')
    file=path/'state.safetensors'
    if file.stat().st_size>16*1024*1024:raise ValueError('Oversize state')
    if sha(file)!=meta.get('sha256'):raise ValueError('State checksum mismatch')
    data=load_file(str(file));expected={'z','rng'}|({'presence'} if memory.presence is not None else set())
    if set(data)!=expected:raise ValueError('Unexpected state fields')
    z=data['z']
    if z.shape!=memory.z.shape or z.dtype!=torch.float32 or not torch.isfinite(z).all():raise ValueError('Invalid neural state')
    if 'presence' in data and (data['presence'].shape!=memory.presence.shape or data['presence'].dtype!=torch.bool):raise ValueError('Invalid presence')
    if data['rng'].dtype!=torch.uint8 or data['rng'].shape!=generator.get_state().shape:raise ValueError('Invalid RNG')
    for k in ('events','rounds'):
        if type(meta.get(k))!=int or meta[k]<0:raise ValueError('Invalid clock')
    # Validate RNG on a throwaway generator before any mutation.
    trial=torch.Generator();trial.set_state(data['rng'])
    memory.z=z.clone()
    if memory.presence is not None:memory.presence=data['presence'].clone()
    generator.set_state(data['rng']);memory.events=meta['events'];memory.rounds=meta['rounds']
