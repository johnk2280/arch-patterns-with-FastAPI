from collections.abc import Sequence
from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy import insert
from sqlalchemy import Result
from sqlalchemy import select
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
        return (await self._create(data)).scalar_one()

    async def _create(self, data: dict[str, Any]) -> Result[tuple[M]]:
        return await self.session.execute(
            insert(self.model_class)
            .values(**data)
            .returning(self.model_class)
        )

    async def get(self, filters: dict[str, Any]) -> M:
        return (await self._read(filters)).scalar_one()

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
    ) -> Sequence[M]:
        if filters is None:
            filters = {}

        raise NotImplementedError

    async def _read(self, filters: dict[str, Any]) -> Result[tuple[M]]:
        return await self.session.execute(
            select(self.model_class)
            .filter_by(**filters)
        )

    async def _update(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _delete(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class AsyncBatchRepo(AsyncSQLARepository[Batch]):
    model_class = Batch
