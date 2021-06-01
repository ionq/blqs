import gc
import inspect
import textwrap

import pytest

import blqs
import blqs.build_test_testing as btt


def test_build_empty_function():
    def empty():
        """My doc"""

    transformed_fn = blqs.build(empty)
    assert transformed_fn() == blqs.Program()
    assert transformed_fn.__name__ == "empty"
    assert transformed_fn.__doc__ == "My doc"


def test_build_statements():
    h = blqs.Op("H")
    cx = blqs.Op("CX")

    def fn():
        h(0)
        cx(0, 1)
        h(1)

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(h(0), cx(0, 1), h(1))


def test_build_transforms_inner_function():
    h = blqs.Op("H")

    def fn():
        def inner_fn():
            if blqs.Register("a"):
                h(0)

        h(1)
        inner_fn()

    transformed_fn = blqs.build(fn)
    if_stmt = blqs.If(blqs.Register("a"))
    if_stmt.if_block().append(h(0))
    assert transformed_fn() == blqs.Program.of(h(1), if_stmt)


def test_build_new_block_for_built_inner_function():
    h = blqs.Op("H")

    def fn():
        @blqs.build
        def inner_fn():
            h(0)

        h(1)
        inner_fn()

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(h(1), blqs.Block.of(h(0)))


def test_build_if_blqs():
    def if_fn():
        if blqs.Register("a"):
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn)
    if_stmt = blqs.If(blqs.Register("a"))
    if_stmt.if_block().append(blqs.Op("H")(0))
    assert transformed_fn() == blqs.Program.of(if_stmt)


def test_build_if_else_blqs():
    def if_fn():
        if blqs.Register("a"):
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(if_fn)
    if_stmt = blqs.If(blqs.Register("a"))
    if_stmt.if_block().append(blqs.Op("H")(0))
    if_stmt.else_block().append(blqs.Op("H")(1))
    assert transformed_fn() == blqs.Program.of(if_stmt)


def test_build_if_native():
    def if_fn():
        if True:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))

    def if_fn():
        if False:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn() == blqs.Program.of()


def test_build_if_else_native():
    def if_fn():
        if True:
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))

    def if_fn():
        if False:
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(1))


def test_build_if_capture():
    def if_fn(x):
        if x:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn)
    if_stmt = blqs.If(blqs.Register("a"))
    if_stmt.if_block().append(blqs.Op("H")(0))
    assert transformed_fn(blqs.Register("a")) == blqs.Program.of(if_stmt)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn(True) == blqs.Program.of(blqs.Op("H")(0))
    assert transformed_fn(False) == blqs.Program.of()


def test_build_if_elif_blqs():
    def if_fn():
        if blqs.Register("a"):
            blqs.Op("H")(0)
        elif blqs.Register("b"):
            blqs.Op("H")(1)
        else:
            blqs.Op("H")(2)

    transformed_fn = blqs.build(if_fn)
    if_stmt = blqs.If(blqs.Register("a"))
    if_stmt.if_block().append(blqs.Op("H")(0))
    elif_stmt = blqs.If(blqs.Register("b"))
    elif_stmt.if_block().append(blqs.Op("H")(1))
    elif_stmt.else_block().append(blqs.Op("H")(2))
    if_stmt.else_block().append(elif_stmt)
    assert transformed_fn() == blqs.Program.of(if_stmt)


def test_build_for_blqs():
    def fn():
        for x in blqs.Iterable("range(5)", blqs.Register("a")):
            blqs.Op("H")(x)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    assert transformed_fn() == blqs.Program.of(for_stmt)


def test_build_for_else_blqs():
    def fn():
        for x in blqs.Iterable("range(5)", blqs.Register("a")):
            blqs.Op("H")(x)
        else:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    for_stmt.else_block().append(blqs.Op("H")(0))
    assert transformed_fn() == blqs.Program.of(for_stmt)


