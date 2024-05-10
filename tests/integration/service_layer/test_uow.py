from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain import OrderLine
from domain.models import Product
from infrastructure.storage.repositories import AsyncBatchRepo
from service_layer.uow import BatchUOW


async def test_uow_can_retrieve_a_batch_allocate_to_it(
    async_session: AsyncSession,
):
    await async_session.execute(
        insert(Product)
        .values(
            [
                dict(sku='HIPSTER-WORKBENCH'),
            ],
        ),
    )
    repo = AsyncBatchRepo(async_session)
    await repo.add(
            {
                'reference': 'batch-1',
                'sku': 'HIPSTER-WORKBENCH',
                '_purchased_quantity': 100,
                'eta': None,
                },
            )
    await async_session.commit()
    
    uow = BatchUOW()
    async with uow:
        batch = await uow.batches.get({'reference': 'batch-1'})
        line = OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        await uow.commit()
    
    expected = await repo.get({'id': batch.id})

    assert expected._allocations == {line}
    assert expected.available_quantity == 90
