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

import blqs_cirq as bc


def test_cirq_blqs_op_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOp(cirq.H))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X, op_name="x"))


def test_cirq_blqs_op_fields():
    op = bc.CirqBlqsOp(cirq.X)
    assert op.gate() == cirq.X
    assert op.name() == "X"
    op = bc.CirqBlqsOp(cirq.X, op_name="x")
    assert op.name() == "x"


def test_cirq_blqs_op_str():
    assert str(bc.CirqBlqsOp(cirq.X)) == str(cirq.X)
    assert str(bc.CirqBlqsOp(cirq.XPowGate(exponent=0.5))) == str(cirq.XPowGate(exponent=0.5))


def test_cirq_blqs_op_factory_eq():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOpFactory(cirq.HPowGate))
    equals_tester.add_equality_group(bc.CirqBlqsOpFactory(cirq.XPowGate))
    equals_tester.add_equality_group(bc.CirqBlqsOpFactory(cirq.bit_flip))


def test_cirq_blqs_op_factory_fields():
    assert bc.CirqBlqsOpFactory(cirq.HPowGate).cirq_gate_factory() == cirq.HPowGate
    assert bc.CirqBlqsOpFactory(cirq.bit_flip).cirq_gate_factory() == cirq.bit_flip


def test_cirq_blqs_op_factory_is_a_factory():
    assert bc.CirqBlqsOpFactory(cirq.HPowGate)(exponent=0.5) == bc.CirqBlqsOp(
        cirq.HPowGate(exponent=0.5)
    )
    assert bc.CirqBlqsOpFactory(cirq.bit_flip)(0.5) == bc.CirqBlqsOp(cirq.BitFlipChannel(0.5))


def test_cirq_blqs_op_factory_str():
    assert str(bc.CirqBlqsOpFactory(cirq.HPowGate)) == "HPowGate"
    assert str(bc.CirqBlqsOpFactory(cirq.bit_flip)) == "bit_flip"
