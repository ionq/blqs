import blqs


def test_is_readable():
    class Readable(blqs.SupportsIsReadable):
        def _is_readable_(self):
            return True

    assert blqs.is_readable(Readable())

    class NotReadable(blqs.SupportsIsReadable):
        def _is_readable_(self):
            return False

    assert not blqs.is_readable((NotReadable()))

    assert not blqs.is_readable("a")


def test_is_writable():
    class Writable(blqs.SupportsIsWritable):
        def _is_writable_(self):
            return True

    assert blqs.is_writable(Writable())

    class NotWritable(blqs.SupportsIsWritable):
        def _is_writable_(self):
            return False

    assert not blqs.is_writable((NotWritable()))

    assert not blqs.is_writable("a")


def test_is_iterable():
    class Iterable(blqs.SupportsIsIterable):
        def _is_iterable_(self):
            return True

    assert blqs.is_iterable(Iterable())

    class NotIterable(blqs.SupportsIsIterable):
        def _is_iterable_(self):
            return False

    assert not blqs.is_iterable(NotIterable())

    assert not blqs.is_iterable("a")


def test_readable_targets():
    class ReadableTargets(blqs.SupportsReadableTargets):
        def _readable_targets_(self):
            return ["a", "b"]

    assert blqs.readable_targets(ReadableTargets()) == ["a", "b"]

    assert blqs.readable_targets("a") == tuple()

    class Readable(blqs.SupportsIsReadable):
        def _is_readable_(self):
            return True

    r = Readable()
    assert blqs.readable_targets(r) == (r,)

    class NotReadable(blqs.SupportsIsReadable):
        def _is_readable_(self):
            return False

    assert blqs.readable_targets(NotReadable()) == tuple()
