from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

from domain.model import Batch

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def get(self, reference: str) -> T:
        pass

    @abstractmethod
    def list(self) -> list[T]:
        pass


class SQLAlchemyRepository(AbstractRepository[Batch]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> list[Batch]:
        return self.session.query(Batch).all()


class FakeRepository(AbstractRepository[Batch]):
    def __init__(self, batches: list[Batch]) -> None:
        self._batches = set(batches)

    def add(self, item: Batch) -> None:
        self._batches.add(item)

    def get(self, reference: str) -> Batch:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)
