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

# This file is for testing and is line space sensitive. That is the lines on which the
# code is defined matters for these tests. If you need to add new test code, please add
# it to the end.
import functools
import blqs


class LocatedException(Exception):
    def __init__(self, lineno):
        self.lineno = lineno

    def __str__(self):
        return "oh no"


@blqs.build
def only_raise():
    raise LocatedException(32)


@blqs.build
def multiple_statements():
    a = 1
    print(a)
    raise LocatedException(39)


@blqs.build
def if_native():
    if True:
        print("yes")
        raise LocatedException(46)
    else:
        print("no")


@blqs.build
def if_blqs():
    if blqs.Register("a"):
        raise LocatedException(54)


@blqs.build
def else_native():
    if False:
        print("yes")
    else:
        print("no")
        raise LocatedException(63)


@blqs.build
def else_blqs():
    if blqs.Register("a"):
        print("a")
    else:
        print("b")
        raise LocatedException(72)


@blqs.build
def elif_native():
    if False:
        print("1")
    elif True:
        print("2")
        raise LocatedException(81)
    else:
        print("3")


@blqs.build
def elif_blqs():
    if blqs.Register("a"):
        print("1")
    elif blqs.Register("b"):
        print("2")
        raise LocatedException(92)
    else:
        print("3")


@blqs.build
def for_native():
    for _ in range(5, 10):
        raise LocatedException(100)


@blqs.build
def for_blqs():
    for _ in blqs.Iterable("range(5)", blqs.Register("a")):
        raise LocatedException(106)


@blqs.build
def for_else_native():
    for x in range(5, 10):
        print(x)
    else:
        raise LocatedException(114)


@blqs.build
def for_else_blqs():
    for x in blqs.Iterable("range(5)", blqs.Register("a")):
        print(x)
    else:
        raise LocatedException(122)


@blqs.build
def while_native():
    while True:
        raise LocatedException(128)


@blqs.build
def while_blqs():
    while blqs.Register("a"):
        raise LocatedException(134)


@blqs.build
def while_else_native():
    while False:
        print("yes")
    else:
        raise LocatedException(142)


@blqs.build
def while_else_blqs():
    while blqs.Register("a"):
        print("yes")
    else:
        raise LocatedException(150)


@blqs.build
def larger_traceback():
    def inner_fn():
        raise LocatedException(156)

    inner_fn()


@blqs.build
def blqs_build_decorator():
    blqs.Op("X")(0)


@blqs.build_with_config(blqs.BuildConfig(support_if=False))
def blqs_build_with_config_decorator():
    blqs.Op("X")(0)


# pylint: disable=wrong-import-position
from blqs import build, build_with_config


@build
def build_decorator():
    blqs.Op("X")(0)


@build_with_config(blqs.BuildConfig(support_if=False))
def build_with_config_decorator():
    blqs.Op("X")(0)


# pylint: disable=wrong-import-position
import blqs as bq


@bq.build
def blqs_alias_build_decorator():
    blqs.Op("X")(0)


@bq.build_with_config(blqs.BuildConfig(support_if=False))
def blqs_alias_build_with_config_decorator():
    blqs.Op("X")(0)


# pylint: disable=wrong-import-position
from blqs import build as bld

# pylint: disable=wrong-import-position
from blqs import build_with_config as bwc


@bld
def blqs_build_alias_decorator():
    blqs.Op("X")(0)


@bwc(blqs.BuildConfig(support_if=False))
def blqs_build_with_config_alias_decorator():
    blqs.Op("X")(0)


def decorator(func):
    def wrapper():
        func()
        blqs.Op("H")(0)

    return wrapper


@blqs.build
@decorator
def blqs_build_with_before_decorator():
    blqs.Op("X")(0)


@decorator
@blqs.build
def blqs_build_with_after_decorator():
    blqs.Op("X")(0)


def decorator_wrapped(func):
    @functools.wraps(func)
    def wrapper():
        func()
        blqs.Op("H")(0)

    return wrapper


@blqs.build
@decorator_wrapped
def blqs_build_with_before_decorator_wrapped():
    blqs.Op("X")(0)


@decorator_wrapped
@blqs.build
def blqs_build_with_after_decorator_wrapped():
    blqs.Op("X")(0)


@decorator
def blqs_build_with_only_decorator():
    blqs.Op("X")(0)


@decorator_wrapped
def blqs_build_with_only_decorator_wrapped():
    blqs.Op("X")(0)
