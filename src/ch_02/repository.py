from abc import ABC
from abc import abstractmethod

from sqlalchemy.orm import Session

from ch_02.model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        pass

    @abstractmethod
    def get(self, reference) -> Batch:
        pass


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()
