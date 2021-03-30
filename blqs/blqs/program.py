from blqs import block, block_stack


class Program(block.Block):
    """The top level Block containing the entirety of a program."""

    def __init__(self):
        super().__init__(parent_statement=None)
        assert (
            block_stack.get_current_block() is None
        ), "Program should only be created when the current block stack is empty."

    def __str__(self):
        return "\n".join(str(e) for e in self)
