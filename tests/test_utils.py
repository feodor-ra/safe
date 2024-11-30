from typing import Any

import pytest

from src.safe import Failure, Success, is_failure, is_success


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
