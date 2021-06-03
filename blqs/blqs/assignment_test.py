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


def test_assign_equality():
    e = pymore.EqualsTester()
    e.make_equality_group(lambda: blqs.Assign(["a", "b"], (1, 2)))
    e.add_equality_group(blqs.Assign(["a"], "c"))
    e.add_equality_group(blqs.Assign(["a"], "d"))
    e.add_equality_group(blqs.Assign(["b"], "c"))


def test_assign_fields():
    a = blqs.Assign(["a", "b"], "c")
    assert a.assign_names() == ["a", "b"]
    assert a.value() == "c"


def test_assign_str():
    assert str(blqs.Assign(["a", "b"], "c")) == "a, b = c"
    assert str(blqs.Assign(["a"], "c")) == "a = c"
