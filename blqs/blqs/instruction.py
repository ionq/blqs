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

    def block(self):
        return self._block

    def __str__(self):
        return f"{self._operand} {','.join(str(t) for t in self._targets)}"