def test_build_for_blqs_multiple_loop_variables():
    def fn():
        for x, y in blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")):
            blqs.Op("H")(x)
            blqs.Op("H")(y)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("b")))
    assert transformed_fn() == blqs.Program.of(for_stmt)


def test_build_for_else_blqs_multiple_loop_variables():
    def fn():
        for x, y in blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")):
            blqs.Op("H")(x)
            blqs.Op("H")(y)
        else:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("b")))
    for_stmt.else_block().append(blqs.Op("H")(0))
    assert transformed_fn() == blqs.Program.of(for_stmt)


def test_build_for_native():
    def fn():
        for x in range(2):
            blqs.Op("H")(x)

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0), blqs.Op("H")(1))


def test_build_for_else_native():
    def fn():
        for x in range(2):
            blqs.Op("H")(x)
        else:
            blqs.Op("H")(2)

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0), blqs.Op("H")(1), blqs.Op("H")(2))


def test_build_for_native_multiple_variables():
    def fn():
        for x, y in zip((1, 3), (0, 2)):
            blqs.Op("H")(x)
            blqs.Op("H")(y)

    transformed_fn = blqs.build(fn)
    h = blqs.Op("H")
    assert transformed_fn() == blqs.Program.of(h(1), h(0), h(3), h(2))


def test_build_for_else__native_multiple_variables():
    def fn():
        for x, y in zip((1, 3), (0, 2)):
            blqs.Op("H")(x)
            blqs.Op("H")(y)
        else:
            blqs.Op("H")(5)

    transformed_fn = blqs.build(fn)
    h = blqs.Op("H")
    assert transformed_fn() == blqs.Program.of(h(1), h(0), h(3), h(2), h(5))


def test_while_blqs():
    def fn():
        while blqs.Register("a"):
            blqs.Op("H")(0)

    transformed_fn = blqs.build(fn)
    while_stmt = blqs.While(blqs.Register("a"))
    while_stmt.loop_block().append(blqs.Op("H")(0))
    assert transformed_fn() == blqs.Program.of(while_stmt)


def test_while_else_blqs():
    def fn():
        while blqs.Register("a"):
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(fn)
    while_stmt = blqs.While(blqs.Register("a"))
    while_stmt.loop_block().append(blqs.Op("H")(0))
    while_stmt.else_block().append(blqs.Op("H")(1))
    assert transformed_fn() == blqs.Program.of(while_stmt)


def test_while_native():
    def fn():
        i = 0
        while i < 2:
            blqs.Op("H")(i)
            i += 1

    transformed_fn = blqs.build(fn)
    h = blqs.Op("H")
    assert transformed_fn() == blqs.Program.of(h(0), h(1))


def test_while_else_native():
    def fn():
        i = 0
        while i < 2:
            blqs.Op("H")(i)
            i += 1
        else:
            blqs.Op("H")(4)

    transformed_fn = blqs.build(fn)
    h = blqs.Op("H")
    assert transformed_fn() == blqs.Program.of(h(0), h(1), h(4))


def test_assign_blqs():
    def fn():
        a = blqs.Register("a")

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a",), blqs.Register("a"))
    assert transformed_fn() == blqs.Program.of(assign_stmt)


def test_assign_readable_targets_blqs():
    def fn():
        a, b = blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a", "b"), blqs.Op("M")(blqs.Register("a"), blqs.Register("b")))

    assert transformed_fn() == blqs.Program.of(
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")), assign_stmt
    )


def test_assign_readable_targets_list_blqs():
    def fn():
        [a, b] = blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a", "b"), blqs.Op("M")(blqs.Register("a"), blqs.Register("b")))
    assert transformed_fn() == blqs.Program.of(
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")), assign_stmt
    )


def test_build_delete_blqs():
    def fn():
        a = blqs.Register("a")
        del a

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(
        blqs.Assign(("a",), blqs.Register("a")), blqs.Delete(("a",))
    )


