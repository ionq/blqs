class Register:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    @property
    def is_readable(self):
        return True

    @property
    def is_assignable(self):
        return True

    def __str__(self):
        return f"R({self._name})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name
