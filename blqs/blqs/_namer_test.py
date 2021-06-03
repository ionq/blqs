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
from blqs import _namer


def test_namer_basic():
    namer = _namer.Namer()
    assert namer.new_name("a") == "a"
    assert namer.new_name("a") == "a_0"
    assert namer.new_name("a") == "a_1"
    assert namer.new_name("a") == "a_2"


def test_namer_multi_digit():
    namer = _namer.Namer()
    for _ in range(11):
        _ = namer.new_name("a")
    assert namer.new_name("a") == "a_10"
    assert namer.new_name("a") == "a_11"


def test_namer_different_names():
    namer = _namer.Namer()
    assert namer.new_name("a") == "a"
    assert namer.new_name("b") == "b"
    assert namer.new_name("a") == "a_0"
    assert namer.new_name("a") == "a_1"
    assert namer.new_name("b") == "b_0"


def test_namer_used():
    namer = _namer.Namer(["a"])
    assert namer.new_name("a") == "a_0"
    assert namer.new_name("a") == "a_1"
    assert namer.new_name("b") == "b"


def test_namer_multiple_used():
    namer = _namer.Namer(["a", "b"])
    assert namer.new_name("a") == "a_0"
    assert namer.new_name("a") == "a_1"
    assert namer.new_name("b") == "b_0"
    assert namer.new_name("c") == "c"


def test_namer_multiple_underscores():
    namer = _namer.Namer()
    assert namer.new_name("a_b") == "a_b"
    assert namer.new_name("a_b_0") == "a_b_0"
    assert namer.new_name("a_b_c") == "a_b_c"
    assert namer.new_name("a_b_c_0") == "a_b_c_0"


def test_namer_used_with_underscores():
    namer = _namer.Namer(["a_b"])
    assert namer.new_name("a_b") == "a_b_0"


def test_namer_used_with_underscores_digits():
    namer = _namer.Namer(["a_0"])
    assert namer.new_name("a") == "a"
    assert namer.new_name("a") == "a_1"


def test_namer_used_with_underscores_digits_match():
    namer = _namer.Namer(["a_0"])
    assert namer.new_name("a_0") == "a"
    assert namer.new_name("a_0") == "a_1"
