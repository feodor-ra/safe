import pytest

from src.safe import Failure, Success, async_safe
from tests.helpers import error_coroutine, error_factory_coroutine, simple_coroutine

pytestmark = pytest.mark.asyncio


async def test_without_exceptions():
    decorated = async_safe(simple_coroutine)
    value = 1

    result = await decorated(value)

    assert result == Success(value)


def test_get_origin_function_via_unsafe():
    decorated = async_safe(simple_coroutine)
    assert decorated.unsafe is simple_coroutine


def test_registered_exceptions():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    assert set(decorated.registered) == {KeyError}


def test_registered_multiple_exceptions():
    decorated = (async_safe @ KeyError | ValueError)(simple_coroutine)
    assert set(decorated.registered) == {KeyError, ValueError}


def test_registered_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (async_safe @ exceptions)(simple_coroutine)
    assert set(decorated.registered) == exceptions


def test_registered_multiple_with_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (async_safe @ TypeError | exceptions)(simple_coroutine)
    assert set(decorated.registered) == {*exceptions, TypeError}


def test_registered_from_function_exception():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    use_decorated = (async_safe @ decorated)(simple_coroutine)
    assert set(use_decorated.registered) == {KeyError}


def test_registered_multiple_from_function_exception():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    use_decorated = (async_safe @ TypeError | decorated)(simple_coroutine)
    assert set(use_decorated.registered) == {TypeError, KeyError}


def test_registered_exceptions_duplicate():
    decorated = (async_safe @ KeyError | KeyError)(simple_coroutine)
    assert list(decorated.registered) == [KeyError]


async def test_with_exceptions():
    decorated = (async_safe @ KeyError)(error_coroutine)
    error = KeyError()

    result = await decorated(error)

    assert isinstance(result, Failure)
    assert result.error is error


async def test_unregistered_exception():
    decorated = (async_safe @ KeyError)(error_coroutine)

    with pytest.raises(ValueError, match="test"):
        await decorated(ValueError("test"))


async def test_error_factory():
    decorated = (async_safe @ ValueError)(error_factory_coroutine)
    error = ValueError("test")

    result = await decorated(error)

    assert isinstance(result, Success)
    assert result.value is error


def test_wraps():
    @async_safe
    async def with_doc_str() -> None:
        """Test doc string"""

    assert with_doc_str.__doc__ == "Test doc string"
