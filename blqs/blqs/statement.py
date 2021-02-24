from blqs import block_stack


class Statement:
    """An object that corresponds to some action that is consumed by an executor."""

    def __init__(self):
        # When in a block context, always append the statement on creation.
        if (current_block := block_stack.get_current_block()) is not None:
            current_block.append(self)
