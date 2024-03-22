import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings

settings = get_settings()


def test_first():
    assert 1 + 1 == 2


def test_environ():
    assert settings.ENVIRONMENT == 'test'
    assert (settings.database_url ==
            'postgresql+asyncpg://postgres:postgres@localhost:5432'
            '/test_arch_patterns')


async def test_some_asyncio_code():
    res = await asyncio.sleep(1)
    assert res is None


async def test_some_async_session(async_session):
    assert isinstance(async_session, AsyncSession)


async def test_some_async_client(async_client):

    assert isinstance(async_client, AsyncClient)
    assert async_client.base_url == 'http://testserver'

