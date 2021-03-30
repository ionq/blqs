import pymore

import blqs


def test_iterable_equality():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Iterable("name", "var"))
    eq.add_equality_group(blqs.Iterable("name", "var1"))
    eq.add_equality_group(blqs.Iterable("name1", "var"))


def test_iterable_str():
    assert str(blqs.Iterable("name", "var")) == "name"


def test_iterable_fields():
    i = blqs.Iterable("name", "var")
    assert i.name() == "name"
    assert i.loop_vars() == "var"


def test_iterable_is_iterable():
    assert blqs.Iterable("name", "var")._is_iterable_()
    assert blqs.is_iterable(blqs.Iterable("name", "var"))
