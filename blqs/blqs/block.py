import collections.abc
import functools

from blqs import _stack


class Block:
    def __init__(self):
        self._elements = []
        self._parent_block = get_current_block()
        if self._parent_block is not None:
            self._parent_block.append(self)
        self._level = (
            self._parent_block.level() + 1 if self._parent_block is not None else 0
        )
        self._target_set = (
            set(self._parent_block.target_set())
            if self._parent_block is not None
            else set()
        )

    def __enter__(self):
        push_new_block(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pop_block()

    def elements(self):
        return self._elements

    def __getitem__(self, key):
        return self._elements[key]

    def append(self, element):
        self._elements.append(element)

    def extend(self, elements):
        self._elements.extend(elements)

    def __len__(self):
        return len(self._elements)

    def __bool__(self):
        return bool(self._elements[-1]) if self._elements else False

    def level(self):
        return self._level

    def target_set(self):
        return self._target_set

    def add_targets(self, *targets):
        self._target_set.update(targets)

    def __str__(self):
        indents = "  " * self._level
        return "\n".join(indents + str(e) for e in self._elements)


class _BlockStack(_stack.ThreadLocalStack):
    def __init__(self):
        super().__init__()


_default_block_stack = _BlockStack()


def get_current_block():
    return _default_block_stack.peek()


def push_new_block(block):
    _default_block_stack.push(block)


def pop_block():
    return _default_block_stack.pop()
