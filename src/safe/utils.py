from collections.abc import Callable, Coroutine, Iterable
from typing import Any, TypeGuard, cast

from .typing import E_co, Failure, Success, T, Wrapper


def is_success(result: Success[T] | Failure[T, E_co], /) -> TypeGuard[Success[T]]:
    """Determine if the result of the call is of the type specified in `return`."""  # noqa: DOC201
    return isinstance(result, Success)


def is_failure(result: Success[T] | Failure[T, E_co], /) -> TypeGuard[Failure[T, E_co]]:
    """Determine if the result of the call is a registered exception from `raises`."""  # noqa: DOC201
    return not is_success(result)


def registered(
    decorated: Callable[..., Success[T] | Failure[T, E_co]]
    | Callable[..., Coroutine[Any, Any, Success[T] | Failure[T, E_co]]]
    | Wrapper,
    /,
) -> Iterable[type[E_co]]:
    """Get registered exceptions types from decorated function.

    Args:
        decorated: decorated function with `@safe` or `@async_safe`

    Returns:
        Iterable[type[E_co]]: registered exceptions types

    """
    if isinstance(decorated, Wrapper):
        return cast(Iterable[type[E_co]], decorated.__registered__)
    return ()


def unsafe(result: Success[T] | Failure[T, Any], /) -> T:
    """Equivalent to result.unsafe."""  # noqa: DOC201
    return result.unsafe


__all__ = ("is_failure", "is_success", "registered", "unsafe")
