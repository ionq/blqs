# Copyright 2021 The Blqs Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Sequence


class Namer:
    """Produces new names for symbols that do not conflict with other symbols."""

    def __init__(self, used_names: Sequence[str] = None):
        """Initialize the Namer.

        The namer is stateful, it records all new names that were created by the namer.

        Args:
            used_names: A set of names that are already used. The namer will not produce
                names from this list.
        """
        self._used_names = set(used_names or {})

    def new_name(self, name_base: str) -> str:
        """Create a new name which does not conflict with already created, or used names.

        This creates a new name based upon `name_base`.  If `name_base` does not end in `_<number>`,
        then the new name will be either `name_base` or `name_base_<number>`.  The new name
        will be guaranteed to not conflict with
            * `used_names` for this `Namer` instance.
            * any names added by this `Namer` instance.
        The new name will attempt to added the lowest number (if necessary) as the postfix.
        If the name ends in `_<number>` then this will produce the same, but for the string
        with this number removed.

        Args:
            name_base: The name to try to base this new name upon.

        Returns:
            A non conflicting new symbol satisfying the conditions described above.
        """
        new_name = name_base
        name_parts = name_base.split("_")
        # If ends in a `_<digit>``, we will try to replace with other integer.
        if name_parts[-1].isdigit():
            new_name = "_".join(name_parts[:-1])
        n = 0
        final_name = new_name
        while final_name in self._used_names:
            final_name = f"{new_name}_{n}"
            n += 1
        self._used_names.add(final_name)
        return final_name
