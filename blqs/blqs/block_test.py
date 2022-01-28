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


def test_block_eq():
    eq = pymore.EqualsTester()
    eq.add_equality_group(blqs.Block(), blqs.Block())
    eq.make_equality_group(lambda: blqs.Block.of("a"))
    eq.make_equality_group(lambda: blqs.Block.of("a", "b"))
    eq.add_equality_group(blqs.Block.of(blqs.Block.of()))
    eq.add_equality_group(blqs.Block.of(blqs.Block.of("a")))


def test_block_str():
    assert str(blqs.Block.of("a")) == "  a"
    assert str(blqs.Block.of("a", "b")) == "  a\n  b"
    assert str(blqs.Block.of(blqs.Block.of("a"), "b")) == "    a\n  b"


def test_block_of():
    b = blqs.Block()
    b.extend(["a", "b"])
    c = blqs.Block.of("a", "b")
    assert b == c


def test_block_indexable():
    b = blqs.Block.of("a", "b", "c")
    assert b[0] == "a"
    assert b[-1] == "c"
    assert b[2] == "c"


def test_block_slicing():
    b = blqs.Block.of("a", "b", "c")
    assert b[0:1] == ["a"]
    assert b[0:2] == ["a", "b"]
    assert b[::-1] == ["c", "b", "a"]
    assert b[slice(0, 3, 2)] == ["a", "c"]


def test_block_append_and_extend():
    b = blqs.Block()
    b.append("a")
    b.append("b")

    c = blqs.Block()
    c.extend(["a", "b"])

    assert b == c


def test_block_len():
    assert len(blqs.Block()) == 0
    assert len(blqs.Block.of("a")) == 1
    assert len(blqs.Block.of("a", "a", "c")) == 3


def test_block_bool():
    assert not blqs.Block()
    assert blqs.Block.of("a")


def test_block_not_mutable():
    b = blqs.Block.of("a")
    with pytest.raises(NotImplementedError, match="modified"):
        b[0] = "b"


def test_block_statements():
    assert blqs.Block().statements() == tuple()
    assert blqs.Block.of("a").statements() == ("a",)
    assert blqs.Block.of("a", "b").statements() == ("a", "b")


def test_block_context_manager_captures():
    with blqs.Block() as b:
        s1 = blqs.Statement()
        s2 = blqs.Statement()
    assert b == blqs.Block.of(s1, s2)


def test_block_context_manager_default_blocks():
    assert blqs.get_current_block() is None
    with blqs.Block() as b:
        assert blqs.get_current_block() == b
    assert blqs.get_current_block() is None

    with blqs.Block() as c:
        assert blqs.get_current_block() == c
        with blqs.Block() as d:
            assert blqs.get_current_block() == d
        assert blqs.get_current_block() == c


def test_block_context_manager_captures_nested():
    with blqs.Block() as b:
        with blqs.Block():
            s1 = blqs.Statement()
        s2 = blqs.Statement()
        s3 = blqs.Statement()
    assert b == blqs.Block.of(blqs.Block.of(s1), s2, s3)


def test_block_statements_immutable():
    b = blqs.Block.of("a", "b")
    s = b.statements()
    with pytest.raises(TypeError, match="does not support item assignment"):
        s[0] = "b"


def test_block_parent_statement():
    blqs.Block(parent_statement=True)
    assert blqs.get_current_block() is None
