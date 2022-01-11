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


class For(statement.Statement):
    def __init__(self, iterable: blqs.SupportsIterable):
        super().__init__()
        assert protocols.is_iterable(iterable), (
            "For's iterable parameter must be iterable. "
            f"See {protocols.SupportsIterable.__name__}."
        )
        self._iterable = iterable
        self._loop_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def iterable(self) -> blqs.SupportsIterable:
        return self._iterable

    def loop_vars(self):
        return protocols.loop_vars(self._iterable)

    def loop_block(self) -> blqs.Block:
        return self._loop_block

    def else_block(self) -> blqs.Block:
        return self._else_block

    def __str__(self):
        loop_var_str = ", ".join(str(x) for x in protocols.loop_vars(self._iterable))
        loop_str = f"for {loop_var_str} in {self._iterable}:\n{self._loop_block}"
        else_str = f"\nelse:\n{self._else_block}"
        return loop_str + else_str if self._else_block else loop_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._iterable == other._iterable
            and self._loop_block == other._loop_block
            and self._else_block == other._else_block
        )

    def __hash__(self):
        return hash((self._iterable, self._loop_block, self._else_block))


class While(statement.Statement):
    def __init__(self, condition: protocols.SupportsIsReadable):
        super().__init__()
        assert protocols.is_readable(condition), (
            "While's condition parameter must be readable. "
            f"See {protocols.SupportsIsReadable.__name__}"
        )
        self._condition = condition
        self._loop_block = block.Block(parent_statement=self)
        self._else_block = block.Block(parent_statement=self)

    def condition(self) -> blqs.SupportsIsReadable:
        return self._condition

    def loop_block(self) -> blqs.Block:
        return self._loop_block

    def else_block(self) -> blqs.Block:
        return self._else_block

    def __str__(self):
        loop_str = f"while {self._condition}:\n{self._loop_block}\n"
        else_str = f"else:\n{self._else_block}"
        return loop_str + else_str if self._else_block else loop_str

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._condition == other._condition
            and self._loop_block == other._loop_block
            and self._else_block == other._else_block
        )

    def __hash__(self):
        return hash((self._condition, self._loop_block, self._else_block))
