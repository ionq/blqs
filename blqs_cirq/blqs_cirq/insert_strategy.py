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
import blqs


class InsertStrategy(blqs.Statement):
    """Statement to switch to a new cirq.InsertionStrategy."""

    def __init__(self, strategy: cirq.InsertStrategy):
        super().__init__()
        self._strategy = strategy
        self._insert_strategy_block = blqs.Block(parent_statement=self)

    def strategy(self):
        return self._strategy

    def insert_strategy_block(self):
        return self._insert_strategy_block

    def __enter__(self):
        self._insert_strategy_block.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._insert_strategy_block.__exit__(exc_type, exc_value, traceback)

    def __str__(self):
        return f"with InsertStrategy({self._strategy}):\n{self._insert_strategy_block}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._strategy == other._strategy
            and self._insert_strategy_block == other._insert_strategy_block
        )

    def __hash__(self):
        return hash((self._strategy, self._insert_strategy_block))
