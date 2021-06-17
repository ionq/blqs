# Copyright 2021 The Blqs Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import inspect

import pytest

import blqs
import blqs.testing_samples as ts


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

    def if_fn_false():
        if False:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn_false)
    assert transformed_fn() == blqs.Program.of()


def test_build_if_else_native():
    def if_fn():
        if True:
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))

    def if_fn_false():
        if False:
            blqs.Op("H")(0)
        else:
            blqs.Op("H")(1)

    transformed_fn = blqs.build(if_fn_false)
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
        blqs.Op("M")(a)

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a",), blqs.Register("a"))
    assert transformed_fn() == blqs.Program.of(assign_stmt, blqs.Op("M")(blqs.Register("a")))


def test_assign_readable_targets_blqs():
    def fn():
        a, b = blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))
        blqs.Op("M")(a, b)

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a", "b"), blqs.Op("M")(blqs.Register("a"), blqs.Register("b")))

    assert transformed_fn() == blqs.Program.of(
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")),
        assign_stmt,
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")),
    )


def test_assign_readable_targets_list_blqs():
    def fn():
        [a, b] = blqs.Op("M")(blqs.Register("a"), blqs.Register("b"))
        blqs.Op("M")(a, b)

    transformed_fn = blqs.build(fn)
    assign_stmt = blqs.Assign(("a", "b"), blqs.Op("M")(blqs.Register("a"), blqs.Register("b")))
    assert transformed_fn() == blqs.Program.of(
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")),
        assign_stmt,
        blqs.Op("M")(blqs.Register("a"), blqs.Register("b")),
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


def test_build_with_config_support_if():
    def if_fn():
        if blqs.Register("a"):
            blqs.Op("H")(0)

    config = blqs.BuildConfig(support_if=False)
    transformed_fn = blqs.build_with_config(config)(if_fn)
    # blqs.Register("a") is truthy, so we just get the op.
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))


def test_build_with_config_support_for():
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
    transformed_fn = blqs.build_with_config(config)(fn)

    # FakeIterable is a blqs.Iterable but it acts like a real one because of config.
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0), blqs.Op("H")(1))


def test_build_with_config_support_while():
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
    transformed_fn = blqs.build_with_config(config)(fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))


def test_build_with_config_support_assign():
    def fn():
        a = blqs.Register("a")
        blqs.Op("H")(a)

    config = blqs.BuildConfig(support_assign=False)
    transformed_fn = blqs.build_with_config(config)(fn)
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(blqs.Register("a")))


def test_build_with_config_support_delete():
    def fn():
        a = blqs.Register("a")
        del a

    config = blqs.BuildConfig(support_delete=False)
    transformed_fn = blqs.build_with_config(config)(fn)
    assign_stmt = blqs.Assign(("a",), blqs.Register("a"))
    assert transformed_fn() == blqs.Program.of(assign_stmt)


def test_build_inside_of_class():
    class MyClass:
        @blqs.build
        def my_func(self):
            """Mydoc"""
            blqs.Op("H")(0)

    transformed_fn = MyClass().my_func
    assert transformed_fn() == blqs.Program.of(blqs.Op("H")(0))
    assert transformed_fn.__name__ == "my_func"
    assert transformed_fn.__doc__ == "Mydoc"


def test_build_inside_of_class_args():
    class MyClass:
        @blqs.build
        def my_func(self, x):
            """Mydoc"""
            blqs.Op("H")(x)

    transformed_fn = MyClass().my_func
    assert transformed_fn(1) == blqs.Program.of(blqs.Op("H")(1))


def test_build_single_before_decorators_plain_works():
    """This is the one simple case of decorators that works."""

    def add_an_op(f):
        def wrapper(*args, **kwargs):
            blqs.Op("X")(0)
            f(*args, **kwargs)

        return wrapper

    class MyClass:
        @blqs.build
        @add_an_op
        def my_func(self):
            blqs.Op("H")(0)

    transformed_fn = MyClass().my_func
    assert transformed_fn() == blqs.Program.of(blqs.Op("X")(0), blqs.Op("H")(0))


def test_build_after_decorators_fails():
    def add_an_op(f):
        def wrapper(*args, **kwargs):
            blqs.Op("X")(0)
            f(*args, **kwargs)

        return wrapper

    class MyClass:
        @add_an_op
        @blqs.build
        def my_func(self):
            blqs.Op("H")(0)

    with pytest.raises(ValueError, match="decorator"):
        MyClass().my_func()


@pytest.mark.parametrize(
    "method",
    [
        ts.only_raise,
        ts.multiple_statements,
        ts.if_native,
        ts.if_blqs,
        ts.else_native,
        ts.else_blqs,
        ts.elif_native,
        ts.elif_blqs,
        ts.for_native,
        ts.for_blqs,
        ts.for_else_native,
        ts.for_else_blqs,
        ts.while_native,
        ts.while_blqs,
        ts.while_else_native,
        ts.while_else_blqs,
        ts.larger_traceback,
    ],
)
def test_build_exception_only_raise(method):
    with pytest.raises(ts.LocatedException, match="oh no") as e:
        method()
    cause = e.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert cause.original_filename() == inspect.getfile(blqs.testing_samples)
    assert e.value.lineno in cause.linenos_dict().values()


@pytest.mark.parametrize(
    "method",
    [
        ts.blqs_build_decorator,
        ts.blqs_build_with_config_decorator,
        ts.build_decorator,
        ts.blqs_build_with_config_decorator,
        ts.blqs_alias_build_decorator,
        ts.blqs_alias_build_with_config_decorator,
        ts.blqs_build_alias_decorator,
        ts.blqs_build_with_config_alias_decorator,
    ],
)
def test_decorator_types(method):
    assert method() == blqs.Program.of(blqs.Op("X")(0))


def test_build_with_before_decorator():
    assert ts.blqs_build_with_before_decorator() == blqs.Program.of(
        blqs.Op("X")(0), blqs.Op("H")(0)
    )
    with pytest.raises(ValueError, match="decorator"):
        ts.blqs_build_with_after_decorator()
    with pytest.raises(ValueError, match="decorator"):
        ts.blqs_build_with_before_decorator_wrapped()
    with pytest.raises(ValueError, match="decorator"):
        ts.blqs_build_with_after_decorator_wrapped()

    assert ts.build(ts.blqs_build_with_only_decorator)() == blqs.Program.of(
        blqs.Op("X")(0), blqs.Op("H")(0)
    )
