import pytest

import blqs


def test_block_stack():
    assert blqs.get_current_block() == None

    b = blqs.Block.of("b")
    c = blqs.Block.of("c")
    blqs.push_new_block(b)
    blqs.push_new_block(c)
    assert blqs.get_current_block() == c
    blqs.pop_block()
    assert blqs.get_current_block() == b
    blqs.pop_block()


def test_block_pop_stack_empty():
    with pytest.raises(IndexError):
        blqs.pop_block()
