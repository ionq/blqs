import pymore

import blqs


def test_str():
    assert str(blqs.Operand("abc")) == "abc"


def test_eq():
    tester = pymore.EqualsTester()
    tester.make_equality_group(lambda: blqs.Operand("a"))
    tester.make_equality_group(lambda: blqs.Operand("b"))


def test_name():
    assert blqs.Operand("a").name() == "a"


def test_call():
    o = blqs.Operand("a")
    assert o(0) == blqs.Instruction(o, 0)
    assert o(0, "a") == blqs.Instruction(o, 0, "a")
