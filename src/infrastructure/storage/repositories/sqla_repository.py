from collections.abc import Sequence
from functools import reduce
from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy import insert
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain import Batch
from domain import DomainModel
from domain.models import Product
from service_layer.ports import AbstractRepository

M = TypeVar("M", bound=DomainModel)


class AsyncSQLARepository(AbstractRepository[M], Generic[M]):

    model_class: type[M]
    relationships: Sequence[str]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: dict[str, Any]) -> M:
        return (await self._create([data])).scalar_one()

    async def add_many(self, data: Sequence[dict[str, Any]]) -> Sequence[M]:
        return (await self._create(data)).scalars().all()

    async def _create(self, data: Sequence[dict[str, Any]]) -> Result[tuple[M]]:
        return await self.session.execute(
            insert(self.model_class).returning(self.model_class),
            data,
        )

    async def get(self, filters: dict[str, Any]) -> M:
        return (await self._read(filters)).scalar_one()

    async def get_many(
        self,
        filters: dict[str, Any] | None = None,
    ) -> Sequence[M]:
        if filters is None:
            filters = {}

        return (await self._read(filters)).scalars().all()

    async def _read(self, filters: dict[str, Any]) -> Result[tuple[M]]:
        stmt = select(self.model_class).filter_by(**filters)
        return await self.session.execute(self._add_relationships(stmt))

    def _add_relationships(
        self,
        expression: Select[tuple[M]],
    ) -> Select[tuple[M]]:
        return reduce(
            lambda stmt, rel_name: stmt.options(
                selectinload(getattr(self.model_class, rel_name)),
            ),
            self.relationships,
            expression,
        )

    async def _update(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _delete(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class AsyncBatchRepo(AsyncSQLARepository[Batch]):

    model_class = Batch
    relationships = ('_allocations',)


class AsyncProductRepo(AsyncSQLARepository):
    model_class = Product
    relationships = ('batches',)

