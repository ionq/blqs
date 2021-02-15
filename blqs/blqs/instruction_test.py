import blqs


def test_str():
    assert str(blqs.Instruction(blqs.Operand("a"), 0)) == "a 0"
    assert str(blqs.Instruction(blqs.Operand("a"), 0, 1)) == "a 0,1"
    assert str(blqs.Instruction(blqs.Operand("ABC"), 0, "a")) == "ABC 0,a"


def test_eq():
    assert blqs.Instruction(blqs.Operand("a"), 0) == blqs.Instruction(blqs.Operand("a"), 0)
    assert blqs.Instruction(blqs.Operand("a"), 1) == blqs.Instruction(blqs.Operand("a"), 1)
    assert blqs.Instruction(blqs.Operand("b"), 1) == blqs.Instruction(blqs.Operand("b"), 1)
