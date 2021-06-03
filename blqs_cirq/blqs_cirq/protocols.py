from typing import Generic, Union, TypeVar

F = TypeVar("F")
T = TypeVar("T")


class SupportsDecoding(Generic[F, T]):
    def _decode_(self, input: F) -> T:
        """Deco"""


def decode(decoder: SupportsDecoding[F, T], input: F) -> Union[T, F]:
    if hasattr(decoder, "_decode_"):
        return decoder._decode_(input)
    return input
