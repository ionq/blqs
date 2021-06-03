import blqs_cirq as bc
from blqs_cirq import measure, H, HPowGate, reset, rx, CX, qft


@bc.build
def program():
    H(0)
    HPowGate(exponent=0.1)(0)
    rx(0.1)(0)

    measure(0, key="a")
    measure(0, 1, key="b")

    qft(0, 1, inverse=True)

    with bc.CircuitOperation(repetitions=10):
        H(1)
        CX(0, 1)

    reset(0)


def main():
    p = program()
    print(p)


if __name__ == "__main__":
    main()
