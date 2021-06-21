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
import functools
import inspect

from typing import Callable, Type, Union

import cirq

import blqs

GateLikeType = Union[cirq.Gate, Callable[[], cirq.Gate], functools.partial]


class CirqBlqsOp(blqs.Op):
    """A `blqs.Op` corresponding to a `cirq.Gate`."""

    def __init__(self, gate: GateLikeType, op_name: str = None):
        """Construct a CirqBlqsOp.

        Args:
            gate: The gate for this op. Alternatively a method that can be called to produce a gate.
            op_name: If specified the op name, otherwise the op name will be `str(gate)`.
        """
        super().__init__(op_name or str(gate))
        self._gate = gate

    def gate(self) -> GateLikeType:
        """The `cirq.Gate` or a callable which produces this gate for this op."""
        return self._gate

    def __getattribute__(self, name: str):
        if name == "__doc__":
            if self._gate.__doc__ is None:
                return "Gate has no documentation."
            return f"From Cirq documentation:\n{self._gate.__doc__}"
        else:
            return super().__getattribute__(name)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name == other._name and self._gate == other._gate

    def __hash__(self):
        return hash((self._name, self._gate))


class CirqBlqsOpFactory:
    """A wrapper for Cirq gate classes or methods with params that when called give a `cirq.Gate`.

    Example, supposing that `MyGateClass` is a `cirq.Gate` subclass and it uses an
    `__init__` with two args and two keywork args:
        ```
        factory = CirqBlqsOpFactory(MyGateClass)
        cirq_blqs_op = factory(arg1, arg2, kw1=val1, kw2=val2)
        ```
    """

    def __init__(
        self,
        cirq_gate_factory: Union[Type, Callable[..., cirq.Gate]],
    ):
        self._cirq_gate_factory = cirq_gate_factory

    def cirq_gate_factory(self):
        return self._cirq_gate_factory

    def __call__(self, *args, **kwargs) -> CirqBlqsOp:
        gate = self._cirq_gate_factory(*args, **kwargs)
        return CirqBlqsOp(gate)

    def __getattribute__(self, name: str):
        if name == "__doc__":
            if self._cirq_gate_factory.__doc__ is None:
                return "Gate factory has no documentation."
            return f"From Cirq documentation:\n{self._cirq_gate_factory.__doc__}"
        else:
            return super().__getattribute__(name)

    def __str__(self):
        return str(self._cirq_gate_factory.__name__)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._cirq_gate_factory == other._cirq_gate_factory

    def __hash__(self):
        return hash(self._cirq_gate_factory)


def create_cirq_blqs_op(
    cirq_construct: Union[cirq.Gate, Type[cirq.Gate], Callable[..., cirq.Gate]]
) -> Union[CirqBlqsOp, CirqBlqsOpFactory, Callable[..., CirqBlqsOp]]:
    """Construct a blqs object for the relevant cirq gate, class, or method.

    Note that this will not work for methods that require qubit targets and parameters to construct
    a `cirq.Operation`.  See `measure` for an example of how to handle this case.
    """
    if inspect.isclass(cirq_construct):
        return CirqBlqsOpFactory(cirq_construct)
    elif inspect.isfunction(cirq_construct):

        def wrapped(*args, **kwargs):
            return CirqBlqsOp(cirq_construct(*args, **kwargs))

        return wrapped
    else:
        return CirqBlqsOp(cirq_construct)
