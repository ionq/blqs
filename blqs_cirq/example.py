import cirq
import blqs_cirq as bc
from blqs_cirq import measure, H, HPowGate, rx, CX, qft, Repeat


@bc.build
def program():
    H(0)
    HPowGate(exponent=0.1)(0)
    rx(0.1)(0)

    measure(0, key="a")
    measure(0, 1, key="b")

    qft(0, 1, inverse=True)


def main():
    p = program()
    print(p)


if __name__ == "__main__":
    main()
