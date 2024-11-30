from typing import NoReturn


def simple_function(x: int) -> int:
    return x


def error_factory_function(error: Exception) -> Exception:
    return error


def error_function(error: Exception) -> NoReturn:
    raise error


async def simple_coroutine(x: int) -> int:  # noqa: RUF029
    return x


async def error_factory_coroutine(error: Exception) -> Exception:  # noqa: RUF029
    return error


async def error_coroutine(error: Exception) -> NoReturn:  # noqa: RUF029
    raise error
