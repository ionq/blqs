import dataclasses
import functools
from typing import Optional, Callable

import cirq

import blqs

from blqs_cirq import protocols, qubits, circuit_operation


@dataclasses.dataclass
class BuildConfig:
    """Configuration for the build compilation."""

    qubit_decoder: qubits.DefaultQubitDecoder = qubits.DEFAULT_QUBIT_DECODER
    support_circuit_operation: bool = True


def build(func: Callable, build_config: Optional[BuildConfig] = None) -> Callable:
    build_config = build_config or BuildConfig()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        blqs_func = blqs.build(func)
        program = blqs_func(*args, **kwargs)
        return _build_circuit(program, build_config)

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
        elif isinstance(statement, circuit_operation.CircuitOperation):
            if build_config.support_circuit_operation:
                subcircuit = _build_circuit(statement.statements(), build_config).freeze()
                circuit.append(
                    cirq.CircuitOperation(subcircuit, **statement.circuit_operation_kwargs())
                )
            else:
                raise ValueError(
                    "Encountered CircuitOperation block, but support fo such blocks is "
                    "disabled in build config."
                )
        else:
            raise ValueError(
                f"Unsupported statement type {type(statement)}. Statement: {statement}."
            )

    return circuit
