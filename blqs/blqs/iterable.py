class Iterable:
    def __init__(self, name, loop_vars):
        self._name = name
        self._loop_vars = loop_vars

    def name(self):
        return self._name

    def loop_vars(self):
        return self._loop_vars

    @property
    def is_iterable(self):
        return True

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name
