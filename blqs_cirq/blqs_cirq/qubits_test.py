import pytest

import cirq
import blqs_cirq as bc


@pytest.mark.parametrize(
    "qubit",
    (
        cirq.LineQubit(0),
        cirq.NamedQubit("a"),
        cirq.LineQid(0, 3),
        cirq.NamedQid("d", 3),
        cirq.GridQubit(2, 3),
    ),
)
def test_default_qubit_decoder_qid(qubit):
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, qubit) == qubit


def test_default_qubit_decoder_int():
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, 0) == cirq.LineQubit(0)
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, 3) == cirq.LineQubit(3)


def test_default_qubit_decoder_str():
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, "a") == cirq.NamedQubit("a")
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, "bcd") == cirq.NamedQubit("bcd")


def test_default_qubit_decoder_list_tuple():
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, (0, 1)) == cirq.GridQubit(0, 1)
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, (2, 3)) == cirq.GridQubit(2, 3)
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, [0, 1]) == cirq.GridQubit(0, 1)
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, [2, 3]) == cirq.GridQubit(2, 3)


def test_default_qubit_decoder_fallthru():
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, (0, 1, 2)) == cirq.NamedQubit("(0, 1, 2)")
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, (0, "a")) == cirq.NamedQubit("(0, 'a')")
    assert bc.decode(bc.DEFAULT_QUBIT_DECODER, 1.0) == cirq.NamedQubit("1.0")
