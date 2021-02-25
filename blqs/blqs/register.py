class Register:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    @property
    def has_value(self):
        return True

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name
