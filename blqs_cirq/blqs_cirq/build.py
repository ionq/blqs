import dataclasses
import functools

import blqs
import cirq

from blqs_cirq import protocols, repeat, qubits

from typing import Optional, Callable


@dataclasses.dataclass
class BuildConfig:
    """Configuration for the build compilation."""

    qubit_decoder: qubits.DefaultQubitDecoder = qubits.DEFAULT_QUBIT_DECODER


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
        if isinstance(statement, blqs.Statement):
            qubits = [protocols.decode(build_config.qubit_decoder, t) for t in statement.targets()]
            if hasattr(statement.op(), "gate"):
                circuit.append(statement.op().gate().on(*qubits))
            elif hasattr(statement.op(), "gate_fn"):
                circuit.append(statement.op().gate_fn()(*qubits))
        else:
            raise ValueError()

    return circuit
