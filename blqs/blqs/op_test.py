import pymore

import blqs


def test_str():
    assert str(blqs.Op("abc")) == "abc"


def test_eq():
    tester = pymore.EqualsTester()
    tester.make_equality_group(lambda: blqs.Op("a"))
    tester.make_equality_group(lambda: blqs.Op("b"))


def test_name():
    assert blqs.Op("a").name() == "a"


def test_call():
    o = blqs.Op("a")
    assert o(0) == blqs.Instruction(o, 0)
    assert o(0, "a") == blqs.Instruction(o, 0, "a")
