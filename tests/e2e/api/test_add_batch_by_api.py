from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import Product
from infrastructure.storage.repositories import AsyncProductRepo


async def test_api_add_batch(
    async_session: AsyncSession,
    async_client: AsyncClient,
):
    data = {
        'reference': 'in-stock-batch',
        'sku': 'RETRO-CLOCK',
        '_purchased_quantity': 100,
        'eta': None,
    }
    product_repo = AsyncProductRepo(async_session)
    await product_repo.add(
        dict(
            sku=data['sku'],
        ),
    )
    await async_session.commit()
    await async_session.close()

    response = await async_client.post('/batches', json=data)

    assert response.status_code == 201
    assert response.json()['reference'] == 'in-stock-batch'
