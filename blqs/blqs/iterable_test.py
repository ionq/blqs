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


def test_iterable_equality():
    eq = pymore.EqualsTester()
    eq.make_equality_group(lambda: blqs.Iterable("name", blqs.Register("var")))
    eq.add_equality_group(blqs.Iterable("name", blqs.Register("var1")))
    eq.add_equality_group(blqs.Iterable("name1", blqs.Register("var")))
    eq.add_equality_group(blqs.Iterable("name1", blqs.Register("var"), blqs.Register("var1")))


def test_iterable_str():
    assert str(blqs.Iterable("name", blqs.Register("var"))) == "name"


def test_iterable_fields():
    i = blqs.Iterable("name", blqs.Register("var"))
    assert i.name() == "name"


def test_iterable_is_iterable():
    assert blqs.Iterable("name", blqs.Register("var"))._is_iterable_()
    assert blqs.is_iterable(blqs.Iterable("name", blqs.Register("var")))


def test_iterable_loop_vars():
    i = blqs.Iterable("name", blqs.Register("var"))
    assert blqs.loop_vars(i) == (blqs.Register("var"),)

    i = blqs.Iterable("name", blqs.Register("var"), blqs.Register("var1"))
    assert i.name() == "name"
    assert blqs.loop_vars(i) == (blqs.Register("var"), blqs.Register("var1"))
