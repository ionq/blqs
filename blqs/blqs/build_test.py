import blqs


def test_build_empty_function():
    def empty():
        """My doc"""

    transformed_fn = blqs.build(empty)
    assert transformed_fn() == blqs.Program()
    assert transformed_fn.__name__ == "empty"
    assert transformed_fn.__doc__ == "My doc"


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

    def if_fn(x):
        if x:
            blqs.Op("H")(0)

    transformed_fn = blqs.build(if_fn)
    assert transformed_fn(True) == blqs.Program.of(blqs.Op("H")(0))
