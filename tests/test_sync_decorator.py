import pytest

from src.safe import Failure, Success, safe
from tests.helpers import error_factory_function, error_function, simple_function


def test_without_exceptions():
    decorated = safe(simple_function)
    value = 1

    result = decorated(value)

    assert result == Success(value)


def test_get_origin_function_via_unsafe():
    decorated = safe(simple_function)
    assert decorated.unsafe is simple_function


def test_registered_exceptions():
    decorated = (safe @ KeyError)(simple_function)
    assert set(decorated.registered) == {KeyError}


def test_registered_multiple_exceptions():
    decorated = (safe @ KeyError | ValueError)(simple_function)
    assert set(decorated.registered) == {KeyError, ValueError}


def test_registered_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (safe @ exceptions)(simple_function)
    assert set(decorated.registered) == exceptions


def test_registered_multiple_with_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (safe @ TypeError | exceptions)(simple_function)
    assert set(decorated.registered) == {*exceptions, TypeError}


def test_registered_from_function_exception():
    decorated = (safe @ KeyError)(simple_function)
    use_decorated = (safe @ decorated)(simple_function)
    assert set(use_decorated.registered) == {KeyError}


def test_registered_multiple_from_function_exception():
    decorated = (safe @ KeyError)(simple_function)
    use_decorated = (safe @ TypeError | decorated)(simple_function)
    assert set(use_decorated.registered) == {TypeError, KeyError}


def test_registered_exceptions_duplicate():
    decorated = (safe @ KeyError | KeyError)(simple_function)
    assert list(decorated.registered) == [KeyError]


def test_with_exceptions():
    decorated = (safe @ KeyError)(error_function)
    error = KeyError()

    result = decorated(error)

    assert isinstance(result, Failure)
    assert result.error is error


def test_unregistered_exception():
    decorated = (safe @ KeyError)(error_function)

    with pytest.raises(ValueError, match="test"):
        decorated(ValueError("test"))


def test_error_factory():
    decorated = (safe @ ValueError)(error_factory_function)
    error = ValueError("test")

    result = decorated(error)

    assert isinstance(result, Success)
    assert result.value is error


def test_wraps():
    @safe
    def with_doc_str() -> None:
        """Test doc string"""

    assert with_doc_str.__doc__ == "Test doc string"
