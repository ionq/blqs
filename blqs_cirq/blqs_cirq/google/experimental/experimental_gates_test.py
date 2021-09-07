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
from blqs_cirq.google import experimental as bcge


def test_google_experimental_gates():
    def google_experimental_gates():
        bcge.CouplerPulse(
            hold_time=cirq.Duration(nanos=10),
            coupling_mhz=25.0,
            rise_time=cirq.Duration(nanos=18),
            padding_time=cirq.Duration(nanos=4),
        )(0, 1)

    q0, q1 = cirq.LineQubit.range(2)

    assert bc.build(google_experimental_gates)() == cirq.Circuit(
        [
            cirq_google.experimental.CouplerPulse(
                hold_time=cirq.Duration(nanos=10),
                coupling_mhz=25.0,
                rise_time=cirq.Duration(nanos=18),
                padding_time=cirq.Duration(nanos=4),
            )(q0, q1),
        ]
    )
