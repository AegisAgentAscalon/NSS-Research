"""Shared directed-replay observations for the two installed numerical families."""
from pathlib import Path
from tempfile import TemporaryDirectory
from .neural_contracts import pairs
from .runtime import ContractError, fail


def replay_observations(session_type, artifacts, binding, scope, *, atol, rtol):
    import torch
    from .neural_backend import deterministic_cpu
    from .ledger import Ledger
    from .neural_execution import NeuralSession, CandidateSession
    if session_type not in (NeuralSession, CandidateSession):
        fail('VALIDATION_FAILED','No caller-defined numerical executors')
    with TemporaryDirectory(prefix='megamind-qual-check-') as d, deterministic_cpu(binding['trial_seed']):
        ledger=Ledger(Path(d)/'actions');task='qualification-replay'
        ledger.perform({'schema_version':1,'key':'qualification:mock','task_id':task,
            'payload':{'operation':'append_marker','value':'isolated checker fixture'},'status':'PENDING','receipt':None})
        s=session_type(artifacts,binding['runtime_sha256'])
        source=s.state(scope['source'],pairs('test')[:4],task);cache=source['cache'].clone()
        try:s.accept(source,scope['destination'],task)
        except ContractError as exc:stale=exc.code=='INCOMPATIBLE_CONFIGURATION'
        else:stale=False
        recovered=s.recover(source,scope['destination'],task,ledger,authorized=True)
        if recovered['status']!='SUCCESS':fail(recovered['status'],'Qualification replay failed')
        clean=session_type(artifacts,binding['runtime_sha256']).predict(scope['destination'],pairs('test')[:4])
        denied=s.recover(source,scope['destination'],task,ledger,authorized=False)
        reverse=s.recover(recovered['state'],scope['source'],task,ledger,authorized=True)
        return {'stale_rejected':stale,'source_unchanged':torch.equal(source['cache'],cache),
            'exact_match':torch.equal(recovered['state']['cache'],clean),
            'tolerance_match':torch.allclose(recovered['state']['cache'],clean,atol=atol,rtol=rtol),
            'maximum_error':float((recovered['state']['cache']-clean).abs().max()),
            'draft_cleared':recovered['state']['draft']=='','denial_preserved':denied['status']=='AUTHORIZATION_DENIED',
            'reverse_rejected':reverse['status']=='INCOMPATIBLE_CONFIGURATION','checker_mock_effect_count':ledger.effect_count()}
