from typing import Any

import pytest

from src.safe import Failure, Success


def test_unsafe_get_from_success():
    value = "test"
    result = Success(value)
    assert result.unsafe == value


def test_unsafe_get_from_failure():
    message = "test"
    exc = Exception(message)
    result = Failure[Any, Exception](exc)

    with pytest.raises(type(exc), match=message):
        result.unsafe  # noqa: B018
