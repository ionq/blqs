import pymore

import blqs


def test_assign_equality():
    e = pymore.EqualsTester()
    e.make_equality_group(lambda: blqs.Assign(["a", "b"], (1, 2)))
    e.add_equality_group(blqs.Assign(["a"], "c"))
    e.add_equality_group(blqs.Assign(["a"], "d"))
    e.add_equality_group(blqs.Assign(["b"], "c"))


def test_assign_fields():
    a = blqs.Assign(["a", "b"], "c")
    assert a.assign_names() == ["a", "b"]
    assert a.value() == "c"


def test_assign_str():
    assert str(blqs.Assign(["a", "b"], "c")) == "a, b = c"
    assert str(blqs.Assign(["a"], "c")) == "a = c"
