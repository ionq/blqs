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
import pymore

import blqs_cirq as bc


def test_cirq_blqs_op_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOp(cirq.H))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X, op_name="x"))


def test_cirq_blqs_op_fields():
    op = bc.CirqBlqsOp(cirq.X)
    assert op.gate() == cirq.X
    assert op.name() == "X"
    op = bc.CirqBlqsOp(cirq.X, op_name="x")
    assert op.name() == "x"


def test_cirq_blqs_op_str():
    assert str(bc.CirqBlqsOp(cirq.X)) == str(cirq.X)
    assert str(bc.CirqBlqsOp(cirq.XPowGate(exponent=0.5))) == str(cirq.XPowGate(exponent=0.5))


def test_cirq_blqs_op_factory_eq():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOpFactory(cirq.HPowGate))
    equals_tester.add_equality_group(bc.CirqBlqsOpFactory(cirq.XPowGate))
    equals_tester.add_equality_group(bc.CirqBlqsOpFactory(cirq.bit_flip))


def test_cirq_blqs_op_factory_fields():
    assert bc.CirqBlqsOpFactory(cirq.HPowGate).cirq_gate_factory() == cirq.HPowGate
    assert bc.CirqBlqsOpFactory(cirq.bit_flip).cirq_gate_factory() == cirq.bit_flip


def test_cirq_blqs_op_factory_is_a_factory():
    assert bc.CirqBlqsOpFactory(cirq.HPowGate)(exponent=0.5) == bc.CirqBlqsOp(
        cirq.HPowGate(exponent=0.5)
    )
    assert bc.CirqBlqsOpFactory(cirq.bit_flip)(0.5) == bc.CirqBlqsOp(cirq.BitFlipChannel(0.5))


def test_cirq_blqs_op_factory_str():
    assert str(bc.CirqBlqsOpFactory(cirq.HPowGate)) == "HPowGate"
    assert str(bc.CirqBlqsOpFactory(cirq.bit_flip)) == "bit_flip"


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
        # Contrib gates. Move to contrib.
        cirq.contrib.acquaintance.bipartite.BipartiteSwapNetworkGate,
        cirq.contrib.acquaintance.gates.AcquaintanceOpportunityGate,
        cirq.contrib.acquaintance.gates.SwapNetworkGate,
        cirq.contrib.acquaintance.permutation.MappingDisplayGate,
        cirq.contrib.acquaintance.permutation.PermutationGate,
        cirq.contrib.acquaintance.permutation.SwapPermutationGate,
        cirq.contrib.acquaintance.shift.CircularShiftGate,
        cirq.contrib.acquaintance.shift_swap_network.ShiftSwapNetworkGate,
        cirq.contrib.acquaintance.permutation.LinearPermutationGate,
        # Interop gates
        cirq.interop.quirk.cells.qubit_permutation_cells.QuirkQubitPermutationGate,
    }

    for clz in cirq_gate_subclasses:
        if clz in excluded_cirq_classes:
            continue
        assert hasattr(bc, clz.__name__)
