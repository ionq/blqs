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
    class Iterable(blqs.SupportsIterable):
        def _is_iterable_(self):
            return True

        def _loop_vars_(self):
            return ("a",)

    assert blqs.is_iterable(Iterable())

    class NotIterable(blqs.SupportsIterable):
        def _is_iterable_(self):
            return False

    assert not blqs.is_iterable(NotIterable())

    class NoLoopVars:
        def _is_iterable_(self):
            return True

    assert not blqs.is_iterable(NoLoopVars())

    class NoIsIterable:
        def _loop_vars_(self):
            return True

    assert not blqs.is_iterable(NoIsIterable())

    assert not blqs.is_iterable("a")


def test_loop_vars():
    class Iterable(blqs.SupportsIterable):
        def _is_iterable_(self):
            return True

        def _loop_vars_(self):
            return "a", "b"

    assert blqs.loop_vars(Iterable()) == ("a", "b")


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


def test_is_deletable():
    class IsDeletable(blqs.SupportsIsDeletable):
        def _is_deletable_(self):
            return True

    assert blqs.is_deletable(IsDeletable())

    class NotDeletable(blqs.SupportsIsDeletable):
        def _is_deletable_(self):
            return False

    assert not blqs.is_deletable(NotDeletable())

    assert not blqs.is_deletable("a")
