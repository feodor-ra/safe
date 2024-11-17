'''A library for safely handling function execution results.

Provides the decorators safe and async_safe (for regular functions and coroutines, respectively).

The result of a decorated function is a `Success[T] | Failure[type[Exception]]` value,
allowing you to use a type checker to verify which exception types are expected to be raised
during its execution.

Exception types that are not registered will not be caught and wrapped in Failure; instead,
they will propagate as raised exceptions.

Example:
```
@safe @ KeyError | TypeError
def foo():
    """This function is expected to raise KeyError or TypeError."""
```

You can also pass an already decorated function to copy its registered exception types
and combine them with others:

```
@safe @ foo | ValueError
def bar():
    """
    This function is expected to raise KeyError or TypeError from foo,
    as well as potentially ValueError.
    """
```

'''

from .decorator import async_safe, safe
from .typing import Failure, Success
from .utils import is_failure, is_success

__all__ = ("Failure", "Success", "async_safe", "is_failure", "is_success", "safe")
