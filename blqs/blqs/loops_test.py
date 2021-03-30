import pymore

import blqs


def test_for_eq():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.For((1, 2)))

    f = blqs.For((1, 2))
    with f.loop_block():
        s1 = blqs.Statement()
    eq.add_equality_group(f)

    f = blqs.For((1, 2))
    with f.loop_block():
        s1 = blqs.Statement()
    with f.else_block():
        s2 = blqs.Statement()
    eq.add_equality_group(f)

    f = blqs.For((1, 2))
    with f.loop_block():
        s1 = blqs.Statement()
    with f.else_block():
        s2 = blqs.Statement()
        s3 = blqs.Statement()
    eq.add_equality_group(f)


def test_for_str():
    iterable = blqs.Iterable("range(5)", ("a",))
    loop = blqs.For(iterable)
    with loop.loop_block():
        op = blqs.Op("MOV")
        op(0, 1)
    assert str(loop) == "for ('a',) in range(5):\n  MOV 0,1"

    with loop.else_block():
        op = blqs.Op("H")
        op(0)
    assert str(loop) == "for ('a',) in range(5):\n  MOV 0,1\nelse:\n  H 0"


def test_for_iterable():
    assert blqs.For((1, 2)).iterable() == (1, 2)

    iterable = blqs.Iterable("range(5)", ("a",))
    assert blqs.For(iterable).iterable() == iterable

    assert blqs.For(iterable).loop_vars() == ("a",)


def test_for_blocks():
    loop = blqs.For(blqs.Iterable("range(5)", ("a",)))
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
