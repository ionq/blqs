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

from blqs_cirq import insert_strategy, moment, protocols, qubits, repeat


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
        support_insert_strategy: Whether or not `InsertStrategy` is supported.
        support_moment: Whether or not `Moment` is supported.

    """

    output_circuit: bool = True
    qubit_decoder: qubits.DefaultQubitDecoder = qubits.DEFAULT_QUBIT_DECODER
    blqs_build_config: Optional[blqs.BuildConfig] = None
    support_circuit_operation: bool = True
    support_insert_strategy: bool = True
    support_moment: bool = True


def build(func: Callable) -> Callable:
    """Turn the supplied function into a builder for the Circuit the function specifies.

    Typical use is as a decorator
    ```
    @build
    def my_func(my_arg):
         my_code

    circuit = my_func(a_arg)
    ```
    but can also be called directly
    ```
    def my_func(my_arg):
         my_code

    circuit = build(my_func)(a_arg)
    ```

    If one wants to pass in a configuration for how the builder works, see `build_with_config`.
    """

    return _build(func)


def build_with_config(build_config: BuildConfig):
    """A factory for producing a `blqs_cirq.build` decorator with the given configuration.

    Typical use is in creating a decorator with the given config
        ```
        @build_with_config(build_config=my_config)
        def my_func(my_arg):
            my_code

        circuit = my_func(a_arg)
        ```
    """
    return functools.partial(_build, build_config=build_config)


def _build(func: Callable, build_config: Optional[BuildConfig] = None) -> Callable:
    """Turn the supplied function into a circuit for the code the function contains.

    This method is not intended to be called directly, use build or build_with_config above.
    """
    build_config = build_config or BuildConfig()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import blqs_cirq as __blqs_cirq

        blqs_build_config = build_config.blqs_build_config or blqs.BuildConfig()
        blqs_build_config.additional_decorator_specs = [
            blqs.DecoratorSpec(module=__blqs_cirq, method=build),
            blqs.DecoratorSpec(module=__blqs_cirq, method=build_with_config),
            *blqs_build_config.additional_decorator_specs,
        ]
        blqs_func = blqs.build_with_config(blqs_build_config)(func)
        program = blqs_func(*args, **kwargs)
        return _build_circuit(program, build_config) if build_config.output_circuit else program

    return wrapper


def _build_circuit(program, build_config, inside_insert_strategy=False, inside_moment=False):
    circuit = cirq.Circuit()
    for statement in program:
        if isinstance(statement, blqs.Instruction):
            targets = statement.targets()
            if hasattr(statement.op(), "gate"):
                qubits = [protocols.decode(build_config.qubit_decoder, t) for t in targets]
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
                    "disabled in the build config."
                )
        elif isinstance(statement, insert_strategy.InsertStrategy):
            if build_config.support_insert_strategy:
                if inside_insert_strategy:
                    raise ValueError("InsertStrategies cannot be nested, as the this is ambiguous.")
                if inside_moment:
                    raise ValueError("InsertStrategy cannot be used inside a Moment.")
                ops = [
                    _build_circuit(
                        [statement], build_config, inside_insert_strategy=True
                    ).all_operations()
                    for statement in statement.insert_strategy_block().statements()
                ]
                circuit.append(ops, strategy=statement.strategy())
            else:
                raise ValueError(
                    "Encountered InsertStrategy block, but support for such blocks is "
                    "disabled in the build config."
                )
        elif isinstance(statement, moment.Moment):
            if inside_moment:
                raise ValueError("Moments cannot be nested.")
            if build_config.support_moment:
                ops = _build_circuit(
                    statement.statements(), build_config, inside_moment=True
                ).all_operations()
                circuit.append(cirq.Moment(ops))
            else:
                raise ValueError(
                    "Encountered Moment block, but support for Moments is "
                    "disabled in the build config."
                )
        else:
            raise ValueError(
                f"Unsupported statement type {type(statement)}. Statement: {statement}."
            )
    return circuit
