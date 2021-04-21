import cirq
import blqs_cirq as bc
from blqs_cirq import H, HPowGate


@bc.build
def program():
    q = cirq.LineQubit(0)
    H(q)
    HPowGate(exponent=0.1)(q)


def main():
    p = program()
    print(p)


if __name__ == "__main__":
    main()
