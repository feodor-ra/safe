import pytest

from src.safe import Success, async_safe, safe


class Class:
    @safe
    def testing_method(self, a: int) -> str:  # noqa: PLR6301
        return f"{a}"

    @async_safe
    async def testings_coroutine(self, a: int) -> str:  # noqa: PLR6301
        return f"{a}"


@pytest.fixture
def cls() -> Class:
    return Class()


def test_decorated_method(cls: Class):
    assert cls.testing_method(1) == Success("1")


@pytest.mark.asyncio
async def test_decorated_coroutine(cls: Class):
    assert await cls.testings_coroutine(1) == Success("1")
