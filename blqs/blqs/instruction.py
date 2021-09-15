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
from typing import TYPE_CHECKING

from blqs import protocols, statement

if TYPE_CHECKING:
    from blqs import op


class Instruction(statement.Statement):
    def __init__(self, op: "op.Op", *targets):
        super().__init__()
        self._op = op
        self._targets = tuple(targets)

    def op(self) -> "op.Op":
        return self._op

    def targets(self):
        return self._targets

    def _readable_targets_(self):
        return tuple(t for t in self._targets if protocols.is_readable(t))

    def __str__(self):
        return (
            f"{self._op} {', '.join(str(t) for t in self._targets)}"
            if self._targets
            else f"{self._op}"
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._op == other._op and self._targets == other._targets

    def __hash__(self):
        return hash((self._op, *self._targets))
