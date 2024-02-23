from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.model import Batch
from service_layer.ports import AbstractRepository


# TODO: Доработать репозиторий
class BatchRepository(AbstractRepository[Batch, AsyncSession]):

    model_class = Batch

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    async def get(self, reference: str) -> Batch:
        stmt = select(Batch).filter_by(reference=reference)
        # return self.session.query(Batch).filter_by(reference=reference).one()
        result = await self.session.execute(stmt)
        return result.scalar()

    def list(self) -> list[Batch]:
        stmt = select(Batch)
        # TODO: проверить
        # return self.session.query(Batch).all()
        return self.session.execute(stmt).all()


class FakeRepository(AbstractRepository[Batch, Any]):

    def __init__(self, batches: list[Batch]) -> None:
        super().__init__('')
        self._batches = set(batches)

    def add(self, item: Batch) -> None:
        self._batches.add(item)

    def get(self, reference: str) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)
