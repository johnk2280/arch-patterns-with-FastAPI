from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import Batch
from domain.models import OrderLine
from infrastructure.adapters.orm import allocations
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


async def test_async_batch_repository_can_retrieve_a_batch_with_allocation(
    async_session: AsyncSession,
):
    order_line = (await async_session.execute(
        insert(OrderLine)
        .values(
            [
                {
                    'order_id': 'order-1',
                    'sku': 'RED-CHAIR',
                    'qty': 12,
                },
            ]
        )
        .returning(OrderLine),
    )).scalar()

    batch = (await async_session.execute(
        insert(Batch)
        .values(
            [
                {
                    'reference': 'batch-1',
                    'sku': 'GENERIC-SOFA',
                    '_purchased_quantity': 100,
                },
            ],
        )
        .returning(Batch),
    )).scalar()
    await async_session.execute(
        insert(allocations)
        .values(
            [
                {
                    'order_line_id': order_line.id,
                    'batch_id': batch.id,
                },
            ],
        )
    )

    repo = AsyncBatchRepository(async_session)
    retrieved = await repo.get('batch-1')

    expected = Batch('batch-1', 'GENERIC-SOFA', 100)

    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine(order_id='order-1', sku='RED-CHAIR', qty=12, id=1),
    }


async def test_async_batch_repository_can_retrieve_batches_with_allocations(
    async_session: AsyncSession,
):
    order_line = (await async_session.execute(
        insert(OrderLine)
        .values(
            [
                {
                    'order_id': 'order-1',
                    'sku': 'RED-CHAIR',
                    'qty': 12,
                },
            ]
        )
        .returning(OrderLine),
    )).scalar()

    batch = (await async_session.execute(
        insert(Batch)
        .values(
            [
                {
                    'reference': 'batch-1',
                    'sku': 'GENERIC-SOFA',
                    '_purchased_quantity': 100,
                },
            ],
        )
        .returning(Batch),
    )).scalar()
    await async_session.execute(
        insert(allocations)
        .values(
            [
                {
                    'order_line_id': order_line.id,
                    'batch_id': batch.id,
                },
            ],
        )
    )

    repo = AsyncBatchRepository(async_session)
    batches = await repo.get_all()

    expected = Batch('batch-1', 'GENERIC-SOFA', 100)
    expected._allocations.add(order_line)

    assert batches == [expected]
    assert batches[0]._allocations == expected._allocations
