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
import blqs


def test_statement_in_block():

    with blqs.Block() as b:
        s1 = blqs.Statement()
        s2 = blqs.Statement()

    expected = blqs.Block()
    expected.extend([s1, s2])
    assert b == expected


def test_statement_in_nested_block():
    with blqs.Block() as b:
        with blqs.Block() as c:
            s1 = blqs.Statement()
            s2 = blqs.Statement()
        s3 = blqs.Statement()

    expected = blqs.Block()
    expected.extend([s1, s2])
    assert c == expected

    expected = blqs.Block()
    expected.append(c)
    expected.append(s3)
    assert b == expected


def test_statement_no_default_block():
    s1 = blqs.Statement()
    with blqs.Block() as b:
        pass
    s2 = blqs.Statement()

    assert s1 not in b
    assert s2 not in b
