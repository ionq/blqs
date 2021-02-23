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
    m = M(1, "a")
    m.has_value = True
    if m:
        H(0)
    else:
        H(1)


@blqs.build
def sub_block():
    H(0)
    CX(3, 2)


def main():
    # Cirq and qiskit style.
    b = blqs.Block()
    b.append(H(1))
    b.extend([H(0), CX(0, 1)])

    c = blqs.Block()
    c.append(H(0))
    c.append(CX(3, 2))
    b.append(c)

    b.append(M(1, "a"))

    d = blqs.If("a")
    d.if_block().append(H(0))
    d.else_block().append(H(1))
    b.append(d)
    print(f"----\n{b}\n----\n")

    # Tensorflow graph style.
    with blqs.Block() as p:
        H(1)
        H(0)
        CX(0, 1)
        with blqs.Block():
            H(0)
            CX(3, 2)
        M(1, "a")
        cond = blqs.If("a")
        with cond.if_block():
            H(0)
        with cond.else_block():
            H(1)
    print(f"----\n{p}\n----\n")

    # Autograph style.
    q = example()
    print(f"----\n{q}\n----\n")


if __name__ == "__main__":
    main()
