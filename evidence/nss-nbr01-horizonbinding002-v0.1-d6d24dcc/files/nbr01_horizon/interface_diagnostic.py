"""POST-HOC diagnostic: selected record vs explicit qualified-event encoding.

The latter is a declared NEW VIEW, not a rewrite of original source confidence.
Original observations are retained unchanged. In this synthetic task only,
qualification is exactly computable from the supplied observation policy.
"""
from __future__ import annotations
import json,time,hashlib
from pathlib import Path
import torch
from .data import exact_latest,evaluation_batch,digest
from .evaluate import predict,metrics
from .util import load_model,write_json,weights_digest,sha


def run(root,output):
    root,output=Path(root),Path(output);output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in sorted((root/'evidence/main').glob('tape_reader_*.safetensors')):
        tr=json.loads(p.with_suffix('.json').read_text());m=load_model(p,'tape_reader');before=weights_digest(m)
        for condition in ['retain','near_write','noisy_observation']:
            for horizon in [0,4096]:
                x,y,protected=evaluation_batch(tr['seed'],condition,horizon)
                before_data=digest(x,y)
                observed_policy,records=exact_latest(x)
                # The new view encodes "the exact service qualified this event"
                # in the model's trained WRITE-strength range. This .85 is NOT
                # the original source score and must never be stored as such.
                qualified=records.clone();mask=observed_policy<8
                qualified[:,:,2]=torch.where(mask,.85,qualified[:,:,2])
                for view,events in [('raw_selected_records',records),('qualified_event_view',qualified)]:
                    pred=predict(m,events,'native')
                    rows.append(dict(seed=tr['seed'],curriculum=tr['curriculum'],view=view,
                        condition=condition,horizon=horizon,**metrics(pred,y,protected),
                        dataset_sha256=before_data,
                        agreement_with_observation_only_ledger=int((pred==observed_policy).sum())))
                if digest(x,y)!=before_data:raise RuntimeError('Original evidence changed')
        if weights_digest(m)!=before:raise RuntimeError('Weights changed')
    result=dict(status='POST_HOC_EXPLORATORY_RUN',rows=rows,source_observations_unchanged=True,
        evaluation_weight_updates=0,main_results_unchanged=True,
        intervention='Dedicated synthetic qualified-event view with fixed .85 write strength; NOT inflated factual confidence or rewritten original score.',
        conclusion_boundary='Can diagnose this interface mismatch. It does not establish a qualified NSS bridge, semantic trustworthiness, or recovery of hidden intended updates.')
    write_json(output/'INTERFACE_DIAGNOSTIC.json',result);return result
