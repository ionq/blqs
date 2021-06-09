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


class CircuitOperation(blqs.Block):
    def __init__(self, parent_statement=None, **circuit_op_kwargs):
        super().__init__(parent_statement)
        self._circuit_operation_kwargs = circuit_op_kwargs

    def circuit_operation_kwargs(self):
        return self._circuit_operation_kwargs

    def __str__(self):
        return f"with CircuitOperation({self._circuit_operation_kwargs}):\n{super().__str__()}"


class Repeat(CircuitOperation):
    def __init__(self, repetitions, parent_statement=None):
        super().__init__(parent_statement, repetitions=repetitions)
        self._repetitions = repetitions

    def repetitions(self):
        return self.repetitions

    def __str__(self):

        return f"repeat({self.repetitions} times):"
