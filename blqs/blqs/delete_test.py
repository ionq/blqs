import pymore

import blqs


def test_delete_equality():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Delete(("a",)))
    eq.add_equality_group(blqs.Delete(("b",)))
    eq.add_equality_group(blqs.Delete(("a", "b")))
    eq.add_equality_group(blqs.Delete(("b", "a")))


def test_delete_str():
    delete = blqs.Delete(("a",))
    assert str(delete) == "del a"

    delete = blqs.Delete(("a", "b"))
    assert str(delete) == "del a, b"


def test_delete_delete_names():
    delete = blqs.Delete(("a", "b"))
    assert delete.delete_names() == ("a", "b")
