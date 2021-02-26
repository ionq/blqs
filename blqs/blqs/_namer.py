class Namer:
    """Produces new names for symbols that do not conflict with other symbols."""

    def __init__(self, global_names):
        """Initialize the Namer.

        Args:
            global_names: A set of names that are globally defined.
        """
        self._global_names = global_names
        self._added_names = set()

    def new_name(self, name_base, local_names):
        """Create a new name which does not conflict with global, already created, or local names.

        This creates a new name based upon `name_base`.  If `name_base` does not end in `_<number>`,
        then the new name will be either `name_base` or `name_base_<number>`.  The new name
        will be guaranteed to not conflict with
            * `global_names` for this `Namer` instance.
            * `local_names` passed to this call.
            * any names added by this `Namer` instance.
        The new name will attempt to added the lowest number (if necessary) as the postfix.

        Args:
            name_base: The name to try to base this new name upon.
            local_names: A set of names local to this Namer that should be avoided.

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
        while (
            new_name in self._global_names
            or new_name in local_names
            or new_name in self._added_names
        ):
            n += 1
            new_name = f"{new_name}_{n}"
        self._added_names.add(new_name)
        return new_name
