# Copyright 2021 The Blqs Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import functools
from typing import Dict, Optional, Tuple, Union

import cirq
import numpy as np
import sympy

import blqs
from blqs_cirq import cirq_blqs_op

# Single qubit gate constants.
H = cirq_blqs_op.create_cirq_blqs_op(cirq.H)
S = cirq_blqs_op.create_cirq_blqs_op(cirq.S)
T = cirq_blqs_op.create_cirq_blqs_op(cirq.T)
X = cirq_blqs_op.create_cirq_blqs_op(cirq.X)
Y = cirq_blqs_op.create_cirq_blqs_op(cirq.Y)
Z = cirq_blqs_op.create_cirq_blqs_op(cirq.Z)

# Single qubit gate classes.
HPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.HPowGate)
PhasedXPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PhasedXPowGate)
PhasedXZGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PhasedXZGate)
Rx = cirq_blqs_op.create_cirq_blqs_op(cirq.Rx)
Ry = cirq_blqs_op.create_cirq_blqs_op(cirq.Ry)
Rz = cirq_blqs_op.create_cirq_blqs_op(cirq.Rz)
XPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.XPowGate)
YPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.YPowGate)
ZPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ZPowGate)


# Single qubit functions
rx = cirq_blqs_op.create_cirq_blqs_op(cirq.rx)
ry = cirq_blqs_op.create_cirq_blqs_op(cirq.ry)
rz = cirq_blqs_op.create_cirq_blqs_op(cirq.rz)

# Two qubit gate constants.
CZ = cirq_blqs_op.create_cirq_blqs_op(cirq.CZ)
CNOT = CX = cirq_blqs_op.create_cirq_blqs_op(cirq.CNOT)
SWAP = cirq_blqs_op.create_cirq_blqs_op(cirq.SWAP)
ISWAP = cirq_blqs_op.create_cirq_blqs_op(cirq.ISWAP)
XX = cirq_blqs_op.create_cirq_blqs_op(cirq.XX)
YY = cirq_blqs_op.create_cirq_blqs_op(cirq.YY)
ZZ = cirq_blqs_op.create_cirq_blqs_op(cirq.ZZ)

# Two qubit gate classes.
FSimGate = cirq_blqs_op.create_cirq_blqs_op(cirq.FSimGate)
CZPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.CZPowGate)
CXPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.CXPowGate)
XXPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.XXPowGate)
YYPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.YYPowGate)
ZZPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ZZPowGate)
PhasedFSimGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PhasedFSimGate)
PhasedISwapPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PhasedISwapPowGate)
ISwapPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ISwapPowGate)
SwapPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.SwapPowGate)
TwoQubitDiagonalGate = cirq_blqs_op.create_cirq_blqs_op(cirq.TwoQubitDiagonalGate)

# Two qubit gate functions.
ms = cirq_blqs_op.create_cirq_blqs_op(cirq.ms)

# Three qubit gate constants.
CCX = CCNOT = TOFFOLI = cirq_blqs_op.create_cirq_blqs_op(cirq.CCX)
CCZ = cirq_blqs_op.create_cirq_blqs_op(cirq.CCZ)
CSWAP = FREDKIN = cirq_blqs_op.create_cirq_blqs_op(cirq.CSWAP)

# Three qubit gate classes.
CCXPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.CCXPowGate)
CCZPowGate = cirq_blqs_op.create_cirq_blqs_op(cirq.CCZPowGate)
CSwapGate = cirq_blqs_op.create_cirq_blqs_op(cirq.CSwapGate)
ThreeQubitDiagonalGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ThreeQubitDiagonalGate)

