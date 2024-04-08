from abc import ABC
from abc import abstractmethod
from typing import Any

from domain import Batch
from .abstract_repository import AbstractRepository


class AbstractUOW(ABC):

    batches: AbstractRepository[Batch]

    @abstractmethod
    async def __aenter__(self) -> Any:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
