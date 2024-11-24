# safe-returns

A decorator for converting the output type of a function into an algebraic data type,
representing the function’s result and its possible exception types.
This helps in tracking exception types and improves type-checker hints.

## Install

[pypi](https://pypi.org/project/safe-returns/)

```bash
pip install safe-returns
```

## Uses

```python
from safe import safe, Success, Failure

@safe @ ValueError | KeyError
def foo() -> int | str: ...


match foo():
    case Success(value=int() as number):
        print(f"It's int {number=}")
    case Success(value=str() as string):
        print(f"It's str {string=}")
    case Failure(error=ValueError()):
        print("Catch ValueError")
    # reportMatchNotExhaustive warning – KeyError are not handled
```

## Documentation

- [home](https://feodor-ra.github.io/safe-returns/)
- [features](https://feodor-ra.github.io/safe-returns/features/)
