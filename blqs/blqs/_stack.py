"""A thread local stack."""

import threading


class ThreadLocalStack(threading.local):
    def __init__(self):
        self._stack = []

    def peek(self):
        return self._stack[-1] if self._stack else None

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if len(self._stack) != 0:
            return self._stack.pop()
        raise IndexError("Pop from an empty stack.")
