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



