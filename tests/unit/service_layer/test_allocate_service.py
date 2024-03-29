from datetime import datetime

import pytest

from domain import Batch
from domain import OrderLine
from service_layer.exceptions import InvalidSkuError
from service_layer.services import allocate_line
from tests.fake_repository import FakeRepository
from tests.fake_session import FakeSession


async def test_return_allocations():
    repo = FakeRepository[Batch](Batch)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    batch = await repo.add(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        }
    )
    fake_session = FakeSession()

    result = await allocate_line(line, repo, fake_session)

    assert result == batch
    assert fake_session.committed


async def test_error_for_invalid_sku():
    repo = FakeRepository[Batch](Batch)
    line = OrderLine('oref', 'RED-CHAIR', 10)
    batch = await repo.add(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        }
    )
    fake_session = FakeSession()

    with pytest.raises(InvalidSkuError):
        await allocate_line(line, repo, fake_session)






