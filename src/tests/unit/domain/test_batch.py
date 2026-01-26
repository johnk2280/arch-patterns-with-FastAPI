from datetime import UTC
from datetime import datetime

import pytest

from domain.models import Batch


def test_allocating_order_line_to_batch_success() -> None:
    batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=datetime.now(UTC))
    line = OrderLine('order-ref', 'SMALL-TABLE', 2)

    batch.allocate(line)

    batch.avaliable_quantity == 18


def test_allocating_order_line_to_batch_failed() -> None:
    batch = Batch('batch-001', 'SMALL-TABLE', qty=2, eta=date.today())
    line = OrderLine('order-ref', 'SMALL-TABLE', 21)

    with pytest.raises(OutOfStock):
        batch.allocate(line)
