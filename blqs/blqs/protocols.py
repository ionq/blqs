from typing import Tuple

try:
    from typing import Protocol  # type: ignore
except ImportError:
    from typing_extensions import Protocol  # type: ignore


class SupportsIsReadable(Protocol):
    @property
    def is_readable(self) -> bool:
        ...


def is_readable(val) -> bool:
    return hasattr(val, "is_readable") and val.is_readable


class SupportsIsWritable(Protocol):
    @property
    def is_writeable(self) -> bool:
        ...


def is_writable(val) -> bool:
    return hasattr(val, "is_writable") and val.is_writable


class SupportsIsIterable(Protocol):
    @property
    def is_iterable(self) -> bool:
        ...


def is_iterable(val) -> bool:
    return hasattr(val, "is_iterable") and val.is_iterable


def readable_targets(val) -> Tuple:
    if hasattr(val, "readable_targets"):
        return val.readable_targets()
    if hasattr(val, "is_readable"):
        return (val,)
    return tuple()
