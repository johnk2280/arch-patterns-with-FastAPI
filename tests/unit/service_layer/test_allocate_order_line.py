from datetime import date
from datetime import datetime
from datetime import timedelta

import pytest

from domain import Batch
from domain import OrderLine
from domain.exeptions import OutOfStockError
from service_layer.exceptions import InvalidSkuError
from service_layer.services import add_batch
from service_layer.services import allocate_line
from tests.fake_repository import FakeRepository
from tests.fake_session import FakeSession
from tests.fake_unit_of_work import FakeUOW

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TOMORROW + timedelta(days=10)


async def test_prefers_current_stock_batches_to_shipments():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    in_stock_batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        uow
    )
    shipment_batch = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        uow
    )
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    await allocate_line(line, uow)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


async def test_prefers_earlier_batches():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    earliest = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TODAY,
        },
        uow,
    )
    medium = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        uow,
    )
    latest = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': LATER,
        },
        uow,
    )

    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    await allocate_line(line, uow)

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


async def test_returns_allocated_batch_ref():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    in_stock_batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        uow,
    )
    await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        uow,
    )
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocation = await allocate_line(line, uow)

    assert allocation.reference == in_stock_batch.reference


async def test_raises_out_of_stock_exception_if_cannot_allocate():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'SMALL_FORK',
            '_purchased_quantity': 25,
            'eta': TODAY,
        },
        uow,
    )
    line = OrderLine('oref', 'SMALL_FORK', 25)

    await allocate_line(line, uow)

    with pytest.raises(OutOfStockError, match='SMALL_FORK'):
        line_2 = OrderLine('order-02', 'SMALL_FORK', 25)
        await allocate_line(line_2, uow)


async def test_return_allocations():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    batch = await add_batch(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        },
        uow,
    )

    result = await allocate_line(line, uow)

    assert result == batch


async def test_error_for_invalid_sku():
    repo = FakeRepository[Batch](Batch)
    uow = FakeUOW()
    uow.batches = repo
    line = OrderLine('oref', 'RED-CHAIR', 10)
    await add_batch(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        },
        uow,
    )

    with pytest.raises(InvalidSkuError):
        await allocate_line(line, uow)
