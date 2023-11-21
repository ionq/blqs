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
"""A thread local stack."""

import threading

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ThreadLocalStack(threading.local, Generic[T]):
    def __init__(self) -> None:
        self._stack: List[T] = []

    def peek(self) -> Optional[T]:
        return self._stack[-1] if self._stack else None

    def push(self, value: T):
        self._stack.append(value)

    def pop(self) -> T:
        if len(self._stack) != 0:
            return self._stack.pop()
        raise IndexError("Pop from an empty stack.")