# N qubit gate classes.
DiagonalGate = cirq_blqs_op.create_cirq_blqs_op(cirq.DiagonalGate)
DensePauliString = cirq_blqs_op.create_cirq_blqs_op(cirq.DensePauliString)
IdentityGate = cirq_blqs_op.create_cirq_blqs_op(cirq.IdentityGate)
MeasurementGate = cirq_blqs_op.create_cirq_blqs_op(cirq.MeasurementGate)
MatrixGate = cirq_blqs_op.create_cirq_blqs_op(cirq.MatrixGate)
MutableDensePauliString = cirq_blqs_op.create_cirq_blqs_op(cirq.MutableDensePauliString)
QubitPermutationGate = cirq_blqs_op.create_cirq_blqs_op(cirq.QubitPermutationGate)
QuantumFourierTransformGate = cirq_blqs_op.create_cirq_blqs_op(cirq.QuantumFourierTransformGate)
ParallelGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ParallelGate)
PhaseGradientGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PhaseGradientGate)
WaitGate = cirq_blqs_op.create_cirq_blqs_op(cirq.WaitGate)
ControlledGate = cirq_blqs_op.create_cirq_blqs_op(cirq.ControlledGate)

# N qubit gate functions.
def measure(*targets, key=None, invert_mask=()) -> blqs.Instruction:
    measurement_fn = functools.partial(cirq.measure, key=key, invert_mask=invert_mask)
    return cirq_blqs_op.CirqBlqsOp(measurement_fn, "measure")(*targets)


def qft(*qubits, without_reverse=False, inverse=False) -> blqs.Instruction:
    qft_fn = functools.partial(cirq.qft, without_reverse=without_reverse, inverse=inverse)
    return cirq_blqs_op.CirqBlqsOp(qft_fn, "qft")(*qubits)


def wait(
    *targets,
    duration: cirq.DURATION_LIKE = None,
    picos: Union[int, float, sympy.Basic] = 0,
    nanos: Union[int, float, sympy.Basic] = 0,
    micros: Union[int, float, sympy.Basic] = 0,
    millis: Union[int, float, sympy.Basic] = 0,
):
    wait_fn = functools.partial(
        cirq.wait,
        duration=duration,
        picos=picos,
        nanos=nanos,
        micros=micros,
        millis=millis,
    )
    return cirq_blqs_op.CirqBlqsOp(wait_fn, "wait")(*targets)


# Noise classes.
AmplitudeDampingChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.AmplitudeDampingChannel)
AsymmetricDepolarizingChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.AsymmetricDepolarizingChannel)
BitFlipChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.BitFlipChannel)
DepolarizingChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.DepolarizingChannel)
GeneralizedAmplitudeDampingChannel = cirq_blqs_op.create_cirq_blqs_op(
    cirq.GeneralizedAmplitudeDampingChannel
)
KrausChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.KrausChannel)
MixedUnitaryChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.MixedUnitaryChannel)
PauliMeasurementGate = cirq_blqs_op.create_cirq_blqs_op(cirq.PauliMeasurementGate)
PhaseDampingChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.PhaseDampingChannel)
PhaseFlipChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.PhaseFlipChannel)
ResetChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.ResetChannel)
RandomGateChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.RandomGateChannel)
StatePreparationChannel = cirq_blqs_op.create_cirq_blqs_op(cirq.StatePreparationChannel)

# Noise functions.
asymmetric_depolarize = cirq_blqs_op.create_cirq_blqs_op(cirq.asymmetric_depolarize)
depolarize = cirq_blqs_op.create_cirq_blqs_op(cirq.depolarize)
generalized_amplitude_damp = cirq_blqs_op.create_cirq_blqs_op(cirq.generalized_amplitude_damp)
amplitude_damp = cirq_blqs_op.create_cirq_blqs_op(cirq.amplitude_damp)
phase_damp = cirq_blqs_op.create_cirq_blqs_op(cirq.phase_damp)
phase_flip = cirq_blqs_op.create_cirq_blqs_op(cirq.phase_flip)
bit_flip = cirq_blqs_op.create_cirq_blqs_op(cirq.bit_flip)


