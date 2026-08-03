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

from blqs_cirq import contrib
from blqs_cirq.build import (
    BuildConfig,
    build,
    build_with_config,
)
from blqs_cirq.cirq_blqs_op import (
    CirqBlqsOp,
    CirqBlqsOpFactory,
    create_cirq_blqs_op,
)
from blqs_cirq.gates import (
    CCNOT,
    CCX,
    CCZ,
    CNOT,
    CSWAP,
    CX,
    CZ,
    FREDKIN,
    ISWAP,
    SWAP,
    TOFFOLI,
    XX,
    YY,
    ZZ,
    AmplitudeDampingChannel,
    AsymmetricDepolarizingChannel,
    BitFlipChannel,
    BooleanHamiltonianGate,
    CCXPowGate,
    CCZPowGate,
    CliffordGate,
    ControlledGate,
    CSwapGate,
    CXPowGate,
    CZPowGate,
    DensePauliString,
    DepolarizingChannel,
    DiagonalGate,
    FSimGate,
    GeneralizedAmplitudeDampingChannel,
    GlobalPhaseGate,
    H,
    HPowGate,
    IdentityGate,
    ISwapPowGate,
    KrausChannel,
    MatrixGate,
    MeasurementGate,
    MixedUnitaryChannel,
    MSGate,
    MutableDensePauliString,
    ParallelGate,
    PauliInteractionGate,
    PauliMeasurementGate,
    PauliStringPhasorGate,
    PhaseDampingChannel,
    PhasedFSimGate,
    PhasedISwapPowGate,
    PhasedXPowGate,
    PhasedXZGate,
    PhaseFlipChannel,
    PhaseGradientGate,
    QuantumFourierTransformGate,
    QubitPermutationGate,
    RandomGateChannel,
    ResetChannel,
    Rx,
    Ry,
    Rz,
    S,
    SingleQubitCliffordGate,
    StatePreparationChannel,
    SwapPowGate,
    T,
    ThreeQubitDiagonalGate,
    TwoQubitDiagonalGate,
    UniformSuperpositionGate,
    WaitGate,
    X,
    XPowGate,
    XXPowGate,
    Y,
    YPowGate,
    YYPowGate,
    Z,
    ZPowGate,
    ZZPowGate,
    amplitude_damp,
    asymmetric_depolarize,
    bit_flip,
    depolarize,
    generalized_amplitude_damp,
    measure,
    ms,
    phase_damp,
    phase_flip,
    qft,
    reset,
    rx,
    ry,
    rz,
    wait,
)
from blqs_cirq.insert_strategy import (
    InsertStrategy,
)
from blqs_cirq.moment import (
    Moment,
)
from blqs_cirq.protocols import (
    NotImplementedType,
    SupportsDecoding,
    decode,
)
from blqs_cirq.qubits import (
    DEFAULT_QUBIT_DECODER,
    DefaultQubitDecoder,
)
from blqs_cirq.repeat import (
    CircuitOperation,
    Repeat,
)
