import pymore
import pytest

import blqs


def test_program_str():
    assert str(blqs.Program.of("a", "b")) == "a\nb"
    assert str(blqs.Program.of(blqs.Block.of("a"), "b")) == "  a\nb"


def test_program_not_at_top_block_stack():
    with blqs.Block():
        with pytest.raises(AssertionError, match="stack is empty"):
            blqs.Program()
