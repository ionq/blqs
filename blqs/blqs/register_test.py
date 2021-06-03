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

import blqs


def test_register_eq():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Register("a"))
    eq.add_equality_group(blqs.Register("b"))


def test_register_str():
    assert str(blqs.Register("abc")) == "R(abc)"


def test_register_field():
    assert blqs.Register("abc").name() == "abc"


def test_register_is_readable():
    assert blqs.Register("abc")._is_readable_()
    assert blqs.is_readable(blqs.Register("abc"))
    assert not blqs.is_readable(blqs.Register("abc", is_readable=False))


def test_register_is_writable():
    assert blqs.Register("abc")._is_writable_()
    assert blqs.is_writable(blqs.Register("abc"))
    assert not blqs.is_writable(blqs.Register("abc", is_writable=False))


def test_register_is_deletable():
    assert blqs.Register("abc")._is_deletable_()
    assert blqs.is_deletable(blqs.Register("abc"))
    assert not blqs.is_deletable(blqs.Register("abc", is_deletable=False))
