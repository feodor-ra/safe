from typing import Any

import pytest

from src.safe import Failure, Success, is_failure, is_success, registered, safe, unsafe
from tests.helpers import error_function, simple_function


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Success[Any](1), True),
        (Failure[Any, Exception](Exception()), False),
    ],
)
def test_is_success(value: Success[Any] | Failure[Any, Exception], expected: bool):
    assert is_success(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Success[Any](1), False),
        (Failure[Any, Exception](Exception()), True),
    ],
)
def test_is_failure(value: Success[Any] | Failure[Any, Exception], expected: bool):
    assert is_failure(value) is expected


def test_registered_from_decorated():
    decorated = (safe @ KeyError)(simple_function)
    assert list(registered(decorated)) == [KeyError]


def test_registered_from_same():
    def func() -> Success[int] | Failure[int, KeyError]:
        return Success(1)

    assert list(registered(func)) == []


def test_unsafe():
    decorated = safe(simple_function)
    value = 10

    result = decorated(value)

    assert unsafe(result) == value


def test_unsafe_error():
    decorated = (safe @ Exception)(error_function)

    result = decorated(Exception("test"))

    with pytest.raises(Exception, match="test"):
        unsafe(result)
