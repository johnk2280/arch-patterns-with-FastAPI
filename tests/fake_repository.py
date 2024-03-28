from typing import Any
from typing import Generic
from typing import Sequence
from typing import TypeVar

from sqlalchemy.exc import NoResultFound

from domain import DomainModel
from service_layer.ports import AbstractRepository

M = TypeVar('M', bound=DomainModel)


class FakeRepository(AbstractRepository[M], Generic[M]):

    def __init__(self, model_class: type[M]) -> None:
        self._items: list[M] = []
        self._model_class = model_class

    async def add(self, data: dict[str, Any]) -> M:
        return await self._create(data)

    async def _create(self, data: dict[str, Any]) -> M:
        item: M = self._model_class(**data)
        self._items.append(item)
        return item

    async def get(self, data: dict[str, str | int]) -> M:
        [items] = data.items()
        try:
            return (await self._read(*items))[0]
        except IndexError:
            raise NoResultFound from None

    async def get_many(self, *args: Any, **kwargs: Any) -> Sequence[M]:
        return self._items

    async def _read(self, field: str, value: str | int) -> list[M]:
        return [el for el in self._items if getattr(el, field, None) == value]

    async def _update(self, *args: Any, **kwargs: Any) -> M:
        raise NotImplementedError

    async def _delete(self, *args: Any, **kwargs: Any) -> M:
        raise NotImplementedError
