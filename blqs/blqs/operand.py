from blqs import instruction


class Operand:
    """The identifier component of an `Instruction`.

    Operands can be called with a list of targets to produce an `Instruction`:

    ```
    o = Operand('H')
    # Create an Instruction
    o(0)
    ```
    """

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def __str__(self):
        return str(self._name)

    def __call__(self, *targets):
        return instruction.Instruction(self, *targets)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)
