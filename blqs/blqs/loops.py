from blqs import block, protocols, statement


class For(statement.Statement):
    def __init__(self, iterable: protocols.SupportsIsIterable):
        super().__init__()
        self._iterable = iterable
        self._loop_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def iterable(self) -> protocols.SupportsIsIterable:
        return self._iterable

    def loop_vars(self):
        return self._iterable.loop_vars()

    def loop_block(self) -> block.Block:
        return self._loop_block

    def else_block(self) -> block.Block:
        return self._else_block

    def __str__(self):
        loop_str = f"for {self.loop_vars()} in {self._iterable}:\n{self._loop_block}"
        else_str = f"\nelse:\n{self._else_block}"
        return loop_str + else_str if self._else_block else loop_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._iterable == other._iterable
            and self._loop_block == other._loop_block
            and self._else_block == other._else_block
        )

    def __hash__(self):
        return hash((self._iterable, self._loop_block, self._else_block))


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

    def __hash__(self):
        return hash((self._condition, self._loop_block, self._else_block))
