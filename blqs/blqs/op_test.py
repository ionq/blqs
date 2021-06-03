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


def test_str():
    assert str(blqs.Op("abc")) == "abc"


def test_eq():
    tester = pymore.EqualsTester()
    tester.make_equality_group(lambda: blqs.Op("a"))
    tester.make_equality_group(lambda: blqs.Op("b"))


def test_name():
    assert blqs.Op("a").name() == "a"


def test_call():
    o = blqs.Op("a")
    assert o(0) == blqs.Instruction(o, 0)
    assert o(0, "a") == blqs.Instruction(o, 0, "a")
