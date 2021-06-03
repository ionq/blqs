from typing import Any, Generic, TypeVar

F = TypeVar("F")
T = TypeVar("T")


class SupportsDecoding(Generic[F, T]):
    def _decode_(input: F) -> T:
        """Deco"""


def decode(decoder: SupportsDecoding, input: F) -> T:
    if hasattr(decoder, "_decode_"):
        return decoder._decode_(input)
    return input
