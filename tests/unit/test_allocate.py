from datetime import date
from datetime import timedelta

import pytest

from domain.model import allocate
from domain.models import Batch
from domain.models import OrderLine

# from domain.model import Batch
# from domain.model import OrderLine
# from domain.model import OutOfStockError

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TOMORROW + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    batch = Batch()

    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, TOMORROW)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch('in-stock-batch', 'RETRO-CLOCK', 100, TODAY)
    medium = Batch('shipment-batch', 'RETRO-CLOCK', 100, TOMORROW)
    latest = Batch('shipment-batch', 'RETRO-CLOCK', 100, LATER)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    allocate(line, [earliest, medium, latest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, TOMORROW)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch-001', 'SMALL_FORK', 25, TODAY)
    line = OrderLine('order-01', 'SMALL_FORK', 25)
    allocate(line, [batch])

    with pytest.raises(OutOfStockError, match='SMALL_FORK'):
        line_2 = OrderLine('order-02', 'SMALL_FORK', 25)
        allocate(line_2, [batch])
