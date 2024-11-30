from __future__ import annotations

from collections.abc import Callable, Coroutine, Iterable
from functools import wraps
from typing import Any, Generic, Self, cast, overload

from .typing import E_co, Failure, N, P, Success, T, Wrapper


class SafeDecorator(Generic[E_co]):
    def __init__(self, exceptions: Iterable[type[E_co]]) -> None:
        self._registered: set[type[E_co]] = set(exceptions)

    @classmethod
    def combine(cls, base: SafeDecorator[E_co], *exc_types: type[N]) -> Self:
        return cls((*base.registered, *exc_types))  # type: ignore reportArgumentType

    @property
    def registered(self) -> tuple[type[E_co], ...]:
        return tuple(self._registered)


class SafeSyncDecorator(SafeDecorator[Any]):
    @overload
    def __matmul__(self, value: type[N], /) -> SafeSyncFullDecorator[N]: ...
    @overload
    def __matmul__(self, value: Iterable[type[N]], /) -> SafeSyncFullDecorator[N]: ...
    @overload
    def __matmul__(
        self,
        value: Callable[..., Success[Any] | Failure[Any, N]],
        /,
    ) -> SafeSyncFullDecorator[N]: ...
    @overload
    def __matmul__(
        self,
        value: Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeSyncFullDecorator[N]: ...
    def __matmul__(
        self,
        value: type[N]
        | Iterable[type[N]]
        | Callable[..., Success[Any] | Failure[Any, N]]
        | Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeSyncFullDecorator[N]:
        if isinstance(value, type) and issubclass(value, Exception):
            return SafeSyncFullDecorator[N].combine(self, value)
        if isinstance(value, Iterable):
            return SafeSyncFullDecorator[N].combine(self, *value)
        if isinstance(value, Wrapper):
            return SafeSyncFullDecorator[N].combine(self, *value.__registered__)
        return cast(SafeSyncFullDecorator[N], self)

    def __call__(self, func: Callable[P, T]) -> Callable[P, Success[T]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Success[T]:
            return Success(func(*args, **kwargs))

        wrapper.__registered__ = self.registered  # type: ignore reportFunctionMemberAccess

        return wraps(func)(wrapper)


class SafeAsyncDecorator(SafeDecorator[Any]):
    @overload
    def __matmul__(self, value: type[N], /) -> SafeAsyncFullDecorator[N]: ...
    @overload
    def __matmul__(self, value: Iterable[type[N]], /) -> SafeAsyncFullDecorator[N]: ...
    @overload
    def __matmul__(
        self,
        value: Callable[..., Success[Any] | Failure[Any, N]],
        /,
    ) -> SafeAsyncFullDecorator[N]: ...
    @overload
    def __matmul__(
        self,
        value: Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeAsyncFullDecorator[N]: ...
    def __matmul__(
        self,
        value: type[N]
        | Iterable[type[N]]
        | Callable[..., Success[Any] | Failure[Any, N]]
        | Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeAsyncFullDecorator[N]:
        if isinstance(value, type) and issubclass(value, Exception):
            return SafeAsyncFullDecorator[N].combine(self, value)
        if isinstance(value, Iterable):
            return SafeAsyncFullDecorator[N].combine(self, *value)
        if isinstance(value, Wrapper):
            return SafeAsyncFullDecorator[N].combine(self, *value.__registered__)
        return cast(SafeAsyncFullDecorator[N], self)

    def __call__(
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
    ) -> Callable[P, Coroutine[Any, Any, Success[T]]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Success[T]:
            return Success(await func(*args, **kwargs))

        wrapper.__registered__ = self.registered  # type: ignore reportFunctionMemberAccess

        return wraps(func)(wrapper)


class SafeSyncFullDecorator(SafeDecorator[E_co]):
    @overload
    def __or__(self, value: type[N], /) -> SafeSyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(self, value: Iterable[type[N]], /) -> SafeSyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(
        self,
        value: Callable[..., Success[Any] | Failure[Any, N]],
        /,
    ) -> SafeSyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(
        self,
        value: Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeSyncFullDecorator[E_co | N]: ...
    def __or__(
        self,
        value: type[N]
        | Iterable[type[N]]
        | Callable[..., Success[Any] | Failure[Any, N]]
        | Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeSyncFullDecorator[E_co | N]:
        if isinstance(value, type) and issubclass(value, Exception):
            return self.combine(self, value)
        if isinstance(value, Iterable):
            return self.combine(self, *value)
        if isinstance(value, Wrapper):
            return self.combine(self, *value.__registered__)
        return self

    def __call__(self, func: Callable[P, T]) -> Callable[P, Success[T] | Failure[T, E_co]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Success[T] | Failure[T, E_co]:
            try:
                return Success(func(*args, **kwargs))
            except self.registered as exc:
                return Failure(exc)

        wrapper.__registered__ = self.registered  # type: ignore reportFunctionMemberAccess
        return wraps(func)(wrapper)


class SafeAsyncFullDecorator(SafeDecorator[E_co]):
    @overload
    def __or__(self, value: type[N], /) -> SafeAsyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(self, value: Iterable[type[N]], /) -> SafeAsyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(
        self,
        value: Callable[..., Success[Any] | Failure[Any, N]],
        /,
    ) -> SafeAsyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(
        self,
        value: Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeAsyncFullDecorator[E_co | N]: ...
    def __or__(
        self,
        value: type[N]
        | Iterable[type[N]]
        | Callable[..., Success[Any] | Failure[Any, N]]
        | Callable[..., Coroutine[Any, Any, Success[Any] | Failure[Any, N]]],
        /,
    ) -> SafeAsyncFullDecorator[E_co | N]:
        if isinstance(value, type) and issubclass(value, Exception):
            return self.combine(self, value)
        if isinstance(value, Iterable):
            return self.combine(self, *value)
        if isinstance(value, Wrapper):
            return self.combine(self, *value.__registered__)
        return self

    def __call__(
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
    ) -> Callable[P, Coroutine[Any, Any, Success[T] | Failure[T, E_co]]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Success[T] | Failure[T, E_co]:
            try:
                return Success(await func(*args, **kwargs))
            except self.registered as exc:
                return Failure(exc)

        wrapper.__registered__ = self.registered  # type: ignore reportFunctionMemberAccess
        return wraps(func)(wrapper)


safe = SafeSyncDecorator([])
async_safe = SafeAsyncDecorator([])


__all__ = ("async_safe", "safe")
