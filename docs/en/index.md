# Safe Returns

A decorator for transforming the output type of a function into an [algebraic data type](https://en.wikipedia.org/wiki/Algebraic_data_type), combining it with possible exception types.

---

The main goal of this package is to explicitly define the exception types a function can raise and track them using type checkers.

The package provides two decorators: `@safe` and `@async_safe` for functions and coroutines, respectively.

The decorator offers a convenient mechanism to specify exception types that may occur during function execution. This simplifies writing exception-handling code by leveraging **IDE** hints and type checkers, eliminating the need to examine the implementation of the called function to determine possible exceptions.

## Key Features

- The package supports decorating functions and coroutines.
- The function result is wrapped in a `Success` object to distinguish between an exception and a returned value, such as one from an exception factory.
- Extensive type-specification mechanisms. Using the *or* operator (`|`), akin to `UnionType`, you can list specific types, pass collections constructed at runtime, or use similarly decorated functions.
- The generative typing mechanism does not limit the number of exception types that the type checker can recognize.
- Uses pure Python for typing and does not rely on additional dependencies.

## Requirements

Requires `Python >= 3.11`.

## Installation

Install from PyPI: [safe-returns](https://pypi.org/project/safe-returns/).

=== "pip"

    ```bash
    pip install safe-returns
    ```
=== "poetry"

    ```bash
    poetry add safe-returns
    ```
=== "uv"

    ```bash
    uv add safe-returns
    ```

## Examples

When using pattern matching, you will receive a warning if `KeyError` is not handled.

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
        print("Catch ValueError")
```

For more examples, see [Features](features.md).

## License

This project is distributed under the MIT License.
