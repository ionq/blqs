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


def test_delete_equality():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Delete(("a",)))
    eq.add_equality_group(blqs.Delete(("b",)))
    eq.add_equality_group(blqs.Delete(("a", "b")))
    eq.add_equality_group(blqs.Delete(("b", "a")))


def test_delete_str():
    delete = blqs.Delete(("a",))
    assert str(delete) == "del a"

    delete = blqs.Delete(("a", "b"))
    assert str(delete) == "del a, b"


def test_delete_delete_names():
    delete = blqs.Delete(("a", "b"))
    assert delete.delete_names() == ("a", "b")
