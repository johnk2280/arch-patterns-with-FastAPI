from domain import Batch
from service_layer.services import add_batch
from tests.fake_repository import FakeRepository
from tests.fake_unit_of_work import FakeUOW


async def test_add_batch():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo

    batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        uow,
    )

    assert batch is not None
    assert batch.reference == 'in-stock-batch'
