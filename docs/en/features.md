# Features

## Basic Usage

```python
from safe import safe

@safe @ ValueError
def foo(a: int) -> str:
    if a < 0:
        raise ValueError
    return f"Hello {a} times"
```

The entry point is the `@safe` decorator, where the exception types that may occur should be specified after the `@`.

The resulting function will have the following type:

```python
foo(42) # -> Success[str] | Failure[str, ValueError]
```

Subsequent work with the function result involves type refinement:

```python
from safe import Success, Failure

if isinstance(result := foo(42), Success):
    print(result.value)
else:
    print("We encountered an error!", result.error)
```

## Specifying Exceptions

The specified exceptions will be guaranteed to be caught, including their subclasses. However, exceptions that are not specified will not be caught and will propagate upwards:

```python
from safe import safe

@safe @ TypeError
def foo():
    raise ValueError

try:
    result = foo()
except ValueError:
    print("Caught an unregistered exception")
```

The concept here is simple: anything not explicitly specified by the developer as expected is treated as unexpected behavior. Such exceptions are considered program errors that should either terminate the program or be caught at a high level if further execution is possible.

### Without Specification

The decorator can be used without specifying exception types. In this case, it will only wrap results in the `Success` data class.

This ensures consistency in the code approach.

```python
from safe import safe

@safe
def foo() -> float:
    return 3.22

foo() # -> Success[float]
```

### Specifying Multiple Types

#### Using Pipe (`|`)

Exception types can be explicitly specified using the *or* operator `|`.

```python
from safe import safe

@safe @ KeyError | ValueError
def foo() -> int: ...
```

#### Using a Collection

You can also specify exception types by passing an iterable, provided its types are analyzable by the type checker.

```python
from safe import safe

exc_types = (KeyError, ValueError, TypeError)

@safe @ exc_types
def foo() -> int: ...
```

#### Using a Decorated Function

You can also specify another function that has been decorated with `@safe`.

```python
from safe import safe

@safe @ KeyError
def foo() -> int: ...

@safe @ foo
def bar() -> float: ...
```

#### Combining Them All

Using *or* `|`, you can combine all of these approaches, passing any number of iterables, explicit types, and other functions.

```python
from safe import safe

exc_types = (ValueError, TypeError)

@safe @ KeyError | exc_types
def foo() -> int: ...

@safe @ foo | IndexError
def bar() -> int: ...

@safe @ foo | bar | (AssertionError, ) | ArithmeticError
def zoo() -> int: ...
```

If types are repeated in the combination, the type checker will correctly recognize only one instance.

## Working with Results

### Unsafe Usage

Both `Success` and `Failure` have a property `unsafe`, which is typed as the function's `returns_type`. However, calling it on a `Failure` will raise the captured exception.

This can be used when one safe function calls another and does not handle its exceptions, leaving this responsibility to higher-level code.

```python
from safe import safe

@safe @ ValueError
def foo(a: int) -> str:
    if a < 0:
        raise ValueError
    return f"It's {a}"


@safe @ foo
def bar(a: int) -> list[str]:
    return [foo(a).unsafe]
```

### Retrieving the Original Function

If you need to get the original function without the safe-catching mechanism, you can access it through the `unsafe` property.

```python
from safe import safe

@safe @ KeyError
def foo(a: int) -> tuple[int, int]: ...


foo         # (int) -> Success[tuple[int, int]] | Failure[int, KeyError]
foo.unsafe  # (int) -> tuple[int, int]

foo.unsafe(5)
```

### Utilities `is_success` and `is_failure`

The library provides `is_success` and `is_failure` utilities for convenience and to avoid repeated checks.

```python
if isinstance(result := foo(5), Success):
    ...


from safe import is_success, is_failure

if is_success(result := foo(5)):
    ...
else:
    ...

if is_failure(result := foo(0)):
    ...
else:
    ...
```

These utilities serve as `TypeGuard` checks for `isinstance`.

### Pattern Matching

The full potential of this approach is revealed when used in conjunction with the `match case` [construct](https://peps.python.org/pep-0636/):

```python
from safe import safe, Success, Failure

@safe @ ValueError | KeyError
def foo() -> int | str: ...


match foo():
    case Success(value=int()):
        print("It's int")
    case Success(value=str()):
        print("It's str")
    case Failure(error=ValueError()):
        print("Caught ValueError")
```

From the code, it is evident that the `KeyError` exception is not handled, and this will be detected by the type checker ([pyright](https://github.com/microsoft/pyright) or [mypy](https://github.com/python/mypy)), flagging it with a `reportMatchNotExhaustive` error.

You can resolve this by adding its handling or propagating it upwards:

```python
match foo():
    case Success(value=int() as value):
        print(f"It's int {value=}")
    case Success(value=str() as value):
        print(f"It's str {value=}")
    case Failure(error=ValueError()):
        print("Caught ValueError")
    case Failure(error as error):
        raise error
```

## Asynchronous Support

To decorate coroutines, use the separate `@async_safe` decorator.

```python
from safe import async_safe


@async_safe @ ValueError
async def foo(a: int) -> str: ...


foo # (int) -> Coroutine[Any, Any, Success[str] | Failure[str, ValueError]]
```
