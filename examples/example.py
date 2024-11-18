from typing import reveal_type as reveal_type

from safe import Failure, Success, safe

# === Как использовать декоратор


# Сделает вывод в Success, но ошибки не будут перехватываться
@safe
def function_1(a: str) -> str:
    return a + a


function_1("hello")
# function_1('hello') -> Success[str]


# Так будет перехватывать ValueError
@safe @ ValueError
def function_2(b: int) -> int:
    if b < 0:
        raise ValueError
    return b + b


function_2(10)
# function_2(10) -> Success[int] | Failure[int, ValueError]


# Можно задавать несколько ошибок через pipe
# И перехватываться ValueError или TypeError
@safe @ ValueError | TypeError
def function_3(c: int) -> int:
    if not isinstance(c, int):
        raise TypeError
    return function_2.unsafe(c)


function_3(10)
# function_3(10) -> Success[int] | Failure[int, ValueError | TypeError]


# Можно задать ошибки как Iterable и потом объединить с другими ошибок через pipe
function_4_errors = (ValueError, TypeError)


@safe @ function_4_errors | AssertionError
def function_4(d: int) -> int:
    assert d != 42
    return function_3.unsafe(d)


function_4(43)
# function_4(43) -> Success[int] | Failure[int, ValueError | TypeError | AssertionError]


# Так же можно указать safe-функцию и будет скопированы ее ошибки (или несколько через pipe)
@safe @ function_4 | KeyError
def function_5(f: int) -> int:
    if f % 100 == 0 and f:
        raise KeyError
    return function_4.unsafe(f)


function_5(101)
# function_5(101) -> Success[int] | Failure[int, ValueError | TypeError | AssertionError | KeyError]


# === Как работать с такими функциями


# можно получить доступ к оригинальной функции через .unsafe
function_5.unsafe(102)
# function_5.unsafe(102) -> int


# так же можно работать не безлопастно с результатом (в таком случае если была ошибка она поднимится)
value_5 = function_5(103).unsafe
# value_5 is int


# можно использовать pattern matching
# pyright будется сейчас ругатся так как KeyError не обрабатывается
match function_5(104):
    case Success(value):
        print(value)  # int
    case Failure(error=ValueError() as exc):
        ...
    case Failure(error=TypeError() as exc):
        ...
    case Failure(error=AssertionError() as exc):
        ...


# можно получить типы ошибок которые перехватываются
assert set(function_5.registered) == {ValueError, TypeError, AssertionError, KeyError}
