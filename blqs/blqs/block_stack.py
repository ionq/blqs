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
from typing import Optional, TYPE_CHECKING

from blqs import _stack


if TYPE_CHECKING:
    import blqs  # coverage: ignore


class _BlockStack(_stack.ThreadLocalStack["blqs.Block"]):
    def __init__(self):
        super().__init__()


_default_block_stack = _BlockStack()


def get_current_block() -> Optional["blqs.Block"]:
    """Gets the block that is currently at the top of the global default stack of blocks.

    There is a global default stack of blocks. This returns the current top of the
    stack. It does not remove this from the stack (for that see `pop_block`).

    The global default stack is thread local, i.e. different threads see different
    stacks.
    """
    return _default_block_stack.peek()


def push_new_block(block: "blqs.Block"):
    """Push a new block onto the global default stack of blocks."""
    _default_block_stack.push(block)


def pop_block() -> "blqs.Block":
    """Pop a block from the top of the global default stack.

    Raises:
        IndexError: if the stack is empty.
    """
    return _default_block_stack.pop()
