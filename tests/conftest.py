from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from src.infrastructure.adapters.orm import mapper_registry
from src.infrastructure.adapters.orm import start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db, future=True)()
    clear_mappers()


@pytest_asyncio.fixture
def async_engine() -> AsyncEngine:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    return engine


@pytest_asyncio.fixture
async def create(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        conn.run_sync(mapper_registry.metadata.create_all)
        yield conn
        conn.run_sync(mapper_registry.metadata.drop_all)

    # async with async_engine.begin() as conn:
    #     conn.run_sync(mapper_registry.metadata.drop_all)
    # mapper_registry.metadata.create_all(engine)
    # return engine


@pytest_asyncio.fixture
async def async_session(
    async_engine: AsyncEngine,
    create: AsyncGenerator,
) -> AsyncGenerator[AsyncSession, None]:
    # start_mappers()
    async with AsyncSession(bind=async_engine) as session:
        yield session

