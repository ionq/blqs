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
from blqs import block_stack


class Statement:
    """Statements are the basic building blocks of a blqs program.

    If statement are created within the context of a `blqs.Block`, then the
    statement constructor adds this statement to the block.

    ```
    with blqs.Block() as b:
        MyStatement1()
        MyStatement2()
    # b will contain MyStatement1 and MyStatement2
    assert b == [MyStatement1(), MyStatement(2)]
    ```
    """

    def __init__(self):
        # When in a block context, always append the statement on creation.
        current_block = block_stack.get_current_block()
        if current_block is not None:
            current_block.append(self)
