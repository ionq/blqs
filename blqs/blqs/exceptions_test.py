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
import inspect

import pytest

import blqs
from blqs import exceptions


def test_generated_code_exception():
    e = blqs.GeneratedCodeException({1: 3, 5: 4}, "original.py", "generated.py")

    assert e.linenos_dict() == {1: 3, 5: 4}
    assert e.original_filename() == "original.py"
    assert e.generated_filename() == "generated.py"
    assert "1 -> 3" in str(e)
    assert "5 -> 4" in str(e)
    assert "generated.py -> original.py" in str(e)


def test_generated_code_exception_no_linenos_dict():
    e = blqs.GeneratedCodeException({}, "original.py", "generated.py")
    assert "<could not be determined>" in str(e)
    assert "generated.py -> original.py" in str(e)


def test_generated_code_exception_no_filename():
    e = blqs.GeneratedCodeException({1: 3, 5: 4}, None, "generated.py")
    assert "1 -> 3" in str(e)
    assert "5 -> 4" in str(e)
    assert "generated.py -> <could not be determined>" in str(e)


def test_raise_with_line_mapping():
    def func():
        raise ValueError("oh no")

    try:
        func()
    except Exception as e:
        f = e

    # Make the test robust to where the actual line appears in the test code.
    actual_lineno = inspect.getsourcelines(func)[-1]
    actual_filename = inspect.getsourcefile(func)

    with pytest.raises(ValueError, match="oh no") as et:
        exceptions._raise_with_line_mapping(
            f, func, {actual_lineno: 1, actual_lineno + 1: 2}, actual_filename
        )
    cause = et.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert cause.linenos_dict() == {actual_lineno + 1: actual_lineno + 1}

    # Same because there is no generated code in test.
    assert "exceptions_test" in cause.original_filename()
    assert "exceptions_test" in cause.generated_filename()


def test_raise_with_line_mapping_no_traceback():
    e = ValueError("oh no")

    def func():
        raise e  # coverage: ignore

    actual_lineno = inspect.getsourcelines(func)[-1]
    actual_filename = inspect.getsourcefile(func)

    with pytest.raises(ValueError, match="oh no") as et:
        exceptions._raise_with_line_mapping(
            e, func, {actual_lineno: 1, actual_lineno + 1: 2}, actual_filename
        )
    cause = et.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert len(cause.linenos_dict()) == 0


def test_raise_with_line_mapping_deeper_traceback():
    def func():
        def inner_func():
            raise ValueError("oh no")

        inner_func()

    try:
        func()
    except Exception as e:
        f = e

    # Make the test robust to where the actual line appears in the test code.
    actual_lineno = inspect.getsourcelines(func)[-1]
    actual_filename = inspect.getsourcefile(func)

    with pytest.raises(ValueError, match="oh no") as et:
        exceptions._raise_with_line_mapping(
            f, func, {actual_lineno + i: i + 1 for i in range(10)}, actual_filename
        )
    cause = et.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    # Traceback is at inner_func, call to inner_func, and func call.
    assert cause.linenos_dict() == {
        actual_lineno + 2: actual_lineno + 2,
        actual_lineno + 4: actual_lineno + 4,
        actual_lineno + 7: actual_lineno + 7,
    }
