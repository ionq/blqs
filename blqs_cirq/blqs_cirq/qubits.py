from typing import Any

import cirq

from blqs_cirq import protocols


class DefaultQubitDecoder(protocols.SupportsDecoding[Any, cirq.Qid]):
    def _decode_(self, val: Any) -> cirq.Qid:
        if isinstance(val, cirq.Qid):
            return val
        elif isinstance(val, int):
            return cirq.LineQubit(val)
        elif isinstance(val, str):
            return cirq.NamedQubit(val)
        elif isinstance(val, (tuple, list)):
            if len(val) == 2 and all(isinstance(x, int) for x in val):
                return cirq.GridQubit(*val)
        return cirq.NamedQubit(str(val))


DEFAULT_QUBIT_DECODER = DefaultQubitDecoder()
