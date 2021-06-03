import blqs


class CircuitOperation(blqs.Block):
    def __init__(self, parent_statement=None, **circuit_op_kwargs):
        super().__init__(parent_statement)
        self._circuit_operation_kwargs = circuit_op_kwargs

    def circuit_operation_kwargs(self):
        return self._circuit_operation_kwargs
