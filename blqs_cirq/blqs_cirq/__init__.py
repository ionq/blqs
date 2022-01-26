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

from blqs_cirq.build import (
    build,
    build_with_config,
    BuildConfig,
)


from blqs_cirq.cirq_blqs_op import (
    CirqBlqsOp,
    CirqBlqsOpFactory,
    create_cirq_blqs_op,
)

from blqs_cirq.gates import (
    AmplitudeDampingChannel,
    amplitude_damp,
    asymmetric_depolarize,
    bit_flip,
    AsymmetricDepolarizingChannel,
    BitFlipChannel,
    CCNOT,
    CCX,
    CCXPowGate,
    CCZ,
    CCZPowGate,
    CNOT,
    ControlledGate,
    CSWAP,
    CSwapGate,
    CX,
    CXPowGate,
    CZ,
    CZPowGate,
    DiagonalGate,
    DensePauliString,
    depolarize,
    DepolarizingChannel,
    FREDKIN,
    FSimGate,
    GeneralizedAmplitudeDampingChannel,
    generalized_amplitude_damp,
    H,
    HPowGate,
    ISWAP,
    ISwapPowGate,
    IdentityGate,
    KrausChannel,
    MatrixGate,
    MeasurementGate,
    measure,
    MixedUnitaryChannel,
    ms,
    MutableDensePauliString,
    ParallelGate,
    PauliInteractionGate,
    PauliMeasurementGate,
    PhaseDampingChannel,
    PhaseFlipChannel,
    PhasedFSimGate,
    PhasedISwapPowGate,
    PhasedXPowGate,
    PhasedXZGate,
    phase_damp,
    phase_flip,
    PhaseGradientGate,
    qft,
    QuantumFourierTransformGate,
    QubitPermutationGate,
    RandomGateChannel,
    reset,
    ResetChannel,
    rx,
    ry,
    rz,
    Rx,
    Ry,
    Rz,
    S,
    SWAP,
    SwapPowGate,
    SingleQubitCliffordGate,
    StatePreparationChannel,
    T,
    TOFFOLI,
    ThreeQubitDiagonalGate,
    TwoQubitDiagonalGate,
    wait,
    WaitGate,
    X,
    XPowGate,
    XX,
    XXPowGate,
    Y,
    YPowGate,
    YY,
    YYPowGate,
    Z,
    ZPowGate,
    ZZ,
    ZZPowGate,
)

from blqs_cirq.insert_strategy import (
    InsertStrategy,
)

from blqs_cirq.moment import (
    Moment,
)

from blqs_cirq.protocols import (
    decode,
    SupportsDecoding,
    NotImplementedType,
)

from blqs_cirq.qubits import (
    DefaultQubitDecoder,
    DEFAULT_QUBIT_DECODER,
)

from blqs_cirq.repeat import (
    CircuitOperation,
    Repeat,
)

from blqs_cirq import contrib
