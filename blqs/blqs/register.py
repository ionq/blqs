class Register:
    """A register containing a value.

    By default registers are `SupportsIsReadable` and `SupportsIsWritable`.
    """

    def __init__(self, name: str):
        self._name = name

    def name(self) -> str:
        return self._name

    def _is_readable_(self) -> bool:
        return True

    def _is_writable_(self) -> bool:
        return True

    def __str__(self):
        return f"R({self._name})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash((self._name,))
