import pymore

import blqs


def test_iterable_equality():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Iterable("name", blqs.Register("var")))
    eq.add_equality_group(blqs.Iterable("name", blqs.Register("var1")))
    eq.add_equality_group(blqs.Iterable("name1", blqs.Register("var")))
    eq.add_equality_group(blqs.Iterable("name1", blqs.Register("var"), blqs.Register("var1")))


def test_iterable_str():
    assert str(blqs.Iterable("name", blqs.Register("var"))) == "name"


def test_iterable_fields():
    i = blqs.Iterable("name", blqs.Register("var"))
    assert i.name() == "name"
    assert i.loop_vars() == (blqs.Register("var"),)

    i = blqs.Iterable("name", blqs.Register("var"), blqs.Register("var1"))
    assert i.name() == "name"
    assert i.loop_vars() == (blqs.Register("var"), blqs.Register("var1"))


def test_iterable_is_iterable():
    assert blqs.Iterable("name", blqs.Register("var"))._is_iterable_()
    assert blqs.is_iterable(blqs.Iterable("name", blqs.Register("var")))
