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
        cirq.circuits.qasm_output.QasmUGate,
        cirq.circuits.qasm_output.QasmTwoQubitGate,
        cirq.circuits.quil_output.QuilOneQubitGate,
        cirq.circuits.quil_output.QuilTwoQubitGate,
        cirq.ion.ion_gates.MSGate,
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


def test_single_qubit_gate_constants():
    def single_qubit_gate_constants():
        bc.H(0)
        bc.S(0)
        bc.T(0)
        bc.X(0)
        bc.Y(0)
        bc.Z(0)

    q0 = cirq.LineQubit(0)
    assert bc.build(single_qubit_gate_constants)() == cirq.Circuit(
        [cirq.H(q0), cirq.S(q0), cirq.T(q0), cirq.X(q0), cirq.Y(q0), cirq.Z(q0)]
    )


def test_single_qubit_gate_classes():
    def single_qubit_gate_classes():
        bc.HPowGate(exponent=0.5)(0)
        bc.PhasedXPowGate(exponent=0.5, phase_exponent=0.25)(0)
        bc.PhasedXZGate(x_exponent=0.5, z_exponent=0.25, axis_phase_exponent=0.125)(0)
        bc.Rx(rads=0.5)(0)
        bc.Ry(rads=0.5)(0)
        bc.Rz(rads=0.5)(0)
        bc.XPowGate(exponent=0.5)(0)
        bc.YPowGate(exponent=0.5)(0)
        bc.ZPowGate(exponent=0.5)(0)

    q0 = cirq.LineQubit(0)
    assert bc.build(single_qubit_gate_classes)() == cirq.Circuit(
        [
            cirq.HPowGate(exponent=0.5)(q0),
            cirq.PhasedXPowGate(exponent=0.5, phase_exponent=0.25)(q0),
            cirq.PhasedXZGate(x_exponent=0.5, z_exponent=0.25, axis_phase_exponent=0.125)(q0),
            cirq.Rx(rads=0.5)(q0),
            cirq.Ry(rads=0.5)(q0),
            cirq.Rz(rads=0.5)(q0),
            cirq.XPowGate(exponent=0.5)(q0),
            cirq.YPowGate(exponent=0.5)(q0),
            cirq.ZPowGate(exponent=0.5)(q0),
        ]
    )


def test_single_qubit_gate_functions():
    def single_qubit_gate_functions():
        bc.rx(rads=0.5)(0)
        bc.ry(rads=0.5)(0)
        bc.rz(rads=0.5)(0)

    q0 = cirq.LineQubit(0)
    assert bc.build(single_qubit_gate_functions)() == cirq.Circuit(
        [
            cirq.Rx(rads=0.5)(q0),
            cirq.Ry(rads=0.5)(q0),
            cirq.Rz(rads=0.5)(q0),
        ]
    )


def test_two_qubit_gate_constants():
    def two_qubit_gate_constants():
        bc.CZ(0, 1)
        bc.CNOT(0, 1)
        bc.CX(0, 1)
        bc.SWAP(0, 1)
        bc.ISWAP(0, 1)
        bc.XX(0, 1)
        bc.YY(0, 1)
        bc.ZZ(0, 1)

    q0, q1 = cirq.LineQubit.range(2)
    assert bc.build(two_qubit_gate_constants)() == cirq.Circuit(
        [
            cirq.CZ(q0, q1),
            cirq.CNOT(q0, q1),
            cirq.CX(q0, q1),
            cirq.SWAP(q0, q1),
            cirq.ISWAP(q0, q1),
            cirq.XX(q0, q1),
            cirq.YY(q0, q1),
            cirq.ZZ(q0, q1),
        ]
    )


