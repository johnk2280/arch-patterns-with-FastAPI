import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import clear_mappers

from config import get_settings
from infrastructure.storage.orm import mapper_registry
from infrastructure.entrypoints.rest_api.app import app

settings = get_settings()


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def async_engine() -> AsyncEngine:

    assert settings.ENVIRONMENT == 'test'

    DATABASE_PARAMS = dict(
        poolclass=NullPool,
    )
    engine = create_async_engine(settings.database_url, **DATABASE_PARAMS)
    return engine


@pytest.fixture(scope='session', autouse=True)
async def async_db_engine(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncEngine, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield async_engine

    clear_mappers()
    async with async_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest.fixture(scope='function', autouse=True)
async def async_session(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(
        bind=async_db_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session

        for table in mapper_registry.metadata.sorted_tables:
            await session.execute(
                text(f'TRUNCATE {table.name} CASCADE;'),
            )
            await session.commit()


@pytest.fixture(scope='function')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://testserver') as ac:
        yield ac
