from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from domain.model import Batch
from service_layer.ports import AbstractRepository
from service_layer.ports.repository import AbstractAsyncRepository


class AsyncBatchRepository(AbstractAsyncRepository[Batch, AsyncSession]):

    model_class = Batch

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add(self, item: Batch) -> None:
        self.session.add(item)

    async def get(self, reference: str) -> Batch:
        return (
            await self.session.execute(
                select(Batch)
                .filter_by(reference=reference)
                .options(selectinload(Batch._allocations))
            )
        ).scalar()

    async def get_all(self) -> Sequence[Batch]:
        return (await self.session.execute(
            select(Batch)
            .options(selectinload(Batch._allocations))
        )).scalars().all()


class BatchRepository(AbstractRepository[Batch, Session]):

    model_class = Batch

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        stmt = select(Batch).filter_by(reference=reference)
        # return self.session.query(Batch).filter_by(reference=reference).one()
        return self.session.execute(stmt).scalar()

    def list(self) -> list[Batch]:
        # TODO: покрыть тестами
        stmt = select(Batch)
        # return self.session.query(Batch).all()
        return self.session.execute(stmt).all()


class FakeRepository(AbstractRepository[Batch, Any]):

    def __init__(self, batches: list[Batch]) -> None:
        super().__init__([])
        self._batches = set(batches)

    def add(self, item: Batch) -> None:
        self._batches.add(item)

    def get(self, reference: str) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)
