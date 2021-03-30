import pymore

import blqs


def test_register_eq():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Register("a"))
    eq.add_equality_group(blqs.Register("b"))


def test_register_str():
    assert str(blqs.Register("abc")) == "R(abc)"


def test_register_field():
    assert blqs.Register("abc").name() == "abc"


def test_register_is_readable():
    assert blqs.Register("abc").is_readable
    assert blqs.is_readable(blqs.Register("abc"))


def test_register_is_writable():
    assert blqs.Register("abc").is_writable
    assert blqs.is_assignable(blqs.Register("abc"))
