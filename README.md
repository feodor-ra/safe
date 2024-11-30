# safe-returns

A decorator for converting the output type of a function into an algebraic data type,
representing the function’s result and its possible exception types.
This helps in tracking exception types and improves type-checker hints.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/safe-returns)
![PyPI - Status](https://img.shields.io/pypi/status/safe-returns)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/safe-returns)
![PyPI - Downloads](https://img.shields.io/pypi/dm/safe-returns)

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/feodor-ra/safe-returns/blob/master/.pre-commit-config.yaml)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/feodor-ra/safe-returns/releases)

![Test results](https://github.com/feodor-ra/safe-returns/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/feodor-ra/safe-returns/badge.svg?branch=master)](https://coveralls.io/github/feodor-ra/safe-returns?branch=master)

[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://feodor-ra.github.io/safe-returns/)
![GitHub License](https://img.shields.io/github/license/feodor-ra/safe-returns)
![GitHub Release](https://img.shields.io/github/v/release/feodor-ra/safe-returns)
![GitHub Repo stars](https://img.shields.io/github/stars/feodor-ra/safe-returns)

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

- [Russian](https://feodor-ra.github.io/safe-returns/ru/)
- [English](https://feodor-ra.github.io/safe-returns/en/)
