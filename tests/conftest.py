from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from infrastructure.adapters.orm.orm import mapper_registry
from infrastructure.adapters.orm.orm import start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def async_in_memory_db():
    engine = create_async_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db, future=True)()
    clear_mappers()


@pytest_asyncio.fixture
async def async_session(
    async_in_memory_db: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    start_mappers()
    async_session = async_sessionmaker(
        bind=async_in_memory_db,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session
        clear_mappers()
