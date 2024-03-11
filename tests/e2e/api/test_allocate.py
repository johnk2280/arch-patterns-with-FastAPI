import pytest


@pytest.mark.usefixtures('restart_api')
async def test_api_returns_allocation(add_stock):
    ...