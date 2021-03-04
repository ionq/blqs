from blqs import block
from blqs import statement


class For(statement.Statement):
    def __init__(self, loop_vars, iterable):
        super().__init__()
        self._loop_vars = loop_vars
        self._iterable = iterable
        self._loop_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def loop_vars(self):
        return self._loop_vars

    def iterable(self):
        return self._iterable

    def loop_block(self):
        return self._loop_block

    def else_block(self):
        return self._else_block

    def __str__(self):
        loop_str = f"for {self._loop_vars} in {self._iterable}:\n{self._loop_block}\n"
        else_str = f"else:\n{self._else_block}"
        return loop_str + else_str if self._else_block else loop_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._loop_vars == other._loop_vars
            and self._iterable == other._iterable
            and self._loop_block == other._loop_block
            and self._else_block == other._else_block
        )


class While(statement.Statement):
    def __init__(self, condition):
        super().__init__()
        self._condition = condition
        self._loop_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def condition(self):
        return self._condition

    def loop_block(self):
        return self._loop_block

    def else_block(self):
        return self._else_block

    def __str__(self):
        loop_str = f"while {self._condition}:\n{self._loop_block}\n"
        else_str = f"else:\n{self._else_block}"
        return loop_str + else_str if self._else_block else loop_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._condition == other._condition
            and self._loop_block == other._loop_block
            and self._else_block == other._else_block
        )
