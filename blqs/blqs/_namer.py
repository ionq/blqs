class Namer:
    """Produces new names for symbols that do not conflict with other symbols."""

    def __init__(self, used_names):
        """Initialize the Namer.

        Args:
            used_names: A set of names that are already named and should not be used.
        """
        self._used_names = set(used_names)

    def new_name(self, name_base):
        """Create a new name which does not conflict with already created, or used names.

        This creates a new name based upon `name_base`.  If `name_base` does not end in `_<number>`,
        then the new name will be either `name_base` or `name_base_<number>`.  The new name
        will be guaranteed to not conflict with
            * `used_names` for this `Namer` instance.
            * any names added by this `Namer` instance.
        The new name will attempt to added the lowest number (if necessary) as the postfix.

        Args:
            name_base: The name to try to base this new name upon.

        Returns:
            A non conflicting symbol that starts with `name_base` but may have a numeric postfix
            `name_base_<number`.
        """
        new_name = name_base
        name_parts = name_base.split("_")
        # If ends in a `_<digit>``, we will try to replace with other integer.
        if name_parts[-1].isdigit():
            new_name = "_".join(name_parts[:-1])
        n = 0
        while new_name in self._used_names:
            n += 1
            new_name = f"{new_name}_{n}"
        self._used_names.add(new_name)
        return new_name
