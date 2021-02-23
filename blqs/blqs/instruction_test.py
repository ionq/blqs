import pymore

import blqs


def test_str():
    assert str(blqs.Instruction(blqs.Operand("a"), 0)) == "a 0"
    assert str(blqs.Instruction(blqs.Operand("a"), 0, 1)) == "a 0,1"
    assert str(blqs.Instruction(blqs.Operand("ABC"), 0, "a")) == "ABC 0,a"


def test_eq():
    tester = pymore.EqualsTester()
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Operand("a"), 0))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Operand("b"), 0))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Operand("b"), 1, 2))
