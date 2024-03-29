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

import cirq_google


from blqs_cirq import cirq_blqs_op

SycamoreGate = cirq_blqs_op.create_cirq_blqs_op(cirq_google.SycamoreGate)
InternalGate = cirq_blqs_op.create_cirq_blqs_op(cirq_google.InternalGate)
