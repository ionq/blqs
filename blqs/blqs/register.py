class Register:
    """A register containing a value.

    Registers implement protocols `SupportsIsReadable`, `SupportsIsWritable` and
    `SupporstIsDeletable`.
    """

    def __init__(
        self, name: str, is_readable=True, is_writable: bool = True, is_deletable: bool = True
    ):
        """Create a register.

        Args:
            name: The name of the register.
            is_readable: Whether the register is readable or not.
            is_writable: Whether the register can be written to.
            is_deletable: Whether the register can be deleted.
        """
        self._name = name
        self._is_readable = is_readable
        self._is_writable = is_writable
        self._is_deletable = is_deletable

    def name(self) -> str:
        return self._name

    def _is_readable_(self) -> bool:
        return self._is_readable

    def _is_writable_(self) -> bool:
        return self._is_writable

    def _is_deletable_(self) -> bool:
        return self._is_deletable

    def __str__(self):
        return f"R({self._name})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash((self._name,))
