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
    raise LocatedException(17)


@blqs.build
def multiple_statements():
    a = 1
    print(a)
    raise LocatedException(24)


@blqs.build
def if_native():
    if True:
        print("yes")
        raise LocatedException(31)
    else:
        print("no")


@blqs.build
def if_blqs():
    if blqs.Register("a"):
        raise LocatedException(39)


@blqs.build
def else_native():
    if False:
        print("yes")
    else:
        print("no")
        raise LocatedException(48)


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
        raise LocatedException(66)
    else:
        print("3")


@blqs.build
def elif_blqs():
    if blqs.Register("a"):
        print("1")
    elif blqs.Register("b"):
        print("2")
        raise LocatedException(77)
    else:
        print("3")


@blqs.build
def for_native():
    for _ in range(5, 10):
        raise LocatedException(85)


@blqs.build
def for_blqs():
    for _ in blqs.Iterable("range(5)", blqs.Register("a")):
        raise LocatedException(91)


@blqs.build
def for_else_native():
    for x in range(5, 10):
        print(x)
    else:
        raise LocatedException(99)


@blqs.build
def for_else_blqs():
    for x in blqs.Iterable("range(5)", blqs.Register("a")):
        print(x)
    else:
        raise LocatedException(107)


@blqs.build
def while_native():
    while True:
        raise LocatedException(113)


@blqs.build
def while_blqs():
    while blqs.Register("a"):
        raise LocatedException(119)


@blqs.build
def while_else_native():
    while False:
        print("yes")
    else:
        raise LocatedException(127)


@blqs.build
def while_else_blqs():
    while blqs.Register("a"):
        print("yes")
    else:
        raise LocatedException(135)


@blqs.build
def larger_traceback():
    def inner_fn():
        raise LocatedException(141)

    inner_fn()
