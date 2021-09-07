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
import cirq_google

import blqs_cirq as bc
from blqs_cirq import google as bcg


def test_all_gate_subclasses_in_cirq_google():
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    cirq_gate_subclasses = all_subclasses(cirq.Gate)

    cirq_google_members = set(x for _, x in inspect.getmembers(cirq_google, inspect.isclass))
    cirq_google_gate_subclasses = {
        clz for clz in cirq_gate_subclasses if clz in cirq_google_members
    }

    for clz in cirq_google_gate_subclasses:
        assert hasattr(bcg, clz.__name__)


def test_google_gates():
    def google_gates():
        bcg.SycamoreGate()(0, 1)

    q0, q1 = cirq.LineQubit.range(2)

    assert bc.build(google_gates)() == cirq.Circuit(
        [
            cirq_google.SycamoreGate()(q0, q1),
        ]
    )
