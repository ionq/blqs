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


from blqs_cirq.gates import (
    AmplitudeDampingChannel,
    AsymmetricDepolarizingChannel,
    BitFlipChannel,
    CCNOT,
    CCX,
    CCXPowGate,
    CCZ,
    CCZPowGate,
    CNOT,
    CSWAP,
    CSwapGate,
    CX,
    CXPowGate,
    CZ,
    CZPowGate,
    CirqBlqsOp,
    CirqBlqsOpFactory,
    FREDKIN,
    FSimGate,
    GeneralizedAmplitudeDampingChannel,
    H,
    HPowGate,
    ISWAP,
    IdentityGate,
    MSGate,
    MatrixGate,
    MeasurementGate,
    measure,
    PauliInteractionGate,
    PhaseDampingChannel,
    PhaseFlipChannel,
    PhasedFSimGate,
    PhasedISwapPowGate,
    PhasedXPowGate,
    QasmTwoQubitGate,
    QasmUGate,
    qft,
    QubitPermutationGate,
    QuilOneQubitGate,
    QuilTwoQubitGate,
    reset,
    ResetChannel,
    rx,
    SWAP,
    SingleQubitCliffordGate,
    TOFOLLI,
    ThreeQubitDiagonalGate,
    X,
    XPowGate,
    XX,
    Y,
    YPowGate,
    YY,
    Z,
    ZPowGate,
    ZZ,
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
