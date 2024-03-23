from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from domain import Batch
from domain import DomainModel
from service_layer.ports import AbstractRepository

M = TypeVar("M", bound=DomainModel)


class AsyncSQLARepository(AbstractRepository[M], Generic[M]):

    model_class: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: dict[str, Any]) -> M:
        raise NotImplementedError

    async def _create(self, data: dict[str, Any]) -> M:
        raise NotImplementedError

    async def get(self, filters: dict[str, Any]) -> M:
        raise NotImplementedError

    async def get_many(self, filters: dict[str, Any]) -> list[M]:
        raise NotImplementedError

    async def _read(self, filters: dict[str, Any]) -> Any:
        raise NotImplementedError

    async def _update(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _delete(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class AsyncBatchRepo(AsyncSQLARepository[Batch]):
    model_class = Batch
