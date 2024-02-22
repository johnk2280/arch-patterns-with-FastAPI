from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.model import Batch
from service_layer.ports import AbstractRepository


# TODO: Доработать репозиторий
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
        return self.session.query(Batch).all()


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
