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


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch-001', 'SMALL_FORK', 25, TODAY)
    line = OrderLine('order-01', 'SMALL_FORK', 25)

    allocate(line, [batch])

    with pytest.raises(OutOfStockError, match='SMALL_FORK'):
        line_2 = OrderLine('order-02', 'SMALL_FORK', 25)
        allocate(line_2, [batch])
