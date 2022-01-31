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
import pytest

import blqs_cirq as bc


def test_cirq_blqs_op_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOp(cirq.H))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X, op_name="x"))


def test_cirq_blqs_instruction_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.CirqBlqsOp(cirq.H)(0))
    equals_tester.add_equality_group(bc.CirqBlqsOp(cirq.X)(0))


def test_cirq_blqs_op_fields():
    op = bc.CirqBlqsOp(cirq.X)
    assert op.gate() == cirq.X
    assert op.name() == "X"
    op = bc.CirqBlqsOp(cirq.X, op_name="x")
    assert op.name() == "x"


def test_cirq_blqs_op_str():
    assert str(bc.CirqBlqsOp(cirq.X)) == str(cirq.X)
    assert str(bc.CirqBlqsOp(cirq.XPowGate(exponent=0.5))) == str(cirq.XPowGate(exponent=0.5))


def test_cirq_blqs_op_doc_delegation():
    op = bc.CirqBlqsOp(cirq.X)
    assert "From Cirq documentation" in op.__doc__
    assert "X" in op.__doc__


def test_cirq_blqs_op_delegated_power():
    op = bc.CirqBlqsOp(cirq.X)
    assert op**0.1 == bc.CirqBlqsOp(gate=cirq.X**0.1, op_name="X")


def test_cirq_blqs_op_delegated_with_probability():
    op = bc.CirqBlqsOp(cirq.X)
    assert op.with_probability(0.1) == bc.CirqBlqsOp(gate=cirq.X.with_probability(0.1), op_name="X")


def test_cirq_blqs_op_delegated_controlled():
    op = bc.CirqBlqsOp(cirq.X)
    delegated = op.controlled(1, control_values=[0], control_qid_shape=(3,))
    expected = bc.CirqBlqsOp(
        gate=cirq.X.controlled(1, control_values=[0], control_qid_shape=(3,)),
        op_name="X",
    )
    assert delegated == expected


def test_cirq_blqs_op_doc_delegation_no_documentation():
    class NoDocumentationGate(cirq.SingleQubitGate):
        pass

    op = bc.CirqBlqsOp(NoDocumentationGate())
    assert op.__doc__ == "Gate has no documentation in Cirq."

    # Clean up the gate class, otherwise it shows up as a subclass of cirq.Gate and
    # this can interfere with other tests (!).
    NoDocumentationGate.__bases__ = (type("DummyClass", (object,), {}),)


def test_cirq_blqs_op_undefined_attribute():
    with pytest.raises(AttributeError):
        _ = bc.CirqBlqsOp(cirq.X).notdefined


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


def test_cirq_blqs_op_factory_doc_delegation():
    op = bc.CirqBlqsOpFactory(cirq.XPowGate)
    assert "From Cirq documentation" in op.__doc__
    assert "X axis" in op.__doc__


def test_cirq_blqs_op_factory_doc_delegation_no_documentation():
    class NoDocumentationGate(cirq.Gate):
        pass

    op = bc.CirqBlqsOpFactory(NoDocumentationGate)
    assert op.__doc__ == "Gate factory has no documentation."

    # Clean up the gate class, otherwise it shows up as a subclass of cirq.Gate and
    # this can interfere with other tests (!).
    NoDocumentationGate.__bases__ = (type("DummyClass", (object,), {}),)


def test_cirq_blqs_op_factory_undefined_attribute():
    with pytest.raises(AttributeError):
        _ = bc.CirqBlqsOpFactory(cirq.XPowGate).notdefined


def test_create_cirq_blqs_op_gate():
    assert bc.create_cirq_blqs_op(cirq.X) == bc.CirqBlqsOp(gate=cirq.X)


def test_create_cirq_blqs_op_class():
    assert bc.create_cirq_blqs_op(cirq.XPowGate) == bc.CirqBlqsOpFactory(
        cirq_gate_factory=cirq.XPowGate
    )
    assert bc.create_cirq_blqs_op(cirq.XPowGate)(exponent=0.5) == bc.CirqBlqsOp(
        gate=cirq.XPowGate(exponent=0.5)
    )


def test_create_cirq_blqs_op_function():
    def x_pow(exponent):
        return cirq.XPowGate(exponent=exponent)

    my_x_pow = bc.create_cirq_blqs_op(x_pow)
    assert my_x_pow(exponent=1) == bc.CirqBlqsOp(gate=cirq.XPowGate(exponent=1))
