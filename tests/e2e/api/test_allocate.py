import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.storage.repositories import AsyncProductRepo


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
    product_repo = AsyncProductRepo(async_session)

    await product_repo.add_many(
        [
            dict(sku=sku),
            dict(sku=other_sku),
        ],
    )
    await async_session.commit()
    await async_session.close()

    await async_client.post(
        '/batches',
        json={
            'reference': later_batch,
            'sku': sku,
            '_purchased_quantity': 100,
            'eta': '2011-01-02',
        },
    )
    await async_client.post(
        '/batches',
        json={
            'reference': early_batch,
            'sku': sku,
            '_purchased_quantity': 100,
            'eta': '2011-01-01',
        },
    )
    await async_client.post(
        '/batches',
        json={
            'reference': other_batch,
            'sku': other_sku,
            '_purchased_quantity': 100,
            'eta': None,
        },
    )
    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}

    response = await async_client.post('/allocate', json=data)

    assert response.status_code == 201
    assert response.json() == {'reference': early_batch}


async def test_allocations_are_persisted(
    async_session: AsyncSession,
    async_client: AsyncClient,
):
    sku = random_sku()
    early_batch = random_batchref('1')
    later_batch = random_batchref('2')
    product_repo = AsyncProductRepo(async_session)

    await product_repo.add_many(
        [
            dict(sku=sku),
        ],
    )
    await async_session.commit()
    await async_session.close()

    await async_client.post(
        '/batches',
        json={
            'reference': later_batch,
            'sku': sku,
            '_purchased_quantity': 100,
            'eta': '2011-01-02',
        },
    )
    await async_client.post(
        '/batches',
        json={
            'reference': early_batch,
            'sku': sku,
            '_purchased_quantity': 100,
            'eta': '2011-01-01',
        },
    )
    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 100}

    response = await async_client.post('/allocate', json=data)

    assert response.status_code == 201
    assert response.json() == {'reference': early_batch}

    data_2 = {'order_id': random_order_id(), 'sku': sku, 'qty': 10}
    response_2 = await async_client.post('/allocate', json=data_2)

    assert response_2.status_code == 201

    assert response_2.json() == {'reference': later_batch}


async def test_400_message_for_out_of_stock(
    async_session: AsyncSession,
    async_client: AsyncClient,
):
    sku = random_sku()

    early_batch = random_batchref('1')

    product_repo = AsyncProductRepo(async_session)

    await product_repo.add_many([dict(sku=sku)])

    await async_session.commit()

    await async_session.close()

    await async_client.post(
        '/batches',
        json={
            'reference': early_batch,
            'sku': sku,
            '_purchased_quantity': 10,
            'eta': '2011-01-01',
        },
    )

    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 100}

    response = await async_client.post('/allocate', json=data)

    assert response.status_code == 413
    assert response.json() == {
        'message': f'Артикула {sku} нет в наличии',
    }


async def test_404_message_for_invalid_sku(
    async_client: AsyncClient,
):
    sku = random_sku()

    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 100}

    response = await async_client.post('/allocate', json=data)

    assert response.status_code == 404
    assert response.json() == {
        'message': f'Недопустимый артикул: {sku}',
    }
