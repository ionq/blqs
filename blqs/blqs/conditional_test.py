import pymore

import blqs


def test_if_equals():
    b = blqs.If(True)
    b.if_block().append("a")

    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: b)

    c = blqs.If(False)
    c.if_block().append("a")
    eq.add_equality_group(c)

    d = blqs.If(True)
    d.if_block().append("a")
    d.else_block().append("c")
    eq.add_equality_group(d)


def test_if_str():
    b = blqs.If(True)
    b.if_block().extend(["a", "b"])
    assert str(b) == "if True:\n  a\n  b"

    c = blqs.If("c")
    c.if_block().append("a")
    c.else_block().append("b")
    assert str(c) == "if c:\n  a\nelse:\n  b"


def test_if_condition():
    b = blqs.If("abc")
    assert b.condition() == "abc"


def test_if_context_manager():
    b = blqs.If("cond")
    with b.if_block():
        s1 = blqs.Statement()
    with b.else_block():
        s2 = blqs.Statement()

    expected = blqs.If("cond")
    expected.if_block().append(s1)
    expected.else_block().append(s2)
    assert b == expected
