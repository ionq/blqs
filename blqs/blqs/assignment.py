from typing import Sequence, TYPE_CHECKING

from blqs import statement


if TYPE_CHECKING:
    import blqs  # coverage: ignore


class Assign(statement.Statement):
    """An assignment statement.

    Assignment statements capture the names that are assigned to and the value
    to which these names have been assigned.
    """

    def __init__(self, assign_names: Sequence[str], value: "blqs.SupportsIsReadable"):
        super().__init__()
        self._assign_names = assign_names
        self._value = value

    def assign_names(self) -> Sequence[str]:
        return self._assign_names

    def value(self) -> "blqs.SupportsIsReadable":
        return self._value

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._assign_names == other._assign_names and self._value == other._value

    def __hash__(self):
        return hash((*self._assign_names, self._value))

    def __str__(self):
        return f"{', '.join(self._assign_names)} = {self._value}"
