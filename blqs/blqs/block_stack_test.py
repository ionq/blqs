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
import pytest

import blqs


def test_block_stack():
    assert blqs.get_current_block() is None

    b = blqs.Block.of("b")
    c = blqs.Block.of("c")
    blqs.push_new_block(b)
    blqs.push_new_block(c)
    assert blqs.get_current_block() == c
    blqs.pop_block()
    assert blqs.get_current_block() == b
    blqs.pop_block()


def test_block_pop_stack_empty():
    with pytest.raises(IndexError):
        blqs.pop_block()
