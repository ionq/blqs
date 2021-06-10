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
import sympy

import blqs_cirq as bc


def test_circuit_operation():
    def fn():
        bc.H(0)
        with bc.CircuitOperation():
            bc.H(1)

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.CircuitOperation(cirq.Circuit([cirq.H(cirq.LineQubit(1))]).freeze()),
        ]
    )


def test_circuit_operation_args():
    def fn():
        with bc.CircuitOperation(
            repetitions=3,
            qubit_map={cirq.LineQubit(1): cirq.LineQubit(0)},
            measurement_key_map={"a:0": "b"},
            param_resolver={sympy.Symbol("x"): 0.1},
            repetition_ids=["1", "3", "5"],
        ):
            bc.HPowGate(exponent=sympy.Symbol("x"))(1)
            bc.measure(1, key="a")

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.CircuitOperation(
                circuit=cirq.Circuit(
                    [
                        cirq.HPowGate(exponent=sympy.Symbol("x"))(cirq.LineQubit(1)),
                        cirq.measure(cirq.LineQubit(1), key="a"),
                    ]
                ).freeze(),
                repetitions=3,
                qubit_map={cirq.LineQubit(1): cirq.LineQubit(0)},
                measurement_key_map={"a:0": "b"},
                param_resolver={sympy.Symbol("x"): 0.1},
                repetition_ids=["1", "3", "5"],
            ),
        ]
    )


def test_circuit_operation_nested():
    def fn():
        bc.H(0)
        with bc.CircuitOperation():
            bc.H(1)
            with bc.CircuitOperation():
                bc.H(2)
            with bc.CircuitOperation():
                bc.H(3)

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.CircuitOperation(
                cirq.Circuit(
                    [
                        cirq.H(cirq.LineQubit(1)),
                        cirq.CircuitOperation(cirq.Circuit([cirq.H(cirq.LineQubit(2))]).freeze()),
                        cirq.CircuitOperation(cirq.Circuit([cirq.H(cirq.LineQubit(3))]).freeze()),
                    ]
                ).freeze()
            ),
        ]
    )


def test_repeat():
    def fn():
        bc.H(0)
        with bc.Repeat(3):
            bc.H(1)

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.H(cirq.LineQubit(0)),
            cirq.CircuitOperation(
                cirq.Circuit(
                    [
                        cirq.H(cirq.LineQubit(1)),
                    ]
                ).freeze(),
                repetitions=3,
            ),
        ]
    )
