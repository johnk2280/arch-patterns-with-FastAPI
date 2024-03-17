from typing import Any
from typing import Generic
from typing import TypeVar

from domain.models import Batch
from domain.models import DomainModel
from service_layer.ports import AbstractRepository

T = TypeVar('T', bound=DomainModel)


class FakeRepository(AbstractRepository, Generic[T]):

    def __init__(self, items: list[T]) -> None:
        self._items = set[T](items)

    def _create(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def _read(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def _update(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def _delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def add(self, item: Batch) -> None:
        raise NotImplementedError

    def get(self, reference: str) -> Batch:
        raise NotImplementedError

    def list(self) -> list[Batch]:
        raise NotImplementedError
