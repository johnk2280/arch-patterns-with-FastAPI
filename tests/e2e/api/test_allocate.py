import uuid
from datetime import datetime

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.adapters.repositories import AsyncBatchRepo


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_order_id(name=""):
    return f"order-{name}-{random_suffix()}"


async def test_api_returns_allocation(
    async_session: AsyncSession,
    async_client: AsyncClient,
):
    sku, other_sku = random_sku(), random_sku('other')
    early_batch = random_batchref('1')
    later_batch = random_batchref('2')
    other_batch = random_batchref('3')

    repo = AsyncBatchRepo(async_session)
    await repo.add_many(
        [
            {
                'reference': later_batch,
                'sku': sku,
                '_purchased_quantity': 100,
                'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
            },
            {
                'reference': early_batch,
                'sku': sku,
                '_purchased_quantity': 100,
                'eta': datetime.strptime('2011-01-01', '%Y-%m-%d')
            },
            {
                'reference': other_batch,
                'sku': other_sku,
                '_purchased_quantity': 100,
                'eta': None,
            },
        ]
    )
    await async_session.commit()

    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}
    response = await async_client.post('/allocate', json=data)

    assert response.status_code == 201
    assert response.json() == {'reference': early_batch}


# async def test_allocations_are_persisted(
#     async_session: AsyncSession,
#     async_client: AsyncClient,
# ):
#     sku, other_sku = random_sku(), random_sku('other')
#     early_batch = random_batchref('1')
#     later_batch = random_batchref('2')
#     other_batch = random_batchref('3')
#
#     repo = AsyncBatchRepo(async_session)
#     await repo.add_many(
#         [
#             {
#                 'reference': later_batch,
#                 'sku': sku,
#                 '_purchased_quantity': 100,
#                 'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
#             },
#             {
#                 'reference': early_batch,
#                 'sku': sku,
#                 '_purchased_quantity': 100,
#                 'eta': datetime.strptime('2011-01-01', '%Y-%m-%d')
#             },
#         ]
#     )
#     await async_session.commit()
#
#     data = {'order_id': random_order_id(), 'sku': sku, 'qty': 100}
#     response = await async_client.post('/allocate', json=data)
#
#     assert response.status_code == 201
#     assert response.json() == early_batch
