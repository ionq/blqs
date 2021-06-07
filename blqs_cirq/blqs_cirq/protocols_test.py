# Copyright 2021 The Blqs Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
import blqs_cirq as bc


def test_decode():
    class Decoder(bc.SupportsDecoding):
        def _decode_(self, val: int) -> str:
            return str(val)

    decoder = Decoder()
    assert bc.decode(decoder, 1) == "1"
    assert bc.decode(decoder, 10) == "10"
    assert bc.decode(decoder, 10, default=11) == "10"


def test_decode_not_implemented():
    class DecoderNotImplemented(bc.SupportsDecoding):
        def _decode_(self, val: int) -> str:
            return NotImplemented

    decoder = DecoderNotImplemented()
    assert bc.decode(decoder, 1, "10") == "10"
    with pytest.raises(NotImplementedError, match="_decode_"):
        _ = bc.decode(decoder, 1)


def test_decode_no_decode_method():
    class DecoderWithNoDecode:
        pass

    decoder = DecoderWithNoDecode()
    assert bc.decode(decoder, 10, default="11") == "11"
    with pytest.raises(NotImplementedError, match="_decode_"):
        _ = bc.decode(decoder, 10)
