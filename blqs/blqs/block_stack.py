from blqs import _stack


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
