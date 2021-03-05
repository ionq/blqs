import contextlib
import textwrap

from blqs import block, statement


class If(statement.Statement):
    def __init__(self, condition):
        super().__init__()
        self._condition = condition
        self._if_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def condition(self):
        return self._condition

    def if_block(self):
        return self._if_block

    def else_block(self):
        return self._else_block

    def __str__(self):
        if_str = f"if {self._condition}:\n{self._if_block}\n"
        else_str = f"else:\n{self._else_block}"
        return if_str + else_str if self._else_block else if_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._condition == other._condition
            and self._if_block == other._if_block
            and self._else_block == other._else_block
        )