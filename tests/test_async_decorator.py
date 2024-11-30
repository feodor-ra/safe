import pytest

from src.safe import Failure, Success, async_safe, registered
from tests.helpers import error_coroutine, error_factory_coroutine, simple_coroutine


@pytest.mark.asyncio
async def test_without_exceptions():
    decorated = async_safe(simple_coroutine)
    value = 1

    result = await decorated(value)

    assert result == Success(value)


def test_registered_exceptions():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    assert set(registered(decorated)) == {KeyError}


def test_registered_not_supported():
    decorated = (async_safe @ 1)(simple_coroutine)  # type: ignore reportOperatorIssue
    assert not registered(decorated)  # type: ignore reportUnknownArgumentType


def test_registered_multiple_exceptions():
    decorated = (async_safe @ KeyError | ValueError)(simple_coroutine)
    assert set(registered(decorated)) == {KeyError, ValueError}


def test_registered_not_supported_multiple():
    decorated = (async_safe @ KeyError | 1)(simple_coroutine)  # type: ignore reportOperatorIssue
    assert set(registered(decorated)) == {KeyError}  # type: ignore reportUnknownArgumentType


def test_registered_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (async_safe @ exceptions)(simple_coroutine)
    assert set(registered(decorated)) == exceptions


def test_registered_multiple_with_collection_exceptions():
    exceptions = {KeyError, ValueError}
    decorated = (async_safe @ TypeError | exceptions)(simple_coroutine)
    assert set(registered(decorated)) == {*exceptions, TypeError}


def test_registered_from_function_exception():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    use_decorated = (async_safe @ decorated)(simple_coroutine)
    assert set(registered(use_decorated)) == {KeyError}


def test_registered_multiple_from_function_exception():
    decorated = (async_safe @ KeyError)(simple_coroutine)
    use_decorated = (async_safe @ TypeError | decorated)(simple_coroutine)
    assert set(registered(use_decorated)) == {TypeError, KeyError}


def test_registered_exceptions_duplicate():
    decorated = (async_safe @ KeyError | KeyError)(simple_coroutine)
    assert list(registered(decorated)) == [KeyError]


@pytest.mark.asyncio
async def test_with_exceptions():
    decorated = (async_safe @ KeyError)(error_coroutine)
    error = KeyError()

    result = await decorated(error)

    assert isinstance(result, Failure)
    assert result.error is error


@pytest.mark.asyncio
async def test_unregistered_exception():
    decorated = (async_safe @ KeyError)(error_coroutine)

    with pytest.raises(ValueError, match="test"):
        await decorated(ValueError("test"))


@pytest.mark.asyncio
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
