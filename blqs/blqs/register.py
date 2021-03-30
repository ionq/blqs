class Register:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def _is_readable_(self):
        return True

    def _is_writable_(self):
        return True

    def __str__(self):
        return f"R({self._name})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash((self._name,))
