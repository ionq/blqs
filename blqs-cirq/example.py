import blqs-cirq as bc

@bc.build
def program():
    q = cirq.LineQubit(0)
    bc.H(q)


def main():
    p = program()
    print(p)

if __name__ == "__main__":
    main()
