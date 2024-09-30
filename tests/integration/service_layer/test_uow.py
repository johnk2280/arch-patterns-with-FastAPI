from sqlalchemy.ext.asyncio import AsyncSession

from domain import OrderLine
from infrastructure.storage.repositories import AsyncBatchRepo
from infrastructure.storage.repositories.sqla_repository import AsyncProductRepo
from service_layer.uow import BatchUOW


async def test_uow_can_retrieve_a_batch_allocate_to_it(
    async_session: AsyncSession,
):
    product_repo = AsyncProductRepo(async_session)
    await product_repo.add_many(
            [
                dict(sku='HIPSTER-WORKBENCH'),
            ],
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
