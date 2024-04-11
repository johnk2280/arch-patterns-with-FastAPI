from typing import Any

from domain import Batch
from service_layer.ports import AbstractUOW
from tests.fake_repository import FakeRepository


class FakeUOW(AbstractUOW):
    batches: FakeRepository[Batch]

    def __init__(self) -> None:
        self.is_committed = False

    async def __aenter__(self) -> Any:
        pass

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    async def commit(self) -> None:
        self.is_committed = True

    async def rollback(self) -> None:
        pass
