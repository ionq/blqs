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
from typing import Any, Tuple

try:
    from typing import Protocol
except ImportError:  # coverage: ignore
    from typing_extensions import Protocol  # type:ignore


class SupportsIsReadable(Protocol):
    """A protocol for objects that are readable.

    Readable objects can be used in conditionals and loops.
    """

    def _is_readable_(self) -> bool:
        """Returns whether the object is readable."""


def is_readable(val: Any) -> bool:
    """Determine whether an object is readable.

    Readable objects can be used in conditionals and loops.

    Checks to see if the value has the `_is_readable_` attribute and then returns the value of
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

    Checks to see if the value has the `_is_writable_` attribute and then returns the value of
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

    Checks to see if the value has the `_is_iterable_` attribute and then returns the value of
    that attribute.
    """
    return hasattr(val, "_is_iterable_") and val._is_iterable_()


class SupportsReadableTargets(Protocol):
    """A protocol for objects that have readable targets.

    Readable targets can be used for the right hand side of an assignment.
    """

    def _readable_targets_(self) -> Tuple:
        """Returns the readable targets of the object."""


def readable_targets(val: Any) -> Tuple:
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


class SupportsIsDeletable(Protocol):
    """A protocol for object that can be deleted.

    Deletable objects can be used in a delete command.
    """

    def _is_deletable_(self) -> bool:
        """Returns whether the object is deletable."""


def is_deletable(val: Any) -> bool:
    """Determine whether an object is deletable.

    Deletable objects can be used in a delete command.

    Checks to see if the value has the `_is_deletable_` attribute and then returns the value of
    that attribute.
    """
    return hasattr(val, "_is_deletable_") and val._is_deletable_()
