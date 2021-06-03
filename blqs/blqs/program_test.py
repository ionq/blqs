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
import pymore
import pytest

import blqs


def test_program_str():
    assert str(blqs.Program.of("a", "b")) == "a\nb"
    assert str(blqs.Program.of(blqs.Block.of("a"), "b")) == "  a\nb"


def test_program_not_at_top_block_stack():
    with blqs.Block():
        with pytest.raises(AssertionError, match="stack is empty"):
            blqs.Program()


def test_program_equality():
    eq = pymore.EqualsTester()
    eq.add_equality_group(blqs.Program(), blqs.Program())
    eq.make_equality_group(lambda: blqs.Program.of("a"))
    eq.make_equality_group(lambda: blqs.Program.of("a", "b"))
    eq.add_equality_group(blqs.Program.of(blqs.Block.of()))
    eq.add_equality_group(blqs.Program.of(blqs.Block.of("a")))
