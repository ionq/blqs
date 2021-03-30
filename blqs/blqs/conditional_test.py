import pymore
import pytest

import blqs


def test_if_equals():
    b = blqs.If(blqs.Register("a"))
    b.if_block().append("a")

    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: b)

    c = blqs.If(blqs.Register("b"))
    c.if_block().append("a")
    eq.add_equality_group(c)

    d = blqs.If(blqs.Register("b"))
    d.if_block().append("a")
    d.else_block().append("c")
    eq.add_equality_group(d)


def test_if_str():
    b = blqs.If(blqs.Register("a"))
    b.if_block().extend(["a", "b"])
    assert str(b) == "if R(a):\n  a\n  b"

    c = blqs.If(blqs.Register("c"))
    c.if_block().append("a")
    c.else_block().append("b")
    assert str(c) == "if R(c):\n  a\nelse:\n  b"


def test_if_condition_not_readable():
    with pytest.raises(AssertionError, match="SupportsIsReadable"):
        _ = blqs.If(True)


def test_if_condition():
    b = blqs.If(blqs.Register("abc"))
    assert b.condition() == blqs.Register("abc")


def test_if_context_manager():
    b = blqs.If(blqs.Register("cond"))
    with b.if_block():
        s1 = blqs.Statement()
    with b.else_block():
        s2 = blqs.Statement()

    expected = blqs.If(blqs.Register("cond"))
    expected.if_block().append(s1)
    expected.else_block().append(s2)
    assert b == expected
