import blqs


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


def test_build_for():
    def fn():
        for x in blqs.Iterable("range(5)", blqs.Register("a")):
            blqs.Op("H")(x)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    assert transformed_fn() == blqs.Program.of(for_stmt)


def test_build_for_multiple_loop_variables():
    def fn():
        for x, y in blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")):
            blqs.Op("H")(x)
            blqs.Op("H")(y)

    transformed_fn = blqs.build(fn)
    for_stmt = blqs.For(blqs.Iterable("range(5)", blqs.Register("a"), blqs.Register("b")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("a")))
    for_stmt.loop_block().append(blqs.Op("H")(blqs.Register("b")))
    assert transformed_fn() == blqs.Program.of(for_stmt)