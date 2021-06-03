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
from typing import Sequence

from blqs import statement


class Delete(statement.Statement):
    def __init__(self, delete_names: Sequence[str]):
        super().__init__()
        self._delete_names = delete_names

    def delete_names(self) -> Sequence[str]:
        return self._delete_names

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._delete_names == other._delete_names

    def __hash__(self):
        return hash(self._delete_names)

    def __str__(self):
        return f"del {', '.join(self._delete_names)}"
