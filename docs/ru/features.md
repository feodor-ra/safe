# Возможности

## Базовое использование

```python
from safe import safe

@safe @ ValueError
def foo(a: int) -> str:
    if a < 0:
        raise ValueError
    return f"Hello {a} times"
```

Точка входа – декоратора `@safe`, для указания типов исключений которые могут поражаться,
их нужно указать после `@`.

Результатом будет функция со следующий типизацией:

```python
foo(42) # -> Success[str] | Failure[str, ValueError]
```

Предполагается дальнеишая работа с результатом функции через уточнение типа:

```python
from safe import Success, Failure

if isinstance(result := foo(42), Success):
    print(result.value)
else:
    print("We has error!", result.error)
```

## Указание исключений

Указанные исключения будут гарантированно перехвачены. Они сами или их потомки.
Однако, типы исключений которые не указаны будут перехвачены не будут и будут пропущены выше:

```python
from safe import safe

@safe @ TypeError
def foo():
    raise ValueError

try:
    result = foo()
except ValueError:
    print("Catch unregistered exception")
```

Концепция тут проста – все что разработчик не указывает как что-то ожидаемое – таковым и
является, и такого рода исключения это непредвиденно поведение программы, которые должно либо
приводить к ее завершению, либо перехватываться на высоком уровне и подавляться если дальнеишая
работа программы возможна исходя из ошибки.

### Без указания

Декоратор можно использовать без указания типов исключений – в таком случае будет только
обертка результатов в датакласс `Success`.

Нужно это для поддержания консистентности подхода в коде.

```python
from safe import safe

@safe
def foo() -> float:
    return 3.22

foo() # -> Success[float]
```

### Множественное указание типов

#### Через пайп

Типы можно указывать явно через оператор *или* `|`.

```python
from safe import safe

@safe @ KeyError | ValueError
def foo() -> int: ...
```

#### Через передачу коллекции

Так же можно указывать передавая Iterable тип, важно что бы его типы мог вычислить тайп-чекер.

```python
from safe import safe

exc_types = (KeyError, ValueError, TypeError)

@safe @ exc_types
def foo() -> int: ...
```

#### Через передачу функции

И так же указывая задекорированную декоратором `@safe` другую функцию.

```python
from safe import safe

@safe @ KeyError
def foo() -> int: ...

@safe @ foo
def bar() -> float: ...
```

#### Комбинируя это все вместе

Используя *или* `|` можно все это скомбинировать передавая любое количество `Iterable` коллекций,
явных типов и других функций.

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

Причем если в комбинации будут повторятся типы, типизация будет работать корректно и учитывать
только один из них.

## Работа с результатом

### Не безопасное использование

У `Success` и `Failure` есть *property* `unsafe` – которое типизировано в обоих случаях,
как `returns_type` функции, однако при вызове у последнего поднимает перехваченную ошибку.

Пример применения – это если одна безопасная функция вызывается в другой, которая не обрабатывает ее исключений
и отдает эту обязанность вышестоящему коду.

```python
from sage import safe

@safe @ ValueError
def foo(a: int) -> str:
    if a < 0:
        raise ValueError
    return f"It's {a}"


@safe @ foo
def bar(a: int) -> list[str]:
    return [foo(a).unsafe]
```

### Получение оригинала функции

Если есть необходимость получить оригинальную функцию, без механизма безлопастного перехвата,
у функции можно вызвать *property* `unsafe`

```python
from safe import safe

@safe @ KeyError
def foo(a: int) -> tuple[int, int]: ...


foo         # (int) -> Success[tuple[int, int]] | Failure[int, KeyError]
foo.unsafe  # (int) -> tuple[int, int]

foo.unsafe(5)
```

### Утилиты `is_success` и `is_failure`

Библиотека содержит утилиты `is_success` и `is_failure` для удобства работы и избежания проверок

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

Сами они являются `TypeGuard` проверкой `isinstance`.

### Паттер-матчинг

Весь потенциал подхода раскрывается именно при использование в связке с `match case` [конструкцией](https://peps.python.org/pep-0636/):

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

По коду видно что исключение `KeyError` не обрабатывается и это заметит тайп-чекер
([pyright](https://github.com/microsoft/pyright) или [mypy](https://github.com/python/mypy)),
указав в коде что `KeyError` ожидается обработать – ошибка `reportMatchNotExhaustive`.

Ее можно решить добавив ее обработки или пропустив объединив обработку или передав выше:

```python
match foo():
    case Success(value=int() as value):
        print(f"It's int {value=}")
    case Success(value=str() as value):
        print(f"It's str {value=}")
    case Failure(error=ValueError()):
        print("Catch ValueError")
    case Failure(error as error):
        raise error
```

## Асинхронность

Для декорирования корутин нужно использовать отдельный декоратор – `@async_safe`

```python
from safe import async_safe


@async_safe @ ValueError
async def foo(a: int) -> str: ...


foo # (int) -> Coroutine[Any, Any, Success[str] | Failure[str, ValueError]]
```
