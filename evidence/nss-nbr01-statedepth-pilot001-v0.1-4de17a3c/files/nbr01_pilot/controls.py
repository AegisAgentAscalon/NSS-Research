"""Independently implemented explicit-state control. Not a trained model."""
from dataclasses import dataclass

@dataclass
class ExactState:
    value: int = 8
    count: int = 0
    def observe(self, token: int):
        if type(token) is not int or not 0 <= token <= 15:
            raise ValueError('Invalid event')
        if token <= 7:
            self.value = token
        self.count += 1
    def query(self, keep: bool = True):
        return self.value if keep else 8
