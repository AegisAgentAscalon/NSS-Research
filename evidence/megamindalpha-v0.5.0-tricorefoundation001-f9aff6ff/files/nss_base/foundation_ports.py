"""External engine boundaries. Specifications are not a connected implementation.

Keep Forge generic and Runtime independent. No second optimizer/training engine is
created here, and a model registry is not interpreted as training capability.
"""
from abc import ABC, abstractmethod
from .runtime import fail


class ForgePort(ABC):
    @abstractmethod
    def capabilities(self):
        """Source-backed supported job kinds, state access and exact-resume behavior."""

    @abstractmethod
    def submit_approved_candidate(self, job, approval):
        """Submit to the same standalone engine used by ordinary GUI/CLI training."""


class UnconnectedForge(ForgePort):
    def capabilities(self):
        return {'status':'NOT_CONNECTED','training':False,'exact_resume':False,'source_identity':None}

    def submit_approved_candidate(self,job,approval):
        fail('NOT_SUPPORTED','Generic Forge source/adapter is not connected in this release')


class RuntimePort(ABC):
    @abstractmethod
    def capabilities(self):
        """Report actual independent execution, cancellation and resource support."""


class UnconnectedRuntime(RuntimePort):
    def capabilities(self):
        return {'status':'NOT_CONNECTED','execution_permit':False,'hard_preemption':False,
                'hardware_budget_measured':False,'source_identity':None}
