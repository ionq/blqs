import inspect

import blqs
import cirq


class CirqBlqsOp(blqs.Op):
    def __init__(self, gate):
        super().__init__(str(gate))
        self._gate = gate

    def gate(self):
        return self._gate


    def __doc__(self):


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


class Gates:
    def __init__():
        self._dispatch = {"H": cirq_blqs_op(cirq.H), "HPowGate": cirq_blqs_op(cirq.HPowGate)}

    def __getattr__(self, item):
        if item in self._dispatch:
            return self._dispatch[item]


# Single qubit gate constants.
X = cirq_blqs_op(cirq.X)
Y = cirq_blqs_op(cirq.Y)
Z = cirq_blqs_op(cirq.Z)
H = cirq_blqs_op(cirq.H)
S = cirq_blqs_op(cirq.S)
T = cirq_blqs_op(cirq.T)

# Single qubit gate classes.
XPowGate = cirq_blqs_op(cirq.XPowGate)
YPowGate = cirq_blqs_op(cirq.YPowGate)
ZPowGate = cirq_blqs_op(cirq.ZPowGate)
HPowGate = cirq_blqs_op(cirq.HPowGate)
PhasedXPowGate = cirq_blqs_op(cirq.PhasedXPowGate)

# Two qubit gate classes
CZ = cirq_blqs_op(cirq.CZ)
CNOT = CX = cirq_blqs_op(cirq.CNOT)
SWAP = cirq_blqs_op(cirq.SWAP)
ISWAP = cirq_blqs_op(cirq.ISWAP)
XX = cirq_blqs_op(cirq.XX)
YY = cirq_blqs_op(cirq.YY)
ZZ = cirq_blqs_op(cirq.ZZ)

