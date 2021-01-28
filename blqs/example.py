import blqs

H = blqs.Operand("H")
CX = blqs.Operand("CX")
M = blqs.Operand("M")


def main():

    with blqs.Block() as b:
        H(1)
        H(0)
        CX(0, 1)
        with blqs.Block() as c:
            H(3)
            CX(3, 2)
        M(1, "a")
    print(b)


if __name__ == "__main__":
    main()
