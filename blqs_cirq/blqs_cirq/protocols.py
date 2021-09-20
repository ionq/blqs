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
from typing import Any, TypeVar, Union

try:
    from typing import Protocol
except ImportError:  # coverage: ignore
    from typing_extensions import Protocol  # type:ignore


F = TypeVar("F", contravariant=True)
T = TypeVar("T", covariant=True)

# There is no type for NotImplemented which currently works with mypy.
NotImplementedType = Any


class SupportsDecoding(Protocol[F, T]):
    """A protocol that supports decoding an object in one representation to another.

    TypeVars:
        F: the type decoding from.
        T: the type decoding to.
    """

    def _decode_(self, val: F) -> Union[T, NotImplementedType]:
        """Decode the given value from the `F` type to the `T` type.

        If the value cannot be decoded, then this should return `NotImplemented`.
        """


def decode(
    decoder: SupportsDecoding[F, T],
    val: F,
    default: Union[T, NotImplementedType] = NotImplemented,
) -> T:
    """Use the given decoder to decode a value or return a default.

    Args:
        decoder: The decoder which implements the `SupportsDecoding` protocol.
        val: The value to decode.
        default: A default value.

    Returns:
        The value obtained by applying the decoder's `_decode_` method to it, or the give `default`
        if is specified.

    Raises:
        NotImplementedError: if no default is specified, and either there was no `_decode_`
            method or there was one and it returned `NotImplemented`.
    """
    decode_method = getattr(decoder, "_decode_", None)
    result = NotImplemented if decode_method is None else decode_method(val)
    if result is not NotImplemented:
        return result
    if default is not NotImplemented:
        return default
    raise NotImplementedError(
        "No default was specified and the decoder did not have `_decode_` method or one was and it "
        "returned NotImplemented."
    )
