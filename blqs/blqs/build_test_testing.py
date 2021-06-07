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

# This file is for testing and is linespace sensitive. That is the lines on which the
# code is defined matters for these tests. If you need to add new test code, please add
# it to the end.
import blqs


class LocatedException(Exception):
    def __init__(self, lineno):
        self.lineno = lineno

    def __str__(self):
        return "oh no"


@blqs.build
def only_raise():
    raise LocatedException(31)


@blqs.build
def multiple_statements():
    a = 1
    print(a)
    raise LocatedException(38)


@blqs.build
def if_native():
    if True:
        print("yes")
        raise LocatedException(45)
    else:
        print("no")


@blqs.build
def if_blqs():
    if blqs.Register("a"):
        raise LocatedException(53)


@blqs.build
def else_native():
    if False:
        print("yes")
    else:
        print("no")
        raise LocatedException(62)


@blqs.build
def else_blqs():
    if blqs.Register("a"):
        print("a")
    else:
        print("b")
        raise LocatedException(57)


@blqs.build
def elif_native():
    if False:
        print("1")
    elif True:
        print("2")
        raise LocatedException(80)
    else:
        print("3")


@blqs.build
def elif_blqs():
    if blqs.Register("a"):
        print("1")
    elif blqs.Register("b"):
        print("2")
        raise LocatedException(91)
    else:
        print("3")


@blqs.build
def for_native():
    for _ in range(5, 10):
        raise LocatedException(99)


@blqs.build
def for_blqs():
    for _ in blqs.Iterable("range(5)", blqs.Register("a")):
        raise LocatedException(105)


@blqs.build
def for_else_native():
    for x in range(5, 10):
        print(x)
    else:
        raise LocatedException(113)


@blqs.build
def for_else_blqs():
    for x in blqs.Iterable("range(5)", blqs.Register("a")):
        print(x)
    else:
        raise LocatedException(121)


@blqs.build
def while_native():
    while True:
        raise LocatedException(127)


@blqs.build
def while_blqs():
    while blqs.Register("a"):
        raise LocatedException(133)


@blqs.build
def while_else_native():
    while False:
        print("yes")
    else:
        raise LocatedException(141)


@blqs.build
def while_else_blqs():
    while blqs.Register("a"):
        print("yes")
    else:
        raise LocatedException(149)


@blqs.build
def larger_traceback():
    def inner_fn():
        raise LocatedException(155)

    inner_fn()
