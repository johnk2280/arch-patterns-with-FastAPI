from datetime import date

from ch_01.model import Batch
from ch_01.model import OrderLine


def test_allocate_to_a_batch_reduces_the_available_quantity():
    batch = Batch(
        'batch-001',
        'SMALL_TABLE',
        qty=20,
        eta=date.today(),
    )
    line = OrderLine('order-ref', 'SMALL_TABLE', 2)
    batch.allocate(line)

    assert batch.available_quantity == 18

