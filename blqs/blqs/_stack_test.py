import threading

import pytest

from blqs import _stack


def test_stack():
    stack = _stack.ThreadLocalStack()
    stack.push(0)
    stack.push("1")
    assert stack.peek() == "1"
    assert stack.pop() == "1"
    assert stack.pop() == 0
    with pytest.raises(IndexError, match="empty stack"):
        stack.pop()


def test_stack_thread_local():
    stack = _stack.ThreadLocalStack()
    stack.push(0)
    assert stack.peek() == 0

    def f():
        assert stack.peek() != 0
        stack.push(1)
        assert stack.peek() == 1

    t1 = threading.Thread(target=f)
    t1.start()
    t1.join()

    assert stack.peek() == 0
