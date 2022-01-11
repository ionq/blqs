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

from blqs import block, protocols, statement


if TYPE_CHECKING:
    import blqs  # coverage: ignore


class If(statement.Statement):
    def __init__(self, condition: blqs.SupportsIsReadable):
        super().__init__()
        assert protocols.is_readable(condition), (
            "If's condition parameter must be readable. See "
            f"{protocols.SupportsIsReadable.__name__}.",
        )
        self._condition = condition
        self._if_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def condition(self) -> blqs.SupportsIsReadable:
        return self._condition

    def if_block(self) -> blqs.Block:
        return self._if_block

    def else_block(self) -> blqs.Block:
        return self._else_block

    def __str__(self):
        if_str = f"if {self._condition}:\n{self._if_block}"
        else_str = f"\nelse:\n{self._else_block}"
        return if_str + else_str if self._else_block else if_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._condition == other._condition
            and self._if_block == other._if_block
            and self._else_block == other._else_block
        )

    def __hash__(self):
        return hash((self._condition, self._if_block, self._else_block))
