import asyncio  # noqa

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from infrastructure.adapters.repositories import AsyncBatchRepository


async def test_async_batch_repository_can_save_a_batch(
    async_session: AsyncSession,
):
    batch = Batch('batch-1', 'RUSTY-SOAPDISH', 100)
    repo = AsyncBatchRepository(async_session)
    await repo.add(batch)

    rows = (await async_session.execute(select(Batch))).scalars().all()

    assert len(rows) == 1
    assert rows == [batch]
