from blqs import protocols, statement


class Instruction(statement.Statement):
    def __init__(self, op, *targets):
        super().__init__()
        self._op = op
        self._targets = tuple(targets)

    def op(self):
        return self._op

    def targets(self):
        return self._targets

    def _readable_targets_(self):
        return tuple(t for t in self._targets if protocols.is_readable(t))

    def __str__(self):

        return (
            f"{self._op} {','.join(str(t) for t in self._targets)}"
            if self._targets
            else f"{self._op}"
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._op == other._op and self._targets == other._targets

    def __hash__(self):
        return hash((self._op, *self._targets))
