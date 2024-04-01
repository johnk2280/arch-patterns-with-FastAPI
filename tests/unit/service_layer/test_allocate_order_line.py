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

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
LATER = TOMORROW + timedelta(days=10)


async def test_prefers_current_stock_batches_to_shipments():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    in_stock_batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        repo,
        session,
    )
    shipment_batch = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        repo,
        session,
    )
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    await allocate_line(line, repo, session)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


async def test_prefers_earlier_batches():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    earliest = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TODAY,
        },
        repo,
        session
    )
    medium = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        repo,
        session
    )
    latest = await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': LATER,
        },
        repo,
        session
    )

    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    await allocate_line(line, repo, session)

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


async def test_returns_allocated_batch_ref():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    in_stock_batch = await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': None,
        },
        repo,
        session,
    )
    await add_batch(
        {
            'reference': 'shipment-batch',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 100,
            'eta': TOMORROW,
        },
        repo,
        session,
    )
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocation = await allocate_line(line, repo, session)

    assert allocation.reference == in_stock_batch.reference


async def test_raises_out_of_stock_exception_if_cannot_allocate():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    await add_batch(
        {
            'reference': 'in-stock-batch',
            'sku': 'SMALL_FORK',
            '_purchased_quantity': 25,
            'eta': TODAY,
        },
        repo,
        session,
    )
    line = OrderLine('oref', 'SMALL_FORK', 25)

    await allocate_line(line, repo, session)

    with pytest.raises(OutOfStockError, match='SMALL_FORK'):
        line_2 = OrderLine('order-02', 'SMALL_FORK', 25)
        await allocate_line(line_2, repo, session)


async def test_return_allocations():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    line = OrderLine('oref', 'RETRO-CLOCK', 10)
    batch = await add_batch(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        },
        repo,
        session,
    )
    fake_session = FakeSession()

    result = await allocate_line(line, repo, fake_session)

    assert result == batch
    assert fake_session.committed


async def test_error_for_invalid_sku():
    session = FakeSession()
    repo = FakeRepository[Batch](Batch)
    line = OrderLine('oref', 'RED-CHAIR', 10)
    await add_batch(
        {
            'reference': 'batch-1',
            'sku': 'RETRO-CLOCK',
            '_purchased_quantity': 10,
            'eta': datetime.strptime('2011-01-02', '%Y-%m-%d')
        },
        repo,
        session,
    )
    fake_session = FakeSession()

    with pytest.raises(InvalidSkuError):
        await allocate_line(line, repo, fake_session)
