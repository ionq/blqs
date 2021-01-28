from blqs import block


class Instruction:
    def __init__(self, operand, *targets):
        if (current_block := block.get_current_block()) is not None:
            current_block.append(self)
            current_block.add_targets(*targets)
            self._block = current_block
        else:
            raise ValueError("Instructions cannot be created outside of a block.")
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
