import blqs


def test_statement_in_block():

    with blqs.Block() as b:
        s1 = blqs.Statement()
        s2 = blqs.Statement()

    expected = blqs.Block()
    expected.extend([s1, s2])
    assert b == expected


def test_statement_in_nested_block():
    with blqs.Block() as b:
        with blqs.Block() as c:
            s1 = blqs.Statement()
            s2 = blqs.Statement()
        s3 = blqs.Statement()

    expected = blqs.Block()
    expected.extend([s1, s2])
    assert c == expected

    expected = blqs.Block()
    expected.append(c)
    expected.append(s3)
    assert b == expected


def test_statement_no_default_block():
    s1 = blqs.Statement()
    with blqs.Block() as b:
        pass
    s2 = blqs.Statement()

    assert s1 not in b
    assert s2 not in b
