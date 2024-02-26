import asyncio

from config import get_settings

settings = get_settings()


def test_first():
    assert 1 + 1 == 2


def test_environ():
    assert settings.ENVIRONMENT == 'test'
    assert (settings.database_url ==
            'postgresql+asyncpg://postgres:postgres@localhost:5432'
            '/test_sphr_karma')


async def test_some_asyncio_code():
    res = await asyncio.sleep(1)
    assert res is None
