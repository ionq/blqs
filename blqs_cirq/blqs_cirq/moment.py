# Copyright 2022 The Blqs Developers
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


class Moment(blqs.Block):
    """A block that is used to construct a Moment.

    Typical usage is
    ```
    with blqs_cirq.Moment():
        H(0)
        Z(1)
    ```
    which creates moment with the two gates.

    Creating a moment operations that have qubits that overlap is valid,
    but if this is compiled, it will throw a normal Cirq exception.
    """

    def __str__(self):
        return f"with Moment():\n{super().__str__()}"
