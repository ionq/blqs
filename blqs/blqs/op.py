from blqs import instruction


class Op:
    """The identifier component of an `Instruction`.

    Ops can be called with a list of targets to produce an `Instruction`:

    ```
    o = Op('H')
    # Create an Instruction
    o(0)
    ```
    """

    def __init__(self, name: str):
        self._name = name

    def name(self) -> str:
        return self._name

    def __str__(self):
        return str(self._name)

    def __call__(self, *targets) -> "instruction.Instruction":
        return instruction.Instruction(self, *targets)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)
