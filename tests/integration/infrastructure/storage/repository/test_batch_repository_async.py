from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import Batch
from domain.models import OrderLine
from domain.models import Product
from infrastructure.storage.orm import allocations
from infrastructure.storage.repositories import AsyncBatchRepo


async def test_async_batch_repository_can_save_a_batch(
    async_session: AsyncSession,
):
    batch_data = {
        'reference': 'batch-1',
        'sku': 'RUSTY-SOAPDISH',
        '_purchased_quantity': 100,
    }
    await async_session.execute(
        insert(Product)
        .values(
            [
                dict(sku='RUSTY-SOAPDISH'),
            ],
        ),
    )
    await async_session.commit()
    await async_session.close()
    repo = AsyncBatchRepo(async_session)

    res = await repo.add(batch_data)

    rows = (await async_session.execute(select(Batch))).scalars().all()

    assert res.reference == batch_data['reference']
    assert len(rows) == 1
    assert rows == [Batch(**batch_data)]


async def test_async_batch_repository_can_save_a_batch_collection(
    async_session: AsyncSession,
):
    batch_data = [
        {
            'reference': 'batch-1',
            'sku': 'RUSTY-SOAPDISH',
            '_purchased_quantity': 100,
        },
        {
            'reference': 'batch-2',
            'sku': 'RED-CHAIR',
            '_purchased_quantity': 20,
        },
    ]
    await async_session.execute(
        insert(Product)
        .values(
            [
                dict(sku='RUSTY-SOAPDISH'),
                dict(sku='RED-CHAIR'),
            ],
        ),
    )
    await async_session.commit()
    await async_session.close()
    repo = AsyncBatchRepo(async_session)

    res = await repo.add_many(batch_data)

    rows = (await async_session.execute(select(Batch))).scalars().all()

    assert len(res) == 2
    assert len(rows) == 2
    assert res == rows
    assert rows == [Batch(**data) for data in batch_data]


async def test_async_batch_repository_can_retrieve_a_batch_with_allocation(
    async_session: AsyncSession,
):
    await async_session.execute(
        insert(Product)
        .values(
            [
                dict(sku='RED-CHAIR'),
                dict(sku='GENERIC-SOFA'),
            ],
        ),
    )
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

    expected = Batch('batch-1', 'GENERIC-SOFA', 100)
    repo = AsyncBatchRepo(async_session)

    retrieved = await repo.get({'reference': 'batch-1'})

    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine(
            order_id='order-1',
            sku='RED-CHAIR',
            qty=12,
            id=order_line.id
        ),
    }


async def test_async_batch_repository_can_retrieve_batches_with_allocations(
    async_session: AsyncSession,
):
    await async_session.execute(
        insert(Product)
        .values(
            [
                dict(sku='RED-CHAIR'),
                dict(sku='GENERIC-SOFA'),
            ],
        ),
    )
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
    repo = AsyncBatchRepo(async_session)

    batches = await repo.get_many()

    expected = Batch('batch-1', 'GENERIC-SOFA', 100)
    expected._allocations.add(order_line)

    assert batches == [expected]
    assert batches[0]._allocations == expected._allocations
