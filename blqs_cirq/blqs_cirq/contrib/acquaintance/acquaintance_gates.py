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

from cirq.contrib import acquaintance

from blqs_cirq import cirq_blqs_op

AcquaintanceOpportunityGate = cirq_blqs_op.create_cirq_blqs_op(
    acquaintance.AcquaintanceOpportunityGate
)
BipartiteSwapNetworkGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.BipartiteSwapNetworkGate)
CircularShiftGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.CircularShiftGate)
LinearPermutationGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.LinearPermutationGate)
ShiftSwapNetworkGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.ShiftSwapNetworkGate)
SwapPermutationGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.permutation.SwapPermutationGate)
SwapNetworkGate = cirq_blqs_op.create_cirq_blqs_op(acquaintance.SwapNetworkGate)