def test_two_qubit_gate_classes():
    def two_qubit_gate_classes():
        bc.FSimGate(theta=0.5, phi=0.2)(0, 1)
        bc.CZPowGate(exponent=0.5)(0, 1)
        bc.CXPowGate(exponent=0.5)(0, 1)
        bc.XXPowGate(exponent=0.5)(0, 1)
        bc.YYPowGate(exponent=0.5)(0, 1)
        bc.ZZPowGate(exponent=0.5)(0, 1)
        bc.PhasedFSimGate(theta=0.5, zeta=0.25, chi=0.25, gamma=0.25, phi=0.125)(0, 1)
        bc.PauliInteractionGate(cirq.X, False, cirq.X, False, exponent=0.5)(0, 1)
        bc.PhasedISwapPowGate(phase_exponent=0.5, exponent=0.25)(0, 1)
        bc.ISwapPowGate(exponent=0.5)(0, 1)
        bc.SwapPowGate(exponent=0.5)(0, 1)
        bc.TwoQubitDiagonalGate([0.5, 0.25, 0.5, 0.125])(0, 1)

    q0, q1 = cirq.LineQubit.range(2)
    assert bc.build(two_qubit_gate_classes)() == cirq.Circuit(
        [
            cirq.FSimGate(theta=0.5, phi=0.2)(q0, q1),
            cirq.CZPowGate(exponent=0.5)(q0, q1),
            cirq.CXPowGate(exponent=0.5)(q0, q1),
            cirq.XXPowGate(exponent=0.5)(q0, q1),
            cirq.YYPowGate(exponent=0.5)(q0, q1),
            cirq.ZZPowGate(exponent=0.5)(q0, q1),
            cirq.PhasedFSimGate(theta=0.5, zeta=0.25, chi=0.25, gamma=0.25, phi=0.125)(q0, q1),
            cirq.PauliInteractionGate(cirq.X, False, cirq.X, False, exponent=0.5)(q0, q1),
            cirq.PhasedISwapPowGate(phase_exponent=0.5, exponent=0.25)(q0, q1),
            cirq.ISwapPowGate(exponent=0.5)(q0, q1),
            cirq.SwapPowGate(exponent=0.5)(q0, q1),
            cirq.TwoQubitDiagonalGate([0.5, 0.25, 0.5, 0.125])(q0, q1),
        ]
    )


def test_two_qubit_gate_functions():
    def two_qubit_gate_functions():
        bc.ms(rads=0.5)(0, 1)

    q0, q1 = cirq.LineQubit.range(2)
    assert bc.build(two_qubit_gate_functions)() == cirq.Circuit(
        [
            cirq.ms(rads=0.5)(q0, q1),
        ]
    )


def test_three_qubit_gate_constants():
    def three_qubit_gate_constants():
        bc.CCX(0, 1, 2)
        bc.TOFFOLI(0, 1, 2)
        bc.CCNOT(0, 1, 2)
        bc.CCZ(0, 1, 2)
        bc.CSWAP(0, 1, 2)
        bc.FREDKIN(0, 1, 2)

    q0, q1, q2 = cirq.LineQubit.range(3)
    assert bc.build(three_qubit_gate_constants)() == cirq.Circuit(
        [
            cirq.CCX(q0, q1, q2),
            cirq.TOFFOLI(q0, q1, q2),
            cirq.CCNOT(q0, q1, q2),
            cirq.CCZ(q0, q1, q2),
            cirq.CSWAP(q0, q1, q2),
            cirq.FREDKIN(q0, q1, q2),
        ]
    )


def test_three_qubit_gate_classes():
    def three_qubit_gate_classes():
        bc.CCXPowGate(exponent=0.5)(0, 1, 2)
        bc.CCZPowGate(exponent=0.5)(0, 1, 2)
        bc.CSwapGate()(0, 1, 2)
        bc.ThreeQubitDiagonalGate([0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.5])(0, 1, 2)

    q0, q1, q2 = cirq.LineQubit.range(3)
    assert bc.build(three_qubit_gate_classes)() == cirq.Circuit(
        [
            cirq.CCXPowGate(exponent=0.5)(q0, q1, q2),
            cirq.CCZPowGate(exponent=0.5)(q0, q1, q2),
            cirq.CSwapGate()(q0, q1, q2),
            cirq.ThreeQubitDiagonalGate([0.5, 0.25, 0.5, 0.25, 0.5, 0.25, 0.25, 0.5])(q0, q1, q2),
        ]
    )
