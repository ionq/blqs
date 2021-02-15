import blqs


def test_str():
    assert str(blqs.Operand("abc")) == "abc"


def test_eq():
    assert blqs.Operand("a") == blqs.Operand("a")
    assert blqs.Operand("a") != blqs.Operand("b")
    assert hash(blqs.Operand("a")) == hash(blqs.Operand("a"))
    assert hash(blqs.Operand("a")) != hash(blqs.Operand("b"))
    blqs.Operand("a") == "a"


def test_name():
    assert blqs.Operand("a").name() == "a"


def test_call():
    o = blqs.Operand("a")
    assert o(0) == blqs.Instruction(o, 0)
    assert o(0, "a") == blqs.Instruction(o, 0, "a")
