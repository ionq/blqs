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

import cirq
import pymore

import blqs
import blqs_cirq as bc


def test_insert_strategy_equality():
    equals_tester = pymore.EqualsTester()
    equals_tester.make_equality_group(lambda: bc.InsertStrategy(cirq.InsertStrategy.NEW))
    equals_tester.add_equality_group(bc.InsertStrategy(cirq.InsertStrategy.INLINE))


def test_insert_strategy_block():
    with bc.InsertStrategy(cirq.InsertStrategy.NEW) as insert_strategy:
        bc.H(0)
        bc.H(1)
    assert insert_strategy.insert_strategy_block() == blqs.Block.of(bc.H(0), bc.H(1))


def test_insert_strategy_strategy():
    with bc.InsertStrategy(cirq.InsertStrategy.NEW) as insert_strategy:
        bc.H(0)
        bc.H(1)
    assert insert_strategy.strategy() == cirq.InsertStrategy.NEW


def test_insert_strategy_str():
    with bc.InsertStrategy(cirq.InsertStrategy.NEW) as insert_strategy:
        bc.H(0)
    assert str(insert_strategy) == "with InsertStrategy(NEW):\n  H 0"
