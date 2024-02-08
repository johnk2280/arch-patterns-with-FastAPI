from sqlalchemy.orm import Session

from domain.model import Batch
from service_layer.ports import AbstractRepository


class BatchRepository(AbstractRepository[Batch, Session]):

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> list[Batch]:
        return self.session.query(Batch).all()


class FakeRepository(AbstractRepository[Batch]):

    def __init__(self, batches: list[Batch]) -> None:
        super().__init__('')
        self._batches = set(batches)

    def add(self, item: Batch) -> None:
        self._batches.add(item)

    def get(self, reference: str) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)
