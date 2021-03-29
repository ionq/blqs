from blqs import statement


class Assign(statement.Statement):
    """An assignment statement.

    Assignment statements capture the names that are assigned to and the value
    to which these names have been assigned.
    """

    def __init__(self, assign_names, value):
        super().__init__()
        self._assign_names = assign_names
        self._value = value

    def assign_names(self):
        return self._assign_names

    def value(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._assign_names == other._assign_names and self._value == other._value

    def __str__(self):
        if len(self._assign_names) == 1:
            return f"{self._assign_names[0]} = {self._value}"
        else:
            return f"{', '.join(self._assign_names)} = {self._value}"
