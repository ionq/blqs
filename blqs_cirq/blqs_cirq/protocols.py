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
from typing import Any, Generic, Protocol, Union, TypeVar

F = TypeVar("F", contravariant=True)
T = TypeVar("T", covariant=True)

# This is a special indicator value used by the
RaiseTypeErrorIfNotProvided: Any = ([],)


class SupportsDecoding(Protocol[F, T]):
    """A protocol that supports decoding an object in one representation to another."""

    def _decode_(self, val: F) -> T:
        """Decode the given value from the `F` type to the `T` type.

        If the value cannot be decoded, then this should return `NotImplemented`.
        """


def decode(
    decoder: SupportsDecoding[F, T], val: F, default: Any = RaiseTypeErrorIfNotProvided
) -> Union[T, F]:
    decode_method = getattr(decoder, "_decode_", None)
    result = NotImplemented if decode_method is None else decode_method(val)
    if result is not NotImplemented:
        return result
    if default is not RaiseTypeErrorIfNotProvided:
        return default
    raise NotImplementedError()
