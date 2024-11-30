from __future__ import annotations

from collections.abc import Callable, Coroutine, Iterable
from functools import update_wrapper
from typing import Any, Generic, Self, overload

from .typing import E_co, Failure, N, P, Success, T


class SafeWrapper(Generic[P, T, E_co]):
    def __init__(self, func: Callable[P, T], decorator: SafeDecorator[E_co]) -> None:
        self._func = func
        self._decorator = decorator
        update_wrapper(self, func)  # type: ignore reportArgumentType

    @property
    def registered(self) -> Iterable[type[E_co]]:
        """Registered exception types that the decorator catches."""
        return self._decorator.registered

    @property
    def unsafe(self) -> Callable[P, T]:
        """The original non-decorated function."""
        return self._func


class SafeSyncWrapper(SafeWrapper[P, T, Any]):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Success[T]:
        return Success(self._func(*args, **kwargs))


class SafeSyncFullWrapper(SafeWrapper[P, T, E_co]):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Success[T] | Failure[T, E_co]:
        try:
            return Success(self._func(*args, **kwargs))
        except self._decorator.registered as exc:
            return Failure(exc)


class SafeAsyncWrapper(SafeWrapper[P, Coroutine[Any, Any, T], Any]):
    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Success[T]:
        return Success(await self._func(*args, **kwargs))


class SafeAsyncFullWrapper(SafeWrapper[P, Coroutine[Any, Any, T], E_co]):
    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Success[T] | Failure[T, E_co]:
        try:
            return Success(await self._func(*args, **kwargs))
        except self._decorator.registered as exc:
            return Failure(exc)


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
    def __matmul__(self, value: SafeWrapper[Any, Any, N], /) -> SafeSyncFullDecorator[N]: ...
    def __matmul__(
        self,
        value: type[N] | Iterable[type[N]] | SafeWrapper[Any, Any, N],
        /,
    ) -> SafeSyncFullDecorator[N]:
        if isinstance(value, Iterable):
            return SafeSyncFullDecorator[N].combine(self, *value)
        if isinstance(value, SafeWrapper):
            return SafeSyncFullDecorator[N].combine(self, *value.registered)
        return SafeSyncFullDecorator[N].combine(self, value)

    def __call__(self, func: Callable[P, T]) -> SafeSyncWrapper[P, T]:
        return SafeSyncWrapper(func, self)


class SafeAsyncDecorator(SafeDecorator[Any]):
    @overload
    def __matmul__(self, value: type[N], /) -> SafeAsyncFullDecorator[N]: ...
    @overload
    def __matmul__(self, value: Iterable[type[N]], /) -> SafeAsyncFullDecorator[N]: ...
    @overload
    def __matmul__(
        self,
        value: SafeWrapper[Any, Any, N],
        /,
    ) -> SafeAsyncFullDecorator[N]: ...
    def __matmul__(
        self,
        value: type[N] | Iterable[type[N]] | SafeWrapper[Any, Any, N],
        /,
    ) -> SafeAsyncFullDecorator[N]:
        if isinstance(value, Iterable):
            return SafeAsyncFullDecorator[N].combine(self, *value)
        if isinstance(value, SafeWrapper):
            return SafeAsyncFullDecorator[N].combine(self, *value.registered)
        return SafeAsyncFullDecorator[N].combine(self, value)

    def __call__(self, func: Callable[P, Coroutine[Any, Any, T]]) -> SafeAsyncWrapper[P, T]:
        return SafeAsyncWrapper(func, self)


class SafeSyncFullDecorator(SafeDecorator[E_co]):
    @overload
    def __or__(self, value: type[N], /) -> SafeSyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(self, value: Iterable[type[N]], /) -> SafeSyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(
        self,
        value: SafeWrapper[Any, Any, N],
        /,
    ) -> SafeSyncFullDecorator[E_co | N]: ...
    def __or__(
        self,
        value: type[N] | Iterable[type[N]] | SafeWrapper[Any, Any, N],
        /,
    ) -> SafeSyncFullDecorator[E_co | N]:
        if isinstance(value, Iterable):
            return self.combine(self, *value)
        if isinstance(value, SafeWrapper):
            return self.combine(self, *value.registered)
        return self.combine(self, value)

    def __call__(self, func: Callable[P, T]) -> SafeSyncFullWrapper[P, T, E_co]:
        return SafeSyncFullWrapper(func, self)


class SafeAsyncFullDecorator(SafeDecorator[E_co]):
    @overload
    def __or__(self, value: type[N], /) -> SafeAsyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(self, value: Iterable[type[N]], /) -> SafeAsyncFullDecorator[E_co | N]: ...
    @overload
    def __or__(self, value: SafeWrapper[Any, Any, N], /) -> SafeAsyncFullDecorator[E_co | N]: ...
    def __or__(
        self,
        value: type[N] | Iterable[type[N]] | SafeWrapper[Any, Any, N],
        /,
    ) -> SafeAsyncFullDecorator[E_co | N]:
        if isinstance(value, Iterable):
            return self.combine(self, *value)
        if isinstance(value, SafeWrapper):
            return self.combine(self, *value.registered)
        return self.combine(self, value)

    def __call__(
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
    ) -> SafeAsyncFullWrapper[P, T, E_co]:
        return SafeAsyncFullWrapper(func, self)


safe = SafeSyncDecorator([])
async_safe = SafeAsyncDecorator([])


__all__ = ("async_safe", "safe")
