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
from blqs import protocols


class Iterable:
    """An object that is iterable."""

    def __init__(self, name: str, *loop_vars):
        """Create the iterable.

        Args:
            name: The name of the iterable.
            loop_vars: the targets that are to be iterated over.
        """
        self._name = name
        self._loop_vars = (*loop_vars,)
        assert all(protocols.is_writable(v) for v in self._loop_vars), (
            "Iterable must have all loop variable writable. "
            f"See {protocols.SupportsIsWritable.__name__}."
        )

    def name(self):
        return self._name

    def _loop_vars_(self):
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
