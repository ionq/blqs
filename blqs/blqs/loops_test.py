import pymore
import pytest

import blqs


def test_for_eq():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.For(blqs.Iterable("range(5)", blqs.Register("a"))))

    f = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    with f.loop_block():
        s1 = blqs.Statement()
    eq.add_equality_group(f)

    f = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    with f.loop_block():
        s1 = blqs.Statement()
    with f.else_block():
        s2 = blqs.Statement()
    eq.add_equality_group(f)

    f = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    with f.loop_block():
        s1 = blqs.Statement()
    with f.else_block():
        s2 = blqs.Statement()
        s3 = blqs.Statement()
    eq.add_equality_group(f)


def test_for_str():
    iterable = blqs.Iterable("range(5)", blqs.Register("a"))
    loop = blqs.For(iterable)
    with loop.loop_block():
        op = blqs.Op("MOV")
        op(0, 1)
    assert str(loop) == "for R(a) in range(5):\n  MOV 0,1"

    with loop.else_block():
        op = blqs.Op("H")
        op(0)
    assert str(loop) == "for R(a) in range(5):\n  MOV 0,1\nelse:\n  H 0"


def test_for_iterable_not_iterable():
    with pytest.raises(AssertionError, match="SupportsIsIterable"):
        _ = blqs.For(1)


def test_for_iterable():
    iterable = blqs.Iterable("range(5)", blqs.Register("a"))
    assert blqs.For(iterable).iterable() == iterable

    assert blqs.For(iterable).loop_vars() == (blqs.Register("a"),)


def test_for_blocks():
    loop = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    with loop.loop_block():
        s1 = blqs.Statement()
    assert loop.loop_block() == blqs.Block.of(s1)

    with loop.else_block():
        s2 = blqs.Statement()
    assert loop.else_block() == blqs.Block.of(s2)


def test_while_eq():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.While(blqs.Register("a")))
    eq.add_equality_group(blqs.While(blqs.Register("b")))

    loop = blqs.While(blqs.Register("a"))
    with loop.loop_block():
        s1 = blqs.Statement()
    eq.add_equality_group(loop)

    loop = blqs.While(blqs.Register("a"))
    with loop.loop_block():
        s1 = blqs.Statement()
    with loop.loop_block():
        s2 = blqs.Statement()
    eq.add_equality_group(loop)


def test_while_str():
    loop = blqs.While(blqs.Register("a"))
    with loop.loop_block():
        op = blqs.Op("MOV")
        op(0, 1)
    assert str(loop) == "while R(a):\n  MOV 0,1\n"
    with loop.else_block():
        op = blqs.Op("H")
        op(0)
    assert str(loop) == "while R(a):\n  MOV 0,1\nelse:\n  H 0"


def test_while_condition_not_readable():
    with pytest.raises(AssertionError, match="SupportsIsReadable"):
        _ = blqs.While(True)


def test_while_condition():
    loop = blqs.While(blqs.Register("a"))
    assert loop.condition() == blqs.Register("a")


def test_while_blocks():
    loop = blqs.While(blqs.Register("a"))
    with loop.loop_block():
        s1 = blqs.Statement()
    assert loop.loop_block() == blqs.Block.of(s1)
    with loop.else_block():
        s2 = blqs.Statement()
    assert loop.else_block() == blqs.Block.of(s2)
