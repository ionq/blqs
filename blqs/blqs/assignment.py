from blqs import statement


class Assign(statement.Statement):
    def __init__(self, target_names, value):
        super().__init__()
        self._target_names = target_names
        self._value = value

    def __str__(self):
        return f"{','.join(self._target_names)} = {self._value}"
