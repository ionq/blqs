# Copyright 2022 The Blqs Developers
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
import pytest

import blqs_cirq as bc


def test_moment():
    def fn():
        with bc.Moment():
            bc.H(0)
            bc.CX(1, 2)

    q0, q1, q2 = cirq.LineQubit.range(3)
    assert bc.build(fn)() == cirq.Circuit(cirq.Moment([cirq.H(q0), cirq.CX(q1, q2)]))


def test_multiple_moments():
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


def test_empty_moment():
    def fn():
        with bc.Moment():
            pass

    assert bc.build(fn)() == cirq.Circuit(cirq.Moment([]))


def test_moment_target_overlap():
    def fn():
        with bc.Moment():
            bc.H(0)
            bc.CX(0, 1)

    with pytest.raises(ValueError, match="Overlapping operations"):
        bc.build(fn)()

    def fn_repeat():
        with bc.Moment():
            bc.H(0)
            with bc.Repeat(repetitions=10):
                bc.CX(0, 1)

    with pytest.raises(ValueError, match="Overlapping operations"):
        bc.build(fn_repeat)()


def test_moment_repeat():
    def fn():
        with bc.Moment():
            with bc.Repeat(repetitions=10):
                bc.H(0)

    h = cirq.Circuit([cirq.H(cirq.LineQubit(0))])

    assert bc.build(fn)() == cirq.Circuit([cirq.CircuitOperation(h.freeze(), repetitions=10)])


def test_moment_append_extend():
    m = bc.Moment()
    m.append(bc.H(0))
    m.extend([bc.X(1), bc.X(2)])
    assert m.statements() == (bc.H(0), bc.X(1), bc.X(2))


def test_moment_context_manager():
    with bc.Moment() as m:
        bc.H(0)
        bc.X(1)
    assert m.statements() == (bc.H(0), bc.X(1))


def test_moment_str():
    with bc.Moment() as m:
        pass
    assert str(m) == "with Moment():\n"

    with bc.Moment() as m:
        bc.H(0)
        bc.H(1)
    assert str(m) == "with Moment():\n  H 0\n  H 1"


def test_moment_equality():
    m0 = bc.Moment()
    with bc.Moment() as m1:
        bc.H(0)
    with bc.Moment() as m2:
        bc.H(1)
    with bc.Moment() as m3:
        bc.H(0)
        bc.H(1)

    equals_tester = pymore.EqualsTester()

    equals_tester.make_equality_group(lambda: m0)
    equals_tester.make_equality_group(lambda: m1)
    equals_tester.add_equality_group(m2)
    equals_tester.add_equality_group(m3)
