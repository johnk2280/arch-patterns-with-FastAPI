import httpx
import pytest

import config


@pytest.mark.usefixtures('restart_api')
async def test_api_returns_allocation(add_stock):
    sku, other_sku = random_sku(), random_sku('other')
    early_batch = random_batchref(1)
    later_batch = random_batchref(2)
    other_batch = random_batchref(3)
    add_stock([
        (later_batch, sku, 100, '2011-01-02'),
        (early_batch, sku, 100, '2011-01-01'),
        (other_batch, other_sku, 100, None),
    ])

    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()

    async with httpx.AsyncClient() as client:
        response = await client.post(f'{url}/allocate', json=data)

    assert response.status_code == 200
    assert response.json()['batch_ref'] == early_batch

