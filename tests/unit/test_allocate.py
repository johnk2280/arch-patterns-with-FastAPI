from datetime import date
from datetime import timedelta

import pytest

from domain.models import allocate

from domain.models import Batch
from domain.models import OrderLine
from domain.exeptions import OutOfStockError

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TOMORROW + timedelta(days=10)


# TODO: Переместить все тесты (модели доменной области) в тесты сервисного слоя
def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, TOMORROW)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation.reference == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch-001', 'SMALL_FORK', 25, TODAY)
    line = OrderLine('order-01', 'SMALL_FORK', 25)

    allocate(line, [batch])

    with pytest.raises(OutOfStockError, match='SMALL_FORK'):
        line_2 = OrderLine('order-02', 'SMALL_FORK', 25)
        allocate(line_2, [batch])
