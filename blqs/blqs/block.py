import functools
import textwrap

from blqs import block_stack
from blqs import statement


class Block(statement.Statement):
    def __init__(self, parent_statement=None):
        if not parent_statement:
            super().__init__()
        self._statements = []
        self._parent_statement = parent_statement

    def __enter__(self):
        block_stack.push_new_block(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        block_stack.pop_block()

    def statements(self):
        return self._statements

    def __getitem__(self, key):
        return self._statements[key]

    def append(self, statement):
        self._statements.append(statement)

    def extend(self, statements):
        self._statements.extend(statements)

    def __len__(self):
        return len(self._statements)

    def __str__(self):
        return textwrap.indent("\n".join(str(e) for e in self._statements), "  ")
