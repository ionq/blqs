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
        a = M(1, "a")
        with blqs.IfBlock(a) as d:
            H(0)
        with d.else_if_block(a) as e:
            H(0)
            H(1)
        with e.else_block():
            H(1)

    print(b)


if __name__ == "__main__":
    main()
