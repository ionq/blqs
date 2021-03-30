"""A thread local stack."""

import threading

from typing import Generic, TypeVar

T = TypeVar("T")


class ThreadLocalStack(threading.local, Generic[T]):
    def __init__(self):
        self._stack: List[T] = []

    def peek(self) -> T:
        return self._stack[-1] if self._stack else None

    def push(self, value: T):
        self._stack.append(value)

    def pop(self) -> T:
        if len(self._stack) != 0:
            return self._stack.pop()
        raise IndexError("Pop from an empty stack.")
