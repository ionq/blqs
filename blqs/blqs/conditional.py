import textwrap

from blqs import block


class IfBlock(block.Block):
    def __init__(self, condition):
        super().__init__()
        self._condition = condition

    def condition(self):
        return self._condition

    def else_if_block(self, condition):
        return ElseIfBlock(condition, self)

    def else_block(self):
        return ElseBlock(self)

    def __str__(self):
        return (
            textwrap.indent(f"if {self._condition}:\n", (self._level - 1) * "  ")
            + super().__str__()
        )


class ElseIfBlock(block.Block):
    def __init__(self, condition, prior_block):
        super().__init__()
        self._prior_block = prior_block
        self._condition = condition

    def else_if_block(self, condition):
        return ElseIfBlock(condition, self)

    def else_block(self):
        return ElseBlock(self)

    def __str__(self):
        return (
            textwrap.indent(f"elif {self._condition}:\n", (self._level - 1) * "  ")
            + super().__str__()
        )


class ElseBlock(block.Block):
    def __init__(self, prior_block):
        super().__init__()
        self._prior_block = prior_block

    def __str__(self):
        return textwrap.indent(f"else:\n", (self._level - 1) * "  ") + super().__str__()
