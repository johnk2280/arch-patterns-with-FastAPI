from datetime import datetime

from domain import Batch
from domain import OrderLine
from tests.fake_repository import FakeRepository


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

    result = allocation(line, repo, fake_session)



