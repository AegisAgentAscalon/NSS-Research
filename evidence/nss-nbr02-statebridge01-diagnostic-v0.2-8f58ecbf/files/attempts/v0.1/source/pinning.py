"""Small supplied version/state registry. Not a trained management-token interface."""
import hashlib
import numpy as np
class PinnedStates:
    def __init__(self,version,states,prefix_hash):
        if not isinstance(version,str) or len(version)!=64:raise ValueError('INVALID_VERSION')
        self.version=version;self.prefix_hash=prefix_hash;self.states=np.asarray(states,np.float32).copy()
        self.states.setflags(write=False);self.digest=hashlib.sha256(self.states.tobytes()).hexdigest()
    def read(self,requested_version):
        if requested_version!=self.version:raise ValueError('STATE_WEIGHT_VERSION_MISMATCH')
        if hashlib.sha256(self.states.tobytes()).hexdigest()!=self.digest:raise ValueError('STATE_MUTATED')
        return self.states.copy()
