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
import cirq
import cirq_google

import blqs_cirq as bc


def test_all_gate_subclasses():
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    cirq_gate_subclasses = all_subclasses(cirq.Gate)

    excluded_cirq_classes = {
        # Private Pauli gates. Don't ask.
        cirq.ops.pauli_gates._PauliX,
        cirq.ops.pauli_gates._PauliY,
        cirq.ops.pauli_gates._PauliZ,
        # Private parent gates.
        cirq.ops.dense_pauli_string.BaseDensePauliString,
        cirq.ops.eigen_gate.EigenGate,
        cirq.ops.pauli_gates.Pauli,
        # Private gates.
        cirq.optimizers.two_qubit_to_fsim._BGate,
        cirq.ops.raw_types._InverseCompositeGate,
        # Gate features
        cirq.ops.gate_features.SingleQubitGate,
        cirq.ops.gate_features.SupportsOnEachGate,
        cirq.ops.gate_features.TwoQubitGate,
        cirq.ops.gate_features.ThreeQubitGate,
        # Interop gates
        cirq.interop.quirk.cells.qubit_permutation_cells.QuirkQubitPermutationGate,
        # Contrib gates.
        # When cirq.contrib is removed these should be removed.
        cirq.contrib.acquaintance.bipartite.BipartiteSwapNetworkGate,
        cirq.contrib.acquaintance.gates.AcquaintanceOpportunityGate,
        cirq.contrib.acquaintance.gates.SwapNetworkGate,
        cirq.contrib.acquaintance.permutation.MappingDisplayGate,
        cirq.contrib.acquaintance.permutation.PermutationGate,
        cirq.contrib.acquaintance.permutation.SwapPermutationGate,
        cirq.contrib.acquaintance.shift.CircularShiftGate,
        cirq.contrib.acquaintance.shift_swap_network.ShiftSwapNetworkGate,
        cirq.contrib.acquaintance.permutation.LinearPermutationGate,
        # Google gates
        # When cirq.google is remove these should be removed.
        cirq_google.ops.sycamore_gate.SycamoreGate,
    }

    for clz in cirq_gate_subclasses:
        if clz in excluded_cirq_classes:
            continue
        assert hasattr(bc, clz.__name__)
