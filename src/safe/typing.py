from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeAlias, TypeVar

T = TypeVar("T")
E_co = TypeVar("E_co", bound=Exception, covariant=True)


class Unsafe(ABC, Generic[T]):
    @property
    @abstractmethod
    def unsafe(self) -> T:
        """Unsafely retrieve the function result.

        if the result is positive, return the value from return;
        otherwise, raise any of the registered exceptions.
        """


@dataclass(frozen=True, slots=True)
class Success(Unsafe[T]):
    """Wrap the result of the function call for a positive outcome."""

    value: T

    @property
    def unsafe(self) -> T:  # noqa: D102
        return self.value


@dataclass(frozen=True, slots=True)
class Failure(Unsafe[T], Generic[T, E_co]):
    """Wrap the registered exception from the function call."""

    error: E_co

    @property
    def unsafe(self) -> T:  # noqa: D102
        raise self.error


P = ParamSpec("P")
N = TypeVar("N", bound=Exception)
R: TypeAlias = Success[T] | Failure[T, E_co]


__all__ = ("Failure", "Success")
