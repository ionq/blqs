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
import inspect

import cirq
import cirq.contrib.acquaintance as acquaintance

import blqs_cirq as bc
from blqs_cirq.contrib import acquaintance as bca


def test_all_gate_subclasses_in_acquaintance():
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    cirq_gate_subclasses = all_subclasses(cirq.Gate)

    excluded_classes = {
        cirq.contrib.acquaintance.permutation.MappingDisplayGate,
        cirq.contrib.acquaintance.permutation.PermutationGate,
    }

    cirq_acquaintance_members = set(x for _, x in inspect.getmembers(acquaintance, inspect.isclass))
    cirq_acquaintance_gate_subclasses = {
        clz
        for clz in cirq_gate_subclasses
        if clz in cirq_acquaintance_members and clz not in excluded_classes
    }

    for clz in cirq_acquaintance_gate_subclasses:
        assert hasattr(bca, clz.__name__)


def test_acquaintance_gates():
    def acquaintance_gates():
        #        bca.AcquaintanceOpportunityGate(2)(0, 1)
        bca.BipartiteSwapNetworkGate(acquaintance.BipartiteGraphType.COMPLETE, 2)(0, 1, 2, 3)
        bca.CircularShiftGate(3, 2)(0, 1, 2)
        bca.LinearPermutationGate(2, permutation={0: 1, 1: 0})(0, 1)

        bca.ShiftSwapNetworkGate([1], [2])(0, 1, 2)
        bca.SwapPermutationGate()(0, 1)
        bca.SwapNetworkGate((2, 2), 3)(0, 1, 2, 3)

    q0, q1, q2, q3 = cirq.LineQubit.range(4)
    assert bc.build(acquaintance_gates)() == cirq.Circuit(
        [
            acquaintance.BipartiteSwapNetworkGate(acquaintance.BipartiteGraphType.COMPLETE, 2)(
                q0, q1, q2, q3
            ),
            acquaintance.CircularShiftGate(3, 2)(q0, q1, q2),
            acquaintance.LinearPermutationGate(2, permutation={0: 1, 1: 0})(q0, q1),
            acquaintance.ShiftSwapNetworkGate([1], [2])(q0, q1, q2),
            acquaintance.SwapPermutationGate()(q0, q1),
            acquaintance.SwapNetworkGate((2, 2), 3)(q0, q1, q2, q3),
        ]
    )


def test_acquaintance_opportunity_gate():
    # AcquaintanceOpportunityGate does not have equality.
    def acquaintance_opportunity_gate():
        bca.AcquaintanceOpportunityGate(1)(0)

    q0 = cirq.LineQubit(0)
    circuit = bc.build(acquaintance_opportunity_gate)()
    op = circuit[0][q0]
    assert type(op.gate) == acquaintance.AcquaintanceOpportunityGate
    assert op.gate.num_qubits() == 1
