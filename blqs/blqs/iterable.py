from blqs import protocols


class Iterable:
    """An object that is iterable."""

    def __init__(self, name: str, loop_vars):
        """Create the iterable.

        Args:
            name: The name of the iterable.
            loop_vars: the targets that are to be iterated over.
        """
        self._name = name
        assert all(protocols.is_writable(v) for v in loop_vars), (
            "Iterable must have all loop variable writable. "
            f"See {protocols.SupportsIsWritable.__name__}."
        )
        self._loop_vars = tuple(loop_vars)

    def name(self):
        return self._name

    def loop_vars(self):
        return self._loop_vars

    def _is_iterable_(self):
        return True

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name and self._loop_vars == other._loop_vars

    def __hash__(self):
        return hash((self._name, self._loop_vars))