# Special functions.
def reset(qubit) -> blqs.Instruction:
    return cirq_blqs_op.CirqBlqsOp(cirq.ResetChannel(getattr(qubit, "dimension", 2)))(qubit)


# Special single qubit gate classes
class SingleQubitCliffordGate(cirq_blqs_op.CirqBlqsOp):

    I = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.I)
    H = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.H)
    X = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.X)
    Y = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Y)
    Z = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Z)
    X_sqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.X_sqrt)
    Y_sqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Y_sqrt)
    Z_sqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Z_sqrt)
    X_nsqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.X_nsqrt)
    Y_nsqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Y_nsqrt)
    Z_nsqrt = cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.Z_nsqrt)

    @staticmethod
    def from_xz_map(
        x_to: Tuple[cirq.Pauli, bool], z_to: Tuple[cirq.Pauli, bool]
    ) -> cirq_blqs_op.CirqBlqsOp:
        return cirq_blqs_op.CirqBlqsOp(cirq.SingleQubitCliffordGate.from_xz_map(x_to, z_to))

    @staticmethod
    def from_single_map(
        pauli_map_to: Optional[Dict[cirq.Pauli, Tuple[cirq.Pauli, bool]]] = None,
        *,
        x_to: Optional[Tuple[cirq.Pauli, bool]] = None,
        y_to: Optional[Tuple[cirq.Pauli, bool]] = None,
        z_to: Optional[Tuple[cirq.Pauli, bool]] = None,
    ) -> cirq_blqs_op.CirqBlqsOp:
        return cirq_blqs_op.CirqBlqsOp(
            cirq.SingleQubitCliffordGate.from_single_map(
                pauli_map_to=pauli_map_to, x_to=x_to, y_to=y_to, z_to=z_to
            )
        )

    @staticmethod
    def from_double_map(
        pauli_map_to: Optional[Dict[cirq.Pauli, Tuple[cirq.Pauli, bool]]] = None,
        *,
        x_to: Optional[Tuple[cirq.Pauli, bool]] = None,
        y_to: Optional[Tuple[cirq.Pauli, bool]] = None,
        z_to: Optional[Tuple[cirq.Pauli, bool]] = None,
    ) -> cirq_blqs_op.CirqBlqsOp:
        return cirq_blqs_op.CirqBlqsOp(
            cirq.SingleQubitCliffordGate.from_double_map(
                pauli_map_to=pauli_map_to, x_to=x_to, y_to=y_to, z_to=z_to
            )
        )

    @staticmethod
    def from_pauli(pauli: cirq.Pauli, sqrt: bool = False) -> cirq_blqs_op.CirqBlqsOp:
        return cirq_blqs_op.CirqBlqsOp(
            cirq.SingleQubitCliffordGate.from_pauli(pauli=pauli, sqrt=sqrt)
        )

    @staticmethod
    def from_quarter_turns(pauli: cirq.Pauli, quarter_turns: int) -> cirq_blqs_op.CirqBlqsOp:
        return cirq_blqs_op.CirqBlqsOp(
            cirq.SingleQubitCliffordGate.from_quarter_turns(
                pauli=pauli, quarter_turns=quarter_turns
            )
        )

    @staticmethod
    def from_unitary(u: np.ndarray) -> Optional[cirq_blqs_op.CirqBlqsOp]:
        gate = cirq.SingleQubitCliffordGate.from_unitary(u=u)
        return cirq_blqs_op.CirqBlqsOp(gate) if gate is not None else None


# Special two qubit gate classes


class PauliInteractionGate(cirq_blqs_op.CirqBlqsOp):
    def __init__(self, *args, **kwargs):

        super().__init__(gate=cirq.PauliInteractionGate(*args, **kwargs))

    CZ = cirq_blqs_op.CirqBlqsOp(cirq.PauliInteractionGate.CZ)
    CNOT = cirq_blqs_op.CirqBlqsOp(cirq.PauliInteractionGate.CNOT)
