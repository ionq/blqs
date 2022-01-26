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
import sympy

import blqs
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


def test_circuit_operation_fields():
    with bc.CircuitOperation(
        repetitions=3,
        param_resolver={sympy.Symbol("x"): 0.1},
    ) as co:
        bc.HPowGate(exponent=sympy.Symbol("x"))(1)
    assert co.circuit_op_kwargs() == {
        "repetitions": 3,
        "param_resolver": {sympy.Symbol("x"): 0.1},
    }
    assert co.circuit_op_block() == blqs.Block.of(bc.HPowGate(exponent=sympy.Symbol("x"))(1))


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


def test_circuit_operation_empty():
    def fn():
        with bc.CircuitOperation():
            pass

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.CircuitOperation(cirq.Circuit().freeze()),
        ]
    )


def test_circuit_operation_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.add_equality_group(bc.CircuitOperation(), bc.CircuitOperation())
    equals_tester.add_equality_group(bc.CircuitOperation(repetitions=3))
    equals_tester.add_equality_group(
        bc.CircuitOperation(
            qubit_map={cirq.LineQubit(1): cirq.LineQubit(0)},
        )
    )
    equals_tester.add_equality_group(
        bc.CircuitOperation(
            qubit_map={cirq.LineQubit(1): cirq.LineQubit(2)},
        )
    )
    with bc.CircuitOperation() as co:
        bc.H(0)
    equals_tester.add_equality_group(co)
    with bc.CircuitOperation() as co:
        bc.H(0)
        bc.H(1)
    equals_tester.add_equality_group(co)


def test_circuit_operation_str():
    assert str(bc.CircuitOperation()) == "with CircuitOperation():\n"
    with bc.CircuitOperation() as co:
        bc.H(0)

    assert str(co) == "with CircuitOperation():\n  H 0"

    with bc.CircuitOperation(repetitions=1) as co:
        bc.H(0)
    assert str(co) == "with CircuitOperation({'repetitions': 1}):\n  H 0"

    with bc.CircuitOperation(repetitions=1, measurement_key_map={"a:0": "b"}) as co:
        bc.H(0)
    assert (
        str(co)
        == "with CircuitOperation({'repetitions': 1, 'measurement_key_map': {'a:0': 'b'}}):\n  H 0"
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


def test_repeat_empty():
    def fn():
        with bc.Repeat(3):
            pass

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.CircuitOperation(
                cirq.Circuit().freeze(),
                repetitions=3,
            ),
        ]
    )


def test_repeat_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.add_equality_group(bc.Repeat(1), bc.Repeat(1))
    equals_tester.add_equality_group(bc.Repeat(3))
    with bc.Repeat(4) as r:
        bc.H(0)
    equals_tester.add_equality_group(r)


def test_repeat_fields():
    with bc.Repeat(3) as r:
        bc.H(0)
    assert r.circuit_op_kwargs() == {"repetitions": 3}
    assert r.circuit_op_block() == blqs.Block.of(bc.H(0))


def test_repeat_str():
    r = bc.Repeat(3)
    assert str(r) == "repeat(3 times):\n"

    with bc.Repeat(3) as r:
        bc.H(0)
    assert str(r) == "repeat(3 times):\n  H 0"
