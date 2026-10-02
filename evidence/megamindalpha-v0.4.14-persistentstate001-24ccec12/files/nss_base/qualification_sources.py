"""Closed evidence adapter selection; no plugins, callbacks or dynamic imports."""
from .qualification_neural import NeuralEvidence
from .qualification_candidate import CandidateEvidence
from .runtime import fail


def require_source(value):
    if type(value) not in (NeuralEvidence, CandidateEvidence):
        fail('VALIDATION_FAILED', 'Only installed exact probe/candidate source adapters are supported')
    return value


def add_source_arguments(parser):
    parser.add_argument('--journal', help='Existing legacy probe journal; use with --data')
    parser.add_argument('--data', help='Existing legacy probe data owner')
    parser.add_argument('--candidate-config', help='Existing learner-owner config for new candidate evidence')


def source_from_args(args, *, optional=False):
    from .neural_contracts import read_document
    from .qualification_candidate import from_config
    journal=getattr(args,'journal',None);data=getattr(args,'data',None)
    config=getattr(args,'candidate_config',None)
    if config:
        if journal or data:fail('VALIDATION_FAILED','Select candidate config OR legacy journal/data, not both')
        return from_config(read_document(config))
    if journal and data:return NeuralEvidence(journal,data)
    if optional and not journal and not data:return None
    fail('VALIDATION_FAILED','Specify --candidate-config or both --journal and --data')
