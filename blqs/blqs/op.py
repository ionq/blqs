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
from __future__ import annotations
from typing import TYPE_CHECKING

from blqs import instruction


if TYPE_CHECKING:
    import blqs  # coverage: ignore


class Op:
    """The identifier component of an `Instruction`.

    Ops can be called with a list of targets to produce an `Instruction`:

    ```
    o = Op('H')
    # Create an Instruction
    o(0)
    ```
    """

    def __init__(self, name: str):
        self._name = name

    def name(self) -> str:
        return self._name

    def __str__(self):
        return str(self._name)

    def __call__(self, *targets) -> blqs.Instruction:
        return instruction.Instruction(self, *targets)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)
