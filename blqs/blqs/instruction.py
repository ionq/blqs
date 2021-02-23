from blqs import statement


class Instruction(statement.Statement):
    def __init__(self, operand, *targets):
        super().__init__()
        self._operand = operand
        self._targets = targets

    def operand(self):
        return self._operand

    def targets(self):
        return self._targets

    def __str__(self):
        return f"{self._operand} {','.join(str(t) for t in self._targets)}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._operand == other._operand and self._targets == other._targets

    def __hash__(self):
        return hash((self._operand, *self._targets))
