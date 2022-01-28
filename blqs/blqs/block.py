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

import textwrap
from typing import Iterable, Iterator, List, TYPE_CHECKING, Tuple

from blqs import block_stack, statement

if TYPE_CHECKING:
    import blqs  # coverage: ignore


class Block(statement.Statement):
    """An append only container of statements.

    Blocks are a basic building blocks of blqs. They correspond to a body of a block of
    code.

    Blocks can be constructed in a variety of fashions.

        1. You can create a block and append elements onto this block.

        ```
        b = blqs.Block()
        b.append(H(0))
        b.extend([H(1), H(2)])
        ```

        2. You can create a block and then use that block in a `with` statement to enter a
        context where objects that are `blqs.Statement`s get added to the block automatically:

        ```
        with blqs.Block() as b:
            H(0)
            H(1)
            H(2)
        ```

        3. The main benefit of blqs, you can create the block using an appropriate annotation
        on a function definition:

        ```
        @blqs.build
        def my_block():
           H(0)
           H(1)
           H(2)

        b = my_block()
        ```

        The key benefit of this third method is that you can use it write idiomatic python code
        which is also converted over to appropriate blqs constructions (or not).

    Once constructed, `Block`s maybe iterated over and accessed by index or slice.
    `Block`s do not support mutation of their elements (though if those elements are
    references, the objects these reference refer to can be mutated).

    `Block`s have a boolean value of `False` if they contain no statements, otherwise
    they are `True`.

    See also `blqs.Program` for a top level `Block`.
    """

    def __init__(self, parent_statement: blqs.Statement = None):
        """Construction a block.

        Args:
            parent_statement: If set to not None, this block is not treated as a statement
                to be added to the current default block. Typically this is never set by client
                code, but is used by other statements that have their own `blqs.Block`s
                (arising, for example, in `if` statements).
        """
        if not parent_statement:
            super().__init__()
        self._statements: List[statement.Statement] = []

    @classmethod
    def of(cls, *statements) -> Block:
        """Static constructor for `blqs.Block`s.

        Example:
        ```
        blqs.Block.of(statement1, statement2)
        ```
        """
        b = cls()
        b.extend(statements)
        return b

    def __enter__(self) -> Block:
        block_stack.push_new_block(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        block_stack.pop_block()

    def statements(self) -> Tuple[statement.Statement, ...]:
        """The statements that make up a block, returned as an immutable tuple."""
        return tuple(self._statements)

    def __getitem__(self, key):
        return self._statements[key]

    def __setitem__(self, index, value):
        raise NotImplementedError("Block elements cannot be modified.")

    def __iter__(self) -> Iterator[blqs.Statement]:
        return iter(self._statements)

    def append(self, stmt: blqs.Statement):
        self._statements.append(stmt)

    def extend(self, statements: Iterable[blqs.Statement]):
        self._statements.extend(statements)

    def __len__(self) -> int:
        return len(self._statements)

    def __str__(self) -> str:
        return textwrap.indent("\n".join(str(e) for e in self), "  ")

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._statements == other._statements

    def __hash__(self):
        return hash((*self._statements,))

    def __bool__(self) -> bool:
        return bool(self._statements)
