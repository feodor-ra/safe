from typing import TypeGuard

from .typing import E_co, Failure, Success, T


def is_success(result: Success[T] | Failure[T, E_co], /) -> TypeGuard[Success[T]]:
    """Determine if the result of the call is of the type specified in `return`."""  # noqa: DOC201
    return isinstance(result, Success)


def is_failure(result: Success[T] | Failure[T, E_co], /) -> TypeGuard[Failure[T, E_co]]:
    """Determine if the result of the call is a registered exception from `raises`."""  # noqa: DOC201
    return not is_success(result)


__all__ = ("is_failure", "is_success")
