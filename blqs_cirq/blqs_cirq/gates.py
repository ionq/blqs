import functools
import inspect

import blqs
import cirq

from typing import Callable, Type, Union


GateLikeType = Union[cirq.Gate, Callable[[], cirq.Gate], functools.partial]


class CirqBlqsOp(blqs.Op):
    """A `blqs.Op` corresponding to a `cirq.Gate`."""

    def __init__(self, gate: GateLikeType, op_name: str = None):
        """Construct a CirqBlqsOp.

        Args:
            gate: The gate for this op. Alternatively a method that can be called to produce a gate.
            op_name: If specified the op name, otherwise the op name will be `str(gate)`.
        """
        super().__init__(op_name or str(gate))
        self._gate = gate

    def gate(self) -> GateLikeType:
        """The `cirq.Gate` or a callable which produces this gate for this op."""
        return self._gate


class CirqBlqsOpFactory:
    """A wrapper for Cirq gate classes or methods with params that when called give a `cirq.Gate`.

    Example, supposing that `MyGateClass` is a `cirq.Gate` subclass and it uses the standard
    `__init__` with two args and two keywork args:
        ```
        factory = CirqBlqsOpFactory(MyGateClass)
        cirq_blqs_op = factory(arg1, arg2, kw1=val1, kw2=val2)
        ```
    """

    def __init__(self, cirq_gate_class: Callable[..., cirq.Gate]):
        self._cirq_gate_class = cirq_gate_class

    def __call__(self, *args, **kwargs) -> CirqBlqsOp:
        gate = self._cirq_gate_class(*args, **kwargs)
        return CirqBlqsOp(gate)


def cirq_blqs_op(
    cirq_construct: Union[cirq.Gate, Type[cirq.Gate], Callable[..., cirq.Gate]]
) -> Union[CirqBlqsOp, CirqBlqsOpFactory, Callable[..., CirqBlqsOp]]:
    """Construct a blqs object for the relevant cirq gate, class, or method.

    Note that this will not work for methods that require qubit targets and parameters to construct
    a `cirq.Operation`.  See `measure` for an example of how to handle this case.
    """
    if inspect.isclass(cirq_construct):
        return CirqBlqsOpFactory(cirq_construct)
    elif inspect.isfunction(cirq_construct):

        def wrapped(*args, **kwargs):
            return CirqBlqsOp(cirq_construct(*args, **kwargs))

        return wrapped
    else:
        return CirqBlqsOp(cirq_construct)


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
Rx = cirq_blqs_op(cirq.Rx)
Ry = cirq_blqs_op(cirq.Ry)
Rz = cirq_blqs_op(cirq.Rz)
HPowGate = cirq_blqs_op(cirq.HPowGate)
PhasedXPowGate = cirq_blqs_op(cirq.PhasedXPowGate)
QasmUGate = cirq_blqs_op(cirq.circuits.qasm_output.QasmUGate)
QuilOneQubitGate = cirq_blqs_op(cirq.circuits.quil_output.QuilOneQubitGate)
FSimGate = cirq_blqs_op(cirq.FSimGate)
PhasedFSimGate = cirq_blqs_op(cirq.PhasedFSimGate)
SingleQubitCliffordGate = cirq_blqs_op(cirq.SingleQubitCliffordGate)
WaitGate = cirq_blqs_op(cirq.WaitGate)

# Single qubit functions
rx = cirq_blqs_op(cirq.rx)
ry = cirq_blqs_op(cirq.ry)
rz = cirq_blqs_op(cirq.rz)

# Two qubit gate constants.
CZ = cirq_blqs_op(cirq.CZ)
CNOT = CX = cirq_blqs_op(cirq.CNOT)
SWAP = cirq_blqs_op(cirq.SWAP)
ISWAP = cirq_blqs_op(cirq.ISWAP)
XX = cirq_blqs_op(cirq.XX)
YY = cirq_blqs_op(cirq.YY)
ZZ = cirq_blqs_op(cirq.ZZ)

