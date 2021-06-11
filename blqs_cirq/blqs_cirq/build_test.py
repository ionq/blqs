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
import pytest

import blqs
import blqs_cirq as bc


def test_build_empty_function():
    def fn():
        pass

    assert bc.build(fn)() == cirq.Circuit()


def test_build_statements():
    def fn():
        bc.H(0)
        bc.CX(0, 1)

    assert bc.build(fn)() == cirq.Circuit(
        [cirq.H(cirq.LineQubit(0)), cirq.CX(cirq.LineQubit(0), cirq.LineQubit(1))]
    )


def test_build_statements_instruction_unsupported():
    def fn():
        blqs.Op("H")(0)

    with pytest.raises(ValueError, match="H 0"):
        bc.build(fn)()


def test_build_unsupported_statement():
    class UnsupportedStatement(blqs.Statement):
        pass

    def fn():
        UnsupportedStatement()

    with pytest.raises(ValueError, match="UnsupportedStatement"):
        bc.build(fn)()


def test_build_circuit_op():
    def fn():
        with bc.CircuitOperation(repetitions=3):
            bc.H(0)
        bc.H(1)

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.CircuitOperation(
                cirq.Circuit([cirq.H(cirq.LineQubit(0))]).freeze(), repetitions=3
            ),
            cirq.H(cirq.LineQubit(1)),
        ]
    )


def test_build_repeat():
    def fn():
        with bc.Repeat(3):
            bc.H(0)
        bc.H(1)

    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.CircuitOperation(
                cirq.Circuit([cirq.H(cirq.LineQubit(0))]).freeze(), repetitions=3
            ),
            cirq.H(cirq.LineQubit(1)),
        ]
    )


def test_build_with_config_program_output():
    def fn():
        bc.H(0)

    build_config = bc.BuildConfig(output_circuit=False)
    assert bc.build_with_config(build_config)(fn)() == blqs.Program.of(bc.H(0))


def test_build_with_config_qubit_decoder():
    class IntToNamed:
        def _decode_(self, val):
            if isinstance(val, int):
                return cirq.NamedQubit(str(val))

    def fn():
        bc.H(0)

    build_config = bc.BuildConfig(qubit_decoder=IntToNamed())
    assert bc.build_with_config(build_config)(fn)() == cirq.Circuit([cirq.H(cirq.NamedQubit("0"))])


def test_build_with_config_circuit_op_disable():
    def fn():
        with bc.Repeat(3):
            bc.H(0)

    build_config = bc.BuildConfig(support_circuit_operation=False)
    with pytest.raises(ValueError, match="CircuitOperation"):
        bc.build_with_config(build_config)(fn)()


def test_build_with_config_if_disable():
    def fn():
        if blqs.Iterable("range", blqs.Register("a")):
            bc.H(0)

    build_config = bc.BuildConfig(blqs_build_config=blqs.BuildConfig(support_if=False))
    # Normally this would throw because if statements that support the iterable protocol
    # should be supported. However it just evaluates the iterable to be Truthy, so gives the
    # single statement
    assert bc.build_with_config(build_config)(fn)() == cirq.Circuit([cirq.H(cirq.LineQubit(0))])
