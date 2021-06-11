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
from typing import Dict

import blqs


class CircuitOperation(blqs.Statement):
    def __init__(self, **circuit_op_kwargs):
        super().__init__()
        self._circuit_op_block = blqs.Block(parent_statement=self)
        self._circuit_op_kwargs = circuit_op_kwargs

    def circuit_op_kwargs(self) -> Dict:
        return self._circuit_op_kwargs

    def circuit_op_block(self) -> blqs.Block:
        return self._circuit_op_block

    def __enter__(self):
        self._circuit_op_block.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._circuit_op_block.__exit__(exc_type, exc_value, traceback)

    def __str__(self):
        return f"with CircuitOperation({self._circuit_op_kwargs or ''}):\n{self._circuit_op_block}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self._circuit_op_block == other._circuit_op_block
            and self._circuit_op_kwargs == other._circuit_op_kwargs
        )


class Repeat(CircuitOperation):
    def __init__(self, repetitions: int):
        super().__init__(repetitions=repetitions)

    def repetitions(self) -> int:
        return self.circuit_op_kwargs()["repetitions"]

    def __str__(self):
        return f"repeat({self.repetitions()} times):\n{self._circuit_op_block}"
