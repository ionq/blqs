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
from typing import Any

import cirq

from blqs_cirq import protocols


class DefaultQubitDecoder(protocols.SupportsDecoding[Any, cirq.Qid]):
    """A default decoder that transforms python objects into `cirq.Qids`.

    This performs the following transformations:
        * If the value is already a `cirq.Qid` then this value is returned unchanged.
        * If the value is an integer, a `cirq.LineQubit` with this value for its index is returned.
        * If the value is a string, a `cirq.NameQubit` with this value as its name is returned.
        * If the value is a tuple or list of length 2, a `cirq.GridQubit` is returned with the
            two elements corresponding to the row and column of this qubit.
        * Otherwise a `cirq.NamedQubit` is returned with a name given by the `str` of the value.
    """

    def _decode_(self, val: Any) -> cirq.Qid:
        if isinstance(val, cirq.Qid):
            return val
        elif isinstance(val, int):
            return cirq.LineQubit(val)
        elif isinstance(val, str):
            return cirq.NamedQubit(val)
        elif isinstance(val, (tuple, list)):
            if len(val) == 2 and all(isinstance(x, int) for x in val):
                return cirq.GridQubit(*val)
        return cirq.NamedQubit(str(val))


DEFAULT_QUBIT_DECODER = DefaultQubitDecoder()
