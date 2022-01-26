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


def test_build_insert_strategy():
    a, b = cirq.NamedQubit("a"), cirq.NamedQubit("b")
    # This order insures that each of the different strategies produce different moment
    # structures.
    stream = [cirq.X(a), cirq.CZ(a, b), cirq.X(b), cirq.X(b), cirq.X(a)]

    def fn(strategy):
        with bc.InsertStrategy(strategy):
            bc.X("a")
            bc.CZ("a", "b")
            bc.X("b")
            bc.X("b")
            bc.X("a")

    for strategy in (
        cirq.InsertStrategy.NEW,
        cirq.InsertStrategy.INLINE,
        cirq.InsertStrategy.NEW_THEN_INLINE,
        cirq.InsertStrategy.EARLIEST,
    ):
        circuit = cirq.Circuit()
        circuit.append(stream, strategy=strategy)
        assert bc.build(fn)(strategy) == circuit


def test_build_insert_strategy_nesting_disallowed():
    def fn():
        with bc.InsertStrategy(cirq.InsertStrategy.NEW):
            bc.X(0)
            with bc.InsertStrategy(cirq.InsertStrategy.INLINE):
                bc.X(1)

    with pytest.raises(ValueError, match="InsertStrategies"):
        bc.build(fn)()


def test_build_with_config_insert_strategy_disabled():
    def fn():
        with bc.InsertStrategy(cirq.InsertStrategy.NEW):
            bc.X(0)

    build_config = bc.BuildConfig(support_insert_strategy=False)

    with pytest.raises(ValueError, match="InsertStrategy"):
        bc.build_with_config(build_config)(fn)()


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


def test_build_with_config_circuit_op_disabled():
    def fn():
        with bc.Repeat(3):
            bc.H(0)

    build_config = bc.BuildConfig(support_circuit_operation=False)
    with pytest.raises(ValueError, match="CircuitOperation"):
        bc.build_with_config(build_config)(fn)()


def test_build_moment():
    def fn():
        with bc.Moment():
            bc.CX(1, 2)
        with bc.Moment():
            bc.X(0)

    q0, q1, q2 = cirq.LineQubit.range(3)
    assert bc.build(fn)() == cirq.Circuit(
        [
            cirq.Moment([cirq.CX(q1, q2)]),
            cirq.Moment([cirq.X(q0)]),
        ]
    )


def test_build_moment_moment_invalid():
    def fn():
        with bc.Moment():
            with bc.Moment():
                bc.H(0)

    with pytest.raises(ValueError, match="Moments cannot be nested"):
        bc.build(fn)()


def test_build_moment_insert_strategy_invalid():
    def fn():
        with bc.Moment():
            with bc.InsertStrategy(strategy=cirq.InsertStrategy.NEW):
                bc.H(0)

    with pytest.raises(ValueError, match="InsertStrategy cannot be used"):
        bc.build(fn)()


def test_build_with_config_moment_disabled():
    def fn():
        with bc.Moment():
            bc.H(0)

    build_config = bc.BuildConfig(support_moment=False)
    with pytest.raises(ValueError, match="Moment"):
        bc.build_with_config(build_config)(fn)()


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


def test_build_with_config_if_disabled():
    def fn():
        if blqs.Iterable("range", blqs.Register("a")):
            bc.H(0)

    build_config = bc.BuildConfig(blqs_build_config=blqs.BuildConfig(support_if=False))
    # Normally this would throw because if statements that support the iterable protocol
    # should be supported. However it just evaluates the iterable to be Truthy, so gives the
    # single statement
    assert bc.build_with_config(build_config)(fn)() == cirq.Circuit([cirq.H(cirq.LineQubit(0))])
