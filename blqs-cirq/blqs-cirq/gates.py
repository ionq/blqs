import blqs
import cirq


class BlqsHPowGate(blqs.Op):
    def __init__(self):
        super().__init__("H")

