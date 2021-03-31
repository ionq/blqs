from typing import Any, Tuple

try:
    from typing import Protocol
except ImportError:
    # Protocol is only available in Python 3.7 via the typing_extensions package.
    from typing_extensions import Protocol  # type: ignore


class SupportsIsReadable(Protocol):
    """A protocol for objects that are readable.

    Readable objects can be used in conditionals and loops.
    """

    def _is_readable_(self) -> bool:
        """Returns whether the object is readable."""


def is_readable(val: Any) -> bool:
    """Determine whether an object is readable.

    Readable objects can be used in conditionals and loops.

    Checks to see if the value has the `is_readable` attribute and then returns the value of
    that attribute.
    """
    return hasattr(val, "_is_readable_") and val._is_readable_()


class SupportsIsWritable(Protocol):
    """A protocol for objects that are writable.

    Writable objects can be used in assign statements.
    """

    def _is_writeable_(self) -> bool:
        """Returns whether the object is writable."""


def is_writable(val: Any) -> bool:
    """Determine whether an object is writable.

    Writable objects can be used in conditionals and loops.

    Checks to see if the value has the `is_writable` attribute and then returns the value of
    that attribute.
    """
    return hasattr(val, "_is_writable_") and val._is_writable_()


class SupportsIsIterable(Protocol):
    """A protocol for objects that are iterable.

    Iterable objects can be used in for loops.
    """

    def _is_iterable_(self) -> bool:
        """Returns whether the object is iterable."""


def is_iterable(val: Any) -> bool:
    """Determine whether an object is iterable.

    Iterable objects can be used in conditionals and loops.

    Checks to see if the value has the `is_iterable` attribute and then returns the value of
    that attribute.
    """
    return hasattr(val, "_is_iterable_") and val._is_iterable_()


class SupportsReadableTargets(Protocol):
    """A protocol for objects that have readble targets.

    Readable targets can be used for the right hand side of an assignment.
    """

    def _readable_targets_(self) -> Tuple:
        """Returns the readable targets of the object."""


def readable_targets(val) -> Tuple:
    """Determine the readable targets of an object.

    An object has readable targets if either

        * it implements the SupportsReadableTargets protocol, in which case the readable targets
            will be those returned by the `readable_targets` property.

        * it implements the SupportsIsReadableProtocol, in which case the readable targets will
            be the this object itself (as a single element of a tuple).
    """
    if hasattr(val, "_readable_targets_"):
        return val._readable_targets_()
    if hasattr(val, "_is_readable_") and val._is_readable_():
        return (val,)
    return tuple()
