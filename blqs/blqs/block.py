import functools
import textwrap

from blqs import block_stack
from blqs import statement


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

    Once constructed, `Block`s maybe interated over and accessed by index or slice.
    `Block`s do not support mutation of their elements (though if those elements are
    references, the objects these reference refer to can be mutated).

    See also `blqs.Program` for a top level `Block`.
    """

    def __init__(self, parent_statement=None):
        """Construction a block.

        Args:
            parent_statement: If set this block does inherits its statement properties
                (i.e. belonging to another block), from this block. Typically this is never
                set by client code, but is used by other statements that have their own
                `blqs.Block`s (arising, for example, in `if` statements).
        """
        if not parent_statement:
            super().__init__()
        self._statements = []
        self._parent_statement = parent_statement

    @staticmethod
    def of(*statements):
        """Static constructor for `Blocks`.

        Sample:
        ```
        blqs.Block.of("a", "b")
        ```
        """
        b = Block()
        b.extend(statements)
        return b

    def __enter__(self):
        block_stack.push_new_block(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        block_stack.pop_block()

    def statements(self):
        """The statements that make up a block, returned as an immutable tuple."""
        return tuple(self._statements)

    def parent_statement(self):
        """The parent statement to which this statement belongs.

        This is not None for statement that contain blocks, like an if statement.
        """
        return self._parent_statement

    def __getitem__(self, key):
        return self._statements[key]

    def __setitem__(self, index, value):
        raise NotImplementedError("Block elements cannot be modified.")

    def append(self, statement):
        self._statements.append(statement)

    def extend(self, statements):
        self._statements.extend(statements)

    def __len__(self):
        return len(self._statements)

    def __str__(self):
        return textwrap.indent("\n".join(str(e) for e in self), "  ")

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.statements() == other.statements()

    def __bool__(self):
        return bool(self._statements)
