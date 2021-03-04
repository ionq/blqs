import contextlib
import textwrap

from blqs import block
from blqs import statement


@contextlib.contextmanager
def no_op():
    try:
        yield None
    finally:
        pass


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


class BareIf:
    def __init__(self, condition):
        self._condition = condition

    def if_block(self):
        return no_op() if self._condition else None

    def else_block(self):
        return no_op() if not self._condition else None
