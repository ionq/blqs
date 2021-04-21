import inspect

import blqs
import cirq


class CirqBlqsOp(blqs.Op):
    def __init__(self, gate):
        super().__init__(str(gate))
        self._gate = gate

    def gate(self):
        return self._gate


class CirqBlqsOpFactory:
    def __init__(self, cirq_gate_class):
        self._cirq_gate_class = cirq_gate_class

    def __call__(self, *args, **kwargs):
        return CirqBlqsOp(self._cirq_gate_class(*args, **kwargs))


def cirq_blqs_op(cirq_gate):
    if inspect.isclass(cirq_gate):
        return CirqBlqsOpFactory(cirq_gate)
    else:
        return CirqBlqsOp(cirq_gate)


H = cirq_blqs_op(cirq.H)
HPowGate = cirq_blqs_op(cirq.HPowGate)
