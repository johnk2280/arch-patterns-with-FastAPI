from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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

    response = await async_client.post('/batches', json=data)

    assert response.status_code == 201
    assert response.json()['reference'] == 'in-stock-batch'
