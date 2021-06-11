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
import dataclasses
import functools
from typing import Optional, Callable

import cirq

import blqs

from blqs_cirq import protocols, qubits, repeat


@dataclasses.dataclass
class BuildConfig:
    """Configuration for the build compilation.

    Attributes:
        output_circuit: Whether or not to output a `cirq.Circuit`. If `False` outputs
            a `blqs.Program`.
        qubit_decoder: Is applied to the targets of a operation, making it simpler to
            write simple qubit strings like `0` in place of Cirq's more verbose `cirq.LineQubit(0)`,
            for example.
        blqs_build_config: If supplied an extra config passed to the build stage of blqs.
        support_circuit_operation: Whether or not `CircuitOperation` or `Repeat` ops are supported.
            If they are included and support is off, a `ValueError` is thrown.
    """

    output_circuit: bool = True
    qubit_decoder: qubits.DefaultQubitDecoder = qubits.DEFAULT_QUBIT_DECODER
    blqs_build_config: Optional[blqs.BuildConfig] = None
    support_circuit_operation: bool = True


def build(func: Callable) -> Callable:
    return _build(func)


def build_with_config(build_config: BuildConfig):
    return functools.partial(_build, build_config=build_config)


def _build(func: Callable, build_config: Optional[BuildConfig] = None) -> Callable:
    build_config = build_config or BuildConfig()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        blqs_build_config = build_config.blqs_build_config or blqs.BuildConfig()
        blqs_func = blqs.build_with_config(blqs_build_config)(func)
        program = blqs_func(*args, **kwargs)
        return _build_circuit(program, build_config) if build_config.output_circuit else program

    return wrapper


def _build_circuit(program, build_config):
    circuit = cirq.Circuit()
    for statement in program:
        if isinstance(statement, blqs.Instruction):
            qubits = [protocols.decode(build_config.qubit_decoder, t) for t in statement.targets()]
            if hasattr(statement.op(), "gate"):
                circuit.append(statement.op().gate()(*qubits))
            else:
                raise ValueError(
                    f"Unsupported instruction type: {type(statement)}. Instruction: {statement}."
                )
        elif isinstance(statement, repeat.CircuitOperation):
            if build_config.support_circuit_operation:
                subcircuit = _build_circuit(
                    statement.circuit_op_block().statements(), build_config
                ).freeze()
                circuit.append(cirq.CircuitOperation(subcircuit, **statement.circuit_op_kwargs()))
            else:
                raise ValueError(
                    "Encountered CircuitOperation or Repeat block, but support for such blocks is "
                    "disabled in build config."
                )
        else:
            raise ValueError(
                f"Unsupported statement type {type(statement)}. Statement: {statement}."
            )

    return circuit
