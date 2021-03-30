import pymore

import blqs


def test_instruction_str():
    assert str(blqs.Instruction(blqs.Op("a"))) == "a"
    assert str(blqs.Instruction(blqs.Op("a"), 0)) == "a 0"
    assert str(blqs.Instruction(blqs.Op("a"), 0, 1)) == "a 0,1"
    assert str(blqs.Instruction(blqs.Op("ABC"), 0, "a")) == "ABC 0,a"


def test_instruction_eq():
    tester = pymore.EqualsTester()
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Op("a")))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Op("a"), 0))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Op("b"), 0))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Op("b"), 1, 2))
    tester.make_equality_group(lambda: blqs.Instruction(blqs.Op("b"), 1, 3))


def test_instruction_fields():
    i = blqs.Instruction(blqs.Op("b"), 1, 2)
    assert i.op() == blqs.Op("b")
    assert i.targets() == (1, 2)


def test_instruction_readable_targets():
    i = blqs.Instruction(blqs.Op("b"))
    assert i._readable_targets_() == tuple()
    assert blqs.readable_targets(i) == tuple()

    i = blqs.Instruction(blqs.Op("b"), 1, 2)
    assert i._readable_targets_() == tuple()
    assert blqs.readable_targets(i) == tuple()

    i = blqs.Instruction(blqs.Op("a"), blqs.Register("b"))
    assert i._readable_targets_() == (blqs.Register("b"),)
    assert blqs.readable_targets(i) == (blqs.Register("b"),)

    i = blqs.Instruction(blqs.Op("a"), 0, blqs.Register("b"))
    assert i._readable_targets_() == (blqs.Register("b"),)
    assert blqs.readable_targets(i) == (blqs.Register("b"),)