# Two qubit gate classes.
CZPowGate = cirq_blqs_op(cirq.CZPowGate)
CXPowGate = cirq_blqs_op(cirq.CXPowGate)
XXPowGate = cirq_blqs_op(cirq.XXPowGate)
YYPowGate = cirq_blqs_op(cirq.YYPowGate)
ZZPowGate = cirq_blqs_op(cirq.ZZPowGate)
QasmTwoQubitGate = cirq_blqs_op(cirq.circuits.qasm_output.QasmTwoQubitGate)
QuilTwoQubitGate = cirq_blqs_op(cirq.circuits.quil_output.QuilTwoQubitGate)
MSGate = cirq_blqs_op(cirq.ion.ion_gates.MSGate)
PauliInteractionGate = cirq_blqs_op(cirq.PauliInteractionGate)
PhasedISwapPowGate = cirq_blqs_op(cirq.PhasedISwapPowGate)
ISwapPowGate = cirq_blqs_op(cirq.ISwapPowGate)
SwapPowGate = cirq_blqs_op(cirq.SwapPowGate)
TwoQubitDiagonalGate = cirq_blqs_op(cirq.TwoQubitDiagonalGate)

# Three qubit gate constants.
CCX = cirq_blqs_op(cirq.CCX)
CCZ = TOFOLLI = CCNOT = cirq_blqs_op(cirq.CCZ)
CSWAP = FREDKIN = cirq_blqs_op(cirq.CSWAP)

# Three qubit gate classes.
CCXPowGate = cirq_blqs_op(cirq.CCXPowGate)
CCZPowGate = cirq_blqs_op(cirq.CCZPowGate)
CSwapGate = cirq_blqs_op(cirq.CSwapGate)
ThreeQubitDiagonalGate = cirq_blqs_op(cirq.ThreeQubitDiagonalGate)

# N qubit gate classes.
IdentityGate = cirq_blqs_op(cirq.IdentityGate)
MeasurementGate = cirq_blqs_op(cirq.MeasurementGate)
MatrixGate = cirq_blqs_op(cirq.MatrixGate)
QubitPermutationGate = cirq_blqs_op(cirq.QubitPermutationGate)
QuantumFourierTransformGate = cirq_blqs_op(cirq.QuantumFourierTransformGate)
PhaseGradientGate = cirq_blqs_op(cirq.PhaseGradientGate)


# Noise classes
AmplitudeDampingChannel = cirq_blqs_op(cirq.AmplitudeDampingChannel)
AsymmetricDepolarizingChannel = cirq_blqs_op(cirq.AsymmetricDepolarizingChannel)
BitFlipChannel = cirq_blqs_op(cirq.BitFlipChannel)
DepolarizingChannel = cirq_blqs_op(cirq.DepolarizingChannel)
GeneralizedAmplitudeDampingChannel = cirq_blqs_op(cirq.GeneralizedAmplitudeDampingChannel)
PhaseDampingChannel = cirq_blqs_op(cirq.PhaseDampingChannel)
PhaseFlipChannel = cirq_blqs_op(cirq.PhaseFlipChannel)
ResetChannel = cirq_blqs_op(cirq.ResetChannel)
RandomGateChannel = cirq_blqs_op(cirq.RandomGateChannel)

# Noise functions
asymmetric_depolarize = cirq_blqs_op(cirq.asymmetric_depolarize)
depolarize = cirq_blqs_op(cirq.depolarize)
generalized_amplitude_damp = cirq_blqs_op(cirq.generalized_amplitude_damp)
amplitude_damp = cirq_blqs_op(cirq.amplitude_damp)
phase_damp = cirq_blqs_op(cirq.phase_damp)
phase_flip = cirq_blqs_op(cirq.phase_flip)
bit_flip = cirq_blqs_op(cirq.bit_flip)

# N qubit gate functions.
def measure(*targets, key=None, invert_mask=()) -> blqs.Instruction:
    measurement_fn = functools.partial(cirq.measure, key=key, invert_mask=invert_mask)
    return CirqBlqsOp(measurement_fn, "measure")(*targets)


def qft(*qubits, without_reverse=False, inverse=False) -> blqs.Instruction:
    qft_fn = functools.partial(cirq.qft, without_reverse=without_reverse, inverse=inverse)
    return CirqBlqsOp(qft_fn, "qft")(*qubits)


# Special functions
def reset(qubit) -> blqs.Instruction:
    return CirqBlqsOp(cirq.ResetChannel(getattr(qubit, "dimension", 2)))(qubit)
