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
from blqs import block, block_stack


class Program(block.Block):
    """The top level Block containing the entirety of a program."""

    def __init__(self):
        super().__init__(parent_statement=None)
        assert (
            block_stack.get_current_block() is None
        ), "Program should only be created when the current block stack is empty."

    def __str__(self):
        return "\n".join(str(e) for e in self)
