from blqs import statement

from typing import Sequence


class Delete(statement.Statement):
    def __init__(self, delete_names: Sequence[str]):
        super().__init__()
        self._delete_names = delete_names

    def delete_names(self) -> Sequence[str]:
        return self._delete_names

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._delete_names == other._delete_names

    def __hash__(self):
        return hash(self._delete_names)

    def __str__(self):
        return f"del {', '.join(self._delete_names)}"
