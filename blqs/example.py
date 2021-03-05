import blqs
import gast

H = blqs.Operand("H")
CX = blqs.Operand("CX")
M = blqs.Operand("M")


@blqs.build
def example():
    H(1)
    H(0)
    CX(0, 1)

    sub_block()

    M(1, blqs.Register("a"))
    if blqs.Register("a"):
        H(0)
    else:
        H(1)
    val = False
    if val:
        H(3)
    else:
        H(2)

    for b in blqs.Iterable("range(4)", blqs.Register("b")):
        H(b)
    for i in range(4):
        H(i)

    M(1, blqs.Register("a"))
    while blqs.Register("a"):
        print("here")
        M(1, blqs.Register("a"))
        H(1)
    i = 0
    # while i < 5:
    #     print(i)
    #     i += 2


@blqs.build
def sub_block():
    H(0)
    CX(3, 2)


def main():
    # Cirq and qiskit style.
    b = blqs.Program()
    b.append(H(1))
    b.extend([H(0), CX(0, 1)])

    c = blqs.Block()
    c.extend([H(0), CX(3, 2)])
    b.append(c)

    a = blqs.Register("a")
    b.append(M(1, a))

    d = blqs.If(a)
    d.if_block().append(H(0))
    d.else_block().append(H(1))
    b.append(d)

    val = True
    if val:
        b.append(H(3))
    else:
        b.append(H(2))
    print(f"----\n{b}\n----\n")

    # Tensorflow graph style.
    with blqs.Program() as p:
        H(1)
        H(0)
        CX(0, 1)
        with blqs.Block():
            H(0)
            CX(3, 2)
        a = blqs.Register("a")
        M(1, a)
        cond = blqs.If(a)
        with cond.if_block():
            H(0)
        with cond.else_block():
            H(1)
        val = True
        if val:
            H(3)
        else:
            H(2)

    print(f"----\n{p}\n----\n")

    # Autograph style.
    q = example()
    print(f"----\n{q}\n----\n")


if __name__ == "__main__":
    main()