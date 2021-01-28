from blqs import instruction


class Operand:
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return str(self._name)

    def __call__(self, *targets):
        return instruction.Instruction(self, *targets)
