from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

M = TypeVar('M')  # subtype of DeclarativeBase
S = TypeVar('S')  # any session


class AbstractRepository(ABC, Generic[M, S]):

    model_class: type[M]

    def __init__(self, session: S) -> None:
        if not self.model_class:
            raise ValueError(
                'Can not initiate the class without model_class attribute',
            )

        self.session = session

    @abstractmethod
    def add(self, item: M) -> None:
        pass

    @abstractmethod
    def get(self, reference: str) -> M:
        pass

    @abstractmethod
    def list(self) -> list[M]:
        pass
