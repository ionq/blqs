import inspect
import textwrap

import pytest

import blqs
from blqs import exceptions


def test_generated_code_exception():
    try:
        raise ValueError("oh no")
    except Exception as ex:
        e = blqs.GeneratedCodeException(ex, 3, "filename.py")
        assert e.exception() == ex
    assert e.lineno() == 3
    assert e.filename() == "filename.py"
    assert "3" in str(e)
    assert "filename.py" in str(e)
    assert "exceptions_test" in str(e)


def test_generated_code_exception_no_traceback():
    ex = ValueError("oh noe")
    e = blqs.GeneratedCodeException(ex, 3, "filename.py")
    assert e.exception() == ex
    assert e.lineno() == 3
    assert e.filename() == "filename.py"
    assert "3" in str(e)
    assert "filename.py" in str(e)
    assert "<could not be determined>" in str(e)


def test_generated_code_exception_no_lineno():
    try:
        raise ValueError("oh no")
    except Exception as ex:
        e = blqs.GeneratedCodeException(ex, None, "filename.py")
        assert e.exception() == ex
    assert e.lineno() == None
    assert e.filename() == "filename.py"
    assert "<could not be determined>" in str(e)
    assert "filename.py" in str(e)
    assert "exceptions_test" in str(e)


def test_generated_code_exception_no_filename():
    try:
        raise ValueError("oh no")
    except Exception as ex:
        e = blqs.GeneratedCodeException(ex, 3, None)
        assert e.exception() == ex
    assert e.lineno() == 3
    assert e.filename() == None
    assert "3" in str(e)
    assert "<could not be determined>" in str(e)
    assert "exceptions_test" in str(e)


def test_raise_with_line_mapping():
    def func():
        raise ValueError("oh no")

    try:
        func()
    except Exception as e:
        f = e

    # Make the test robust to where the actual line appears in the test code.
    actual_lineno = inspect.getsourcelines(func)[-1]

    with pytest.raises(ValueError, match="oh no") as et:
        exceptions._raise_with_line_mapping(f, func, {actual_lineno: 1, actual_lineno + 1: 2})
    cause = et.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert cause.exception() == et.value
    assert cause.lineno() == actual_lineno + 1
    assert "exceptions_test" in cause.filename()


def test_raise_with_line_mapping_no_traceback():
    e = ValueError("oh no")

    def func():
        raise e  # coverage: ignore

    with pytest.raises(ValueError, match="oh no") as et:
        exceptions._raise_with_line_mapping(e, func, {1: 1, 2: 2})
    cause = et.value.__cause__
    assert type(cause) == blqs.GeneratedCodeException
    assert cause.exception() == et.value
    assert cause.lineno() == None
    assert "exceptions_test" in cause.filename()