def test_build_delete_blqs_multiple():
    def fn():
        a, b = blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))
        del a, b

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of(
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")),
        blqs.Assign(("a", "b"), blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))),
        blqs.Delete(("a", "b")),
    )


def test_build_delete_native():
    def fn():
        a = 1
        del a

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of()


def test_build_delete_native_multiple():
    def fn():
        a, b = 1, 2
        del a, b

    transformed_fn = blqs.build(fn)
    assert transformed_fn() == blqs.Program.of()


def test_build_config_support_if():
    def if_fn():
        if blqs.Register("a"):
            blqs.Op("H")(0)

    config = blqs.BuildConfig(support_if=False)
    transformed_fn = blqs.build(if_fn, config)
    # blqs.Register("a") is truthy, so we just get the op.
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))


def test_build_config_support_for():
    class FakeIterable(blqs.Iterable):
        def __init__(self, name: str, *loop_vars):
            super().__init__(name, *loop_vars)
            self.items = [0, 1]

        def __getitem__(self, key):
            return self.items[key]

    def fn():
        for x in FakeIterable("range(5)", blqs.Register("a")):
            blqs.Op("H")(x)

    config = blqs.BuildConfig(support_for=False)
    transformed_fn = blqs.build(fn, config)

    # FakeIterable is a blqs.Iterable but it acts like a real one because of config.
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0), blqs.Op("H")(1))


def test_build_config_support_while():
    class SettableRegister(blqs.Register):
        def __init__(self, name):
            super().__init__(name)
            self.value = True

        def set_false(self):
            self.value = False

        def __bool__(self):
            return bool(self.value)

    a = SettableRegister("a")

    def fn():
        while a:
            blqs.Op("H")(0)
            # We use a method here to not have this captured by an assign.
            a.set_false()

    config = blqs.BuildConfig(support_while=False)
    transformed_fn = blqs.build(fn, config)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))


def test_build_config_support_assign():
    def fn():
        a = blqs.Register("a")

    config = blqs.BuildConfig(support_assign=False)
    transformed_fn = blqs.build(fn, config)
    assert transformed_fn() == blqs.Program.of()


def test_build_config_support_delete():
    def fn():
        a = blqs.Register("a")
        del a

    config = blqs.BuildConfig(support_delete=False)
    transformed_fn = blqs.build(fn, config)
    assign_stmt = blqs.Assign(("a",), blqs.Register("a"))
    assert transformed_fn() == blqs.Program.of(assign_stmt)


def test_build_inside_of_class():
    class MyClass:
        @blqs.build
        def my_func(self):
            blqs.Op("H")(0)

    transformed_fn = MyClass().my_func
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))
    assert transformed_fn.__name__ == "my_func"


def test_build_before_decorator():
    def add_an_op(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            blqs.Op("X")(0)

        return wrapper

    class MyClass:
        @blqs.build
        @add_an_op
        def my_func(self):
            blqs.Op("H")(0)

    transformed_fn = MyClass().my_func
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0), blqs.Op("X")(0))
    # Didn't user itertools.wraps
    assert transformed_fn.__name__ == "wrapper"


@pytest.mark.parametrize(
    "method",
    [
        btt.only_raise,
        btt.multiple_statements,
        btt.if_native,
        btt.if_blqs,
        btt.else_native,
        btt.else_blqs,
        btt.elif_native,
        btt.elif_blqs,
        btt.for_native,
        btt.for_blqs,
        btt.for_else_native,
        btt.for_else_blqs,
        btt.while_native,
        btt.while_blqs,
        btt.while_else_native,
        btt.while_else_blqs,
        btt.larger_traceback,
    ],
)
def test_build_exception_only_raise(method):
    with pytest.raises(btt.LocatedException, match="oh no") as e:
        method()
    cause = e.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert cause.original_filename() == inspect.getfile(blqs.build_test_testing)
    assert e.value.lineno in cause.linenos_dict().values()
