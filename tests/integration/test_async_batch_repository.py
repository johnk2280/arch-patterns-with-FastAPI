import asyncio  # noqa

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from infrastructure.adapters.repositories import AsyncBatchRepository


# Для проверки подключения pytest_asyncio
async def my_coroutine() -> float:
    await asyncio.sleep(0.1)
    return 2.71828182845


@pytest.mark.asyncio
async def test_my_coroutine() -> None:
    assert 2 < await my_coroutine() < 3


@pytest.mark.asyncio
async def test_async_batch_repository_can_save_a_batch(
    async_session: AsyncSession,
):
    batch = Batch('batch-1', 'RUSTY-SOAPDISH', 100)
    repo = AsyncBatchRepository(async_session)
    await repo.aadd(batch)

    stmt = select(Batch)
    rows = await async_session.execute(stmt)

    assert len(rows.scalars()) == 1
    assert rows == [batch]

