from blqs import _stack

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import blqs


class _BlockStack(_stack.ThreadLocalStack["blqs.Block"]):
    def __init__(self):
        super().__init__()


_default_block_stack = _BlockStack()


def get_current_block() -> "blqs.Block":
    """Gets the block that is currently at the top of the global default stack of blocks.

    There is a global default stack of blocks. This returns the current top of the
    stack. It does not remove this from the stack (for that see `pop_block`).

    The global default stack is thread local, i.e. different threads see different
    stacks.
    """
    return _default_block_stack.peek()


def push_new_block(block: "blqs.Block"):
    """Push a new block onto the global default stack of blocks."""
    _default_block_stack.push(block)


def pop_block() -> "blqs.Block":
    """Pop a block from the top of the global default stack.

    Raises:
        IndexError: if the stack is empty.
    """
    return _default_block_stack.pop()
