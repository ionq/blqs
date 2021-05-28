import cirq

from blqs_cirq import protocols

from typing import Any


class DefaultQubitDecoder(protocols.SupportsDecoding[Any, cirq.Qid]):
    def _decode_(self, input: Any) -> cirq.Qid:
        if isinstance(input, cirq.Qid):
            return input
        if isinstance(input, int):
            return cirq.LineQubit(input)
        if isinstance(input, str):
            return cirq.NamedQubit(input)
        if isinstance(input, (tuple, list)):
            if len(input) == 2 and all(isinstance(x, int) for x in input):
                return cirq.GridQubit(*input)
        return cirq.NamedQubit(str(input))


DEFAULT_QUBIT_DECODER = DefaultQubitDecoder()
