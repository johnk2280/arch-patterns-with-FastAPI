from domain import Batch
from service_layer.services import add_batch
from tests.fake_repository import FakeRepository
from tests.fake_session import FakeSession


async def test_add_batch():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)

    batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        repo,
        session,
    )

    assert batch is not None
    assert batch.reference == 'in-stock-batch'
    assert session.committed
