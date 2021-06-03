from typing import Generic, Union, TypeVar

F = TypeVar("F")
T = TypeVar("T")


class SupportsDecoding(Generic[F, T]):
    def _decode_(self, val: F) -> T:
        """Deco"""


def decode(decoder: SupportsDecoding[F, T], val: F) -> Union[T, F]:
    if hasattr(decoder, "_decode_"):
        return decoder._decode_(val)
    return val
