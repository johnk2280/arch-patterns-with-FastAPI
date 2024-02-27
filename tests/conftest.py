import os
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy import create_engine
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from config import get_settings
from infrastructure.adapters.orm import mapper_registry
from infrastructure.adapters.orm import start_mappers

os.environ['ENVIRONMENT'] = 'test'

settings = get_settings()


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


